import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB10", title="Comprehensions, Functional & Sorting", intro="""
    Building lists, dicts and sets in one expression, feeding generators to
    `sum` / `any` / `all`, pairing data with `zip` and `enumerate`, and
    sorting by whatever you like with `key=`. Each question asks you to
    **write the code**. Starting data is given to you as variables. Short is
    nice, but readable wins: some jobs are still better as a plain loop.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", "Build a list of the squares of 1 to 10 with a list comprehension and print it.",
     solution="squares = [n * n for n in range(1, 11)]\nprint(squares)")

nb.q("Real-life", "A shop adds 20% tax. Build a new list with each price plus tax, rounded to 2 decimal places, and print it.",
     given="prices = [9.99, 24.5, 3.2, 100]",
     solution="with_tax = [round(p * 1.2, 2) for p in prices]\nprint(with_tax)")

nb.q("Output-match", "Print a list of the words longer than 3 letters, each in upper case. Use one comprehension with a filter.",
     given='words = ["a", "tree", "is", "green", "and", "tall"]',
     solution="print([w.upper() for w in words if len(w) > 3])")

nb.q("Puzzle", """
    `raw` holds sign-up ages as text, wrapped in a `map`. Print how many ages
    there are, then print their total.
""",
     given='raw = map(int, ["31", "27", "45", "19"])',
     solution="ages = list(raw)\nprint(len(ages))\nprint(sum(ages))")

nb.q("Real-life", "Using generator expressions, print whether **any** score is below 50, then whether **all** scores are at most 100.",
     given="scores = [72, 95, 48, 100, 61]",
     solution="print(any(s < 50 for s in scores))\nprint(all(s <= 100 for s in scores))")

# ------------------------------------------------------------ Combine
nb.q("Build", "Build a dict that maps each fruit to the length of its name with a dict comprehension, and print it.",
     given='fruits = ["apple", "fig", "banana", "kiwi"]',
     solution="lengths = {f: len(f) for f in fruits}\nprint(lengths)")

nb.q("Real-life", "Customers signed up with these names. Use a set comprehension to find the different first letters (upper case) and print them as a sorted list.",
     given='names = ["alice", "bob", "anna", "Carl", "bella", "cora"]',
     solution="letters = {n[0].upper() for n in names}\nprint(sorted(letters))")

nb.q("Real-life", """
    Build a list with `"hot"` for each temperature above 25 and `"mild"` for
    the others (a comprehension with `if` / `else` in the expression). Print it.
""",
     given="temps = [31, 18, 26, 25, 22]",
     solution='labels = ["hot" if t > 25 else "mild" for t in temps]\nprint(labels)')

nb.q("Real-life", "Print the to-do list as numbered lines starting at 1, in the form `1. buy milk`. Use `enumerate`.",
     given='todo = ["buy milk", "call mum", "pay rent"]',
     solution="for number, task in enumerate(todo, start=1):\n    print(f\"{number}. {task}\")")

nb.q("Build", "Pair each student with their score in a dict using `zip` (make it fail loudly if the lists differ in length with `strict=True`). Print the dict.",
     given='students = ["Ana", "Ben", "Cy"]\nscores = [88, 92, 79]',
     solution="grades = dict(zip(students, scores, strict=True))\nprint(grades)")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    From the price list, print the name of the cheapest product and of the
    most expensive one (use `min` / `max` with `key=`). Then print the names
    of the three most expensive products, priciest first.
""",
     given='products = [("lamp", 35), ("desk", 180), ("pen", 2), ("chair", 95), ("rug", 60)]',
     solution="cheapest = min(products, key=lambda p: p[1])\n"
              "priciest = max(products, key=lambda p: p[1])\n"
              "print(cheapest[0])\nprint(priciest[0])\n"
              "ranked = sorted(products, key=lambda p: p[1], reverse=True)\n"
              "print([p[0] for p in ranked[:3]])")

nb.q("Real-life", """
    Sort the students by grade, highest first, and for equal grades by name
    from A to Z. Print one line per student with the name and the grade.
