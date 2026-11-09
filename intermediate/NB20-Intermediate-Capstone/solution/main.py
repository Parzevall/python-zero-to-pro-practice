import json
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

from library import Library, run_events
from shelves import load_catalog
from storage import save_state, load_state, write_loans_csv, read_loans_csv

HERE = Path(__file__).parent


def main():
    catalog, _ = load_catalog(HERE / "books.json")
    with open(HERE / "events.json", encoding="utf-8") as f:
        events = json.load(f)
    final = Library(catalog)
    results = run_events(final, events)
    with tempfile.TemporaryDirectory() as folder:
        save_state(final, Path(folder) / "final.json")
        reloaded = load_state(Path(folder) / "final.json")
        write_loans_csv(reloaded, Path(folder) / "final_loans.csv")
        csv_rows = len(read_loans_csv(Path(folder) / "final_loans.csv"))

    print("=== PAGETURNER LIBRARY: MARCH REPORT ===")
    passed = [r for r in results if r[1]]
    print("Events ok:", len(passed), "failed:", len(results) - len(passed))
    kinds = Counter(r[2].split(":")[0] for r in results if not r[1])
    print("Failures:", kinds.most_common())

    print("On loan:")
    for name in sorted(reloaded.members):
        for isbn, due in reloaded.members[name].loans.items():
            print(f"  {reloaded.catalog.get(isbn).title} -> {name} (due {due})")
    print("Overdue on 2026-04-10:", reloaded.overdue(date(2026, 4, 10)))
    print("Fines:")
    for name in sorted(reloaded.members):
        print(f"  {name:<4}${reloaded.members[name].fines / 100:.2f}")

    taken = Counter(h[3] for h in reloaded.history if h[1] == "out")
    top = taken.most_common(1)[0][0]
    print("Most borrowed:", reloaded.catalog.get(top).title)
    print("CSV rows:", csv_rows)


if __name__ == "__main__":
    main()
