import sys; sys.path.insert(0, "..")
from capstone import Capstone

cap = Capstone("NB32", title="Orderflow: an order-processing pipeline", intro="""
    The course finale. You will build **orderflow**, a small but real project of
    seven files: typed models and a streaming CSV reader, a plugin registry
    built from decorators, a context manager for output files, an async rate
    fetcher with retries (talking to a fake in-process service, so no network),
    a runner that wires everything together, a unittest suite and a `main.py`
    you can run like a real program. Everything from NB21 to NB31 is fair game,
    but only where it genuinely helps: a good design uses the right tool, not
    every tool.
""", story="""
    A small online shop exports its orders as a CSV file, and it is messy:
    bad numbers, missing names, negative quantities, and a currency nobody has
    a rate for. You are building **orderflow**, a package that streams the
    orders, converts every total to US dollars with rates fetched from a
    (fake, in-process) exchange service, runs the orders through pluggable
    steps, writes the survivors to a JSON-lines file and prints a report.
    The modules are flat files named `pipeline_*.py`. Some of them grow over
    several milestones: keep extending the same file, because each demo uses
    your latest version. Your code logs through the `logging` module; the demos
    configure it to print to the terminal.
""")

ORDERS = '''id,customer,sku,qty,price,currency
1001,ana,kb-01,2,45.50,USD
1002,Bo ,ms-02,1,19.99,EUR
1003,cy,kb-01,abc,45.50,USD
1004,dee,mn-03,1,210.00,GBP
1005,ana,ms-02,3,19.99,USD
1006,,kb-01,1,45.50,USD
1007,eli,hd-04,-2,89.00,USD
1008,bo,mn-03,2,210.00,EUR
1009,fay,kb-01,1,45.50,JPY
1010,ana,hd-04,1,89.00,USD
1011,gus,cb-05,1,4.50,USD
'''

MODELS = r'''
"""Typed models and the streaming reader for orderflow."""
import csv
import logging
from dataclasses import dataclass, field
from typing import Iterable, Iterator, TypedDict

log = logging.getLogger("orderflow.models")


class PipelineError(Exception):
    """Base class for every error orderflow raises on purpose."""


class BadRecord(PipelineError):
    def __init__(self, line: int, reason: str) -> None:
        super().__init__(f"line {line}: {reason}")
        self.line = line
        self.reason = reason


@dataclass(frozen=True, slots=True)
class Order:
    id: int
    customer: str
    sku: str
    qty: int
    price: float
    currency: str

    @property
    def total(self) -> float:
        return round(self.qty * self.price, 2)


@dataclass
class Enriched:
    order: Order
    usd_total: float
    tags: list[str] = field(default_factory=list)


class CustomerTotals(TypedDict):
    orders: int
    revenue: float


def parse_order(row: dict[str, str], line: int) -> Order:
    customer = (row["customer"] or "").strip().lower()
    if not customer:
        raise BadRecord(line, "missing customer")
    try:
        qty = int(row["qty"])
        price = float(row["price"])
        order_id = int(row["id"])
    except ValueError as e:
        raise BadRecord(line, f"bad number ({e})") from None
    if qty <= 0 or price <= 0:
        raise BadRecord(line, "qty and price must be positive")
    return Order(order_id, customer, row["sku"].strip().upper(), qty, price,
                 row["currency"].strip().upper())


def read_orders(lines: Iterable[str], rejects: list[BadRecord] | None = None) -> Iterator[Order]:
    """Yield one Order at a time; bad rows are logged and collected, never fatal."""
    reader = csv.DictReader(lines)
    for line, row in enumerate(reader, start=2):
        try:
            yield parse_order(row, line)
        except BadRecord as e:
            log.warning("rejected %s", e)
            if rejects is not None:
                rejects.append(e)
'''

