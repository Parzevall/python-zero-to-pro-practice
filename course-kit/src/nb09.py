import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB09", title="Functions Advanced", intro="""
    Functions as flexible tools and as values: `*args` and `**kwargs`,
    keyword-only and positional-only parameters, `lambda`, dispatch tables,
    closures with `nonlocal`, and `functools.partial`. Every question asks
    you to write the functions and call them.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", "Write `total(*nums)` that returns the sum of any number of arguments. Print `total(4, 8, 15)` and `total()`.",
     solution="def total(*nums):\n    return sum(nums)\nprint(total(4, 8, 15))\nprint(total())")

nb.q("Real-life", "Write `build_profile(name, **details)` that returns a dict holding the name under `\"name\"` plus every extra keyword. Print the profile for Ada, who is 36 and lives in London.",
     solution='def build_profile(name, **details):\n    profile = {"name": name}\n    profile.update(details)\n    return profile\n'
              'print(build_profile("Ada", age=36, city="London"))')

nb.q("Output-match", "The function below is given. Call it with the list unpacked by `*` and the dict unpacked by `**` so it prints the three values on one line.",
     given='def show(a, b, c):\n    print(a, b, c)\n\nfirst_two = [1, 2]\nrest = {"c": 3}',
     solution="show(*first_two, **rest)")

nb.q("Puzzle", "Write `square(n)` as a one-line `lambda` stored in `square`. Print `square(9)` and the name `square.__name__`.",
     solution="square = lambda n: n * n\nprint(square(9))\nprint(square.__name__)")

nb.q("Build", "Write `power(base, exp)` with a one-line docstring, then print its `__name__` and its `__doc__`.",
     solution='def power(base, exp):\n    """Return base to the power exp."""\n    return base ** exp\nprint(power.__name__)\nprint(power.__doc__)')

# ------------------------------------------------------------ Combine
nb.q("Real-life", "Write `average(*scores)` that returns the mean of all the scores it receives. Call it with the unpacked list `marks` and print the result.",
     given="marks = [70, 85, 90, 55]",
     solution="def average(*scores):\n    return sum(scores) / len(scores)\nprint(average(*marks))")

nb.q("Real-life", """
    Write `describe(item, *, currency="EUR")` where `currency` can only be
    passed by keyword. It returns the item's name and price formatted with 2
    decimals and the currency, like the expected output. Print one call with
    the default and one with `currency="USD"`.
""",
     given='book = ("Dune", 12.5)',
     solution='def describe(item, *, currency="EUR"):\n    name, price = item\n    return f"{name}: {price:.2f} {currency}"\n'
              'print(describe(book))\nprint(describe(book, currency="USD"))')

nb.q("Puzzle", """
    Write `halve(n, /)` where `n` is positional-only. Print `halve(10)`. Then call
    `halve(n=10)` inside a `try` block and, when it fails with
    `TypeError`, print `keyword not allowed`.
""",
     solution='def halve(n, /):\n    return n / 2\n'
              "print(halve(10))\ntry:\n    halve(n=10)\nexcept TypeError:\n    print(\"keyword not allowed\")")

nb.q("Real-life", """
    A text-adventure parser stores commands as functions. Build the dict
    `commands` mapping `"north"`, `"south"` and `"look"` to functions that
    return a sentence. Then run each typed word from `typed` through it,
    printing `"Unknown command"` for words that aren't in the dict.
""",
     given='typed = ["look", "north", "dance", "south"]',
     solution='def north():\n    return "You walk north."\n'
              'def south():\n    return "You walk south."\n'
              'def look():\n    return "You see a dusty room."\n'
              'commands = {"north": north, "south": south, "look": look}\n'
              "for word in typed:\n    if word in commands:\n        print(commands[word]())\n    else:\n        print(\"Unknown command\")")

nb.q("Build", """
    Write `make_multiplier(factor)` that returns a new function multiplying
    its argument by `factor`. Create `double` and `triple` with it and print
    `double(7)` and `triple(7)`.
""",
     solution="def make_multiplier(factor):\n    def multiply(x):\n        return x * factor\n    return multiply\n"
              "double = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(7))\nprint(triple(7))")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Write `make_counter()` that returns a function; every call to that
    function returns the next number starting from 1 (use `nonlocal`).
    Make two counters and call the first one three times and the second
    once, printing every result.
""",
     solution="def make_counter():\n    count = 0\n    def next_number():\n        nonlocal count\n        count += 1\n        return count\n    return next_number\n"
              "first = make_counter()\nsecond = make_counter()\n"
              "print(first())\nprint(first())\nprint(first())\nprint(second())")

nb.q("Puzzle", """
    Fill a list with three functions in a loop over `range(3)`, each
    returning the loop number it was made with (not the final one). Pass the
    number as a default argument `lambda n=i: n`. Call all three and print
    the results as a list.
