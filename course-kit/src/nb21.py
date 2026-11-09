import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB21", title="OOP Advanced", intro="""
    Making your own classes behave like built-in types: readable `repr`s,
    equality and hashing, operators, containers, properties, alternative
    constructors, dataclasses, enums, abstract classes, multiple inheritance
    and subclassing built-ins. Every question asks you to **write classes and
    use them**. Values that would come from `input()` are given to you as
    variables.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", """
    Write a class `Point` with `x` and `y` and a `__repr__` that shows text you
    could type to recreate the point, like `Point(3, 4)`. Print one point, then
    print a list holding two points.
""",
     solution='class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n'
              '    def __repr__(self):\n        return f"Point({self.x}, {self.y})"\n\n'
              'print(Point(3, 4))\nprint([Point(0, 0), Point(-1, 5)])')

nb.q("Output-match", """
    Write a class `Price` that stores an `amount`. Make it work in f-strings:
    the format spec `eur` shows two decimals followed by a space and `EUR`;
    any other spec is applied to the number itself. Print the same price once
    with `eur` and once with the spec `010.3f`.
""",
     solution='class Price:\n    def __init__(self, amount):\n        self.amount = amount\n\n'
              '    def __format__(self, spec):\n        if spec == "eur":\n            return f"{self.amount:.2f} EUR"\n'
              '        return format(self.amount, spec)\n\n'
              'p = Price(12.5)\nprint(f"{p:eur}")\nprint(f"{p:010.3f}")')

nb.q("Puzzle", """
    Tags compare **ignoring case**: write a class `Tag` where `Tag("Python")`
    equals `Tag("python")`. Build a `Tag` for each name, put them all in a
    `set`, and print the size of the set and whether `Tag("PYTHON")` is in it.
""",
     given='names = ["Python", "python", "Code", "CODE", "Bugs"]',
     solution='class Tag:\n    def __init__(self, name):\n        self.name = name.lower()\n\n'
              '    def __eq__(self, other):\n        return isinstance(other, Tag) and self.name == other.name\n\n'
              '    def __hash__(self):\n        return hash(self.name)\n\n'
              'tags = {Tag(n) for n in names}\nprint(len(tags))\nprint(Tag("PYTHON") in tags)')

nb.q("Real-life", """
    Write a class `Thermometer` whose `celsius` is a **property**: setting it
    below -273.15 raises `ValueError("below absolute zero")`. Add a read-only
    `fahrenheit` property computed from it. Create one at 25, print its
    Fahrenheit value, then try to set -300, print the error message and print
    that the temperature is still 25.
""",
     solution='class Thermometer:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n'
              '    @property\n    def celsius(self):\n        return self._celsius\n\n'
              '    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError("below absolute zero")\n'
              '        self._celsius = value\n\n'
              '    @property\n    def fahrenheit(self):\n        return self._celsius * 9 / 5 + 32\n\n'
              't = Thermometer(25)\nprint(t.fahrenheit)\n'
              'try:\n    t.celsius = -300\nexcept ValueError as error:\n    print("Rejected:", error)\nprint(t.celsius)')

nb.q("Real-life", """
    A ticket queue at a help desk: write `TicketQueue` holding a list of
    waiting names (passed to `__init__`) so that `len(queue)` is the number
    waiting. Print the length of a queue with three people, then print whether
    an empty queue counts as `True` or `False` in a condition (use `bool()`).
""",
     solution='class TicketQueue:\n    def __init__(self, waiting):\n        self.waiting = list(waiting)\n\n'
              '    def __len__(self):\n        return len(self.waiting)\n\n'
              'print(len(TicketQueue(["Ana", "Ben", "Cy"])))\nprint(bool(TicketQueue([])))')

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    A game moves things around with vectors. Write `Vector` with `x` and `y`,
    a `__repr__` like `Vector(4, 6)`, `+` between two vectors and `*` by a
    number. Print `a + b` and `a * 3`.
""",
     solution='class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n'
              '    def __repr__(self):\n        return f"Vector({self.x}, {self.y})"\n\n'
              '    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\n'
              '    def __mul__(self, factor):\n        return Vector(self.x * factor, self.y * factor)\n\n'
              'a = Vector(1, 2)\nb = Vector(3, 4)\nprint(a + b)\nprint(a * 3)')