REGISTRY = r'''
"""A tiny plugin system: steps register themselves with a decorator."""
import importlib
import logging
from typing import Callable, Iterable, Iterator

from pipeline_models import Enriched

log = logging.getLogger("orderflow.registry")

Step = Callable[[Enriched], Enriched | None]
_STEPS: dict[str, tuple[int, Step]] = {}


def step(name: str, *, order: int) -> Callable[[Step], Step]:
    """Register a function as a pipeline step; lower order runs first."""
    def register(func: Step) -> Step:
        if name in _STEPS:
            raise ValueError(f"step {name!r} is already registered")
        _STEPS[name] = (order, func)
        return func
    return register


def registered() -> list[str]:
    return [name for name, _ in sorted(_STEPS.items(), key=lambda kv: kv[1][0])]


def load_plugins(*module_names: str) -> None:
    for module_name in module_names:
        importlib.import_module(module_name)
        log.info("loaded plugin %s", module_name)


def run_steps(items: Iterable[Enriched], names: list[str] | None = None,
              dropped: list[Enriched] | None = None) -> Iterator[Enriched]:
    """Stream items through the chosen steps; a step returning None drops the item."""
    chosen = names if names is not None else registered()
    unknown = [n for n in chosen if n not in _STEPS]
    if unknown:
        raise KeyError(f"unknown steps: {unknown}")
    for item in items:
        current: Enriched | None = item
        for name in chosen:
            current = _STEPS[name][1](current)
            if current is None:
                log.info("step %s dropped order %s", name, item.order.id)
                if dropped is not None:
                    dropped.append(item)
                break
        else:
            yield item
'''

STEPS = r'''
"""Built-in steps. Importing this module registers them."""
from pipeline_models import Enriched
from pipeline_registry import step


@step("drop_tiny", order=10)
def drop_tiny(item: Enriched) -> Enriched | None:
    return None if item.usd_total < 20 else item


@step("tag_bulk", order=20)
def tag_bulk(item: Enriched) -> Enriched:
    if item.order.qty >= 3:
        item.tags.append("bulk")
    return item


@step("tag_big", order=30)
def tag_big(item: Enriched) -> Enriched:
    if item.usd_total >= 100:
        item.tags.append("big")
    return item
'''

RESOURCES = r'''
"""Resources: a safe output file and a stopwatch that takes a clock."""
import json
import logging
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Iterator

from pipeline_models import Enriched

log = logging.getLogger("orderflow.resources")


class FakeClock:
    """Moves forward by a fixed step on every call, so timings are repeatable."""

    def __init__(self, step: float = 0.5) -> None:
        self.now = 0.0
        self.step = step

    def __call__(self) -> float:
        self.now += self.step
        return self.now


class JsonlSink:
    """Writes one JSON object per line; a failed run leaves no half-written file."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.count = 0

    def __enter__(self) -> "JsonlSink":
        self._file = open(self.path, "w", encoding="utf-8")
        log.info("opened %s", self.path.name)
        return self

    def write(self, item: Enriched) -> None:
        self._file.write(json.dumps(asdict(item), sort_keys=True) + "\n")
        self.count += 1

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._file.close()
        if exc_type is None:
            log.info("closed %s with %d records", self.path.name, self.count)
        else:
            self.path.unlink()
            log.error("rolled back %s after %s", self.path.name, exc_type.__name__)
        return False


@contextmanager
def stopwatch(label: str, clock: Callable[[], float]) -> Iterator[None]:
    started = clock()
    try:
        yield
    finally:
        log.info("%s took %.2fs", label, clock() - started)


def read_jsonl(path: Path) -> Iterator[dict]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)
'''

SOURCE = r'''
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
'''