""",
     solution="funcs = []\nfor i in range(3):\n    funcs.append(lambda n=i: n)\n"
              "results = []\nfor f in funcs:\n    results.append(f())\nprint(results)")

nb.q("Real-life", """
    Write `calculate(a, op, b)` that looks the operator up in a dispatch
    table (a dict from `"+"`, `"-"`, `"*"`, `"/"` to two-argument lambdas)
    instead of an `if` chain, and returns the result. Print the answer for
    each sum.
""",
     given='sums = [(8, "+", 2), (8, "-", 2), (8, "*", 2), (8, "/", 2)]',
     solution='table = {\n    "+": lambda a, b: a + b,\n    "-": lambda a, b: a - b,\n    "*": lambda a, b: a * b,\n    "/": lambda a, b: a / b,\n}\n'
              "def calculate(a, op, b):\n    return table[op](a, b)\n"
              "for a, op, b in sums:\n    print(a, op, b, \"=\", calculate(a, op, b))")

nb.q("Real-life", """
    Use `functools.partial` to make `to_binary` from `int`, so that calling
    `to_binary(text)` converts a binary string to a number (`base=2`). Print
    the conversion for each string.
""",
     given='bits = ["101", "1111", "10000000"]',
     solution="from functools import partial\nto_binary = partial(int, base=2)\nfor b in bits:\n    print(b, to_binary(b))")

nb.q("Real-life", """
    A report function takes a helper as an argument. Write
    `apply_all(func, values)` that returns a list of `func(v)` for every
    value, built with a loop. Use it twice: once with the built-in `len`
    on `words` and once with a lambda that shouts a word (upper case plus
    `!`). Print both lists.
""",
     given='words = ["tea", "coffee", "milk"]',
     solution="def apply_all(func, values):\n    out = []\n    for v in values:\n        out.append(func(v))\n    return out\n"
              "print(apply_all(len, words))\nprint(apply_all(lambda w: w.upper() + \"!\", words))")

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Write `memoize(func)` that returns a wrapper function with a cache dict
    kept in a closure: the first call for an argument runs `func`, later
    calls reuse the stored answer. Memoize `slow_square` (given, it counts
    its own calls in `calls`), call the memoized version for 4, 4, 5, 4, and
    print the results and then how many times the real function ran.
""",
     given="calls = 0\ndef slow_square(n):\n    global calls\n    calls += 1\n    return n * n",
     solution="def memoize(func):\n    cache = {}\n    def wrapper(n):\n        if n not in cache:\n            cache[n] = func(n)\n        return cache[n]\n    return wrapper\n"
              "fast = memoize(slow_square)\nresults = []\nfor n in [4, 4, 5, 4]:\n    results.append(fast(n))\nprint(results)\nprint(calls)")

nb.q("Puzzle", """
    Write `compose(*funcs)` that returns one function applying the given
    functions from right to left (`compose(f, g)(x)` is `f(g(x))`). Build
    `clean` from `str.title`, `str.strip` and a lambda replacing `_` with a
    space, in the order strip, replace, title; print the cleaned strings.
""",
     given='raw = ["  ada_lovelace ", "grace_hopper  "]',
     solution="def compose(*funcs):\n    def run(x):\n        for f in reversed(funcs):\n            x = f(x)\n        return x\n    return run\n"
              'clean = compose(str.title, lambda s: s.replace("_", " "), str.strip)\n'
              "for name in raw:\n    print(clean(name))")

nb.q("Real-life", """
    Write `make_logger(prefix)` returning a function `log(*messages, sep=" ")`
    that returns the prefix in square brackets followed by the messages
    joined by `sep`. Make `info = make_logger("INFO")` and `error =
    make_logger("ERROR")`, and print one call to each (with several
    messages, and one with a different `sep`).
""",
     solution='def make_logger(prefix):\n    def log(*messages, sep=" "):\n        return "[" + prefix + "] " + sep.join(messages)\n    return log\n'
              'info = make_logger("INFO")\nerror = make_logger("ERROR")\n'
              'print(info("server", "started"))\nprint(error("disk", "full", sep="-"))')

nb.q("Puzzle", """
    Write `once(func)` that returns a wrapper which runs `func` only on its
    first call (passing along any arguments) and afterwards always returns
    that first result, whatever arguments it gets. Wrap `connect(host)` and
    call it with `"a.com"`, `"b.com"` and `"c.com"`, printing each result.
""",
     given='def connect(host):\n    return "connected to " + host',
     solution="def once(func):\n    done = False\n    result = None\n    def wrapper(*args, **kwargs):\n        nonlocal done, result\n        if not done:\n            result = func(*args, **kwargs)\n            done = True\n        return result\n    return wrapper\n"
              "connect_once = once(connect)\nfor host in [\"a.com\", \"b.com\", \"c.com\"]:\n    print(connect_once(host))")

