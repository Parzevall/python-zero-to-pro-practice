import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

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
