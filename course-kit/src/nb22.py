import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB22", title="Iterators & Generators", intro="""
    What a `for` loop really does with `iter()` and `next()`, how to write
    your own iterators, and how generator functions produce values one at a
    time without building whole lists. You will build lazy pipelines, push
    values **into** generators with `send()`, and finish with a streaming
    CSV transformer. Data that would come from files or sensors is given to
    you in the cell.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "Customers wait in `queue`. Get an iterator from it and serve two customers: print the result of `next()` twice.",
     given='queue = ["Ana", "Ben", "Cy"]',
     solution="line = iter(queue)\nprint(next(line))\nprint(next(line))")

nb.q("Puzzle", "`readings` is an iterator. Print the sum of it, then on the next line print the list made from the same iterator.",
     given="readings = iter([4, 8, 15])",
     solution="print(sum(readings))\nprint(list(readings))")

nb.q("Output-match", "Call `next()` four times on `letters`, printing each result. When it runs out, it must print `empty` instead of crashing.",
     given='letters = iter(["a", "b", "c"])',
     solution='for _ in range(4):\n    print(next(letters, "empty"))')

nb.q("Build", "Write a generator function `countdown(n)` that yields `n`, `n - 1`, ... down to 1. Print `list(countdown(5))`.",
     solution="def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\nprint(list(countdown(5)))")

nb.q("Output-match", "Print two booleans on one line: whether the list `numbers` has a `__next__` method, and whether `iter(numbers)` has one.",
     given="numbers = [1, 2, 3]",
     solution='print(hasattr(numbers, "__next__"), hasattr(iter(numbers), "__next__"))')

# ------------------------------------------------------------ Combine
nb.q("Puzzle", """
    Write a generator function `greeter()` that prints `starting up` and then
    yields `"ready"`. Create the generator object, print `created`, then print
    the result of `next()` on it. The expected output shows when the body runs.
""",
     solution='def greeter():\n    print("starting up")\n    yield "ready"\n'
              'gen = greeter()\nprint("created")\nprint(next(gen))')

nb.q("Real-life", """
    Write an endless generator `fibonacci()` (1, 1, 2, 3, 5, ...). Use
    `itertools.islice` to print the first 10 numbers as a list.
""",
     solution="from itertools import islice\n"
              "def fibonacci():\n    a, b = 1, 1\n    while True:\n        yield a\n        a, b = b, a + b\n"
              "print(list(islice(fibonacci(), 10)))")

nb.q("Build", """
    Loop over `tickets` the way a `for` loop does it inside: get an iterator
    with `iter()`, then use `while True` with `next()`, and stop by catching
    `StopIteration`. Print each ticket.
""",
     given='tickets = ["T-101", "T-102", "T-103"]',
     solution="it = iter(tickets)\n"
              "while True:\n    try:\n        print(next(it))\n    except StopIteration:\n        break")

nb.q("Real-life", """
    A shop's `prices` are sorted from cheapest to most expensive. Use
    `itertools.takewhile` to print the list of prices that are 10 or less.
""",
     given="prices = [2.5, 4, 7.5, 10, 12, 30, 45]",
     solution="from itertools import takewhile\nprint(list(takewhile(lambda price: price <= 10, prices)))")

nb.q("Real-life", """
    A log export starts with comment lines beginning with `#`. Use
    `itertools.dropwhile` to skip them and print the remaining lines, one per
    line.
""",
     given='lines = ["# exported 2024", "# server a", "login ok", "# note", "logout"]',
     solution="from itertools import dropwhile\n"
              'for line in dropwhile(lambda text: text.startswith("#"), lines):\n    print(line)')

# ------------------------------------------------------------ Small real tasks
nb.q("Build", """
    Write an iterator **class** `Countdown` whose `__init__` takes a start
    number and whose `__iter__` returns itself and `__next__` returns the next
    smaller number, raising `StopIteration` after 1. Print `list(Countdown(3))`.
    Then create one `Countdown(3)` object and print `list()` of that same object
    twice.
""",
     solution="class Countdown:\n"
              "    def __init__(self, start):\n        self.current = start\n"
              "    def __iter__(self):\n        return self\n"
              "    def __next__(self):\n"
              "        if self.current < 1:\n            raise StopIteration\n"
              "        value = self.current\n        self.current -= 1\n        return value\n"
              "print(list(Countdown(3)))\ntimer = Countdown(3)\nprint(list(timer))\nprint(list(timer))")

nb.q("Real-life", """
    `shelves` maps a shelf name to its books. Write a generator `all_books(shelves)`
    that uses `yield from` to produce every book on every shelf, in order.
    Print the list of all books.
""",
     given='shelves = {"fiction": ["Dune", "Emma"], "science": ["Cosmos"], "poetry": ["Odes", "Howl"]}',
     solution="def all_books(shelves):\n    for books in shelves.values():\n        yield from books\n"
              "print(list(all_books(shelves)))")

