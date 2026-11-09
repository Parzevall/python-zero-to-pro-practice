import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB26", title="Type Hints", intro="""
    Type hints say what kind of value a name should hold, and Python never
    checks them while the program runs. Tools like mypy catch mistakes before
    you run anything. But the hints are still real objects at runtime, so you
    can read them with `typing.get_type_hints`, `get_origin` and `get_args`,
    and use them to validate real data. Every task here prints something that
    depends on that runtime behaviour: reading hints, `isinstance` checks
    against a `@runtime_checkable` Protocol, generics, and small validators.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Output-match", """
    `price_with_tax` is already annotated. Print the dictionary that
    `typing.get_type_hints` returns for it.
""",
     given="def price_with_tax(price: float, rate: float, rounded: bool = True) -> float:\n"
           "    total = price * (1 + rate)\n"
           "    return round(total, 2) if rounded else total",
     solution="import typing\n\nprint(typing.get_type_hints(price_with_tax))")

nb.q("Puzzle", """
    The hint on `double` says `int`, but the shop's form sent text. Call it
    with `"ab"` and print the result, then print whether `"ab"` is an
    instance of `int`.
""",
     given="def double(n: int) -> int:\n    return n * 2",
     solution='print(double("ab"))\nprint(isinstance("ab", int))')

nb.q("Output-match", """
    A table of scores per student is typed as `dict[str, list[int]]`. Print its origin
    (the plain class) and then its arguments, each on its own line.
""",
     given="from typing import get_origin, get_args\n\nscores_hint = dict[str, list[int]]",
     solution="print(get_origin(scores_hint))\nprint(get_args(scores_hint))")

nb.q("Puzzle", """
    Someone wants to check that `grades` is a `list[int]` with
    `isinstance(grades, list[int])`. Try it, catch the `TypeError` and print
    `cannot check`. Then check it properly: print `True` if `grades` is a list
    and every item is an `int`.
""",
     given="grades = [90, 85, 77]",
     solution="try:\n"
              "    isinstance(grades, list[int])\n"
              "except TypeError:\n"
              '    print("cannot check")\n'
              "print(isinstance(grades, list) and all(isinstance(g, int) for g in grades))")

nb.q("Puzzle", """
    A user's nickname is typed `str | None`. Print the names of the two types
    inside that hint, in the order they were written, as a list of strings.
""",
     given="from typing import get_args\n\nnickname_hint = str | None",
     solution="print([t.__name__ for t in get_args(nickname_hint)])")

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    A drawing app accepts "anything with an `.area()` method". Make a
    `HasArea` Protocol that can be used with `isinstance`, then print, one per
    line, whether `circle`, `square` and `rock` are instances of it.
""",
     given="class Circle:\n"
           "    def __init__(self, r):\n"
           "        self.r = r\n"
           "    def area(self):\n"
           "        return 3.14 * self.r ** 2\n\n"
           "class Square:\n"
           "    def __init__(self, side):\n"
           "        self.side = side\n"
           "    def area(self):\n"
           "        return self.side ** 2\n\n"
           "class Rock:\n"
           "    weight = 12\n\n"
           "circle, square, rock = Circle(1), Square(2), Rock()",
     solution="from typing import Protocol, runtime_checkable\n\n"
              "@runtime_checkable\n"
              "class HasArea(Protocol):\n"
              "    def area(self) -> float: ...\n\n"
              "for shape in (circle, square, rock):\n"
              "    print(isinstance(shape, HasArea))")

nb.q("Real-life", """
    A signup form record must match the `User` TypedDict. Print the required
    keys that are missing from `record` and then the keys that `User` doesn't
    know about, each as a sorted list.
""",
     given="from typing import TypedDict\n\n"
           "class User(TypedDict):\n"
           "    name: str\n"
           "    email: str\n"
           "    age: int\n\n"
           'record = {"name": "Mia", "age": 31, "nickname": "mimi"}',
     solution="known = set(User.__annotations__)\n"
              "print(sorted(User.__required_keys__ - set(record)))\n"
              "print(sorted(set(record) - known))")

