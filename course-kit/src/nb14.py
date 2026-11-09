import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB14", title="OOP Basics", intro="""
    Bundling data and behaviour into your own types: classes, `__init__` and
    `self`, instance and class attributes, `__str__` / `__repr__`,
    inheritance with `super()`, polymorphism, composition, name privacy and
    introspection. Every question asks you to **write classes and use them**.
    Values that would come from `input()` are given to you as variables.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", "Write a class `Dog` whose `__init__` stores a `name`, and a method `bark()` that returns the name followed by ` says woof`. Create a dog called `\"Rex\"` and print `bark()`.",
     solution='class Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def bark(self):\n        return self.name + " says woof"\n\n'
              'rex = Dog("Rex")\nprint(rex.bark())')

nb.q("Real-life", "Write a class `Rectangle` with `width` and `height` attributes and an `area()` method. Print the area of a 6 by 4 rectangle.",
     solution="class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n"
              "    def area(self):\n        return self.width * self.height\n\nprint(Rectangle(6, 4).area())")

nb.q("Output-match", "Write a class `Student` with a `name` and a `grade`, and a `__str__` method that makes `print(student)` show the name, a colon, a space and the grade. Print one student.",
     solution='class Student:\n    def __init__(self, name, grade):\n        self.name = name\n        self.grade = grade\n\n'
              '    def __str__(self):\n        return f"{self.name}: {self.grade}"\n\nprint(Student("Mia", 91))')

nb.q("Puzzle", "Write a class `Counter` that starts at 0 and has a method `click()` that adds 1 and returns nothing. Click a counter five times and print its `count` attribute.",
     solution="class Counter:\n    def __init__(self):\n        self.count = 0\n\n    def click(self):\n        self.count += 1\n\n"
              "c = Counter()\nfor _ in range(5):\n    c.click()\nprint(c.count)")

nb.q("Build", "Write a class `Circle` with a class attribute `PI = 3.14159` and a `radius`, plus a method `circumference()`. Print the circumference of a circle with radius 10.",
     solution="class Circle:\n    PI = 3.14159\n\n    def __init__(self, radius):\n        self.radius = radius\n\n"
              "    def circumference(self):\n        return 2 * self.PI * self.radius\n\nprint(Circle(10).circumference())")

# ------------------------------------------------------------ Combine
nb.q("Real-life", "Write a class `BankAccount` with an `owner`, a starting `balance` of 0, and methods `deposit(amount)` and `withdraw(amount)`. A withdrawal larger than the balance must be ignored. Make the deposits and withdrawals in the given list and print the final balance.",
     given="moves = [(\"deposit\", 100), (\"withdraw\", 30), (\"withdraw\", 500), (\"deposit\", 20)]",
     solution="class BankAccount:\n    def __init__(self, owner):\n        self.owner = owner\n        self.balance = 0\n\n"
              "    def deposit(self, amount):\n        self.balance += amount\n\n"
              "    def withdraw(self, amount):\n        if amount <= self.balance:\n            self.balance -= amount\n\n"
              'account = BankAccount("Ana")\n'
              "for action, amount in moves:\n"
              '    if action == "deposit":\n        account.deposit(amount)\n    else:\n        account.withdraw(amount)\n'
              "print(account.balance)")

nb.q("Output-match", "Write a class `Point` with `x` and `y`, a `__repr__` that looks like the call that creates it (e.g. `Point(2, 3)`), and a method `move(dx, dy)` that shifts the point in place. Create a point, move it, and print it, then print a list holding that point.",
     solution='class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n'
              '    def __repr__(self):\n        return f"Point({self.x}, {self.y})"\n\n'
              "    def move(self, dx, dy):\n        self.x += dx\n        self.y += dy\n\n"
              "p = Point(2, 3)\np.move(1, -5)\nprint(p)\nprint([p])")

nb.q("Puzzle", """
    Every `Ticket` should get the next number automatically (1, 2, 3, ...).
    Use a class attribute to count the tickets created. Create three tickets
    and print each one's `number`.
""",
     solution="class Ticket:\n    created = 0\n\n    def __init__(self):\n        Ticket.created += 1\n        self.number = Ticket.created\n\n"
              "tickets = [Ticket(), Ticket(), Ticket()]\nfor t in tickets:\n    print(t.number)")

nb.q("Real-life", "Write a class `Product` with a `name` and a `price` and a method `discount(percent)` that returns the price after the discount, rounded to 2 decimals (without changing the stored price). For each product in the list, print its name and its price with a 15 percent discount.",
     given='items = [("lamp", 40.0), ("desk", 129.99), ("mug", 7.5)]',
     solution="class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n"
              "    def discount(self, percent):\n        return round(self.price * (1 - percent / 100), 2)\n\n"
              "for name, price in items:\n    product = Product(name, price)\n    print(product.name, product.discount(15))")

