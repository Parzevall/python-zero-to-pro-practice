"""Async access to a fake exchange-rate service (everything stays in-process)."""
import asyncio
import functools
import logging
from collections import Counter
from typing import Awaitable, Callable, Iterable, Iterator, ParamSpec, TypeVar

from pipeline_models import Enriched, Order, PipelineError

log = logging.getLogger("orderflow.source")
P = ParamSpec("P")
R = TypeVar("R")


class TransientError(PipelineError):
    """A temporary failure: worth retrying."""


class UnknownCurrency(PipelineError):
    """A permanent failure: retrying cannot help."""


def retry(times: int) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    def decorate(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return await func(*args, **kwargs)
                except TransientError as e:
                    log.warning("attempt %d/%d failed: %s", attempt, times, e)
                    if attempt == times:
                        raise
            raise AssertionError("unreachable")
        return wrapper
    return decorate


class FakeRateSource:
    RATES = {"USD": 1.0, "EUR": 1.10, "GBP": 1.30}

    def __init__(self, flaky: dict[str, int] | None = None) -> None:
        self.flaky = flaky or {}          # currency -> how many calls fail first
        self.calls: Counter[str] = Counter()
        self.active = 0
        self.max_active = 0

    async def rate(self, currency: str) -> float:
        self.calls[currency] += 1
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        try:
            await asyncio.sleep(0)
            if self.calls[currency] <= self.flaky.get(currency, 0):
                raise TransientError(f"{currency} service busy")
            if currency not in self.RATES:
                raise UnknownCurrency(f"no rate for {currency}")
            return self.RATES[currency]
        finally:
            self.active -= 1


@retry(times=3)
async def fetch_rate(source: FakeRateSource, currency: str) -> float:
    return await source.rate(currency)


async def fetch_rates(currencies: Iterable[str], source: FakeRateSource,
                      limit: int = 2) -> dict[str, float | PipelineError]:
    """Fetch every distinct currency concurrently, at most `limit` at a time."""
    gate = asyncio.Semaphore(limit)

    async def one(code: str) -> float:
        async with gate:
            return await fetch_rate(source, code)

    codes = sorted(set(currencies))
    results = await asyncio.gather(*(one(c) for c in codes), return_exceptions=True)
    rates: dict[str, float | PipelineError] = {}
    for code, result in zip(codes, results):
        if isinstance(result, float | PipelineError):
            rates[code] = result
        else:
            raise result          # a real bug, not a pipeline failure
    return rates


def enrich(orders: Iterable[Order], rates: dict[str, float | PipelineError],
           skipped: list[Order] | None = None) -> Iterator[Enriched]:
    for order in orders:
        rate = rates.get(order.currency)
        if isinstance(rate, float):
            yield Enriched(order, round(order.total * rate, 2))
        else:
            log.warning("skipping order %d: %s", order.id, rate)
            if skipped is not None:
                skipped.append(order)
