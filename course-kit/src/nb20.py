import sys; sys.path.insert(0, "..")
from capstone import Capstone

cap = Capstone("NB20", title="Pageturner Library", intro="""
    The intermediate finale. This time the program is a real project: a
    **library system** split across several Python files that you write in your
    editor, building on a starter module written by a teammate that you must read,
    fix and extend. You'll use classes and inheritance, custom exceptions, JSON
    saving and loading, a CSV report, `datetime`, `Counter` and `match`.
    Everything from NB09 to NB19 is fair game.
""", story="""
    *Pageturner* is a small town library whose records live in a spreadsheet and
    a lot of sticky notes. Your teammate Dana started a Python catalog module
    (`catalog.py`) before going on holiday, and she left it unreviewed: it
    works, but it has a few rough edges. You'll read it, extend it, and build the
    rest of the program around it in separate modules: members, lending rules
    with fines, saving to JSON, a CSV report, and finally a whole month of
    activity (`events.json`) processed end to end by `main.py`.
""")

CATALOG = '''
"""Catalog module, written by Dana (v0.1, not reviewed yet)."""


class LibraryError(Exception):
    """Base class for every error in the library app."""


class BookNotFound(LibraryError):
    pass


class Book:
    def __init__(self, isbn, title, author, year, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.on_loan = 0

    def available(self):
        return self.copies - self.on_loan

    def to_dict(self):
        return {"isbn": self.isbn, "title": self.title, "author": self.author,
                "year": self.year, "copies": self.copies}

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"


class Catalog:
    def __init__(self):
        self.books = {}

    def add(self, book):
        self.books[book.isbn] = book

    def get(self, isbn):
        if isbn not in self.books:
            raise BookNotFound(f"no book with ISBN {isbn}")
        return self.books[isbn]

    def search(self, text):
        found = []
        for book in self.books.values():
            if text in book.title or text in book.author:
                found.append(book)
        return sorted(found, key=lambda b: b.title)

    def __len__(self):
        return len(self.books)
'''

BOOKS = '''[
  {"isbn": "111", "title": "Dune", "author": "Frank Herbert", "year": 1965, "copies": 2},
  {"isbn": "222", "title": "Neuromancer", "author": "William Gibson", "year": 1984},
  {"isbn": "333", "title": "Emma", "author": "Jane Austen", "year": 1815},
  {"isbn": "444", "title": "Persuasion", "author": "Jane Austen", "year": 1817, "copies": 2},
  {"isbn": "555", "title": "Hyperion", "author": "Dan Simmons", "year": 1989},
  {"isbn": "111", "title": "Dune (reprint)", "author": "Frank Herbert", "year": 1990},
  {"isbn": "666", "author": "Anonymous", "year": 2001}
]'''

EVENTS = '''[
  ["2026-03-02", "join", "Ana"],
  ["2026-03-02", "join", "Bo", "premium"],
  ["2026-03-02", "join", "Cy"],
  ["2026-03-03", "out", "Ana", "111"],
  ["2026-03-03", "out", "Ana", "222"],
  ["2026-03-03", "out", "Ana", "333"],
  ["2026-03-04", "out", "Bo", "222"],
  ["2026-03-04", "out", "Bo", "111"],
  ["2026-03-05", "out", "Cy", "999"],
  ["2026-03-06", "out", "Dee", "111"],
  ["2026-03-20", "back", "Ana", "111"],
  ["2026-03-20", "out", "Ana", "444"],
  ["2026-03-21", "back", "Cy", "555"],
  ["2026-03-21", "pay", "Ana"],
  ["2026-03-21", "out", "Ana", "444"],
  ["2026-03-22", "back", "Bo", "111"],
  ["2026-03-22", "dance", "Bo"]
]'''