nb.q("Real-life", """
    An order's status must be one of the values allowed by the `Status`
    Literal. Print the order ids whose status is not allowed, as a list.
""",
     given="from typing import Literal, get_args\n\n"
           'Status = Literal["new", "paid", "shipped"]\n\n'
           "orders = [(1, \"paid\"), (2, \"shiped\"), (3, \"new\"), (4, \"PAID\")]",
     solution="allowed = get_args(Status)\n"
              "print([order_id for order_id, status in orders if status not in allowed])")

nb.q("Build", """
    Write a generic `Stack[T]` class with the new syntax, with `push(item)`
    and `pop()` methods (store items in a list). Push `1`, `2`, `3`, pop once
    and print the popped value, then print `Stack.__type_params__`.
""",
     solution="class Stack[T]:\n"
              "    def __init__(self):\n"
              "        self.items: list[T] = []\n\n"
              "    def push(self, item: T) -> None:\n"
              "        self.items.append(item)\n\n"
              "    def pop(self) -> T:\n"
              "        return self.items.pop()\n\n"
              "stack = Stack()\n"
              "for n in (1, 2, 3):\n"
              "    stack.push(n)\n"
              "print(stack.pop())\n"
              "print(Stack.__type_params__)")

nb.q("Build", """
    Make a type alias `Point` for a `tuple[float, float]` using the `type`
    statement. Write `distance(a, b)` annotated with it (straight-line
    distance), print `distance` between `(0, 0)` and `(3, 4)`, then print
    `Point.__name__` and `Point.__value__`.
""",
     solution="type Point = tuple[float, float]\n\n"
              "def distance(a: Point, b: Point) -> float:\n"
              "    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5\n\n"
              "print(distance((0, 0), (3, 4)))\n"
              "print(Point.__name__)\n"
              "print(Point.__value__)")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    A `Product` dataclass has a `ClassVar` counter and three real fields.
    Create two products, then print the counter and the field names that the
    dataclass machinery sees (the `ClassVar` is not a field).
""",
     given="from dataclasses import dataclass, fields\n"
           "from typing import ClassVar\n\n"
           "@dataclass\n"
           "class Product:\n"
           "    created: ClassVar[int] = 0\n"
           "    sku: str\n"
           "    price: float\n"
           "    stock: int = 0\n\n"
           "    def __post_init__(self):\n"
           "        Product.created += 1",
     solution='Product("A1", 2.5)\n'
              'Product("B2", 9.0, stock=4)\n'
              "print(Product.created)\n"
              "print([f.name for f in fields(Product)])")

nb.q("Puzzle", """
    `UserId` and `OrderId` are `NewType`s over `int`, so type checkers keep
    them apart. At runtime they are just the plain value. Create `UserId(7)`
    and `OrderId(7)`, then print whether they are equal, the type name of
    `UserId(7)`, and `UserId.__supertype__`.
""",
     given="from typing import NewType\n\n"
           "UserId = NewType(\"UserId\", int)\nOrderId = NewType(\"OrderId\", int)",
     solution="user, order = UserId(7), OrderId(7)\n"
              "print(user == order)\n"
              "print(type(user).__name__)\n"
              "print(UserId.__supertype__)")

nb.q("Build", """
    Write `parse(value)` with two `@overload` stubs (a `str` gives back an
    `int`, a `list[str]` gives back a `list[int]`) and a real body that does
    the dispatch by hand with `isinstance`. Print `parse("42")`,
    `parse(["1", "2"])` and the number of overloads that
    `typing.get_overloads(parse)` reports.
""",
     solution="import typing\n"
              "from typing import overload\n\n"
              "@overload\n"
              "def parse(value: str) -> int: ...\n"
              "@overload\n"
              "def parse(value: list[str]) -> list[int]: ...\n"
              "def parse(value):\n"
              "    if isinstance(value, str):\n"
              "        return int(value)\n"
              "    return [int(v) for v in value]\n\n"
              'print(parse("42"))\n'
              'print(parse(["1", "2"]))\n'
              "print(len(typing.get_overloads(parse)))")

nb.q("Real-life", """
    `Settings` lists the type of each config value. For every key in `config`
    print `<key>: ok` if the value matches the hint, otherwise
    `<key>: expected <type name>`. Use `typing.get_type_hints`, and remember
    that `True` is also an `int`: a `port` of `True` must be rejected.