nb.q("Puzzle", """
    Write `Cash` (an `amount` in euros, `__repr__` like `Cash(12)`) whose `+`
    works only between two `Cash` objects. For anything else `__add__` must
    **return** the special value that lets Python raise its normal `TypeError`.
    Print `Cash(5) + Cash(7)`, then try `Cash(5) + "x"` and print
    `cannot add` when that fails.
""",
     solution='class Cash:\n    def __init__(self, amount):\n        self.amount = amount\n\n'
              '    def __repr__(self):\n        return f"Cash({self.amount})"\n\n'
              '    def __add__(self, other):\n        if not isinstance(other, Cash):\n            return NotImplemented\n'
              '        return Cash(self.amount + other.amount)\n\n'
              'print(Cash(5) + Cash(7))\n'
              'try:\n    Cash(5) + "x"\nexcept TypeError:\n    print("cannot add")')

nb.q("Real-life", """
    A teacher wants to call `sum()` on a list of `Score` objects (each has a
    `value`, and `__repr__` like `Score(9)`). Write `Score` so that `+` gives a
    new `Score` and `sum(scores)` works, even though `sum` starts from the
    plain number 0. Print the total of the given scores.
""",
     solution='class Score:\n    def __init__(self, value):\n        self.value = value\n\n'
              '    def __repr__(self):\n        return f"Score({self.value})"\n\n'
              '    def __add__(self, other):\n        if not isinstance(other, Score):\n            return NotImplemented\n'
              '        return Score(self.value + other.value)\n\n'
              '    def __radd__(self, other):\n        if other == 0:\n            return self\n        return NotImplemented\n\n'
              'scores = [Score(4), Score(9), Score(7)]\nprint(sum(scores))')

nb.q("Real-life", """
    Write `Inventory` wrapping a dict of stock counts, so a shop can use it
    like a container: `inv["apple"] = 5` stores, `inv["apple"]` reads,
    `"apple" in inv` tests, `len(inv)` counts the products and a `for` loop
    over it visits the product names. Its truth value must be `True` only if
    some product has stock above 0. Set three products, loop over it, print
    the length and a membership test, then print the truth value of an
    inventory whose products are all at 0.
""",
     solution='class Inventory:\n    def __init__(self):\n        self._stock = {}\n\n'
              '    def __setitem__(self, name, count):\n        self._stock[name] = count\n\n'
              '    def __getitem__(self, name):\n        return self._stock[name]\n\n'
              '    def __contains__(self, name):\n        return name in self._stock\n\n'
              '    def __len__(self):\n        return len(self._stock)\n\n'
              '    def __iter__(self):\n        return self._stock.__iter__()\n\n'
              '    def __bool__(self):\n        return any(count > 0 for count in self._stock.values())\n\n'
              'inv = Inventory()\ninv["apple"] = 5\ninv["pear"] = 0\ninv["fig"] = 12\n'
              'for name in inv:\n    print(name, inv[name])\n'
              'print(len(inv), "pear" in inv, "kiwi" in inv)\n'
              'empty = Inventory()\nempty["apple"] = 0\nprint(bool(empty))')

nb.q("Real-life", """
    Write a class `VAT` that is built with a rate and can then be **called like
    a function**: `vat(10.0)` returns the price with VAT added, rounded to 2
    decimals. Use a 20% rate and apply it to every price in the list with
    `map`; print the results as a list.
""",
     given="prices = [10.0, 25.5, 99.99]",
     solution='class VAT:\n    def __init__(self, rate):\n        self.rate = rate\n\n'
              '    def __call__(self, price):\n        return round(price * (1 + self.rate), 2)\n\n'
              'vat = VAT(0.20)\nprint(list(map(vat, prices)))')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Write a class `Duration` that stores total `minutes`. Give it a
    **classmethod** `from_text` that builds one from text like `"2h 15m"`, a
    **staticmethod** `pad(n)` returning a number as two digits (`5` becomes
    `"05"`), a computed property `hours` (minutes divided by 60, rounded to 2
    decimals) and a `__str__` that shows `HH:MM`, using `pad`. Build durations
    from the given texts and print each one with its hours.
