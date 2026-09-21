"""Notebook 08 - OOP (Q-271..Q-314)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-271",
    level=Level.L1,
    topic="Classes",
    kind="function",
    entry="make_point",
    prompt=(
        "Define a class `Point` whose `__init__` takes `x` and `y` and stores them "
        "as attributes of the instance.\n\n"
        "Then write `make_point(x, y)` that builds one and returns the **tuple** "
        "`(p.x, p.y)` read back off the instance."
    ),
    hint=(
        "`__init__` receives the new object as its first parameter. Storing a value "
        "on it means assigning to an attribute of that parameter, not to a bare local "
        "name."
    ),
    solution="""\
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_point(x, y):
    p = Point(x, y)
    return (p.x, p.y)""",
    explanation=(
        "`self` is not a keyword — it is just the conventional name for the first "
        "parameter, which Python fills in with the instance being built. Writing "
        "`x = x` inside `__init__` assigns a local that dies at the end of the call; "
        "only `self.x = x` attaches anything to the object."
    ),
    starter="""\
class Point:
    def __init__(self, x, y):
        ...


def make_point(x, y):
    ...""",
    cases=[
        Case(expected=(1, 2), args=(1, 2)),
        Case(expected=(0, 0), args=(0, 0)),
        Case(expected=(-1, 2.5), args=(-1, 2.5)),
        Case(expected=("a", "b"), args=("a", "b")),
    ],
)

q(
    qid="Q-272",
    level=Level.L1,
    topic="Classes",
    kind="function",
    entry="greetings",
    prompt=(
        "Define a class `Greeter` whose `__init__` takes a `name`, plus a method "
        "`greet()` that returns the string `\"Hello, NAME!\"`.\n\n"
        "Then write `greetings(names)` that builds one `Greeter` per name and returns "
        "the **list** of their `greet()` results, in order."
    ),
    hint=(
        "A method is a `def` indented inside the `class` body, and its first parameter "
        "is the instance. `greet` takes no arguments from the caller — everything it "
        "needs is already on the object."
    ),
    solution="""\
class Greeter:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"


def greetings(names):
    return [Greeter(n).greet() for n in names]""",
    explanation=(
        "A method is an ordinary function that lives in the class and takes the "
        "instance as its first argument; `g.greet()` is sugar for "
        "`Greeter.greet(g)`. Forgetting `self` in the signature is the classic first "
        "error, and it shows up as a confusing \"takes 0 positional arguments but 1 "
        "was given\"."
    ),
    starter="""\
class Greeter:
    def __init__(self, name):
        ...

    def greet(self):
        ...


def greetings(names):
    ...""",
    cases=[
        Case(expected=["Hello, Ada!"], args=(["Ada"],)),
        Case(expected=[], args=([],)),
        Case(expected=["Hello, A!", "Hello, B!"], args=(["A", "B"],)),
        Case(expected=["Hello, !"], args=([""],)),
    ],
)

q(
    qid="Q-273",
    level=Level.L1,
    topic="Attributes",
    kind="function",
    entry="dog_facts",
    prompt=(
        "Define a class `Dog` with a **class attribute** `species` set to "
        "`\"Canis familiaris\"`, and an `__init__` that stores an instance attribute "
        "`name`.\n\n"
        "Then write `dog_facts(name)` that builds one dog and returns the tuple "
        "`(d.name, d.species, Dog.species)`."
    ),
    hint=(
        "One of the two attributes is written directly in the class body, outside any "
        "method. Read both off the instance anyway — attribute lookup does not stop at "
        "the instance."
    ),
    solution="""\
class Dog:
    species = "Canis familiaris"

    def __init__(self, name):
        self.name = name


def dog_facts(name):
    d = Dog(name)
    return (d.name, d.species, Dog.species)""",
    explanation=(
        "Attribute lookup checks the instance first and then the class, which is why "
        "`d.species` works even though no `__init__` ever set it. A class attribute is "
        "created once when the class body runs, so every instance shares the one "
        "object — harmless for a constant string, and a genuine trap for a list (Q-284)."
    ),
    starter="""\
class Dog:
    ...

    def __init__(self, name):
        ...


def dog_facts(name):
    ...""",
    cases=[
        Case(expected=("Rex", "Canis familiaris", "Canis familiaris"), args=("Rex",)),
        Case(expected=("Ada", "Canis familiaris", "Canis familiaris"), args=("Ada",)),
        Case(expected=("", "Canis familiaris", "Canis familiaris"), args=("",)),
    ],
)

q(
    qid="Q-274",
    level=Level.L1,
    topic="Classes",
    kind="function",
    entry="run_counter",
    prompt=(
        "Define a class `Counter` whose `__init__` sets `self.count` to `0`, with a "
        "method `bump()` that adds one to `self.count`.\n\n"
        "Then write `run_counter(n)` that builds one counter, calls `bump()` `n` "
        "times, and returns the final `count` as an `int`."
    ),
    hint=(
        "The method changes state rather than returning a new value — so it has to "
        "write back to the attribute it read, on the same object it was called on."
    ),
    solution="""\
class Counter:
    def __init__(self):
        self.count = 0

    def bump(self):
        self.count += 1


def run_counter(n):
    c = Counter()
    for _ in range(n):
        c.bump()
    return c.count""",
    explanation=(
        "`self.count += 1` reads the attribute, adds one, and stores it back on the "
        "instance — that persistence between calls is the whole reason an object "
        "exists rather than a plain function. A method that mutates state should "
        "usually return `None`, not the new value, so nobody is tempted to chain it."
    ),
    starter="""\
class Counter:
    def __init__(self):
        ...

    def bump(self):
        ...


def run_counter(n):
    ...""",
    cases=[
        Case(expected=0, args=(0,)),
        Case(expected=1, args=(1,)),
        Case(expected=5, args=(5,)),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-275",
    level=Level.L2,
    topic="Inheritance",
    kind="function",
    entry="dog_facts",
    prompt=(
        "Define `Animal` with an `__init__` taking `name` and a method `describe()` "
        "returning `\"NAME is an animal\"`. Then define `Dog(Animal)` that adds "
        "nothing at all — its body is just `pass`.\n\n"
        "Write `dog_facts(name)` returning the tuple "
        "`(d.describe(), isinstance(d, Animal), issubclass(Dog, Animal))`."
    ),
    hint=(
        "An empty subclass still gets its parent's `__init__` and every method. The "
        "two booleans ask about the object and about the class respectively — different "
        "questions, different builtins."
    ),
    solution="""\
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is an animal"


class Dog(Animal):
    pass


def dog_facts(name):
    d = Dog(name)
    return (d.describe(), isinstance(d, Animal), issubclass(Dog, Animal))""",
    explanation=(
        "Subclassing copies nothing: `Dog` holds a reference to `Animal` and lookup "
        "walks up the chain at call time, so a later edit to `Animal.describe` is "
        "visible from every `Dog` immediately. `isinstance` asks about an object and "
        "`issubclass` about a class — passing an instance to `issubclass` raises "
        "`TypeError`, which is the usual mix-up."
    ),
    starter="""\
class Animal:
    def __init__(self, name):
        ...

    def describe(self):
        ...


class Dog(Animal):
    ...


def dog_facts(name):
    ...""",
    cases=[
        Case(expected=("Rex is an animal", True, True), args=("Rex",)),
        Case(expected=("Ada is an animal", True, True), args=("Ada",)),
        Case(expected=(" is an animal", True, True), args=("",)),
    ],
)

q(
    qid="Q-276",
    level=Level.L2,
    topic="Inheritance",
    kind="function",
    entry="employee_facts",
    prompt=(
        "Define `Person` with `__init__(self, name)`. Then define `Employee(Person)` "
        "with `__init__(self, name, salary)` that delegates the `name` to the parent "
        "with `super().__init__(...)` and stores `salary` itself.\n\n"
        "Write `employee_facts(name, salary)` returning "
        "`(e.name, e.salary, isinstance(e, Person))`."
    ),
    hint=(
        "Defining `__init__` in the subclass replaces the parent's entirely — nothing "
        "the parent sets happens unless you ask for it. One call, at the top of the "
        "child's `__init__`, restores it."
    ),
    solution="""\
class Person:
    def __init__(self, name):
        self.name = name


class Employee(Person):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary


def employee_facts(name, salary):
    e = Employee(name, salary)
    return (e.name, e.salary, isinstance(e, Person))""",
    explanation=(
        "An overriding `__init__` does not extend the parent's, it *replaces* it, so "
        "forgetting `super().__init__(name)` leaves `self.name` unset and the failure "
        "surfaces far away as an `AttributeError`. Prefer `super()` over "
        "`Person.__init__(self, name)`: it is the only form that keeps working once a "
        "class ends up in a multiple-inheritance chain (Q-313)."
    ),
    starter="""\
class Person:
    def __init__(self, name):
        ...


class Employee(Person):
    def __init__(self, name, salary):
        ...


def employee_facts(name, salary):
    ...""",
    cases=[
        Case(expected=("Ada", 100, True), args=("Ada", 100)),
        Case(expected=("Bo", 0, True), args=("Bo", 0)),
        Case(expected=("Cy", 42.5, True), args=("Cy", 42.5)),
    ],
)

q(
    qid="Q-277",
    level=Level.L2,
    topic="Polymorphism",
    kind="function",
    entry="chorus",
    prompt=(
        "Define `Animal` with `speak()` returning `\"...\"`, then `Dog(Animal)` and "
        "`Cat(Animal)` that **override** `speak()` to return `\"Woof\"` and "
        "`\"Meow\"`.\n\n"
        "Write `chorus(kinds)` where `kinds` is a list of the strings `\"dog\"`, "
        "`\"cat\"` or `\"animal\"`. Build one object per entry and return the **list** "
        "of `speak()` results, in order."
    ),
    hint=(
        "The calling code should look identical for all three — no `if` on the type "
        "once the object exists. A dict mapping the string to the class keeps the "
        "dispatch in one place."
    ),
    solution="""\
class Animal:
    def speak(self):
        return "..."


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"