RUNNER = r'''
"""The runner: reads, enriches, filters, writes, and summarises."""
import logging
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from pipeline_models import BadRecord, CustomerTotals, Enriched, read_orders
from pipeline_registry import registered, run_steps
from pipeline_resources import JsonlSink, stopwatch
from pipeline_source import FakeRateSource, enrich, fetch_rates

log = logging.getLogger("orderflow.runner")


@dataclass
class Report:
    read: int = 0
    rejected: list[BadRecord] = field(default_factory=list)
    skipped_ids: list[int] = field(default_factory=list)
    dropped_ids: list[int] = field(default_factory=list)
    written: list[Enriched] = field(default_factory=list)

    def totals(self) -> dict[str, CustomerTotals]:
        out: dict[str, CustomerTotals] = {}
        for item in self.written:
            entry = out.setdefault(item.order.customer, {"orders": 0, "revenue": 0.0})
            entry["orders"] += 1
            entry["revenue"] = round(entry["revenue"] + item.usd_total, 2)
        return out

    def render(self) -> str:
        tags = Counter(tag for item in self.written for tag in item.tags)
        lines = ["=== ORDERFLOW REPORT ===",
                 f"Rows read: {self.read}, rejected: {len(self.rejected)}",
                 f"Skipped (no rate): {sorted(self.skipped_ids)}",
                 f"Dropped by steps: {sorted(self.dropped_ids)}",
                 f"Written: {len(self.written)}",
                 f"Tags: {dict(sorted(tags.items()))}",
                 "Revenue by customer (USD):"]
        for name, entry in sorted(self.totals().items()):
            lines.append(f"  {name:<4} {entry['orders']} order(s)  {entry['revenue']:>8.2f}")
        return "\n".join(lines)


async def run_pipeline(source_path: Path, output_path: Path, rate_source: FakeRateSource,
                       clock: Callable[[], float], steps: list[str] | None = None) -> Report:
    report = Report()
    with stopwatch("read", clock):
        with open(source_path, encoding="utf-8") as f:
            orders = list(read_orders(f, report.rejected))
    report.read = len(orders) + len(report.rejected)

    with stopwatch("rates", clock):
        rates = await fetch_rates([o.currency for o in orders], rate_source)

    skipped, dropped = [], []
    enriched = enrich(orders, rates, skipped)
    with JsonlSink(output_path) as sink:
        for item in run_steps(enriched, steps, dropped):
            sink.write(item)
            report.written.append(item)
    report.skipped_ids = [o.id for o in skipped]
    report.dropped_ids = [d.order.id for d in dropped]
    log.info("steps used: %s", steps or registered())
    return report
'''