# ------------------------------------------------------------ Q20 project
nb.project("Event System", story="""
    You're writing the notification core of a small game. Parts of the game
    register **handlers** for named events (`"level_up"`, `"item_found"`);
    when the game **emits** an event, every handler for it runs. Build it
    from closures and dicts, one step at a time.
""",
     given="log = []",
     steps=[
         ("Write `make_bus()` that returns a dict with three functions under the keys `\"on\"`, `\"emit\"` and `\"off\"`, sharing one `handlers` dict (event name to list of handler functions). Step one: only `on(event, handler)` does anything, adding the handler. Create `bus = make_bus()` and register a handler `log_it(*args, **kwargs)` (it appends `(args, kwargs)` to `log`) for `\"level_up\"`. Print how many keys `bus` has.",
          "def make_bus():\n    handlers = {}\n    def on(event, handler):\n        handlers.setdefault(event, []).append(handler)\n    def emit(event, *args, **kwargs):\n        pass\n    def off(event, handler):\n        pass\n    return {\"on\": on, \"emit\": emit, \"off\": off}\n"
          "def log_it(*args, **kwargs):\n    log.append((args, kwargs))\n"
          "bus = make_bus()\nbus[\"on\"](\"level_up\", log_it)\nprint(len(bus))"),
         ("Redefine `make_bus()` so `emit(event, *args, **kwargs)` calls every handler registered for the event, passing the arguments through (unknown events do nothing), and `off` still does nothing. Make a new bus, register `log_it` for `\"level_up\"`, emit `\"level_up\"` with `5, hero=\"Ada\"` and emit `\"nothing_here\"`. Print `log`.",
          "def make_bus():\n    handlers = {}\n    def on(event, handler):\n        handlers.setdefault(event, []).append(handler)\n    def emit(event, *args, **kwargs):\n        for handler in handlers.get(event, []):\n            handler(*args, **kwargs)\n    def off(event, handler):\n        pass\n    return {\"on\": on, \"emit\": emit, \"off\": off}\n"
          "log.clear()\nbus = make_bus()\nbus[\"on\"](\"level_up\", log_it)\nbus[\"emit\"](\"level_up\", 5, hero=\"Ada\")\nbus[\"emit\"](\"nothing_here\")\nprint(log)"),
         ("Redefine `make_bus()` once more, now with a working `off(event, handler)` that removes the handler if it is registered (and does nothing otherwise). Make a new bus, register `log_it` and a second handler `shout(item)` that you write (it prints the item in upper case) for `\"item_found\"`, emit `\"item_found\"` with `\"sword\"`, remove `shout`, emit again with `\"shield\"`. Print `log`.",
          "def make_bus():\n    handlers = {}\n    def on(event, handler):\n        handlers.setdefault(event, []).append(handler)\n    def emit(event, *args, **kwargs):\n        for handler in handlers.get(event, []):\n            handler(*args, **kwargs)\n    def off(event, handler):\n        if handler in handlers.get(event, []):\n            handlers[event].remove(handler)\n    return {\"on\": on, \"emit\": emit, \"off\": off}\n"
          "def shout(item):\n    print(item.upper())\n"
          "log.clear()\nbus = make_bus()\nbus[\"on\"](\"item_found\", log_it)\nbus[\"on\"](\"item_found\", shout)\nbus[\"emit\"](\"item_found\", \"sword\")\nbus[\"off\"](\"item_found\", shout)\nbus[\"emit\"](\"item_found\", \"shield\")\nprint(log)"),
         ("Use `functools.partial` to make `announce = partial(bus[\"emit\"], \"level_up\")`. Register a lambda handler on `\"level_up\"` that appends `\"Level \" + str(level)` to a list `messages` (it takes one `level` argument), then call `announce(2)` and `announce(3)`. Print `messages`.",
          "from functools import partial\nmessages = []\nannounce = partial(bus[\"emit\"], \"level_up\")\nbus[\"on\"](\"level_up\", lambda level: messages.append(\"Level \" + str(level)))\nannounce(2)\nannounce(3)\nprint(messages)"),
         ("Write `counting(handler)` that wraps any handler and returns a function that calls it and keeps the number of calls with `nonlocal`; return the pair `(wrapper, get_count)`, where `get_count()` returns the number of calls so far. Register a wrapped copy of `log_it` for `\"tick\"` on a new bus, emit `\"tick\"` four times, and print the count.",
          "def counting(handler):\n    count = 0\n    def wrapper(*args, **kwargs):\n        nonlocal count\n        count += 1\n        return handler(*args, **kwargs)\n    def get_count():\n        return count\n    return wrapper, get_count\n"
          "bus = make_bus()\ntick_handler, tick_count = counting(log_it)\nbus[\"on\"](\"tick\", tick_handler)\nfor _ in range(4):\n    bus[\"emit\"](\"tick\")\nprint(tick_count())"),
     ])

nb.build()