SHELVES = '''
import json
from catalog import Catalog, Book, LibraryError


class DuplicateBook(LibraryError):
    pass


class SmartCatalog(Catalog):
    def add(self, book):
        if book.isbn in self.books:
            raise DuplicateBook(f"ISBN {book.isbn} is already in the catalog")
        super().add(book)

    def search(self, text):
        text = text.lower()
        found = []
        for book in self.books.values():
            if text in book.title.lower() or text in book.author.lower():
                found.append(book)
        return sorted(found, key=lambda b: b.title)

    def by_author(self):
        groups = {}
        for book in self.books.values():
            groups.setdefault(book.author, []).append(book.title)
        return {author: sorted(titles) for author, titles in groups.items()}


def load_catalog(path):
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    catalog = SmartCatalog()
    skipped = []
    for row in rows:
        try:
            book = Book(row["isbn"], row["title"], row["author"],
                        row["year"], row.get("copies", 1))
            catalog.add(book)
        except DuplicateBook as e:
            skipped.append(str(e))
        except KeyError as e:
            skipped.append(f"record {row['isbn']} is missing {e}")
    return catalog, skipped
'''

MEMBERS = '''
from catalog import LibraryError


class LimitReached(LibraryError):
    pass


class FineOwed(LibraryError):
    pass


class Member:
    limit = 2
    loan_days = 14

    def __init__(self, name):
        self.name = name
        self.loans = {}      # isbn -> due date
        self.fines = 0       # in cents

    def kind(self):
        return "standard"

    def check(self):
        if self.fines > 0:
            raise FineOwed(f"{self.name} owes {self.fines} cents")
        if len(self.loans) >= self.limit:
            raise LimitReached(f"{self.name} already has {self.limit} books")

    def __str__(self):
        return f"{self.name} ({self.kind()})"


class PremiumMember(Member):
    limit = 4
    loan_days = 21

    def kind(self):
        return "premium"
'''

LIBRARY = '''
from datetime import date, timedelta
from catalog import LibraryError
from members import Member, PremiumMember

FINE_PER_DAY = 25  # cents


class UnknownMember(LibraryError):
    pass


class NoCopiesLeft(LibraryError):
    pass


class NotBorrowed(LibraryError):
    pass


class Library:
    def __init__(self, catalog):
        self.catalog = catalog
        self.members = {}
        self.history = []    # (date text, "out" or "back", member, isbn)

    def join(self, name, premium=False):
        member = PremiumMember(name) if premium else Member(name)
        self.members[name] = member
        return member

    def member(self, name):
        if name not in self.members:
            raise UnknownMember(f"{name} is not a member")
        return self.members[name]

    def checkout(self, name, isbn, today):
        member = self.member(name)
        book = self.catalog.get(isbn)
        member.check()
        if book.available() <= 0:
            raise NoCopiesLeft(f"{book.title} has no copies left")
        book.on_loan += 1
        due = today + timedelta(days=member.loan_days)
        member.loans[isbn] = due
        self.history.append((today.isoformat(), "out", name, isbn))
        return due

    def give_back(self, name, isbn, today):
        member = self.member(name)
        if isbn not in member.loans:
            raise NotBorrowed(f"{name} has not borrowed {isbn}")
        due = member.loans.pop(isbn)
        self.catalog.get(isbn).on_loan -= 1
        fine = max(0, (today - due).days) * FINE_PER_DAY
        member.fines += fine
        self.history.append((today.isoformat(), "back", name, isbn))
        return fine

    def pay(self, name):
        member = self.member(name)
        paid = member.fines
        member.fines = 0
        return paid

    def overdue(self, today):
        late = []
        for name in sorted(self.members):
            for isbn, due in sorted(self.members[name].loans.items()):
                if due < today:
                    late.append((name, isbn, (today - due).days))
        return late

def run_events(library, events):
    outcomes = []
    for when, *rest in events:
        today = date.fromisoformat(when)
        try:
            match rest:
                case ["join", name]:
                    library.join(name)
                    message = f"{name} joined"
                case ["join", name, "premium"]:
                    library.join(name, premium=True)
                    message = f"{name} joined as premium"
                case ["out", name, isbn]:
                    due = library.checkout(name, isbn, today)
                    message = f"{name} took {isbn}, due {due}"
                case ["back", name, isbn]:
                    fine = library.give_back(name, isbn, today)
                    message = f"{name} returned {isbn}, fine {fine}"
                case ["pay", name]:
                    message = f"{name} paid {library.pay(name)}"
                case _:
                    raise LibraryError(f"unknown action {rest[0]}")
            outcomes.append((when, True, message))
        except LibraryError as e:
            outcomes.append((when, False, f"{type(e).__name__}: {e}"))
    return outcomes
'''


