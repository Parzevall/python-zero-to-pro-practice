import logging
import sys

logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

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