""",
     given='texts = ["2h 15m", "0h 45m", "10h 5m"]',
     solution='class Duration:\n    def __init__(self, minutes):\n        self.minutes = minutes\n\n'
              '    @classmethod\n    def from_text(cls, text):\n        hours, minutes = text.split()\n'
              '        return cls(int(hours[:-1]) * 60 + int(minutes[:-1]))\n\n'
              '    @staticmethod\n    def pad(n):\n        return str(n).zfill(2)\n\n'
              '    @property\n    def hours(self):\n        return round(self.minutes / 60, 2)\n\n'
              '    def __str__(self):\n        return Duration.pad(self.minutes // 60) + ":" + Duration.pad(self.minutes % 60)\n\n'
              'for text in texts:\n    d = Duration.from_text(text)\n    print(d, d.hours)')

nb.q("Real-life", """
    Version numbers must sort by their numbers, not as text (`"1.10"` is newer
    than `"1.9"`). Write `Version` built from text like `"1.10.2"`, with `==`
    and `<` defined by hand and the other comparisons filled in with the
    `total_ordering` decorator. `str(version)` gives the original text. Print
    the given versions sorted from oldest to newest, then the newest one.
""",
     given='texts = ["1.9.0", "1.10.2", "1.2.11", "0.9.9", "1.10.0"]',
     solution='from functools import total_ordering\n\n\n'
              '@total_ordering\nclass Version:\n    def __init__(self, text):\n        self.text = text\n'
              '        self.parts = tuple(int(p) for p in text.split("."))\n\n'
              '    def __eq__(self, other):\n        return self.parts == other.parts\n\n'
              '    def __lt__(self, other):\n        return self.parts < other.parts\n\n'
              '    def __str__(self):\n        return self.text\n\n'
              'versions = [Version(t) for t in texts]\n'
              'print([str(v) for v in sorted(versions)])\nprint(max(versions))')

nb.q("Real-life", """
    Write a dataclass `Student` using `slots=True` and `kw_only=True`, with a
    `name`, a list of `grades` that starts empty for every student (no shared
    list!) and a `__post_init__` that turns the name into title case. Create
    two students from the given names, add a grade to the first only, print
    both, and print whether their `grades` lists are the same object.
""",
     given='name_a = "ada lovelace"\nname_b = "alan turing"',
     solution='from dataclasses import dataclass, field\n\n\n'
              '@dataclass(slots=True, kw_only=True)\nclass Student:\n    name: str\n'
              '    grades: list = field(default_factory=list)\n\n'
              '    def __post_init__(self):\n        self.name = self.name.title()\n\n'
              'a = Student(name=name_a)\nb = Student(name=name_b)\na.grades.append(90)\n'
              'print(a)\nprint(b)\nprint(a.grades is b.grades)')

nb.q("Real-life", """
    A calendar needs appointments that can be sorted, de-duplicated and never
    changed by accident. Write a **frozen**, **ordered** dataclass `Slot` with
    `day`, `hour` and `title` (in that order). From the given list, print the
    sorted list of unique slots. Then use `copy.replace` to make a copy of the
    first slot of the original list moved to hour 16 and print it, and print
    `frozen` when assigning to a field of a slot fails.
