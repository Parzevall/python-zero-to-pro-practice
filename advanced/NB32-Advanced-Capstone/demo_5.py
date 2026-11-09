import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

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
