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