def chorus(kinds):
    table = {"dog": Dog, "cat": Cat, "animal": Animal}
    return [table[k]().speak() for k in kinds]""",
    explanation=(
        "Polymorphism means the *object* decides which `speak` runs, so one loop "
        "serves every animal and a new subclass needs no edit to `chorus`. That is the "
        "payoff: `if isinstance(a, Dog): ... elif isinstance(a, Cat): ...` has to be "
        "rewritten every time the zoo grows."
    ),
    starter="""\
class Animal:
    def speak(self):
        ...


class Dog(Animal):
    ...


class Cat(Animal):
    ...


def chorus(kinds):
    ...""",
    cases=[
        Case(expected=["Woof", "Meow"], args=(["dog", "cat"],)),
        Case(expected=["...", "Woof", "..."], args=(["animal", "dog", "animal"],)),
        Case(expected=[], args=([],)),
        Case(expected=["Meow", "Meow"], args=(["cat", "cat"],)),
    ],
)

q(
    qid="Q-278",
    level=Level.L2,
    topic="Dunder Methods",
    kind="function",
    entry="label",
    prompt=(
        "Define `User` with `__init__(self, name)` and a `__str__` returning "
        "`\"User: NAME\"`.\n\n"
        "Write `label(name)` that builds one and returns the tuple "
        "`(str(u), f\"{u}\")` — both elements are strings."
    ),
    hint=(
        "You never call the dunder yourself. Two very ordinary pieces of syntax reach "
        "for it on your behalf, and the prompt uses both."
    ),
    solution="""\
class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"User: {self.name}"


def label(name):
    u = User(name)
    return (str(u), f"{u}")""",
    explanation=(
        "`str()`, `print()` and f-string interpolation all route through `__str__`, so "
        "defining it once gives you a readable object everywhere a human will look. "
        "`__str__` must return a `str` — returning anything else raises `TypeError` at "
        "the call site rather than where the bug lives."
    ),
    starter="""\
class User:
    def __init__(self, name):
        ...

    def __str__(self):
        ...


def label(name):
    ...""",
    cases=[
        Case(expected=("User: Ada", "User: Ada"), args=("Ada",)),
        Case(expected=("User: bo", "User: bo"), args=("bo",)),
        Case(expected=("User: ", "User: "), args=("",)),
    ],
)

q(
    qid="Q-279",
    level=Level.L2,
    topic="Dunder Methods",
    kind="function",
    entry="show",
    prompt=(
        "Define `Point` with `__init__(self, x, y)` and a `__repr__` returning "
        "`\"Point(1, 2)\"` for `Point(1, 2)` — the text that would rebuild the "
        "object.\n\n"
        "Define **no** `__str__`. Write `show(x, y)` returning the 3-tuple "
        "`(repr(p), str(p), repr([p]))`."
    ),
    hint=(
        "With no `__str__` defined, `str()` does not fall back to the default object "
        "text — it falls back to something you *did* define. And a container never "
        "asks its elements for their friendly form."
    ),
    solution="""\
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def show(x, y):
    p = Point(x, y)
    return (repr(p), str(p), repr([p]))""",
    explanation=(
        "`__str__` falls back to `__repr__` but never the other way round, which is "
        "why `__repr__` is the one to define when you only define one. Containers "
        "always use `repr` on their elements, so a list of objects with only `__str__` "
        "still prints as `<__main__.Point object at 0x...>` — the single most common "
        "reason a debug print says nothing useful."
    ),
    starter="""\
class Point:
    def __init__(self, x, y):
        ...

    def __repr__(self):
        ...


def show(x, y):
    ...""",
    cases=[
        Case(expected=("Point(1, 2)", "Point(1, 2)", "[Point(1, 2)]"), args=(1, 2)),
        Case(expected=("Point(0, 0)", "Point(0, 0)", "[Point(0, 0)]"), args=(0, 0)),
        Case(expected=("Point(-1, 5)", "Point(-1, 5)", "[Point(-1, 5)]"), args=(-1, 5)),
    ],
)

q(
    qid="Q-280",
    level=Level.L2,
    topic="Class & Static Methods",
    kind="function",
    entry="use_add",
    prompt=(
        "Define `MathUtil` with a `@staticmethod` `add(a, b)` returning `a + b`. It "
        "takes no `self` and no `cls`.\n\n"
        "Write `use_add(a, b)` returning the tuple "
        "`(MathUtil.add(a, b), MathUtil().add(a, b))` — called once on the class and "
        "once on an instance."
    ),
    hint=(
        "The decorator switches off the automatic first argument. Without it, calling "
        "through an instance would pass the instance in as `a`."
    ),
    solution="""\
class MathUtil:
    @staticmethod
    def add(a, b):
        return a + b


def use_add(a, b):
    return (MathUtil.add(a, b), MathUtil().add(a, b))""",
    explanation=(
        "`@staticmethod` is a plain function that happens to live in a class namespace: "
        "it gets no instance and no class, so both call sites behave identically. Reach "
        "for it when a helper is conceptually part of the class but needs none of its "
        "state — and be honest that a module-level function is often the better answer."
    ),
    starter="""\
class MathUtil:
    @staticmethod
    def add(a, b):
        ...


def use_add(a, b):
    ...""",
    cases=[
        Case(expected=(3, 3), args=(1, 2)),
        Case(expected=(0, 0), args=(0, 0)),
        Case(expected=(0, 0), args=(-1, 1)),
        Case(expected=("ab", "ab"), args=("a", "b")),
    ],
)

q(
    qid="Q-281",
    level=Level.L2,
    topic="Class & Static Methods",
    kind="function",
    entry="parse_date",
    prompt=(
        "Define `Date` with `__init__(self, year, month, day)` storing three ints, "
        "plus a `@classmethod` `from_string(cls, text)` that parses `\"2024-05-17\"` "
        "and returns a `Date`.\n\n"
        "Write `parse_date(text)` that uses the classmethod and returns the tuple "
        "`(d.year, d.month, d.day)` — three ints."
    ),
    hint=(
        "The first parameter is the class itself, so the last line of `from_string` "
        "can build an instance without naming `Date` anywhere. `str.split` on the "
        "dash gives you three pieces, still as strings."
    ),
    solution="""\
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, text):
        year, month, day = text.split("-")
        return cls(int(year), int(month), int(day))


def parse_date(text):
    d = Date.from_string(text)
    return (d.year, d.month, d.day)""",
    explanation=(
        "This is the *alternative constructor* pattern: `__init__` takes the canonical "
        "form and a classmethod adapts every other input shape to it, so parsing lives "
        "next to the type it produces. Using `cls(...)` rather than `Date(...)` is what "
        "makes the constructor inherit correctly — a subclass gets its own type back "
        "for free (Q-308)."
    ),
    starter="""\
class Date:
    def __init__(self, year, month, day):
        ...

    @classmethod
    def from_string(cls, text):
        ...


def parse_date(text):
    ...""",
    cases=[
        Case(expected=(2024, 5, 17), args=("2024-05-17",)),
        Case(expected=(1999, 1, 1), args=("1999-01-01",)),
        Case(expected=(2000, 12, 31), args=("2000-12-31",)),
    ],
)

q(
    qid="Q-282",
    level=Level.L2,
    topic="Properties",
    kind="function",
    entry="area_of",
    prompt=(
        "Define `Rectangle` with `__init__(self, width, height)` and an `area` "
        "**property** that computes `width * height`.\n\n"
        "Write `area_of(width, height)` returning `r.area` — accessed as an attribute, "
        "with no parentheses."
    ),
    hint=(
        "Decorate the method and the call parentheses disappear at every call site. "
        "The value must not be stored in `__init__`, or it goes stale when the sides "
        "change."
    ),
    solution="""\
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height


def area_of(width, height):
    return Rectangle(width, height).area""",
    explanation=(
        "`@property` lets a computed value be read like a plain attribute, so a field "
        "can later become a computation without breaking a single caller. Computing it "
        "on demand also means it can never disagree with `width` and `height`, which a "
        "value cached in `__init__` eventually will."
    ),
    starter="""\
class Rectangle:
    def __init__(self, width, height):
        ...

    @property
    def area(self):
        ...


def area_of(width, height):
    ...""",
    cases=[
        Case(expected=12, args=(3, 4)),
        Case(expected=0, args=(0, 5)),
        Case(expected=5.0, args=(2.5, 2)),
    ],
)

q(
    qid="Q-283",
    level=Level.L2,
    topic="Composition",
    kind="function",
    entry="shelf_pages",
    prompt=(
        "Define `Book` with `__init__(self, title, pages)`, and `Shelf` which starts "
        "with an empty list of books, has `add(book)`, and has "
        "`total_pages()` returning the sum of its books' pages.\n\n"
        "A shelf is not a kind of book — it **has** books. Write "
        "`shelf_pages(specs)` where `specs` is a list of `(title, pages)` tuples; "
        "build a shelf, add a `Book` for each, and return "
        "`(number_of_books, total_pages)`."
    ),
    hint=(
        "Give `Shelf.__init__` its own empty list. `total_pages` should not reach into "
        "`book.pages` counts it has cached — it should ask the list it already holds."
    ),
    solution="""\
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages


class Shelf:
    def __init__(self):
        self.books = []

    def add(self, book):
        self.books.append(book)

    def total_pages(self):
        return sum(b.pages for b in self.books)


def shelf_pages(specs):
    shelf = Shelf()
    for title, pages in specs:
        shelf.add(Book(title, pages))
    return (len(shelf.books), shelf.total_pages())""",
    explanation=(
        "Composition — \"has-a\" — is the default relationship between objects, and "
        "inheritance is the exception you reach for only when a subclass genuinely *is* "
        "the parent. Note the empty list is created in `__init__`, once per shelf; "
        "writing `books = []` in the class body would give every shelf the same list "
        "(Q-284)."
    ),
    starter="""\
class Book:
    def __init__(self, title, pages):
        ...


class Shelf:
    def __init__(self):
        ...

    def add(self, book):
        ...

    def total_pages(self):
        ...


