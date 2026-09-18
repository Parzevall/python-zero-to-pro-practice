"""Notebook 01 - Foundations & Operators (Q-001..Q-036)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-001",
    level=Level.L1,
    topic="Variables",
    kind="value",
    entry="me",
    prompt=(
        "Create three variables — `name` (a string), `age` (a whole number) and "
        "`height` (a number with a decimal point) — then set `me` to the tuple "
        "`(name, age, height)`.\n\n"
        "Use exactly `\"Ada\"`, `36` and `1.7` so the checker can verify the types."
    ),
    hint="A tuple is written with commas: `me = name, age, height`. Note `36` and `36.0` are different types.",
    solution='name = "Ada"\nage = 36\nheight = 1.7\nme = (name, age, height)',
    explanation=(
        "Python infers each type from the literal you write: quotes make a `str`, "
        "a bare whole number makes an `int`, and a decimal point makes a `float`. "
        "The checker is strict about type, so `36.0` would not pass for `age`."
    ),
    starter="name = ...\nage = ...\nheight = ...\nme = ...",
    cases=[Case(expected=("Ada", 36, 1.7))],
)

q(
    qid="Q-002",
    level=Level.L1,
    topic="Primitive Types",
    kind="function",
    entry="kinds",
    prompt=(
        "Write `kinds(values)`. Given a list of any objects, return a **list of "
        "strings**: the name of each value's type, in the same order.\n\n"
        "`kinds([1, \"a\"])` returns `['int', 'str']` — the bare name, with no "
        "`<class ...>` wrapper around it."
    ),
    hint=(
        "`type(x)` hands you back the type itself, not a string. Types are objects "
        "too, and every one of them carries its own name as an attribute."
    ),
    solution="def kinds(values):\n    return [type(v).__name__ for v in values]",
    explanation=(
        "`str(type(v))` gives `\"<class 'int'>\"` — readable for a human, useless for "
        "a comparison — which is why `.__name__` is the attribute you want. Note that "
        "`type()` reports the *exact* class and ignores inheritance, so `True` comes "
        "back as `bool` and never as `int`."
    ),
    starter="def kinds(values):\n    ...",
    cases=[
        Case(expected=["int", "str", "float", "bool"], args=([1, "a", 1.5, True],)),
        Case(expected=[], args=([],)),
        Case(expected=["NoneType", "list", "tuple", "dict"], args=([None, [1], (1,), {}],)),
    ],
)

q(
    qid="Q-003",
    level=Level.L1,
    topic="Variables",
    kind="function",
    entry="swap",
    prompt=(
        "Write `swap(a, b)` that returns the **tuple** `(b, a)`.\n\n"
        "Do it with tuple unpacking — one assignment statement, no temporary "
        "variable like `tmp`."
    ),
    hint=(
        "Assignment in Python can have several names on the left and several values "
        "on the right. Ask yourself when the right-hand side is evaluated relative "
        "to when the names are rebound."
    ),
    solution="def swap(a, b):\n    a, b = b, a\n    return (a, b)",
    explanation=(
        "The whole right-hand side is evaluated into a tuple *before* any name on "
        "the left is rebound, so neither value can be clobbered mid-swap and no "
        "temporary is needed. The same rule is what makes the Fibonacci one-liner "
        "`a, b = b, a + b` compute `a + b` from the old `a`."
    ),
    starter="def swap(a, b):\n    ...",
    cases=[
        Case(expected=(2, 1), args=(1, 2)),
        Case(expected=("right", "left"), args=("left", "right")),
        Case(expected=(0, 0), args=(0, 0)),
        Case(expected=([3], (1, 2)), args=((1, 2), [3])),
    ],
)

q(
    qid="Q-004",
    level=Level.L1,
    topic="Arithmetic",
    kind="function",
    entry="basics",
    prompt=(
        "Write `basics(a, b)` that returns the 4-tuple "
        "`(a + b, a - b, a * b, a / b)` — sum, difference, product, quotient, in "
        "that order.\n\n"
        "Assume `b` is never `0`."
    ),
    hint=(
        "Three of the four results keep the type of the operands. One of them does "
        "not, no matter what you feed it — work out which before you check your answer."
    ),
    solution="def basics(a, b):\n    return (a + b, a - b, a * b, a / b)",
    explanation=(
        "`/` is *true division*: it always produces a `float`, even when the division "
        "comes out exact, so `6 / 3` is `3.0` and not `3`. That was the single most "
        "disruptive change from Python 2, and it is why `//` exists as a separate "
        "operator for when you want an integer back."
    ),
    starter="def basics(a, b):\n    ...",
    cases=[
        Case(expected=(9, 5, 14, 3.5), args=(7, 2)),
        Case(expected=(6, 0, 9, 1.0), args=(3, 3)),
        Case(expected=(-2, -6, -8, -2.0), args=(-4, 2)),
    ],
)

q(
    qid="Q-005",
    level=Level.L1,
    topic="Arithmetic",
    kind="function",
    entry="split",
    prompt=(
        "Write `split(a, b)` that returns the tuple `(a // b, a % b)` — the whole "
        "number of times `b` fits into `a`, and what is left over.\n\n"
        "Both inputs are positive integers, so both results are integers."
    ),
    hint=(
        "`//` and `%` are two halves of one division. There is also a single builtin "
        "that produces both at once; using it here is fine, but know what it is called."
    ),
    solution="def split(a, b):\n    return (a // b, a % b)",
    explanation=(
        "These two operators are defined together so that `b * (a // b) + (a % b)` "
        "always reconstructs `a` exactly — that identity, not any rounding rule, is "
        "what pins down their behaviour. `divmod(a, b)` computes the pair in one "
        "step, which is both faster and impossible to get out of sync."
    ),
    starter="def split(a, b):\n    ...",
    cases=[
        Case(expected=(3, 2), args=(17, 5)),
        Case(expected=(1, 0), args=(5, 5)),
        Case(expected=(0, 4), args=(4, 5)),
        Case(expected=(0, 0), args=(0, 5)),
    ],
)

q(
    qid="Q-006",
    level=Level.L1,
    topic="Arithmetic",
    kind="function",
    entry="power",
    prompt=(
        "Write `power(base, exp)` that returns `base` raised to the power `exp`, "
        "using the `**` operator.\n\n"
        "Return whatever `**` gives you — do not cast the result."
    ),
    hint=(
        "Two of the test cases do not use a positive whole exponent. Think about "
        "what type Python has to reach for when the answer cannot be an integer."
    ),
    solution="def power(base, exp):\n    return base ** exp",
    explanation=(
        "`**` binds tighter than unary minus, so `-2 ** 2` is `-4` and not `4` — "
        "parenthesise when you mean the other thing. It also switches to `float` "
        "whenever the result cannot be an integer, which includes every negative "
        "and every fractional exponent."
    ),
    starter="def power(base, exp):\n    ...",
    cases=[
        Case(expected=1024, args=(2, 10)),
        Case(expected=1, args=(5, 0)),
        Case(expected=0.5, args=(2, -1)),
        Case(expected=3.0, args=(9, 0.5)),
    ],
)

q(
    qid="Q-007",
    level=Level.L1,
    topic="Casting",
    kind="function",
    entry="to_int",
    prompt=(
        "Write `to_int(text)` that takes a string holding a whole number and "
        "returns it as an `int`.\n\n"
        "The string may have spaces around it and may carry a leading `-`."
    ),
    hint=(
        "One builtin does all of this already, including the whitespace. You do not "
        "need `.strip()`, and you do not need to handle the sign yourself."
    ),
    solution="def to_int(text):\n    return int(text)",
    explanation=(
        "`int()` on a string parses an integer *literal*: it tolerates surrounding "
        "whitespace, a leading sign, and underscores like `1_000`, but nothing else. "
        "That is why `int(\"3.0\")` raises `ValueError` even though `float(\"3.0\")` "
        "is fine — the string has to spell an integer, not merely denote one."
    ),
    starter="def to_int(text):\n    ...",
    cases=[
        Case(expected=42, args=("42",)),
        Case(expected=-7, args=("-7",)),
        Case(expected=0, args=("0",)),
        Case(expected=8, args=("  8  ",)),
    ],
)

q(
    qid="Q-008",
    level=Level.L1,
    topic="Casting",
    kind="function",
    entry="label",
    prompt=(
        "Write `label(n)` that returns the string `\"value: \"` followed by `n`.\n\n"
        "`label(42)` returns `'value: 42'`. `n` may be an int or a float."
    ),
    hint=(
        "`+` between a string and a number is a `TypeError`, not a convenience. "
        "Something has to change type first — or you can sidestep `+` entirely with "
        "an f-string."
    ),
    solution='def label(n):\n    return "value: " + str(n)',
    explanation=(
        "Python never coerces silently across `+`, because `\"3\" + 4` has two equally "
        "defensible answers and guessing wrong is worse than refusing. `str()` (or an "
        "f-string, which calls it for you) is you making that choice explicit."
    ),
    starter="def label(n):\n    ...",
    cases=[
        Case(expected="value: 42", args=(42,)),
        Case(expected="value: 0", args=(0,)),
        Case(expected="value: -3", args=(-3,)),
        Case(expected="value: 1.5", args=(1.5,)),
    ],
)

q(
    qid="Q-009",
    level=Level.L1,
    topic="Comparison",
    kind="function",
    entry="is_bigger",
    prompt=(
        "Write `is_bigger(a, b)` that returns `True` when `a` is strictly greater "
        "than `b`, and `False` otherwise. Equal values are not bigger.\n\n"
        "Return a `bool` — the checker will not accept `1` for `True`."
    ),
    hint=(
        "A comparison is already an expression with a value. Ask what `a > b` "
        "evaluates to on its own, before any `if` touches it."
    ),
    solution="def is_bigger(a, b):\n    return a > b",
    explanation=(
        "`if a > b: return True else: return False` is four lines that compute what "
        "`a > b` already is — comparison operators evaluate to the real `True` and "
        "`False` singletons, not to something bool-ish. Reviewers call the long form "
        "a *boolean trap*, and it is the most common tell of a beginner in a diff."
    ),
    starter="def is_bigger(a, b):\n    ...",
    cases=[
        Case(expected=True, args=(5, 3)),
        Case(expected=False, args=(3, 5)),
        Case(expected=False, args=(4, 4)),
        Case(expected=True, args=(-1, -2)),
    ],
)

q(
    qid="Q-010",
    level=Level.L1,
    topic="Logical",
    kind="function",
    entry="both_and_either",
    prompt=(
        "Write `both_and_either(a, b)` where `a` and `b` are booleans. Return the "
        "3-tuple `(a and b, a or b, not a)`.\n\n"
        "All three elements must be `bool`."
    ),
    hint=(
        "These are the three logical *keywords*, not the symbols `&`, `|` and `~` — "
        "those are bitwise operators and a different question entirely."
    ),
    solution="def both_and_either(a, b):\n    return (a and b, a or b, not a)",
    explanation=(
        "`and` and `or` return one of their *operands* rather than a fresh boolean — "
        "invisible here because the operands are already booleans, but central from "
        "Q-019 onward. `not` is the odd one out: it always produces a real `bool`, "
        "whatever you give it."
    ),
    starter="def both_and_either(a, b):\n    ...",
    cases=[
        Case(expected=(False, True, False), args=(True, False)),
        Case(expected=(True, True, False), args=(True, True)),
        Case(expected=(False, False, True), args=(False, False)),
        Case(expected=(False, True, True), args=(False, True)),
    ],
)

q(
    qid="Q-011",
    level=Level.L1,
    topic="Membership",
    kind="function",
    entry="has_vowel",
    prompt=(
        "Write `has_vowel(word)` that returns `True` if `word` contains at least one "
        "of `a`, `e`, `i`, `o`, `u`, and `False` otherwise.\n\n"
        "`word` is always lowercase and may be empty. Use the `in` operator — no "
        "loops, no `any()`."
    ),
    hint=(
        "`in` answers the question for one vowel at a time. You have five questions "
        "and need `True` if any of them says yes — which keyword joins them that way?"
    ),
    solution=(
        "def has_vowel(word):\n"
        '    return "a" in word or "e" in word or "i" in word or "o" in word or "u" in word'
    ),
    explanation=(
        "On a string, `in` tests for a *substring*, not just a single character — "
        "`\"th\" in \"python\"` is also `True`. The operator is generic and the "
        "container decides what it means: for a list it tests elements, for a dict "
        "it tests keys, for a set it is a hash lookup."
    ),
    starter="def has_vowel(word):\n    ...",
    cases=[
        Case(expected=True, args=("python",)),
        Case(expected=False, args=("rhythm",)),
        Case(expected=False, args=("",)),
        Case(expected=True, args=("aeiou",)),
    ],
)

q(
    qid="Q-012",
    level=Level.L1,
    topic="Environment",
    kind="output",
    entry="show_version",
    prompt=(
        "Write `show_version()` so it prints the major and minor version of the "
        "running interpreter as `3.13` — read it from `sys.version_info`, do not "
        "hard-code the string."
    ),
    hint="`sys.version_info` is a named tuple: `.major` and `.minor` are ints. An f-string joins them.",
    solution=(
        "import sys\n\n\n"
        "def show_version():\n"
        '    print(f"{sys.version_info.major}.{sys.version_info.minor}")'
    ),
    explanation=(
        "`sys.version_info` is the reliable way to branch on Python version, because "
        "it compares as a tuple of ints — `sys.version_info >= (3, 12)` just works. "
        "`sys.version` is a human-readable string that also contains the compiler and "
        "build date, and should never be parsed."
    ),
    starter="import sys\n\n\ndef show_version():\n    ...",
    cases=[Case(expected="3.13")],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-013",
    level=Level.L2,
    topic="Primitive Types",
    kind="function",
    entry="truthy",
    prompt=(
        "Write `truthy(values)` that returns a **list of bools**: the truth value of "
        "each item, in order.\n\n"
        "`truthy([0, \"a\"])` returns `[False, True]`."
    ),
    hint=(
        "There is a builtin whose whole job is to answer the question `if` would ask. "
        "Do not write the rules out by hand — each type already knows its own answer."
    ),
    solution="def truthy(values):\n    return [bool(v) for v in values]",
    explanation=(
        "The default rule is narrow: zero of any numeric type, and *empty* containers "
        "and strings, are falsy; every other object is truthy. So `\"0\"`, `\"False\"` "
        "and `[[]]` are all `True` — a container is judged on whether it holds "
        "anything, never on what it holds."
    ),
    starter="def truthy(values):\n    ...",
    cases=[
        Case(expected=[False, False, False, False], args=([0, "", [], None],)),
        Case(expected=[True, True, True, True], args=([1, "a", [0], {"k": 1}],)),
        Case(expected=[], args=([],)),
        Case(expected=[False, True, True, False], args=([0.0, "0", [[]], 0j],)),
    ],
)

q(
    qid="Q-014",
    level=Level.L2,
    topic="Casting",
    kind="function",
    entry="safe_int",
    prompt=(
        "Write `safe_int(text, default)` that returns `int(text)` when the string "
        "parses, and returns `default` unchanged when it does not.\n\n"
        "Catch `ValueError` specifically — not a bare `except:`."
    ),
    hint=(
        "`try`/`except` is the tool. The interesting decision is how *narrow* to make "
        "the `except` clause: name the one exception that a bad numeric string raises."
    ),
    solution=(
        "def safe_int(text, default):\n"
        "    try:\n"
        "        return int(text)\n"
        "    except ValueError:\n"
        "        return default"
    ),
    explanation=(
        "A bare `except:` also swallows `KeyboardInterrupt` and your own `NameError` "
        "typos, quietly turning a bug into a plausible-looking default — the worst "
        "kind of failure, because nothing ever reports it. Note that `int(None)` "
        "raises `TypeError`, not `ValueError`, so it still propagates here; that is "
        "the point, since a `None` where a string belongs is a caller error."
    ),
    starter="def safe_int(text, default):\n    ...",
    cases=[
        Case(expected=42, args=("42", 0)),
        Case(expected=0, args=("abc", 0)),
        Case(expected=-1, args=("", -1)),
        Case(expected=7, args=("3.5", 7)),
    ],
)

q(
    qid="Q-015",
    level=Level.L2,
    topic="Arithmetic",
    kind="function",
    entry="to_time",
    prompt=(
        "Write `to_time(seconds)` that turns a non-negative whole number of seconds "
        "into the tuple `(hours, minutes, seconds)`.\n\n"
        "`to_time(3661)` returns `(1, 1, 1)`. Minutes and seconds are always in "
        "`0..59`. Use `divmod`."
    ),
    hint=(
        "`divmod(a, b)` returns `(a // b, a % b)`. Peel off the smallest unit first, "
        "then feed what is left back through `divmod` for the next one up."
    ),
    solution=(
        "def to_time(seconds):\n"
        "    minutes, secs = divmod(seconds, 60)\n"
        "    hours, mins = divmod(minutes, 60)\n"
        "    return (hours, mins, secs)"
    ),
    explanation=(
        "Chained `divmod` is the standard way to break a total into mixed units, and "
        "it works smallest-unit-first because each step hands the leftover *whole* "
        "units to the next. Doing it with separate `//` and `%` computes the same "
        "division twice and lets the two drift apart if you edit one and not the other."
    ),
    starter="def to_time(seconds):\n    ...",
    cases=[
        Case(expected=(1, 1, 1), args=(3661,)),
        Case(expected=(0, 0, 0), args=(0,)),
        Case(expected=(0, 0, 59), args=(59,)),
        Case(expected=(23, 59, 59), args=(86399,)),
        Case(expected=(2, 0, 0), args=(7200,)),
    ],
)

q(
    qid="Q-016",
    level=Level.L2,
    topic="Arithmetic",
    kind="function",
    entry="two_ways",
    prompt=(
        "Write `two_ways(x)` that takes a float and returns the tuple "
        "`(round(x), int(x))`.\n\n"
        "Both elements are `int`. The point is to see where the two disagree — do "
        "not try to make them match."
    ),
    hint=(
        "One of these two heads for the nearest whole number; the other always heads "
        "toward zero. Two of the test cases sit exactly halfway, which is where a "
        "third rule appears."
    ),
    solution="def two_ways(x):\n    return (round(x), int(x))",
    explanation=(
        "`int()` *truncates* toward zero while `round()` goes to the nearest value, "
        "so they part company on negatives (`int(-2.7)` is `-2`, `round(-2.7)` is "
        "`-3`). At an exact `.5` tie `round()` picks the **even** neighbour, which is "
        "why `round(2.5)` is `2` and `round(3.5)` is `4` — Q-036 rebuilds that rule "
        "from scratch."
    ),
    starter="def two_ways(x):\n    ...",
    cases=[
        Case(expected=(3, 2), args=(2.7,)),
        Case(expected=(-3, -2), args=(-2.7,)),
        Case(expected=(2, 2), args=(2.5,)),
        Case(expected=(4, 3), args=(3.5,)),
    ],
)

q(
    qid="Q-017",
    level=Level.L2,
    topic="Dynamic Typing",
    kind="function",
    entry="rebind",
    prompt=(
        "Write `rebind(start)`. Inside it, use a **single** variable named `thing` "
        "three times over:\n\n"
        "1. bind it to `start`,\n"
        "2. then rebind it to `str(thing)`,\n"
        "3. then rebind it to `[thing]` (a one-item list).\n\n"
        "After each of the three steps record `type(thing).__name__`, and return the "
        "three names as a list of strings."
    ),
    hint=(
        "Nothing here converts `thing` in place; each step points the same name at a "
        "brand-new object. Ask yourself whether `type()` is reporting on the name or "
        "on what the name currently holds."
    ),
    solution=(
        "def rebind(start):\n"
        "    thing = start\n"
        "    names = [type(thing).__name__]\n"
        "    thing = str(thing)\n"
        "    names.append(type(thing).__name__)\n"
        "    thing = [thing]\n"
        "    names.append(type(thing).__name__)\n"
        "    return names"
    ),
    explanation=(
        "In Python a name is an untyped label and the *object* carries the type, so a "
        "variable never has a type to change — rebinding just moves the label, and the "
        "old object is collected once nothing points at it. That is why a type "
        "annotation like `thing: int` is advice to readers and type-checkers and is "
        "not enforced at runtime."
    ),
    starter="def rebind(start):\n    ...",
    cases=[
        Case(expected=["int", "str", "list"], args=(7,)),
        Case(expected=["float", "str", "list"], args=(1.5,)),
        Case(expected=["NoneType", "str", "list"], args=(None,)),
        Case(expected=["str", "str", "list"], args=("hi",)),
    ],
)

q(
    qid="Q-018",
    level=Level.L2,
    topic="Comparison",
    kind="function",
    entry="in_range",
    prompt=(
        "Write `in_range(lo, x, hi)` returning `True` when `x` lies between `lo` and "
        "`hi` **inclusive** of both ends, `False` otherwise.\n\n"
        "Write it as one chained comparison, not as two comparisons joined by `and`."
    ),
    hint=(
        "Python lets you write a comparison the way mathematics does, with the value "
        "in the middle and a bound on each side. Read the argument order in the "
        "signature — it is already arranged for you."
    ),
    solution="def in_range(lo, x, hi):\n    return lo <= x <= hi",
    explanation=(
        "A chained comparison evaluates the middle expression **once** and "
        "short-circuits, so it is both faster and safer than `lo <= x and x <= hi` "
        "when `x` is a function call or has a side effect. Chaining only reads "
        "naturally for ordering operators though: `a == b == c` tests all three for "
        "equality, which is *not* what `(a == b) == c` means."
    ),
    starter="def in_range(lo, x, hi):\n    ...",
    cases=[
        Case(expected=True, args=(1, 5, 10)),
        Case(expected=False, args=(1, 0, 10)),
        Case(expected=True, args=(1, 1, 10)),
        Case(expected=True, args=(1, 10, 10)),
        Case(expected=False, args=(5, 3, 1)),
    ],
)

q(
    qid="Q-019",
    level=Level.L2,
    topic="Logical",
    kind="function",
    entry="first_truthy",
    prompt=(
        "Write `first_truthy(a, b)` that returns `a` when `a` is truthy, and `b` "
        "otherwise.\n\n"
        "Return the **operand itself**, not `True`/`False`: `first_truthy(0, \"x\")` "
        "returns the string `'x'`, and `first_truthy(None, 0)` returns the int `0`."
    ),
    hint=(
        "This is a single operator, and the behaviour the prompt describes is exactly "
        "what that operator already does. The trap is wrapping it in something that "
        "flattens the result."
    ),
    solution="def first_truthy(a, b):\n    return a or b",
    explanation=(
        "`or` returns the first truthy operand, or the last operand if none is truthy "
        "— it never converts to `bool`, which is what makes `name = given or "
        "\"anonymous\"` a useful idiom. It is also what makes that idiom a bug when "
        "`0`, `\"\"` or `[]` is a legitimate value: reach for `if given is None` there."
    ),
    starter="def first_truthy(a, b):\n    ...",
    cases=[
        Case(expected="fallback", args=(0, "fallback")),
        Case(expected="set", args=("set", "fallback")),
        Case(expected=0, args=(None, 0)),
        Case(expected=[1], args=([], [1])),
        Case(expected=False, args=(0, False)),
    ],
)

q(
    qid="Q-020",
    level=Level.L2,
    topic="Identity",
    kind="function",
    entry="same_and_equal",
    prompt=(
        "Write `same_and_equal(a, b)` that returns the tuple `(a is b, a == b)`.\n\n"
        "Both elements are `bool`. Do not try to make the two agree — the whole point "
        "is the cases where they do not."
    ),
    hint=(
        "One of these two operators asks about the objects themselves; the other asks "
        "the objects a question about their values. Only one of them can ever be "
        "overridden by a class."
    ),
    solution="def same_and_equal(a, b):\n    return (a is b, a == b)",
    explanation=(
        "`is` compares object identity — effectively memory address — while `==` asks "
        "the object, via `__eq__`, whether the values match. They coincide for `None` "
        "and for the small integers CPython caches, which is exactly why `x is 0` "
        "seems to work and then mysteriously stops (see Q-025). Reserve `is` for "
        "`None`, `True`, `False` and sentinel objects."
    ),
    starter="def same_and_equal(a, b):\n    ...",
    cases=[
        Case(expected=(False, True), args=([1, 2], [1, 2])),
        Case(expected=(True, True), args=(None, None)),
        Case(expected=(False, True), args=(1, 1.0)),
        Case(expected=(False, False), args=([1], [2])),
    ],
)

q(
    qid="Q-021",
    level=Level.L2,
    topic="Membership",
    kind="function",
    entry="missing_keys",
    prompt=(
        "Write `missing_keys(d, keys)` that returns a **list** of the entries of "
        "`keys` that are not keys of the dict `d`, keeping the order they appear in "
        "`keys`.\n\n"
        "Use `not in`. `missing_keys({\"a\": 1}, [\"a\", \"b\"])` returns `['b']`."
    ),
    hint=(
        "`not in` on a dict asks about one half of each entry — decide which half "
        "before you write it. Building the result as a comprehension keeps the order "
        "for free."
    ),
    solution="def missing_keys(d, keys):\n    return [k for k in keys if k not in d]",
    explanation=(
        "`in` on a dict tests **keys** and never values, and it does so in constant "
        "time via the hash table — `k in d.keys()` is the identical test spelled "
        "longer. The case that catches people is a key whose value is falsy or "
        "`None`: it is still present, so membership and truthiness are different "
        "questions."
    ),
    starter="def missing_keys(d, keys):\n    ...",
    cases=[
        Case(expected=["c", "d"], args=({"a": 1, "b": 2}, ["a", "c", "d"])),
        Case(expected=["a"], args=({}, ["a"])),
        Case(expected=[], args=({"a": 1}, [])),
        Case(expected=[], args=({"a": None}, ["a"])),
    ],
)

q(
    qid="Q-022",
    level=Level.L2,
    topic="Environment",
    kind="function",
    entry="setting",
    prompt=(
        "Write `setting(name, fallback)` that returns the value of the environment "
        "variable `name`, or `fallback` when that variable is not set.\n\n"
        "It must never raise, whatever `name` is. The starter sets `SPRINT_MODE` for "
        "you so there is something to find — keep that line."
    ),
    hint=(
        "`os.environ` behaves like a dict, and dicts have a lookup method that takes "
        "a second argument for the not-found case. Subscripting with `[...]` is the "
        "version that raises."
    ),
    solution=(
        "import os\n\n"
        'os.environ["SPRINT_MODE"] = "fast"\n\n\n'
        "def setting(name, fallback):\n"
        "    return os.environ.get(name, fallback)"
    ),
    explanation=(
        "`os.environ` is a snapshot taken when the process started; writing to it "
        "affects this process and any child it spawns, and can never reach back to "
        "the shell you launched from. `.get(name, fallback)` is the idiom because "
        "`os.environ[name]` raises `KeyError`, and configuration that is merely "
        "absent is usually not an error."
    ),
    starter=(
        "import os\n\n"
        'os.environ["SPRINT_MODE"] = "fast"  # so there is something to find\n\n\n'
        "def setting(name, fallback):\n    ..."
    ),
    cases=[
        Case(expected="fast", args=("SPRINT_MODE", "slow")),
        Case(expected="slow", args=("SPRINT_MODE_UNSET", "slow")),
        Case(expected=None, args=("SPRINT_MODE_UNSET", None)),
        Case(expected="unnamed", args=("", "unnamed")),
    ],
)

q(
    qid="Q-023",
    level=Level.L2,
    topic="Arithmetic",
    kind="function",
    entry="floor_negative",
    prompt=(
        "Write `floor_negative(a, b)` that returns `a // b`.\n\n"
        "That is the entire body. The work is predicting the four test cases before "
        "you run them — at least one of them is not what a C or JavaScript habit "
        "would tell you."
    ),
    hint=(
        "`//` is named *floor* division, not *integer* division, and the two words "
        "mean different things once a negative sign is involved. Picture the real "
        "quotient on a number line and ask which way you move off it."
    ),
    solution="def floor_negative(a, b):\n    return a // b",
    explanation=(
        "`//` rounds toward **negative infinity**, so `-7 // 2` is `-4` (the floor of "
        "`-3.5`) and not `-3`. C, Java, Go and JavaScript truncate toward zero "
        "instead, which is why modulo logic ported from those languages develops a "
        "sign bug on the first negative input. If you genuinely want truncation, "
        "`math.trunc(a / b)` says so out loud."
    ),
    starter="def floor_negative(a, b):\n    ...",
    cases=[
        Case(expected=3, args=(7, 2)),
        Case(expected=-4, args=(-7, 2)),
        Case(expected=-4, args=(7, -2)),
        Case(expected=3, args=(-7, -2)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-024",
    level=Level.L3,
    topic="Arithmetic",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "print(0.1 + 0.2 == 0.3)\n"
        "print(0.1 + 0.2)\n"
        "```\n\n"
        "Set `answer` to the two printed lines, e.g. "
        "`answer = \"True\\n3.0\"`. Get the second line exactly right, digit for digit."
    ),
    hint=(
        "A float is stored in base 2. Write 1/10 out in binary the way you would "
        "write 1/3 in decimal and ask where it has to stop."
    ),
    solution='answer = "False\\n0.30000000000000004"',
    explanation=(
        "None of `0.1`, `0.2` or `0.3` is exactly representable in binary, so the "
        "stored values are each slightly off and their sum lands one step above the "
        "stored `0.3`. `print` normally hides this by showing the shortest decimal "
        "string that round-trips back to the same float, which is why `0.1` looks "
        "clean on its own. Compare floats with `math.isclose`, and use "
        "`decimal.Decimal` when the base-10 digits themselves matter — money, above all."
    ),
    starter="answer = ...",
    cases=[Case(expected="False\n0.30000000000000004")],
)

q(
    qid="Q-025",
    level=Level.L3,
    topic="Identity",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "a = 256\nb = 256\nprint(a is b)\n\n"
        "c = 257\nd = 257\nprint(c is d)\n"
        "```\n\n"
        "Set `answer` to the two printed lines, e.g. `answer = \"True\\nFalse\"`."
    ),
    hint="CPython pre-creates a fixed pool of small integer objects at startup. Where does that pool stop?",
    solution='answer = "True\\nFalse"',
    explanation=(
        "CPython caches ints from -5 to 256, so `a` and `b` are literally the same "
        "object. 257 is outside the cache, so two separate objects are built and "
        "`is` is False — even though `==` is True for both. This is exactly why you "
        "compare values with `==` and only use `is` for `None`, `True` and `False`. "
        "The cache is an implementation detail: never write code that depends on it."
    ),
    starter="answer = ...",
    cases=[Case(expected="True\nFalse")],
)

q(
    qid="Q-026",
    level=Level.L3,
    topic="Casting",
    kind="function",
    entry="parse_number",
    prompt=(
        "Write `parse_number(text)` that turns a numeric string into a number, "
        "choosing the type by **value**, not by spelling:\n\n"
        "- return an `int` when the value is a whole number — so `\"3\"`, `\"3.0\"` "
        "and `\"-4.00\"` all give ints;\n"
        "- return a `float` otherwise.\n\n"
        "The checker is strict on type: `3.0` will not pass where `3` is expected. "
        "Assume the string always parses."
    ),
    hint=(
        "Only one of the two parsers accepts every input here, so it has to go first. "
        "Once you hold a float, it can tell you itself whether it has a fractional "
        "part — look for a method on `float`."
    ),
    solution=(
        "def parse_number(text):\n"
        "    value = float(text)\n"
        "    if value.is_integer():\n"
        "        return int(value)\n"
        "    return value"
    ),
    explanation=(
        "Parsing through `float` first is what lets one function accept both "
        "spellings, but it caps you at 53 bits of precision: a 20-digit integer "
        "string comes back rounded, so parse with `int()` directly when the input is "
        "known to be an integer. Keeping the distinction matters downstream — `int` "
        "and `float` hash the same but display differently, and only `int` stays exact."
    ),
    starter="def parse_number(text):\n    ...",
    cases=[
        Case(expected=3, args=("3",)),
        Case(expected=2.5, args=("2.5",)),
        Case(expected=3, args=("3.0",)),
        Case(expected=0, args=("-0.0",)),
        Case(expected=1000, args=("1e3",)),
    ],
)

q(
    qid="Q-027",
    level=Level.L3,
    topic="Arithmetic",
    kind="function",
    entry="wrap",
    prompt=(
        "Write `wrap(index, length)` that maps any integer `index` onto a valid "
        "position in a sequence of `length` items, wrapping around in both "
        "directions.\n\n"
        "`wrap(7, 5)` is `2` and `wrap(-1, 5)` is `4`. The result is always in "
        "`0..length-1`. `length` is always positive. No `if` statement is needed."
    ),
    hint=(
        "One operator already does this, including for negative input — the reason it "
        "works is the sign rule you met in Q-023. Ask what range `%` can possibly "
        "produce when the divisor is positive."
    ),
    solution="def wrap(index, length):\n    return index % length",
    explanation=(
        "Python's `%` takes the sign of the **divisor**, so for a positive `length` "
        "the result is guaranteed to land in `[0, length)` — the wrapping is free, "
        "with no guard clause. In C or JavaScript the same expression yields `-1` for "
        "`-1 % 5`, which is why code ported from those languages carries a stray "
        "`if (i < 0) i += n` that is dead weight here."
    ),
    starter="def wrap(index, length):\n    ...",
    cases=[
        Case(expected=2, args=(2, 5)),
        Case(expected=2, args=(7, 5)),
        Case(expected=4, args=(-1, 5)),
        Case(expected=3, args=(-7, 5)),
        Case(expected=0, args=(0, 5)),
    ],
)

q(
    qid="Q-028",
    level=Level.L3,
    topic="Logical",
    kind="custom",
    entry="xor",
    constraints=["no-builtin:bool", "max-lines:3"],
    prompt=(
        "Write `xor(a, b)` for boolean `a` and `b`: return `True` when exactly one "
        "of them is `True`, and `False` when they are both `True` or both "
        "`False`.\n\n"
        "Build it out of `and`, `or` and `not` only. No `^`, no `!=`, no `bool()`, "
        "no `if` — and the body must be at most 3 lines."
    ),
    hint=(
        "There are exactly two ways to satisfy 'one of them'. They are mirror images "
        "of each other, and `or` is what lets you accept either one."
    ),
    solution="def xor(a, b):\n    return (a and not b) or (b and not a)",
    explanation=(
        "`!=` happens to behave like xor here only because `bool` has exactly two "
        "values; it is a comparison, not a logical operator, and it stops agreeing "
        "the moment a truthy non-bool shows up (`1 != 2` is `True`, yet both are "
        "truthy). The prompt stipulates booleans for the same reason your answer "
        "needs them: `and`/`or` return an *operand*, so `xor(0, 0)` would hand back "
        "`0` rather than `False`."
    ),
    starter="def xor(a, b):\n    ...",
    cases=[
        Case(expected=False, args=(True, True)),
        Case(expected=True, args=(True, False)),
        Case(expected=True, args=(False, True)),
        Case(expected=False, args=(False, False)),
    ],
)

q(
    qid="Q-029",
    level=Level.L3,
    topic="Comparison",
    kind="function",
    entry="newest",
    prompt=(
        "Write `newest(records)` where `records` is a list of `(name, year, month)` "
        "tuples. Return the `name` of the most recent record.\n\n"
        "Later years win; within the same year, the later month wins. If two records "
        "tie exactly, return the one that appears first. For an empty list return "
        "`None`. Do not import a date library."
    ),
    hint=(
        "You are sorting by two fields with a priority between them. Python already "
        "compares sequences that way — so what shape should `max`'s `key` produce?"
    ),
    solution=(
        "def newest(records):\n"
        "    if not records:\n"
        "        return None\n"
        "    best = max(records, key=lambda r: (r[1], r[2]))\n"
        "    return best[0]"
    ),
    explanation=(
        "Tuples compare lexicographically — element 0 decides, and element 1 is only "
        "consulted on a tie — which is exactly the ordering a `(year, month)` date "
        "needs, with no library. `max` returns the **first** maximal item, a "
        "documented guarantee rather than an accident, so the tie-break in the prompt "
        "comes for free; `min` behaves the same way."
    ),
    starter="def newest(records):\n    ...",
    cases=[
        Case(expected="b", args=([("a", 2020, 5), ("b", 2021, 1), ("c", 2020, 12)],)),
        Case(expected="b", args=([("a", 2021, 3), ("b", 2021, 11)],)),
        Case(expected="solo", args=([("solo", 1999, 1)],)),
        Case(expected=None, args=([],)),
        Case(expected="first", args=([("first", 2020, 1), ("second", 2020, 1)],)),
    ],
)

q(
    qid="Q-030",
    level=Level.L3,
    topic="Dynamic Typing",
    kind="function",
    entry="describe",
    prompt=(
        "Write `describe(value)` that returns one of these strings:\n\n"
        "- `'bool'` for `True`/`False`\n"
        "- `'int'` for an integer\n"
        "- `'float'` for a float\n"
        "- `'str'` for a string\n"
        "- `'other'` for anything else\n\n"
        "Dispatch with `isinstance`, not with `type(value) is ...`. The order of your "
        "checks is the whole question."
    ),
    hint=(
        "`isinstance` answers 'is it this class *or a subclass of it*'. Two of the "
        "five types in that list stand in exactly that relationship — find them, and "
        "the ordering decides itself."
    ),
    solution=(
        "def describe(value):\n"
        "    if isinstance(value, bool):\n"
        '        return "bool"\n'
        "    if isinstance(value, int):\n"
        '        return "int"\n'
        "    if isinstance(value, float):\n"
        '        return "float"\n'
        "    if isinstance(value, str):\n"
        '        return "str"\n'
        '    return "other"'
    ),
    explanation=(
        "`bool` is a subclass of `int`, so `isinstance(True, int)` is `True` and an "
        "`int` branch placed first would silently swallow every boolean. The general "
        "rule for any `isinstance` chain is most-specific-first; `type(x) is int` "
        "avoids the problem but also rejects legitimate `int` subclasses, which is "
        "usually not what you want."
    ),
    starter="def describe(value):\n    ...",
    cases=[
        Case(expected="bool", args=(True,)),
        Case(expected="int", args=(1,)),
        Case(expected="float", args=(1.5,)),
        Case(expected="str", args=("x",)),
        Case(expected="other", args=(None,)),
        Case(expected="other", args=([1],)),
    ],
)

q(
    qid="Q-031",
    level=Level.L3,
    topic="Comparison",
    kind="custom",
    entry="status",
    constraints=["no-builtin:len"],
    prompt=(
        "Here is working but unidiomatic code:\n\n"
        "```python\n"
        "def status(flag, items):\n"
        "    if flag == True:\n"
        "        if len(items) > 0:\n"
        '            return "ready"\n'
        '        return "empty"\n'
        '    return "off"\n'
        "```\n\n"
        "Rewrite it so it behaves the same on booleans but also does the *right* "
        "thing for any truthy `flag` and any container `items`: `\"off\"` when `flag` "
        "is falsy, `\"ready\"` when `flag` is truthy and `items` is non-empty, "
        "`\"empty\"` when `flag` is truthy and `items` is empty.\n\n"
        "You may not call `len()`."
    ),
    hint=(
        "Both of those conditions ask a value to prove something it already knows how "
        "to report. What does `if` do to its condition before testing it?"
    ),
    solution=(
        "def status(flag, items):\n"
        "    if not flag:\n"
        '        return "off"\n'
        "    if items:\n"
        '        return "ready"\n'
        '    return "empty"'
    ),
    explanation=(
        "`flag == True` is a *narrower* test than truthiness — it passes only for "
        "`True` and `1`, so `2`, `\"yes\"` and a non-empty list all fail it even "
        "though every one of them is truthy. `len(items) > 0` makes a container count "
        "itself when you only wanted a yes/no; `if items:` asks `__bool__`, falls "
        "back to `__len__`, and works on generators and custom types where `len()` "
        "would raise."
    ),
    starter="def status(flag, items):\n    ...",
    cases=[
        Case(expected="ready", args=(True, [1, 2])),
        Case(expected="empty", args=(True, [])),
        Case(expected="off", args=(False, [1])),
        Case(expected="ready", args=(2, "abc")),
        Case(expected="ready", args=(True, [0])),
        Case(expected="off", args=(0, [])),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-032",
    level=Level.L4,
    topic="Casting",
    kind="function",
    entry="to_number",
    prompt=(
        "Write `to_number(text)`, a parser strict enough to trust with user input.\n\n"
        "Accept, ignoring surrounding whitespace: integer literals including "
        "underscores (`\"1_000\"` -> `1000`, an `int`), and finite decimal or "
        "exponent literals (`\"12.\"` -> `12.0`, `\"1e3\"` -> `1000.0`, both "
        "`float`). Return an `int` whenever the text is written as an integer, a "
        "`float` otherwise.\n\n"
        "Raise `ValueError` for everything else — including `\"\"`, `\"True\"`, "
        "`\"abc\"`, and also `\"nan\"` and `\"inf\"`.\n\n"
        "Note: `check()` can only exercise the values that parse; it cannot assert "
        "that something raises. Try `to_number(\"nan\")` in a cell yourself."
    ),
    hint=(
        "Two parsers tried in order, then one more check after the second succeeds. "
        "The last one exists because `float()` cheerfully accepts three strings that "
        "no price field should ever contain."
    ),
    solution=(
        "import math\n\n\n"
        "def to_number(text):\n"
        "    stripped = text.strip()\n"
        "    try:\n"
        "        return int(stripped)\n"
        "    except ValueError:\n"
        "        pass\n"
        "    value = float(stripped)  # raises ValueError on junk\n"
        "    if not math.isfinite(value):\n"
        '        raise ValueError(f"not a finite number: {text!r}")\n'
        "    return value"
    ),
    explanation=(
        "`float()` is far more permissive than people expect: it takes `\"1_000\"`, "
        "`\"12.\"`, `\"  3  \"` and — the one that gets shipped to production — "
        "`\"nan\"` and `\"inf\"`, so \"it parsed\" is not the same as \"it is a usable "
        "number\". A NaN then poisons every comparison downstream silently, because "
        "`nan < 1`, `nan > 1` and `nan == 1` are all `False`. Trying `int()` first is "
        "what preserves the integer type; `math.isfinite` is what closes the hole."
    ),
    starter="import math\n\n\ndef to_number(text):\n    ...",
    cases=[
        Case(expected=42, args=("42",)),
        Case(expected=-7, args=("  -7  ",)),
        Case(expected=1000, args=("1_000",)),
        Case(expected=12.0, args=("12.",)),
        Case(expected=3.5, args=("3.5",)),
        Case(expected=1000.0, args=("1e3",)),
        Case(expected=0, args=("0",)),
    ],
)

q(
    qid="Q-033",
    level=Level.L4,
    topic="Arithmetic",
    kind="function",
    entry="divide",
    prompt=(
        "Write `divide(a, b)` returning the tuple `(quotient, remainder)` for "
        "integers `a` and `b`, matching what `divmod(a, b)` gives — including every "
        "sign combination.\n\n"
        "When `b` is `0`, return `(None, None)` instead of raising.\n\n"
        "Derive it: floor the true quotient, then recover the remainder from it. Do "
        "not call `divmod`, and do not use `//` or `%`."
    ),
    hint=(
        "One identity has to hold for every pair: `a == b * quotient + remainder`. "
        "Pin down the quotient first — the word *floor* in 'floor division' is the "
        "instruction — and the remainder has no freedom left."
    ),
    solution=(
        "import math\n\n\n"
        "def divide(a, b):\n"
        "    if b == 0:\n"
        "        return (None, None)\n"
        "    quotient = math.floor(a / b)\n"
        "    return (quotient, a - b * quotient)"
    ),
    explanation=(
        "Python defines `a // b` as the floor of the exact quotient and then *derives* "
        "the remainder from `a == b * (a // b) + a % b`. Every sign rule you memorised "
        "falls out of that one identity: once the quotient rounds down, the remainder "
        "has to carry the divisor's sign. C, Java and Go satisfy the same identity "
        "with a truncating quotient, which is why ported modulo code breaks on the "
        "first negative input. (`math.floor(a / b)` routes through a float, so for "
        "integers beyond 2**53 the real `a // b` is the only exact route.)"
    ),
    starter="import math\n\n\ndef divide(a, b):\n    ...",
    cases=[
        Case(expected=(3, 1), args=(7, 2)),
        Case(expected=(-4, 1), args=(-7, 2)),
        Case(expected=(-4, -1), args=(7, -2)),
        Case(expected=(3, -1), args=(-7, -2)),
        Case(expected=(None, None), args=(5, 0)),
        Case(expected=(0, 0), args=(0, 7)),
    ],
)

q(
    qid="Q-034",
    level=Level.L4,
    topic="Primitive Types",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "print(True + True)\n"
        "print(isinstance(True, int))\n"
        'print({1: "a", True: "b"})\n'
        "```\n\n"
        "Set `answer` to the three printed lines. The third line is the one to think "
        "hardest about — give the dict exactly as Python would print it."
    ),
    hint=(
        "Start from what `bool` actually *is* in Python's type hierarchy. Then recall "
        "that a dict finds a key by hash first and equality second — never by type."
    ),
    solution='answer = "2\\nTrue\\n{1: \'b\'}"',
    explanation=(
        "`bool` is a subclass of `int` with `True == 1`, so booleans do arithmetic "
        "(`sum(flags)` counting the `True`s is the useful consequence). Because dict "
        "lookup goes by hash and then equality, `1` and `True` are the *same key*: "
        "the second entry overwrites the value but the dict keeps the key object it "
        "already had, so it prints `1` and not `True`. Mixing the two as keys loses "
        "data with no error at all."
    ),
    starter="answer = ...",
    cases=[Case(expected="2\nTrue\n{1: 'b'}")],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-035",
    level=Level.L5,
    topic="Comparison",
    kind="custom",
    entry="almost_equal",
    constraints=["no-builtin:isclose"],
    prompt=(
        "Reimplement `math.isclose` as "
        "`almost_equal(a, b, rel_tol=1e-09, abs_tol=0.0)`, returning a `bool`.\n\n"
        "It must agree with `math.isclose` on every input, so reproduce the full "
        "contract:\n\n"
        "- the test is `|a - b| <= max(rel_tol * max(|a|, |b|), abs_tol)`;\n"
        "- equal values are always close, and that includes `inf` and `inf`;\n"
        "- an infinity is close to nothing but itself;\n"
        "- `nan` is close to nothing at all, including another `nan`.\n\n"
        "You may use `math.isinf`/`math.isnan`, but not `math.isclose` itself."
    ),
    hint=(
        "Two special values have to be settled before any subtraction happens — one "
        "is equal to itself in a way `inf - inf` cannot express, and the other is "
        "equal to nothing. Only then does the tolerance formula apply, and it is the "
        "larger of two budgets, not the sum."
    ),
    solution=(
        "import math\n\n\n"
        "def almost_equal(a, b, rel_tol=1e-09, abs_tol=0.0):\n"
        "    if a == b:\n"
        "        return True\n"
        "    if math.isinf(a) or math.isinf(b):\n"
        "        return False\n"
        "    if math.isnan(a) or math.isnan(b):\n"
        "        return False\n"
        "    diff = abs(a - b)\n"
        "    return diff <= max(rel_tol * max(abs(a), abs(b)), abs_tol)"
    ),
    explanation=(
        "Taking the `max` of the two magnitudes is what makes the test symmetric — "
        "scaling by `|a|` alone would make `isclose(a, b)` and `isclose(b, a)` "
        "disagree near the boundary. The trap is the default `abs_tol=0.0`: nothing "
        "is ever *relatively* close to exactly zero, so any comparison against `0` "
        "needs an absolute tolerance you choose from the units of your problem. "
        "Handling `==` first is not an optimisation — it is the only way `inf` comes "
        "out close to itself, since `inf - inf` is `nan`."
    ),
    starter="import math\n\n\ndef almost_equal(a, b, rel_tol=1e-09, abs_tol=0.0):\n    ...",
    cases=[
        Case(expected=True, args=(1.0, 1.0000000001)),
        Case(expected=False, args=(1.0, 1.1)),
        Case(expected=False, args=(0.0, 1e-12)),
        Case(expected=True, args=(0.0, 1e-12), kwargs={"abs_tol": 1e-9}),
        Case(expected=True, args=(float("inf"), float("inf"))),
        Case(expected=False, args=(float("inf"), float("-inf"))),
        Case(expected=False, args=(float("nan"), float("nan"))),
        Case(expected=True, args=(1.0, 1.05), kwargs={"rel_tol": 0.1}),
    ],
)

q(
    qid="Q-036",
    level=Level.L5,
    topic="Arithmetic",
    kind="function",
    entry="py_round",
    prompt=(
        "Reimplement the builtin: `py_round(x, ndigits=0)` must agree with "
        "`round(x, ndigits)` on every input, including the ties.\n\n"
        "Round half to **even**: `0.5` -> `0`, `1.5` -> `2`, `2.5` -> `2`, "
        "`-0.5` -> `0`. And `py_round(2.675, 2)` is `2.67`, not `2.68`.\n\n"
        "Return an `int` when `ndigits` is `0`, a `float` otherwise. Do not call "
        "`round`.\n\n"
        "Warning: scaling by `10 ** ndigits` and rounding the product does *not* "
        "work — `2.675 * 100` is exactly `267.5`, which rounds the wrong way. You "
        "need the true value of the float, not an approximation of it."
    ),
    hint=(
        "The standard library has a numeric type that holds exact decimal values and "
        "lets you name the rounding mode. Constructing it from a `float` keeps the "
        "float's true binary value rather than the short string you see printed."
    ),
    solution=(
        "from decimal import ROUND_HALF_EVEN, Decimal\n\n\n"
        "def py_round(x, ndigits=0):\n"
        "    quantum = Decimal(1).scaleb(-ndigits)\n"
        "    value = Decimal(x).quantize(quantum, rounding=ROUND_HALF_EVEN)\n"
        "    return int(value) if ndigits == 0 else float(value)"
    ),
    explanation=(
        "Half-to-even exists because always rounding `.5` upward biases a long series "
        "of sums upward; alternating to the even neighbour cancels the error out, "
        "which is why accountants and IEEE 754 both specify it. The deeper lesson is "
        "the second one: most decimal 'ties' are not ties — `2.675` is stored "
        "slightly *below* 2.675, so `2.67` is the correct nearest answer and no "
        "rounding rule could have given `2.68`. `Decimal(x)` is exact about that "
        "because it takes the float's real binary value; `Decimal(\"2.675\")` would "
        "give you the other answer, and when base-10 digits are what you actually "
        "mean, that is the constructor you want."
    ),
    starter="def py_round(x, ndigits=0):\n    ...",
    cases=[
        Case(expected=0, args=(0.5,)),
        Case(expected=2, args=(1.5,)),
        Case(expected=2, args=(2.5,)),
        Case(expected=0, args=(-0.5,)),
        Case(expected=-2, args=(-1.5,)),
        Case(expected=3, args=(2.7,)),
        Case(expected=7, args=(7,)),
        Case(expected=2.67, args=(2.675, 2)),
        Case(expected=0.2, args=(0.25, 1)),
        Case(expected=0.3, args=(0.35, 1)),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-01",
    title="Receipt calculator",
    brief=(
        "Build `make_receipt(lines, tax_rate)`.\n\n"
        "`lines` is a list of `(name, qty_text, unit_price_text)` triples where the "
        "two numbers arrive as **strings**, the way they would from a form or a CSV. "
        "Return a dict:\n\n"
        "```python\n"
        "{'subtotal': 24.97, 'tax': 2.06, 'total': 27.03, 'items': 3}\n"
        "```\n\n"
        "Rules: quantities are whole numbers, prices have two decimals, every money "
        "value in the result is rounded to 2 decimal places, `items` is the total "
        "quantity (not the number of lines), and a malformed number raises "
        "`ValueError`. Tax is applied to the rounded subtotal."
    ),
    hint=(
        "Round once at each boundary, not continuously — compute the exact subtotal, "
        "round it, then derive tax from the rounded value. Rounding as you go makes "
        "the total disagree with the parts."
    ),
    solution=(
        "def make_receipt(lines, tax_rate):\n"
        "    subtotal = 0.0\n"
        "    items = 0\n"
        "    for name, qty_text, price_text in lines:\n"
        "        qty = int(qty_text)\n"
        "        price = float(price_text)\n"
        "        subtotal += qty * price\n"
        "        items += qty\n"
        "    subtotal = round(subtotal, 2)\n"
        "    tax = round(subtotal * tax_rate, 2)\n"
        "    return {\n"
        "        'subtotal': subtotal,\n"
        "        'tax': tax,\n"
        "        'total': round(subtotal + tax, 2),\n"
        "        'items': items,\n"
        "    }"
    ),
    explanation=(
        "This is the shape of most real input handling: strings in, numbers out, "
        "money rounded at defined boundaries. `int()` and `float()` already raise "
        "`ValueError` on junk, so the requirement is satisfied by not catching it — "
        "letting an exception propagate is a design choice, not an omission."
    ),
    entry="make_receipt",
    starter="def make_receipt(lines, tax_rate):\n    ...",
    cases=[
        Case(expected={"subtotal": 24.97, "tax": 2.06, "total": 27.03, "items": 3},
             args=([("pen", "2", "4.99"), ("pad", "1", "14.99")], 0.0825)),
        Case(expected={"subtotal": 0.0, "tax": 0.0, "total": 0.0, "items": 0},
             args=([], 0.0825)),
        Case(expected={"subtotal": 10.0, "tax": 0.0, "total": 10.0, "items": 10},
             args=([("nail", "10", "1.00")], 0.0)),
        Case(expected={"subtotal": 7.87, "tax": 0.79, "total": 8.66, "items": 9},
             args=([("bolt", "7", "1.11"), ("washer", "2", "0.05")], 0.10)),
    ],
)

NOTEBOOK = Notebook(
    number=1,
    slug="foundations_and_operators",
    title="Foundations & Operators",
    intro=(
        "Variables, the primitive types, dynamic typing, casting, and all five "
        "families of operator: arithmetic, comparison, logical, identity and "
        "membership.\n\n"
        "These are the questions everything else is built from. Do not skim them — "
        "the traps at the bottom of this notebook (`0.1 + 0.2`, `is` vs `==`, "
        "`True` being an `int`) are the ones that bite people three years in."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