""",
     given="class Settings:\n"
           "    host: str\n"
           "    port: int\n"
           "    debug: bool\n"
           "    ratio: float\n\n"
           'config = {"host": "db.local", "port": True, "debug": False, "ratio": "0.5"}',
     solution="import typing\n\n"
              "hints = typing.get_type_hints(Settings)\n"
              "for key, value in config.items():\n"
              "    expected = hints[key]\n"
              "    good = isinstance(value, expected)\n"
              "    if expected is int and isinstance(value, bool):\n"
              "        good = False\n"
              '    print(f"{key}: ok" if good else f"{key}: expected {expected.__name__}")')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Build", """
    A shape-drawing helper `total_area` accepts a list of anything that has
    an `.area()` method. Write a `HasArea` Protocol, then write `total_area`
    as a generic function whose type parameter `T` is bounded by `HasArea`
    (new syntax). Print the total area of `shapes`, then the name of the bound
    class: `total_area.__type_params__[0].__bound__.__name__`.
""",
     given="class Rect:\n"
           "    def __init__(self, w, h):\n"
           "        self.w, self.h = w, h\n"
           "    def area(self):\n"
           "        return self.w * self.h\n\n"
           "class Tile:\n"
           "    def area(self):\n"
           "        return 1\n\n"
           "shapes = [Rect(2, 3), Tile(), Rect(4, 5)]",
     solution="from typing import Protocol\n\n"
              "class HasArea(Protocol):\n"
              "    def area(self) -> float: ...\n\n"
              "def total_area[T: HasArea](items: list[T]) -> float:\n"
              "    return sum(item.area() for item in items)\n\n"
              "print(total_area(shapes))\n"
              "print(total_area.__type_params__[0].__bound__.__name__)")

nb.q("Puzzle", """
    A report builder has a `Report` base class whose methods chain by
    returning `Self`. `HtmlReport` replaces `render` and marks it with
    `@override` so a checker would catch a typo. Build both: `add(line)`
    stores a line and returns `self`; `render()` joins lines with `|` in
    `Report`, and wraps `<p>..</p>` around each line in `HtmlReport`. Print
    the HTML render of a chain adding `a` then `b`, and then
    `HtmlReport.render.__override__` and `hasattr(Report.render, "__override__")`.
""",
     solution="from typing import Self, override\n\n"
              "class Report:\n"
              "    def __init__(self):\n"
              "        self.lines: list[str] = []\n\n"
              "    def add(self, line: str) -> Self:\n"
              "        self.lines.append(line)\n"
              "        return self\n\n"
              "    def render(self) -> str:\n"
              '        return "|".join(self.lines)\n\n'
              "class HtmlReport(Report):\n"
              "    @override\n"
              "    def render(self) -> str:\n"
              '        return "".join(f"<p>{line}</p>" for line in self.lines)\n\n'
              'print(HtmlReport().add("a").add("b").render())\n'
              "print(HtmlReport.render.__override__)\n"
              'print(hasattr(Report.render, "__override__"))')

nb.q("Build", """
    Write a decorator `enforce` that makes a function's hints real: before the
    call it reads `typing.get_type_hints` and `inspect.signature(...).bind`,
    and raises `TypeError("<name> must be <type name>")` for the first
    argument whose class doesn't match its hint (parameters without hints are
    skipped). Decorate `book_seats(show: str, seats: int)` to return
    `"<show>: <seats> seats"`. Print the result of a good call, then call it
    with `seats="3"` and print the error message.
""",
     solution="import functools\nimport inspect\nimport typing\n\n"
              "def enforce(func):\n"
              "    hints = typing.get_type_hints(func)\n"
              "    signature = inspect.signature(func)\n\n"
              "    @functools.wraps(func)\n"
              "    def wrapper(*args, **kwargs):\n"
              "        bound = signature.bind(*args, **kwargs)\n"
              "        for name, value in bound.arguments.items():\n"
              "            expected = hints.get(name)\n"
              "            if expected is not None and not isinstance(value, expected):\n"
              '                raise TypeError(f"{name} must be {expected.__name__}")\n'
              "        return func(*args, **kwargs)\n"
              "    return wrapper\n\n"
              "@enforce\n"
              "def book_seats(show: str, seats: int):\n"
              '    return f"{show}: {seats} seats"\n\n'
              'print(book_seats("Hamlet", 2))\n'
              "try:\n"
              '    book_seats("Hamlet", seats="3")\n'
              "except TypeError as error:\n"
              "    print(error)")

nb.q("Build", """
    Write `load(cls, data)` that builds an instance of a dataclass from a
    plain dict using the dataclass's hints. For each field: a missing key with
    no default raises `ValueError("missing <field>")`; a value of the wrong
    class raises `ValueError("<field> must be <type name>")`; otherwise it is
    used. Fields hinted `int | None` accept `None`. Load the three dicts in
    `rows` into `Member` and print each result, or the error message.