def shelf_pages(specs):
    ...""",
    cases=[
        Case(expected=(2, 300), args=([("a", 100), ("b", 200)],)),
        Case(expected=(0, 0), args=([],)),
        Case(expected=(1, 0), args=([("empty", 0)],)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-284",
    level=Level.L3,
    topic="Attributes",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "class Basket:\n"
        "    items = []\n"
        "\n"
        "    def add(self, x):\n"
        "        self.items.append(x)\n"
        "\n"
        "a = Basket()\n"
        "b = Basket()\n"
        "a.add(\"apple\")\n"
        "print(b.items)\n"
        "print(a.items is b.items)\n"
        "print(Basket.items)\n"
        "```\n\n"
        "Set `answer` to the three printed lines, e.g. "
        "`answer = \"[]\\nFalse\\n[]\"`."
    ),
    hint=(
        "`self.items.append(...)` never assigns to `self.items` — it looks the "
        "attribute up and then mutates whatever it finds. Where does that lookup land "
        "when the instance has no `items` of its own?"
    ),
    solution='answer = "[\'apple\']\\nTrue\\n[\'apple\']"',
    explanation=(
        "The class body runs once, so `items` is a single list shared by every "
        "instance, and `append` mutates it in place rather than rebinding anything. "
        "This is the most expensive beginner bug in OOP because it stays invisible "
        "until the second instance exists: mutable defaults belong in `__init__`, "
        "never in the class body."
    ),
    starter="answer = ...",
    cases=[Case(expected="['apple']\nTrue\n['apple']")],
)

q(
    qid="Q-285",
    level=Level.L3,
    topic="Attributes",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "class Config:\n"
        "    debug = False\n"
        "\n"
        "a = Config()\n"
        "b = Config()\n"
        "a.debug = True\n"
        "print(a.debug, b.debug)\n"
        "print(Config.debug)\n"
        "print(\"debug\" in a.__dict__, \"debug\" in b.__dict__)\n"
        "```\n\n"
        "Set `answer` to the three printed lines. Mind the spacing — `print` puts one "
        "space between arguments."
    ),
    hint=(
        "Assigning through an instance never reaches the class. Compare that with "
        "Q-284, where nothing was assigned at all — that difference is the whole "
        "question."
    ),
    solution='answer = "True False\\nFalse\\nTrue False"',
    explanation=(
        "`a.debug = True` *creates* an instance attribute that shadows the class one "
        "for `a` only; `b` and `Config` are untouched, and `a.__dict__` now has a key "
        "`b.__dict__` does not. The asymmetry is the trap: reading a class attribute "
        "through an instance works, but writing one through an instance silently makes "
        "a private copy instead."
    ),
    starter="answer = ...",
    cases=[Case(expected="True False\nFalse\nTrue False")],
)

q(
    qid="Q-286",
    level=Level.L3,
    topic="Dunder Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "class Only:\n"
        "    def __repr__(self):\n"
        "        return \"Only()\"\n"
        "\n"
        "class Both:\n"
        "    def __repr__(self):\n"
        "        return \"Both-repr\"\n"
        "\n"
        "    def __str__(self):\n"
        "        return \"Both-str\"\n"
        "\n"
        "print(str(Only()), repr(Only()))\n"
        "print(str(Both()), repr(Both()))\n"
        "print([Both()])\n"
        "```\n\n"
        "Set `answer` to the three printed lines."
    ),
    hint=(
        "One of the two dunders falls back to the other, and the fallback only runs in "
        "one direction. The third line asks a container what it shows for its elements."
    ),
    solution='answer = "Only() Only()\\nBoth-str Both-repr\\n[Both-repr]"',
    explanation=(
        "`str(x)` uses `__str__` if there is one and otherwise borrows `__repr__`; "
        "there is no fallback the other way. A container's own `__repr__` calls `repr` "
        "on every element, which is why a list of objects ignores `__str__` completely "
        "— define `__repr__` first, and `__str__` only when the friendly form genuinely "
        "differs."
    ),
    starter="answer = ...",
    cases=[Case(expected="Only() Only()\nBoth-str Both-repr\n[Both-repr]")],
)

q(
    qid="Q-287",
    level=Level.L3,
    topic="Encapsulation",
    kind="function",
    entry="peek",
    prompt=(
        "Define `Vault` whose `__init__` sets two attributes: `self._hint` to "
        "`\"under the mat\"` and `self.__secret` (two leading underscores) to "
        "`\"hunter2\"`.\n\n"
        "Write `peek(name)` that builds a `Vault` and returns "
        "`getattr(vault, name)`. Let it raise whatever `getattr` raises — do not "
        "catch anything."
    ),
    hint=(
        "One underscore is a convention and changes nothing. Two leading underscores "
        "make the compiler rewrite the attribute's name inside the class body — work "
        "out what it is rewritten *to*, and one of the test cases falls out."
    ),
    solution="""\
class Vault:
    def __init__(self):
        self._hint = "under the mat"
        self.__secret = "hunter2"


def peek(name):
    vault = Vault()
    return getattr(vault, name)""",
    explanation=(
        "A single underscore is documentation — \"internal, do not touch\" — enforced "
        "by nothing. Two leading underscores trigger *name mangling*: inside the class "
        "body `self.__secret` is compiled to `self._Vault__secret`, so the attribute is "
        "still perfectly reachable from outside once you know the rule. Mangling exists "
        "to stop a subclass from colliding with a private name by accident, not to "
        "provide security; Python has no private attributes."
    ),
    starter="""\
class Vault:
    def __init__(self):
        ...


def peek(name):
    ...""",
    cases=[
        Case(expected="under the mat", args=("_hint",)),
        Case(expected="hunter2", args=("_Vault__secret",)),
        Case(expected=None, args=("__secret",), raises=AttributeError),
        Case(expected=None, args=("secret",), raises=AttributeError),
    ],
)

q(
    qid="Q-288",
    level=Level.L3,
    topic="Dunder Methods",
    kind="function",
    entry="compare",
    prompt=(
        "Define `Point` with `__init__(self, x, y)` and an `__eq__` that returns "
        "`True` when both coordinates match. When `other` is not a `Point`, return "
        "`NotImplemented` rather than `False`.\n\n"
        "Write `compare(a, b)` where `a` and `b` are `(x, y)` tuples. Return the pair "
        "`(Point(*a) == Point(*b), Point(*a) == a)` — the second comparison is against "
        "the raw tuple."
    ),
    hint=(
        "`NotImplemented` is a sentinel, not an exception and not `False`. Returning it "
        "tells Python you have no opinion, and it then asks the *other* operand — which "
        "decides the second element of every case."
    ),
    solution="""\
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


def compare(a, b):
    return (Point(*a) == Point(*b), Point(*a) == a)""",
    explanation=(
        "Returning `NotImplemented` gives the right-hand operand its turn, and only "
        "when it also declines does Python fall back to identity — which is why a "
        "`Point` is never equal to a tuple here, and why the answer is `False` rather "
        "than an error. Returning `False` instead would be a lie: it would stop a "
        "future type that *does* know how to compare itself to a `Point` from ever "
        "being asked."
    ),
    starter="""\
class Point:
    def __init__(self, x, y):
        ...

    def __eq__(self, other):
        ...


def compare(a, b):
    ...""",
    cases=[
        Case(expected=(True, False), args=((1, 2), (1, 2))),
        Case(expected=(False, False), args=((1, 2), (3, 4))),
        Case(expected=(True, False), args=((0, 0), (0, 0))),
        Case(expected=(False, False), args=((1, 2), (1, 3))),
    ],
)

q(
    qid="Q-289",
    level=Level.L3,
    topic="Dunder Methods",
    kind="function",
    entry="describe",
    prompt=(
        "Define `Playlist` with `__init__(self, tracks)` storing a list, and a "
        "`__len__` returning how many tracks it holds.\n\n"
        "Write `describe(tracks)` returning the tuple `(len(p), bool(p))`. Define "
        "**no** `__bool__` — the second element is the point of the question."
    ),
    hint=(
        "`bool()` looks for `__bool__` first and, failing that, tries one other dunder "
        "before giving up and saying `True`. You have just defined that other dunder."
    ),
    solution="""\
class Playlist:
    def __init__(self, tracks):
        self.tracks = list(tracks)

    def __len__(self):
        return len(self.tracks)


def describe(tracks):
    p = Playlist(tracks)
    return (len(p), bool(p))""",
    explanation=(
        "Truthiness asks `__bool__`, falls back to `__len__ != 0`, and defaults to "
        "`True` when neither exists — so `__len__` alone makes `if playlist:` mean "
        "\"has tracks\" for free. The default is what bites: an object with neither "
        "dunder is always truthy, so `if response:` on a custom wrapper can silently "
        "never be false."
    ),
    starter="""\
class Playlist:
    def __init__(self, tracks):
        ...

    def __len__(self):
        ...


def describe(tracks):
    ...""",
    cases=[
        Case(expected=(0, False), args=([],)),
        Case(expected=(1, True), args=(["a"],)),
        Case(expected=(2, True), args=(["a", "b"],)),
    ],
)

q(
    qid="Q-290",
    level=Level.L3,
    topic="Dunder Methods",
    kind="function",
    entry="pick",
    prompt=(
        "Define `Row` with `__init__(self, values)` storing a list, and a "
        "`__getitem__(self, index)` that simply hands the index straight through to "
        "that list.\n\n"
        "Write `pick(values, index)` returning `Row(values)[index]`. One test case "
        "passes a `slice` object — do not special-case it."
    ),
    hint=(
        "Delegating to the list means negative indices and slices already work, "
        "because the list itself knows how to handle them. Whatever went inside the "
        "brackets arrives as your `index` parameter, unchanged."
    ),
    solution="""\
class Row:
    def __init__(self, values):
        self.values = list(values)

    def __getitem__(self, index):
        return self.values[index]


def pick(values, index):
    return Row(values)[index]""",
    explanation=(
        "`obj[k]` is exactly `type(obj).__getitem__(obj, k)`, and `obj[1:3]` passes a "
        "single `slice(1, 3)` object as that one argument — so delegating to a list "
        "inherits negative indexing and slicing with no extra code. Defining "
        "`__getitem__` also makes the object iterable via the old protocol, which is "
        "why a `for` loop over a `Row` works even without `__iter__`."
    ),
    starter="""\