nb.q("Real-life", """
    Build a lazy pipeline of two generator functions over `lines`: `parse(lines)`
    yields `(level, message)` pairs by splitting each line at its first `:`,
    and `only_errors(pairs)` yields the messages whose level is `ERROR`. Print
    each error message, then the number of errors.
""",
     given='lines = ["INFO:server started", "ERROR:disk full", "WARN:slow response", "ERROR:timeout", "INFO:done"]',
     solution="def parse(lines):\n    for line in lines:\n        level, message = line.split(\":\", 1)\n        yield level, message\n"
              "def only_errors(pairs):\n    for level, message in pairs:\n        if level == \"ERROR\":\n            yield message\n"
              "errors = list(only_errors(parse(lines)))\nfor message in errors:\n    print(message)\nprint(len(errors))")

nb.q("Real-life", """
    Each `orders` entry is a `(price, quantity)` pair. Use `itertools.starmap`
    to compute the total of every order lazily, then print the list of totals
    and their sum.
""",
     given="orders = [(2.5, 4), (10, 3), (0.75, 8), (4, 1)]",
     solution="from itertools import starmap\n"
              "totals = list(starmap(lambda price, qty: price * qty, orders))\nprint(totals)\nprint(sum(totals))")

nb.q("Real-life", """
    `sensor()` is a generator of temperatures and it can only be read once.
    Use `itertools.tee` to make two independent copies so that you can print
    the highest temperature from one copy and the average of the other (to 1
    decimal place).
""",
     given="def sensor():\n    for value in [18.5, 21.0, 19.5, 24.5, 22.0]:\n        yield value\n\nreadings = sensor()",
     solution="from itertools import tee\n"
              "for_max, for_avg = tee(readings)\n"
              "print(max(for_max))\n"
              "values = list(for_avg)\n"
              "print(round(sum(values) / len(values), 1))")

# ------------------------------------------------------------ Puzzles & builds
nb.q("Build", """
    Write a generator-based coroutine `running_average()` that keeps a total
    and a count. Each time a number is sent in with `send()`, it yields the
    average so far. Prime it with `next()`, send 10, 20 and 60, and print each
    average (rounded to 1 decimal place).
""",
     solution="def running_average():\n"
              "    total = 0\n    count = 0\n    average = None\n"
              "    while True:\n"
              "        number = yield average\n"
              "        total += number\n        count += 1\n        average = total / count\n"
              "avg = running_average()\nnext(avg)\n"
              "for number in [10, 20, 60]:\n    print(round(avg.send(number), 1))")

nb.q("Puzzle", """
    A generator can also `return` a value. Write `read_words(lines)` that
    yields every word from the lines, and when finished returns the number of
    lines it processed. Loop with `next()` and catch `StopIteration` to print
    each word, then print the returned line count from the exception's `value`.
""",
     given='lines = ["red green", "blue", "pink black white"]',
     solution="def read_words(lines):\n    count = 0\n    for line in lines:\n        count += 1\n        yield from line.split()\n    return count\n"
              "gen = read_words(lines)\n"
              "while True:\n    try:\n        print(next(gen))\n    except StopIteration as stop:\n        print(\"lines:\", stop.value)\n        break")

nb.q("Puzzle", """
    Write a generator `worker()` that yields `"waiting"` in a loop. If a
    `ValueError` is thrown into it, it should yield `"reset"` and carry on; in
    a `finally` block it prints `cleanup` when it is closed. Start it with
    `next()`, print the value, `throw(ValueError)` into it and print what comes
    back, then `close()` it.
""",
     solution="def worker():\n"
              "    try:\n        while True:\n            try:\n                yield \"waiting\"\n"
              "            except ValueError:\n                yield \"reset\"\n"
              "    finally:\n        print(\"cleanup\")\n"
              "job = worker()\nprint(next(job))\nprint(job.throw(ValueError))\njob.close()")

nb.q("Puzzle", """
    Print the first 10 numbers that are multiples of 3 **or** 5 in
    increasing order, each only once (3, 5, 6, 9, 10, ...). Write an endless
    generator `multiples(step)` and a generator `merge(a, b)` that lazily
    merges two sorted endless generators, skipping duplicates. Use
    `itertools.islice` to take 10.
""",
     solution="from itertools import islice\n"
              "def multiples(step):\n    n = step\n    while True:\n        yield n\n        n += step\n"
              "def merge(a, b):\n"
              "    x = next(a)\n    y = next(b)\n"
              "    while True:\n"
              "        if x < y:\n            yield x\n            x = next(a)\n"
              "        elif y < x:\n            yield y\n            y = next(b)\n"
              "        else:\n            yield x\n            x = next(a)\n            y = next(b)\n"
              "print(list(islice(merge(multiples(3), multiples(5)), 10)))")

