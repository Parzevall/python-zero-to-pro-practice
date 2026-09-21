"""Notebook 06 - Functions, Scope & Closures (Q-187..Q-228)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-187",
    level=Level.L1,
    topic="Definition",
    kind="function",
    entry="greet",
    prompt=(
        "Write `greet(name)` that returns the string `\"Hello, \"` followed by "
        "`name` and an exclamation mark.\n\n"
        "`greet(\"Ada\")` returns `'Hello, Ada!'`. Return the string — do not print it."
    ),
    hint=(
        "`def` names the function and its parameters; `return` hands a value back to "
        "the caller. An f-string is the tidiest way to splice `name` into the middle."
    ),
    solution='def greet(name):\n    return f"Hello, {name}!"',
    explanation=(
        "Returning and printing are different jobs: `print` writes to the screen and "
        "evaluates to `None`, so a function that prints instead of returning is "
        "useless to every caller that wants the value. Build functions that return, "
        "and let the top of your program decide what to display."
    ),
    starter="def greet(name):\n    ...",
    cases=[
        Case(expected="Hello, Ada!", args=("Ada",)),
        Case(expected="Hello, Bob!", args=("Bob",)),
        Case(expected="Hello, !", args=("",)),
    ],
)

q(
    qid="Q-188",
    level=Level.L1,
    topic="Definition",
    kind="function",
    entry="rectangle",
    prompt=(
        "Write `rectangle(width, height)` that returns the **tuple** "
        "`(area, perimeter)` — the area first, then the perimeter.\n\n"
        "Area is `width * height`; perimeter is `2 * (width + height)`."
    ),
    hint=(
        "A function returns exactly one object, but that object can be a tuple. "
        "Separating two expressions with a comma after `return` builds one."
    ),
    solution=(
        "def rectangle(width, height):\n"
        "    return (width * height, 2 * (width + height))"
    ),
    explanation=(
        "Python has no 'multiple return values' — `return a, b` builds a single tuple, "
        "and `x, y = rectangle(...)` at the call site unpacks it again. Knowing it is "
        "really one tuple explains why you can also write `pair = rectangle(2, 3)` and "
        "index into it."
    ),
    starter="def rectangle(width, height):\n    ...",
    cases=[
        Case(expected=(12, 14), args=(3, 4)),
        Case(expected=(1, 4), args=(1, 1)),
        Case(expected=(0, 10), args=(0, 5)),
        Case(expected=(10.0, 13.0), args=(2.5, 4)),
    ],
)

q(
    qid="Q-189",
    level=Level.L1,
    topic="Defaults",
    kind="function",
    entry="greet_with",
    prompt=(
        "Write `greet_with(name, greeting=\"Hello\")` returning "
        "`f\"{greeting}, {name}!\"`.\n\n"
        "`greet_with(\"Ada\")` returns `'Hello, Ada!'`; `greet_with(\"Ada\", \"Hi\")` "
        "returns `'Hi, Ada!'`. The default must be used only when the caller supplies "
        "nothing — an explicitly passed empty string is still the caller's choice."
    ),
    hint=(
        "A default is written straight into the parameter list with `=`. Parameters "
        "with defaults must come after those without."
    ),
    solution=(
        "def greet_with(name, greeting=\"Hello\"):\n"
        '    return f"{greeting}, {name}!"'
    ),
    explanation=(
        "A default makes a parameter optional without a second function or a `None` "
        "check in the body. The trap the last case points at is that a default fires "
        "on *absence*, never on falsiness — writing `greeting = greeting or \"Hello\"` "
        "inside the body would quietly override the caller's deliberate `\"\"`."
    ),
    starter='def greet_with(name, greeting="Hello"):\n    ...',
    cases=[
        Case(expected="Hello, Ada!", args=("Ada",)),
        Case(expected="Hi, Ada!", args=("Ada", "Hi")),
        Case(expected="Yo, Bob!", args=("Bob",), kwargs={"greeting": "Yo"}),
        Case(expected=", Ada!", args=("Ada", "")),
    ],
)

q(
    qid="Q-190",
    level=Level.L1,
    topic="Varargs",
    kind="function",
    entry="total",
    prompt=(
        "Write `total(*numbers)` that accepts any number of positional arguments and "
        "returns their sum.\n\n"
        "`total(1, 2, 3)` is `6`, and `total()` is `0` — not `None`, and not an error."
    ),
    hint=(
        "The `*` in front of a parameter name collects every leftover positional "
        "argument into one object. That object is a sequence, so a builtin can add it "
        "up in one call."
    ),
    solution="def total(*numbers):\n    return sum(numbers)",
    explanation=(
        "`*numbers` is *packing*: the caller passes loose arguments and the function "
        "receives one container. `sum` on an empty container returns its `start` value "
        "of `0`, which is why the no-argument case needs no special handling at all."
    ),
    starter="def total(*numbers):\n    ...",
    cases=[
        Case(expected=6, args=(1, 2, 3)),
        Case(expected=0, args=()),
        Case(expected=5, args=(5,)),
        Case(expected=4.0, args=(1.5, 2.5)),
    ],
)

q(
    qid="Q-191",
    level=Level.L1,
    topic="Lambda",
    kind="function",
    entry="double",
    prompt=(
        "Bind the name `double` to a **lambda** that takes one number and returns "
        "twice it.\n\n"
        "Write it as an assignment — `double = lambda ...` — not with `def`. "
        "`double(3)` is `6`."
    ),
    hint=(
        "A lambda is one expression with no `return` keyword: the expression *is* the "
        "result. Its parameters go between `lambda` and the colon."
    ),
    solution="double = lambda n: n * 2",
    explanation=(
        "A lambda is an ordinary function object with no name of its own, which is why "
        "assigning one to a variable is something style guides argue against: `def "
        "double(n):` is the same object with a useful `__name__` in tracebacks. "
        "Lambdas earn their place inline, as the `key=` of a sort or a one-off callback."
    ),
    starter="double = ...",
    cases=[
        Case(expected=6, args=(3,)),
        Case(expected=0, args=(0,)),
        Case(expected=-4, args=(-2,)),
        Case(expected=5.0, args=(2.5,)),
    ],
)

q(
    qid="Q-192",
    level=Level.L1,
    topic="Scope",
    kind="function",
    entry="capped",
    prompt=(
        "The starter defines `LIMIT = 10` at module level. Keep that line.\n\n"
        "Write `capped(n)` that returns `n` when it is at or below `LIMIT`, and "
        "`LIMIT` otherwise. Read `LIMIT` from the module — do not add it as a "
        "parameter and do not repeat the number `10` inside the function."
    ),
    hint=(
        "A function body can read any name defined outside it without ceremony. The "
        "builtin `min` expresses 'whichever is smaller' in one call."
    ),
    solution="LIMIT = 10\n\n\ndef capped(n):\n    return min(n, LIMIT)",
    explanation=(
        "Reading an outer name needs no declaration at all — Python only asks for a "
        "keyword when you want to *assign* to one (Q-205 shows what happens when you "
        "forget). Reading module-level constants this way is normal and good; reading "
        "module-level *mutable state* is how functions become impossible to test."
    ),
    starter="LIMIT = 10\n\n\ndef capped(n):\n    ...",
    cases=[
        Case(expected=5, args=(5,)),
        Case(expected=10, args=(20,)),
        Case(expected=10, args=(10,)),
        Case(expected=-3, args=(-3,)),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-193",
    level=Level.L2,
    topic="Arguments",
    kind="function",
    entry="book",
    prompt=(
        "Write `book(title, author, year)` returning the string "
        "`f\"{title} by {author} ({year})\"`.\n\n"
        "Define it with three plain parameters. The checker calls it positionally, by "
        "keyword in a scrambled order, and with a mix of the two — all three must work "
        "without any extra effort on your part."
    ),
    hint=(
        "You do not write anything special to support keyword calls; every ordinary "
        "parameter already accepts one. The only rule is at the *call* site."
    ),
    solution=(
        "def book(title, author, year):\n"
        '    return f"{title} by {author} ({year})"'
    ),
    explanation=(
        "Parameter names are part of a function's public interface: callers may pass "
        "any of them by keyword, in any order, which is why renaming a parameter is a "
        "breaking change. At the call site the one hard rule is that positional "
        "arguments must all come before keyword ones."
    ),
    starter="def book(title, author, year):\n    ...",
    cases=[
        Case(expected="Dune by Herbert (1965)", args=("Dune", "Herbert", 1965)),
        Case(
            expected="The Dispossessed by Le Guin (1974)",
            kwargs={"author": "Le Guin", "year": 1974, "title": "The Dispossessed"},
        ),
        Case(
            expected="Neuromancer by Gibson (1984)",
            args=("Neuromancer",),
            kwargs={"year": 1984, "author": "Gibson"},
        ),
        Case(expected="It by King (1986)", args=("It", "King"), kwargs={"year": 1986}),
    ],
)

q(
    qid="Q-194",
    level=Level.L2,
    topic="Defaults",
    kind="function",
    entry="tag",
    prompt=(
        "Write `tag(name, content, cls=None)` that builds an HTML element.\n\n"
        "With no `cls`, return `f\"<{name}>{content}</{name}>\"`. When `cls` is "
        "supplied, return `f'<{name} class=\"{cls}\">{content}</{name}>'`.\n\n"
        "'Supplied' means the caller passed *something* — including the empty string, "
        "which must still produce `class=\"\"`."
    ),
    hint=(
        "`None` is the standard 'nothing was given' marker. Test for it with the "
        "identity operator, not with truthiness — the last case is the reason."
    ),
    solution=(
        "def tag(name, content, cls=None):\n"
        "    if cls is None:\n"
        '        return f"<{name}>{content}</{name}>"\n'
        "    return f'<{name} class=\"{cls}\">{content}</{name}>'"
    ),
    explanation=(
        "`None` as a default sentinel lets a function tell *absent* apart from *falsy* "
        "— `if not cls:` would collapse the two and throw away a deliberate empty "
        "class. This is the same distinction as Q-189, and it becomes essential in "
        "Q-207 where `None` also protects you from a shared mutable default."
    ),
    starter="def tag(name, content, cls=None):\n    ...",
    cases=[
        Case(expected="<p>hi</p>", args=("p", "hi")),
        Case(expected='<p class="lead">hi</p>', args=("p", "hi", "lead")),
        Case(expected='<div class="box">x</div>', args=("div", "x"), kwargs={"cls": "box"}),
        Case(expected='<p class="">hi</p>', args=("p", "hi", "")),
    ],
)

q(
    qid="Q-195",
    level=Level.L2,
    topic="Varargs",
    kind="function",
    entry="settings",
    prompt=(
        "Write `settings(**options)` that accepts any keyword arguments and returns a "
        "**list of strings** `\"key=value\"`, sorted alphabetically by key.\n\n"
        "`settings(b=2, a=1)` returns `['a=1', 'b=2']`. With no arguments, return `[]`."
    ),
    hint=(
        "`**` in a parameter list collects leftover *keyword* arguments into a "
        "mapping. Sorting its `.items()` orders by key, because tuples compare "
        "element by element."
    ),
    solution=(
        "def settings(**options):\n"
        '    return [f"{k}={v}" for k, v in sorted(options.items())]'
    ),
    explanation=(
        "`**options` arrives as a plain `dict` — a fresh one on every call, so "
        "mutating it cannot affect the caller. It preserves the order the keywords "
        "were written in, which is why sorting here is a deliberate choice rather than "
        "something the language did for you."
    ),
    starter="def settings(**options):\n    ...",
    cases=[
        Case(expected=["a=1", "b=2"], kwargs={"b": 2, "a": 1}),
        Case(expected=[], kwargs={}),
        Case(expected=["debug=True"], kwargs={"debug": True}),
        Case(expected=["m=1.5", "z=s"], kwargs={"z": "s", "m": 1.5}),
    ],
)

q(
    qid="Q-196",
    level=Level.L2,
    topic="Definition",
    kind="function",
    entry="min_max",
    prompt=(
        "Write `min_max(values)` that returns the tuple `(smallest, largest)` of a "
        "list of numbers.\n\n"
        "For an empty list return `(None, None)` — a tuple of two `None`s, not a bare "
        "`None`, so the caller can always unpack two names from the result."
    ),
    hint=(
        "Two builtins already find the ends. The whole question is the guard clause "
        "that has to come first, because both of them raise on an empty sequence."
    ),
    solution=(
        "def min_max(values):\n"
        "    if not values:\n"
        "        return (None, None)\n"
        "    return (min(values), max(values))"
    ),
    explanation=(
        "Keeping the return *shape* constant across every path is what lets callers "
        "write `lo, hi = min_max(xs)` unconditionally; a function that sometimes "
        "returns a pair and sometimes a bare `None` pushes a type check onto everyone "
        "who calls it. An early `return` for the empty case also keeps the happy path "
        "unindented."
    ),
    starter="def min_max(values):\n    ...",
    cases=[
        Case(expected=(1, 3), args=([3, 1, 2],)),
        Case(expected=(None, None), args=([],)),
        Case(expected=(5, 5), args=([5],)),
        Case(expected=(-9, -1), args=([-1, -9],)),
    ],
)

q(
    qid="Q-197",
    level=Level.L2,
    topic="Scope",
    kind="function",
    entry="scopes",
    prompt=(
        "The starter defines `SETTING = \"global\"` at module level. Keep it.\n\n"
        "Write `scopes(value)` containing two inner functions:\n\n"
        "- `local_only()` assigns `SETTING = value` and returns `SETTING`;\n"
        "- `reader()` returns `SETTING` without assigning to it.\n\n"
        "Return the 3-tuple `(local_only(), reader(), SETTING)`. Do not use `global` "
        "or `nonlocal` anywhere."
    ),
    hint=(
        "Ask what an assignment statement does to a name's *scope*, not just to its "
        "value. The third element of the tuple tells you whether anything outside the "
        "inner function noticed."
    ),
    solution=(
        'SETTING = "global"\n\n\n'
        "def scopes(value):\n"
        "    def local_only():\n"
        "        SETTING = value\n"
        "        return SETTING\n\n"
        "    def reader():\n"
        "        return SETTING\n\n"
        "    return (local_only(), reader(), SETTING)"
    ),
    explanation=(
        "Assigning to a name anywhere in a function body makes that name local for the "
        "*whole* body, so `local_only` creates and returns its own private `SETTING` "
        "and the module-level one is untouched. `reader` never assigns, so it falls "
        "through to the module scope — the same name, resolved two different ways, "
        "decided entirely at compile time by the presence of an assignment."
    ),
    starter='SETTING = "global"\n\n\ndef scopes(value):\n    ...',
    cases=[
        Case(expected=("local", "global", "global"), args=("local",)),
        Case(expected=("x", "global", "global"), args=("x",)),
        Case(expected=("", "global", "global"), args=("",)),
    ],
)

q(
    qid="Q-198",
    level=Level.L2,
    topic="Closures",
    kind="function",
    entry="add_with",
    prompt=(
        "Write `add_with(n, x)`. Inside it, define an inner function `adder(value)` "
        "that returns `value + n` — reading `n` from the enclosing call, **not** "
        "taking it as a parameter.\n\n"
        "Then call `adder(x)` and return the result. `add_with(10, 5)` is `15`."
    ),
    hint=(
        "A function defined inside another can see the outer function's local names. "
        "`adder` takes exactly one parameter; `n` reaches it some other way."
    ),
    solution=(
        "def add_with(n, x):\n"
        "    def adder(value):\n"
        "        return value + n\n\n"
        "    return adder(x)"
    ),
    explanation=(
        "An inner function that reads a name from its enclosing function is a "
        "*closure*: `n` stays reachable because the inner function keeps a reference "
        "to the cell holding it, not a copy of its value. That distinction is invisible "
        "here and is the whole of Q-204."
    ),
    starter="def add_with(n, x):\n    ...",
    cases=[
        Case(expected=15, args=(10, 5)),
        Case(expected=7, args=(0, 7)),
        Case(expected=0, args=(-3, 3)),
        Case(expected=3.5, args=(2, 1.5)),
    ],
)

q(
    qid="Q-199",
    level=Level.L2,
    topic="Lambda",
    kind="function",
    entry="sort_by_last",
    prompt=(
        "Write `sort_by_last(names)` that returns a **new** list of the strings sorted "
        "by their last character.\n\n"
        "Use `sorted` with a `key=` lambda. Every string is non-empty. Names whose "
        "last character ties must keep their original relative order."
    ),
    hint=(
        "`key=` takes a function that is called once per item and returns the value to "
        "order by. Negative indexing reaches the last character."
    ),
    solution="def sort_by_last(names):\n    return sorted(names, key=lambda s: s[-1])",
    explanation=(
        "`key=` transforms each item for comparison purposes only — the original "
        "objects are what come back, and each key is computed exactly once rather than "
        "on every comparison. Python's sort is *stable*, so the tie-break in the prompt "
        "is a guarantee of the language, not something you have to arrange."
    ),
    starter="def sort_by_last(names):\n    ...",
    cases=[
        Case(expected=["ada", "bob", "zed"], args=(["bob", "ada", "zed"],)),
        Case(expected=["ab", "xy"], args=(["xy", "ab"],)),
        Case(expected=[], args=([],)),
        Case(expected=["cc", "ac", "bc"], args=(["cc", "ac", "bc"],)),
    ],
)

q(
    qid="Q-200",
    level=Level.L2,
    topic="First-Class",
    kind="function",
    entry="apply_twice",
    prompt=(
        "Write `apply_twice(fn, x)` that calls `fn` on `x`, then calls `fn` again on "
        "that result, and returns the second result.\n\n"
        "`apply_twice(abs, -5)` is `5`. `fn` is any one-argument callable — do not "
        "assume it is a number function."
    ),
    hint=(
        "`fn` is a parameter holding a function object. Adding `(...)` after the name "
        "is what calls it; leaving the parentheses off just refers to it."
    ),
    solution="def apply_twice(fn, x):\n    return fn(fn(x))",
    explanation=(
        "Functions are ordinary objects: they can be passed in, stored in lists and "
        "dicts, and returned. The single most common beginner slip is writing "
        "`fn()` in the parameter list or passing `fn(x)` where `fn` was wanted — the "
        "name is the function, the parentheses are the call."
    ),
    starter="def apply_twice(fn, x):\n    ...",
    cases=[
        Case(expected=5, args=(abs, -5)),
        Case(expected="ABC", args=(str.upper, "abc")),
        Case(expected=1.5, args=(float, "1.5")),
        Case(expected="hi", args=(str.strip, "  hi  ")),
    ],
)

q(
    qid="Q-201",
    level=Level.L2,
    topic="Arguments",
    kind="function",
    entry="repeat",
    prompt=(
        "Write `repeat(text, times)` that returns `text` repeated `times` times.\n\n"
        "Both parameters are **required** — give neither of them a default. "
        "`repeat(\"ab\", 3)` is `'ababab'`, and calling `repeat(\"ab\")` must raise "
        "`TypeError`.\n\n"
        "Note: `check()` tests the failure too. Try `repeat(\"ab\")` in a cell yourself."
    ),
    hint=(
        "You do not write any code to produce that `TypeError` — it comes from the "
        "signature. The temptation to resist is 'helpfully' defaulting `times` to `1`."
    ),
    solution="def repeat(text, times):\n    return text * times",
    explanation=(
        "Python checks the argument count at call time and raises `TypeError` before "
        "your body runs, which makes a missing argument a loud, immediate failure "
        "instead of a silent wrong answer. Adding a default to silence such an error "
        "does not fix the caller's bug; it hides it."
    ),
    starter="def repeat(text, times):\n    ...",
    cases=[
        Case(expected="ababab", args=("ab", 3)),
        Case(expected="", args=("x", 0)),
        Case(expected="hi", args=("hi", 1)),
        Case(expected=None, args=("ab",), raises=TypeError),
        Case(expected=None, args=("ab", 2, 9), raises=TypeError),
    ],
)

q(
    qid="Q-202",
    level=Level.L2,
    topic="Varargs",
    kind="function",
    entry="describe_args",
    prompt=(
        "Write `describe_args(*args)` that returns the 3-tuple "
        "`(type_name, count, as_list)` where:\n\n"
        "- `type_name` is the name of `args`'s type, as a string;\n"
        "- `count` is how many arguments arrived;\n"
        "- `as_list` is `args` converted to a `list`.\n\n"
        "The checker is strict on type, so the third element must really be a list."
    ),
    hint=(
        "Do not guess the first element — ask the object with `type(...).__name__`. "
        "The answer is the same for every call, including the empty one."
    ),
    solution=(
        "def describe_args(*args):\n"
        "    return (type(args).__name__, len(args), list(args))"
    ),
    explanation=(
        "`*args` packs into a **tuple**, never a list, so `args.append(x)` is an "
        "`AttributeError` and `args + [x]` is a `TypeError` — convert first if you "
        "need to mutate. Immutability here is deliberate: the packed arguments belong "
        "to this call and nothing should be able to rewrite them behind the caller's back."
    ),
    starter="def describe_args(*args):\n    ...",
    cases=[
        Case(expected=("tuple", 3, [1, 2, 3]), args=(1, 2, 3)),
        Case(expected=("tuple", 0, []), args=()),
        Case(expected=("tuple", 1, ["a"]), args=("a",)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-203",
    level=Level.L3,
    topic="Defaults",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def add_item(item, acc=[]):\n"
        "    acc.append(item)\n"
        "    return acc\n\n"
        "print(add_item(1))\n"
        "print(add_item(2))\n"
        "print(add_item(3, []))\n"
        "```\n\n"
        "Set `answer` to the three printed lines, e.g. `answer = \"[1]\\n[2]\\n[3]\"`."
    ),
    hint=(
        "Ask *when* the expression `[]` in the parameter list is evaluated: once, or "
        "once per call? The third call answers a different question from the first two."
    ),
    solution='answer = "[1]\\n[1, 2]\\n[3]"',
    explanation=(
        "Default values are evaluated **once**, when the `def` statement runs, and the "
        "resulting object is reused by every call that omits the argument — so one "
        "list is shared across calls and grows forever. This is the single most famous "
        "Python gotcha; the fix is `def add_item(item, acc=None)` plus `if acc is None: "
        "acc = []`, which Q-207 asks you to write."
    ),
    starter="answer = ...",
    cases=[Case(expected="[1]\n[1, 2]\n[3]")],
)

q(
    qid="Q-204",
    level=Level.L3,
    topic="Closures",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "funcs = [lambda: i for i in range(3)]\n"
        "print([f() for f in funcs])\n\n"
        "fixed = [lambda i=i: i for i in range(3)]\n"
        "print([f() for f in fixed])\n"
        "```\n\n"
        "Set `answer` to the two printed lines, e.g. `answer = \"[0, 1, 2]\\n[0, 1, 2]\"`."
    ),
    hint=(
        "A closure keeps a reference to the *variable*, not to the value it held when "
        "the lambda was created. Ask what `i` holds by the time anything is called. "
        "The second line changes `i` from a captured name into something else entirely."
    ),
    solution='answer = "[2, 2, 2]\\n[0, 1, 2]"',
    explanation=(
        "Closures capture **late**: all three lambdas share the one `i` cell, the loop "
        "leaves it at `2`, and only then does anyone call them. The `i=i` version side-"
        "steps the closure completely by evaluating `i` at definition time and storing "
        "it as a default — which works precisely because of the 'evaluated once' rule "
        "from Q-203. This bites hardest when building callbacks or handlers in a loop."
    ),
    starter="answer = ...",
    cases=[Case(expected="[2, 2, 2]\n[0, 1, 2]")],
)

q(
    qid="Q-205",
    level=Level.L3,
    topic="Scope",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "count = 10\n\n"
        "def bump():\n"
        "    print(count)\n"
        "    count = count + 1\n\n"
        "try:\n"
        "    bump()\n"
        "except UnboundLocalError:\n"
        '    print("UnboundLocalError")\n'
        "```\n\n"
        "Set `answer` to everything printed. Think carefully about whether the `print` "
        "on the first line of `bump` produces any output at all."
    ),
    hint=(
        "Scope is decided when the function is *compiled*, not line by line as it "
        "runs. One assignment anywhere in the body is enough to settle it for the "
        "whole body."
    ),
    solution='answer = "UnboundLocalError"',
    explanation=(
        "Because `count` is assigned somewhere in `bump`, the compiler marks it local "
        "for the entire function — so the `print` on the line *above* the assignment "
        "already looks up a local that has no value yet, and raises before printing "
        "anything. The module-level `count` is never consulted. The fix is `global "
        "count` (Q-208) or, far better, passing the value in and returning the new one."
    ),
    starter="answer = ...",
    cases=[Case(expected="UnboundLocalError")],
)

q(
    qid="Q-206",
    level=Level.L3,
    topic="Varargs",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def f(*args, **kwargs):\n"
        "    print(type(args).__name__, type(kwargs).__name__)\n"
        "    print(args)\n"
        "    print(kwargs)\n\n"
        'f(1, 2, mode="fast")\n'
        "```\n\n"
        "Set `answer` to the three printed lines. Reproduce the second and third lines "
        "exactly as Python would display those objects — punctuation included."
    ),
    hint=(
        "Two different containers, and only one of them is mutable. Remember how "
        "Python prints a two-element tuple, and which quote style `repr` prefers for "
        "strings inside a container."
    ),
    solution="answer = \"tuple dict\\n(1, 2)\\n{'mode': 'fast'}\"",
    explanation=(
        "`*args` is always a `tuple` and `**kwargs` always a `dict`, whatever the "
        "caller wrote. `print` shows a container by calling `repr` on its contents, "
        "which is why the inner string appears quoted — the same reason a dict of "
        "strings never prints the way an f-string of them would."
    ),
    starter="answer = ...",
    cases=[Case(expected="tuple dict\n(1, 2)\n{'mode': 'fast'}")],
)

q(
    qid="Q-207",
    level=Level.L3,
    topic="Defaults",
    kind="function",
    entry="append_to",
    prompt=(
        "Fix the bug from Q-203. Write `append_to(item, target=None)` that appends "
        "`item` to `target` and returns `target`.\n\n"
        "When the caller supplies no `target`, work on a **fresh** list every call — "
        "so `append_to(1)` is `[1]` and a later `append_to(2)` is `[2]`, never "
        "`[1, 2]`. When a list is supplied, append to that list in place."
    ),
    hint=(
        "The default must be an immutable marker rather than the container itself. "
        "Build the real container in the body, guarded by an identity test."
    ),
    solution=(
        "def append_to(item, target=None):\n"
        "    if target is None:\n"
        "        target = []\n"
        "    target.append(item)\n"
        "    return target"
    ),
    explanation=(
        "`None` is immutable and unique, so using it as the default means the mutable "
        "list is created fresh inside the body on each call. Use `is None` rather than "
        "`if not target:` — an empty list the caller deliberately passed is falsy too, "
        "and replacing it would silently discard their object instead of filling it."
    ),
    starter="def append_to(item, target=None):\n    ...",
    cases=[
        Case(expected=[1], args=(1,)),
        Case(expected=[2], args=(2,)),
        Case(expected=[0, 3], args=(3, [0])),
        Case(expected=[4], args=(4, [])),
    ],
)

q(
    qid="Q-208",
    level=Level.L3,
    topic="Scope",
    kind="function",
    entry="bump_n",
    prompt=(
        "The starter defines `hits = 0` at module level. Write two functions:\n\n"
        "- `bump()` increments the module-level `hits` by one and returns its new "
        "value — it takes no arguments;\n"
        "- `bump_n(n)` resets `hits` to `0`, then calls `bump()` `n` times and returns "
        "the list of values it produced.\n\n"
        "`bump_n(3)` returns `[1, 2, 3]`. Both functions need the `global` keyword."
    ),
    hint=(
        "Without a declaration, `hits += 1` would make `hits` local and raise the error "
        "from Q-205. The keyword goes on its own line at the top of the body."
    ),
    solution=(
        "hits = 0\n\n\n"
        "def bump():\n"
        "    global hits\n"
        "    hits += 1\n"
        "    return hits\n\n\n"
        "def bump_n(n):\n"
        "    global hits\n"
        "    hits = 0\n"
        "    return [bump() for _ in range(n)]"
    ),
    explanation=(
        "`global` does not create anything — it tells the compiler that assignments to "
        "this name inside the body should retarget the module-level binding instead of "
        "making a local. That it works does not make it a good idea: module state "
        "shared this way is why `bump_n` has to reset `hits` first, and why two callers "
        "in different parts of a program can silently corrupt each other's counts."
    ),
    starter="hits = 0\n\n\ndef bump():\n    ...\n\n\ndef bump_n(n):\n    ...",
    cases=[
        Case(expected=[1, 2, 3], args=(3,)),
        Case(expected=[], args=(0,)),
        Case(expected=[1], args=(1,)),
        Case(expected=[1, 2], args=(2,)),
    ],
)

q(
    qid="Q-209",
    level=Level.L3,
    topic="Scope",
    kind="function",
    entry="run_counter",
    prompt=(
        "Write a factory `make_counter()` that returns a function `tick`. Each call to "
        "`tick()` returns `1`, then `2`, then `3`, and so on — the count lives in "
        "`make_counter`'s local scope and `tick` updates it with `nonlocal`.\n\n"
        "Then write `run_counter(n)` that builds **one** counter, calls it `n` times, "
        "and returns the list of values. `run_counter(3)` is `[1, 2, 3]`. Use no "
        "module-level state and no `global`."
    ),
    hint=(
        "`nonlocal` is the enclosing-function counterpart to `global`. Note that "
        "`run_counter` must call the factory once and reuse the result, not call the "
        "factory inside the loop."
    ),
    solution=(
        "def make_counter():\n"
        "    count = 0\n\n"
        "    def tick():\n"
        "        nonlocal count\n"
        "        count += 1\n"
        "        return count\n\n"
        "    return tick\n\n\n"
        "def run_counter(n):\n"
        "    tick = make_counter()\n"
        "    return [tick() for _ in range(n)]"
    ),
    explanation=(
        "`nonlocal` rebinds a name in the nearest enclosing *function* scope, which is "
        "what turns a closure from read-only into private mutable state. Every call to "
        "`make_counter` creates a brand-new `count` cell, so two counters never "
        "interfere — the property the `global` version in Q-208 cannot offer."
    ),
    starter="def make_counter():\n    ...\n\n\ndef run_counter(n):\n    ...",
    cases=[
        Case(expected=[1, 2, 3], args=(3,)),
        Case(expected=[], args=(0,)),
        Case(expected=[1], args=(1,)),
        Case(expected=[1, 2, 3, 4, 5], args=(5,)),
    ],
)

q(
    qid="Q-210",
    level=Level.L3,
    topic="Arguments",
    kind="function",
    entry="connect",
    prompt=(
        "Write `connect(host, *, port=443, secure=True)` returning the 3-tuple "
        "`(host, port, secure)`.\n\n"
        "The bare `*` makes `port` and `secure` **keyword-only**: "
        "`connect(\"a.com\", 80)` must raise `TypeError`, while "
        "`connect(\"a.com\", port=80)` works.\n\n"
        "Note: `check()` tests the failure too."
    ),
    hint=(
        "Everything written after a bare `*` in the parameter list can only be passed "
        "by name. You write no validation code — the signature enforces it."
    ),
    solution=(
        "def connect(host, *, port=443, secure=True):\n"
        "    return (host, port, secure)"
    ),
    explanation=(
        "Keyword-only parameters kill the unreadable call site: `connect(h, 80, False)` "
        "tells a reviewer nothing, `connect(h, port=80, secure=False)` tells them "
        "everything. They also let you add or reorder options later without breaking "
        "callers, which is why most standard-library functions with flags use them."
    ),
    starter='def connect(host, *, port=443, secure=True):\n    ...',
    cases=[
        Case(expected=("a.com", 443, True), args=("a.com",)),
        Case(expected=("a.com", 80, True), args=("a.com",), kwargs={"port": 80}),
        Case(
            expected=("a.com", 443, False),
            args=("a.com",),
            kwargs={"secure": False},
        ),
        Case(expected=None, args=("a.com", 80), raises=TypeError),
    ],
)

q(
    qid="Q-211",
    level=Level.L3,
    topic="Arguments",
    kind="function",
    entry="clamp",
    prompt=(
        "Write `clamp(value, lo, hi, /)` that returns `value` pushed into the range "
        "`lo..hi`: `lo` when it is below, `hi` when it is above, `value` otherwise.\n\n"
        "The trailing `/` makes all three **positional-only**, so `clamp(5, 0, hi=10)` "
        "must raise `TypeError`.\n\n"
        "Note: `check()` tests the failure too."
    ),
    hint=(
        "Everything written *before* a `/` can only be passed positionally — it is the "
        "mirror image of the bare `*`. The body itself is one nested pair of builtins."
    ),
    solution="def clamp(value, lo, hi, /):\n    return min(max(value, lo), hi)",
    explanation=(
        "Positional-only parameters keep their names out of your public interface, so "
        "you can rename them freely without breaking anyone — which is exactly why "
        "builtins like `len(obj)` and `abs(x)` have always behaved this way. Reach for "
        "`/` when the names are meaningless to callers, and `*` (Q-210) when they are "
        "the whole point."
    ),
    starter="def clamp(value, lo, hi, /):\n    ...",
    cases=[
        Case(expected=5, args=(5, 0, 10)),
        Case(expected=0, args=(-1, 0, 10)),
        Case(expected=10, args=(99, 0, 10)),
        Case(expected=0, args=(0, 0, 10)),
        Case(expected=None, args=(5, 0), kwargs={"hi": 10}, raises=TypeError),
    ],
)

q(
    qid="Q-212",
    level=Level.L3,
    topic="Varargs",
    kind="custom",
    entry="call_logged",
    constraints=["max-lines:6", "no-builtin:eval"],
    prompt=(
        "Write `call_logged(fn, args, kwargs)` where `args` is a tuple and `kwargs` a "
        "dict.\n\n"
        "Inside it define an inner `forward(*a, **kw)` that passes everything straight "
        "through to `fn` and returns the result, then call `forward` with `args` and "
        "`kwargs` **unpacked** into it and return that.\n\n"
        "The body must be at most 6 lines, and you may not use `eval`."
    ),
    hint=(
        "The same `*` and `**` you used to *pack* in a definition *unpack* at a call "
        "site. `forward` must accept anything, so its signature packs and its body "
        "unpacks again."
    ),
    solution=(
        "def call_logged(fn, args, kwargs):\n"
        "    def forward(*a, **kw):\n"
        "        return fn(*a, **kw)\n\n"
        "    return forward(*args, **kwargs)"
    ),
    explanation=(
        "`*`/`**` are two operations wearing one syntax: in a `def` they pack loose "
        "arguments into a tuple and dict, at a call they explode a tuple and dict back "
        "into loose arguments. `def wrapper(*a, **kw): return fn(*a, **kw)` is the "
        "universal pass-through, and it is the skeleton of every decorator you will "
        "ever write (Q-228)."
    ),
    starter="def call_logged(fn, args, kwargs):\n    ...",
    cases=[
        Case(expected=7, args=(max, (3, 7), {})),
        Case(expected=[3, 2, 1], args=(sorted, ([1, 3, 2],), {"reverse": True})),
        Case(expected=2.57, args=(round, (2.567,), {"ndigits": 2})),
        Case(expected={"a": 1}, args=(dict, (), {"a": 1})),
    ],
)

q(
    qid="Q-213",
    level=Level.L3,
    topic="Lambda",
    kind="custom",
    entry="scale_all",
    constraints=["needs-comprehension", "no-builtin:map"],
    prompt=(
        "Write `scale_all(factor, values)` that returns a new list with every item "
        "multiplied by `factor`.\n\n"
        "Build it in two steps: bind a lambda that closes over `factor` to a local "
        "name, then apply it to each item inside a **list comprehension**. No `for` "
        "statement and no `map`."
    ),
    hint=(
        "The lambda takes one parameter, the item; `factor` reaches it from the "
        "enclosing function. The comprehension then calls that local name per item."
    ),
    solution=(
        "def scale_all(factor, values):\n"
        "    scale = lambda v: v * factor\n"
        "    return [scale(v) for v in values]"
    ),
    explanation=(
        "The lambda is a closure over `factor`, so one object encodes both the "
        "operation and its configuration — that is the whole idea behind the validator "
        "factories in this notebook's project. The comprehension is preferred over "
        "`map(scale, values)` because it already produces a list and reads left to "
        "right without a second function to look up."
    ),
    starter="def scale_all(factor, values):\n    ...",
    cases=[
        Case(expected=[2, 4, 6], args=(2, [1, 2, 3])),
        Case(expected=[0, 0], args=(0, [1, 2])),
        Case(expected=[], args=(3, [])),
        Case(expected=[-5], args=(-1, [5])),
    ],
)

q(
    qid="Q-214",
    level=Level.L3,
    topic="First-Class",
    kind="function",
    entry="dispatch",
    prompt=(
        "Write `dispatch(op, a, b)` that performs an arithmetic operation named by the "
        "string `op`: `\"add\"`, `\"sub\"` or `\"mul\"`.\n\n"
        "Build a **dict mapping each name to a lambda** and look the operation up — no "
        "`if`/`elif` chain. For any unknown `op`, return `None`."
    ),
    hint=(
        "Store the functions themselves as the dict's values, without calling them. "
        "A lookup method that returns a default is what turns the unknown case into "
        "`None` instead of a `KeyError`."
    ),
    solution=(
        "def dispatch(op, a, b):\n"
        "    table = {\n"
        '        "add": lambda x, y: x + y,\n'
        '        "sub": lambda x, y: x - y,\n'
        '        "mul": lambda x, y: x * y,\n'
        "    }\n"
        "    fn = table.get(op)\n"
        "    if fn is None:\n"
        "        return None\n"
        "    return fn(a, b)"
    ),
    explanation=(
        "A dispatch table replaces a growing `if`/`elif` ladder with one constant-time "
        "lookup, and adding an operation becomes a one-line data change rather than a "
        "control-flow edit. The thing to get right is storing `lambda x, y: x + y` and "
        "not `x + y` — the value must be the *function*, uncalled, or the dict would "
        "have to evaluate every branch up front."
    ),
    starter="def dispatch(op, a, b):\n    ...",
    cases=[
        Case(expected=5, args=("add", 2, 3)),
        Case(expected=-1, args=("sub", 2, 3)),
        Case(expected=6, args=("mul", 2, 3)),
        Case(expected=None, args=("div", 2, 3)),
    ],
)

q(
    qid="Q-215",
    level=Level.L3,
    topic="Closures",
    kind="function",
    entry="multipliers",
    prompt=(
        "Write `multipliers(n, x)` that builds a list of `n` functions — the first "
        "multiplies by `0`, the second by `1`, and so on up to `n - 1` — then returns "
        "the list of results of calling each one on `x`.\n\n"
        "`multipliers(3, 2)` returns `[0, 2, 4]`. Each function must capture **its "
        "own** factor: the naive version returns `[4, 4, 4]`, and that is the bug to "
        "avoid."
    ),
    hint=(
        "Q-204 showed why a plain captured loop variable gives every function the same "
        "final value, and it also showed the one-token trick that freezes the value at "
        "definition time."
    ),
    solution=(
        "def multipliers(n, x):\n"
        "    funcs = [lambda v, k=k: v * k for k in range(n)]\n"
        "    return [f(x) for f in funcs]"
    ),
    explanation=(
        "`k=k` evaluates the loop variable *now* and stores the result as a per-function "
        "default, so each function gets its own frozen copy instead of sharing one live "
        "cell. `functools.partial(operator.mul, k)` does the same job without the "
        "shadowing trick and is what to reach for in production code."
    ),
    starter="def multipliers(n, x):\n    ...",
    cases=[
        Case(expected=[0, 2, 4], args=(3, 2)),
        Case(expected=[0], args=(1, 5)),
        Case(expected=[], args=(0, 9)),
        Case(expected=[0, 1, 2, 3], args=(4, 1)),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-216",
    level=Level.L4,
    topic="Scope",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'x = "module"\n\n'
        "def outer():\n"
        '    x = "outer"\n\n'
        "    def plain():\n"
        '        x = "inner"\n\n'
        "    def use_nonlocal():\n"
        "        nonlocal x\n"
        '        x = "nonlocal"\n\n'
        "    def use_global():\n"
        "        global x\n"
        '        x = "global"\n\n'
        "    plain()\n"
        "    print(x)\n"
        "    use_nonlocal()\n"
        "    print(x)\n"
        "    use_global()\n"
        "    print(x)\n\n"
        "outer()\n"
        "print(x)\n"
        "```\n\n"
        "Set `answer` to the four printed lines."
    ),
    hint=(
        "Three functions assign to the same name and each reaches a different binding. "
        "The last `print` runs at module level, so ask which of the three assignments "
        "could possibly have touched that one."
    ),
    solution='answer = "outer\\nnonlocal\\nnonlocal\\nglobal"',
    explanation=(
        "Plain assignment creates a local and is invisible outside; `nonlocal` rebinds "
        "the nearest enclosing function's variable; `global` skips every function scope "
        "and goes straight to the module. Note that `use_global` never touched "
        "`outer`'s `x`, which is why the third line still reads `nonlocal` — the two "
        "keywords address different bindings that merely share a name."
    ),
    starter="answer = ...",
    cases=[Case(expected="outer\nnonlocal\nnonlocal\nglobal")],
)

q(
    qid="Q-217",
    level=Level.L4,
    topic="Defaults",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "items = [1, 2]\n\n"
        "def show(data=items):\n"
        "    print(data)\n\n"
        "items.append(3)\n"
        "show()\n"
        "items = [9]\n"
        "show()\n"
        "```\n\n"
        "Set `answer` to the two printed lines. They are not the same as each other "
        "by accident — decide what the default is actually bound to."
    ),
    hint=(
        "The default was evaluated once, at `def` time, and what it captured was an "
        "object rather than the name `items`. One of the two statements between the "
        "calls mutates that object; the other points the name somewhere new."
    ),
    solution='answer = "[1, 2, 3]\\n[1, 2, 3]"',
    explanation=(
        "The default captured the list *object*, so `items.append(3)` — a mutation of "
        "that same object — is visible through it, while `items = [9]` merely rebinds "
        "the module-level name and leaves the default pointing at the old list. This "
        "is the mutable-default trap of Q-203 seen from the other side, and the reason "
        "defaults should be immutable values or `None`."
    ),
    starter="answer = ...",
    cases=[Case(expected="[1, 2, 3]\n[1, 2, 3]")],
)

q(
    qid="Q-218",
    level=Level.L4,
    topic="Closures",
    kind="function",
    entry="memo_calls",
    prompt=(
        "Write `memo_calls(values)` that squares each number in `values`, caching "
        "results so a repeated input is never recomputed.\n\n"
        "Inside, define `square(n)` that closes over a `cache` dict and a `hits` "
        "counter — increment `hits` with `nonlocal` every time the cache already holds "
        "the answer.\n\n"
        "Return the tuple `(results, hits)`: the list of squares in input order, and "
        "the number of cache hits. `memo_calls([2, 3, 2])` returns `([4, 9, 4], 1)`."
    ),
    hint=(
        "The dict is mutated, never reassigned, so it needs no declaration; the integer "
        "counter is rebound on every hit, so it does. That asymmetry is the whole point."
    ),
    solution=(
        "def memo_calls(values):\n"
        "    cache = {}\n"
        "    hits = 0\n\n"
        "    def square(n):\n"
        "        nonlocal hits\n"
        "        if n in cache:\n"
        "            hits += 1\n"
        "            return cache[n]\n"
        "        cache[n] = n * n\n"
        "        return cache[n]\n\n"
        "    results = [square(v) for v in values]\n"
        "    return (results, hits)"
    ),
    explanation=(
        "`cache[n] = ...` mutates an object the closure can already reach, whereas "
        "`hits += 1` rebinds a name and therefore needs `nonlocal` — the rule is about "
        "assignment to the *name*, not about changing data. This is `functools.cache` "
        "in miniature: the cache lives in the closure, so it is private, per-instance, "
        "and dies with the function that owns it."
    ),
    starter="def memo_calls(values):\n    ...",
    cases=[
        Case(expected=([4, 9, 4], 1), args=([2, 3, 2],)),
        Case(expected=([], 0), args=([],)),
        Case(expected=([25], 0), args=([5],)),
        Case(expected=([1, 1, 1], 2), args=([1, 1, 1],)),
    ],
)

q(
    qid="Q-219",
    level=Level.L4,
    topic="Arguments",
    kind="function",
    entry="signature",
    prompt=(
        "Write `signature(*args, **kwargs)` that returns a string showing how it was "
        "called — the argument list only, parentheses included.\n\n"
        "Positional arguments appear first as their `repr`, then keyword arguments as "
        "`name=repr`, all joined by `\", \"`. So `signature(1, \"a\")` returns "
        "`\"(1, 'a')\"`, `signature(1, x=None)` returns `\"(1, x=None)\"`, and "
        "`signature()` returns `\"()\"`."
    ),
    hint=(
        "`repr(v)` and the `!r` conversion in an f-string produce the same text. Build "
        "one list of the pieces, then `\", \".join` it — the empty call then falls out "
        "for free."
    ),
    solution=(
        "def signature(*args, **kwargs):\n"
        "    parts = [repr(a) for a in args]\n"
        '    parts += [f"{k}={v!r}" for k, v in kwargs.items()]\n'
        '    return "(" + ", ".join(parts) + ")"'
    ),
    explanation=(
        "Using `repr` rather than `str` is what makes the output unambiguous: `'1'` and "
        "`1` print identically under `str` and differently under `repr`, and a debug "
        "line that cannot tell them apart is worthless. Keyword arguments keep the "
        "order they were passed in, since `**kwargs` is an ordinary insertion-ordered "
        "dict."
    ),
    starter="def signature(*args, **kwargs):\n    ...",
    cases=[
        Case(expected="(1, 'a')", args=(1, "a")),
        Case(expected="(b=2)", kwargs={"b": 2}),
        Case(expected="(1, x=None)", args=(1,), kwargs={"x": None}),
        Case(expected="()", args=()),
        Case(expected="([1, 2], flag=True)", args=([1, 2],), kwargs={"flag": True}),
    ],
)

q(
    qid="Q-220",
    level=Level.L4,
    topic="Varargs",
    kind="custom",
    entry="merge_all",
    constraints=["no-loops"],
    prompt=(
        "Write `merge_all(*mappings)` that merges any number of dicts left to right "
        "into one **new** dict — later keys win, and none of the inputs is "
        "modified.\n\n"
        "`merge_all({\"a\": 1}, {\"a\": 2})` is `{'a': 2}`; `merge_all()` is `{}`.\n\n"
        "No `for` statement and no `.update()` — fold the sequence with "
        "`functools.reduce`."
    ),
    hint=(
        "`reduce(fn, seq, start)` collapses a sequence to one value, and its `start` "
        "argument is what makes the empty call work. Inside the lambda, `{**a, **b}` "
        "builds a merged copy in one expression."
    ),
    solution=(
        "import functools\n\n\n"
        "def merge_all(*mappings):\n"
        "    return functools.reduce(lambda acc, m: {**acc, **m}, mappings, {})"
    ),
    explanation=(
        "`{**a, **b}` is dict unpacking in a *display*: it builds a new dict rather "
        "than mutating `a`, which is what keeps the inputs untouched — `a.update(b)` "
        "would silently edit the caller's object. Supplying `reduce`'s initial value "
        "is not optional here: without it, the zero-argument call raises `TypeError` "
        "on an empty sequence."
    ),
    starter="import functools\n\n\ndef merge_all(*mappings):\n    ...",
    cases=[
        Case(expected={"a": 1, "b": 2}, args=({"a": 1}, {"b": 2})),
        Case(expected={"a": 2}, args=({"a": 1}, {"a": 2})),
        Case(expected={}, args=()),
        Case(expected={"a": 1}, args=({"a": 1},)),
        Case(expected={"a": 1, "b": 9, "c": 3}, args=({"a": 1, "b": 2}, {"b": 9}, {"c": 3})),
    ],
)

q(
    qid="Q-221",
    level=Level.L4,
    topic="Definition",
    kind="custom",
    entry="depth",
    constraints=["needs-recursion", "no-loops"],
    prompt=(
        "Write `depth(value)` that returns how deeply lists are nested inside "
        "`value`:\n\n"
        "- a non-list returns `0`;\n"
        "- `[1, 2]` returns `1`;\n"
        "- `[[1], [2, [3]]]` returns `3`;\n"
        "- the empty list `[]` returns `1`.\n\n"
        "The function must call itself. No `for` statement."
    ),
    hint=(
        "Two base cases come first — not a list, then an empty list — and the "
        "recursive step is one more than the deepest child. A generator expression "
        "inside `max` visits the children without a `for` statement."
    ),
    solution=(
        "def depth(value):\n"
        "    if not isinstance(value, list):\n"
        "        return 0\n"
        "    if not value:\n"
        "        return 1\n"
        "    return 1 + max(depth(v) for v in value)"
    ),
    explanation=(
        "A recursive function is two things: base cases that return without recursing, "
        "and a step that makes the problem strictly smaller. Forgetting the *empty* "
        "list base case is the classic bug here — `max()` of an empty sequence raises "
        "`ValueError`, so the function would crash on the most ordinary input there is."
    ),
    starter="def depth(value):\n    ...",
    cases=[
        Case(expected=0, args=(5,)),
        Case(expected=1, args=([1, 2],)),
        Case(expected=3, args=([[1], [2, [3]]],)),
        Case(expected=1, args=([],)),
        Case(expected=3, args=([[[]]],)),
        Case(expected=0, args=("abc",)),
    ],
)

q(
    qid="Q-222",
    level=Level.L4,
    topic="First-Class",
    kind="function",
    entry="pipeline",
    prompt=(
        "Write `pipeline(fns, x)` that feeds `x` through every function in the list "
        "`fns`, left to right, each one receiving the previous one's result, and "
        "returns the final value.\n\n"
        "`pipeline([abs, float], -3)` is `3.0`. An empty `fns` returns `x` unchanged."
    ),
    hint=(
        "One accumulator variable, reassigned each time round. The empty-list case "
        "needs no special branch if you start the accumulator at the right value."
    ),
    solution=(
        "def pipeline(fns, x):\n"
        "    for fn in fns:\n"
        "        x = fn(x)\n"
        "    return x"
    ),
    explanation=(
        "Rebinding the parameter `x` is safe and idiomatic — it is a local name, so the "
        "caller's variable is untouched. Composing behaviour as a *list of functions* "
        "rather than a chain of calls means the steps become data you can build, filter "
        "and reorder at runtime; `functools.reduce(lambda v, f: f(v), fns, x)` is the "
        "same idea in one expression."
    ),
    starter="def pipeline(fns, x):\n    ...",
    cases=[
        Case(expected=3.0, args=([abs, float], -3)),
        Case(expected=5, args=([], 5)),
        Case(expected=5, args=([str, len], 12345)),
        Case(expected=3, args=([float, int], "3.9")),
        Case(expected="AB", args=([str.strip, str.upper], "  ab  ")),
    ],
)

q(
    qid="Q-223",
    level=Level.L4,
    topic="Scope",
    kind="function",
    entry="legb",
    prompt=(
        "The starter defines `scope = \"global\"` at module level. Write `legb(mode)` "
        "that demonstrates each rung of the LEGB ladder.\n\n"
        "`legb` sets its own local `scope = \"enclosing\"`, then defines four inner "
        "functions and calls the one named by `mode`, returning its result:\n\n"
        "- `\"local\"` -> assigns its own `scope = \"local\"` and returns it;\n"
        "- `\"enclosing\"` -> returns `scope` without assigning (gets `'enclosing'`);\n"
        "- `\"global\"` -> declares `global scope` and returns it (gets `'global'`);\n"
        "- `\"builtin\"` -> returns `sorted([\"b\", \"a\"])[0]`, which is `'a'`.\n\n"
        "Dispatch on `mode` with a dict of the four functions."
    ),
    hint=(
        "Python resolves a name Local, then Enclosing, then Global, then Builtins — "
        "first hit wins. The `global` declaration is what lets the third function skip "
        "the enclosing rung even though a name is sitting on it."
    ),
    solution=(
        'scope = "global"\n\n\n'
        "def legb(mode):\n"
        '    scope = "enclosing"\n\n'
        "    def local_wins():\n"
        '        scope = "local"\n'
        "        return scope\n\n"
        "    def enclosing_wins():\n"
        "        return scope\n\n"
        "    def global_wins():\n"
        "        global scope\n"
        "        return scope\n\n"
        "    def builtin_wins():\n"
        '        return sorted(["b", "a"])[0]\n\n'
        "    table = {\n"
        '        "local": local_wins,\n'
        '        "enclosing": enclosing_wins,\n'
        '        "global": global_wins,\n'
        '        "builtin": builtin_wins,\n'
        "    }\n"
        "    return table[mode]()"
    ),
    explanation=(
        "LEGB is a search order, not a merge: the first scope that has the name "
        "supplies it and the rest are never consulted. `builtin_wins` finds `sorted` on "
        "the last rung only because nothing nearer defines it — which is exactly why "
        "naming a local variable `list`, `sum` or `id` shadows the builtin for the rest "
        "of that function and produces a baffling `TypeError` later on."
    ),
    starter='scope = "global"\n\n\ndef legb(mode):\n    ...',
    cases=[
        Case(expected="local", args=("local",)),
        Case(expected="enclosing", args=("enclosing",)),
        Case(expected="global", args=("global",)),
        Case(expected="a", args=("builtin",)),
    ],
)

q(
    qid="Q-224",
    level=Level.L4,
    topic="Lambda",
    kind="custom",
    entry="rank",
    constraints=["needs-comprehension", "no-builtin:reversed"],
    prompt=(
        "Write `rank(records)` where `records` is a list of `(name, score)` tuples. "
        "Return a list of the names ordered by score **descending**, with names sorted "
        "alphabetically among equal scores.\n\n"
        "Use `sorted` with a single `key=` lambda producing a tuple — no `reverse=`, no "
        "`reversed`, no second sort pass. Extract the names with a comprehension."
    ),
    hint=(
        "Tuples compare element by element, so one key can encode two priorities. To "
        "flip just the first priority while leaving the second ascending, change the "
        "value rather than the direction."
    ),
    solution=(
        "def rank(records):\n"
        "    ordered = sorted(records, key=lambda r: (-r[1], r[0]))\n"
        "    return [name for name, _ in ordered]"
    ),
    explanation=(
        "Negating the numeric field reverses only that field, which `reverse=True` "
        "cannot do — that flag would reverse the name ordering too and put `'c'` before "
        "`'b'` on a tie. The trick works only for numbers; to mix directions on strings "
        "you sort twice, relying on stability, with the *least* significant key first."
    ),
    starter="def rank(records):\n    ...",
    cases=[
        Case(expected=["b", "c", "a"], args=([("a", 3), ("b", 5), ("c", 5)],)),
        Case(expected=[], args=([],)),
        Case(expected=["z"], args=([("z", 1)],)),
        Case(expected=["a", "b"], args=([("b", 2), ("a", 2)],)),
    ],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-225",
    level=Level.L5,
    topic="Closures",
    kind="custom",
    entry="running_totals",
    constraints=["needs-comprehension", "no-builtin:sum"],
    prompt=(
        "Write `running_totals(values)` that returns the list of running sums: "
        "`[1, 2, 3]` gives `[1, 3, 6]`.\n\n"
        "The accumulator must live in a closure — define an inner `add(v)` that "
        "updates a `total` in the enclosing scope with `nonlocal` and returns the new "
        "running value, then build the result with a **list comprehension** over "
        "`values`. No `sum`, no `itertools.accumulate`, no `for` statement."
    ),
    hint=(
        "The comprehension calls `add` once per item, in order, and collects what it "
        "returns. That the comprehension has a side effect is exactly what makes this "
        "work — and exactly why it is worth thinking about."
    ),
    solution=(
        "def running_totals(values):\n"
        "    total = 0\n\n"
        "    def add(v):\n"
        "        nonlocal total\n"
        "        total += v\n"
        "        return total\n\n"
        "    return [add(v) for v in values]"
    ),
    explanation=(
        "This works because a comprehension evaluates its expression left to right, "
        "once per item, so the closure's `total` threads state through it — but a "
        "comprehension with side effects is a *code smell*: readers expect a pure "
        "mapping, and reordering or parallelising it would silently change the answer. "
        "`itertools.accumulate(values)` says the same thing with no mutable state at all."
    ),
    starter="def running_totals(values):\n    ...",
    cases=[
        Case(expected=[1, 3, 6], args=([1, 2, 3],)),
        Case(expected=[], args=([],)),
        Case(expected=[5], args=([5],)),
        Case(expected=[1, 0, 1], args=([1, -1, 1],)),
        Case(expected=[0.5, 1.0], args=([0.5, 0.5],)),
    ],
)

q(
    qid="Q-226",
    level=Level.L5,
    topic="Arguments",
    kind="custom",
    entry="partial_apply",
    constraints=["no-builtin:partial"],
    prompt=(
        "Reimplement `functools.partial`. Write a factory "
        "`make_partial(fn, *fixed, **fixed_kw)` returning a function `bound(*args, "
        "**kwargs)` that calls `fn` with the fixed arguments **first**, then the later "
        "positional ones, and with the later keywords **overriding** the fixed ones.\n\n"
        "Then write `partial_apply(fn, fixed, fixed_kw, args, kwargs)` that builds the "
        "partial from the tuple `fixed` and dict `fixed_kw`, calls it with the tuple "
        "`args` and dict `kwargs`, and returns the result.\n\n"
        "Do not use `functools.partial`."
    ),
    hint=(
        "`bound` closes over all four of the factory's names. Ordering the positional "
        "arguments is one unpacking after another; the keyword override falls out of "
        "which dict is unpacked second."
    ),
    solution=(
        "def make_partial(fn, *fixed, **fixed_kw):\n"
        "    def bound(*args, **kwargs):\n"
        "        return fn(*fixed, *args, **{**fixed_kw, **kwargs})\n\n"
        "    return bound\n\n\n"
        "def partial_apply(fn, fixed, fixed_kw, args, kwargs):\n"
        "    return make_partial(fn, *fixed, **fixed_kw)(*args, **kwargs)"
    ),
    explanation=(
        "Partial application turns an n-argument function into a configured "
        "m-argument one, and the whole mechanism is a closure over the fixed arguments "
        "— nothing more. Two details carry the semantics: fixed positionals must come "
        "first (you cannot pre-fill argument two and leave one open), and `{**fixed_kw, "
        "**kwargs}` puts the caller's keywords last so they win. The real "
        "`functools.partial` adds introspection and picklability, which a closure "
        "cannot offer."
    ),
    starter=(
        "def make_partial(fn, *fixed, **fixed_kw):\n    ...\n\n\n"
        "def partial_apply(fn, fixed, fixed_kw, args, kwargs):\n    ..."
    ),
    cases=[
        Case(expected=1024, args=(pow, (2,), {}, (10,), {})),
        Case(expected=7, args=(max, (), {}, (3, 7), {})),
        Case(expected=2.6, args=(round, (2.567,), {}, (), {"ndigits": 1})),
        Case(expected=[3, 2, 1], args=(sorted, (), {"reverse": True}, ([1, 3, 2],), {})),
        Case(
            expected=[1, 2, 3],
            args=(sorted, (), {"reverse": True}, ([1, 3, 2],), {"reverse": False}),
        ),
    ],
)

q(
    qid="Q-227",
    level=Level.L5,
    topic="Definition",
    kind="custom",
    entry="take",
    constraints=["needs-generator", "no-builtin:range"],
    prompt=(
        "Write `take(count)` that returns the first `count` whole numbers starting at "
        "zero, as a list: `take(3)` is `[0, 1, 2]` and `take(0)` is `[]`.\n\n"
        "Do it the long way round. **Inside** `take`, define a generator function "
        "`numbers()` that yields `0, 1, 2, ...` forever — an infinite stream, with no "
        "list anywhere in it — then take a finite prefix of it with "
        "`itertools.islice`.\n\n"
        "You may not call `range`, and `take` must not hang."
    ),
    hint=(
        "A function containing `yield` returns a generator when called; its body only "
        "advances when something asks for the next value. `itertools.islice(it, n)` "
        "stops after `n` values, which is what keeps an endless producer safe."
    ),
    solution=(
        "import itertools\n\n\n"
        "def take(count):\n"
        "    def numbers():\n"
        "        n = 0\n"
        "        while True:\n"
        "            yield n\n"
        "            n += 1\n\n"
        "    return list(itertools.islice(numbers(), count))"
    ),
    explanation=(
        "`yield` turns the function into a *generator function*: calling it runs no "
        "code at all, it just builds a generator whose body advances one `yield` at a "
        "time and keeps its local `n` alive between resumptions. That laziness is what "
        "makes an infinite stream safe to define — `list(numbers())` would hang "
        "forever, so the consumer, not the producer, decides where to stop."
    ),
    starter="import itertools\n\n\ndef take(count):\n    ...",
    cases=[
        Case(expected=[0, 1, 2], args=(3,)),
        Case(expected=[], args=(0,)),
        Case(expected=[0], args=(1,)),
        Case(expected=[0, 1, 2, 3, 4], args=(5,)),
    ],
)

q(
    qid="Q-228",
    level=Level.L5,
    topic="Closures",
    kind="custom",
    entry="traced",
    constraints=["no-builtin:wraps"],
    prompt=(
        "Write a decorator by hand. `count_calls(fn)` takes a function and returns a "
        "`wrapper` that:\n\n"
        "- forwards every positional and keyword argument through to `fn` and returns "
        "its result;\n"
        "- keeps a call count reachable from outside as `wrapper.calls`, starting at "
        "`0`;\n"
        "- copies `fn.__name__` onto itself, so the wrapper does not report as "
        "`'wrapper'`.\n\n"
        "Then write `traced(fn, arg_list)` that wraps `fn`, calls the wrapped version "
        "once per item of `arg_list`, and returns the 3-tuple `(results, calls, "
        "name)`.\n\n"
        "Do not use `functools.wraps`."
    ),
    hint=(
        "Store the counter as an *attribute on the wrapper function object* rather "
        "than a closed-over integer — then `wrapper.calls += 1` mutates an object "
        "instead of rebinding a name, and no `nonlocal` is needed. The wrapper can "
        "refer to itself by name because it closes over the enclosing scope."
    ),
    solution=(
        "def count_calls(fn):\n"
        "    def wrapper(*args, **kwargs):\n"
        "        wrapper.calls += 1\n"
        "        return fn(*args, **kwargs)\n\n"
        "    wrapper.calls = 0\n"
        "    wrapper.__name__ = fn.__name__\n"
        "    return wrapper\n\n\n"
        "def traced(fn, arg_list):\n"
        "    wrapped = count_calls(fn)\n"
        "    results = [wrapped(a) for a in arg_list]\n"
        "    return (results, wrapped.calls, wrapped.__name__)"
    ),
    explanation=(
        "A decorator is nothing more than a function that takes a function and returns "
        "a replacement — `@count_calls` above a `def` is exactly `fn = count_calls(fn)`. "
        "`wrapper` finds itself by name because the lookup happens at call time, by "
        "which point the enclosing scope has bound it. Copying `__name__` is the part "
        "everyone forgets: without it, tracebacks, `help()` and logging all report "
        "`'wrapper'`, which is why `functools.wraps` exists to copy the whole set of "
        "metadata for you."
    ),
    starter="def count_calls(fn):\n    ...\n\n\ndef traced(fn, arg_list):\n    ...",
    cases=[
        Case(expected=([1, 2, 3], 3, "abs"), args=(abs, [-1, 2, -3])),
        Case(expected=([], 0, "str"), args=(str, [])),
        Case(expected=([1.5], 1, "float"), args=(float, ["1.5"])),
        Case(expected=([2, 1], 2, "len"), args=(len, ["ab", "c"])),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-06",
    title="Closure-built validation toolkit",
    brief=(
        "Build a small validation library out of **factory functions** — each one "
        "returns a checker that closes over its configuration.\n\n"
        "Write four factories. Every checker they return takes `(field, value)` and "
        "returns either `None` (fine) or a message string:\n\n"
        "- `of_type(expected)` -> `f\"{field}: expected {expected.__name__}, got "
        "{type(value).__name__}\"`\n"
        "- `in_range(lo, hi)` -> `f\"{field}: {value} not in {lo}..{hi}\"` when `value` "
        "is outside the inclusive range\n"
        "- `non_empty()` -> `f\"{field}: must not be empty\"` when `value` is falsy\n"
        "- `all_of(*checks)` -> runs the checkers in order and returns the **first** "
        "message, or `None` if they all pass\n\n"
        "Then wire them into a module-level `SPEC` dict, in this order:\n\n"
        "```python\n"
        "SPEC = {\n"
        '    "name": all_of(of_type(str), non_empty()),\n'
        '    "age": all_of(of_type(int), in_range(13, 120)),\n'
        '    "email": all_of(of_type(str), non_empty()),\n'
        "}\n"
        "```\n\n"
        "Finally write `validate(record)` returning a **list of message strings** in "
        "`SPEC` order — at most one per field. A field missing from `record` gives "
        "`f\"{field}: missing\"` and its checkers are not run. A fully valid record "
        "gives `[]`."
    ),
    hint=(
        "Each factory's body is one `def` plus a `return` of that inner function — the "
        "configuration (`expected`, `lo`/`hi`, `checks`) is captured by the closure and "
        "never passed again. `all_of` is the interesting one: it closes over a tuple "
        "of other closures and stops at the first non-`None` result."
    ),
    solution=(
        "def of_type(expected):\n"
        "    def check(field, value):\n"
        "        if not isinstance(value, expected):\n"
        '            return f"{field}: expected {expected.__name__}, got {type(value).__name__}"\n'
        "        return None\n\n"
        "    return check\n\n\n"
        "def in_range(lo, hi):\n"
        "    def check(field, value):\n"
        "        if not lo <= value <= hi:\n"
        '            return f"{field}: {value} not in {lo}..{hi}"\n'
        "        return None\n\n"
        "    return check\n\n\n"
        "def non_empty():\n"
        "    def check(field, value):\n"
        "        if not value:\n"
        '            return f"{field}: must not be empty"\n'
        "        return None\n\n"
        "    return check\n\n\n"
        "def all_of(*checks):\n"
        "    def check(field, value):\n"
        "        for one in checks:\n"
        "            problem = one(field, value)\n"
        "            if problem is not None:\n"
        "                return problem\n"
        "        return None\n\n"
        "    return check\n\n\n"
        "SPEC = {\n"
        '    "name": all_of(of_type(str), non_empty()),\n'
        '    "age": all_of(of_type(int), in_range(13, 120)),\n'
        '    "email": all_of(of_type(str), non_empty()),\n'
        "}\n\n\n"
        "def validate(record):\n"
        "    errors = []\n"
        "    for field, check in SPEC.items():\n"
        "        if field not in record:\n"
        '            errors.append(f"{field}: missing")\n'
        "            continue\n"
        "        problem = check(field, record[field])\n"
        "        if problem is not None:\n"
        "            errors.append(problem)\n"
        "    return errors"
    ),
    explanation=(
        "Every rule here is one object that carries both its logic and its "
        "configuration, which is why `SPEC` can be plain data and `validate` knows "
        "nothing about types or ranges — adding a rule never touches the engine. The "
        "ordering inside `all_of` is load-bearing: the type check has to run first, "
        "because `in_range` would raise `TypeError` comparing a string to an int, and "
        "returning at the first failure is what keeps one bad field from producing a "
        "cascade of nonsense messages. This is the closure's real job in production "
        "code — configured behaviour, passed around as a value."
    ),
    entry="validate",
    starter=(
        "def of_type(expected):\n    ...\n\n\n"
        "def in_range(lo, hi):\n    ...\n\n\n"
        "def non_empty():\n    ...\n\n\n"
        "def all_of(*checks):\n    ...\n\n\n"
        "SPEC = ...\n\n\n"
        "def validate(record):\n    ..."
    ),
    cases=[
        Case(expected=[], args=({"name": "Ada", "age": 36, "email": "a@b.c"},)),
        Case(
            expected=["name: must not be empty"],
            args=({"name": "", "age": 36, "email": "a@b.c"},),
        ),
        Case(
            expected=["age: expected int, got str"],
            args=({"name": "Ada", "age": "36", "email": "a@b.c"},),
        ),
        Case(
            expected=["age: 9 not in 13..120"],
            args=({"name": "Ada", "age": 9, "email": "a@b.c"},),
        ),
        Case(expected=["email: missing"], args=({"name": "Ada", "age": 36},)),
        Case(
            expected=["name: missing", "age: missing", "email: missing"],
            args=({},),
        ),
        Case(
            expected=["name: expected str, got int", "email: must not be empty"],
            args=({"name": 7, "age": 120, "email": ""},),
        ),
    ],
)

NOTEBOOK = Notebook(
    number=6,
    slug="functions_scope_closures",
    title="Functions, Scope & Closures",
    intro=(
        "Defining functions, every way of passing arguments to them, the four scopes a "
        "name can live in, and closures — functions that carry a piece of their birth "
        "environment around with them.\n\n"
        "This notebook is a step up. The argument rules (`*args`, `**kwargs`, "
        "keyword-only, positional-only) are mechanical and worth drilling, but the "
        "scope questions are where the famous bugs live: a default list that is shared "
        "across every call, a loop of lambdas that all return the same number, and an "
        "`UnboundLocalError` raised by a line that only *reads* a variable. Predict "
        "before you run."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