TESTS = r'''
"""Unit tests for orderflow."""
import asyncio
import tempfile
import types
import unittest
from pathlib import Path

import pipeline_steps  # noqa: F401  (registers the built-in steps)
from pipeline_models import BadRecord, Enriched, Order, parse_order, read_orders
from pipeline_registry import registered, run_steps, step
from pipeline_resources import FakeClock, JsonlSink, read_jsonl
from pipeline_runner import run_pipeline
from pipeline_source import FakeRateSource, TransientError, fetch_rate, fetch_rates

ROW = {"id": "1", "customer": " Ana ", "sku": "kb-01", "qty": "2",
       "price": "10.50", "currency": "usd"}
CSV = ["id,customer,sku,qty,price,currency",
       "1,ana,kb-01,2,10.00,USD",
       "2,bo,kb-01,x,10.00,USD",
       "3,cy,kb-01,1,25.00,USD"]


class ParsingTests(unittest.TestCase):
    def test_valid_row_is_normalised(self):
        order = parse_order(ROW, 2)
        self.assertEqual((order.customer, order.sku, order.currency),
                         ("ana", "KB-01", "USD"))
        self.assertEqual(order.total, 21.0)

    def test_bad_rows_raise_with_line_number(self):
        with self.assertRaises(BadRecord) as caught:
            parse_order({**ROW, "qty": "-1"}, 7)
        self.assertEqual(caught.exception.line, 7)

    def test_reader_is_lazy_and_skips_bad_rows(self):
        rejects = []
        stream = read_orders(CSV, rejects)
        self.assertIsInstance(stream, types.GeneratorType)
        self.assertEqual([o.id for o in stream], [1, 3])
        self.assertEqual(len(rejects), 1)

    def test_orders_are_frozen(self):
        with self.assertRaises(AttributeError):
            parse_order(ROW, 2).qty = 5


class RegistryTests(unittest.TestCase):
    def test_builtin_steps_run_in_order(self):
        self.assertEqual(registered()[:3], ["drop_tiny", "tag_bulk", "tag_big"])

    def test_duplicate_name_is_refused(self):
        with self.assertRaises(ValueError):
            step("tag_big", order=99)(lambda item: item)

    def test_steps_drop_and_tag(self):
        small = Enriched(Order(1, "a", "X", 1, 5.0, "USD"), 5.0)
        large = Enriched(Order(2, "b", "X", 4, 50.0, "USD"), 200.0)
        dropped = []
        kept = list(run_steps([small, large], dropped=dropped))
        self.assertEqual(kept, [large])
        self.assertEqual(large.tags, ["bulk", "big"])
        self.assertEqual(dropped, [small])

    def test_unknown_step_name(self):
        with self.assertRaises(KeyError):
            list(run_steps([], ["nope"]))


class SinkTests(unittest.TestCase):
    def test_success_and_rollback(self):
        item = Enriched(Order(1, "a", "X", 1, 5.0, "USD"), 5.0, ["x"])
        with tempfile.TemporaryDirectory() as folder:
            good, bad = Path(folder, "good.jsonl"), Path(folder, "bad.jsonl")
            with JsonlSink(good) as sink:
                sink.write(item)
            self.assertEqual(next(read_jsonl(good))["tags"], ["x"])
            with self.assertRaises(RuntimeError):
                with JsonlSink(bad) as sink:
                    sink.write(item)
                    raise RuntimeError("boom")
            self.assertFalse(bad.exists())


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_retry_recovers_from_transient_errors(self):
        source = FakeRateSource(flaky={"EUR": 2})
        self.assertEqual(await fetch_rate(source, "EUR"), 1.10)
        self.assertEqual(source.calls["EUR"], 3)

    async def test_retry_gives_up(self):
        source = FakeRateSource(flaky={"EUR": 5})
        with self.assertRaises(TransientError):
            await fetch_rate(source, "EUR")
        self.assertEqual(source.calls["EUR"], 3)

    async def test_concurrency_limit_and_unknown_currency(self):
        source = FakeRateSource()
        rates = await fetch_rates(["USD", "EUR", "GBP", "JPY"], source, limit=2)
        self.assertLessEqual(source.max_active, 2)
        self.assertEqual(source.calls["JPY"], 1)
        self.assertNotIsInstance(rates["JPY"], float)

    async def test_full_run(self):
        with tempfile.TemporaryDirectory() as folder:
            src, out = Path(folder, "in.csv"), Path(folder, "out.jsonl")
            src.write_text("\n".join(CSV) + "\n", encoding="utf-8")
            report = await run_pipeline(src, out, FakeRateSource(), FakeClock())
            self.assertEqual((report.read, len(report.written)), (3, 2))
            self.assertEqual(len(list(read_jsonl(out))), 2)


if __name__ == "__main__":
    unittest.main()
'''

MAIN = r'''
"""Run orderflow from the command line: python main.py"""
import asyncio
import logging
import sys
from pathlib import Path

import pipeline_steps  # noqa: F401  (registers the built-in steps)
from pipeline_resources import FakeClock
from pipeline_runner import Report, run_pipeline
from pipeline_source import FakeRateSource


def main(source: str = "orders.csv", output: str = "orders_out.jsonl") -> Report:
    """Run the whole pipeline once, print the report and return it."""
    rate_source = FakeRateSource(flaky={"GBP": 1})
    report = asyncio.run(run_pipeline(Path(source), Path(output), rate_source, FakeClock()))
    print(report.render())
    return report


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s")
    main()
'''

LOGGING = '''
import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")
'''

cap.starter({"orders.csv": ORDERS})
cap.solution({
    "pipeline_models.py": MODELS,
    "pipeline_registry.py": REGISTRY,
    "pipeline_steps.py": STEPS,
    "pipeline_resources.py": RESOURCES,
    "pipeline_source.py": SOURCE,
    "pipeline_runner.py": RUNNER,
    "test_pipeline.py": TESTS,
    "main.py": MAIN,
})