STORAGE = '''
import csv
import json
from datetime import date
from catalog import Book, LibraryError
from shelves import SmartCatalog
from library import Library


class StorageError(LibraryError):
    pass


def save_state(library, path):
    books = []
    for book in library.catalog.books.values():
        row = book.to_dict()
        row["on_loan"] = book.on_loan
        books.append(row)
    members = []
    for member in library.members.values():
        loans = {isbn: due.isoformat() for isbn, due in member.loans.items()}
        members.append({"name": member.name, "premium": member.kind() == "premium",
                        "fines": member.fines, "loans": loans})
    data = {"books": books, "members": members, "history": library.history}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_state(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise StorageError(f"no saved state at {path}") from None
    catalog = SmartCatalog()
    for row in data["books"]:
        book = Book(row["isbn"], row["title"], row["author"], row["year"], row["copies"])
        book.on_loan = row["on_loan"]
        catalog.add(book)
    library = Library(catalog)
    for row in data["members"]:
        member = library.join(row["name"], row["premium"])
        member.fines = row["fines"]
        for isbn, text in row["loans"].items():
            member.loans[isbn] = date.fromisoformat(text)
    library.history = [tuple(item) for item in data["history"]]
    return library


def write_loans_csv(library, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["member", "isbn", "title", "due"])
        for name in sorted(library.members):
            member = library.members[name]
            for isbn, due in sorted(member.loans.items()):
                title = library.catalog.get(isbn).title
                writer.writerow([name, isbn, title, due.isoformat()])


def read_loans_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
'''

MAIN = '''
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
'''

cap.starter({"catalog.py": CATALOG, "books.json": BOOKS, "events.json": EVENTS})
cap.solution({"shelves.py": SHELVES, "members.py": MEMBERS, "library.py": LIBRARY,
              "storage.py": STORAGE, "main.py": MAIN})

cap.milestone("Shelves", writes=["shelves.py"], prompt="""
    Read `catalog.py` carefully before changing anything. Dana's `Catalog.add` silently
    overwrites a book with the same ISBN, and her `search` is case-sensitive. In a new file
    `shelves.py` write a custom error `DuplicateBook` (a `LibraryError`) and a subclass
    `SmartCatalog(Catalog)` that raises it on duplicates (reuse the parent's `add` with
    `super()`), searches case-insensitively, and has `by_author()` returning a dict of
    author to sorted list of titles. Add `load_catalog(path)` that reads a JSON list of
    book records into a `SmartCatalog` and returns it together with a list of messages
    about the records it had to skip: duplicates and records with a missing field. The
    demo loads `books.json` and prints the number of books, each skipped message, the
    titles found by searching "AUSTEN", and `by_author()`.
""", demo='''
from shelves import load_catalog

catalog, skipped = load_catalog("books.json")
print("Books loaded:", len(catalog))
for message in skipped:
    print("Skipped:", message)
for book in catalog.search("AUSTEN"):
    print(book)
print(catalog.by_author())
''')

cap.milestone("Members", writes=["members.py"], prompt="""
    Create `members.py`. It imports `LibraryError` from `catalog` and defines two errors,
    `LimitReached` and `FineOwed`, then a `Member` class with the class attributes
    `limit = 2` and `loan_days = 14`, a name, a `loans` dict (ISBN to due date) and
    `fines` in cents. Give it `kind()` returning `"standard"`, `check()` which raises
    `FineOwed` when fines are above zero and `LimitReached` when the member already has
    `limit` loans, and `__str__`. Add `PremiumMember(Member)` with limit 4, 21 loan days
    and kind `"premium"`. The demo creates one member of each kind and prints them with
    their limits, then fills a standard member's loans with two fake entries and prints
    the message from the error that `check()` raises.
""", demo='''
from members import Member, PremiumMember, LimitReached

ana = Member("Ana")
bo = PremiumMember("Bo")
for member in (ana, bo):
    print(member, member.limit, member.loan_days)
ana.loans = {"111": None, "222": None}
try:
    ana.check()
except LimitReached as e:
    print("Blocked:", e)
''')

