from datetime import date
from library import Library
from shelves import load_catalog

catalog, _ = load_catalog("books.json")
lib = Library(catalog)
lib.join("Ana")
lib.join("Bo", premium=True)
print("Due:", lib.checkout("Ana", "111", date(2026, 3, 3)))
print("Fine:", lib.give_back("Ana", "111", date(2026, 3, 27)))
attempts = [("Zed", "111"), ("Bo", "999"), ("Ana", "222")]
for name, isbn in attempts:
    try:
        lib.checkout(name, isbn, date(2026, 3, 28))
    except Exception as e:
        print(type(e).__name__, "-", e)