cap.milestone(
    "Models and the streaming reader",
    prompt="""
        Create `pipeline_models.py`. It needs a base error `PipelineError` and `BadRecord(PipelineError)`
        that remembers the `line` and a `reason` (message `line N: reason`). Add a frozen, slotted
        dataclass `Order` (id, customer, sku, qty, price, currency) with a `total` property rounded to
        2 decimals. Write `parse_order(row, line)` which strips and lowercases the customer, uppercases
        sku and currency, and raises `BadRecord` for a missing customer, a number that does not parse,
        or a non-positive qty or price. Then write the generator `read_orders(lines, rejects=None)`
        using `csv.DictReader`: it yields valid orders one at a time and logs a warning for each bad
        row, appending the error to `rejects`. `demo_1.py` reads `orders.csv` and shows the stream is
        lazy (the first order, then the rest) and then lists each rejected error with its reason.
        Run it with `python check.py 1`.
    """,
    writes=["pipeline_models.py"],
    demo=LOGGING + r'''
from pipeline_models import read_orders

rejects = []
with open("orders.csv", encoding="utf-8") as f:
    stream = read_orders(f, rejects)
    print("First:", next(stream))
    rest = list(stream)
print("Then", len(rest), "more orders")
for error in rejects:
    print("Rejected:", error, "|", error.reason)
''')

cap.milestone(
    "The plugin registry",
    prompt="""
        Extend `pipeline_models.py` with a mutable dataclass `Enriched` (an `order`, a `usd_total` and a
        `tags` list that defaults to empty) and a `TypedDict` `CustomerTotals` with `orders` and
        `revenue`. Then create `pipeline_registry.py` with a decorator factory `step(name, *, order)`
        that stores the decorated function in a module-level dict (refuse a duplicate name with
        `ValueError`), `registered()` returning the names sorted by order, `load_plugins(*module_names)`
        that imports each module with `importlib` and logs it, and the generator
        `run_steps(items, names=None, dropped=None)`: each item goes through the chosen steps in order,
        a step that returns `None` drops the item (log it and append it to `dropped`), and unknown step
        names raise `KeyError`. In `pipeline_steps.py` register `drop_tiny` (order 10, drops items
        under 20 dollars), `tag_bulk` (20, tag "bulk" when qty is at least 3) and `tag_big` (30, tag
        "big" at 100 dollars or more). `demo_2.py` loads the plugins, runs three hand-made items
        through the steps and tries to register `"tag_big"` twice.
    """,
    writes=["pipeline_models.py", "pipeline_registry.py", "pipeline_steps.py"],
    demo=LOGGING + r'''
from pipeline_models import Enriched, Order
from pipeline_registry import load_plugins, registered, run_steps, step

load_plugins("pipeline_steps")
print(registered())

items = [
    Enriched(Order(1, "ana", "KB", 1, 5.0, "USD"), 5.0),
    Enriched(Order(2, "bo", "MS", 4, 30.0, "USD"), 120.0),
    Enriched(Order(3, "cy", "MN", 1, 50.0, "USD"), 50.0),
]
dropped = []
for item in run_steps(items, dropped=dropped):
    print(item.order.id, item.tags)
print("Dropped:", [d.order.id for d in dropped])

try:
    step("tag_big", order=40)(lambda item: item)
except ValueError as e:
    print("ValueError:", e)
''')

