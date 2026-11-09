import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

import tempfile
from pathlib import Path
from main import main

with tempfile.TemporaryDirectory() as folder:
    out = Path(folder, "out.jsonl")
    report = main("orders.csv", str(out))
    lines = out.read_text(encoding="utf-8").splitlines()
    print()
    print("Lines in output file:", len(lines), "| matches report:", len(lines) == len(report.written))