cap.milestone("Library", writes=["library.py"], prompt="""
    Create `library.py` with a `Library` class that holds a catalog, a dict of members
    and a `history` list of `(date text, "out" or "back", member, isbn)` tuples. Define
    the errors `UnknownMember`, `NoCopiesLeft` and `NotBorrowed`, and a fine of 25 cents
    per late day. Methods: `join(name, premium=False)`, `member(name)`,
    `checkout(name, isbn, today)` (member check, then copy check, then update `on_loan`,
    the member's loans and the history, and return the due date),
    `give_back(name, isbn, today)` (returns the fine in cents and adds it to the member),
    `pay(name)` and `overdue(today)` returning sorted `(name, isbn, days late)` tuples.
    The demo checks out Dune for Ana on 2026-03-03 and prints the due date, returns it
    ten days late and prints the fine, then tries three failing checkouts (an unknown
    member, an unknown book, a member who owes a fine) and prints each error class name
    and message.
""", demo='''
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
''')

cap.milestone("Saving and the CSV report", writes=["storage.py"], prompt="""
    Create `storage.py` with a `StorageError` and four functions. `save_state(library,
    path)` writes books (with their `on_loan` counts), members (name, premium flag,
    fines, loans as ISO date text) and the history to a JSON file with indent 2.
    `load_state(path)` rebuilds an equal `Library`, turning date text back into `date`
    objects and the history lists back into tuples; a missing file must raise
    `StorageError` (use `from None`). `write_loans_csv(library, path)` writes a CSV with
    the columns member, isbn, title, due, sorted by member, and `read_loans_csv` reads it
    back with `DictReader`. The demo builds a library with a few loans, saves and reloads
    it inside a temporary folder and prints whether the history and Bo's loans match,
    writes the CSV and prints its rows, and finally loads a missing file and prints the
    error.
""", demo='''
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
''')

cap.milestone("A month of events", writes=["library.py"], prompt="""
    `events.json` holds a month of library activity: a list of `[date text, action,
    member, ...]` records. Extend `library.py` with a function `run_events(library,
    events)`. For each event convert the date with `date.fromisoformat` and use `match`
    on the remaining items: `["join", name]`, `["join", name, "premium"]`, `["out", name,
    isbn]`, `["back", name, isbn]`, `["pay", name]`, and a default case that raises
    `LibraryError` for an unknown action. Wrap the handling in `try`/`except
    LibraryError` so one bad event never stops the run. Return a list of `(date text,
    ok, message)` tuples, where the message of a failure is the error class name and its
    text. The demo loads the events, runs them on a fresh library and prints every
    outcome as one line: the date, `ok` or `FAILED`, and the message.
""", demo='''
import json

from library import Library, run_events
from shelves import load_catalog

with open("events.json", encoding="utf-8") as f:
    events = json.load(f)
month = Library(load_catalog("books.json")[0])
for when, ok, message in run_events(month, events):
    print(when, "ok    " if ok else "FAILED", message)
''')

cap.milestone("The finale", writes=["main.py"], prompt="""
    The finale: write `main.py`, which runs the whole program from scratch. Define a
    function `main()` and end the file with `if __name__ == "__main__": main()`. It
    loads the catalog from `books.json`, creates a new `Library`, runs all the events from
    `events.json`, saves the state to a JSON file in a temporary folder, loads it back
    into `reloaded` and uses only `reloaded` for the report. Print a title line, then:
    the number of events that succeeded and failed, the failures counted by error class
    name (use `Counter`, print its `most_common()` result), the books still on loan as
    `title -> member (due date)` lines, the overdue list as of 2026-04-10, each member's
    fines in dollars with 2 decimals (alphabetical), and the title of the most borrowed
    book from the history. Write the loans CSV in the temporary folder too and print how
    many data rows it has. Find the data files next to `main.py` (with `Path(__file__)`),
    not in the current folder. The demo just calls `main()`.
""", demo='''
from main import main

main()
''')

cap.build()
