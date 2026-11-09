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