""",
     given='from dataclasses import dataclass\n\nbookings = [(2, 14, "dentist"), (1, 9, "standup"), (2, 10, "gym"), (1, 9, "standup")]',
     solution='import copy\nfrom dataclasses import dataclass, FrozenInstanceError\n\n\n'
              '@dataclass(frozen=True, order=True)\nclass Slot:\n    day: int\n    hour: int\n    title: str\n\n'
              'slots = [Slot(*b) for b in bookings]\nprint(sorted(set(slots)))\n'
              'print(copy.replace(slots[0], hour=16))\n'
              'try:\n    slots[0].hour = 1\nexcept FrozenInstanceError:\n    print("frozen")')

nb.q("Real-life", """
    A to-do app. Write an `IntEnum` `Priority` (LOW=1, MEDIUM=2, HIGH=3) and a
    `StrEnum` `Status` with members `TODO` and `DONE` whose values are filled
    in by `auto()`. Turn the priority names in `tasks` into `Priority`
    members, print the tasks from most to least important (ties keep their
    original order) as `HIGH: write report`, then print whether
    `Status.DONE == "done"`.
""",
     given='tasks = [("write report", "HIGH"), ("water plants", "LOW"), ("pay rent", "HIGH"), ("call mum", "MEDIUM")]',
     solution='from enum import IntEnum, StrEnum, auto\n\n\n'
              'class Priority(IntEnum):\n    LOW = 1\n    MEDIUM = 2\n    HIGH = 3\n\n\n'
              'class Status(StrEnum):\n    TODO = auto()\n    DONE = auto()\n\n\n'
              'ordered = sorted(tasks, key=lambda task: Priority[task[1]], reverse=True)\n'
              'for title, level in ordered:\n    print(Priority[level].name + ": " + title)\n'
              'print(Status.DONE == "done")')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    The diamond. Write classes `A`, `B`, `C` and `D` where `B` and `C` both
    inherit from `A`, and `D` inherits from `B` then `C`. Each class has a
    method `setup(log)` that appends its own class name to `log`, then
    cooperatively calls `super().setup(log)` (except `A`, which only
    appends). Print the class names in the method resolution order of `D`, then
    call `D().setup(log)` on an empty list and print the log.
""",
     solution='class A:\n    def setup(self, log):\n        log.append("A")\n\n\n'
              'class B(A):\n    def setup(self, log):\n        log.append("B")\n        super().setup(log)\n\n\n'
              'class C(A):\n    def setup(self, log):\n        log.append("C")\n        super().setup(log)\n\n\n'
              'class D(B, C):\n    def setup(self, log):\n        log.append("D")\n        super().setup(log)\n\n\n'
              'print([cls.__name__ for cls in D.__mro__])\n'
              'log = []\nD().setup(log)\nprint(log)')

nb.q("Real-life", """
    A drawing app. Write an abstract base class `Shape` (use `ABC`) with an
    abstract method `area()` and a normal method `describe()` returning
    `"<ClassName> with area <area rounded to 2 decimals>"`. Add `Circle(radius)`
    (use 3.14159 for pi) and `Square(side)`. Print that `Shape()` cannot be
    created (catch the `TypeError`, print `abstract`), then print the
    description of every shape in the given list.
""",
     given='sizes = [("circle", 2), ("square", 3), ("circle", 0.5)]',
     solution='from abc import ABC, abstractmethod\n\n\n'
              'class Shape(ABC):\n    @abstractmethod\n    def area(self):\n        ...\n\n'
              '    def describe(self):\n        return type(self).__name__ + " with area " + str(round(self.area(), 2))\n\n\n'
              'class Circle(Shape):\n    def __init__(self, radius):\n        self.radius = radius\n\n'
              '    def area(self):\n        return 3.14159 * self.radius ** 2\n\n\n'
              'class Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n'
              '    def area(self):\n        return self.side ** 2\n\n\n'
              'try:\n    Shape()\nexcept TypeError:\n    print("abstract")\n'
              'for kind, size in sizes:\n    shape = Circle(size) if kind == "circle" else Square(size)\n    print(shape.describe())')

