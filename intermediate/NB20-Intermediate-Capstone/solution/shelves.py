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
