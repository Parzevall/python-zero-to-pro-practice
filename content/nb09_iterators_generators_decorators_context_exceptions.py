"""Notebook 09 - Iterators, Generators, Decorators, Context Managers &
Exceptions (Q-315..Q-358)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-315",
    level=Level.L1,
    topic="Iterators",
    kind="function",
    entry="first_two",
    prompt=(
        "Write `first_two(values)` that returns the **tuple** of the first two items "
        "of any iterable.\n\n"
        "Drive it by hand: get an iterator with `iter(values)` and pull from it with "
        "`next()` twice. No indexing, no slicing — the argument may be something that "
        "has no positions at all.\n\n"
        "If there are fewer than two items, let `next` do what it already does."
    ),
    hint=(
        "`iter` turns a container into a one-shot cursor; `next` advances that cursor "
        "and hands you the item it passed. Call `iter` once and keep the result — a "
        "second `iter(values)` on a list would start over from the beginning."
    ),
    solution=(
        "def first_two(values):\n"
        "    it = iter(values)\n"
        "    return (next(it), next(it))"
    ),
    explanation=(
        "`for` is sugar for exactly this: call `iter`, call `next` until "
        "`StopIteration`. Holding the iterator in a variable is what makes the two "
        "`next` calls consecutive rather than both returning the first item, and it "
        "is the whole reason a generator can be consumed a piece at a time."
    ),
    starter="def first_two(values):\n    ...",
    cases=[
        Case(expected=(1, 2), args=([1, 2, 3],)),
        Case(expected=("a", "b"), args=("ab",)),
        Case(expected=(10, 20), args=((10, 20),)),
        Case(expected=None, args=([1],), raises=StopIteration),
    ],
)

q(
    qid="Q-316",
    level=Level.L1,
    topic="Exceptions",
    kind="function",
    entry="safe_div",
    prompt=(
        "Write `safe_div(a, b)` that returns `a / b`, or returns `None` when `b` is "
        "zero.\n\n"
        "Catch the division by zero with `try`/`except` naming the exception "
        "explicitly — do not test `b` with an `if`, and do not write a bare `except:`."
    ),
    hint=(
        "Dividing by zero raises one specific exception whose name says exactly what "
        "happened. Name that class in the `except` clause; anything wider catches bugs "
        "you wanted to hear about."
    ),
    solution=(
        "def safe_div(a, b):\n"
        "    try:\n"
        "        return a / b\n"
        "    except ZeroDivisionError:\n"
        "        return None"
    ),
    explanation=(
        "Python's culture is *ask forgiveness, not permission*: attempt the operation "
        "and handle the failure, rather than pre-checking every condition that could "
        "go wrong. The `if b == 0` version looks equivalent but drifts out of sync "
        "with reality the moment `b` is a type whose division fails for some other "
        "reason."
    ),
    starter="def safe_div(a, b):\n    ...",
    cases=[
        Case(expected=2.0, args=(6, 3)),
        Case(expected=None, args=(1, 0)),
        Case(expected=-3.5, args=(-7, 2)),
        Case(expected=0.0, args=(0, 5)),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-317",
    level=Level.L2,
    topic="Generators",
    kind="function",
    entry="squares",
    prompt=(
        "Write two things:\n\n"
        "1. `gen_squares(n)` — a **generator function** that `yield`s `0*0`, `1*1`, "
        "... up to but not including `n*n`.\n"
        "2. `squares(n)` — returns `list(gen_squares(n))`, a plain **list of ints**.\n\n"
        "`squares(4)` returns `[0, 1, 4, 9]`. The checker is strict on type, so a "
        "generator object will never pass where a list is expected — that wrapper is "
        "not decoration, it is the whole convention this notebook uses."
    ),
    hint=(
        "A function becomes a generator the moment its body contains `yield` — no "
        "special declaration, no `return` of anything. Loop over `range(n)` and yield "
        "once per step."
    ),
    solution=(
        "def gen_squares(n):\n"
        "    for i in range(n):\n"
        "        yield i * i\n\n\n"
        "def squares(n):\n"
        "    return list(gen_squares(n))"
    ),
    explanation=(
        "`yield` changes what the `def` *is*: calling `gen_squares(4)` runs no code at "
        "all and hands back a generator object. The classic surprise is printing that "
        "object and seeing `<generator object ...>` instead of numbers — you have the "
        "recipe, not the meal, until something iterates it."
    ),
    starter="def gen_squares(n):\n    ...\n\n\ndef squares(n):\n    ...",
    cases=[
        Case(expected=[0, 1, 4, 9], args=(4,)),
        Case(expected=[], args=(0,)),
        Case(expected=[0], args=(1,)),
        Case(expected=[0, 1, 4, 9, 16, 25], args=(6,)),
    ],
)

q(
    qid="Q-318",
    level=Level.L2,
    topic="Generators",
    kind="function",
    entry="first_naturals",
    prompt=(
        "Write two things:\n\n"
        "1. `naturals()` — an **infinite** generator yielding `0, 1, 2, 3, ...` "
        "forever, with a `while True` loop.\n"
        "2. `first_naturals(n)` — returns a **list** of the first `n` values from a "
        "fresh `naturals()` generator.\n\n"
        "`first_naturals(3)` returns `[0, 1, 2]`. Never call `list()` on the infinite "
        "generator itself."
    ),
    hint=(
        "An infinite generator is safe precisely because nothing runs until something "
        "asks. Take the prefix by calling `next` exactly `n` times — a comprehension "
        "over `range(n)` does it in one line."
    ),
    solution=(
        "def naturals():\n"
        "    n = 0\n"
        "    while True:\n"
        "        yield n\n"
        "        n += 1\n\n\n"
        "def first_naturals(n):\n"
        "    gen = naturals()\n"
        "    return [next(gen) for _ in range(n)]"
    ),
    explanation=(
        "`while True` inside a generator is not a hang: each `yield` suspends the "
        "frame mid-loop and returns control to the caller, who decides whether there "
        "is ever a next iteration. That is what lets generators model streams, "
        "sensors, and `itertools.count` — sequences with no end that still cost O(1) "
        "memory."
    ),
    starter="def naturals():\n    ...\n\n\ndef first_naturals(n):\n    ...",
    cases=[
        Case(expected=[0, 1, 2], args=(3,)),
        Case(expected=[], args=(0,)),
        Case(expected=[0], args=(1,)),
        Case(expected=[0, 1, 2, 3, 4], args=(5,)),
    ],
)

q(
    qid="Q-319",
    level=Level.L2,
    topic="Exceptions",
    kind="function",
    entry="attempt",
    prompt=(
        "Write `attempt(text)` that records which blocks of a full "
        "`try`/`except`/`else`/`finally` actually run, and returns them as a **list of "
        "strings**.\n\n"
        "Append `\"try\"` at the top of the `try` block, then call `int(text)`. Append "
        "`\"except\"` in an `except ValueError` block, `\"else\"` in the `else` block "
        "and `\"finally\"` in the `finally` block. Return the list.\n\n"
        "`attempt(\"42\")` returns `['try', 'else', 'finally']`."
    ),
    hint=(
        "`else` belongs to the *no exception was raised* path and `finally` to the "
        "*whatever happened* path. Keep the `try` block down to the one line that can "
        "actually fail; everything that depends on its success belongs in `else`."
    ),
    solution=(
        "def attempt(text):\n"
        "    events = []\n"
        "    try:\n"
        '        events.append("try")\n'
        "        int(text)\n"
        "    except ValueError:\n"
        '        events.append("except")\n'
        "    else:\n"
        '        events.append("else")\n'
        "    finally:\n"
        '        events.append("finally")\n'
        "    return events"
    ),
    explanation=(
        "`else` exists so the `try` block can stay tiny: code moved into `else` still "
        "runs on success, but an exception it raises is no longer caught by your own "
        "`except`. Putting that code inside `try` instead is the classic way to "
        "accidentally swallow an unrelated `ValueError` from three frames down."
    ),
    starter="def attempt(text):\n    ...",
    cases=[
        Case(expected=["try", "else", "finally"], args=("42",)),
        Case(expected=["try", "except", "finally"], args=("abc",)),
        Case(expected=["try", "except", "finally"], args=("",)),
        Case(expected=["try", "else", "finally"], args=("  7 ",)),
    ],
)

q(
    qid="Q-320",
    level=Level.L2,
    topic="Decorators",
    kind="function",
    entry="add",
    prompt=(
        "Write a decorator `double(func)` that returns a wrapper calling `func` and "
        "returning **twice** whatever it returned.\n\n"
        "Then define `add(a, b)` returning `a + b`, decorated with `@double`, so that "
        "`add(1, 2)` returns `6`.\n\n"
        "The wrapper must accept `*args, **kwargs` so it would work on any function, "
        "not only this one."
    ),
    hint=(
        "A decorator is just a function that takes a function and returns a "
        "replacement. `@double` above `def add` is exactly `add = double(add)` — the "
        "name ends up bound to your inner wrapper."
    ),
    solution=(
        "def double(func):\n"
        "    def wrapper(*args, **kwargs):\n"
        "        return func(*args, **kwargs) * 2\n"
        "    return wrapper\n\n\n"
        "@double\n"
        "def add(a, b):\n"
        "    return a + b"
    ),
    explanation=(
        "There is no decorator machinery in the language beyond that rebinding — "
        "`@` is syntax for one function call. The inner `wrapper` keeps a reference to "
        "`func` through a closure, which is why the original is still reachable even "
        "though its name now points somewhere else."
    ),
    starter=(
        "def double(func):\n"
        "    ...\n\n\n"
        "@double\n"
        "def add(a, b):\n"
        "    ..."
    ),
    cases=[
        Case(expected=6, args=(1, 2)),
        Case(expected=0, args=(0, 0)),
        Case(expected=-4, args=(-3, 1)),
        Case(expected=6.0, args=(2.5, 0.5)),
    ],
)

q(
    qid="Q-321",
    level=Level.L2,
    topic="Context Managers",
    kind="function",
    entry="run_with",
    prompt=(
        "Write a class `Tracker` that is a context manager over a shared list:\n\n"
        "- `Tracker(events)` stores the list;\n"
        "- `__enter__` appends `\"enter\"` and returns `self`;\n"
        "- `__exit__` appends `\"exit\"` and returns `False`.\n\n"
        "Then write `run_with(labels)` that makes a fresh `events = []`, opens "
        "`Tracker(events)` in a `with` statement, appends every string in `labels` "
        "inside the block, and returns `events`.\n\n"
        "`run_with([\"a\"])` returns `['enter', 'a', 'exit']`."
    ),
    hint=(
        "`__exit__` takes three extra parameters — the exception type, value and "
        "traceback — even when nothing went wrong, in which case all three are `None`. "
        "Accept them and ignore them here."
    ),
    solution=(
        "class Tracker:\n"
        "    def __init__(self, events):\n"
        "        self.events = events\n\n"
        "    def __enter__(self):\n"
        '        self.events.append("enter")\n'
        "        return self\n\n"
        "    def __exit__(self, exc_type, exc, tb):\n"
        '        self.events.append("exit")\n'
        "        return False\n\n\n"
        "def run_with(labels):\n"
        "    events = []\n"
        "    with Tracker(events):\n"
        "        for label in labels:\n"
        "            events.append(label)\n"
        "    return events"
    ),
    explanation=(
        "The point of `with` is that `__exit__` runs on *every* way out of the block — "
        "falling off the end, `return`, `break`, or an exception — which is what makes "
        "it the right tool for anything that must be released. Whatever `__enter__` "
        "returns is what `as` binds, and returning `self` is only a convention, not a "
        "rule."
    ),
    starter=(
        "class Tracker:\n"
        "    ...\n\n\n"
        "def run_with(labels):\n"
        "    ..."
    ),
    cases=[
        Case(expected=["enter", "a", "b", "exit"], args=(["a", "b"],)),
        Case(expected=["enter", "exit"], args=([],)),
        Case(expected=["enter", "only", "exit"], args=(["only"],)),
    ],
)

q(
    qid="Q-322",
    level=Level.L2,
    topic="Custom Exceptions",
    kind="function",
    entry="validate",
    prompt=(
        "Define an exception class `NegativeError` that **subclasses `ValueError`**, "
        "then write `validate(n)`:\n\n"
        "- return `n` unchanged when `n >= 0`;\n"
        "- `raise NegativeError` with a message when `n` is negative.\n\n"
        "Because `NegativeError` is a `ValueError`, existing callers that already "
        "write `except ValueError` keep working — the checker relies on that."
    ),
    hint=(
        "A custom exception needs no body at all: `class Name(Base): pass` is a "
        "complete definition. The decision that matters is which base class you "
        "inherit from, because that is what callers will be catching."
    ),
    solution=(
        "class NegativeError(ValueError):\n"
        "    pass\n\n\n"
        "def validate(n):\n"
        "    if n < 0:\n"
        '        raise NegativeError(f"{n} is negative")\n'
        "    return n"
    ),
    explanation=(
        "Choosing the base class is the whole design: inherit from the exception a "
        "caller would *already* be catching, so adding your type breaks nobody, and "
        "callers who care can catch the narrow one. Subclassing `Exception` when "
        "`ValueError` was the honest answer forces every caller to learn your class "
        "name."
    ),
    starter=(
        "class NegativeError(ValueError):\n"
        "    ...\n\n\n"
        "def validate(n):\n"
        "    ..."
    ),
    cases=[
        Case(expected=5, args=(5,)),
        Case(expected=0, args=(0,)),
        Case(expected=None, args=(-1,), raises=ValueError),
        Case(expected=None, args=(-100,), raises=ValueError),
    ],
)

q(
    qid="Q-323",
    level=Level.L2,
    topic="Iterators",
    kind="function",
    entry="manual_sum",
    prompt=(
        "Write `manual_sum(values)` that adds up an iterable of numbers and returns "
        "the total — **without a `for` loop** and without `sum()`.\n\n"
        "Call `iter()` once, then loop with `while True` calling `next()`, and catch "
        "`StopIteration` to know when to stop and return.\n\n"
        "An empty iterable gives `0`."
    ),
    hint=(
        "`StopIteration` is not an error condition — it is how an iterator says "
        "'finished'. Catch it inside the `while` and return the running total from the "
        "handler."
    ),
    solution=(
        "def manual_sum(values):\n"
        "    it = iter(values)\n"
        "    total = 0\n"
        "    while True:\n"
        "        try:\n"
        "            total += next(it)\n"
        "        except StopIteration:\n"
        "            return total"
    ),
    explanation=(
        "This is literally what `for` compiles to, which is why `StopIteration` is a "
        "signal rather than a failure. The practical consequence: a stray "
        "`StopIteration` raised *inside* a generator body used to silently end the "
        "generator — Python 3.7 fixed that by converting it to a `RuntimeError`, "
        "because the silent version hid real bugs."
    ),
    starter="def manual_sum(values):\n    ...",
    cases=[
        Case(expected=6, args=([1, 2, 3],)),
        Case(expected=0, args=([],)),
        Case(expected=5, args=((5,),)),
        Case(expected=4.0, args=([1.5, 2.5],)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-324",
    level=Level.L3,
    topic="Generators",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "gen = (n * n for n in range(3))\n"
        "print(list(gen))\n"
        "print(list(gen))\n"
        "print(sum(gen))\n"
        "```\n\n"
        "Set `answer` to the three printed lines, e.g. "
        "`answer = \"[0, 1, 4]\\n[0, 1, 4]\\n5\"`."
    ),
    hint=(
        "A generator is a cursor, not a collection. Ask where that cursor is sitting "
        "after the first `list()` has finished with it."
    ),
    solution='answer = "[0, 1, 4]\\n[]\\n0"',
    explanation=(
        "A generator is exhausted after one pass and never rewinds — the second "
        "`list()` gets an immediate `StopIteration` and builds `[]`, with no error to "
        "warn you. This bites hardest when a generator is passed to two functions, or "
        "iterated once to count and again to use: store `list(gen)` if you need the "
        "values twice."
    ),
    starter="answer = ...",
    cases=[Case(expected="[0, 1, 4]\n[]\n0")],
)

q(
    qid="Q-325",
    level=Level.L3,
    topic="Generators",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def noisy():\n"
        '    print("start")\n'
        "    yield 1\n"
        '    print("middle")\n'
        "    yield 2\n\n"
        "g = noisy()\n"
        'print("created")\n'
        "print(next(g))\n"
        "```\n\n"
        "Set `answer` to the three printed lines, in the order they appear."
    ),
    hint=(
        "Work out how much of the generator body has executed at the moment "
        "`noisy()` returns. Then ask what the first `next()` runs, and where it stops."
    ),
    solution='answer = "created\\nstart\\n1"',
    explanation=(
        "Calling a generator function runs **none** of its body — it builds a "
        "suspended frame and returns immediately, so `\"created\"` prints first. The "
        "first `next()` runs up to and including the first `yield`, then freezes. "
        "Validation written at the top of a generator therefore fires late, or never: "
        "put argument checks in a plain wrapper function that returns the generator."
    ),
    starter="answer = ...",
    cases=[Case(expected="created\nstart\n1")],
)

q(
    qid="Q-326",
    level=Level.L3,
    topic="Exceptions",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def f():\n"
        "    try:\n"
        '        return "try"\n'
        "    finally:\n"
        '        print("finally")\n\n'
        "print(f())\n\n"
        "def g():\n"
        "    try:\n"
        '        return "try"\n'
        "    finally:\n"
        '        return "finally"\n\n'
        "print(g())\n"
        "```\n\n"
        "Set `answer` to the three printed lines, in order."
    ),
    hint=(
        "A `return` inside `try` does not leave the function immediately — the value "
        "is set aside first. Then ask what happens to that set-aside value if the "
        "`finally` block itself returns."
    ),
    solution='answer = "finally\\ntry\\nfinally"',
    explanation=(
        "`return` inside `try` evaluates its value, then runs `finally` before the "
        "function actually exits — so `f` prints `finally` *before* `print(f())` "
        "prints `try`. If `finally` issues its own `return`, it replaces the pending "
        "one outright: a `return` in `finally` also discards an in-flight exception, "
        "which is why linters flag it."
    ),
    starter="answer = ...",
    cases=[Case(expected="finally\ntry\nfinally")],
)

q(
    qid="Q-327",
    level=Level.L3,
    topic="Decorators",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "import functools\n\n"
        "def plain(func):\n"
        "    def wrapper(*args, **kwargs):\n"
        "        return func(*args, **kwargs)\n"
        "    return wrapper\n\n"
        "def kept(func):\n"
        "    @functools.wraps(func)\n"
        "    def wrapper(*args, **kwargs):\n"
        "        return func(*args, **kwargs)\n"
        "    return wrapper\n\n"
        "@plain\n"
        "def alpha():\n"
        "    pass\n\n"
        "@kept\n"
        "def beta():\n"
        "    pass\n\n"
        "print(alpha.__name__)\n"
        "print(beta.__name__)\n"
        "```\n\n"
        "Set `answer` to the two printed lines."
    ),
    hint=(
        "After decoration the name `alpha` is bound to an object built inside "
        "`plain`. Ask what that object was called where it was defined."
    ),
    solution='answer = "wrapper\\nbeta"',
    explanation=(
        "Without `functools.wraps`, the decorated name points at an object whose "
        "`__name__`, `__doc__` and `__module__` describe the wrapper — so help text, "
        "tracebacks, and anything that dispatches on `__name__` (pytest, Flask's "
        "route registry, `pickle`) all see `wrapper`. `wraps` copies that metadata "
        "across and records the original on `__wrapped__`; put it on every decorator "
        "you write."
    ),
    starter="answer = ...",
    cases=[Case(expected="wrapper\nbeta")],
)

q(
    qid="Q-328",
    level=Level.L3,
    topic="Context Managers",
    kind="function",
    entry="shielded",
    prompt=(
        "Write a class `Swallow` whose `__exit__` returns `True`, and "
        "`shielded(error)`:\n\n"
        "```python\n"
        "def shielded(error):\n"
        "    with Swallow():\n"
        "        if error is not None:\n"
        "            raise error\n"
        '        return "body finished"\n'
        '    return "suppressed"\n'
        "```\n\n"
        "`error` is either `None` or an exception **instance** to raise. Return the "
        "string the code above produces — write `Swallow` so that "
        "`shielded(ValueError(\"x\"))` returns `'suppressed'` rather than blowing up."
    ),
    hint=(
        "`__exit__`'s return value is interpreted as a yes/no answer to one question: "
        "'has this exception been dealt with?' Everything falsy — including the `None` "
        "you get by forgetting to return — means no."
    ),
    solution=(
        "class Swallow:\n"
        "    def __enter__(self):\n"
        "        return self\n\n"
        "    def __exit__(self, exc_type, exc, tb):\n"
        "        return True\n\n\n"
        "def shielded(error):\n"
        "    with Swallow():\n"
        "        if error is not None:\n"
        "            raise error\n"
        '        return "body finished"\n'
        '    return "suppressed"'
    ),
    explanation=(
        "A truthy `__exit__` **suppresses** the exception and execution resumes on the "
        "line after the `with`, which is exactly how `contextlib.suppress` works. It "
        "is also the most dangerous thing a context manager can do by accident: "
        "`return True` written to mean 'cleanup succeeded' silently eats every error "
        "raised in the block."
    ),
    starter=(
        "class Swallow:\n"
        "    ...\n\n\n"
        "def shielded(error):\n"
        "    ..."
    ),
    cases=[
        Case(expected="body finished", args=(None,)),
        Case(expected="suppressed", args=(ValueError("x"),)),
        Case(expected="suppressed", args=(KeyError("k"),)),
        Case(expected="suppressed", args=(ZeroDivisionError(),)),
    ],
)

q(
    qid="Q-329",
    level=Level.L3,
    topic="Generators",
    kind="function",
    entry="flatten_once",
    prompt=(
        "Write `gen_flatten(groups)` — a generator that flattens one level using "
        "`yield from`, not a nested `for` — and `flatten_once(groups)` returning "
        "`list(gen_flatten(groups))`.\n\n"
        "`flatten_once([[1, 2], [3]])` returns the **list** `[1, 2, 3]`. Any iterable "
        "may appear as a group, including a string."
    ),
    hint=(
        "`yield from some_iterable` yields every item of it in turn. That replaces the "
        "inner loop entirely, so the outer `for` is the only loop you need."
    ),
    solution=(
        "def gen_flatten(groups):\n"
        "    for group in groups:\n"
        "        yield from group\n\n\n"
        "def flatten_once(groups):\n"
        "    return list(gen_flatten(groups))"
    ),
    explanation=(
        "`yield from` is not only shorthand for `for x in it: yield x` — it also "
        "forwards `send`, `throw` and `close` to the sub-iterator and captures its "
        "return value, which is what makes generator delegation and recursion work "
        "(Q-349, Q-353). Note that a string is an iterable of characters, so it "
        "flattens into letters."
    ),
    starter="def gen_flatten(groups):\n    ...\n\n\ndef flatten_once(groups):\n    ...",
    cases=[
        Case(expected=[1, 2, 3], args=([[1, 2], [3]],)),
        Case(expected=[], args=([],)),
        Case(expected=[1], args=([[], [1]],)),
        Case(expected=["a", "b", "c"], args=([["a"], "bc"],)),
    ],
)

q(
    qid="Q-330",
    level=Level.L3,
    topic="Decorators",
    kind="function",
    entry="describe",
    prompt=(
        "Write a decorator `logged(func)` that wraps `func` and passes every argument "
        "straight through — but applies `functools.wraps` so the wrapper keeps the "
        "original's identity.\n\n"
        "Decorate `triple(n)` (returning `n * 3`) with it, then write `describe(n)` "
        "returning the **tuple** `(triple.__name__, triple(n))`.\n\n"
        "`describe(2)` returns `('triple', 6)`."
    ),
    hint=(
        "`functools.wraps(func)` is itself a decorator, applied to your inner wrapper "
        "function. It copies the metadata; it does not change what the wrapper does."
    ),
    solution=(
        "import functools\n\n\n"
        "def logged(func):\n"
        "    @functools.wraps(func)\n"
        "    def wrapper(*args, **kwargs):\n"
        "        return func(*args, **kwargs)\n"
        "    return wrapper\n\n\n"
        "@logged\n"
        "def triple(n):\n"
        "    return n * 3\n\n\n"
        "def describe(n):\n"
        "    return (triple.__name__, triple(n))"
    ),
    explanation=(
        "`wraps` copies `__name__`, `__doc__`, `__module__`, `__qualname__` and "
        "`__dict__`, and sets `__wrapped__` so `inspect.signature` can still find the "
        "real parameters. Skipping it makes every decorated function in a codebase "
        "report itself as `wrapper`, which turns tracebacks and log lines into a "
        "guessing game."
    ),
    starter=(
        "import functools\n\n\n"
        "def logged(func):\n"
        "    ...\n\n\n"
        "@logged\n"
        "def triple(n):\n"
        "    ...\n\n\n"
        "def describe(n):\n"
        "    ..."
    ),
    cases=[
        Case(expected=("triple", 6), args=(2,)),
        Case(expected=("triple", 0), args=(0,)),
        Case(expected=("triple", -3), args=(-1,)),
        Case(expected=("triple", 4.5), args=(1.5,)),
    ],
)

q(
    qid="Q-331",
    level=Level.L3,
    topic="Context Managers",
    kind="function",
    entry="run_collecting",
    prompt=(
        "Write `collecting(events)` as a context manager using the "
        "`@contextlib.contextmanager` decorator — **not** a class:\n\n"
        "- append `\"enter\"`, then `yield events`, then append `\"exit\"`;\n"
        "- the append of `\"exit\"` must be in a `finally` so it happens even if the "
        "block raises.\n\n"
        "Then write `run_collecting(labels)` that makes a fresh list, opens "
        "`collecting(...) as log`, appends every string in `labels` to `log`, and "
        "returns the events list.\n\n"
        "`run_collecting([\"a\"])` returns `['enter', 'a', 'exit']`."
    ),
    hint=(
        "The decorated generator must yield exactly once. Everything before the "
        "`yield` is `__enter__`, the yielded value is what `as` binds, and everything "
        "after is `__exit__`."
    ),
    solution=(
        "from contextlib import contextmanager\n\n\n"
        "@contextmanager\n"
        "def collecting(events):\n"
        '    events.append("enter")\n'
        "    try:\n"
        "        yield events\n"
        "    finally:\n"
        '        events.append("exit")\n\n\n'
        "def run_collecting(labels):\n"
        "    events = []\n"
        "    with collecting(events) as log:\n"
        "        for label in labels:\n"
        "            log.append(label)\n"
        "    return events"
    ),
    explanation=(
        "`@contextmanager` turns a one-`yield` generator into a context manager by "
        "resuming it inside `__exit__`. The `try`/`finally` is mandatory, not "
        "stylistic: if the `with` body raises, that exception is thrown back in *at "
        "the `yield`*, so any cleanup written as a plain statement after the `yield` "
        "would simply never run."
    ),
    starter=(
        "from contextlib import contextmanager\n\n\n"
        "@contextmanager\n"
        "def collecting(events):\n"
        "    ...\n\n\n"
        "def run_collecting(labels):\n"
        "    ..."
    ),
    cases=[
        Case(expected=["enter", "a", "exit"], args=(["a"],)),
        Case(expected=["enter", "exit"], args=([],)),
        Case(expected=["enter", "x", "y", "exit"], args=(["x", "y"],)),
    ],
)

q(
    qid="Q-332",
    level=Level.L3,
    topic="Exceptions",
    kind="function",
    entry="inspect_parse",
    prompt=(
        "Write `parse(text)` that returns `int(text)`, but on `ValueError` raises "
        "`RuntimeError(f\"bad input: {text!r}\")` **from** the original exception.\n\n"
        "Then write `inspect_parse(text)` returning a **tuple**:\n\n"
        "- `(\"ok\", value)` when the text parses;\n"
        "- `(type(exc).__name__, type(exc.__cause__).__name__)` when it does not.\n\n"
        "`inspect_parse(\"abc\")` returns `('RuntimeError', 'ValueError')`."
    ),
    hint=(
        "`raise New(...) from original` sets one specific dunder attribute on the new "
        "exception. Bind the original with `except ValueError as exc` so you have "
        "something to chain from."
    ),
    solution=(
        "def parse(text):\n"
        "    try:\n"
        "        return int(text)\n"
        "    except ValueError as exc:\n"
        '        raise RuntimeError(f"bad input: {text!r}") from exc\n\n\n'
        "def inspect_parse(text):\n"
        "    try:\n"
        '        return ("ok", parse(text))\n'
        "    except RuntimeError as exc:\n"
        "        return (type(exc).__name__, type(exc.__cause__).__name__)"
    ),
    explanation=(
        "`raise ... from exc` sets `__cause__`, which is what makes the traceback say "
        "*The above exception was the direct cause of the following exception* instead "
        "of the vaguer *During handling ... another exception occurred*. Translating a "
        "low-level error into a domain one without `from` throws away the original "
        "traceback's meaning — and `from None` deliberately hides it, which is "
        "occasionally what you want."
    ),
    starter="def parse(text):\n    ...\n\n\ndef inspect_parse(text):\n    ...",
    cases=[
        Case(expected=("ok", 42), args=("42",)),
        Case(expected=("RuntimeError", "ValueError"), args=("abc",)),
        Case(expected=("RuntimeError", "ValueError"), args=("",)),
        Case(expected=("RuntimeError", "ValueError"), args=("3.5",)),
    ],
)

q(
    qid="Q-333",
    level=Level.L3,
    topic="Iterators",
    kind="function",
    entry="countdown",
    prompt=(
        "Implement the iterator protocol by hand. Write a class `Countdown(start)` "
        "with:\n\n"
        "- `__iter__` returning `self`;\n"
        "- `__next__` yielding `start`, `start - 1`, ... down to `1`, then raising "
        "`StopIteration`.\n\n"
        "Then write `countdown(start)` returning `list(Countdown(start))`. "
        "`countdown(3)` returns `[3, 2, 1]`; a `start` of `0` or less gives `[]`. "
        "No `yield` anywhere — that is Q-317's job."
    ),
    hint=(
        "The object has to remember where it is between calls, so the current position "
        "belongs on `self`. `__next__` takes no arguments and either returns the next "
        "item or raises."
    ),
    solution=(
        "class Countdown:\n"
        "    def __init__(self, start):\n"
        "        self.current = start\n\n"
        "    def __iter__(self):\n"
        "        return self\n\n"
        "    def __next__(self):\n"
        "        if self.current <= 0:\n"
        "            raise StopIteration\n"
        "        self.current -= 1\n"
        "        return self.current + 1\n\n\n"
        "def countdown(start):\n"
        "    return list(Countdown(start))"
    ),
    explanation=(
        "`__iter__` and `__next__` are two different jobs: an *iterable* can hand out "
        "fresh cursors, an *iterator* is one cursor. Returning `self` from `__iter__` "
        "collapses them, which is why this object — like a generator — is single-use, "
        "and why a second `for` over the same `Countdown` yields nothing. Separate "
        "them (a `list` returns a new iterator each time) when you want repeat passes."
    ),
    starter="class Countdown:\n    ...\n\n\ndef countdown(start):\n    ...",
    cases=[
        Case(expected=[3, 2, 1], args=(3,)),
        Case(expected=[], args=(0,)),
        Case(expected=[1], args=(1,)),
        Case(expected=[], args=(-2,)),
    ],
)

q(
    qid="Q-334",
    level=Level.L3,
    topic="Custom Exceptions",
    kind="function",
    entry="handle",
    prompt=(
        "Build a small exception hierarchy: `AppError(Exception)`, and two subclasses "
        "`NotFound(AppError)` and `Denied(AppError)`.\n\n"
        "Write `handle(kind)`:\n\n"
        "- `kind == \"missing\"` -> raise `NotFound`; `kind == \"denied\"` -> raise "
        "`Denied`; `kind == \"other\"` -> raise `ValueError`; anything else -> return "
        "`\"ok\"`;\n"
        "- catch **only `AppError`** and return `f\"app:{type(exc).__name__}\"`.\n\n"
        "`handle(\"missing\")` returns `'app:NotFound'`. A `ValueError` must escape "
        "uncaught."
    ),
    hint=(
        "One `except` clause naming the base class catches every descendant, and the "
        "instance you bind still knows its own concrete class. Nothing outside the "
        "hierarchy should be listed."
    ),
    solution=(
        "class AppError(Exception):\n"
        "    pass\n\n\n"
        "class NotFound(AppError):\n"
        "    pass\n\n\n"
        "class Denied(AppError):\n"
        "    pass\n\n\n"
        "def handle(kind):\n"
        "    try:\n"
        '        if kind == "missing":\n'
        '            raise NotFound("missing")\n'
        '        if kind == "denied":\n'
        '            raise Denied("denied")\n'
        '        if kind == "other":\n'
        '            raise ValueError("other")\n'
        '        return "ok"\n'
        "    except AppError as exc:\n"
        '        return f"app:{type(exc).__name__}"'
    ),
    explanation=(
        "A single base class per library is the standard shape: callers who want "
        "everything write `except AppError`, callers who want one case write "
        "`except NotFound`, and you can add subclasses later without breaking either. "
        "The escaping `ValueError` is the feature — an error outside your domain "
        "should not be quietly relabelled as one of yours."
    ),
    starter=(
        "class AppError(Exception):\n"
        "    ...\n\n\n"
        "def handle(kind):\n"
        "    ..."
    ),
    cases=[
        Case(expected="app:NotFound", args=("missing",)),
        Case(expected="app:Denied", args=("denied",)),
        Case(expected="ok", args=("fine",)),
        Case(expected=None, args=("other",), raises=ValueError),
    ],
)

q(
    qid="Q-335",
    level=Level.L3,
    topic="Generators",
    kind="function",
    entry="take",
    prompt=(
        "Write `gen_take(iterable, n)` — a generator yielding at most the first `n` "
        "items of `iterable` — and `take(iterable, n)` returning "
        "`list(gen_take(iterable, n))`.\n\n"
        "It must stop early: pulling `n` items from a million-item source may touch "
        "only `n` of them, and asking for more items than exist returns what there is "
        "rather than raising.\n\n"
        "`take([1, 2, 3, 4], 2)` returns the **list** `[1, 2]`."
    ),
    hint=(
        "Drive the source with an explicit iterator so you control how many items are "
        "pulled. Running out early is signalled by `StopIteration` from `next` — catch "
        "it and `return` from the generator."
    ),
    solution=(
        "def gen_take(iterable, n):\n"
        "    it = iter(iterable)\n"
        "    for _ in range(n):\n"
        "        try:\n"
        "            yield next(it)\n"
        "        except StopIteration:\n"
        "            return\n\n\n"
        "def take(iterable, n):\n"
        "    return list(gen_take(iterable, n))"
    ),
    explanation=(
        "A bare `return` inside a generator ends it — it does not return a value to "
        "the `for` loop, it raises `StopIteration` behind the scenes. Catching the "
        "inner `StopIteration` explicitly is required since Python 3.7: letting it "
        "escape the generator body now becomes a `RuntimeError` instead of quietly "
        "ending the stream. `itertools.islice` is the production version of this."
    ),
    starter="def gen_take(iterable, n):\n    ...\n\n\ndef take(iterable, n):\n    ...",
    cases=[
        Case(expected=[1, 2], args=([1, 2, 3, 4], 2)),
        Case(expected=[1], args=([1], 5)),
        Case(expected=[], args=([], 3)),
        Case(expected=[], args=("abc", 0)),
        Case(expected=[0, 1, 2], args=(range(1000000), 3)),
    ],
)

q(
    qid="Q-336",
    level=Level.L3,
    topic="Generators",
    kind="custom",
    entry="running_total",
    constraints=["needs-generator"],
    prompt=(
        "Write `running_total(numbers)` returning the **list** of running totals: "
        "`running_total([1, 2, 3])` returns `[1, 3, 6]`, and an empty input gives "
        "`[]`.\n\n"
        "The work must be done by a **generator defined inside** `running_total` — a "
        "nested `def` that `yield`s the total after each number — with the outer "
        "function returning `list(...)` of it.\n\n"
        "Your solution must contain `yield`: building the list directly does not "
        "count, even though it would produce the same answer."
    ),
    hint=(
        "Carry the total in a local variable across `yield`s — a generator's locals "
        "survive suspension, which is exactly what makes this shape work without a "
        "class or a global. The nested generator closes over `numbers`, so it needs "
        "no parameter of its own."
    ),
    solution=(
        "def running_total(numbers):\n"
        "    def gen():\n"
        "        total = 0\n"
        "        for n in numbers:\n"
        "            total += n\n"
        "            yield total\n\n"
        "    return list(gen())"
    ),
    explanation=(
        "The generator frame keeps its local variables alive between `yield`s, so "
        "accumulating state needs no object and no `nonlocal`. That is why generators "
        "are the natural fit for streaming aggregates — `itertools.accumulate` is this "
        "function, and it works on a feed that never ends."
    ),
    starter="def running_total(numbers):\n    ...",
    cases=[
        Case(expected=[1, 3, 6], args=([1, 2, 3],)),
        Case(expected=[], args=([],)),
        Case(expected=[5], args=([5],)),
        Case(expected=[1, 0, 1], args=([1, -1, 1],)),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-337",
    level=Level.L4,
    topic="Decorators",
    kind="function",
    entry="shout",
    prompt=(
        "Write a **decorator factory** `repeat(times)`: `@repeat(3)` on a function "
        "makes every call run it three times and return a **list** of the three "
        "results.\n\n"
        "Use `functools.wraps` on the wrapper. Then define `shout(word)` returning "
        "`word.upper()`, decorated with `@repeat(3)`, so `shout(\"hi\")` returns "
        "`['HI', 'HI', 'HI']`."
    ),
    hint=(
        "`@repeat(3)` is a *call* first, then a decoration — `shout = repeat(3)(shout)`. "
        "That means one more level of nesting than Q-320: three functions, not two."
    ),
    solution=(
        "import functools\n\n\n"
        "def repeat(times):\n"
        "    def decorate(func):\n"
        "        @functools.wraps(func)\n"
        "        def wrapper(*args, **kwargs):\n"
        "            return [func(*args, **kwargs) for _ in range(times)]\n"
        "        return wrapper\n"
        "    return decorate\n\n\n"
        "@repeat(3)\n"
        "def shout(word):\n"
        "    return word.upper()"
    ),
    explanation=(
        "A decorator with arguments is not a decorator — it is a function that "
        "*returns* one, which is why the body needs three nested `def`s. Forgetting "
        "the middle layer gives the classic `TypeError: decorate() missing 1 required "
        "positional argument`, or worse, a decorator that silently receives your "
        "argument where it expected the function."
    ),
    starter=(
        "import functools\n\n\n"
        "def repeat(times):\n"
        "    ...\n\n\n"
        "# once repeat works, decorate shout with @repeat(3)\n"
        "def shout(word):\n"
        "    ..."
    ),
    cases=[
        Case(expected=["HI", "HI", "HI"], args=("hi",)),
        Case(expected=["", "", ""], args=("",)),
        Case(expected=["A", "A", "A"], args=("a",)),
        Case(expected=["MIX", "MIX", "MIX"], args=("Mix",)),
    ],
)

q(
    qid="Q-338",
    level=Level.L4,
    topic="Decorators",
    kind="function",
    entry="say",
    prompt=(
        "Write two decorators: `add_exclaim` appends `\"!\"` to the wrapped "
        "function's string result, `add_question` appends `\"?\"`.\n\n"
        "Stack **both** on `say(word)` (which returns `word`) so that "
        "`say(\"hi\")` returns `'hi?!'` — the `?` applied first, then the `!`.\n\n"
        "The order of the two `@` lines is the entire question."
    ),
    hint=(
        "Decorators apply bottom-up: the one closest to the `def` wraps the raw "
        "function, and the one above wraps that. So the result you see is built "
        "outermost-last."
    ),
    solution=(
        "def add_exclaim(func):\n"
        "    def wrapper(*args, **kwargs):\n"
        '        return func(*args, **kwargs) + "!"\n'
        "    return wrapper\n\n\n"
        "def add_question(func):\n"
        "    def wrapper(*args, **kwargs):\n"
        '        return func(*args, **kwargs) + "?"\n'
        "    return wrapper\n\n\n"
        "@add_exclaim\n"
        "@add_question\n"
        "def say(word):\n"
        "    return word"
    ),
    explanation=(
        "Stacked decorators read like nested calls written from the inside out: "
        "`say = add_exclaim(add_question(say))`. Application order is bottom-up, but "
        "*execution* order at call time is top-down — the outermost wrapper runs "
        "first and the original runs last, which is why `@app.route` must sit above "
        "`@login_required` and not below it."
    ),
    starter=(
        "def add_exclaim(func):\n"
        "    ...\n\n\n"
        "def add_question(func):\n"
        "    ...\n\n\n"
        "def say(word):\n"
        "    return word"
    ),
    cases=[
        Case(expected="hi?!", args=("hi",)),
        Case(expected="?!", args=("",)),
        Case(expected="ok?!", args=("ok",)),
        Case(expected="a b?!", args=("a b",)),
    ],
)

q(
    qid="Q-339",
    level=Level.L4,
    topic="Decorators",
    kind="function",
    entry="measure",
    prompt=(
        "Write a decorator `memoize(func)` that caches results in a dict keyed by the "
        "single argument, so a repeated argument never reaches `func` again.\n\n"
        "Then write `measure(inputs)` that — **inside the function**, so each call "
        "starts with an empty cache — defines a memoized `square(n)` recording each "
        "real call, maps it over `inputs`, and returns the tuple "
        "`(results_list, number_of_real_calls)`.\n\n"
        "`measure([2, 2, 3])` returns `([4, 4, 9], 2)`."
    ),
    hint=(
        "The cache dict lives in the decorator's scope, not inside the wrapper — "
        "created once per decoration, then closed over. Defining the decorated "
        "function inside `measure` is what keeps the cache from leaking between calls."
    ),
    solution=(
        "import functools\n\n\n"
        "def memoize(func):\n"
        "    cache = {}\n\n"
        "    @functools.wraps(func)\n"
        "    def wrapper(n):\n"
        "        if n not in cache:\n"
        "            cache[n] = func(n)\n"
        "        return cache[n]\n\n"
        "    return wrapper\n\n\n"
        "def measure(inputs):\n"
        "    calls = []\n\n"
        "    @memoize\n"
        "    def square(n):\n"
        "        calls.append(n)\n"
        "        return n * n\n\n"
        "    results = [square(n) for n in inputs]\n"
        "    return (results, len(calls))"
    ),
    explanation=(
        "The cache is per-decoration, so a module-level memoized function keeps its "
        "entries for the life of the process — which is a leak if arguments are "
        "unbounded, and a correctness bug if `func` is not pure. `n not in cache` "
        "rather than `cache.get(n)` matters too: a legitimately cached `None` or `0` "
        "would defeat the truthiness check. `functools.lru_cache` is the real one."
    ),
    starter=(
        "import functools\n\n\n"
        "def memoize(func):\n"
        "    ...\n\n\n"
        "def measure(inputs):\n"
        "    ..."
    ),
    cases=[
        Case(expected=([4, 4, 9], 2), args=([2, 2, 3],)),
        Case(expected=([], 0), args=([],)),
        Case(expected=([25], 1), args=([5],)),
        Case(expected=([1, 1, 1, 1], 1), args=([1, 1, 1, 1],)),
    ],
)

q(
    qid="Q-340",
    level=Level.L4,
    topic="Generators",
    kind="function",
    entry="observe",
    prompt=(
        "Prove laziness by observation. Write `counted(numbers, log)` — a generator "
        "that, for each number, appends it to `log` and then yields it doubled.\n\n"
        "Then write `observe(numbers)` returning the **3-tuple** "
        "`(items_logged_before_any_next, first_value, items_logged_after_one_next)`:\n\n"
        "create the generator, record `len(log)`, call `next()` once, and record "
        "`len(log)` again.\n\n"
        "`observe([5, 6, 7])` returns `(0, 10, 1)`. If the source is empty, let the "
        "`next()` raise."
    ),
    hint=(
        "Nothing in the generator body has run at the moment the generator object is "
        "created. One `next()` runs exactly up to the first `yield` and no further."
    ),
    solution=(
        "def counted(numbers, log):\n"
        "    for n in numbers:\n"
        "        log.append(n)\n"
        "        yield n * 2\n\n\n"
        "def observe(numbers):\n"
        "    log = []\n"
        "    gen = counted(numbers, log)\n"
        "    created = len(log)\n"
        "    first = next(gen)\n"
        "    return (created, first, len(log))"
    ),
    explanation=(
        "A generator does exactly as much work as it is asked for and no more — one "
        "`next()` touches one source item, which is why a generator pipeline over a "
        "10 GB file never loads more than one record. The flip side is that side "
        "effects you write in a generator happen *when consumed*, not when called, so "
        "a generator that is built and never iterated does nothing at all."
    ),
    starter="def counted(numbers, log):\n    ...\n\n\ndef observe(numbers):\n    ...",
    cases=[
        Case(expected=(0, 10, 1), args=([5, 6, 7],)),
        Case(expected=(0, 2, 1), args=([1],)),
        Case(expected=(0, 0, 1), args=([0, 9],)),
        Case(expected=None, args=([],), raises=StopIteration),
    ],
)

q(
    qid="Q-341",
    level=Level.L4,
    topic="Generators",
    kind="function",
    entry="pipeline",
    prompt=(
        "Build a two-stage generator pipeline:\n\n"
        "- `evens(numbers)` — a generator yielding only the even numbers;\n"
        "- `scaled(numbers, factor)` — a generator yielding each number times "
        "`factor`;\n"
        "- `pipeline(numbers, factor)` — returns "
        "`list(scaled(evens(numbers), factor))`, a plain **list**.\n\n"
        "`pipeline([1, 2, 3, 4], 10)` returns `[20, 40]`. Neither generator may build "
        "an intermediate list."
    ),
    hint=(
        "Each stage takes an iterable and yields an iterable, so stages compose by "
        "being passed to one another. No stage ever needs to know how long the stream "
        "is."
    ),
    solution=(
        "def evens(numbers):\n"
        "    for n in numbers:\n"
        "        if n % 2 == 0:\n"
        "            yield n\n\n\n"
        "def scaled(numbers, factor):\n"
        "    for n in numbers:\n"
        "        yield n * factor\n\n\n"
        "def pipeline(numbers, factor):\n"
        "    return list(scaled(evens(numbers), factor))"
    ),
    explanation=(
        "Chained generators form a pull-based pipeline: the outer `list()` asks "
        "`scaled` for one item, which asks `evens` for one item, which asks the "
        "source — so peak memory is one item per stage regardless of input size. The "
        "equivalent list-at-each-stage version materialises the whole dataset three "
        "times, which is the difference between streaming a log file and running out "
        "of RAM."
    ),
    starter=(
        "def evens(numbers):\n"
        "    ...\n\n\n"
        "def scaled(numbers, factor):\n"
        "    ...\n\n\n"
        "def pipeline(numbers, factor):\n"
        "    ..."
    ),
    cases=[
        Case(expected=[20, 40], args=([1, 2, 3, 4], 10)),
        Case(expected=[], args=([], 3)),
        Case(expected=[], args=([1, 3], 2)),
        Case(expected=[0, 2], args=([0, 2], 1)),
    ],
)

q(
    qid="Q-342",
    level=Level.L4,
    topic="Context Managers",
    kind="function",
    entry="watch",
    prompt=(
        "Write a class `Report` whose `__exit__` **inspects** the exception it is "
        "given and records it on `self.seen`:\n\n"
        "- `None` when the block finished cleanly;\n"
        "- the tuple `(exc_type.__name__, str(exc))` otherwise.\n\n"
        "`__exit__` must return `False` so the exception still propagates.\n\n"
        "Then write `watch(error)`: build a `Report`, run a `with` block that raises "
        "`error` when it is not `None` (catching it outside the `with`), and return "
        "`reporter.seen`."
    ),
    hint=(
        "`__exit__(self, exc_type, exc, tb)` receives the class, the instance and the "
        "traceback — all three are `None` on the clean path, which is the test you "
        "need."
    ),
    solution=(
        "class Report:\n"
        "    def __init__(self):\n"
        "        self.seen = None\n\n"
        "    def __enter__(self):\n"
        "        return self\n\n"
        "    def __exit__(self, exc_type, exc, tb):\n"
        "        self.seen = None if exc_type is None else (exc_type.__name__, str(exc))\n"
        "        return False\n\n\n"
        "def watch(error):\n"
        "    reporter = Report()\n"
        "    try:\n"
        "        with reporter:\n"
        "            if error is not None:\n"
        "                raise error\n"
        "    except Exception:\n"
        "        pass\n"
        "    return reporter.seen"
    ),
    explanation=(
        "Observing without suppressing is the useful default: return `False` (or "
        "nothing at all) and you get a hook that can log, time, or roll back while "
        "leaving error handling to the caller. Note `str(KeyError(\"k\"))` is "
        "`\"'k'\"` with quotes — `KeyError` repr's its argument, which is why its "
        "messages look odd in logs."
    ),
    starter="class Report:\n    ...\n\n\ndef watch(error):\n    ...",
    cases=[
        Case(expected=None, args=(None,)),
        Case(expected=("ValueError", "boom"), args=(ValueError("boom"),)),
        Case(expected=("KeyError", "'k'"), args=(KeyError("k"),)),
        Case(expected=("RuntimeError", ""), args=(RuntimeError(),)),
    ],
)

q(
    qid="Q-343",
    level=Level.L4,
    topic="Context Managers",
    kind="function",
    entry="run_guarded",
    prompt=(
        "Write `guarded(events)` with `@contextlib.contextmanager`:\n\n"
        "- append `\"open\"`, then `yield`;\n"
        "- catch `ValueError` around the `yield` and append `\"handled\"` (swallowing "
        "it);\n"
        "- append `\"close\"` in a `finally`.\n\n"
        "Then write `run_guarded(error)`: fresh list, `with guarded(events)`, append "
        "`\"body\"`, raise `error` when it is not `None`, return the list.\n\n"
        "A `ValueError` gives `['open', 'body', 'handled', 'close']`; any other "
        "exception propagates out of `run_guarded` untouched."
    ),
    hint=(
        "An exception raised in the `with` body arrives at the `yield` inside the "
        "generator, so you catch it with an ordinary `try`/`except` wrapped around "
        "that `yield`. Catching it is what suppresses it."
    ),
    solution=(
        "from contextlib import contextmanager\n\n\n"
        "@contextmanager\n"
        "def guarded(events):\n"
        '    events.append("open")\n'
        "    try:\n"
        "        yield\n"
        "    except ValueError:\n"
        '        events.append("handled")\n'
        "    finally:\n"
        '        events.append("close")\n\n\n'
        "def run_guarded(error):\n"
        "    events = []\n"
        "    with guarded(events):\n"
        '        events.append("body")\n'
        "        if error is not None:\n"
        "            raise error\n"
        "    return events"
    ),
    explanation=(
        "In a `@contextmanager` generator, catching the exception at the `yield` is "
        "the equivalent of `__exit__` returning `True`, and letting it through is the "
        "equivalent of returning `False` — no boolean bookkeeping. Watch the return "
        "path though: when the body raises and the manager swallows it, the `with` "
        "block never finishes, so `run_guarded` returns from *after* the block."
    ),
    starter=(
        "from contextlib import contextmanager\n\n\n"
        "@contextmanager\n"
        "def guarded(events):\n"
        "    ...\n\n\n"
        "def run_guarded(error):\n"
        "    ..."
    ),
    cases=[
        Case(expected=["open", "body", "close"], args=(None,)),
        Case(expected=["open", "body", "handled", "close"], args=(ValueError("x"),)),
        Case(expected=["open", "body", "handled", "close"], args=(ValueError("other"),)),
        Case(expected=None, args=(KeyError("k"),), raises=KeyError),
    ],
)

q(
    qid="Q-344",
    level=Level.L4,
    topic="Exceptions",
    kind="function",
    entry="report",
    prompt=(
        "Write `risky(n, log)` that returns `10 / n`, but on `ZeroDivisionError` "
        "appends `\"logged\"` to `log` and then **re-raises the same exception with a "
        "bare `raise`** — not `raise ZeroDivisionError(...)`.\n\n"
        "Then write `report(n)` returning the tuple `(log, value)` on success and "
        "`(log, None)` when the division failed.\n\n"
        "`report(0)` returns `(['logged'], None)`; `report(5)` returns `([], 2.0)`."
    ),
    hint=(
        "Inside an `except` block, `raise` on its own re-raises the exception "
        "currently being handled. That is different from raising a fresh instance of "
        "the same class in one specific, important way."
    ),
    solution=(
        "def risky(n, log):\n"
        "    try:\n"
        "        return 10 / n\n"
        "    except ZeroDivisionError:\n"
        '        log.append("logged")\n'
        "        raise\n\n\n"
        "def report(n):\n"
        "    log = []\n"
        "    try:\n"
        "        value = risky(n, log)\n"
        "    except ZeroDivisionError:\n"
        "        return (log, None)\n"
        "    return (log, value)"
    ),
    explanation=(
        "A bare `raise` preserves the original exception object **and its traceback**, "
        "so the report still points at the line that actually failed; "
        "`raise ZeroDivisionError(...)` throws that away and blames your handler. "
        "Log-and-re-raise is the right shape for a middle layer: record the context, "
        "then let the caller decide policy."
    ),
    starter="def risky(n, log):\n    ...\n\n\ndef report(n):\n    ...",
    cases=[
        Case(expected=([], 2.0), args=(5,)),
        Case(expected=(["logged"], None), args=(0,)),
        Case(expected=([], 5.0), args=(2,)),
        Case(expected=([], -10.0), args=(-1,)),
    ],
)

q(
    qid="Q-345",
    level=Level.L4,
    topic="Exceptions",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def boom():\n"
        "    raise KeyboardInterrupt\n\n"
        "def run(job):\n"
        "    try:\n"
        "        job()\n"
        "    except:\n"
        '        return "handled"\n'
        '    return "fine"\n\n'
        "print(run(boom))\n\n"
        "def run_narrow(job):\n"
        "    try:\n"
        "        job()\n"
        "    except Exception:\n"
        '        return "handled"\n'
        '    return "fine"\n\n'
        "try:\n"
        "    print(run_narrow(boom))\n"
        "except KeyboardInterrupt:\n"
        '    print("escaped")\n'
        "```\n\n"
        "Set `answer` to the two printed lines."
    ),
    hint=(
        "`KeyboardInterrupt` does not sit where you might assume in the exception "
        "hierarchy. Find its base class, then ask which of the two `except` clauses "
        "can possibly match it."
    ),
    solution='answer = "handled\\nescaped"',
    explanation=(
        "`KeyboardInterrupt`, `SystemExit` and `GeneratorExit` inherit from "
        "`BaseException`, **not** `Exception`, precisely so that `except Exception` "
        "leaves them alone. A bare `except:` catches `BaseException` and therefore "
        "makes Ctrl-C do nothing — the reason bare `except` is the single most "
        "reliable smell in a Python review."
    ),
    starter="answer = ...",
    cases=[Case(expected="handled\nescaped")],
)

q(
    qid="Q-346",
    level=Level.L4,
    topic="Exceptions",
    kind="function",
    entry="classify",
    prompt=(
        "Write `classify(error)` that takes an exception **instance**, raises it "
        "inside a `try`, and returns a label from a chain of `except` clauses:\n\n"
        "- `ZeroDivisionError` -> `'divide by zero'`\n"
        "- `ArithmeticError` -> `'arithmetic'`\n"
        "- `LookupError` -> `'lookup'`\n"
        "- anything else -> `'other'`\n\n"
        "`ZeroDivisionError` is a subclass of `ArithmeticError`, and both `KeyError` "
        "and `IndexError` are subclasses of `LookupError` — so the order of your "
        "clauses decides whether the first rule is reachable at all."
    ),
    hint=(
        "`except` clauses are tested top to bottom and the first match wins; a base "
        "class listed early shadows every subclass listed later. Sort them "
        "most-specific-first."
    ),
    solution=(
        "def classify(error):\n"
        "    try:\n"
        "        raise error\n"
        "    except ZeroDivisionError:\n"
        '        return "divide by zero"\n'
        "    except ArithmeticError:\n"
        '        return "arithmetic"\n'
        "    except LookupError:\n"
        '        return "lookup"\n'
        "    except Exception:\n"
        '        return "other"'
    ),
    explanation=(
        "Putting `except ArithmeticError` above `except ZeroDivisionError` makes the "
        "second clause dead code — and Python will not warn you, because it is "
        "perfectly legal. This is the same most-specific-first rule as an `isinstance` "
        "chain, and it is why `except Exception` belongs last or not at all."
    ),
    starter="def classify(error):\n    ...",
    cases=[
        Case(expected="divide by zero", args=(ZeroDivisionError(),)),
        Case(expected="arithmetic", args=(OverflowError(),)),
        Case(expected="lookup", args=(KeyError("k"),)),
        Case(expected="lookup", args=(IndexError(),)),
        Case(expected="other", args=(ValueError(),)),
    ],
)

q(
    qid="Q-347",
    level=Level.L4,
    topic="Iterators",
    kind="function",
    entry="drain",
    prompt=(
        "`iter()` has a two-argument form: `iter(callable, sentinel)` calls the "
        "zero-argument callable over and over and stops — without yielding it — the "
        "moment the result equals `sentinel`.\n\n"
        "Write `drain(items, sentinel)`: copy `items` into a local list, define a "
        "zero-argument `pull()` that pops from the front (returning `sentinel` when "
        "empty), and return `list(iter(pull, sentinel))`.\n\n"
        "`drain([1, 2, 0, 3], 0)` returns the **list** `[1, 2]` — everything before "
        "the sentinel, and nothing after."
    ),
    hint=(
        "The callable takes no arguments, so whatever state it reads must come from "
        "the enclosing scope. Returning the sentinel when the source runs out is what "
        "terminates the loop for you."
    ),
    solution=(
        "def drain(items, sentinel):\n"
        "    source = list(items)\n\n"
        "    def pull():\n"
        "        return source.pop(0) if source else sentinel\n\n"
        "    return list(iter(pull, sentinel))"
    ),
    explanation=(
        "This form exists for the read-until-marker pattern: "
        "`iter(lambda: f.read(4096), b\"\")` streams a file in blocks, and "
        "`iter(sock.recv_line, \"\")` drains a socket — both without a `while True` "
        "and a `break`. The comparison is `==`, not `is`, so a sentinel that compares "
        "equal to a legitimate value will truncate your stream early."
    ),
    starter="def drain(items, sentinel):\n    ...",
    cases=[
        Case(expected=[1, 2], args=([1, 2, 0, 3], 0)),
        Case(expected=[], args=([], 0)),
        Case(expected=[1, 2], args=([1, 2], 0)),
        Case(expected=["a", "b"], args=(["a", "b", "stop", "c"], "stop")),
    ],
)

q(
    qid="Q-348",
    level=Level.L4,
    topic="Custom Exceptions",
    kind="function",
    entry="describe_record",
    prompt=(
        "Write `ValidationError(ValueError)` carrying **structured data**, not just a "
        "message: `ValidationError(field, message)` calls "
        "`super().__init__(f\"{field}: {message}\")` and stores `self.field` and "
        "`self.message`.\n\n"
        "Write `validate_name(record)`: raise `ValidationError(\"name\", \"missing\")` when "
        "`record` has no `\"name\"` key, `ValidationError(\"name\", \"empty\")` when "
        "the value is empty, otherwise return the name.\n\n"
        "Write `describe_record(record)` returning the tuple `(\"ok\", name)` on "
        "success, or `(exc.field, exc.message)` on failure."
    ),
    hint=(
        "Call `super().__init__` with the human-readable message so `str(exc)` still "
        "works, then set your own attributes. A handler should never have to parse a "
        "message string to learn which field failed."
    ),
    solution=(
        "class ValidationError(ValueError):\n"
        "    def __init__(self, field, message):\n"
        '        super().__init__(f"{field}: {message}")\n'
        "        self.field = field\n"
        "        self.message = message\n\n\n"
        "def validate_name(record):\n"
        '    if "name" not in record:\n'
        '        raise ValidationError("name", "missing")\n'
        '    if not record["name"]:\n'
        '        raise ValidationError("name", "empty")\n'
        '    return record["name"]\n\n\n'
        "def describe_record(record):\n"
        "    try:\n"
        '        return ("ok", validate_name(record))\n'
        "    except ValidationError as exc:\n"
        "        return (exc.field, exc.message)"
    ),
    explanation=(
        "Exceptions are ordinary objects, so attach whatever the handler needs to "
        "decide — field names, retry-after seconds, the offending row — instead of "
        "forcing it to regex your message. Forgetting `super().__init__` is the usual "
        "slip: the attributes work, but `str(exc)` comes out empty and the traceback "
        "tells you nothing."
    ),
    starter=(
        "class ValidationError(ValueError):\n"
        "    ...\n\n\n"
        "def validate_name(record):\n"
        "    ...\n\n\n"
        "def describe_record(record):\n"
        "    ..."
    ),
    cases=[
        Case(expected=("ok", "ada"), args=({"name": "ada"},)),
        Case(expected=("name", "missing"), args=({},)),
        Case(expected=("name", "empty"), args=({"name": ""},)),
        Case(expected=("ok", "bob"), args=({"name": "bob", "age": 3},)),
    ],
)

q(
    qid="Q-349",
    level=Level.L4,
    topic="Generators",
    kind="custom",
    entry="deep_flatten",
    constraints=["needs-generator", "needs-recursion"],
    prompt=(
        "Write `deep_flatten(values)` returning a flat **list** of every non-list "
        "item, at any depth: `deep_flatten([1, [2, [3, 4]], 5])` returns "
        "`[1, 2, 3, 4, 5]`. Only `list` counts as nesting — strings stay whole.\n\n"
        "Do it with a **generator nested inside** `deep_flatten` that walks the items "
        "and, on hitting a sub-list, delegates with `yield from deep_flatten(item)` — "
        "so the recursion runs through the outer function. The outer function returns "
        "`list(...)` of that generator.\n\n"
        "Your solution must contain `yield` and `deep_flatten` must call itself."
    ),
    hint=(
        "For each item: if it is a `list`, hand the whole sub-stream over to a "
        "recursive call; otherwise yield the item. `isinstance` decides which, and "
        "`yield from` accepts a list just as happily as a generator."
    ),
    solution=(
        "def deep_flatten(values):\n"
        "    def gen(items):\n"
        "        for item in items:\n"
        "            if isinstance(item, list):\n"
        "                yield from deep_flatten(item)\n"
        "            else:\n"
        "                yield item\n\n"
        "    return list(gen(values))"
    ),
    explanation=(
        "This is the reason `yield from` was added: without it the recursive case "
        "needs `for x in deep_flatten(item): yield x`, and every level of nesting adds "
        "another Python-level loop to every item's journey to the top. The `isinstance` "
        "guard has to be there because a string is iterable — recursing into `\"ab\"` "
        "would yield `\"a\"`, which is itself a one-character string, and the "
        "recursion never bottoms out."
    ),
    starter="def deep_flatten(values):\n    ...",
    cases=[
        Case(expected=[1, 2, 3, 4, 5], args=([1, [2, [3, 4]], 5],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=([[[[]]]],)),
        Case(expected=[1, 2, 3], args=([[1], [2, [3]]],)),
        Case(expected=["a", "b"], args=(["a", ["b"]],)),
    ],
)

q(
    qid="Q-350",
    level=Level.L4,
    topic="Context Managers",
    kind="custom",
    entry="transcript",
    constraints=["needs-with"],
    prompt=(
        "Write a class `Session(log)` modelling a resource that is only usable while "
        "open:\n\n"
        "- `__enter__` sets `self.open = True`, appends `\"open\"` to the log, returns "
        "`self`;\n"
        "- `write(text)` raises `RuntimeError` if not open, else appends `text`;\n"
        "- `__exit__` sets `self.open = False`, appends `\"close\"`, returns `False`.\n\n"
        "Then write `transcript(messages)` that creates a fresh log and a `Session`, "
        "and writes every message **inside a `with` statement**, returning the log. "
        "`transcript([\"a\"])` returns `['open', 'a', 'close']`.\n\n"
        "Your solution must use a `with` statement — calling `__enter__` and "
        "`__exit__` by hand does not count."
    ),
    hint=(
        "The `open` flag is the whole point of the design: it makes misuse outside the "
        "block raise loudly instead of half-working. `__exit__` clears it whichever "
        "way the block ends."
    ),
    solution=(
        "class Session:\n"
        "    def __init__(self, log):\n"
        "        self.log = log\n"
        "        self.open = False\n\n"
        "    def __enter__(self):\n"
        "        self.open = True\n"
        '        self.log.append("open")\n'
        "        return self\n\n"
        "    def write(self, text):\n"
        "        if not self.open:\n"
        '            raise RuntimeError("session is closed")\n'
        "        self.log.append(text)\n\n"
        "    def __exit__(self, exc_type, exc, tb):\n"
        "        self.open = False\n"
        '        self.log.append("close")\n'
        "        return False\n\n\n"
        "def transcript(messages):\n"
        "    log = []\n"
        "    session = Session(log)\n"
        "    with session:\n"
        "        for message in messages:\n"
        "            session.write(message)\n"
        "    return log"
    ),
    explanation=(
        "Guarding operations on an `open` flag is what turns a context manager from a "
        "convenience into a contract — the object refuses to be used at the wrong "
        "time, rather than silently writing to a closed handle. This is exactly why "
        "`open()` files raise `ValueError: I/O operation on closed file`, and why "
        "`with` is preferred over remembering to call `.close()`."
    ),
    starter="class Session:\n    ...\n\n\ndef transcript(messages):\n    ...",
    cases=[
        Case(expected=["open", "a", "b", "close"], args=(["a", "b"],)),
        Case(expected=["open", "close"], args=([],)),
        Case(expected=["open", "x", "close"], args=(["x"],)),
    ],
)

q(
    qid="Q-351",
    level=Level.L4,
    topic="Exceptions",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def f():\n"
        "    try:\n"
        '        raise ValueError("boom")\n'
        "    finally:\n"
        '        return "swallowed"\n\n'
        "print(f())\n\n"
        "def g():\n"
        "    try:\n"
        '        raise ValueError("boom")\n'
        "    finally:\n"
        '        print("cleanup")\n\n'
        "try:\n"
        "    g()\n"
        "except ValueError as exc:\n"
        '    print(f"caught {exc}")\n'
        "```\n\n"
        "Set `answer` to the three printed lines, in order. Neither function has an "
        "`except` clause — think about what a `return` inside `finally` does to an "
        "exception that is already on its way out."
    ),
    hint=(
        "`finally` runs while the exception is in flight, before it leaves the "
        "function. Ask what is left of that in-flight exception once `finally` "
        "performs a normal exit of its own."
    ),
    solution='answer = "swallowed\\ncleanup\\ncaught boom"',
    explanation=(
        "A `return` (or `break`, or `continue`) inside `finally` **discards the "
        "in-flight exception entirely** — `f` reports success and the `ValueError` is "
        "gone without a trace, no log, no traceback. `g` shows the normal behaviour: "
        "`finally` runs its cleanup and the exception carries on. Never put control "
        "flow in a `finally` block."
    ),
    starter="answer = ...",
    cases=[Case(expected="swallowed\ncleanup\ncaught boom")],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-352",
    level=Level.L5,
    topic="Generators",
    kind="function",
    entry="feed",
    prompt=(
        "Generators receive as well as produce. Write `accumulator()` — an infinite "
        "generator whose `yield` expression is assigned: `value = yield total`. It "
        "keeps a running `total`, treats a received `None` as `0`, and yields the "
        "total each time.\n\n"
        "Then write `feed(numbers)`: create the generator, **prime it** with one "
        "`next()`, then `send()` each number and collect the values it yields back "
        "into a **list**.\n\n"
        "`feed([1, 2, 3])` returns `[1, 3, 6]`."
    ),
    hint=(
        "`gen.send(x)` resumes the generator, makes the paused `yield` expression "
        "evaluate to `x`, and returns the next yielded value. A brand-new generator is "
        "not paused at a `yield` yet, which is why the first call has to be `next()`."
    ),
    solution=(
        "def accumulator():\n"
        "    total = 0\n"
        "    while True:\n"
        "        value = yield total\n"
        "        if value is None:\n"
        "            value = 0\n"
        "        total += value\n\n\n"
        "def feed(numbers):\n"
        "    gen = accumulator()\n"
        "    next(gen)\n"
        "    return [gen.send(n) for n in numbers]"
    ),
    explanation=(
        "`yield` is an expression, not a statement: it produces whatever `send` passed "
        "in, which turns a generator into a two-way coroutine. Priming is mandatory — "
        "`send(1)` on a fresh generator raises `TypeError: can't send non-None value "
        "to a just-started generator` — and `next(gen)` is exactly `gen.send(None)`, "
        "which is also why the `None` guard is needed."
    ),
    starter="def accumulator():\n    ...\n\n\ndef feed(numbers):\n    ...",
    cases=[
        Case(expected=[1, 3, 6], args=([1, 2, 3],)),
        Case(expected=[], args=([],)),
        Case(expected=[5], args=([5],)),
        Case(expected=[1, 0], args=([1, -1],)),
    ],
)

q(
    qid="Q-353",
    level=Level.L5,
    topic="Generators",
    kind="function",
    entry="collect",
    prompt=(
        "A generator can `return` a value, and `yield from` captures it.\n\n"
        "- `counter(values)` — yields each value, then `return`s how many it "
        "yielded.\n"
        "- `wrapper(groups)` — for each group, does `n = yield from counter(group)` "
        "and collects the `n`s; at the end `return`s that list of counts.\n"
        "- `collect(groups)` — drives `wrapper` with `next()` in a loop, gathering the "
        "yielded items, and catches `StopIteration` to read `stop.value`. Return the "
        "**tuple** `(items_list, counts_list)`.\n\n"
        "`collect([[1, 2], [3]])` returns `([1, 2, 3], [2, 1])`."
    ),
    hint=(
        "A generator's `return` value is not yielded — it is attached to the "
        "`StopIteration` that ends it, as `.value`. `yield from` unwraps that for you; "
        "at the outermost level you have to catch it yourself."
    ),
    solution=(
        "def counter(values):\n"
        "    count = 0\n"
        "    for value in values:\n"
        "        yield value\n"
        "        count += 1\n"
        "    return count\n\n\n"
        "def wrapper(groups):\n"
        "    totals = []\n"
        "    for group in groups:\n"
        "        n = yield from counter(group)\n"
        "        totals.append(n)\n"
        "    return totals\n\n\n"
        "def collect(groups):\n"
        "    gen = wrapper(groups)\n"
        "    items = []\n"
        "    while True:\n"
        "        try:\n"
        "            items.append(next(gen))\n"
        "        except StopIteration as stop:\n"
        "            return (items, stop.value)"
    ),
    explanation=(
        "`return x` in a generator is sugar for `raise StopIteration(x)`, which is why "
        "a `for` loop discards it completely — loops only see yielded values. "
        "`yield from` is the only construct that reads it, and that channel is what "
        "made generator-based coroutines possible before `async`/`await` existed."
    ),
    starter=(
        "def counter(values):\n"
        "    ...\n\n\n"
        "def wrapper(groups):\n"
        "    ...\n\n\n"
        "def collect(groups):\n"
        "    ..."
    ),
    cases=[
        Case(expected=([1, 2, 3], [2, 1]), args=([[1, 2], [3]],)),
        Case(expected=([], []), args=([],)),
        Case(expected=([], [0]), args=([[]],)),
        Case(expected=(["a", "b", "c"], [1, 2]), args=([["a"], ["b", "c"]],)),
    ],
)

q(
    qid="Q-354",
    level=Level.L5,
    topic="Iterators",
    kind="custom",
    entry="windows",
    constraints=["needs-generator", "no-builtin:zip"],
    prompt=(
        "Write `windows(iterable, size)` returning a **list of tuples**: every "
        "consecutive run of `size` items. `windows([1, 2, 3, 4], 2)` returns "
        "`[(1, 2), (2, 3), (3, 4)]`; a source shorter than `size` gives `[]`. `size` "
        "is always at least 1.\n\n"
        "The sliding itself must be done by a **generator nested inside** `windows`, "
        "with the outer function returning `list(...)` of it.\n\n"
        "It must work on a one-pass iterator: no indexing, no slicing, and no `zip` "
        "over shifted copies. Use a `collections.deque` with `maxlen`."
    ),
    hint=(
        "A `deque(maxlen=size)` drops from the left automatically when it is full, so "
        "appending is the whole sliding step. Yield a *copy* — `tuple(window)` — "
        "because the deque keeps mutating underneath you."
    ),
    solution=(
        "from collections import deque\n\n\n"
        "def windows(iterable, size):\n"
        "    def gen():\n"
        "        window = deque(maxlen=size)\n"
        "        for item in iterable:\n"
        "            window.append(item)\n"
        "            if len(window) == size:\n"
        "                yield tuple(window)\n\n"
        "    return list(gen())"
    ),
    explanation=(
        "The `maxlen` deque gives you O(1) sliding with bounded memory — the whole "
        "point, since the source may be a stream with no length. Yielding `window` "
        "itself instead of `tuple(window)` is the bug that makes every result in the "
        "output list look identical: they would all be the same mutating object. "
        "`itertools.pairwise` is the `size=2` case in the standard library."
    ),
    starter=(
        "from collections import deque\n\n\n"
        "def windows(iterable, size):\n"
        "    ..."
    ),
    cases=[
        Case(expected=[(1, 2), (2, 3), (3, 4)], args=([1, 2, 3, 4], 2)),
        Case(expected=[], args=([1, 2], 3)),
        Case(expected=[(1, 2, 3)], args=([1, 2, 3], 3)),
        Case(expected=[], args=([], 2)),
        Case(expected=[("a", "b"), ("b", "c")], args=("abc", 2)),
    ],
)

q(
    qid="Q-355",
    level=Level.L5,
    topic="Context Managers",
    kind="custom",
    entry="guard",
    constraints=["needs-with", "no-builtin:suppress"],
    prompt=(
        "Reimplement `contextlib.suppress`. Write a class `only(*exc_types)` that "
        "suppresses an exception from its block when it is an instance of any listed "
        "type, records `type(exc).__name__` on `self.caught`, and lets everything else "
        "propagate.\n\n"
        "Then write `guard(error, types)`:\n\n"
        "```python\n"
        "box = only(*types)\n"
        "with box:\n"
        "    if error is not None:\n"
        "        raise error\n"
        '    return ("ran", None)\n'
        'return ("suppressed", box.caught)\n'
        "```\n\n"
        "`guard(ValueError(\"x\"), (ValueError,))` returns `('suppressed', "
        "'ValueError')`. `only()` with no types suppresses nothing. Do not import "
        "`contextlib.suppress`."
    ),
    hint=(
        "`__exit__` gets the exception *class* as its first argument, so the membership "
        "test is `issubclass`, not `isinstance` — and it has to short-circuit on the "
        "clean path where that argument is `None`."
    ),
    solution=(
        "class only:\n"
        "    def __init__(self, *exc_types):\n"
        "        self.exc_types = exc_types\n"
        "        self.caught = None\n\n"
        "    def __enter__(self):\n"
        "        return self\n\n"
        "    def __exit__(self, exc_type, exc, tb):\n"
        "        if exc_type is not None and issubclass(exc_type, self.exc_types):\n"
        "            self.caught = exc_type.__name__\n"
        "            return True\n"
        "        return False\n\n\n"
        "def guard(error, types):\n"
        "    box = only(*types)\n"
        "    with box:\n"
        "        if error is not None:\n"
        "            raise error\n"
        '        return ("ran", None)\n'
        '    return ("suppressed", box.caught)'
    ),
    explanation=(
        "`issubclass` against a tuple handles the whole hierarchy for free, so "
        "`only(ArithmeticError)` catches a `ZeroDivisionError` exactly as an `except` "
        "clause would — and an empty tuple is always `False`, which is why `only()` "
        "correctly suppresses nothing. The reason `suppress` exists at all is that "
        "`try: ... except X: pass` is three lines whose `pass` reviewers can never "
        "tell from an accident."
    ),
    starter="class only:\n    ...\n\n\ndef guard(error, types):\n    ...",
    cases=[
        Case(expected=("ran", None), args=(None, (ValueError,))),
        Case(expected=("suppressed", "ValueError"), args=(ValueError("x"), (ValueError,))),
        Case(expected=("suppressed", "ZeroDivisionError"),
             args=(ZeroDivisionError(), (ArithmeticError,))),
        Case(expected=None, args=(KeyError("k"), (ValueError,)), raises=KeyError),
        Case(expected=None, args=(ValueError("x"), ()), raises=ValueError),
    ],
)

q(
    qid="Q-356",
    level=Level.L5,
    topic="Custom Exceptions",
    kind="function",
    entry="trace",
    prompt=(
        "Write `chain_messages(exc)` that walks an exception chain and returns the "
        "**list of `str(...)` messages**, outermost first. At each step follow "
        "`__cause__` if it is set, otherwise `__context__`, stopping at `None`.\n\n"
        "Supporting code: `parse(text)` raises `ValueError(f\"not a number: {text}\")` "
        "unless `text.isdigit()`; `load(text, chained)` catches that and raises "
        "`StepError(\"parse step failed\")` — **`from exc` when `chained` is true, and "
        "a plain `raise` when it is false**. `StepError` is your own "
        "`Exception` subclass.\n\n"
        "Write `trace(text, chained=True)` returning `(\"ok\", value)` on success, or "
        "`(\"failed\", chain_messages(exc))` when `StepError` escapes.\n\n"
        "`trace(\"abc\")` returns `('failed', ['parse step failed', 'not a number: "
        "abc'])` — and so does `trace(\"abc\", chained=False)`."
    ),
    hint=(
        "Two different dunder attributes record a chain: one you set deliberately with "
        "`from`, one Python fills in automatically whenever you raise inside an "
        "`except` block. Prefer the deliberate one when both are present."
    ),
    solution=(
        "class StepError(Exception):\n"
        "    pass\n\n\n"
        "def chain_messages(exc):\n"
        "    messages = []\n"
        "    current = exc\n"
        "    while current is not None:\n"
        "        messages.append(str(current))\n"
        "        if current.__cause__ is not None:\n"
        "            current = current.__cause__\n"
        "        else:\n"
        "            current = current.__context__\n"
        "    return messages\n\n\n"
        "def parse(text):\n"
        "    if not text.isdigit():\n"
        '        raise ValueError(f"not a number: {text}")\n'
        "    return int(text)\n\n\n"
        "def load(text, chained):\n"
        "    try:\n"
        "        return parse(text)\n"
        "    except ValueError as exc:\n"
        "        if chained:\n"
        '            raise StepError("parse step failed") from exc\n'
        '        raise StepError("parse step failed")\n\n\n'
        "def trace(text, chained=True):\n"
        "    try:\n"
        '        return ("ok", load(text, chained))\n'
        "    except StepError as exc:\n"
        '        return ("failed", chain_messages(exc))'
    ),
    explanation=(
        "`__context__` is set **automatically** for any exception raised while another "
        "is being handled, so the original is never actually lost — `from` only "
        "upgrades the relationship to a deliberate `__cause__`, which changes the "
        "wording in the traceback and signals intent. The one way to truly drop it is "
        "`raise ... from None`, which sets `__suppress_context__` and hides everything "
        "underneath."
    ),
    starter=(
        "class StepError(Exception):\n"
        "    ...\n\n\n"
        "def chain_messages(exc):\n"
        "    ...\n\n\n"
        "def parse(text):\n"
        "    ...\n\n\n"
        "def load(text, chained):\n"
        "    ...\n\n\n"
        "def trace(text, chained=True):\n"
        "    ..."
    ),
    cases=[
        Case(expected=("ok", 42), args=("42",)),
        Case(expected=("failed", ["parse step failed", "not a number: abc"]),
             args=("abc",)),
        Case(expected=("failed", ["parse step failed", "not a number: abc"]),
             args=("abc",), kwargs={"chained": False}),
        Case(expected=("failed", ["parse step failed", "not a number: "]), args=("",)),
        Case(expected=("failed", ["parse step failed", "not a number: 3.5"]),
             args=("3.5",)),
    ],
)

q(
    qid="Q-357",
    level=Level.L5,
    topic="Decorators",
    kind="function",
    entry="measure_calls",
    prompt=(
        "A decorator need not be a function. Write a **class** `Counted` whose "
        "`__init__(func)` stores the function, calls "
        "`functools.update_wrapper(self, func)`, and sets `self.calls = 0`; its "
        "`__call__` increments `self.calls` and delegates.\n\n"
        "Then write `measure_calls(values)` that defines a `@Counted`-decorated "
        "`negate(n)` **inside** the function, maps it over `values`, and returns the "
        "3-tuple `(negate.__name__, results_list, negate.calls)`.\n\n"
        "`measure_calls([1, 2])` returns `('negate', [-1, -2], 2)`."
    ),
    hint=(
        "`@Counted` on a `def` binds the name to an *instance*, so calling it goes "
        "through `__call__` and the counter is plain instance state. "
        "`functools.update_wrapper` is the non-decorator form of `functools.wraps` — "
        "it copies metadata onto an object you already have."
    ),
    solution=(
        "import functools\n\n\n"
        "class Counted:\n"
        "    def __init__(self, func):\n"
        "        functools.update_wrapper(self, func)\n"
        "        self.func = func\n"
        "        self.calls = 0\n\n"
        "    def __call__(self, *args, **kwargs):\n"
        "        self.calls += 1\n"
        "        return self.func(*args, **kwargs)\n\n\n"
        "def measure_calls(values):\n"
        "    @Counted\n"
        "    def negate(n):\n"
        "        return -n\n\n"
        "    results = [negate(v) for v in values]\n"
        "    return (negate.__name__, results, negate.calls)"
    ),
    explanation=(
        "A class-based decorator trades closures for attributes, which makes state "
        "like `calls` inspectable and resettable from outside rather than trapped in a "
        "cell — the reason `functools.lru_cache` exposes `cache_info()`. The catch is "
        "methods: an instance stored on a class is not a descriptor, so `@Counted` on "
        "a method loses `self` binding unless you also implement `__get__`."
    ),
    starter=(
        "import functools\n\n\n"
        "class Counted:\n"
        "    ...\n\n\n"
        "def measure_calls(values):\n"
        "    ..."
    ),
    cases=[
        Case(expected=("negate", [-1, -2], 2), args=([1, 2],)),
        Case(expected=("negate", [], 0), args=([],)),
        Case(expected=("negate", [0], 1), args=([0],)),
        Case(expected=("negate", [3], 1), args=([-3],)),
    ],
)

q(
    qid="Q-358",
    level=Level.L5,
    topic="Context Managers",
    kind="custom",
    entry="run_section",
    # No `no-builtin:contextmanager`: the rule matches bare *calls*, and
    # `@contextmanager` is a decorator Name, so it would never fire. The
    # prompt carries the prohibition instead.
    constraints=["needs-with", "needs-generator"],
    prompt=(
        "Capstone: build `@contextlib.contextmanager` yourself, out of a decorator, a "
        "generator and the context-manager protocol. Do not import `contextlib`.\n\n"
        "- `_CM(gen)` — a class whose `__enter__` returns `next(self.gen)`, and whose "
        "`__exit__` runs `next(self.gen, None)` on the clean path, `self.gen.close()` "
        "when the block raised, and returns `False` either way.\n"
        "- `simple_cm(func)` — a decorator (using `functools.wraps`) returning a "
        "factory that calls `func(*args, **kwargs)` and wraps the resulting generator "
        "in `_CM`.\n"
        "- `run_section(name, fail)` — defines a `@simple_cm`-decorated generator "
        "`section(events, label)` **inside itself**, which appends `f\"enter "
        "{label}\"`, then in a `try`/`finally` yields `label.upper()` and appends "
        "`f\"exit {label}\"`. Then, with a fresh `events` list: `with section(events, "
        "name) as value`, append `f\"body {value}\"`, raise `ValueError` when `fail` "
        "is true; catch that `ValueError` outside the `with` and append `\"caught\"`. "
        "Return `events`.\n\n"
        "`run_section(\"db\", False)` returns `['enter db', 'body DB', 'exit db']`; "
        "with `fail=True` a fourth entry `'caught'` follows."
    ),
    hint=(
        "`gen.close()` throws `GeneratorExit` in at the paused `yield`, which runs the "
        "generator's `finally` and then stops it — that is how cleanup happens without "
        "you re-raising anything. And `next(gen, None)` is the two-argument form that "
        "returns the default instead of raising when the generator is already finished."
    ),
    solution=(
        "import functools\n\n\n"
        "class _CM:\n"
        "    def __init__(self, gen):\n"
        "        self.gen = gen\n\n"
        "    def __enter__(self):\n"
        "        return next(self.gen)\n\n"
        "    def __exit__(self, exc_type, exc, tb):\n"
        "        if exc_type is None:\n"
        "            next(self.gen, None)\n"
        "        else:\n"
        "            self.gen.close()\n"
        "        return False\n\n\n"
        "def simple_cm(func):\n"
        "    @functools.wraps(func)\n"
        "    def factory(*args, **kwargs):\n"
        "        return _CM(func(*args, **kwargs))\n"
        "    return factory\n\n\n"
        "def run_section(name, fail):\n"
        "    @simple_cm\n"
        "    def section(events, label):\n"
        '        events.append(f"enter {label}")\n'
        "        try:\n"
        "            yield label.upper()\n"
        "        finally:\n"
        '            events.append(f"exit {label}")\n\n'
        "    events = []\n"
        "    try:\n"
        "        with section(events, name) as value:\n"
        '            events.append(f"body {value}")\n'
        "            if fail:\n"
        '                raise ValueError("boom")\n'
        "    except ValueError:\n"
        '        events.append("caught")\n'
        "    return events"
    ),
    explanation=(
        "Everything `@contextmanager` does is here: the code before the `yield` is "
        "`__enter__`, the code after is `__exit__`, and the factory exists so each "
        "`with` gets a fresh generator — reusing one would make the manager "
        "single-use. The real `contextlib` version uses `gen.throw(exc)` instead of "
        "`close()`, so the generator can *catch* the exception and suppress it; "
        "`close()` only guarantees `finally` runs, which is why this version can never "
        "swallow anything."
    ),
    starter=(
        "import functools\n\n\n"
        "class _CM:\n"
        "    ...\n\n\n"
        "def simple_cm(func):\n"
        "    ...\n\n\n"
        "def run_section(name, fail):\n"
        "    ..."
    ),
    cases=[
        Case(expected=["enter db", "body DB", "exit db"], args=("db", False)),
        Case(expected=["enter db", "body DB", "exit db", "caught"], args=("db", True)),
        Case(expected=["enter api", "body API", "exit api"], args=("api", False)),
        Case(expected=["enter ", "body ", "exit "], args=("", False)),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-09",
    title="Resilient paginated crawler",
    brief=(
        "Three of this notebook's tools, assembled into one small client.\n\n"
        "**1. `retry(times, exceptions)`** — a decorator factory. The wrapper calls "
        "the function up to `times` times, swallowing any exception in the "
        "`exceptions` tuple, and re-raises the **last** failure with a bare `raise` "
        "if every attempt fails. Use `functools.wraps`.\n\n"
        "**2. `lru(capacity)`** — a decorator factory caching results in a dict keyed "
        "by the positional args. A hit moves the key to most-recently-used "
        "(`cache[key] = cache.pop(key)`); a miss that pushes the cache over "
        "`capacity` evicts the oldest key (`next(iter(cache))`). Count hits and "
        "misses on the wrapper and expose `wrapper.stats()` returning "
        "`(hits, misses)`.\n\n"
        "**3. `paginate(fetch, start=0)`** — a generator. Starting at `cursor = "
        "start`, call `items, cursor = fetch(cursor)` and `yield from items`, stopping "
        "when the returned cursor is `None`. It must never build the full list.\n\n"
        "**Entry point `crawl(pages, fail_times, capacity, passes)`**:\n\n"
        "- `pages` is a list of pages (each a list of items); `fail_times` maps a page "
        "index to how many times fetching it fails before succeeding.\n"
        "- Define `raw_fetch(cursor)`: if that page still owes failures, decrement and "
        "raise `ConnectionError`; otherwise return `(list(page), next_cursor)` where "
        "`next_cursor` is `cursor + 1` or `None` past the last page. With no pages at "
        "all, `raw_fetch(0)` returns `([], None)`.\n"
        "- Wrap it: `fetch = lru(capacity)(retry(3, (ConnectionError,))(raw_fetch))` — "
        "caching **outside** retry, so a cached page is never re-fetched.\n"
        "- Run `list(paginate(fetch))` `passes` times, keeping the last result, and "
        "return `{\"items\": ..., \"hits\": h, \"misses\": m}`.\n\n"
        "With two pages and `passes=2`, the second pass is all hits."
    ),
    hint=(
        "Copy `fail_times` into a local dict before mutating it, and build "
        "`raw_fetch` as a closure over that copy so each `crawl` starts fresh. Put "
        "`lru` on the outside: if retry wrapped the cache instead, a cached page would "
        "still pay the retry machinery on every pass."
    ),
    solution=(
        "import functools\n\n\n"
        "def retry(times, exceptions=(Exception,)):\n"
        "    def decorate(func):\n"
        "        @functools.wraps(func)\n"
        "        def wrapper(*args, **kwargs):\n"
        "            last = None\n"
        "            for _ in range(times):\n"
        "                try:\n"
        "                    return func(*args, **kwargs)\n"
        "                except exceptions as exc:\n"
        "                    last = exc\n"
        "            raise last\n"
        "        return wrapper\n"
        "    return decorate\n\n\n"
        "def lru(capacity):\n"
        "    def decorate(func):\n"
        "        cache = {}\n\n"
        "        @functools.wraps(func)\n"
        "        def wrapper(*args):\n"
        "            if args in cache:\n"
        "                cache[args] = cache.pop(args)\n"
        "                wrapper.hits += 1\n"
        "                return cache[args]\n"
        "            wrapper.misses += 1\n"
        "            value = func(*args)\n"
        "            cache[args] = value\n"
        "            if len(cache) > capacity:\n"
        "                del cache[next(iter(cache))]\n"
        "            return value\n\n"
        "        wrapper.hits = 0\n"
        "        wrapper.misses = 0\n"
        "        wrapper.stats = lambda: (wrapper.hits, wrapper.misses)\n"
        "        return wrapper\n"
        "    return decorate\n\n\n"
        "def paginate(fetch, start=0):\n"
        "    cursor = start\n"
        "    while cursor is not None:\n"
        "        items, cursor = fetch(cursor)\n"
        "        yield from items\n\n\n"
        "def crawl(pages, fail_times, capacity, passes):\n"
        "    remaining = dict(fail_times)\n\n"
        "    def raw_fetch(cursor):\n"
        "        if remaining.get(cursor, 0) > 0:\n"
        "            remaining[cursor] -= 1\n"
        '            raise ConnectionError(f"page {cursor} unavailable")\n'
        "        page = pages[cursor] if cursor < len(pages) else []\n"
        "        nxt = cursor + 1 if cursor + 1 < len(pages) else None\n"
        "        return (list(page), nxt)\n\n"
        "    fetch = lru(capacity)(retry(3, (ConnectionError,))(raw_fetch))\n\n"
        "    items = []\n"
        "    for _ in range(passes):\n"
        "        items = list(paginate(fetch))\n"
        "    hits, misses = fetch.stats()\n"
        '    return {"items": items, "hits": hits, "misses": misses}'
    ),
    explanation=(
        "Decorator order is the design decision here: `lru(retry(fetch))` means a "
        "cached page costs nothing, while `retry(lru(fetch))` would re-enter the retry "
        "loop on every call and — worse — could cache a value produced by a partially "
        "failed sequence. The generator keeps the crawl streaming, so a million-page "
        "source costs one page of memory; and re-raising the *last* exception with a "
        "bare `raise` is what preserves the traceback of the attempt that actually "
        "gave up."
    ),
    entry="crawl",
    starter=(
        "import functools\n\n\n"
        "def retry(times, exceptions=(Exception,)):\n"
        "    ...\n\n\n"
        "def lru(capacity):\n"
        "    ...\n\n\n"
        "def paginate(fetch, start=0):\n"
        "    ...\n\n\n"
        "def crawl(pages, fail_times, capacity, passes):\n"
        "    ..."
    ),
    cases=[
        Case(expected={"items": [1, 2, 3], "hits": 0, "misses": 2},
             args=([[1, 2], [3]], {}, 4, 1)),
        Case(expected={"items": [1, 2, 3], "hits": 2, "misses": 2},
             args=([[1, 2], [3]], {}, 4, 2)),
        Case(expected={"items": ["a", "b", "c"], "hits": 0, "misses": 6},
             args=([["a"], ["b"], ["c"]], {}, 1, 2)),
        Case(expected={"items": [1], "hits": 0, "misses": 1},
             args=([[1]], {0: 2}, 2, 1)),
        Case(expected={"items": [], "hits": 0, "misses": 1},
             args=([], {}, 2, 1)),
        Case(expected=None, args=([[1]], {0: 5}, 2, 1), raises=ConnectionError),
    ],
)

NOTEBOOK = Notebook(
    number=9,
    slug="iterators_generators_decorators_context_exceptions",
    title="Iterators, Generators, Decorators, Context Managers & Exceptions",
    intro=(
        "Five features that share one idea: code that runs somewhere other than where "
        "you wrote it. An iterator suspends between items, a generator suspends "
        "mid-function, a decorator wraps a call you never see, a context manager owns "
        "the exits of a block, and an exception travels up frames until somebody "
        "claims it.\n\n"
        "This is the hardest notebook in the set, and the gotchas are the point: a "
        "generator that is empty the second time you look, a `finally` that eats an "
        "exception whole, a decorator that renames every function in your traceback.\n\n"
        "One convention throughout — the checker is strict on type, and a generator "
        "object is not a list. Whenever a question asks for a list, write the "
        "generator *and* a thin wrapper that returns `list(...)` of it."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