# ------------------------------------------------------------ Q20 project
nb.project("Streaming Sales Report", story="""
    A chain of shops exports `sales.csv`, and the real file has millions of
    rows, so you must **never** load it all into a list. You'll build a
    pipeline of generators that reads, cleans, filters, summarises and
    writes a report one row at a time. The first cell writes a small sample
    file so you can test it.
""",
     given='import csv\nimport os\nimport tempfile\n\n'
           'tmp = tempfile.TemporaryDirectory()\n'
           'path = os.path.join(tmp.name, "sales.csv")\n'
           'report_path = os.path.join(tmp.name, "report.csv")\n'
           'with open(path, "w", newline="") as f:\n'
           '    f.write("store,product,qty,price,status\\n")\n'
           '    f.write("north,tea,4,2.50,paid\\n")\n'
           '    f.write("south,cake,2,4.75,paid\\n")\n'
           '    f.write("north,coffee,,3.20,paid\\n")\n'
           '    f.write("east,tea,10,2.50,refunded\\n")\n'
           '    f.write("south,coffee,6,3.20,paid\\n")\n'
           '    f.write("north,cake,1,4.75,paid\\n")\n'
           '    f.write("east,coffee,3,3.20,paid\\n")\n'
           '    f.write("south,tea,x,2.50,paid\\n")\n'
           '    f.write("east,cake,5,4.75,paid\\n")',
     steps=[
         ("Write a generator `read_rows(path)` that opens the file and yields one "
          "`csv.DictReader` row at a time. Print the first 2 rows' `store` and `product` "
          "(use `itertools.islice`, not a list).",
          "from itertools import islice\n"
          "def read_rows(path):\n"
          "    with open(path, newline=\"\") as f:\n"
          "        for row in csv.DictReader(f):\n"
          "            yield row\n"
          "for row in islice(read_rows(path), 2):\n"
          "    print(row[\"store\"], row[\"product\"])"),
         ("Write a generator `parse(rows)` that yields a new dict for every row with "
          "`qty` as an int, `price` as a float and a `total` (qty times price). Rows with "
          "a missing or invalid quantity must be skipped (catch `ValueError`). Print how "
          "many good rows there are.",
          "def parse(rows):\n"
          "    for row in rows:\n"
          "        try:\n"
          "            qty = int(row[\"qty\"])\n"
          "        except ValueError:\n"
          "            continue\n"
          "        price = float(row[\"price\"])\n"
          "        yield {\"store\": row[\"store\"], \"product\": row[\"product\"],\n"
          "               \"status\": row[\"status\"], \"qty\": qty, \"total\": qty * price}\n"
          "print(sum(1 for sale in parse(read_rows(path))))"),
         ("Write a generator `paid_only(sales)` that yields only the sales whose status "
          "is `paid`. Print each paid sale as `store product total` (total with 2 decimal "
          "places), one per line, from the full pipeline.",
          "def paid_only(sales):\n"
          "    for sale in sales:\n"
          "        if sale[\"status\"] == \"paid\":\n"
          "            yield sale\n"
          "for sale in paid_only(parse(read_rows(path))):\n"
          "    print(sale[\"store\"], sale[\"product\"], f\"{sale['total']:.2f}\")"),
         ("Consume the pipeline once with a single loop and add up the paid totals per "
          "store in a dict. Print the stores in alphabetical order with their totals "
          "(2 decimal places), and the grand total on the last line.",
          "totals = {}\n"
          "for sale in paid_only(parse(read_rows(path))):\n"
          "    totals[sale[\"store\"]] = totals.get(sale[\"store\"], 0) + sale[\"total\"]\n"
          "for store in sorted(totals):\n"
          "    print(store, f\"{totals[store]:.2f}\")\n"
          "print(\"all\", f\"{sum(totals.values()):.2f}\")"),
         ("Write a generator `report_lines(sales)` that yields a CSV line "
          "`store,product,total` (total with 2 decimal places) for each paid sale. Write "
          "them to `report_path` one at a time while looping, never building a list, then "
          "read the file back and print it.",
          "def report_lines(sales):\n"
          "    yield \"store,product,total\"\n"
          "    for sale in sales:\n"
          "        yield f\"{sale['store']},{sale['product']},{sale['total']:.2f}\"\n"
          "with open(report_path, \"w\") as out:\n"
          "    for line in report_lines(paid_only(parse(read_rows(path)))):\n"
          "        out.write(line + \"\\n\")\n"
          "with open(report_path) as f:\n"
          "    print(f.read().rstrip())\n"
          "tmp.cleanup()"),
     ])

nb.build()