cap.milestone(
    "Resources that clean up after themselves",
    prompt="""
        Create `pipeline_resources.py` for things that must be cleaned up. Write a `FakeClock` class:
        calling an instance adds a fixed step (default 0.5) to its time and returns it, so timings are
        repeatable. Write the class-based context manager `JsonlSink(path)`: on entering it opens the
        file and returns itself, `write(item)` appends `json.dumps(asdict(item), sort_keys=True)` as a
        line and counts it, and on exit it closes the file; if the block failed it also deletes the
        half-written file, logs an error and lets the exception continue. Write a `@contextmanager`
        `stopwatch(label, clock)` that logs `label took X.XXs` even if the block fails, and a generator
        `read_jsonl(path)` yielding one dict per line. `demo_3.py` writes two items through a sink in a
        temporary folder and reads them back, raises `RuntimeError` inside a second sink to show its
        file is gone, and times an empty block with a `FakeClock`.
    """,
    writes=["pipeline_resources.py"],
    demo=LOGGING + r'''
import tempfile
from pathlib import Path
from pipeline_models import Enriched, Order
from pipeline_resources import FakeClock, JsonlSink, read_jsonl, stopwatch

items = [Enriched(Order(i, "ana", "KB", 1, 10.0, "USD"), 10.0, ["t"]) for i in (1, 2)]
with tempfile.TemporaryDirectory() as folder:
    good, bad = Path(folder, "good.jsonl"), Path(folder, "bad.jsonl")
    with JsonlSink(good) as sink:
        for item in items:
            sink.write(item)
    print("Count:", sink.count)
    print([row["order"]["id"] for row in read_jsonl(good)])

    try:
        with JsonlSink(bad) as sink:
            sink.write(items[0])
            raise RuntimeError("disk on fire")
    except RuntimeError as e:
        print("Caught:", e, "| file exists:", bad.exists())

with stopwatch("empty block", FakeClock()):
    pass
''')

cap.milestone(
    "Async rates with retries",
    prompt="""
        Create `pipeline_source.py`, the async part. Define `TransientError` and `UnknownCurrency` (both
        `PipelineError`s), and a decorator `retry(times)` for async functions: it catches only
        `TransientError`, logs `attempt N/M failed: ...` and re-raises on the last attempt (use
        `functools.wraps`, and `ParamSpec`/`TypeVar` so type checkers keep the signature).
        `FakeRateSource` is the fake service: its rates are USD 1.0, EUR 1.10, GBP 1.30;
        `flaky={"GBP": 2}` makes the first two GBP calls fail transiently; an unknown currency raises
        `UnknownCurrency`; it counts calls per currency in a `Counter` and records the highest number of
        calls running at the same time (`await asyncio.sleep(0)` inside gives other tasks a turn).
        Write `fetch_rate(source, currency)` with `@retry(times=3)`, then
        `async fetch_rates(currencies, source, limit=2)` which fetches every distinct currency
        concurrently with an `asyncio.Semaphore` and `gather(..., return_exceptions=True)` and returns a
        dict of currency to rate, or to the `PipelineError` that happened. `demo_4.py` runs it with
        `asyncio.run(main())` on USD, EUR, GBP and JPY with a flaky GBP and prints the results, the calls
        per currency and the highest concurrency.
    """,
    writes=["pipeline_source.py"],
    demo=LOGGING + r'''
import asyncio
from pipeline_source import FakeRateSource, fetch_rates

async def main():
    source = FakeRateSource(flaky={"GBP": 2})
    rates = await fetch_rates(["USD", "EUR", "GBP", "JPY", "EUR"], source, limit=2)
    for code, rate in rates.items():
        shown = rate if isinstance(rate, float) else type(rate).__name__
        print(code, shown)
    print("Calls:", dict(sorted(source.calls.items())))
    print("Highest concurrency:", source.max_active)

asyncio.run(main())
''')