nb.q("Puzzle", """
    A `Light` has an attribute `on` that starts as `False`. Give it a
    `toggle()` method that flips it, and an `__str__` that returns `ON` or
    `OFF`. Toggle it three times, printing the light after each toggle.
""",
     solution='class Light:\n    def __init__(self):\n        self.on = False\n\n    def toggle(self):\n        self.on = not self.on\n\n'
              '    def __str__(self):\n        return "ON" if self.on else "OFF"\n\n'
              "lamp = Light()\nfor _ in range(3):\n    lamp.toggle()\n    print(lamp)")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Write a `Pet` class with a `name` and a `tricks` list that starts empty
    for **each** pet, and an `add_trick(trick)` method. Teach `"sit"` to one
    pet and `"roll"` to another, then print each pet's tricks.
""",
     solution="class Pet:\n    def __init__(self, name):\n        self.name = name\n        self.tricks = []\n\n"
              "    def add_trick(self, trick):\n        self.tricks.append(trick)\n\n"
              'a = Pet("Fido")\nb = Pet("Tom")\na.add_trick("sit")\nb.add_trick("roll")\n'
              "print(a.tricks)\nprint(b.tricks)")

nb.q("Real-life", """
    A school has `Person` (name, age, a `describe()` method returning the
    name and age) and `Teacher`, which also has a `subject`. `Teacher` must
    inherit from `Person`, call `super().__init__`, and override `describe()`
    to add the subject (use the parent's `describe()` inside it). Print the
    description of one person and one teacher.
""",
     solution='class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n'
              '    def describe(self):\n        return f"{self.name}, {self.age}"\n\n'
              "class Teacher(Person):\n    def __init__(self, name, age, subject):\n        super().__init__(name, age)\n        self.subject = subject\n\n"
              '    def describe(self):\n        return super().describe() + f", teaches {self.subject}"\n\n'
              'print(Person("Leo", 15).describe())\nprint(Teacher("Ms Park", 41, "math").describe())')

nb.q("Real-life", """
    A zoo has an `Animal` base class (with a `name`) whose `speak()` returns
    an empty string, plus `Cat`, `Cow` and `Duck` subclasses that override
    `speak()` to return `meow`, `moo` and `quack`. Loop over the list of
    animals and print each name with its sound.
""",
     given='names = [("Tom", "cat"), ("Daisy", "cow"), ("Don", "duck")]',
     solution='class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return ""\n\n'
              'class Cat(Animal):\n    def speak(self):\n        return "meow"\n\n'
              'class Cow(Animal):\n    def speak(self):\n        return "moo"\n\n'
              'class Duck(Animal):\n    def speak(self):\n        return "quack"\n\n'
              'kinds = {"cat": Cat, "cow": Cow, "duck": Duck}\n'
              "for name, kind in names:\n    animal = kinds[kind](name)\n    print(animal.name, animal.speak())")

nb.q("Build", """
    Write `Shape` classes `Circle(radius)` and `Square(side)`, each with an
    `area()` method rounded to 2 decimals (use 3.14159 for pi). Loop over a
    mixed list of shapes and print each shape's class name and area.
    Then print the shape count for each kind using `isinstance`.
""",
     solution="class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    def area(self):\n        return round(3.14159 * self.radius ** 2, 2)\n\n"
              "class Square:\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return round(self.side ** 2, 2)\n\n"
              "shapes = [Circle(1), Square(3), Circle(2.5), Square(1.5)]\n"
              "for s in shapes:\n    print(s.__class__.__name__, s.area())\n"
              "circles = 0\nsquares = 0\n"
              "for s in shapes:\n    if isinstance(s, Circle):\n        circles += 1\n    if isinstance(s, Square):\n        squares += 1\n"
              "print(circles, squares)")

nb.q("Real-life", """
    A secret-keeper: write a class `Safe` that stores a `_code` and a
    `__gold` amount. Its method `open(code)` returns the gold when the code
    matches and `0` otherwise. Print what a right and a wrong guess return,
    then print `hasattr(safe, "__gold")` and `hasattr(safe, "_Safe__gold")`.
""",
     solution="class Safe:\n    def __init__(self, code, gold):\n        self._code = code\n        self.__gold = gold\n\n"
              "    def open(self, code):\n        if code == self._code:\n            return self.__gold\n        return 0\n\n"
              "safe = Safe(1234, 500)\nprint(safe.open(1234))\nprint(safe.open(1))\n"
              'print(hasattr(safe, "__gold"))\nprint(hasattr(safe, "_Safe__gold"))')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    A `Vehicle` has `wheels = 4` as a class attribute and `Bike` is a
    subclass that sets its own `wheels = 2`. Create a car (a `Vehicle`), a
    bike, and then set `wheels = 3` on the car **instance** only. Print the
    wheels of the car, the bike, and of `Vehicle` itself.
""",
     solution="class Vehicle:\n    wheels = 4\n\nclass Bike(Vehicle):\n    wheels = 2\n\n"
              "car = Vehicle()\nbike = Bike()\ncar.wheels = 3\nprint(car.wheels, bike.wheels, Vehicle.wheels)")

