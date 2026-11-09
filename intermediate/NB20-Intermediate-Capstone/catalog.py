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
