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
