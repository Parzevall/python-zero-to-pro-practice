import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB25", title="Descriptors & Metaprogramming", intro="""
    What happens when Python looks up, sets and creates things: attribute
    lookup, descriptors (the machinery behind `property`, methods and
    `classmethod`), `__init_subclass__`, building classes with `type()`,
    metaclasses and customised `isinstance`. Every task is something real:
    validated fields, plugin registries, a tiny ORM.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", """
    A `Profile` class has a normal attribute `name = "Ada"`. Add a
    `__getattr__` so that reading any attribute that does **not** exist returns
    the text `"unknown"` instead of raising. Print `name` and `age` of a profile.
""",
     solution='class Profile:\n'
              '    name = "Ada"\n'
              '    def __getattr__(self, attr):\n'
              '        return "unknown"\n\n'
              'p = Profile()\nprint(p.name)\nprint(p.age)')

nb.q("Output-match", """
    Without a `class` statement, use `type()` to create a class `Point` with
    class attributes `x = 0` and `y = 0`. Make an instance and print its `x`
    and the class name.
""",
     solution='Point = type("Point", (), {"x": 0, "y": 0})\np = Point()\nprint(p.x, type(p).__name__)')

nb.q("Real-life", """
    A calculator box receives text typed by users. Use `eval` with its
    builtins switched off (`{"__builtins__": {}}` as globals) to compute each
    expression and print the result. When evaluating raises an exception, print
    `blocked:` and the exception's class name instead.
""",
     given='exprs = ["2 + 3 * 4", "(10 - 4) / 3", "__import__(\'os\').getcwd()"]',
     solution='for text in exprs:\n'
              '    try:\n'
              '        print(eval(text, {"__builtins__": {}}))\n'
              '    except Exception as err:\n'
              '        print("blocked:", type(err).__name__)')

nb.q("Real-life", """
    A shop class charges 20% tax through its `tax_rate(self)` method. For a
    one-off sale test, replace that method **on the class** (monkey-patch)
    with a function that returns `0.0`, then print the rate of a new shop.
""",
     given='class Shop:\n    def tax_rate(self):\n        return 0.2\n\nprint(Shop().tax_rate())',
     solution='Shop.tax_rate = lambda self: 0.0\nprint(Shop().tax_rate())')

nb.q("Build", """
    Using `inspect` and `vars`: print the list of parameter names of the
    `Order` constructor, then print the instance dictionary of
    `Order("tea", 2)`.
""",
     given='class Order:\n    def __init__(self, item, qty=1):\n        self.item = item\n        self.qty = qty',
     solution='import inspect\n'
              'print(list(inspect.signature(Order).parameters))\n'
              'print(vars(Order("tea", 2)))')

# ------------------------------------------------------- Combine
nb.q("Build", """
    Write a descriptor class `Tag` whose `__set_name__` prints
    `bound to <attribute name>`. Use it as two class attributes `color` and
    `wheels` of a `Car` class and just run the class definition.
""",
     solution='class Tag:\n'
              '    def __set_name__(self, owner, name):\n'
              '        print("bound to", name)\n\n'
              'class Car:\n    color = Tag()\n    wheels = Tag()')

nb.q("Real-life", """
    Build a plugin list with `__init_subclass__`. The base class `Plugin` keeps
    a list `names` and every subclass adds its own class name when it is
    defined. Define `Backup` and `Cleanup` as subclasses, then print the list.
""",
     solution='class Plugin:\n'
              '    names = []\n'
              '    def __init_subclass__(cls, **kwargs):\n'
              '        super().__init_subclass__(**kwargs)\n'
              '        Plugin.names.append(cls.__name__)\n\n'
              'class Backup(Plugin): pass\nclass Cleanup(Plugin): pass\nprint(Plugin.names)')

nb.q("Output-match", """
    `property` is built on the descriptor protocol. For the class below, print
    the type name of what is stored under `"celsius"` in the class dictionary,
    then whether that object has `__get__` and whether it has `__set__`.
""",
     given='class Temp:\n    @property\n    def celsius(self):\n        return 21.5',
     solution='prop = Temp.__dict__["celsius"]\n'
              'print(type(prop).__name__)\n'
              'print(hasattr(prop, "__get__"), hasattr(prop, "__set__"))')

nb.q("Puzzle", """
    Create a class `Demo` with attribute `n` set to a `NonData()` and
    attribute `d` set to a `Data()`. Make an instance and assign the text
    `"mine"` to both `n` and `d`. Print `n`, then `d`, and see which one the
    instance really kept.