""",
     given="from dataclasses import dataclass\n\n"
           "@dataclass\n"
           "class Member:\n"
           "    name: str\n"
           "    age: int\n"
           "    team: str | None = None\n\n"
           "rows = [\n"
           '    {"name": "Ana", "age": 30, "team": "red"},\n'
           '    {"name": "Bo"},\n'
           '    {"name": "Cy", "age": "41"},\n'
           "]",
     solution="import dataclasses\nimport typing\n\n"
              "def load(cls, data):\n"
              "    hints = typing.get_type_hints(cls)\n"
              "    values = {}\n"
              "    for field in dataclasses.fields(cls):\n"
              "        if field.name not in data:\n"
              "            if field.default is dataclasses.MISSING:\n"
              '                raise ValueError(f"missing {field.name}")\n'
              "            continue\n"
              "        value = data[field.name]\n"
              "        if not isinstance(value, hints[field.name]):\n"
              "            kinds = typing.get_args(hints[field.name]) or (hints[field.name],)\n"
              '            raise ValueError(f"{field.name} must be {kinds[0].__name__}")\n'
              "        values[field.name] = value\n"
              "    return cls(**values)\n\n"
              "for row in rows:\n"
              "    try:\n"
              "        print(load(Member, row))\n"
              "    except ValueError as error:\n"
              "        print(error)")

nb.q("Puzzle", """
    A function's annotations hide the type tree. Write `describe(hint)` that
    prints the hint as nested text: for a plain class its `__name__`; for a
    generic `origin[arg1, arg2]` using the origin's name and the described
    args (recursively), separated by `, `; for a union (`X | Y`) the described
    parts joined with ` or `. Print the description of each hint in `hints`.
""",
     given="from typing import get_args, get_origin\nimport types\n\n"
           "hints = [int, list[str], dict[str, list[int]], int | None, list[int | str]]",
     solution="def describe(hint):\n"
              "    origin = get_origin(hint)\n"
              "    args = get_args(hint)\n"
              "    if origin is None:\n"
              "        return hint.__name__\n"
              "    if origin is types.UnionType:\n"
              '        return " or ".join(describe(a) for a in args)\n'
              '    return f"{origin.__name__}[{\', \'.join(describe(a) for a in args)}]"\n\n'
              "for hint in hints:\n"
              "    print(describe(hint))")

# ------------------------------------------------------------ Project
nb.project("Typed Repository Layer", story="""
    You are building a small storage layer for a shop. The record type is a
    dataclass, storage backends are described by a `Protocol`, and a generic
    `Repository[T]` checks every record against the dataclass's hints before
    saving it. Each step builds on the previous ones.
