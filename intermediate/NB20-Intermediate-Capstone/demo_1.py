from shelves import load_catalog

catalog, skipped = load_catalog("books.json")
print("Books loaded:", len(catalog))
for message in skipped:
    print("Skipped:", message)
for book in catalog.search("AUSTEN"):
    print(book)
print(catalog.by_author())