""",
     given='class NonData:\n'
           '    def __get__(self, obj, owner=None):\n'
           '        return "descriptor"\n\n'
           'class Data(NonData):\n'
           '    def __set__(self, obj, value):\n'
           '        pass',
     solution='class Demo:\n    n = NonData()\n    d = Data()\n\n'
              'demo = Demo()\ndemo.n = "mine"\ndemo.d = "mine"\n'
              'print(demo.n)\nprint(demo.d)')

nb.q("Output-match", """
    Write a class `Box` with a `__class_getitem__` so that `Box[int]` returns
    the text `Box of int` (use the type's `__name__`). Print `Box[int]` and
    `Box[str]`.
""",
     solution='class Box:\n'
              '    def __class_getitem__(cls, item):\n'
              '        return "Box of " + item.__name__\n\n'
              'print(Box[int])\nprint(Box[str])')

# ------------------------------------------------------- Small real tasks
nb.q("Real-life", """
    Write a descriptor `Typed(expected_type)` that stores the value in the
    instance's `__dict__` under the attribute's own name (use `__set_name__`)
    and raises `TypeError` when the value has the wrong type. Use it for `name`
    (str) and `age` (int) in an `Employee` class whose `__init__` takes both.
    Create `Employee("Mia", 31)` and print its name and age, then try
    `Employee("Sam", "forty")` and print the error message.
""",
     solution='class Typed:\n'
              '    def __init__(self, expected_type):\n'
              '        self.expected_type = expected_type\n'
              '    def __set_name__(self, owner, name):\n'
              '        self.name = name\n'
              '    def __get__(self, obj, owner=None):\n'
              '        if obj is None:\n'
              '            return self\n'
              '        return obj.__dict__[self.name]\n'
              '    def __set__(self, obj, value):\n'
              '        if not isinstance(value, self.expected_type):\n'
              '            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")\n'
              '        obj.__dict__[self.name] = value\n\n'
              'class Employee:\n'
              '    name = Typed(str)\n'
              '    age = Typed(int)\n'
              '    def __init__(self, name, age):\n'
              '        self.name = name\n'
              '        self.age = age\n\n'
              'mia = Employee("Mia", 31)\nprint(mia.name, mia.age)\n'
              'try:\n    Employee("Sam", "forty")\nexcept TypeError as err:\n    print(err)')

nb.q("Real-life", """
    Write an `Audited` class that records the name of every attribute read from
    an instance in a list `reads` (stored in the instance dictionary), by
    overriding `__getattribute__`. Take care not to recurse forever. Set
    `price` and `stock` in `__init__`, read `price`, `stock` and `price` again,
    and print the log of names.
""",
     solution='class Audited:\n'
              '    def __init__(self):\n'
              '        self.__dict__["reads"] = []\n'
              '        self.price = 9.5\n'
              '        self.stock = 12\n'
              '    def __getattribute__(self, name):\n'
              '        if name in ("price", "stock"):\n'
              '            object.__getattribute__(self, "reads").append(name)\n'
              '        return object.__getattribute__(self, name)\n\n'
              'item = Audited()\nitem.price\nitem.stock\nitem.price\n'
              'print(item.reads)')

nb.q("Puzzle", """
    See how `classmethod` works by building your own. Write a descriptor class
    `MyClassMethod` that wraps a function, and whose `__get__` returns a
    callable that passes the **owner class** as the first argument (a lambda
    or a small inner function works). Use it on `Pizza.from_text("margherita:8")`,
    which should return a `Pizza` with a name and a price, then print its
    name and price as a number.
""",
     solution='class MyClassMethod:\n'
              '    def __init__(self, func):\n'
              '        self.func = func\n'
              '    def __get__(self, obj, owner=None):\n'
              '        return lambda *args: self.func(owner, *args)\n\n'
              'class Pizza:\n'
              '    def __init__(self, name, price):\n'
              '        self.name = name\n'
              '        self.price = price\n'
              '    @MyClassMethod\n'
              '    def from_text(cls, text):\n'
              '        name, price = text.split(":")\n'
              '        return cls(name, int(price))\n\n'
              'pizza = Pizza.from_text("margherita:8")\nprint(pizza.name, pizza.price)')

nb.q("Real-life", """
    Export formats register themselves. Write a base class `Exporter` with a
    dict `registry`; `__init_subclass__(cls, fmt, **kwargs)` stores the
    subclass under `fmt`. Create `CsvExporter` (`fmt="csv"`, `run(rows)`
    returns the rows joined by commas) and `LinesExporter` (`fmt="lines"`,
    joined by newlines). Write `export(fmt, rows)` that looks up the class,
    creates it and returns its output, then print both formats for `rows`.
""",
     given='rows = ["tea", "milk", "eggs"]',
     solution='class Exporter:\n'
              '    registry = {}\n'
              '    def __init_subclass__(cls, fmt, **kwargs):\n'
              '        super().__init_subclass__(**kwargs)\n'
              '        Exporter.registry[fmt] = cls\n\n'
              'class CsvExporter(Exporter, fmt="csv"):\n'
              '    def run(self, rows):\n'
              '        return ",".join(rows)\n\n'
              'class LinesExporter(Exporter, fmt="lines"):\n'
              '    def run(self, rows):\n'
              '        return "\\n".join(rows)\n\n'
              'def export(fmt, rows):\n'
              '    return Exporter.registry[fmt]().run(rows)\n\n'
              'print(export("csv", rows))\nprint(export("lines", rows))')

nb.q("Real-life", """
    Generate data classes from a schema, using `type()` and no `class`
    keyword. Write `make_model(name, fields)` that returns a new class whose
    `__init__` takes one positional argument per field name and stores it, and
    whose `__repr__` returns `Name(field=value, ...)` in field order. Build all
    models in `schema` and print one instance of each.
""",
     given='schema = {"Dog": ["name", "age"], "Book": ["title", "pages", "author"]}',
     solution='def make_model(name, fields):\n'
              '    def __init__(self, *values):\n'
              '        for field, value in zip(fields, values):\n'
              '            setattr(self, field, value)\n'
              '    def __repr__(self):\n'
              '        parts = [f"{f}={getattr(self, f)!r}" for f in fields]\n'
              '        return f"{name}({\', \'.join(parts)})"\n'
              '    return type(name, (), {"__init__": __init__, "__repr__": __repr__})\n\n'
              'models = {n: make_model(n, f) for n, f in schema.items()}\n'
              'print(models["Dog"]("Rex", 4))\n'
              'print(models["Book"]("Dune", 412, "Herbert"))')

# ------------------------------------------------------- Puzzles & builds
nb.q("Real-life", """
    Build reusable validated fields. A base descriptor `Field` stores values in
    the instance `__dict__` (use `__set_name__`) and calls `self.check(value)`
    before storing. `IntField(low, high)` raises `ValueError` with the message
    `<name> must be between <low> and <high>` when out of range, and
    `TextField(max_len)` raises `ValueError` with `<name> is too long` when the
    text is longer. Use them in a `Product` class (`title` TextField 10,
    `stock` IntField 0 to 100), then try three products and print either
    `ok` and the title, or the error message for each.
""",
     given='attempts = [("Tea", 20), ("Extra long title", 5), ("Milk", 500)]',
     solution='class Field:\n'
              '    def __set_name__(self, owner, name):\n'
              '        self.name = name\n'
              '    def __get__(self, obj, owner=None):\n'
              '        if obj is None:\n'
              '            return self\n'
              '        return obj.__dict__[self.name]\n'
              '    def __set__(self, obj, value):\n'
              '        self.check(value)\n'
              '        obj.__dict__[self.name] = value\n\n'
              'class IntField(Field):\n'
              '    def __init__(self, low, high):\n'
              '        self.low, self.high = low, high\n'
              '    def check(self, value):\n'
              '        if not self.low <= value <= self.high:\n'
              '            raise ValueError(f"{self.name} must be between {self.low} and {self.high}")\n\n'
              'class TextField(Field):\n'
              '    def __init__(self, max_len):\n'
              '        self.max_len = max_len\n'
              '    def check(self, value):\n'
              '        if len(value) > self.max_len:\n'
              '            raise ValueError(f"{self.name} is too long")\n\n'
              'class Product:\n'
              '    title = TextField(10)\n'
              '    stock = IntField(0, 100)\n'
              '    def __init__(self, title, stock):\n'
              '        self.title = title\n'
              '        self.stock = stock\n\n'
              'for title, stock in attempts:\n'
              '    try:\n'
              '        product = Product(title, stock)\n'
              '        print("ok", product.title)\n'
              '    except ValueError as err:\n'
              '        print(err)')

nb.q("Puzzle", """
    Write your own `cached_property` as a **non-data** descriptor: its
    `__get__` calls the function, stores the result in the instance
    `__dict__` under the same name, and returns it, so the next read never
    reaches the descriptor again. Use it on `Report.total` (sums the `sales`
    list given to the report, and counts every real computation in a class
    attribute `computed`). Read `total` three times and print the total and the
    number of computations.
""",
     solution='class cached:\n'
              '    def __init__(self, func):\n'
              '        self.func = func\n'
              '    def __set_name__(self, owner, name):\n'
              '        self.name = name\n'
              '    def __get__(self, obj, owner=None):\n'
              '        if obj is None:\n'
              '            return self\n'
              '        value = self.func(obj)\n'
              '        obj.__dict__[self.name] = value\n'
              '        return value\n\n'
              'class Report:\n'
              '    computed = 0\n'
              '    def __init__(self, sales):\n'
              '        self.sales = sales\n'
              '    @cached\n'
              '    def total(self):\n'
              '        Report.computed += 1\n'
              '        return sum(self.sales)\n\n'
              'report = Report([120, 80, 45])\n'
              'report.total\nreport.total\n'
              'print(report.total, Report.computed)')

nb.q("Real-life", """
    A game needs exactly one `Settings` object. Write a metaclass `Singleton`
    (a subclass of `type`) that keeps a dict of instances and overrides
    `__call__`, so calling the class again returns the first instance. `Settings`
    counts in a class attribute `created` how many times `__init__` really ran.
    Create it three times, then print whether all three are the same object
    and the value of `created`.
""",
     solution='class Singleton(type):\n'
              '    instances = {}\n'
              '    def __call__(cls, *args, **kwargs):\n'
              '        if cls not in Singleton.instances:\n'
              '            Singleton.instances[cls] = super().__call__(*args, **kwargs)\n'
              '        return Singleton.instances[cls]\n\n'
              'class Settings(metaclass=Singleton):\n'
              '    created = 0\n'
              '    def __init__(self):\n'
              '        Settings.created += 1\n\n'
              'a = Settings()\nb = Settings()\nc = Settings()\n'
              'print(a is b is c)\nprint(Settings.created)')

nb.q("Puzzle", """
    Customise `isinstance`. Write an abstract class `Sized2` (from `abc.ABC`)
    with a `__subclasshook__` classmethod that says any class defining
    `__len__` counts as a subclass (return `NotImplemented` otherwise). Print
    `isinstance` for `[1, 2]`, `"hi"` and `42`. Then make `Ticket`, a plain
    class with no `__len__`, count as well by using `Sized2.register(Ticket)`,
    and print `isinstance(Ticket(), Sized2)`.
""",
     solution='from abc import ABC\n\n'
              'class Sized2(ABC):\n'
              '    @classmethod\n'
              '    def __subclasshook__(cls, other):\n'
              '        if cls is Sized2 and hasattr(other, "__len__"):\n'
              '            return True\n'
              '        return NotImplemented\n\n'
              'class Ticket: pass\n\n'
              'print(isinstance([1, 2], Sized2), isinstance("hi", Sized2), isinstance(42, Sized2))\n'
              'Sized2.register(Ticket)\nprint(isinstance(Ticket(), Sized2))')

# ------------------------------------------------------------ Q20 story project
nb.project("Mini ORM", story="""
    Your team wants a tiny in-memory ORM so the shop's data classes stop
    repeating validation code. You'll build it in layers: typed field
    descriptors, a model base class that discovers its fields and registers
    itself, a generated `repr`, and simple saving and querying. Each step uses
    the classes from the step before.
""",
     given='raw_rows = [\n    {"table": "Customer", "name": "Mia", "age": 31},\n'
           '    {"table": "Customer", "name": "Leo", "age": 17},\n'
           '    {"table": "Item", "name": "Tea", "price": 4},\n]',
     steps=[
         ("Write a descriptor base class `Field(kind)` that stores the value in the "
          "instance `__dict__` under its own name (`__set_name__`) and raises `TypeError` "
          "with the message `<name> expects <kind name>` for a wrong type. Define "
          "`IntField()` and `StrField()` as subclasses that fix the kind to `int` / `str`. "
          "Test them on a small throwaway class: set a good value and print it, then set a "
          "wrong one and print the error.",
          'class Field:\n'
          '    def __init__(self, kind):\n'
          '        self.kind = kind\n'
          '    def __set_name__(self, owner, name):\n'
          '        self.name = name\n'
          '    def __get__(self, obj, owner=None):\n'
          '        if obj is None:\n'
          '            return self\n'
          '        return obj.__dict__.get(self.name)\n'
          '    def __set__(self, obj, value):\n'
          '        if not isinstance(value, self.kind):\n'
          '            raise TypeError(f"{self.name} expects {self.kind.__name__}")\n'
          '        obj.__dict__[self.name] = value\n\n'
          'class IntField(Field):\n'
          '    def __init__(self):\n'
          '        super().__init__(int)\n\n'
          'class StrField(Field):\n'
          '    def __init__(self):\n'
          '        super().__init__(str)\n\n'
          'class Demo:\n    label = StrField()\n\n'
          'demo = Demo()\ndemo.label = "ok"\nprint(demo.label)\n'
          'try:\n    demo.label = 5\nexcept TypeError as err:\n    print(err)'),
         ("Write a base class `Model`. Its `__init_subclass__` collects every `Field` in the "
          "new class into a dict `fields` (name to descriptor, in definition order) and stores "
          "the class in `Model.registry` under its class name. `__init__(self, **values)` sets "
          "each given value through the descriptors. Define `Customer` (`name` StrField, `age` "
          "IntField) and `Item` (`name` StrField, `price` IntField). Print the registry's "
          "sorted keys and the field names of `Customer`.",
          'class Model:\n'
          '    registry = {}\n'
          '    def __init_subclass__(cls, **kwargs):\n'
          '        super().__init_subclass__(**kwargs)\n'
          '        cls.fields = {n: f for n, f in vars(cls).items() if isinstance(f, Field)}\n'
          '        Model.registry[cls.__name__] = cls\n'
          '    def __init__(self, **values):\n'
          '        for key, value in values.items():\n'
          '            setattr(self, key, value)\n\n'
          'class Customer(Model):\n    name = StrField()\n    age = IntField()\n\n'
          'class Item(Model):\n    name = StrField()\n    price = IntField()\n\n'
          'print(sorted(Model.registry))\nprint(list(Customer.fields))'),
         ("Attach a generated `__repr__` to `Model` (write a function and assign it): it "
          "should return `ClassName(field=value, ...)` using the class's `fields`, in order, "
          "with `!r` on the values. Then build every row of `raw_rows` with the registry "
          "(look the class up by the row's `\"table\"` key, pass the other keys as values) and "
          "print each object.",
          'def model_repr(self):\n'
          '    parts = [f"{n}={getattr(self, n)!r}" for n in self.fields]\n'
          '    return f"{type(self).__name__}({\', \'.join(parts)})"\n\n'
          'Model.__repr__ = model_repr\n'
          'objects = []\n'
          'for row in raw_rows:\n'
          '    values = {k: v for k, v in row.items() if k != "table"}\n'
          '    objects.append(Model.registry[row["table"]](**values))\n'
          'for obj in objects:\n    print(obj)'),
         ("Add storage by attaching to `Model`: a dict `tables` mapping a class name to a list "
          "of saved objects, a method `save(self)` that appends the object to its class's list, "
          "and a classmethod `where(cls, **conditions)` returning the saved objects whose "
          "attributes all match the conditions (no conditions means all). Save every object, "
          "then print the names of customers with `age` 31 and the number of saved items.",
          'Model.tables = {}\n\n'
          'def save(self):\n'
          '    Model.tables.setdefault(type(self).__name__, []).append(self)\n\n'
          'def where(cls, **conditions):\n'
          '    found = []\n'
          '    for obj in Model.tables.get(cls.__name__, []):\n'
          '        if all(getattr(obj, k) == v for k, v in conditions.items()):\n'
          '            found.append(obj)\n'
          '    return found\n\n'
          'Model.save = save\nModel.where = classmethod(where)\n'
          'for obj in objects:\n    obj.save()\n'
          'print([c.name for c in Customer.where(age=31)])\n'
          'print(len(Item.where()))'),
         ("Final check: try to create `Customer(name=\"Zed\", age=\"old\")` and print the "
          "error message; then print the saved customers who are 18 or older, using "
          "`Customer.where()` and a list comprehension.",
          'try:\n    Customer(name="Zed", age="old")\nexcept TypeError as err:\n    print(err)\n'
          'adults = [c for c in Customer.where() if c.age >= 18]\nprint(adults)'),
     ])

nb.build()