""",
     given="from dataclasses import dataclass\n\n"
           "@dataclass\n"
           "class Item:\n"
           "    sku: str\n"
           "    name: str\n"
           "    price: float\n"
           "    stock: int = 0",
     steps=[
         ("Write `check(cls, data)` that returns a list of problem strings for a dict `data` against the "
          "dataclass `cls`, using `typing.get_type_hints`: `missing <field>` for a required field absent, "
          "`<field> must be <type name>` for a wrong class (an `int` is fine where `float` is expected). "
          "Print the problems for a good dict, and for `{\"sku\": \"A1\", \"price\": \"cheap\"}`.",
          "import dataclasses\nimport typing\n\n"
          "def check(cls, data):\n"
          "    hints = typing.get_type_hints(cls)\n"
          "    problems = []\n"
          "    for field in dataclasses.fields(cls):\n"
          "        if field.name not in data:\n"
          "            if field.default is dataclasses.MISSING:\n"
          '                problems.append(f"missing {field.name}")\n'
          "            continue\n"
          "        expected = hints[field.name]\n"
          "        if expected is float:\n"
          "            expected = (int, float)\n"
          "        if not isinstance(data[field.name], expected):\n"
          '            problems.append(f"{field.name} must be {hints[field.name].__name__}")\n'
          "    return problems\n\n"
          'print(check(Item, {"sku": "A1", "name": "Pen", "price": 2, "stock": 5}))\n'
          'print(check(Item, {"sku": "A1", "price": "cheap"}))'),
         ("Write a `Storage` Protocol (runtime checkable) with `save(key, value)` and `load(key)`, and a "
          "`MemoryStorage` class backed by a dict (`load` returns `None` for an unknown key). Print "
          "`isinstance(MemoryStorage(), Storage)` and `isinstance(object(), Storage)`.",
          "from typing import Protocol, runtime_checkable\n\n"
          "@runtime_checkable\n"
          "class Storage(Protocol):\n"
          "    def save(self, key: str, value: dict) -> None: ...\n"
          "    def load(self, key: str) -> dict | None: ...\n\n"
          "class MemoryStorage:\n"
          "    def __init__(self):\n"
          "        self.data = {}\n\n"
          "    def save(self, key, value):\n"
          "        self.data[key] = value\n\n"
          "    def load(self, key):\n"
          "        return self.data.get(key)\n\n"
          "print(isinstance(MemoryStorage(), Storage))\n"
          "print(isinstance(object(), Storage))"),
         ("Write `class Repository[T]` taking a record class and a storage. `add(data)` raises "
          "`ValueError` with the problems joined by `; ` if `check` finds any, otherwise saves the dict under "
          "its `sku` and returns the built `T`. `get(sku)` returns a `T` or `None`. Add the good item, try the "
          "bad one and print the error, then print `get(\"A1\")` and `get(\"Z9\")`.",
          "class Repository[T]:\n"
          "    def __init__(self, cls: type[T], storage: Storage):\n"
          "        self.cls = cls\n"
          "        self.storage = storage\n\n"
          "    def add(self, data: dict) -> T:\n"
          "        problems = check(self.cls, data)\n"
          "        if problems:\n"
          '            raise ValueError("; ".join(problems))\n'
          '        self.storage.save(data["sku"], data)\n'
          "        return self.cls(**data)\n\n"
          "    def get(self, sku: str) -> T | None:\n"
          "        data = self.storage.load(sku)\n"
          "        return self.cls(**data) if data is not None else None\n\n"
          "repo = Repository(Item, MemoryStorage())\n"
          'repo.add({"sku": "A1", "name": "Pen", "price": 2, "stock": 5})\n'
          "try:\n"
          '    repo.add({"sku": "B2", "price": "cheap"})\n'
          "except ValueError as error:\n"
          "    print(error)\n"
          'print(repo.get("A1"))\n'
          'print(repo.get("Z9"))'),
         ("Write `JsonStorage(path)` that keeps everything in one JSON file (read the whole file on each "
          "call, write it back on `save`; a missing file counts as empty). Inside a temporary directory "
          "make a `Repository(Item, JsonStorage(...))`, add two items, then create a second repository on the "
          "same file and print `get` for one of them, to prove the data persisted. Also print "
          "`isinstance` of the storage against `Storage`.",
          "import json\nimport tempfile\nfrom pathlib import Path\n\n"
          "class JsonStorage:\n"
          "    def __init__(self, path):\n"
          "        self.path = Path(path)\n\n"
          "    def _read(self):\n"
          "        if not self.path.exists():\n"
          "            return {}\n"
          "        return json.loads(self.path.read_text())\n\n"
          "    def save(self, key, value):\n"
          "        data = self._read()\n"
          "        data[key] = value\n"
          "        self.path.write_text(json.dumps(data))\n\n"
          "    def load(self, key):\n"
          "        return self._read().get(key)\n\n"
          "with tempfile.TemporaryDirectory() as folder:\n"
          '    storage = JsonStorage(Path(folder) / "items.json")\n'
          "    first = Repository(Item, storage)\n"
          '    first.add({"sku": "C3", "name": "Ink", "price": 7.5})\n'
          '    first.add({"sku": "D4", "name": "Pad", "price": 3, "stock": 2})\n'
          "    second = Repository(Item, JsonStorage(storage.path))\n"
          '    print(second.get("D4"))\n'
          "    print(isinstance(storage, Storage))"),
     ])

nb.build()