""",
     given='students = [("Zoe", 90), ("Adam", 85), ("Mia", 90), ("Ben", 85), ("Leo", 70)]',
     solution="ranked = sorted(students, key=lambda s: (-s[1], s[0]))\n"
              "for name, grade in ranked:\n    print(name, grade)")

nb.q("Build", """
    Transpose the matrix with `zip(*matrix)` so rows become columns, and
    print the result as a list of lists. Then print the sum of each column
    of the original matrix.
""",
     given="matrix = [[1, 2, 3], [4, 5, 6]]",
     solution="flipped = [list(col) for col in zip(*matrix)]\nprint(flipped)\n"
              "print([sum(col) for col in zip(*matrix)])")

nb.q("Build", """
    Flatten the list of lists into one list of numbers with a **single**
    comprehension (two `for` clauses), keeping only the even numbers. Print it.
""",
     given="baskets = [[1, 2, 3], [4], [5, 6, 7, 8], []]",
     solution="evens = [n for basket in baskets for n in basket if n % 2 == 0]\nprint(evens)")

nb.q("Real-life", """
    The staff list is already sorted by name. Sort it by department only
    (use `operator.itemgetter` as the key), so people in the same department
    stay in name order. Print one `department name` line per person.
""",
     given='staff = [{"name": "Ada", "dept": "IT"}, {"name": "Bo", "dept": "HR"}, {"name": "Cat", "dept": "IT"}, {"name": "Dan", "dept": "HR"}, {"name": "Eve", "dept": "Ops"}]',
     solution="from operator import itemgetter\n"
              'for person in sorted(staff, key=itemgetter("dept")):\n'
              '    print(person["dept"], person["name"])')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Find the 3 most frequent words in the text: count them in a dict, then
    sort the pairs by count (highest first), and by word (A to Z) when counts
    tie. Print the three `word count` lines.
""",
     given='text = "the cat and the dog and the bird saw a cat and a dog"',
     solution="counts = {}\nfor word in text.split():\n    counts[word] = counts.get(word, 0) + 1\n"
              "ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))\n"
              "for word, n in ranked[:3]:\n    print(word, n)")

nb.q("Puzzle", """
    Group the words that are anagrams of each other (same letters). Use the
    sorted letters of a word as the dict key. Print each group as a sorted
    list, one group per line, with the groups ordered by their first word.
""",
     given='words = ["listen", "silent", "enlist", "google", "gogole", "cat", "act", "tac", "dog"]',
     solution="groups = {}\nfor word in words:\n"
              '    key = "".join(sorted(word))\n'
              "    groups.setdefault(key, []).append(word)\n"
              "result = sorted(sorted(g) for g in groups.values())\n"
              "for group in result:\n    print(group)")

nb.q("Puzzle", """
    Print the first 6 rows of Pascal's triangle, one list per row. Start from
    `[1]`; every next row starts and ends with 1 and each middle number is the
    sum of two neighbours in the previous row (a comprehension with `zip`
    over the previous row and the previous row shifted by one).
""",
     solution="row = [1]\nfor _ in range(6):\n    print(row)\n"
              "    row = [1] + [a + b for a, b in zip(row, row[1:])] + [1]")

nb.q("Real-life", """
    A shop has a table of unit prices (rows are products, columns are
    months) and a table of quantities with the same shape. Build the revenue
    matrix (price times quantity at each position) with a nested
    comprehension and `zip`, print it, then print the grand total.
""",
     given="prices = [[2, 3, 2], [10, 10, 12]]\nqty = [[5, 4, 6], [1, 2, 0]]",
     solution="revenue = [[p * q for p, q in zip(price_row, qty_row)]\n"
              "           for price_row, qty_row in zip(prices, qty)]\n"
              "print(revenue)\nprint(sum(sum(row) for row in revenue))")