class Row:
    def __init__(self, values):
        ...

    def __getitem__(self, index):
        ...


def pick(values, index):
    ...""",
    cases=[
        Case(expected=20, args=([10, 20, 30], 1)),
        Case(expected=30, args=([10, 20, 30], -1)),
        Case(expected=[10, 20], args=([10, 20, 30], slice(0, 2))),
        Case(expected=None, args=([10, 20, 30], 5), raises=IndexError),
    ],
)

q(
    qid="Q-291",
    level=Level.L3,
    topic="Dunder Methods",
    kind="function",
    entry="has",
    prompt=(
        "Define `Inventory` with `__init__(self, items)` storing a list of strings, "
        "and a `__contains__` that answers **case-insensitively**: `\"sword\"` is in "
        "an inventory holding `\"Sword\"`.\n\n"
        "Write `has(items, query)` returning `query in Inventory(items)` — a `bool`."
    ),
    hint=(
        "`__contains__` receives the thing being searched for and returns a truthy "
        "value. Lowercasing both sides is enough; the interesting part is that `in` is "
        "now yours to define however you like."
    ),
    solution="""\
class Inventory:
    def __init__(self, items):
        self.items = list(items)

    def __contains__(self, item):
        return item.lower() in [i.lower() for i in self.items]


def has(items, query):
    return query in Inventory(items)""",
    explanation=(
        "`in` is not hard-wired to equality: with `__contains__` defined, the container "
        "decides what membership means, which is how a case-insensitive or "
        "range-based container is built. Without it Python falls back to iterating and "
        "comparing with `==`, so an object with only `__iter__` still supports `in`, "
        "just in linear time and with no say in the rule. Note Python coerces the "
        "result to a real `bool` for you."
    ),
    starter="""\
class Inventory:
    def __init__(self, items):
        ...

    def __contains__(self, item):
        ...


def has(items, query):
    ...""",
    cases=[
        Case(expected=True, args=(["Sword", "Shield"], "sword")),
        Case(expected=True, args=(["Sword", "Shield"], "SHIELD")),
        Case(expected=False, args=(["Sword"], "bow")),
        Case(expected=False, args=([], "sword")),
    ],
)

q(
    qid="Q-292",
    level=Level.L3,
    topic="Dunder Methods",
    kind="custom",
    entry="add_all",
    constraints=["no-builtin:sum"],
    prompt=(
        "Define `Money` with `__init__(self, cents)` and an `__add__` returning a "
        "**new** `Money` holding the combined cents — it must not modify either "
        "operand.\n\n"
        "Write `add_all(amounts)` where `amounts` is a list of ints. Start from "
        "`Money(0)`, fold each amount in with the `+` operator, and return the final "
        "`.cents` as an `int`. You may not call `sum()`."
    ),
    hint=(
        "Overloading `+` means `a + b` calls `a.__add__(b)`. Returning a fresh object "
        "rather than mutating `self` is what keeps `+` behaving the way `+` on ints "
        "and strings already does."
    ),
    solution="""\
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __add__(self, other):
        return Money(self.cents + other.cents)


def add_all(amounts):
    total = Money(0)
    for amount in amounts:
        total = total + Money(amount)
    return total.cents""",
    explanation=(
        "`+` is expected to be non-mutating — `a + b` leaves both operands alone and "
        "produces a third object — so `__add__` returns a new `Money` instead of doing "
        "`self.cents += ...`. Mutating in place is what `__iadd__` is for, and a class "
        "that confuses the two makes `total = total + item` quietly corrupt `item`. "
        "(`sum()` would work here too, since it starts from `0` — but `0 + Money(...)` "
        "would need `__radd__`.)"
    ),
    starter="""\
class Money:
    def __init__(self, cents):
        ...

    def __add__(self, other):
        ...


def add_all(amounts):
    ...""",
    cases=[
        Case(expected=300, args=([100, 200],)),
        Case(expected=0, args=([],)),
        Case(expected=50, args=([50],)),
        Case(expected=0, args=([100, -100],)),
    ],
)

q(
    qid="Q-293",
    level=Level.L3,
    topic="Properties",
    kind="function",
    entry="set_width",
    prompt=(
        "Define `Rectangle` with a `width` **property** whose setter rejects a "
        "negative value by raising `ValueError`, storing the accepted value in "
        "`self._width`. `__init__(self, width)` must go through the setter, so a bad "
        "value is rejected at construction too.\n\n"
        "Write `set_width(start, new)` that builds `Rectangle(start)`, assigns "
        "`new` to `.width`, and returns the resulting `.width`. Let the `ValueError` "
        "escape."
    ),
    hint=(
        "The setter is a second method with the same name, decorated with "
        "`@width.setter`. For `__init__` to be validated too, it must assign to the "
        "public name, not to the underscore one."
    ),
    solution="""\
class Rectangle:
    def __init__(self, width):
        self.width = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value < 0:
            raise ValueError("width must not be negative")
        self._width = value


def set_width(start, new):
    r = Rectangle(start)
    r.width = new
    return r.width""",
    explanation=(
        "A property setter is the Java-style getter/setter pair without the ceremony: "
        "callers keep writing `r.width = 3`, and validation is added later without "
        "touching a single call site — which is exactly why Python code does not write "
        "defensive accessors up front. Note `__init__` assigns `self.width`, not "
        "`self._width`: assigning the private name directly is the standard way people "
        "accidentally bypass their own validation."
    ),
    starter="""\
class Rectangle:
    def __init__(self, width):
        ...

    @property
    def width(self):
        ...

    @width.setter
    def width(self, value):
        ...


def set_width(start, new):
    ...""",
    cases=[
        Case(expected=5, args=(1, 5)),
        Case(expected=0, args=(3, 0)),
        Case(expected=None, args=(1, -1), raises=ValueError),
        Case(expected=None, args=(-1, 5), raises=ValueError),
    ],
)

q(
    qid="Q-294",
    level=Level.L3,
    topic="Class & Static Methods",
    kind="function",
    entry="build_and_count",
    prompt=(
        "Define `Widget` with a class attribute `count = 0`, an `__init__(self, name)` "
        "that increments it, a `@classmethod made(cls)` returning the current count, "
        "and a `@classmethod reset(cls)` setting it back to `0`.\n\n"
        "Write `build_and_count(names)` that resets, builds one `Widget` per name, and "
        "returns `Widget.made()` as an `int`."
    ),
    hint=(
        "The counter belongs to the class, not to any instance — so `__init__` must "
        "not write it through `self`. Think about what Q-285 showed happens if it does."
    ),
    solution="""\
class Widget:
    count = 0

    def __init__(self, name):
        self.name = name
        Widget.count += 1

    @classmethod
    def made(cls):
        return cls.count

    @classmethod
    def reset(cls):
        cls.count = 0


def build_and_count(names):
    Widget.reset()
    for name in names:
        Widget(name)
    return Widget.made()""",
    explanation=(
        "`self.count += 1` would read the class attribute and then *write an instance* "
        "one, so the shared counter would stay at zero forever while every widget "
        "quietly reported `1` — the exact shadowing from Q-285. Naming the class "
        "explicitly (or going through a classmethod) is what keeps the write landing "
        "where the read came from."
    ),
    starter="""\
class Widget:
    count = 0

    def __init__(self, name):
        ...

    @classmethod
    def made(cls):
        ...

    @classmethod
    def reset(cls):
        ...


def build_and_count(names):
    ...""",
    cases=[
        Case(expected=0, args=([],)),
        Case(expected=1, args=(["a"],)),
        Case(expected=3, args=(["a", "b", "c"],)),
    ],
)

q(
    qid="Q-295",
    level=Level.L3,
    topic="Inheritance",
    kind="function",
    entry="logged",
    prompt=(
        "Define `Logger` with an empty `self.lines` list and a `log(msg)` that appends "
        "`msg`. Define `TimestampLogger(Logger)` that **overrides** `log` to prefix "
        "`\"[t] \"` and then hand the work to the parent with `super()`.\n\n"
        "Write `logged(messages)` that builds a `TimestampLogger`, logs each message, "
        "and returns its `lines` list."
    ),
    hint=(
        "An override does not have to replace the parent's behaviour — it can wrap it. "
        "Doing the appending yourself would duplicate the one line the parent already "
        "owns."
    ),
    solution="""\
class Logger:
    def __init__(self):
        self.lines = []

    def log(self, msg):
        self.lines.append(msg)


class TimestampLogger(Logger):
    def log(self, msg):
        super().log("[t] " + msg)


def logged(messages):
    logger = TimestampLogger()
    for message in messages:
        logger.log(message)
    return logger.lines""",
    explanation=(
        "Extending rather than replacing is the usual reason to override: the subclass "
        "adds its own step and delegates the rest, so a later change to how the parent "
        "stores lines needs no edit here. Calling `self.log(...)` instead of "
        "`super().log(...)` would recurse forever — the single most common way this "
        "pattern is broken."
    ),
    starter="""\
class Logger:
    def __init__(self):
        ...

    def log(self, msg):
        ...


class TimestampLogger(Logger):
    def log(self, msg):
        ...


def logged(messages):
    ...""",
    cases=[
        Case(expected=["[t] a"], args=(["a"],)),
        Case(expected=[], args=([],)),
        Case(expected=["[t] a", "[t] b"], args=(["a", "b"],)),
    ],
)

q(
    qid="Q-296",
    level=Level.L3,
    topic="Polymorphism",
    kind="custom",
    entry="total_area",
    constraints=["needs-comprehension"],
    prompt=(
        "Define `Square` with `__init__(self, side)` and `Rect` with "
        "`__init__(self, w, h)`. They share no base class — each just has its own "
        "`area()` method.\n\n"
        "Write `total_area(specs)` where each spec is `(\"square\", side)` or "
        "`(\"rect\", w, h)`. Build the objects **with a comprehension**, then return "
        "the sum of their areas."
    ),
    hint=(
        "Nothing in the summing step should ask what type a shape is — that question "
        "is answered once, while building. Two unrelated classes that both offer "
        "`area()` are already interchangeable here."
    ),
    solution="""\
