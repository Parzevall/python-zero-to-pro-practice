import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

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