cap.milestone(
    "Enrich and run: the runner",
    prompt="""
        First extend `pipeline_source.py` with the generator `enrich(orders, rates, skipped=None)`: it
        yields `Enriched` objects with the total converted to dollars (2 decimals), and logs and skips
        any order with no usable rate, appending it to `skipped`. Then create `pipeline_runner.py`, which
        wires every module together. A `Report` dataclass holds the number of rows read, the list of
        rejected errors, the ids skipped for a missing rate, the ids dropped by steps and the list of
        written `Enriched` items. Give it `totals()` (customer to a `CustomerTotals` with order count
        and revenue, rounded to 2 decimals) and `render()` returning the report text: a title line
        `=== ORDERFLOW REPORT ===`, rows read and rejected, the skipped ids, the dropped ids, the
        written count, the tag counts (a sorted dict) and a revenue line per customer, alphabetical,
        with the amount right-aligned to 8 wide. Then write `async run_pipeline(source_path,
        output_path, rate_source, clock, steps=None)`: read all orders (timed with
        `stopwatch("read", clock)`), fetch the distinct currencies (timed as `rates`), enrich, run the
        steps and write the survivors inside a `JsonlSink`, and return the `Report`. `demo_5.py` runs it
        on `orders.csv` into a temporary folder and prints the number read, the number written and the
        written order ids.
    """,
    writes=["pipeline_source.py", "pipeline_runner.py"],
    demo=LOGGING + r'''
import asyncio
import tempfile
from pathlib import Path
import pipeline_steps  # registers the steps
from pipeline_resources import FakeClock
from pipeline_runner import run_pipeline
from pipeline_source import FakeRateSource

async def main():
    with tempfile.TemporaryDirectory() as folder:
        report = await run_pipeline(Path("orders.csv"), Path(folder, "out.jsonl"),
                                    FakeRateSource(flaky={"GBP": 1}), FakeClock())
        print("Read:", report.read, "Written:", len(report.written))
        print([item.order.id for item in report.written])

asyncio.run(main())
''')

cap.milestone(
    "A real test suite",
    prompt="""
        Write `test_pipeline.py`, a `unittest` suite that covers every module: parsing (normalisation,
        `BadRecord` carries its line number, `read_orders` returns a generator and skips bad rows,
        `Order` is frozen), the registry (built-in order, duplicate names refused, drop and tag
        behaviour, unknown step), the sink (success, and the file is gone after a failure) and, in an
        `IsolatedAsyncioTestCase`, the retry decorator (recovers; gives up after 3 attempts), the
        concurrency limit with an unknown currency, and a full run in a temporary directory. Use
        in-memory rows and `tempfile`, not `orders.csv`, so the suite does not depend on other files, and
        finish with the usual `if __name__ == "__main__": unittest.main()`. This is a real script now,
        so `python -m unittest test_pipeline` works from the project folder. `demo_6.py` loads your
        suite, runs it with a `TextTestRunner` that writes to a `StringIO` and prints whether the run
        was successful, how many tests ran and the number of failures and errors.
    """,
    writes=["test_pipeline.py"],
    demo=r'''
import io
import logging
import unittest

import test_pipeline

suite = unittest.defaultTestLoader.loadTestsFromModule(test_pipeline)
runner = unittest.TextTestRunner(stream=io.StringIO())
logging.disable(logging.CRITICAL)
try:
    result = runner.run(suite)
finally:
    logging.disable(logging.NOTSET)
print("Success:", result.wasSuccessful())
print("Tests run:", result.testsRun)
print("Failures:", len(result.failures), "Errors:", len(result.errors))
''')

cap.milestone(
    "The finale: main.py",
    prompt="""
        Write `main.py`, the entry point. Define `main(source="orders.csv", output="orders_out.jsonl")`
        which builds a `FakeRateSource` with `flaky={"GBP": 1}`, runs `run_pipeline` with
        `asyncio.run` (never a top-level `await`) and a `FakeClock`, prints the report text and returns
        the `Report`. Import `pipeline_steps` so the built-in steps are registered. Close the file with
        `if __name__ == "__main__":`, set up `logging.basicConfig` to print to stdout there and call
        `main()`, so `python main.py` runs the real thing while importing the module does nothing.
        `demo_7.py` imports your `main` function and calls it on `orders.csv` with the output going to a
        temporary folder, so the report is printed, and then shows the output file has one line per
        written order.
    """,
    writes=["main.py"],
    demo=LOGGING + r'''
import tempfile
from pathlib import Path
from main import main

with tempfile.TemporaryDirectory() as folder:
    out = Path(folder, "out.jsonl")
    report = main("orders.csv", str(out))
    lines = out.read_text(encoding="utf-8").splitlines()
    print()
    print("Lines in output file:", len(lines), "| matches report:", len(lines) == len(report.written))
''')

cap.build()
