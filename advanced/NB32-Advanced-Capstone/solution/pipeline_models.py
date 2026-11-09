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