class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side


class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h


def total_area(specs):
    shapes = [Square(s[1]) if s[0] == "square" else Rect(s[1], s[2]) for s in specs]
    return sum(shape.area() for shape in shapes)""",
    explanation=(
        "This is *duck typing*: `Square` and `Rect` share no ancestor, yet both are "
        "usable anywhere an `area()` is wanted, because Python resolves the method on "
        "the object at call time rather than on a declared type. Inheritance is one way "
        "to guarantee an interface, not the only way — which is why Python libraries "
        "accept \"anything with a `.read()`\" rather than a specific base class."
    ),
    starter="""\
class Square:
    def __init__(self, side):
        ...

    def area(self):
        ...


class Rect:
    def __init__(self, w, h):
        ...

    def area(self):
        ...


def total_area(specs):
    ...""",
    cases=[
        Case(expected=9, args=([("square", 3)],)),
        Case(expected=14, args=([("square", 2), ("rect", 2, 5)],)),
        Case(expected=0, args=([],)),
        Case(expected=0, args=([("rect", 0, 7)],)),
    ],
)

q(
    qid="Q-297",
    level=Level.L3,
    topic="Encapsulation",
    kind="function",
    entry="try_account",
    prompt=(
        "Define `Account` storing `self._balance`, exposing a **read-only** `balance` "
        "property (a getter and no setter), and a `deposit(amount)` that adds to the "
        "private attribute and returns nothing.\n\n"
        "Write `try_account(action, amount)` that builds `Account(100)` and then:\n\n"
        "- `\"read\"` — return `a.balance`;\n"
        "- `\"deposit\"` — deposit `amount`, then return `a.balance`;\n"
        "- `\"set\"` — assign `amount` to `a.balance` and let whatever happens happen."
    ),
    hint=(
        "A property with only a getter is not merely undocumented for writing — the "
        "write actively fails. Think about which exception type a refused attribute "
        "assignment raises."
    ),
    solution="""\
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount


def try_account(action, amount):
    a = Account(100)
    if action == "read":
        return a.balance
    if action == "deposit":
        a.deposit(amount)
        return a.balance
    a.balance = amount
    return a.balance""",
    explanation=(
        "A getter-only property makes the attribute genuinely read-only from outside: "
        "the assignment raises `AttributeError` instead of silently creating a second "
        "attribute that shadows nothing useful. That is the real value of encapsulation "
        "here — every change to the balance has to go through a method that can enforce "
        "the rules, while `_balance` stays a plain attribute for the class's own use."
    ),
    starter="""\
class Account:
    def __init__(self, balance):
        ...

    @property
    def balance(self):
        ...

    def deposit(self, amount):
        ...


def try_account(action, amount):
    ...""",
    cases=[
        Case(expected=100, args=("read", 0)),
        Case(expected=150, args=("deposit", 50)),
        Case(expected=100, args=("deposit", 0)),
        Case(expected=None, args=("set", 999), raises=AttributeError),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-298",
    level=Level.L4,
    topic="Dunder Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "class Tag:\n"
        "    def __init__(self, name):\n"
        "        self.name = name\n"
        "\n"
        "    def __eq__(self, other):\n"
        "        return self.name == other.name\n"
        "\n"
        "a = Tag(\"x\")\n"
        "print(a == Tag(\"x\"))\n"
        "print(Tag.__hash__ is None)\n"
        "try:\n"
        "    print({a})\n"
        "except TypeError:\n"
        "    print(\"unhashable\")\n"
        "```\n\n"
        "Set `answer` to the three printed lines."
    ),
    hint=(
        "Equality and hashing have to agree: two objects that compare equal must hash "
        "the same. Python cannot keep that promise on your behalf once you write your "
        "own `__eq__`, so it does something drastic instead."
    ),
    solution='answer = "True\\nTrue\\nunhashable"',
    explanation=(
        "Defining `__eq__` sets `__hash__` to `None` unless you define it too, because "
        "the inherited identity-based hash would put two equal objects in different "
        "buckets and break every dict and set. The fix is to define `__hash__` over the "
        "same fields (`return hash(self.name)`) — or to accept immutability and let "
        "`@dataclass(frozen=True)` generate both for you."
    ),
    starter="answer = ...",
    cases=[Case(expected="True\nTrue\nunhashable")],
)

q(
    qid="Q-299",
    level=Level.L4,
    topic="Inheritance",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "class A:\n"
        "    def who(self):\n"
        "        return \"A\"\n"
        "\n"
        "class B(A):\n"
        "    def who(self):\n"
        "        return \"B\"\n"
        "\n"
        "class C(A):\n"
        "    def who(self):\n"
        "        return \"C\"\n"
        "\n"
        "class D(B, C):\n"
        "    pass\n"
        "\n"
        "print(D().who())\n"
        "print([cls.__name__ for cls in D.__mro__])\n"
        "```\n\n"
        "Set `answer` to the two printed lines. Give the list exactly as Python would "
        "print it."
    ),
    hint=(
        "The search is not depth-first — if it were, `A` would be reached before `C` "
        "and `C` could never override anything. A shared ancestor is always visited "
        "after every class that inherits from it."
    ),
    solution="answer = \"B\\n['D', 'B', 'C', 'A', 'object']\"",
    explanation=(
        "Python linearises the hierarchy with C3: local order is preserved and no class "
        "appears before one of its subclasses, which puts `A` last even though `B` "
        "lists it directly. The practical consequence is that `super()` does not mean "
        "\"my parent\" — it means \"the next class in *this object's* MRO\", which is "
        "why `C` gets a turn at all (Q-313)."
    ),
    starter="answer = ...",
    cases=[Case(expected="B\n['D', 'B', 'C', 'A', 'object']")],
)

q(
    qid="Q-300",
    level=Level.L4,
    topic="Dunder Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "class Point:\n"
        "    def __init__(self, x):\n"
        "        self.x = x\n"
        "\n"
        "    def __eq__(self, other):\n"
        "        return self.x == other.x\n"
        "\n"
        "a = Point(1)\n"
        "b = Point(1)\n"
        "print(a == b)\n"
        "print(a is b)\n"
        "print(a in [b])\n"
        "print([a].index(b))\n"
        "```\n\n"
        "Set `answer` to the four printed lines."
    ),
    hint=(
        "`__eq__` changes what `==` means and nothing else. The last two lines are "
        "list operations — look up which comparison the list protocol is documented to "
        "use."
    ),
    solution='answer = "True\\nFalse\\nTrue\\n0"',
    explanation=(
        "`is` asks whether two names point at the same object and can never be "
        "overridden, so a custom `__eq__` leaves it untouched — two equal points are "
        "still two objects. Container searches like `in`, `.index()` and `.remove()` "
        "use identity-or-equality (`x is e or x == e`), which is why they follow your "
        "`__eq__` while `is` does not."
    ),
    starter="answer = ...",
    cases=[Case(expected="True\nFalse\nTrue\n0")],
)

q(
    qid="Q-301",
    level=Level.L4,
    topic="Properties",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output. Note the missing decorator:\n\n"
        "```python\n"
        "class Box:\n"
        "    def __init__(self, n):\n"
        "        self._n = n\n"
        "\n"
        "    def size(self):   # oops - no @property\n"
        "        return self._n\n"
        "\n"
        "b = Box(0)\n"
        "print(type(b.size).__name__)\n"
        "print(b.size == 0)\n"
        "print(bool(b.size))\n"
        "print(b.size() == 0)\n"
        "```\n\n"
        "Set `answer` to the four printed lines."
    ),
    hint=(
        "Without the decorator, `b.size` never runs the body — it produces the callable "
        "itself. Then ask what an arbitrary object with no `__bool__` and no `__len__` "
        "is worth in a boolean context."
    ),
    solution='answer = "method\\nFalse\\nTrue\\nTrue"',
    explanation=(
        "A forgotten `@property` turns every read into a bound method object, and the "
        "danger is that nothing raises: the method object is not equal to anything you "
        "compare it with, and it is always truthy, so `if box.size:` quietly takes the "
        "wrong branch forever. This is why `if user.is_admin:` on a method rather than "
        "a property is a genuine security bug — it is always true."
    ),
    starter="answer = ...",
    cases=[Case(expected="method\nFalse\nTrue\nTrue")],
)

q(
    qid="Q-302",
    level=Level.L4,
    topic="Dunder Methods",
    kind="function",
    entry="sort_names",
    prompt=(
        "Define `Card` with `__init__(self, name, rank)` and a `__lt__` comparing "
        "`rank` only.\n\n"
        "Write `sort_names(pairs)` where `pairs` is a list of `(name, rank)` tuples. "
        "Build the cards, sort them with the plain builtin `sorted` — no `key=` — and "
        "return the **list of names** in the resulting order."
    ),
    hint=(
        "`sorted` needs exactly one comparison to do its job, and `__lt__` is the one "
        "it asks for. Equal ranks should keep their original order; check whether you "
        "need to arrange that yourself."
    ),
    solution="""\
class Card:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

    def __lt__(self, other):
        return self.rank < other.rank


def sort_names(pairs):
    cards = [Card(name, rank) for name, rank in pairs]
    return [card.name for card in sorted(cards)]""",
    explanation=(
        "`sorted`, `min` and `max` are all built on `<` alone, so a single `__lt__` "
        "makes a class orderable — but only for `<`, since Python derives no other "
        "operator from it (use `functools.total_ordering`, as in Q-314, for the rest). "
        "Python's sort is stable, so ties keep their input order without any effort."
    ),
    starter="""\
class Card:
    def __init__(self, name, rank):
        ...

    def __lt__(self, other):
        ...


