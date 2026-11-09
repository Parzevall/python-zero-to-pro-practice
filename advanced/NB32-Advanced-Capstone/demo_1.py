import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

from pipeline_models import read_orders

rejects = []
with open("orders.csv", encoding="utf-8") as f:
    stream = read_orders(f, rejects)
    print("First:", next(stream))
    rest = list(stream)
print("Then", len(rest), "more orders")
for error in rejects:
    print("Rejected:", error, "|", error.reason)
