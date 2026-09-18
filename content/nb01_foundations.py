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
    project=None,  # Task 8 sets this
)