# ------------------------------------------------------------ Q20 project
nb.project("Sales Report", story="""
    The regional manager sends you the quarter's sales records and wants
    ranked tables instead of a wall of numbers. Each step adds one piece of
    the report; the last step wraps it all in a function.
""",
     given='''
sales = [
    {"region": "North", "product": "lamp", "qty": 10, "price": 35},
    {"region": "South", "product": "desk", "qty": 3, "price": 180},
    {"region": "North", "product": "desk", "qty": 2, "price": 180},
    {"region": "East", "product": "pen", "qty": 120, "price": 2},
    {"region": "South", "product": "lamp", "qty": 8, "price": 35},
    {"region": "East", "product": "chair", "qty": 6, "price": 95},
    {"region": "North", "product": "pen", "qty": 90, "price": 2},
    {"region": "South", "product": "chair", "qty": 5, "price": 95},
    {"region": "East", "product": "lamp", "qty": 4, "price": 35},
    {"region": "North", "product": "chair", "qty": 3, "price": 95},
]
''',
     steps=[
         ("Build a list `revenues` with the revenue of each record (`qty` times `price`) using a comprehension. Print the number of records and the total revenue (use a generator expression or `sum`).",
          "revenues = [s[\"qty\"] * s[\"price\"] for s in sales]\nprint(len(revenues))\nprint(sum(revenues))"),
         ("Build a dict `by_region` of total revenue per region (a loop that adds to a dict is fine here, a comprehension would be harder to read). Then print the regions as ranked lines `1. North 1234`, biggest total first, ties by name.",
          "by_region = {}\nfor s in sales:\n"
          "    by_region[s[\"region\"]] = by_region.get(s[\"region\"], 0) + s[\"qty\"] * s[\"price\"]\n"
          "ranked = sorted(by_region.items(), key=lambda pair: (-pair[1], pair[0]))\n"
          "for place, (region, total) in enumerate(ranked, start=1):\n"
          "    print(f\"{place}. {region} {total}\")"),
         ("Do the same per product: build `by_product`, then print a table with the product name padded to 8 characters and the total right-aligned in 6 characters, biggest first, ties by name.",
          "by_product = {}\nfor s in sales:\n"
          "    by_product[s[\"product\"]] = by_product.get(s[\"product\"], 0) + s[\"qty\"] * s[\"price\"]\n"
          "for product, total in sorted(by_product.items(), key=lambda pair: (-pair[1], pair[0])):\n"
          "    print(f\"{product:<8}{total:>6}\")"),
         ("Print the 3 biggest single sales (by revenue), one per line as `region product revenue`. Sort the records with `operator.itemgetter` or a `key=` function, adding a `revenue` field to each record first with a list comprehension. Break ties by product name.",
          "rich = [{**s, \"revenue\": s[\"qty\"] * s[\"price\"]} for s in sales]\n"
          "top = sorted(rich, key=lambda s: (-s[\"revenue\"], s[\"product\"]))[:3]\n"
          "for s in top:\n    print(s[\"region\"], s[\"product\"], s[\"revenue\"])"),
         ("Write `report(sales)` that prints the grand total (compute it with `functools.reduce`), then each region with its share of the grand total as a percentage rounded to 1 decimal, biggest region first. Call it.",
          "from functools import reduce\n"
          "def report(sales):\n"
          "    grand = reduce(lambda total, s: total + s[\"qty\"] * s[\"price\"], sales, 0)\n"
          "    print(\"Grand total:\", grand)\n"
          "    by_region = {}\n"
          "    for s in sales:\n"
          "        by_region[s[\"region\"]] = by_region.get(s[\"region\"], 0) + s[\"qty\"] * s[\"price\"]\n"
          "    for region, total in sorted(by_region.items(), key=lambda pair: (-pair[1], pair[0])):\n"
          "        print(f\"{region}: {round(total / grand * 100, 1)}%\")\n"
          "report(sales)"),
     ])

nb.build()