nb.q("Puzzle", """
    File permissions as flags. Write a `Flag` enum `Perm` with `READ`, `WRITE`
    and `EXEC` (use `auto()`). A user starts with `READ | WRITE`. Print whether
    `WRITE` and `EXEC` are in the user's permissions, then give the user
    `EXEC` and take `WRITE` away (with `|=` and `&= ~`). Finally print the
    result as a string of `r`, `w`, `x` with `-` for a missing flag.
""",
     solution='from enum import Flag, auto\n\n\n'
              'class Perm(Flag):\n    READ = auto()\n    WRITE = auto()\n    EXEC = auto()\n\n\n'
              'user = Perm.READ | Perm.WRITE\n'
              'print(Perm.WRITE in user, Perm.EXEC in user)\n'
              'user |= Perm.EXEC\nuser &= ~Perm.WRITE\n'
              'letters = ""\n'
              'for perm, letter in zip(Perm, "rwx"):\n    letters += letter if perm in user else "-"\n'
              'print(letters)')

nb.q("Real-life", """
    HTTP header names ignore case. Subclass `UserDict` (not `dict`) into
    `Headers`, so every way of storing, reading and testing a key lower-cases
    it first: `h["Content-Type"] = ...`, `h["content-type"]`, `"ACCEPT" in h`
    and `h.update({...})` must all agree. Store a content type, update with an
    upper-case `ACCEPT` key, then print the content type read with a different
    case, whether `"Accept"` is in the headers, and the sorted keys.
""",
     solution='from collections import UserDict\n\n\n'
              'class Headers(UserDict):\n    def __setitem__(self, key, value):\n        super().__setitem__(key.lower(), value)\n\n'
              '    def __getitem__(self, key):\n        return super().__getitem__(key.lower())\n\n'
              '    def __contains__(self, key):\n        return super().__contains__(key.lower())\n\n\n'
              'h = Headers()\nh["Content-Type"] = "text/html"\nh.update({"ACCEPT": "*/*"})\n'
              'print(h["content-TYPE"])\nprint("Accept" in h)\nprint(sorted(h))')

