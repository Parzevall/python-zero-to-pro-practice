import json

from library import Library, run_events
from shelves import load_catalog

with open("events.json", encoding="utf-8") as f:
    events = json.load(f)
month = Library(load_catalog("books.json")[0])
for when, ok, message in run_events(month, events):
    print(when, "ok    " if ok else "FAILED", message)