def sort_names(pairs):
    ...""",
    cases=[
        Case(expected=["low", "high"], args=([("high", 9), ("low", 2)],)),
        Case(expected=[], args=([],)),
        Case(expected=["a", "b", "c"], args=([("a", 1), ("b", 2), ("c", 3)],)),
        Case(expected=["first", "second"], args=([("first", 5), ("second", 5)],)),
    ],
)

q(
    qid="Q-303",
    level=Level.L4,
    topic="Dunder Methods",
    kind="function",
    entry="apply_factor",
    prompt=(
        "Define `Multiplier` with `__init__(self, factor)` and a `__call__(self, x)` "
        "returning `x * factor`, so the instance can be used like a function.\n\n"
        "Write `apply_factor(factor, values)` returning the tuple "
        "`(callable(m), [m(v) for v in values])` — a bool and a list."
    ),
    hint=(
        "`m(3)` is not special syntax for functions; it is a dunder like any other. "
        "The builtin in the first element of the tuple asks whether the *type* defines "
        "it."
    ),
    solution="""\
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor


def apply_factor(factor, values):
    m = Multiplier(factor)
    return (callable(m), [m(v) for v in values])""",
    explanation=(
        "Anything with `__call__` is callable, which is what lets a configured object "
        "be passed straight to `map`, `sorted(key=...)` or a framework that expects a "
        "function. Compared with a closure it gives you the same behaviour plus "
        "inspectable state and a useful `__repr__` — that is exactly how decorators "
        "with arguments and most \"policy object\" designs are built."
    ),
    starter="""\
class Multiplier:
    def __init__(self, factor):
        ...

    def __call__(self, x):
        ...


def apply_factor(factor, values):
    ...""",
    cases=[
        Case(expected=(True, [2, 4, 6]), args=(2, [1, 2, 3])),
        Case(expected=(True, []), args=(3, [])),
        Case(expected=(True, [0, 0]), args=(0, [5, 9])),
        Case(expected=(True, ["aa"]), args=(2, ["a"])),
    ],
)

q(
    qid="Q-304",
    level=Level.L4,
    topic="Dunder Methods",
    kind="function",
    entry="countdown_list",
    prompt=(
        "Define `Countdown` with `__init__(self, start)` and an `__iter__` that "
        "**yields** `start, start - 1, ... , 1`. Write `__iter__` as a generator — no "
        "separate iterator class, no `__next__`.\n\n"
        "Write `countdown_list(start)` returning `list(Countdown(start))`. For "
        "`start = 0` the list is empty."
    ),
    hint=(
        "A `def` containing `yield` returns a generator when called — and a generator "
        "is already an iterator. That is precisely what `__iter__` is required to hand "
        "back."
    ),
    solution="""\
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        for n in range(self.start, 0, -1):
            yield n


def countdown_list(start):
    return list(Countdown(start))""",
    explanation=(
        "Making `__iter__` a generator collapses the whole iterator protocol into one "
        "method: Python calls it, gets a fresh generator, and that generator supplies "
        "`__next__` and `StopIteration` for you. Because each call produces a *new* "
        "generator, the object can be iterated repeatedly — whereas returning `self` "
        "from `__iter__` gives a one-shot object that is silently empty the second "
        "time round."
    ),
    starter="""\
class Countdown:
    def __init__(self, start):
        ...

    def __iter__(self):
        ...


def countdown_list(start):
    ...""",
    cases=[
        Case(expected=[3, 2, 1], args=(3,)),
        Case(expected=[1], args=(1,)),
        Case(expected=[], args=(0,)),
        Case(expected=[5, 4, 3, 2, 1], args=(5,)),
    ],
)

q(
    qid="Q-305",
    level=Level.L4,
    topic="Inheritance",
    kind="function",
    entry="make",
    prompt=(
        "Using `abc`, define `Shape(ABC)` with an `@abstractmethod name(self)`, then "
        "`Circle(Shape)` and `Square(Shape)` returning `\"circle\"` and `\"square\"`.\n\n"
        "Write `make(kind)`: for `\"circle\"` and `\"square\"` return the matching "
        "object's `name()`; for anything else, attempt to instantiate `Shape()` itself "
        "and let the failure escape."
    ),
    hint=(
        "An abstract base class is not blocked from being subclassed — it is blocked "
        "from being *instantiated* while any abstract method is unimplemented. That "
        "check happens at construction, and it is not an `AttributeError`."
    ),
    solution="""\
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def name(self):
        ...


class Circle(Shape):
    def name(self):
        return "circle"


class Square(Shape):
    def name(self):
        return "square"


def make(kind):
    if kind == "circle":
        return Circle().name()
    if kind == "square":
        return Square().name()
    return Shape().name()""",
    explanation=(
        "`ABCMeta` refuses to construct any class that still has unimplemented "
        "abstract methods, so the mistake is caught at the moment of creation rather "
        "than when the missing method is finally called in production. That is the "
        "trade: an ABC states the interface up front, where duck typing (Q-296) leaves "
        "it implicit and fails later."
    ),
    starter="""\
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def name(self):
        ...


class Circle(Shape):
    ...


class Square(Shape):
    ...


def make(kind):
    ...""",
    cases=[
        Case(expected="circle", args=("circle",)),
        Case(expected="square", args=("square",)),
        Case(expected=None, args=("shape",), raises=TypeError),
        Case(expected=None, args=("",), raises=TypeError),
    ],
)

q(
    qid="Q-306",
    level=Level.L4,
    topic="Composition",
    kind="function",
    entry="car_report",
    prompt=(
        "Define `Engine` with `__init__(self, hp)` and `start()` returning "
        "`\"vroom\"`. Define `Car` which **builds its own** `Engine` in `__init__`, "
        "delegates `start()` to it, and exposes the engine's `hp` through a property.\n\n"
        "`Car` must not inherit from `Engine`. Write `car_report(make, hp)` returning "
        "`(c.make, c.hp, c.start(), isinstance(c, Engine))`."
    ),
    hint=(
        "Delegation is a one-line method that forwards the call. The property exists "
        "so callers never have to write `car.engine.hp` — the engine stays an "
        "implementation detail."
    ),
    solution="""\
class Engine:
    def __init__(self, hp):
        self.hp = hp

    def start(self):
        return "vroom"


class Car:
    def __init__(self, make, hp):
        self.make = make
        self.engine = Engine(hp)

    @property
    def hp(self):
        return self.engine.hp

    def start(self):
        return self.engine.start()


def car_report(make, hp):
    c = Car(make, hp)
    return (c.make, c.hp, c.start(), isinstance(c, Engine))""",
    explanation=(
        "Inheriting would have made a car *be* an engine — true for `isinstance`, false "
        "for anyone reading the code, and it would drag in every future `Engine` method "
        "whether it made sense on a car or not. Composition exposes only what you "
        "forward, so the engine can be swapped for an `ElectricMotor` without a single "
        "caller noticing."
    ),
    starter="""\
class Engine:
    def __init__(self, hp):
        ...

    def start(self):
        ...


class Car:
    def __init__(self, make, hp):
        ...

    @property
    def hp(self):
        ...

    def start(self):
        ...


def car_report(make, hp):
    ...""",
    cases=[
        Case(expected=("Volvo", 150, "vroom", False), args=("Volvo", 150)),
        Case(expected=("Kia", 0, "vroom", False), args=("Kia", 0)),
        Case(expected=("", 90, "vroom", False), args=("", 90)),
    ],
)

q(
    qid="Q-307",
    level=Level.L4,
    topic="Properties",
    kind="function",
    entry="round_trip",
    prompt=(
        "Define `Temp` storing only `self._celsius`, with a `fahrenheit` property "
        "that converts on read (`c * 9 / 5 + 32`) and converts back on write "
        "(`(f - 32) * 5 / 9`). Store nothing in Fahrenheit.\n\n"
        "Write `round_trip(celsius, new_f)` that builds `Temp(celsius)`, records "
        "`t.fahrenheit`, then assigns `new_f` to `t.fahrenheit`, and returns "
        "`(recorded_fahrenheit, t._celsius)` — two floats."
    ),
    hint=(
        "There is one source of truth and one derived view of it. The setter's job is "
        "to run the conversion backwards so the single stored field stays authoritative."
    ),
    solution="""\
class Temp:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9


def round_trip(celsius, new_f):
    t = Temp(celsius)
    recorded = t.fahrenheit
    t.fahrenheit = new_f
    return (recorded, t._celsius)""",
    explanation=(
        "A property pair turns a derived value into a writable view of one stored "
        "field, so the two units can never drift apart — storing both and \"keeping "
        "them in sync\" is the bug this design removes. Note the results are floats "
        "even for whole degrees, because `/` is true division; exact round-trips are "
        "not guaranteed either, since `(c * 9 / 5 + 32 - 32) * 5 / 9` is binary "
        "floating point, not algebra."
    ),
    starter="""\
class Temp:
    def __init__(self, celsius):
        ...

    @property
    def fahrenheit(self):
        ...

    @fahrenheit.setter
    def fahrenheit(self, value):
        ...


def round_trip(celsius, new_f):
    ...""",
    cases=[
        Case(expected=(32.0, 100.0), args=(0, 212)),
        Case(expected=(212.0, 0.0), args=(100, 32)),
        Case(expected=(-40.0, -40.0), args=(-40, -40)),
    ],
)

q(
    qid="Q-308",
    level=Level.L4,
    topic="Class & Static Methods",
    kind="function",
    entry="created_name",
    prompt=(
        "Define `Base` with `__init__(self, label)` and a `@classmethod create(cls, "
        "label)` that returns a new instance. Define `Child(Base)` with an empty body.\n\n"
        "Write `created_name(which, label)`: call `create` on `Base` when `which` is "
        "`\"base\"` and on `Child` otherwise, then return "
        "`(type(obj).__name__, obj.label)`."
    ),
    hint=(
        "`cls` is whichever class the call was made through, not the class the method "
        "was written in. Hard-coding the class name in `create` is what breaks the "
        "`Child` case."
    ),
    solution="""\
class Base:
    def __init__(self, label):
        self.label = label

    @classmethod
    def create(cls, label):
        return cls(label)


class Child(Base):
    pass


def created_name(which, label):
    cls = Base if which == "base" else Child
    obj = cls.create(label)
    return (type(obj).__name__, obj.label)""",
    explanation=(
        "A classmethod receives the class it was *called on*, so `cls(label)` builds a "
        "`Child` when invoked as `Child.create(...)` — the factory is inherited and "
        "still returns the right type. Writing `return Base(label)` would work until "
        "the first subclass appeared and then silently hand back the wrong class, which "
        "is why alternative constructors always use `cls`."
    ),
    starter="""\