nb.q("Real-life", """
    Build a small library with **composition**. A `Book` has a `title` and
    an `available` flag (starts `True`). A `Library` holds a list of books
    with `add(book)`, `lend(title)` (returns `True` and marks the book not
    available if it exists and is available, otherwise `False`) and
    `available_titles()` returning the titles that can still be borrowed.
    Add three books, lend two titles (one of them twice), and print each
    lend result, then the available titles.
""",
     solution="class Book:\n    def __init__(self, title):\n        self.title = title\n        self.available = True\n\n"
              "class Library:\n    def __init__(self):\n        self.books = []\n\n"
              "    def add(self, book):\n        self.books.append(book)\n\n"
              "    def lend(self, title):\n        for book in self.books:\n            if book.title == title and book.available:\n                book.available = False\n                return True\n        return False\n\n"
              "    def available_titles(self):\n        return [b.title for b in self.books if b.available]\n\n"
              "lib = Library()\nfor t in [\"Dune\", \"Emma\", \"Ulysses\"]:\n    lib.add(Book(t))\n"
              'print(lib.lend("Dune"))\nprint(lib.lend("Dune"))\nprint(lib.lend("Emma"))\n'
              "print(lib.available_titles())")

nb.q("Puzzle", """
    Write `Stack` with `push(item)`, `pop()` and `peek()`, and `is_empty()`,
    storing the items in a list. `pop()` and `peek()` on an empty stack must
    raise `IndexError("stack is empty")`. Push the given words, print what
    `pop()` returns, print what `peek()` returns, then pop until it is empty;
    finally pop once more inside `try` / `except` and print the error message.
""",
     given='words = ["a", "b", "c"]',
     solution="class Stack:\n    def __init__(self):\n        self.items = []\n\n"
              "    def push(self, item):\n        self.items.append(item)\n\n"
              '    def pop(self):\n        if not self.items:\n            raise IndexError("stack is empty")\n        return self.items.pop()\n\n'
              '    def peek(self):\n        if not self.items:\n            raise IndexError("stack is empty")\n        return self.items[-1]\n\n'
              "    def is_empty(self):\n        return not self.items\n\n"
              "s = Stack()\nfor w in words:\n    s.push(w)\n"
              "print(s.pop())\nprint(s.peek())\n"
              "while not s.is_empty():\n    s.pop()\n"
              "try:\n    s.pop()\nexcept IndexError as e:\n    print(e)")

nb.q("Puzzle", """
    Introspection: write a class `Config` whose `__init__` takes a dict and
    sets each key as an attribute (use `setattr`). Build one from the given
    settings, print its `__dict__`, then use `getattr` with a default of
    `\"n/a\"` to print the `theme` and the `language` values.
""",
     given='settings = {"theme": "dark", "volume": 7}',
     solution="class Config:\n    def __init__(self, values):\n        for key in values:\n            setattr(self, key, values[key])\n\n"
              "cfg = Config(settings)\nprint(cfg.__dict__)\n"
              'print(getattr(cfg, "theme", "n/a"))\nprint(getattr(cfg, "language", "n/a"))')

