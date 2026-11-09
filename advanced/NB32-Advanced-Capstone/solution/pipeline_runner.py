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