# ------------------------------------------------------------ Q20 story project
nb.project("Money Library", story="""
    The *Globe Shop* sells in three currencies and keeps messing up its totals
    with floats and loose numbers. You will build a tiny money library: a
    currency enum, a safe `Money` type with operators, a converter and a
    shopping basket. Each step builds on the one before.
""",
     given='RATES = {"EUR": "1", "USD": "0.92", "GBP": "1.17"}   # value of 1 unit in EUR\n'
           'purchases = [("coffee beans", "12.50", "EUR"), ("headphones", "89.99", "USD"),\n'
           '             ("book", "15.00", "GBP"), ("stickers", "3.20", "EUR")]',
     steps=[
         ("Create a `StrEnum` `Currency` with members `EUR`, `USD` and `GBP` (values are the same "
          "text). Print the list of values, then try `Currency(\"JPY\")` and print `unknown currency` "
          "when it fails.",
          "from decimal import Decimal\nfrom enum import StrEnum\n\n\n"
          "class Currency(StrEnum):\n    EUR = \"EUR\"\n    USD = \"USD\"\n    GBP = \"GBP\"\n\n\n"
          "print([c.value for c in Currency])\n"
          "try:\n    Currency(\"JPY\")\nexcept ValueError:\n    print(\"unknown currency\")"),
         ("Write a frozen dataclass `Money(amount, currency)` where `amount` must be a `Decimal` "
          "(otherwise `TypeError`). Support `+` (same currency only, else `ValueError`; other types "
          "return `NotImplemented`), `__radd__` so `sum()` works, `*` by an `int`, `<` (plus "
          "`total_ordering`) and a `__str__` like `12.50 EUR`. Print a sum of two, the sum of a "
          "list, a product, the larger of two, and the two error messages' types.",
          "from dataclasses import dataclass\nfrom functools import total_ordering\n\n\n"
          "@total_ordering\n@dataclass(frozen=True)\nclass Money:\n"
          "    amount: Decimal\n    currency: Currency\n\n"
          "    def __post_init__(self):\n        if not isinstance(self.amount, Decimal):\n"
          "            raise TypeError(\"amount must be a Decimal\")\n\n"
          "    def __add__(self, other):\n        if not isinstance(other, Money):\n            return NotImplemented\n"
          "        if self.currency != other.currency:\n            raise ValueError(\"currency mismatch\")\n"
          "        return Money(self.amount + other.amount, self.currency)\n\n"
          "    def __radd__(self, other):\n        return self if other == 0 else NotImplemented\n\n"
          "    def __mul__(self, factor):\n        if not isinstance(factor, int):\n            return NotImplemented\n"
          "        return Money(self.amount * factor, self.currency)\n\n"
          "    def __lt__(self, other):\n        return self.amount < other.amount\n\n"
          "    def __str__(self):\n        return f\"{self.amount:.2f} {self.currency}\"\n\n\n"
          "a = Money(Decimal(\"12.50\"), Currency.EUR)\nb = Money(Decimal(\"3.20\"), Currency.EUR)\n"
          "print(a + b)\nprint(sum([a, b, a]))\nprint(b * 3)\nprint(max(a, b))\n"
          "for bad in (lambda: a + Money(Decimal(\"1\"), Currency.USD), lambda: Money(1.5, Currency.EUR)):\n"
          "    try:\n        bad()\n    except (ValueError, TypeError) as error:\n        print(type(error).__name__)"),
         ("Write `convert(money, target)` that changes a `Money` into the target currency using "
          "`RATES` (value in EUR, as `Decimal`), rounded to 2 decimals with `quantize(Decimal(\"0.01\"))`. "
          "Build `items`, a list of `(name, Money)` from `purchases`, and print every item "
          "converted to EUR as `name: amount`.",
          "def convert(money, target):\n    in_eur = money.amount * Decimal(RATES[money.currency])\n"
          "    amount = (in_eur / Decimal(RATES[target])).quantize(Decimal(\"0.01\"))\n"
          "    return Money(amount, target)\n\n\n"
          "items = [(name, Money(Decimal(price), Currency(code))) for name, price, code in purchases]\n"
          "for name, money in items:\n    print(name + \": \" + str(convert(money, Currency.EUR)))"),
         ("Write a `SummaryMixin` whose `summary()` returns `<ClassName>: <n> items, total <total>`, "
          "and a `Basket(SummaryMixin)` that behaves like a container of `name -> Money`: "
          "`[]` read and write, `in`, `len`, and a `total` property (everything converted to EUR "
          "and summed, starting from zero euros). Fill a basket from `items` and print its summary, "
          "`\"book\" in basket` and `basket[\"book\"]`.",
          "class SummaryMixin:\n    def summary(self):\n"
          "        return f\"{type(self).__name__}: {len(self)} items, total {self.total}\"\n\n\n"
          "class Basket(SummaryMixin):\n    def __init__(self):\n        self.items = {}\n\n"
          "    def __setitem__(self, name, money):\n        self.items[name] = money\n\n"
          "    def __getitem__(self, name):\n        return self.items[name]\n\n"
          "    def __contains__(self, name):\n        return name in self.items\n\n"
          "    def __len__(self):\n        return len(self.items)\n\n"
          "    @property\n    def total(self):\n        zero = Money(Decimal(\"0\"), Currency.EUR)\n"
          "        return sum((convert(m, Currency.EUR) for m in self.items.values()), zero)\n\n\n"
          "basket = Basket()\nfor name, money in items:\n    basket[name] = money\n"
          "print(basket.summary())\nprint(\"book\" in basket)\nprint(basket[\"book\"])"),
         ("Print the shop's receipt: the items sorted from most to least expensive **in EUR**, one "
          "per line as `name: <original price> = <price in EUR>`, then the line `TOTAL: <total>`.",
          "ranked = sorted(basket.items.items(), key=lambda pair: convert(pair[1], Currency.EUR), reverse=True)\n"
          "for name, money in ranked:\n    print(f\"{name}: {money} = {convert(money, Currency.EUR)}\")\n"
          "print(\"TOTAL:\", basket.total)"),
     ])

nb.build()