# ------------------------------------------------------------ Q20 project
nb.project("Parking Lot", story="""
    You're writing the software for a small car park with a few spots of
    different sizes. Each step adds one class on top of the previous ones;
    the last step runs a day of traffic and prints a status report.
""",
     given='arrivals = [("car", "AB-12"), ("bike", "ZX-99"), ("car", "CD-34"), ("car", "EF-56"), ("bike", "GH-78")]',
     steps=[
         ("Write a `Vehicle` base class with a `plate` and a class attribute `size = 2`, and subclasses `Car` (size 2) and `Bike` (size 1). Give `Vehicle` a `__str__` that returns the class name and the plate, like the expected output. Print one car and one bike.",
          'class Vehicle:\n    size = 2\n\n    def __init__(self, plate):\n        self.plate = plate\n\n'
          '    def __str__(self):\n        return f"{self.__class__.__name__} {self.plate}"\n\n'
          "class Car(Vehicle):\n    size = 2\n\nclass Bike(Vehicle):\n    size = 1\n\n"
          'print(Car("AB-12"))\nprint(Bike("ZX-99"))'),
         ("Write a `Spot` class with a `number`, a `capacity` (the size it can hold) and a `vehicle` that starts as `None`. Add `can_fit(vehicle)` (spot is empty and the vehicle's size is at most the capacity). Create a spot with capacity 1 and print whether it can fit the car and the bike.",
          "class Spot:\n    def __init__(self, number, capacity):\n        self.number = number\n        self.capacity = capacity\n        self.vehicle = None\n\n"
          "    def can_fit(self, vehicle):\n        return self.vehicle is None and vehicle.size <= self.capacity\n\n"
          'small = Spot(1, 1)\nprint(small.can_fit(Car("AB-12")))\nprint(small.can_fit(Bike("ZX-99")))'),
         ("Write a `ParkingLot` that **has** a list of spots (composition). Its `__init__` takes a list of capacities and numbers the spots from 1. Add `park(vehicle)`, which puts the vehicle in the first spot that fits and returns that spot's number, or `None` if nothing fits. Build a lot with capacities `[1, 2, 2]` and park the first three arrivals, printing the spot numbers.",
          "class ParkingLot:\n    def __init__(self, capacities):\n        self.spots = []\n        for i, cap in enumerate(capacities, start=1):\n            self.spots.append(Spot(i, cap))\n\n"
          "    def park(self, vehicle):\n        for spot in self.spots:\n            if spot.can_fit(vehicle):\n                spot.vehicle = vehicle\n                return spot.number\n        return None\n\n"
          'kinds = {"car": Car, "bike": Bike}\nlot = ParkingLot([1, 2, 2])\n'
          "for kind, plate in arrivals[:3]:\n    print(lot.park(kinds[kind](plate)))"),
         ("Add a `leave(plate)` method to `ParkingLot` (redefine the whole class with it). It empties the spot holding that plate and returns `True`, or returns `False` if no such vehicle is parked. In a new lot with capacities `[1, 2, 2]` park all the arrivals, print what each `park` returned, then make `\"AB-12\"` and `\"QQ-00\"` leave and print both results.",
          "class ParkingLot:\n    def __init__(self, capacities):\n        self.spots = []\n        for i, cap in enumerate(capacities, start=1):\n            self.spots.append(Spot(i, cap))\n\n"
          "    def park(self, vehicle):\n        for spot in self.spots:\n            if spot.can_fit(vehicle):\n                spot.vehicle = vehicle\n                return spot.number\n        return None\n\n"
          "    def leave(self, plate):\n        for spot in self.spots:\n            if spot.vehicle is not None and spot.vehicle.plate == plate:\n                spot.vehicle = None\n                return True\n        return False\n\n"
          "lot = ParkingLot([1, 2, 2])\n"
          "for kind, plate in arrivals:\n    print(lot.park(kinds[kind](plate)))\n"
          'print(lot.leave("AB-12"))\nprint(lot.leave("QQ-00"))'),
         ("Add a `report()` method that **prints** one line per spot, in the form `Spot 1 (cap 1): Bike ZX-99` or `Spot 2 (cap 2): free`, then a last line `Free spots: N`. Redefine `ParkingLot` once more with `report()` added, run the same day as before (all arrivals, then `\"AB-12\"` leaves) in a fresh lot and call `report()`.",
          "class ParkingLot:\n    def __init__(self, capacities):\n        self.spots = []\n        for i, cap in enumerate(capacities, start=1):\n            self.spots.append(Spot(i, cap))\n\n"
          "    def park(self, vehicle):\n        for spot in self.spots:\n            if spot.can_fit(vehicle):\n                spot.vehicle = vehicle\n                return spot.number\n        return None\n\n"
          "    def leave(self, plate):\n        for spot in self.spots:\n            if spot.vehicle is not None and spot.vehicle.plate == plate:\n                spot.vehicle = None\n                return True\n        return False\n\n"
          "    def report(self):\n        free = 0\n        for spot in self.spots:\n"
          "            if spot.vehicle is None:\n                free += 1\n                state = \"free\"\n            else:\n                state = str(spot.vehicle)\n"
          '            print(f"Spot {spot.number} (cap {spot.capacity}): {state}")\n'
          '        print("Free spots:", free)\n\n'
          "lot = ParkingLot([1, 2, 2])\n"
          "for kind, plate in arrivals:\n    lot.park(kinds[kind](plate))\n"
          'lot.leave("AB-12")\nlot.report()'),
     ])

nb.build()
