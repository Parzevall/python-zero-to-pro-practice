import tempfile
from datetime import date
from pathlib import Path

from library import Library
from shelves import load_catalog
from storage import save_state, load_state, write_loans_csv, read_loans_csv, StorageError

lib = Library(load_catalog("books.json")[0])
lib.join("Ana")
lib.join("Bo", premium=True)
lib.checkout("Ana", "111", date(2026, 3, 3))
lib.give_back("Ana", "111", date(2026, 3, 27))
lib.checkout("Bo", "333", date(2026, 3, 5))
with tempfile.TemporaryDirectory() as folder:
    state = Path(folder) / "state.json"
    save_state(lib, state)
    again = load_state(state)
    print(again.history == lib.history)
    print(again.members["Bo"].loans == lib.members["Bo"].loans)
    print(again.members["Ana"].fines, again.members["Bo"].kind())
    csv_path = Path(folder) / "loans.csv"
    write_loans_csv(again, csv_path)
    for row in read_loans_csv(csv_path):
        print(dict(row))
    try:
        load_state(Path(folder) / "nothing-here.json")
    except StorageError:
        print("StorageError: no saved state")