class Base:
    def __init__(self, label):
        ...

    @classmethod
    def create(cls, label):
        ...


class Child(Base):
    ...


def created_name(which, label):
    ...""",
    cases=[
        Case(expected=("Base", "a"), args=("base", "a")),
        Case(expected=("Child", "b"), args=("child", "b")),
        Case(expected=("Child", ""), args=("child", "")),
    ],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-309",
    level=Level.L5,
    topic="Dunder Methods",
    kind="function",
    entry="vector_ops",
    prompt=(
        "Define `Vector` with `__init__(self, x, y)` and these dunders: `__add__`, "
        "`__mul__` (by a number), `__rmul__`, `__eq__` (only against another "
        "`Vector`), and `__repr__` giving `\"Vector(1, 2)\"`.\n\n"
        "Write `vector_ops(a, b, k)` where `a` and `b` are `(x, y)` tuples. Return the "
        "4-tuple `(repr(va + vb), repr(va * k), repr(k * va), (va + vb) == (vb + va))`."
    ),
    hint=(
        "`k * va` does not call `__mul__` — the int is on the left and gets asked "
        "first. Work out what Python does when the left operand declines, and which "
        "second dunder that reaches."
    ),
    solution="""\
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    def __rmul__(self, k):
        return self * k

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


def vector_ops(a, b, k):
    va = Vector(*a)
    vb = Vector(*b)
    return (repr(va + vb), repr(va * k), repr(k * va), (va + vb) == (vb + va))""",
    explanation=(
        "For `k * va` Python asks `int.__mul__(k, va)` first, gets `NotImplemented`, "
        "and only then tries the *reflected* operation `va.__rmul__(k)` — without it, "
        "`2 * v` raises `TypeError` while `v * 2` works, an asymmetry that looks "
        "inexplicable from the call site. Every binary operator has this reflected "
        "twin, which is also why returning `NotImplemented` rather than `False` from "
        "`__eq__` (Q-288) matters."
    ),
    starter="""\
class Vector:
    def __init__(self, x, y):
        ...

    def __add__(self, other):
        ...

    def __mul__(self, k):
        ...

    def __rmul__(self, k):
        ...

    def __eq__(self, other):
        ...

    def __repr__(self):
        ...


def vector_ops(a, b, k):
    ...""",
    cases=[
        Case(expected=("Vector(4, 6)", "Vector(2, 4)", "Vector(2, 4)", True),
             args=((1, 2), (3, 4), 2)),
        Case(expected=("Vector(0, 0)", "Vector(0, 0)", "Vector(0, 0)", True),
             args=((0, 0), (0, 0), 3)),
        Case(expected=("Vector(1, 1)", "Vector(0, 0)", "Vector(0, 0)", True),
             args=((1, 1), (0, 0), 0)),
        Case(expected=("Vector(-1, 1)", "Vector(3, -3)", "Vector(3, -3)", True),
             args=((1, -1), (-2, 2), 3)),
    ],
)

q(
    qid="Q-310",
    level=Level.L5,
    topic="Composition",
    kind="custom",
    entry="tree_size",
    constraints=["needs-recursion"],
    prompt=(
        "Define one class `Node` with `__init__(self, name, size=0, children=())` and "
        "a `total_size()` returning its own size plus the total size of every child, "
        "however deep.\n\n"
        "Write `tree_size(spec)` where a spec is either `(\"file\", name, size)` or "
        "`(\"dir\", name, [child_specs])`. It must **call itself** for each child. "
        "Return the total size as a number. A directory of its own contributes `0`."
    ),
    hint=(
        "A node that holds nodes is the composite pattern — `total_size` asks each "
        "child the same question it was asked. Collapsing each child subtree into a "
        "single sized `Node` keeps the recursion to one line."
    ),
    solution="""\
class Node:
    def __init__(self, name, size=0, children=()):
        self.name = name
        self.size = size
        self.children = list(children)

    def total_size(self):
        return self.size + sum(child.total_size() for child in self.children)


def tree_size(spec):
    kind, name, payload = spec
    if kind == "file":
        return Node(name, size=payload).total_size()
    children = [Node(c[1], size=tree_size(c)) for c in payload]
    return Node(name, children=children).total_size()""",
    explanation=(
        "The composite pattern lets a leaf and a container answer the same question, "
        "so `total_size` never asks what kind of node it is holding — the recursion "
        "terminates by itself when a node has no children. Note `children=()` as the "
        "default rather than `[]`: a mutable default is evaluated once at definition "
        "time and shared by every call, which is the function-level form of the class "
        "attribute bug in Q-284."
    ),
    starter="""\
class Node:
    def __init__(self, name, size=0, children=()):
        ...

    def total_size(self):
        ...


def tree_size(spec):
    ...""",
    cases=[
        Case(expected=10, args=(("file", "a.txt", 10),)),
        Case(expected=0, args=(("dir", "empty", []),)),
        Case(expected=30, args=(("dir", "root", [("file", "a", 10), ("file", "b", 20)]),)),
        Case(expected=6, args=(("dir", "root", [
            ("file", "a", 1),
            ("dir", "sub", [("file", "b", 2), ("dir", "deep", [("file", "c", 3)])]),
        ]),)),
    ],
)

q(
    qid="Q-311",
    level=Level.L5,
    topic="Encapsulation",
    kind="function",
    entry="touch",
    prompt=(
        "Define `Frozen` that sets `self.x` and `self.y` in `__init__`, then sets "
        "`self._locked = True` as its last statement. Override `__setattr__` so that "
        "once `_locked` is set, any further assignment raises `AttributeError`; before "
        "that, assignments go through normally.\n\n"
        "Write `touch(action, value)` building `Frozen(1, 2)` and then:\n\n"
        "- `\"read\"` — return `(f.x, f.y)`;\n"
        "- `\"write\"` — do `f.x = value` and return `(f.x, f.y)`;\n"
        "- `\"delete\"` — do `del f.x` and return `hasattr(f, \"x\")`."
    ),
    hint=(
        "`self._locked = True` goes through your own `__setattr__` too, so the guard "
        "has to tolerate the flag not existing yet. To actually store a value once you "
        "have overridden the hook, call the base implementation explicitly. And ask "
        "yourself which dunder `del` uses."
    ),
    solution="""\
class Frozen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._locked = True

    def __setattr__(self, name, value):
        if getattr(self, "_locked", False):
            raise AttributeError(f"{type(self).__name__} is immutable")
        object.__setattr__(self, name, value)


def touch(action, value):
    f = Frozen(1, 2)
    if action == "read":
        return (f.x, f.y)
    if action == "delete":
        del f.x
        return hasattr(f, "x")
    f.x = value
    return (f.x, f.y)""",
    explanation=(
        "`__setattr__` intercepts *every* assignment, including the ones inside "
        "`__init__`, so it must both tolerate the half-built object and store through "
        "`object.__setattr__` — writing `self.name = value` inside it recurses until "
        "the stack overflows. The deletion case is the lesson: guarding one hook leaves "
        "`__delattr__` wide open, which is why real immutability comes from "
        "`@dataclass(frozen=True)`, a `NamedTuple`, or `__slots__` plus discipline "
        "rather than from a hand-rolled guard."
    ),
    starter="""\
class Frozen:
    def __init__(self, x, y):
        ...

    def __setattr__(self, name, value):
        ...


def touch(action, value):
    ...""",
    cases=[
        Case(expected=(1, 2), args=("read", 0)),
        Case(expected=False, args=("delete", 0)),
        Case(expected=None, args=("write", 9), raises=AttributeError),
        Case(expected=None, args=("write", 0), raises=AttributeError),
    ],
)

q(
    qid="Q-312",
    level=Level.L5,
    topic="Dunder Methods",
    kind="custom",
    entry="run",
    constraints=["needs-with"],
    prompt=(
        "Define two context managers over a shared `log` list. `Tracker` appends "
        "`\"enter\"` in `__enter__` (returning `self`) and `\"exit\"` in `__exit__`, "
        "returning a falsy value. `Swallower` is identical except its `__exit__` "
        "returns `True`.\n\n"
        "Write `run(kind, should_raise)`: build a `Swallower` for `\"swallow\"` and a "
        "`Tracker` otherwise; in a **`with` block** append `\"body\"` and raise "
        "`ValueError` if asked; after the block append `\"after\"`; wrap the whole "
        "thing in `try/except ValueError` appending `\"caught\"`. Return the log."
    ),
    hint=(
        "`__exit__` receives the exception and its return value decides the exception's "
        "fate. One of these two managers stops the `ValueError` from ever reaching your "
        "`except` clause — and that changes which of the two trailing entries appears."
    ),
    solution="""\
class Tracker:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("enter")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.log.append("exit")
        return False


class Swallower(Tracker):
    def __exit__(self, exc_type, exc, tb):
        super().__exit__(exc_type, exc, tb)
        return True


def run(kind, should_raise):
    log = []
    manager = Swallower(log) if kind == "swallow" else Tracker(log)
    try:
        with manager:
            log.append("body")
            if should_raise:
                raise ValueError("boom")
        log.append("after")
    except ValueError:
        log.append("caught")
    return log""",
    explanation=(
        "`__exit__` always runs, and a **truthy** return value suppresses the "
        "exception — so `Swallower` makes the `with` statement complete normally and "
        "execution continues to `\"after\"`, while `Tracker` lets the `ValueError` "
        "propagate to the `except`. Returning `True` unconditionally is almost always "
        "wrong: it hides every error, including ones you never anticipated, which is "
        "why the default should be to return `None` and say nothing."
    ),
    starter="""\
class Tracker:
    def __init__(self, log):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc, tb):
        ...


class Swallower(Tracker):
    def __exit__(self, exc_type, exc, tb):
        ...


def run(kind, should_raise):
    ...""",
    cases=[
        Case(expected=["enter", "body", "exit", "after"], args=("plain", False)),
        Case(expected=["enter", "body", "exit", "caught"], args=("plain", True)),
        Case(expected=["enter", "body", "exit", "after"], args=("swallow", True)),
        Case(expected=["enter", "body", "exit", "after"], args=("swallow", False)),
    ],
)

q(
    qid="Q-313",
    level=Level.L5,
    topic="Inheritance",
    kind="function",
    entry="pipeline",
    prompt=(
        "Define `Base` with `steps()` returning `[\"base\"]`. Define `Loud(Base)` and "
        "`Fast(Base)` whose `steps()` each return their own name prepended to "
        "`super().steps()`. Define `Both(Loud, Fast)` doing the same with "
        "`\"both\"`.\n\n"
        "Write `pipeline(which)` taking `\"both\"`, `\"loud\"`, `\"fast\"` or "
        "`\"base\"`, building that class and returning its `steps()` list. Every class "
        "must use `super()` — never name a parent directly."
    ),
    hint=(
        "Inside `Loud.steps`, `super()` does not necessarily mean `Base`. It means the "
        "next class along the MRO of the object that is actually running — and for a "
        "`Both` instance that is a class `Loud` has never heard of. Q-299 has the "
        "ordering rule."
    ),
    solution="""\
class Base:
    def steps(self):
        return ["base"]


class Loud(Base):
    def steps(self):
        return ["loud"] + super().steps()


class Fast(Base):
    def steps(self):
        return ["fast"] + super().steps()


class Both(Loud, Fast):
    def steps(self):
        return ["both"] + super().steps()


def pipeline(which):
    table = {"both": Both, "loud": Loud, "fast": Fast, "base": Base}
    return table[which]().steps()""",
    explanation=(
        "`super()` walks the MRO of `type(self)`, so inside a `Both` instance "
        "`Loud.steps`'s `super()` resolves to `Fast` — every class in the chain gets a "
        "turn, which is what makes cooperative mixins work. Writing "
        "`Base.steps(self)` instead would skip `Fast` entirely and, in a diamond, call "
        "the shared ancestor twice; that is the concrete reason `super()` is not just "
        "a nicer spelling."
    ),
    starter="""\
class Base:
    def steps(self):
        ...


class Loud(Base):
    def steps(self):
        ...


class Fast(Base):
    def steps(self):
        ...


class Both(Loud, Fast):
    def steps(self):
        ...


def pipeline(which):
    ...""",
    cases=[
        Case(expected=["both", "loud", "fast", "base"], args=("both",)),
        Case(expected=["loud", "base"], args=("loud",)),
        Case(expected=["fast", "base"], args=("fast",)),
        Case(expected=["base"], args=("base",)),
    ],
)

q(
    qid="Q-314",
    level=Level.L5,
    topic="Dunder Methods",
    kind="function",
    entry="compare_versions",
    prompt=(
        "Define `Version`, decorated with `functools.total_ordering`. `__init__` takes "
        "a string like `\"1.2.0\"` and stores `self.parts` as a tuple of ints. Define "
        "`__eq__` and `__lt__` over `parts` and nothing else — no `__le__`, `__gt__` "
        "or `__ge__`.\n\n"
        "Write `compare_versions(a, b)` returning the 5-tuple "
        "`(va < vb, va <= vb, va > vb, va >= vb, va == vb)` — five bools."
    ),
    hint=(
        "Comparing the tuples of ints does all the ordering work, including "
        "`\"1.10\"` beating `\"1.2\"`. The decorator fills in the three operators you "
        "did not write, from the two you did."
    ),
    solution="""\
from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts


def compare_versions(a, b):
    va = Version(a)
    vb = Version(b)
    return (va < vb, va <= vb, va > vb, va >= vb, va == vb)""",
    explanation=(
        "`@total_ordering` derives `<=`, `>` and `>=` from `__eq__` plus one ordering "
        "operator, so a single source of truth cannot drift out of sync the way four "
        "hand-written comparisons eventually do. Comparing tuples of ints is also what "
        "makes version ordering correct: `\"1.10\"` sorts *after* `\"1.2\"` numerically "
        "but before it as a string, which is the classic release-numbering bug."
    ),
    starter="""\
from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, text):
        ...

    def __eq__(self, other):
        ...

    def __lt__(self, other):
        ...


def compare_versions(a, b):
    ...""",
    cases=[
        Case(expected=(True, True, False, False, False), args=("1.2.0", "1.10.0")),
        Case(expected=(False, True, False, True, True), args=("2.0", "2.0")),
        Case(expected=(False, False, True, True, False), args=("3.1", "3.0.9")),
        Case(expected=(True, True, False, False, False), args=("1.0", "1.0.1")),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-08",
    title="Bank account hierarchy",
    brief=(
        "Build a small account hierarchy, then drive it with "
        "`run_account(spec, ops)`.\n\n"
        "`Account(owner, balance)` stores `self._balance`, exposes a **read-only** "
        "`balance` property, and has `deposit(amount)` and `withdraw(amount)`. Both "
        "raise `ValueError` for a non-positive amount, and `withdraw` raises "
        "`ValueError` when the amount exceeds what is available. Give it a `__repr__` "
        "of the form `Account('Ada', 120)` using the **actual class name**, and an "
        "`__eq__` that requires the same class, owner and balance.\n\n"
        "`Savings(Account)` adds `rate` (default `0.02`) and `add_interest()`, which "
        "adds `round(balance * rate, 2)` to the balance. `Current(Account)` adds "
        "`overdraft` (default `0`) and may be withdrawn down to `-overdraft` — change "
        "*only* what 'available' means, not `withdraw` itself.\n\n"
        "`run_account(spec, ops)`: `spec` is `(kind, owner, opening)` with `kind` in "
        "`\"basic\"`/`\"savings\"`/`\"current\"` (a current account gets an overdraft "
        "of `100`). Each op is `(\"deposit\", n)`, `(\"withdraw\", n)`, "
        "`(\"interest\",)` or `(\"set_balance\", n)`. Apply them in order, catching "
        "`ValueError` and `AttributeError` and appending the exception's type name to "
        "an `errors` list. Return\n\n"
        "```python\n"
        "(repr(acct), acct.balance, errors, acct == Account(owner, acct.balance))\n"
        "```"
    ),
    hint=(
        "Put the overdraft rule behind a small overridable hook — a `_available()` "
        "method the base class uses in `withdraw` — so the subclass changes one line "
        "and inherits every validation. `type(self).__name__` inside `__repr__` gives "
        "each subclass the right name for free."
    ),
    solution="""\
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def _available(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._available():
            raise ValueError("insufficient funds")
        self._balance -= amount

    def __repr__(self):
        return f"{type(self).__name__}({self.owner!r}, {self._balance})"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return (type(self), self.owner, self._balance) == (
            type(other), other.owner, other._balance,
        )


class Savings(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        self._balance += round(self._balance * self.rate, 2)


class Current(Account):
    def __init__(self, owner, balance=0, overdraft=0):
        super().__init__(owner, balance)
        self.overdraft = overdraft

    def _available(self):
        return self._balance + self.overdraft


def run_account(spec, ops):
    kind, owner, opening = spec
    if kind == "savings":
        acct = Savings(owner, opening)
    elif kind == "current":
        acct = Current(owner, opening, overdraft=100)
    else:
        acct = Account(owner, opening)
    errors = []
    for op in ops:
        try:
            if op[0] == "deposit":
                acct.deposit(op[1])
            elif op[0] == "withdraw":
                acct.withdraw(op[1])
            elif op[0] == "interest":
                acct.add_interest()
            elif op[0] == "set_balance":
                acct.balance = op[1]
        except (ValueError, AttributeError) as exc:
            errors.append(type(exc).__name__)
    return (repr(acct), acct.balance, errors, acct == Account(owner, acct.balance))""",
    explanation=(
        "The design move worth keeping is the `_available()` hook: `withdraw` owns "
        "every rule that is the same for all accounts, and `Current` overrides the one "
        "line that genuinely differs — no copied validation, no `isinstance` check. "
        "Two behaviours fall out of the rest: `acct.balance = n` raises `AttributeError` "
        "because the property has no setter, and `Savings` is never `==` a plain "
        "`Account` because the comparison includes the exact type, so a subclass cannot "
        "sneak past an equality check."
    ),
    entry="run_account",
    starter="""\
class Account:
    def __init__(self, owner, balance=0):
        ...


class Savings(Account):
    ...


class Current(Account):
    ...


def run_account(spec, ops):
    ...""",
    cases=[
        Case(expected=("Account('Ada', 120)", 120, [], True),
             args=(("basic", "Ada", 100), [("deposit", 50), ("withdraw", 30)])),
        Case(expected=("Account('Ada', 100)", 100, ["ValueError"], True),
             args=(("basic", "Ada", 100), [("withdraw", 200)])),
        Case(expected=("Current('Bo', -70)", -70, [], False),
             args=(("current", "Bo", 50), [("withdraw", 120)])),
        Case(expected=("Current('Bo', 50)", 50, ["ValueError"], False),
             args=(("current", "Bo", 50), [("withdraw", 200)])),
        Case(expected=("Savings('Cy', 1020.0)", 1020.0, [], False),
             args=(("savings", "Cy", 1000), [("interest",)])),
        Case(expected=("Account('Ada', 0)", 0, ["ValueError", "AttributeError"], True),
             args=(("basic", "Ada", 0), [("deposit", -5), ("interest",)])),
        Case(expected=("Account('Dee', 10)", 10, ["AttributeError"], True),
             args=(("basic", "Dee", 10), [("set_balance", 99)])),
    ],
)

NOTEBOOK = Notebook(
    number=8,
    slug="oop",
    title="OOP",
    intro=(
        "Classes and instances, inheritance and `super()`, polymorphism, "
        "encapsulation, composition, properties, class and static methods, and the "
        "dunder methods that let your own types behave like builtins.\n\n"
        "This notebook is harder than the ones before it, on purpose. Most of the "
        "traps here are not syntax — they are the places where Python's object model "
        "does something reasonable that you did not ask for: a mutable class attribute "
        "shared by every instance, an assignment that silently shadows instead of "
        "updating, a `__eq__` that makes your object unhashable, a forgotten "
        "`@property` that is always truthy."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
