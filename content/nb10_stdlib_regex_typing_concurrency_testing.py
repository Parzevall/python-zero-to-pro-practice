"""Notebook 10 - Stdlib, Regex, Typing, Concurrency, Testing & Debugging
(Q-359..Q-400). The last notebook of the course."""

import math
import operator

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-359",
    level=Level.L1,
    topic="Modules",
    kind="function",
    entry="circle_area",
    prompt=(
        "Import the `math` module and write `circle_area(r)` that returns the area "
        "of a circle of radius `r`, rounded to 2 decimal places.\n\n"
        "`circle_area(1)` returns `3.14`. Use `math.pi` — do not type the digits "
        "yourself."
    ),
    hint=(
        "`import math` makes the whole module available under one name; you reach "
        "inside it with a dot. The constant you want is spelled in lowercase."
    ),
    solution=(
        "import math\n\n\n"
        "def circle_area(r):\n"
        "    return round(math.pi * r ** 2, 2)"
    ),
    explanation=(
        "`import math` binds one name and keeps every constant behind it, which is "
        "why `math.pi` reads unambiguously while `from math import *` would let a "
        "later assignment to `pi` silently shadow it. Modules are imported once per "
        "process and cached in `sys.modules`, so a second `import math` anywhere in "
        "your program costs nothing."
    ),
    starter="import math\n\n\ndef circle_area(r):\n    ...",
    cases=[
        Case(expected=3.14, args=(1,)),
        Case(expected=0.0, args=(0,)),
        Case(expected=12.57, args=(2,)),
        Case(expected=0.79, args=(0.5,)),
    ],
)

q(
    qid="Q-360",
    level=Level.L1,
    topic="Collections",
    kind="function",
    entry="tally",
    prompt=(
        "Write `tally(words)` that counts how often each word appears and returns "
        "the result as a **plain `dict`**.\n\n"
        "Use `collections.Counter` to do the counting, then convert. The checker is "
        "strict on type: a `Counter` will not pass where a `dict` is expected, even "
        "though the two compare equal."
    ),
    hint=(
        "`Counter(words)` does the whole count in one call. The only remaining job "
        "is changing the wrapper — the builtin that builds a dict from any mapping "
        "is the one you want."
    ),
    solution=(
        "from collections import Counter\n\n\n"
        "def tally(words):\n"
        "    return dict(Counter(words))"
    ),
    explanation=(
        "`Counter` is a `dict` subclass, so `==` says yes but `type(x) is dict` says "
        "no — and code that later does `json.dumps` or an `isinstance` check can "
        "care about the difference. Converting at the boundary of your function is "
        "the habit: use the rich type internally, hand back the plain one."
    ),
    starter="from collections import Counter\n\n\ndef tally(words):\n    ...",
    cases=[
        Case(expected={"a": 2, "b": 1}, args=(["a", "b", "a"],)),
        Case(expected={}, args=([],)),
        Case(expected={"x": 1}, args=(["x"],)),
        Case(expected={"a": 3}, args=(["a", "a", "a"],)),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-361",
    level=Level.L2,
    topic="Testing",
    kind="function",
    entry="assert_close",
    prompt=(
        "Write `assert_close(a, b, tol)` — the kind of helper a test suite is built "
        "from.\n\n"
        "It returns `None` when `abs(a - b) <= tol`, and raises `AssertionError` "
        "otherwise. Use the `assert` statement, and give it a message that names "
        "both values."
    ),
    hint=(
        "`assert <condition>, <message>` raises `AssertionError` with that message "
        "when the condition is falsy, and does nothing at all when it is truthy. A "
        "function that falls off the end returns `None` by itself."
    ),
    solution=(
        "def assert_close(a, b, tol):\n"
        '    assert abs(a - b) <= tol, f"{a} and {b} differ by more than {tol}"'
    ),
    explanation=(
        "pytest rewrites plain `assert` statements so the failure message shows the "
        "actual operand values — which is why you write `assert x == y` and not "
        "`self.assertEqual`. The message you attach is for the case the values alone "
        "cannot explain; leaving it off is fine, leaving the comparison vague is not. "
        "Remember `python -O` strips every `assert`, so never put real logic in one."
    ),
    starter="def assert_close(a, b, tol):\n    ...",
    cases=[
        Case(expected=None, args=(1.0, 1.0, 0.1)),
        Case(expected=None, args=(1.0, 1.05, 0.1)),
        Case(expected=None, args=(5, 5, 0)),
        Case(expected=None, args=(1.0, 2.0, 0.1), raises=AssertionError),
        Case(expected=None, args=(0.0, -3.0, 1.0), raises=AssertionError),
    ],
)

q(
    qid="Q-362",
    level=Level.L2,
    topic="Regex",
    kind="function",
    entry="find_numbers",
    prompt=(
        "Write `find_numbers(text)` that returns a **list of strings**: every run of "
        "consecutive digits in `text`, in order.\n\n"
        "`find_numbers(\"a1b22\")` returns `['1', '22']`. Return the matched text, "
        "not `int`s. Use `re.findall`."
    ),
    hint=(
        "`\\d` matches one digit; a quantifier turns it into a run. Write the pattern "
        "as a raw string so the backslash reaches the regex engine intact."
    ),
    solution=(
        "import re\n\n\n"
        "def find_numbers(text):\n"
        '    return re.findall(r"\\d+", text)'
    ),
    explanation=(
        "`re.findall` returns *all* non-overlapping matches as a list and never "
        "returns `None`, which makes it the easiest entry point into `re`. Always "
        "write patterns as raw strings: `\"\\d\"` happens to survive today but "
        "Python now warns about unknown escapes, and `\"\\b\"` really is a backspace "
        "character rather than a word boundary."
    ),
    starter="import re\n\n\ndef find_numbers(text):\n    ...",
    cases=[
        Case(expected=["1", "22", "333"], args=("a1b22c333",)),
        Case(expected=[], args=("none here",)),
        Case(expected=["42"], args=("42",)),
        Case(expected=["7"], args=("x-7y",)),
    ],
)

q(
    qid="Q-363",
    level=Level.L2,
    topic="JSON",
    kind="function",
    entry="to_json",
    prompt=(
        "Write `to_json(obj)` that serialises `obj` to a JSON **string** with the "
        "keys sorted alphabetically.\n\n"
        "`to_json({\"b\": 1, \"a\": 2})` returns `'{\"a\": 2, \"b\": 1}'` — note the "
        "default spacing, which you should not change."
    ),
    hint=(
        "One function in `json` turns an object into a string; its sibling reads a "
        "string back. The sorting is a keyword argument, not something you do "
        "yourself beforehand."
    ),
    solution=(
        "import json\n\n\n"
        "def to_json(obj):\n"
        "    return json.dumps(obj, sort_keys=True)"
    ),
    explanation=(
        "`dumps` makes a string and `dump` writes to a file — the trailing `s` is "
        "the only difference, and mixing them up is the single most common `json` "
        "mistake. `sort_keys=True` is what makes serialised output stable enough to "
        "diff or hash; without it you are at the mercy of insertion order."
    ),
    starter="import json\n\n\ndef to_json(obj):\n    ...",
    cases=[
        Case(expected='{"a": 2, "b": 1}', args=({"b": 1, "a": 2},)),
        Case(expected="[1, 2]", args=([1, 2],)),
        Case(expected="{}", args=({},)),
        Case(expected='{"a": null, "b": true}', args=({"a": None, "b": True},)),
    ],
)

q(
    qid="Q-364",
    level=Level.L2,
    topic="Datetime",
    kind="function",
    entry="days_between",
    prompt=(
        "Write `days_between(start, end)` where both arguments are ISO date strings "
        "like `\"2024-03-01\"`. Return the number of days from `start` to `end` as "
        "an **`int`**.\n\n"
        "The result is negative when `end` comes first. Do not call `today()` or "
        "`now()` — everything you need is in the arguments."
    ),
    hint=(
        "`datetime.date` has a classmethod that parses exactly this format. "
        "Subtracting two dates gives you a `timedelta`, which carries the number you "
        "want in one of its attributes."
    ),
    solution=(
        "from datetime import date\n\n\n"
        "def days_between(start, end):\n"
        "    return (date.fromisoformat(end) - date.fromisoformat(start)).days"
    ),
    explanation=(
        "`date.fromisoformat` handles leap years for you — 2024-01-01 to 2024-03-01 "
        "is 60 days, not 59 — which is the whole reason never to do date arithmetic "
        "by multiplying out days per month. `timedelta.days` is a whole number of "
        "days and can be negative; `.seconds` is the *remainder* within a day, not a "
        "total, and reading it as one is a classic bug."
    ),
    starter="from datetime import date\n\n\ndef days_between(start, end):\n    ...",
    cases=[
        Case(expected=60, args=("2024-01-01", "2024-03-01")),
        Case(expected=-60, args=("2024-03-01", "2024-01-01")),
        Case(expected=0, args=("2024-05-05", "2024-05-05")),
        Case(expected=1, args=("2023-12-31", "2024-01-01")),
    ],
)

q(
    qid="Q-365",
    level=Level.L2,
    topic="Random",
    kind="function",
    entry="roll",
    prompt=(
        "Write `roll(n)` that returns a list of `n` dice rolls — integers from 1 to "
        "6 inclusive.\n\n"
        "**Seed the generator with `random.seed(0)` as the first thing the function "
        "does**, so the same call always gives the same list. Use `random.randint`."
    ),
    hint=(
        "`random.randint(a, b)` includes both ends, unlike almost everything else in "
        "Python. Reseed on every call, not once at import, or the second call will "
        "continue the stream instead of restarting it."
    ),
    solution=(
        "import random\n\n\n"
        "def roll(n):\n"
        "    random.seed(0)\n"
        "    return [random.randint(1, 6) for _ in range(n)]"
    ),
    explanation=(
        "`random` is a deterministic pseudo-random generator: the seed fixes the "
        "entire stream, which is what makes a randomised test reproducible instead "
        "of a lottery. `randint(1, 6)` is inclusive on both ends while "
        "`randrange(1, 6)` stops at 5 — and for anything security-related you want "
        "`secrets`, never `random`."
    ),
    starter="import random\n\n\ndef roll(n):\n    ...",
    cases=[
        Case(expected=[4], args=(1,)),
        Case(expected=[4, 4, 1], args=(3,)),
        Case(expected=[4, 4, 1, 3, 5], args=(5,)),
        Case(expected=[], args=(0,)),
    ],
)

q(
    qid="Q-366",
    level=Level.L2,
    topic="Type Hints",
    kind="function",
    entry="mean",
    prompt=(
        "Write `mean` with **full type annotations**:\n\n"
        "```python\n"
        "def mean(values: list[float]) -> float:\n"
        "```\n\n"
        "Return the arithmetic mean as a `float`, and `0.0` for an empty list. Use "
        "the builtin generic `list[float]` — not `typing.List`, which has been "
        "deprecated since 3.9."
    ),
    hint=(
        "The annotation goes after a colon on the parameter and after an arrow "
        "before the body's colon. Guard the empty case first, or the division will "
        "raise."
    ),
    solution=(
        "def mean(values: list[float]) -> float:\n"
        "    if not values:\n"
        "        return 0.0\n"
        "    return sum(values) / len(values)"
    ),
    explanation=(
        "Annotations are stored on `mean.__annotations__` and are read by mypy, "
        "pyright and your editor — the interpreter itself never checks them (Q-377 "
        "makes that vivid). Since 3.9 the builtin containers are subscriptable "
        "directly, so `list[float]` needs no import at all."
    ),
    starter="def mean(values: list[float]) -> float:\n    ...",
    cases=[
        Case(expected=2.0, args=([1.0, 2.0, 3.0],)),
        Case(expected=0.0, args=([],)),
        Case(expected=5.0, args=([5.0],)),
        Case(expected=1.5, args=([1, 2],)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-367",
    level=Level.L3,
    topic="Collections",
    kind="function",
    entry="group_by_initial",
    prompt=(
        "Write `group_by_initial(words)` that groups words by their lowercased first "
        "letter.\n\n"
        "Return a **plain `dict`** mapping that letter to the list of words that "
        "start with it, each list in the order the words arrived. Build it with "
        "`collections.defaultdict(list)` and convert at the end.\n\n"
        "`group_by_initial([\"Ant\", \"ant\"])` returns `{'a': ['Ant', 'ant']}`."
    ),
    hint=(
        "`defaultdict(list)` calls `list()` for you the first time a key is touched, "
        "so you can append immediately with no `if key not in d` dance. Remember the "
        "return type is asked to be plain."
    ),
    solution=(
        "from collections import defaultdict\n\n\n"
        "def group_by_initial(words):\n"
        "    groups = defaultdict(list)\n"
        "    for word in words:\n"
        "        groups[word[0].lower()].append(word)\n"
        "    return dict(groups)"
    ),
    explanation=(
        "`defaultdict` removes the setdefault/`in` boilerplate that group-by code is "
        "otherwise made of, and because dicts preserve insertion order the groups "
        "come out in first-seen order for free. The catch is that *any* lookup "
        "creates the key — `groups[\"z\"]` in a debug print silently adds an empty "
        "list — so convert to a plain `dict` before you hand the result out."
    ),
    starter=(
        "from collections import defaultdict\n\n\n"
        "def group_by_initial(words):\n    ..."
    ),
    cases=[
        Case(expected={"a": ["apple", "avocado"], "b": ["banana"]},
             args=(["apple", "avocado", "banana"],)),
        Case(expected={}, args=([],)),
        Case(expected={"a": ["Ant", "ant"]}, args=(["Ant", "ant"],)),
        Case(expected={"z": ["zed"]}, args=(["zed"],)),
    ],
)

q(
    qid="Q-368",
    level=Level.L3,
    topic="Regex",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "import re\n"
        'print(re.match(r"\\d+", "abc123"))\n'
        'print(re.search(r"\\d+", "abc123").group())\n'
        'print(bool(re.match(r"\\d+", "123abc")))\n'
        "```\n\n"
        "Set `answer` to the three printed lines."
    ),
    hint=(
        "One of these two functions is allowed to start looking anywhere; the other "
        "is not. Neither of them requires the pattern to consume the *whole* string."
    ),
    solution='answer = "None\\n123\\nTrue"',
    explanation=(
        "`re.match` is anchored at position 0 and returns `None` the moment the "
        "pattern does not fit there, while `re.search` scans forward — the mismatch "
        "that produces the classic `AttributeError: 'NoneType' object has no "
        "attribute 'group'`. Neither anchors the *end*: `re.match(r\"\\d+\", "
        "\"123abc\")` succeeds on the prefix, so use `re.fullmatch` when you mean "
        "'the entire string'."
    ),
    starter="answer = ...",
    cases=[Case(expected="None\n123\nTrue")],
)

q(
    qid="Q-369",
    level=Level.L3,
    topic="Regex",
    kind="function",
    entry="parse_date",
    prompt=(
        "Write `parse_date(text)` that finds an ISO date anywhere in `text` — four "
        "digits, a dash, two digits, a dash, two digits — using **named groups** "
        "called `year`, `month` and `day`.\n\n"
        "Return a **plain `dict`** of the three captured **strings** (keep the "
        "leading zeros), or `None` when there is no such date."
    ),
    hint=(
        "A named group is written `(?P<name>...)`. A match object can hand you every "
        "named group at once as a dict — look for the method whose name says exactly "
        "that. And you must search, not match."
    ),
    solution=(
        "import re\n\n"
        'DATE_RE = re.compile(r"(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})")\n\n\n'
        "def parse_date(text):\n"
        "    found = DATE_RE.search(text)\n"
        "    if found is None:\n"
        "        return None\n"
        "    return found.groupdict()"
    ),
    explanation=(
        "Named groups turn a match into self-documenting code: `m[\"month\"]` "
        "survives someone inserting a group in front of it, `m.group(2)` does not. "
        "`groupdict()` hands back a real `dict` of strings — the regex engine never "
        "converts types, so `\"03\"` stays a string until you call `int` on it."
    ),
    starter="import re\n\n\ndef parse_date(text):\n    ...",
    cases=[
        Case(expected={"year": "2024", "month": "03", "day": "05"}, args=("2024-03-05",)),
        Case(expected={"year": "1999", "month": "12", "day": "31"},
             args=("date: 1999-12-31!",)),
        Case(expected=None, args=("nope",)),
        Case(expected=None, args=("24-3-5",)),
    ],
)

q(
    qid="Q-370",
    level=Level.L3,
    topic="Itertools",
    kind="function",
    entry="pairs",
    prompt=(
        "Write `pairs(items)` that returns a **list of 2-tuples**: every unordered "
        "pair of distinct positions, in the order `itertools.combinations` produces "
        "them.\n\n"
        "`pairs([1, 2, 3])` returns `[(1, 2), (1, 3), (2, 3)]`. A list with fewer "
        "than two items gives `[]`."
    ),
    hint=(
        "One `itertools` function produces exactly this and takes the group size as "
        "its second argument. It returns an iterator, so the result needs wrapping "
        "before you hand it back."
    ),
    solution=(
        "from itertools import combinations\n\n\n"
        "def pairs(items):\n"
        "    return list(combinations(items, 2))"
    ),
    explanation=(
        "`combinations` treats positions, not values, as distinct and emits them in "
        "input order — so it never produces both `(a, b)` and `(b, a)`, which is "
        "what separates it from `permutations`. Like every `itertools` function it "
        "returns a lazy iterator that is consumed once, so `list()` is not decoration."
    ),
    starter="from itertools import combinations\n\n\ndef pairs(items):\n    ...",
    cases=[
        Case(expected=[(1, 2), (1, 3), (2, 3)], args=([1, 2, 3],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=([1],)),
        Case(expected=[("a", "b")], args=(["a", "b"],)),
    ],
)

q(
    qid="Q-371",
    level=Level.L3,
    topic="Functools",
    kind="function",
    entry="product",
    prompt=(
        "Write `product(numbers)` that multiplies every number together and returns "
        "the result, using `functools.reduce`.\n\n"
        "The product of an empty list is `1`. Do not write an explicit loop."
    ),
    hint=(
        "`reduce(func, iterable, initial)` folds left, two items at a time. The third "
        "argument is not optional here — think about what `reduce` does when handed "
        "an empty sequence and nothing to start from."
    ),
    solution=(
        "from functools import reduce\n\n\n"
        "def product(numbers):\n"
        "    return reduce(lambda a, b: a * b, numbers, 1)"
    ),
    explanation=(
        "Without the `1`, `reduce` raises `TypeError` on an empty iterable — passing "
        "an explicit identity is what makes a fold total rather than a special case. "
        "`reduce` moved out of builtins in Python 3 because an explicit loop is "
        "usually clearer; reach for it when the operation genuinely is a fold, and "
        "prefer `math.prod` for this particular one."
    ),
    starter="from functools import reduce\n\n\ndef product(numbers):\n    ...",
    cases=[
        Case(expected=24, args=([1, 2, 3, 4],)),
        Case(expected=1, args=([],)),
        Case(expected=5, args=([5],)),
        Case(expected=0, args=([2, 0, 3],)),
    ],
)

q(
    qid="Q-372",
    level=Level.L3,
    topic="Pathlib",
    kind="function",
    entry="describe_path",
    prompt=(
        "Write `describe_path(text)` that takes a POSIX path as a string and returns "
        "the 4-tuple `(name, stem, suffix, parent)` — all four as **strings**.\n\n"
        "`describe_path(\"/var/log/app.log\")` returns "
        "`('app.log', 'app', '.log', '/var/log')`.\n\n"
        "Use `pathlib.PurePosixPath`, which does pure string surgery and never "
        "touches the disk. Note `parent` must be a `str`, not a path object."
    ),
    hint=(
        "Three of the four are attributes with exactly those names. The fourth is "
        "also an attribute, but it hands you a path object — convert it."
    ),
    solution=(
        "from pathlib import PurePosixPath\n\n\n"
        "def describe_path(text):\n"
        "    path = PurePosixPath(text)\n"
        "    return (path.name, path.stem, path.suffix, str(path.parent))"
    ),
    explanation=(
        "`pathlib` replaces a pile of `os.path` calls with attributes that read like "
        "the thing you want, and the `Pure*` variants are safe in tests because they "
        "never stat anything. Watch the double extension: the suffix of "
        "`notes.tar.gz` is `.gz` and the stem is `notes.tar` — `suffixes` (plural) is "
        "what gives you both."
    ),
    starter="from pathlib import PurePosixPath\n\n\ndef describe_path(text):\n    ...",
    cases=[
        Case(expected=("app.log", "app", ".log", "/var/log"), args=("/var/log/app.log",)),
        Case(expected=("notes.tar.gz", "notes.tar", ".gz", "."), args=("notes.tar.gz",)),
        Case(expected=("README", "README", "", "/tmp"), args=("/tmp/README",)),
        Case(expected=("b", "b", "", "a"), args=("a/b/",)),
    ],
)

q(
    qid="Q-373",
    level=Level.L3,
    topic="Collections",
    kind="function",
    entry="last_n",
    prompt=(
        "Write `last_n(items, n)` that returns a **list** of the last `n` items, in "
        "order — fewer than `n` if the input is shorter, and `[]` when `n` is `0`.\n\n"
        "Feed the items one at a time into a `collections.deque(maxlen=n)` and "
        "convert it at the end. The checker is strict: a `deque` is not a `list`."
    ),
    hint=(
        "A deque with a `maxlen` drops from the opposite end automatically as you "
        "append, so no slicing or length check is needed. `extend` does the feeding "
        "in one call."
    ),
    solution=(
        "from collections import deque\n\n\n"
        "def last_n(items, n):\n"
        "    window = deque(maxlen=n)\n"
        "    window.extend(items)\n"
        "    return list(window)"
    ),
    explanation=(
        "A bounded `deque` is the standard ring buffer: appending past `maxlen` "
        "discards from the far end in O(1), which `items[-n:]` cannot do when the "
        "items arrive from a stream you never want to hold in full. Beware `n == 0`, "
        "which makes a deque that discards everything — and beware `items[-0:]`, "
        "which returns the *whole* list rather than nothing."
    ),
    starter="from collections import deque\n\n\ndef last_n(items, n):\n    ...",
    cases=[
        Case(expected=[3, 4, 5], args=([1, 2, 3, 4, 5], 3)),
        Case(expected=[1, 2], args=([1, 2], 5)),
        Case(expected=[], args=([], 3)),
        Case(expected=[], args=([1, 2, 3], 0)),
    ],
)

q(
    qid="Q-374",
    level=Level.L3,
    topic="Concurrency",
    kind="predict",
    entry="answer",
    prompt=(
        "No code to run — decide `True` or `False` for each claim, one per line, in "
        "order:\n\n"
        "1. Splitting a pure-Python CPU-bound loop across 4 `threading.Thread`s "
        "makes it roughly 4x faster.\n"
        "2. Splitting 4 blocking network downloads across 4 `threading.Thread`s "
        "makes them finish sooner.\n"
        "3. Splitting the same pure-Python CPU-bound loop across 4 processes with "
        "`multiprocessing` makes it faster.\n\n"
        "Set `answer` to the three words, e.g. `answer = \"True\\nTrue\\nTrue\"`."
    ),
    hint=(
        "One lock in the interpreter decides all three. Ask what a thread is holding "
        "while it executes bytecode, and whether it is still holding it while it "
        "waits on a socket."
    ),
    solution='answer = "False\\nTrue\\nTrue"',
    explanation=(
        "CPython's Global Interpreter Lock lets exactly one thread execute bytecode "
        "at a time, so threads cannot add CPU throughput — but a thread *releases* "
        "the GIL while it blocks on I/O, which is why waiting in parallel works "
        "beautifully. Processes each get their own interpreter and their own GIL, at "
        "the cost of pickling everything that crosses between them. Hence the rule: "
        "threads (or `asyncio`) for I/O-bound work, processes for CPU-bound work."
    ),
    starter="answer = ...",
    cases=[Case(expected="False\nTrue\nTrue")],
)

q(
    qid="Q-375",
    level=Level.L3,
    topic="Testing",
    kind="function",
    entry="build_cases",
    prompt=(
        "`@pytest.mark.parametrize(\"a,b,expected\", CASES)` needs `CASES` to be a "
        "list of tuples, one tuple per run, with the arguments in the same order as "
        "the names in the string.\n\n"
        "Write `build_cases(func, arg_pairs)`: given a two-argument function and a "
        "list of `(a, b)` tuples, return the **list of 3-tuples** `(a, b, "
        "func(a, b))` — a parametrize table with the expected values filled in by "
        "calling the function."
    ),
    hint=(
        "One comprehension: unpack each pair, and put the call in the third slot. "
        "The shape of the result is what parametrize consumes, so keep it tuples "
        "inside a list."
    ),
    solution=(
        "def build_cases(func, arg_pairs):\n"
        "    return [(a, b, func(a, b)) for a, b in arg_pairs]"
    ),
    explanation=(
        "`parametrize` turns one test body into N independent tests, so a failure "
        "names the exact row instead of stopping at the first bad input — that is "
        "why it beats a `for` loop inside a single test. Generating the expected "
        "column by calling the function under test is a *characterisation* test: it "
        "pins current behaviour before a refactor, but it can never tell you that "
        "behaviour was right."
    ),
    starter="def build_cases(func, arg_pairs):\n    ...",
    cases=[
        Case(expected=[(1, 2, 3), (0, 0, 0)], args=(operator.add, [(1, 2), (0, 0)])),
        Case(expected=[], args=(operator.add, [])),
        Case(expected=[(2, 3, 6)], args=(operator.mul, [(2, 3)])),
        Case(expected=[(5, 2, 3)], args=(operator.sub, [(5, 2)])),
    ],
)

q(
    qid="Q-376",
    level=Level.L3,
    topic="Debugging",
    kind="predict",
    entry="answer",
    prompt=(
        "Here is a traceback exactly as Python printed it:\n\n"
        "```\n"
        "Traceback (most recent call last):\n"
        '  File "app.py", line 9, in <module>\n'
        "    main()\n"
        '  File "app.py", line 6, in main\n'
        '    return totals["gamma"]\n'
        "           ~~~~~~^^^^^^^^^\n"
        "KeyError: 'gamma'\n"
        "```\n\n"
        "Set `answer` to two lines: the name of the function where the error "
        "actually happened, then the `app.py` line number of the statement that "
        "raised. For example `answer = \"main\\n9\"`."
    ),
    hint=(
        "The header says *most recent call last*, so read the frames from the bottom "
        "up. The caret line underneath points at the sub-expression that blew up "
        "within its frame."
    ),
    solution='answer = "main\\n6"',
    explanation=(
        "A traceback is a call stack printed oldest-first, so the frame nearest the "
        "exception message — the bottom one — is where execution actually stopped; "
        "everything above it is just how you got there. Since 3.11 the `~~~^^^` "
        "markers narrow it further to the failing sub-expression, which is what tells "
        "you it was the subscript and not the `return`."
    ),
    starter="answer = ...",
    cases=[Case(expected="main\n6")],
)

q(
    qid="Q-377",
    level=Level.L3,
    topic="Type Hints",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def double(n: int) -> int:\n"
        "    return n * 2\n\n"
        'print(double("ab"))\n'
        'print(double.__annotations__["n"] is int)\n'
        "```\n\n"
        "Set `answer` to the two printed lines."
    ),
    hint=(
        "Ask what the interpreter *does* with an annotation when the function is "
        "called. Then ask what `*` means between a string and an integer."
    ),
    solution='answer = "abab\\nTrue"',
    explanation=(
        "Annotations are metadata, not a contract: nothing checks them at call time, "
        "so `double(\"ab\")` happily returns `'abab'` because `str * int` is valid "
        "Python. They are stored on `__annotations__` for mypy, pyright and your "
        "editor to read — if you want enforcement at runtime you have to opt in, with "
        "`pydantic`, `beartype`, or a check you write yourself."
    ),
    starter="answer = ...",
    cases=[Case(expected="abab\nTrue")],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-378",
    level=Level.L4,
    topic="Regex",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "import re\n"
        'text = "<a><b>"\n'
        'print(re.findall(r"<.*>", text))\n'
        'print(re.findall(r"<.*?>", text))\n'
        "```\n\n"
        "Set `answer` to the two printed lines, written exactly as Python prints a "
        "list of strings."
    ),
    hint=(
        "`*` takes as much as it can and only gives characters back when the rest of "
        "the pattern fails. The `?` after it reverses that appetite."
    ),
    solution="answer = \"['<a><b>']\\n['<a>', '<b>']\"",
    explanation=(
        "`.*` is greedy: it swallows to the end of the string and then backtracks to "
        "the *last* `>`, producing one match that spans both tags. `.*?` is lazy and "
        "stops at the first `>`, giving the two matches you meant. The sharper fix "
        "for markup-like input is a negated class, `<[^>]*>`, which cannot overshoot "
        "at all and so needs no backtracking."
    ),
    starter="answer = ...",
    cases=[Case(expected="['<a><b>']\n['<a>', '<b>']")],
)

q(
    qid="Q-379",
    level=Level.L4,
    topic="Regex",
    kind="function",
    entry="mask_digits",
    prompt=(
        "Write `mask_digits(text)` that replaces every run of digits with the same "
        "number of `#` characters, leaving everything else alone.\n\n"
        "`mask_digits(\"id 4821 x7\")` returns `'id #### x#'`.\n\n"
        "Use `re.sub` with a **function** as the replacement, not a fixed string — "
        "the length of each replacement depends on the match."
    ),
    hint=(
        "`re.sub(pattern, repl, text)` accepts a callable for `repl`; it is handed "
        "the match object and must return the replacement string. The match knows "
        "its own text."
    ),
    solution=(
        "import re\n\n\n"
        "def mask_digits(text):\n"
        '    return re.sub(r"\\d+", lambda m: "#" * len(m.group()), text)'
    ),
    explanation=(
        "A callable `repl` is the escape hatch for any substitution that has to "
        "compute something, and it sidesteps escaping entirely — the string it "
        "returns is used literally, so a `\\1` or `\\g<0>` in it means nothing. With "
        "a *string* `repl` the opposite is true: backslashes are interpreted as group "
        "references, which is how a stray `\\1` in replacement text turns into an "
        "`error: invalid group reference`."
    ),
    starter="import re\n\n\ndef mask_digits(text):\n    ...",
    cases=[
        Case(expected="id #### x#", args=("id 4821 x7",)),
        Case(expected="none", args=("none",)),
        Case(expected="", args=("",)),
        Case(expected="###", args=("007",)),
    ],
)

q(
    qid="Q-380",
    level=Level.L4,
    topic="Regex",
    kind="function",
    entry="settings_from",
    prompt=(
        "Write `settings_from(text)` that pulls `key=value` assignments out of a "
        "string and returns them as a **list of `(key, value)` tuples of strings**, "
        "in order.\n\n"
        "`settings_from(\"a=1;b=2\")` returns `[('a', '1'), ('b', '2')]`. Keys and "
        "values are runs of word characters; anything else is a separator and is "
        "ignored. Use `re.findall` with two capturing groups."
    ),
    hint=(
        "What `findall` gives back depends on how many groups your pattern has: none, "
        "one, or more than one all behave differently. Two groups is exactly the case "
        "that yields tuples."
    ),
    solution=(
        "import re\n\n\n"
        "def settings_from(text):\n"
        '    return re.findall(r"(\\w+)=(\\w+)", text)'
    ),
    explanation=(
        "`findall` has three modes and this is the third: with no groups it returns "
        "whole matches, with one group it returns that group's text, and with two or "
        "more it returns a tuple per match. Adding a group to an existing pattern "
        "therefore changes the *shape* of your results — which is what "
        "non-capturing `(?:...)` exists to prevent."
    ),
    starter="import re\n\n\ndef settings_from(text):\n    ...",
    cases=[
        Case(expected=[("a", "1"), ("b", "2")], args=("a=1;b=2",)),
        Case(expected=[], args=("",)),
        Case(expected=[("x", "9")], args=("x=9",)),
        Case(expected=[], args=("noequals",)),
        Case(expected=[("mode", "fast")], args=("  mode=fast  ",)),
    ],
)

q(
    qid="Q-381",
    level=Level.L4,
    topic="Concurrency",
    kind="function",
    entry="lengths",
    prompt=(
        "Write `lengths(texts)` that returns a **list of `int`s** — the length of "
        "each string, in the same order as the input.\n\n"
        "Do the work through a `concurrent.futures.ThreadPoolExecutor` with "
        "`max_workers=4`, using its `.map()`. Use the executor as a context manager "
        "so it shuts down cleanly, and convert the result to a list."
    ),
    hint=(
        "`pool.map(func, iterable)` mirrors the builtin `map` but runs the calls in "
        "worker threads. It returns a lazy iterator, and leaving the `with` block "
        "waits for every task to finish."
    ),
    solution=(
        "from concurrent.futures import ThreadPoolExecutor\n\n\n"
        "def lengths(texts):\n"
        "    with ThreadPoolExecutor(max_workers=4) as pool:\n"
        "        return list(pool.map(len, texts))"
    ),
    explanation=(
        "`Executor.map` keeps results in **input order** no matter which worker "
        "finishes first, which is what makes it a drop-in for `map` — use "
        "`as_completed` when you want them in completion order instead. It also "
        "re-raises a worker's exception at the point you consume that item, so a "
        "failure inside a thread is never silently lost. Exiting the `with` block "
        "calls `shutdown(wait=True)`."
    ),
    starter=(
        "from concurrent.futures import ThreadPoolExecutor\n\n\n"
        "def lengths(texts):\n    ..."
    ),
    cases=[
        Case(expected=[1, 3, 2], args=(["a", "bbb", "cc"],)),
        Case(expected=[], args=([],)),
        Case(expected=[1], args=(["x"],)),
        Case(expected=[0, 2], args=(["", "yy"],)),
    ],
)

q(
    qid="Q-382",
    level=Level.L4,
    topic="Collections",
    kind="function",
    entry="centroid",
    prompt=(
        "Write `centroid(pairs)` where `pairs` is a list of `(x, y)` tuples.\n\n"
        "Define `Point = namedtuple(\"Point\", \"x y\")`, wrap each pair in one, and "
        "compute the average position using **attribute access** (`p.x`, `p.y`) "
        "rather than indexing.\n\n"
        "Return a **plain `dict`** `{'x': ..., 'y': ...}` with both values as "
        "`float`s, or `None` for an empty list."
    ),
    hint=(
        "`Point(*pair)` unpacks a 2-tuple straight into the two fields. Dividing by "
        "the count with `/` already gives you floats, so no cast is needed."
    ),
    solution=(
        "from collections import namedtuple\n\n"
        'Point = namedtuple("Point", "x y")\n\n\n'
        "def centroid(pairs):\n"
        "    points = [Point(*pair) for pair in pairs]\n"
        "    if not points:\n"
        "        return None\n"
        "    n = len(points)\n"
        "    return {\n"
        '        "x": sum(p.x for p in points) / n,\n'
        '        "y": sum(p.y for p in points) / n,\n'
        "    }"
    ),
    explanation=(
        "A `namedtuple` *is* a tuple — same memory, same unpacking, still hashable "
        "and immutable — but `p.x` says what `p[0]` only implies, which is the whole "
        "value. Because it is a tuple it also compares equal to a plain one, so it "
        "slots into existing code with no changes; when you want defaults, mutability "
        "or methods, graduate to a `dataclass`."
    ),
    starter=(
        "from collections import namedtuple\n\n"
        'Point = namedtuple("Point", "x y")\n\n\n'
        "def centroid(pairs):\n    ..."
    ),
    cases=[
        Case(expected={"x": 1.0, "y": 1.0}, args=([(0, 0), (2, 2)],)),
        Case(expected=None, args=([],)),
        Case(expected={"x": 1.0, "y": 5.0}, args=([(1, 5)],)),
        Case(expected={"x": 1.0, "y": 0.0}, args=([(0, 0), (1, 0), (2, 0)],)),
    ],
)

q(
    qid="Q-383",
    level=Level.L4,
    topic="Collections",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "from collections import Counter\n"
        "a = Counter(a=3, b=1)\n"
        "b = Counter(a=3, b=2)\n"
        "print(a - b)\n"
        "print(a + b)\n"
        'print((a - b)["a"])\n'
        "```\n\n"
        "Set `answer` to the three printed lines, each written exactly as Python "
        "would show it."
    ),
    hint=(
        "`Counter` arithmetic is modelled on *multisets*, where a count below one "
        "means the element simply is not there. The third line asks a different "
        "question from the first two — what does a `Counter` do for a missing key?"
    ),
    solution="answer = \"Counter()\\nCounter({'a': 6, 'b': 3})\\n0\"",
    explanation=(
        "`+` and `-` between Counters **discard every count that is not positive**, "
        "so `a - b` drops `a` (3-3 = 0) and `b` (1-2 = -1) and leaves an empty "
        "Counter — the classic surprise when you use subtraction to compute a diff "
        "and the zeros vanish. Use `a.subtract(b)`, which mutates in place and keeps "
        "zero and negative counts, when you need them. Line three is the other half: "
        "indexing a missing key returns `0` rather than raising, and unlike "
        "`defaultdict` it does not insert the key."
    ),
    starter="answer = ...",
    cases=[Case(expected="Counter()\nCounter({'a': 6, 'b': 3})\n0")],
)

q(
    qid="Q-384",
    level=Level.L4,
    topic="Itertools",
    kind="function",
    entry="group_lengths",
    prompt=(
        "Write `group_lengths(words)` that groups words by their length using "
        "`itertools.groupby`.\n\n"
        "Return a **plain `dict`** mapping each length (an `int`) to the list of "
        "words of that length, with the words in their original relative order.\n\n"
        "`group_lengths([\"bb\", \"a\", \"ccc\", \"dd\"])` returns "
        "`{1: ['a'], 2: ['bb', 'dd'], 3: ['ccc']}`. There is one preparation step "
        "`groupby` requires that the prompt is deliberately not telling you."
    ),
    hint=(
        "`groupby` only ever compares each item with the one immediately before it. "
        "That means it can only find a group if equal keys are already adjacent — so "
        "something has to happen to the input first, with the same key function."
    ),
    solution=(
        "from itertools import groupby\n\n\n"
        "def group_lengths(words):\n"
        "    ordered = sorted(words, key=len)\n"
        "    return {k: list(g) for k, g in groupby(ordered, key=len)}"
    ),
    explanation=(
        "`itertools.groupby` breaks a stream into *runs* of consecutive equal keys — "
        "it is not SQL's GROUP BY — so unsorted input silently produces several "
        "groups with the same key and the last one wins in a dict. Sorting with the "
        "identical key function is the fix, and because `sorted` is stable the words "
        "keep their original relative order. The second trap: each group is a lazy "
        "iterator tied to the shared source, so it is empty as soon as you advance "
        "to the next group — `list(g)` has to happen now, not later."
    ),
    starter="from itertools import groupby\n\n\ndef group_lengths(words):\n    ...",
    cases=[
        Case(expected={1: ["a"], 2: ["bb", "dd"], 3: ["ccc"]},
             args=(["bb", "a", "ccc", "dd"],)),
        Case(expected={}, args=([],)),
        Case(expected={1: ["x"]}, args=(["x"],)),
        Case(expected={2: ["ab", "cd"]}, args=(["ab", "cd"],)),
    ],
)

q(
    qid="Q-385",
    level=Level.L4,
    topic="Functools",
    kind="custom",
    entry="fib",
    constraints=["needs-recursion"],
    prompt=(
        "Write `fib(n)` returning the nth Fibonacci number, with `fib(0) == 0` and "
        "`fib(1) == 1`.\n\n"
        "It must be **recursive** — `fib` has to call itself — and it must be "
        "decorated with `@functools.lru_cache(maxsize=None)`.\n\n"
        "One of the test cases is `fib(35)`. Without the cache that is about 30 "
        "million calls and takes seconds; with it, 36."
    ),
    hint=(
        "Write the naive two-call recursion first, then put one decorator line above "
        "the `def`. The decorator needs the arguments to be hashable, which plain "
        "`int`s are."
    ),
    solution=(
        "from functools import lru_cache\n\n\n"
        "@lru_cache(maxsize=None)\n"
        "def fib(n):\n"
        "    if n < 2:\n"
        "        return n\n"
        "    return fib(n - 1) + fib(n - 2)"
    ),
    explanation=(
        "`lru_cache` keys on the *arguments*, so the exponential recursion collapses "
        "to linear the moment the decorator is in place — the recursive calls go "
        "through the wrapper, which is what makes memoising a recursive function work "
        "at all. Two real costs to know: arguments must be hashable (no lists), and "
        "the cache holds a strong reference to every argument — so `@lru_cache` on a "
        "*method* keeps `self` alive forever and quietly leaks every instance. Cache "
        "the free function, or use `functools.cached_property` on the instance."
    ),
    starter=(
        "from functools import lru_cache\n\n\n"
        "@lru_cache(maxsize=None)\n"
        "def fib(n):\n    ..."
    ),
    cases=[
        Case(expected=0, args=(0,)),
        Case(expected=1, args=(1,)),
        Case(expected=55, args=(10,)),
        Case(expected=832040, args=(30,)),
        Case(expected=9227465, args=(35,)),
    ],
)

q(
    qid="Q-386",
    level=Level.L4,
    topic="Functools",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "from functools import partial\n\n"
        "def add_item(item, bucket=[]):\n"
        "    bucket.append(item)\n"
        "    return bucket\n\n"
        "push = partial(add_item)\n"
        'print(push("a"))\n'
        'print(push("b"))\n'
        "```\n\n"
        "Set `answer` to the two printed lines."
    ),
    hint=(
        "Ask when the default `[]` is evaluated: once, or once per call? `partial` "
        "changes nothing about that — it only remembers arguments you *did* pass."
    ),
    solution="answer = \"['a']\\n['a', 'b']\"",
    explanation=(
        "A default argument is evaluated **once**, when the `def` executes, and that "
        "single list is reused by every call that does not override it — so the "
        "bucket accumulates across calls forever. `partial` does not insulate you: it "
        "stores the arguments it was given and forwards the rest, leaving the "
        "function's own defaults exactly as they were. The fix is always the same: "
        "default to `None` and build the container inside the body."
    ),
    starter="answer = ...",
    cases=[Case(expected="['a']\n['a', 'b']")],
)

q(
    qid="Q-387",
    level=Level.L4,
    topic="File I/O",
    kind="custom",
    entry="wc",
    constraints=["needs-with"],
    prompt=(
        "Write `wc(text)` — a `wc`-style counter that returns the tuple "
        "`(line_count, word_count)`.\n\n"
        "The catch: it must read `text` through a **file-like object**, not by "
        "splitting the string directly. Wrap it in `io.StringIO` and open it with a "
        "`with` statement, then use `.readlines()`.\n\n"
        "A line is a line as `readlines()` sees it; words are whitespace-separated. "
        "`wc(\"\")` is `(0, 0)`."
    ),
    hint=(
        "`io.StringIO(text)` is an in-memory text file and supports the same context "
        "manager protocol as a real one. Counting words per line and summing is "
        "easier than one pass over the whole text."
    ),
    solution=(
        "import io\n\n\n"
        "def wc(text):\n"
        "    with io.StringIO(text) as handle:\n"
        "        lines = handle.readlines()\n"
        "    return (len(lines), sum(len(line.split()) for line in lines))"
    ),
    explanation=(
        "`with` guarantees the file is closed on every path out — exception included "
        "— which is the difference between a leaked handle and a program that runs "
        "for a month. Writing against `io.StringIO` instead of a real path is also "
        "the standard way to make I/O code testable: the function only needs "
        "*something file-shaped*, so tests need no `tmp_path`, no cleanup, and no "
        "disk. Note `.readlines()` keeps the `\\n` on each line, which is why "
        "`.split()` and not `len(line)` is doing the word counting."
    ),
    starter="import io\n\n\ndef wc(text):\n    ...",
    cases=[
        Case(expected=(2, 3), args=("a b\nc\n",)),
        Case(expected=(0, 0), args=("",)),
        Case(expected=(1, 4), args=("one line no newline",)),
        Case(expected=(2, 0), args=("\n\n",)),
    ],
)

q(
    qid="Q-388",
    level=Level.L4,
    topic="Datetime",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "from datetime import datetime, timezone\n\n"
        "naive = datetime(2024, 1, 1, 12, 0)\n"
        "aware = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)\n"
        "print(naive == aware)\n"
        "try:\n"
        "    print(naive < aware)\n"
        "except TypeError as exc:\n"
        "    print(type(exc).__name__)\n"
        "```\n\n"
        "Set `answer` to the two printed lines."
    ),
    hint=(
        "One of these two datetimes knows what part of the world it is in; the other "
        "does not. Equality and ordering do not have to agree about what to do with "
        "that — one of them can fall back on 'not the same thing'."
    ),
    solution='answer = "False\\nTypeError"',
    explanation=(
        "A naive datetime carries no `tzinfo`, so Python refuses to *order* it "
        "against an aware one — there is no defensible answer — and raises "
        "`TypeError: can't compare offset-naive and offset-aware datetimes`. "
        "Equality gets an exemption and simply returns `False` instead of raising, "
        "which is worse in practice: the bug sails through `==` and only detonates on "
        "the first `<`, `sorted()` or `min()`. Pick one convention per program; "
        "aware-UTC everywhere (`datetime.now(timezone.utc)`) is the one that scales."
    ),
    starter="answer = ...",
    cases=[Case(expected="False\nTypeError")],
)

q(
    qid="Q-389",
    level=Level.L4,
    topic="Type Hints",
    kind="function",
    entry="make_user",
    prompt=(
        "Declare a `TypedDict` describing a user record:\n\n"
        "```python\n"
        "class User(TypedDict):\n"
        "    name: str\n"
        "    age: int\n"
        "```\n\n"
        "Then write `make_user(name, age)` that returns such a record. Raise "
        "`ValueError` when `age` is negative.\n\n"
        "What comes back is an ordinary `dict` at runtime — the checker compares it "
        "as one."
    ),
    hint=(
        "A `TypedDict` is a type-checker construct, not a class you instantiate with "
        "attributes: build a normal dict literal with those keys. The validation is "
        "yours to write — the annotation will not do it."
    ),
    solution=(
        "from typing import TypedDict\n\n\n"
        "class User(TypedDict):\n"
        "    name: str\n"
        "    age: int\n\n\n"
        "def make_user(name, age):\n"
        "    if age < 0:\n"
        '        raise ValueError("age must not be negative")\n'
        '    user: User = {"name": name, "age": age}\n'
        "    return user"
    ),
    explanation=(
        "`TypedDict` gives a plain dict a *structural* type, so mypy flags a "
        "misspelled key or an `int` where a `str` belongs while the runtime object "
        "stays exactly a dict — no class, no overhead, and JSON-serialisable as-is. "
        "That is also its limit: nothing validates the actual data at runtime, which "
        "is why the `ValueError` has to be written by hand (and why `pydantic` exists "
        "for data arriving from outside your program)."
    ),
    starter=(
        "from typing import TypedDict\n\n\n"
        "class User(TypedDict):\n"
        "    name: str\n"
        "    age: int\n\n\n"
        "def make_user(name, age):\n    ..."
    ),
    cases=[
        Case(expected={"name": "Ada", "age": 36}, args=("Ada", 36)),
        Case(expected={"name": "Bo", "age": 0}, args=("Bo", 0)),
        Case(expected={"name": "", "age": 7}, args=("", 7)),
        Case(expected=None, args=("Cy", -1), raises=ValueError),
    ],
)

q(
    qid="Q-390",
    level=Level.L4,
    topic="Type Hints",
    kind="function",
    entry="apply_or",
    prompt=(
        "Write `apply_or` with this exact signature:\n\n"
        "```python\n"
        "def apply_or(\n"
        "    func: Optional[Callable[[int], int]], value: int, default: int\n"
        ") -> int:\n"
        "```\n\n"
        "Return `func(value)` when `func` is given, and `default` when it is `None`. "
        "Import `Callable` and `Optional` from `typing`.\n\n"
        "Test for `None` with `is`, not with truthiness."
    ),
    hint=(
        "`Callable[[int], int]` means 'takes one int, returns an int' — the first "
        "bracket is the argument *list*. `Optional[X]` is shorthand for `X | None`, "
        "which is exactly the case your body has to branch on."
    ),
    solution=(
        "from typing import Callable, Optional\n\n\n"
        "def apply_or(\n"
        "    func: Optional[Callable[[int], int]], value: int, default: int\n"
        ") -> int:\n"
        "    if func is None:\n"
        "        return default\n"
        "    return func(value)"
    ),
    explanation=(
        "`Optional[X]` does not mean 'may be omitted' — it means the value may be "
        "`None`, and a type checker will demand you narrow it before calling. "
        "Narrowing with `if func is None` is what does that; `if not func:` would "
        "compile but is wrong in principle, since a callable object can define "
        "`__bool__`. Modern code writes the same type as `Callable[[int], int] | "
        "None`, no import needed."
    ),
    starter=(
        "from typing import Callable, Optional\n\n\n"
        "def apply_or(\n"
        "    func: Optional[Callable[[int], int]], value: int, default: int\n"
        ") -> int:\n    ..."
    ),
    cases=[
        Case(expected=6, args=(abs, -6, 0)),
        Case(expected=0, args=(None, 5, 0)),
        Case(expected=-4, args=(operator.neg, 4, 0)),
        Case(expected=5, args=(math.isqrt, 26, 0)),
    ],
)

q(
    qid="Q-391",
    level=Level.L4,
    topic="Concurrency",
    kind="function",
    entry="parallel_count",
    prompt=(
        "Write `parallel_count(n_threads, per_thread)` that starts `n_threads` "
        "threads, has each one increment a single shared counter `per_thread` times, "
        "waits for all of them, and returns the final count as an `int`.\n\n"
        "Guard the increment with a `threading.Lock` so the answer is always exactly "
        "`n_threads * per_thread`. Start every thread before joining any of them."
    ),
    hint=(
        "`with lock:` around the increment is the whole synchronisation. Two separate "
        "loops — one to `start()`, one to `join()` — is what makes them run "
        "concurrently instead of one after another."
    ),
    solution=(
        "import threading\n\n\n"
        "def parallel_count(n_threads, per_thread):\n"
        "    total = 0\n"
        "    lock = threading.Lock()\n\n"
        "    def worker():\n"
        "        nonlocal total\n"
        "        for _ in range(per_thread):\n"
        "            with lock:\n"
        "                total += 1\n\n"
        "    threads = [threading.Thread(target=worker) for _ in range(n_threads)]\n"
        "    for thread in threads:\n"
        "        thread.start()\n"
        "    for thread in threads:\n"
        "        thread.join()\n"
        "    return total"
    ),
    explanation=(
        "`total += 1` is three bytecodes — load, add, store — and a thread switch "
        "between the load and the store loses an update, so the GIL protects the "
        "interpreter's own state but not yours. The lock makes the read-modify-write "
        "atomic; `with lock` releases it even if the body raises, which a manual "
        "`acquire()`/`release()` pair does not. Starting in one loop and joining in a "
        "second matters: `start(); join()` in the same loop runs them strictly "
        "sequentially."
    ),
    starter="import threading\n\n\ndef parallel_count(n_threads, per_thread):\n    ...",
    cases=[
        Case(expected=4000, args=(4, 1000)),
        Case(expected=0, args=(1, 0)),
        Case(expected=10, args=(2, 5)),
        Case(expected=800, args=(8, 100)),
    ],
)

q(
    qid="Q-392",
    level=Level.L4,
    topic="Concurrency",
    kind="function",
    entry="fetch_all",
    prompt=(
        "Write `fetch_all(values)` — an ordinary **synchronous** function that "
        "returns a **list** with each value doubled, but does the work with "
        "`asyncio`.\n\n"
        "Define an `async def` coroutine that doubles one value (with an `await "
        "asyncio.sleep(0)` in it to stand in for I/O), gather them all with "
        "`asyncio.gather`, and drive the whole thing from `fetch_all` with "
        "`asyncio.run(...)`.\n\n"
        "`fetch_all` itself must not be `async` — the caller sees a plain function."
    ),
    hint=(
        "`asyncio.run(coro)` is the single bridge from sync code into the event loop: "
        "it creates a loop, runs the coroutine to completion and closes the loop. "
        "`gather` takes the coroutines as separate arguments, so unpack with `*`."
    ),
    solution=(
        "import asyncio\n\n\n"
        "async def _double(value):\n"
        "    await asyncio.sleep(0)\n"
        "    return value * 2\n\n\n"
        "async def _main(values):\n"
        "    return await asyncio.gather(*(_double(v) for v in values))\n\n\n"
        "def fetch_all(values):\n"
        "    return asyncio.run(_main(values))"
    ),
    explanation=(
        "Calling an `async def` gives you a *coroutine object* and runs none of the "
        "body — the most common asyncio mistake is forgetting the `await` and "
        "wondering why nothing happened. `asyncio.gather` schedules them all "
        "concurrently and returns their results **in argument order**, not completion "
        "order. `asyncio.run` is the only entry point you should use from sync code, "
        "and it must not be called while a loop is already running (which is why it "
        "fails inside Jupyter, where a loop already exists)."
    ),
    starter="import asyncio\n\n\ndef fetch_all(values):\n    ...",
    cases=[
        Case(expected=[2, 4, 6], args=([1, 2, 3],)),
        Case(expected=[], args=([],)),
        Case(expected=[0], args=([0],)),
        Case(expected=[-2, 10], args=([-1, 5],)),
    ],
)

q(
    qid="Q-393",
    level=Level.L4,
    topic="Testing",
    kind="function",
    entry="run_with_fixture",
    prompt=(
        "A pytest *fixture* is a factory: every test that asks for it gets a freshly "
        "built object, never the one the previous test scribbled on.\n\n"
        "Write `run_with_fixture(factory, items)` that models this. For each item, "
        "call `factory()` to build a brand-new container, append the item to it, and "
        "collect that container. Return the **list of containers**.\n\n"
        "`run_with_fixture(list, [1, 2])` returns `[[1], [2]]` — not `[[1, 2], "
        "[1, 2]]`. Call `factory()` inside the loop, not once before it."
    ),
    hint=(
        "The whole question is where the `factory()` call goes. Hoisting it above "
        "the loop is the bug you are demonstrating, not an optimisation."
    ),
    solution=(
        "def run_with_fixture(factory, items):\n"
        "    results = []\n"
        "    for item in items:\n"
        "        state = factory()\n"
        "        state.append(item)\n"
        "        results.append(state)\n"
        "    return results"
    ),
    explanation=(
        "This is why a fixture is a function and not a module-level object: state "
        "built once at import is shared by every test, so test 7 starts failing "
        "because test 3 mutated it, and the suite passes or fails depending on "
        "*order*. pytest's `scope=` argument is exactly the dial between the two — "
        "`function` scope (the default) rebuilds per test, `session` scope shares one "
        "and asks you to keep it read-only."
    ),
    starter="def run_with_fixture(factory, items):\n    ...",
    cases=[
        Case(expected=[[1], [2]], args=(list, [1, 2])),
        Case(expected=[], args=(list, [])),
        Case(expected=[["a"]], args=(list, ["a"])),
        Case(expected=[[1], [1]], args=(list, [1, 1])),
    ],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-394",
    level=Level.L5,
    topic="Regex",
    kind="function",
    entry="tokenize",
    prompt=(
        "Write `tokenize(source)` — a real tokenizer for a tiny expression language, "
        "built from **one compiled regex** with named alternatives.\n\n"
        "Return a **list of `(kind, text)` tuples of strings**, where `kind` is one "
        "of:\n\n"
        "- `NUMBER` — digits, optionally followed by `.` and more digits\n"
        "- `NAME` — a letter or `_`, then letters/digits/underscores\n"
        "- `OP` — one of `+ - * / =`\n\n"
        "Whitespace is skipped and produces no token. Any other character raises "
        "`ValueError`.\n\n"
        "`tokenize(\"x = 1\")` returns `[('NAME', 'x'), ('OP', '='), "
        "('NUMBER', '1')]`."
    ),
    hint=(
        "Join the alternatives with `|` into one pattern, each in its own named "
        "group, and walk it with `finditer`. A match object's `lastgroup` tells you "
        "which alternative won. Add a final catch-all group so an illegal character "
        "matches something you can reject, rather than being silently skipped."
    ),
    solution=(
        "import re\n\n"
        "TOKEN_RE = re.compile(\n"
        '    r"(?P<NUMBER>\\d+(?:\\.\\d+)?)"\n'
        '    r"|(?P<NAME>[A-Za-z_]\\w*)"\n'
        '    r"|(?P<OP>[+\\-*/=])"\n'
        '    r"|(?P<SKIP>\\s+)"\n'
        '    r"|(?P<BAD>.)"\n'
        ")\n\n\n"
        "def tokenize(source):\n"
        "    tokens = []\n"
        "    for found in TOKEN_RE.finditer(source):\n"
        "        kind = found.lastgroup\n"
        '        if kind == "SKIP":\n'
        "            continue\n"
        '        if kind == "BAD":\n'
        '            raise ValueError(f"unexpected character {found.group()!r}")\n'
        "        tokens.append((kind, found.group()))\n"
        "    return tokens"
    ),
    explanation=(
        "This master-pattern approach is how `re` is used for real lexing — the "
        "standard library's own tokenizer example is built the same way — because one "
        "alternation with `lastgroup` beats trying each pattern in turn at every "
        "position. Two details carry the whole design. Alternation is **ordered and "
        "first-match-wins**, so `NUMBER` must precede `NAME` or `1x` tokenizes wrong, "
        "and `\\d+(?:\\.\\d+)?` uses a non-capturing group so it does not disturb "
        "`lastgroup`. And the trailing `(?P<BAD>.)` is what converts silence into an "
        "error: `finditer` simply skips text nothing matches, so without a catch-all "
        "a junk character vanishes and you debug a mystery instead of reading an "
        "exception."
    ),
    starter="import re\n\n\ndef tokenize(source):\n    ...",
    cases=[
        Case(expected=[("NAME", "x"), ("OP", "="), ("NUMBER", "1"), ("OP", "+"),
                       ("NUMBER", "2")],
             args=("x = 1 + 2",)),
        Case(expected=[], args=("",)),
        Case(expected=[("NUMBER", "3.5"), ("OP", "*"), ("NAME", "y")], args=("3.5*y",)),
        Case(expected=[("NAME", "_v1")], args=("_v1",)),
        Case(expected=None, args=("a $ b",), raises=ValueError),
    ],
)

q(
    qid="Q-395",
    level=Level.L5,
    topic="Itertools",
    kind="custom",
    entry="sliding_sums",
    constraints=["needs-generator"],
    prompt=(
        "Write `sliding_sums(values, size)` that returns a **list** of the sums of "
        "every contiguous window of length `size`.\n\n"
        "`sliding_sums([1, 2, 3, 4], 2)` returns `[3, 5, 7]`. When the input is "
        "shorter than the window, return `[]`. A `size` of `0` or less raises "
        "`ValueError`.\n\n"
        "The windows must be produced by a **generator** — define an inner `def` that "
        "`yield`s one sum at a time and materialise it with `list(...)` at the end. "
        "Slice each window with `itertools.islice`, not with `values[a:b]`."
    ),
    hint=(
        "Validate `size` before defining the generator, so the `ValueError` fires on "
        "the call and not on the first item pulled out. `range(len(values) - size + "
        "1)` gives the valid start positions — and goes empty on its own when the "
        "input is too short."
    ),
    solution=(
        "from itertools import islice\n\n\n"
        "def sliding_sums(values, size):\n"
        "    if size <= 0:\n"
        '        raise ValueError("size must be positive")\n\n'
        "    def windows():\n"
        "        for start in range(len(values) - size + 1):\n"
        "            yield sum(islice(values, start, start + size))\n\n"
        "    return list(windows())"
    ),
    explanation=(
        "Validating *before* the generator is defined is the real lesson: a `raise` "
        "inside a generator body does not happen when you call the function, it "
        "happens when something first iterates it — so a validating generator "
        "reports bad arguments at a stack frame far from the mistake. Splitting a "
        "plain wrapper around a generator core is the standard fix. `islice` also "
        "earns its place here: unlike a slice it works on any iterable and copies "
        "nothing, which is what lets the same shape run over a stream that never "
        "fits in memory."
    ),
    starter="from itertools import islice\n\n\ndef sliding_sums(values, size):\n    ...",
    cases=[
        Case(expected=[3, 5, 7], args=([1, 2, 3, 4], 2)),
        Case(expected=[], args=([1, 2], 5)),
        Case(expected=[], args=([], 3)),
        Case(expected=[5], args=([5], 1)),
        Case(expected=[6, 9], args=([1, 2, 3, 4], 3)),
        Case(expected=None, args=([1, 2, 3], 0), raises=ValueError),
    ],
)

q(
    qid="Q-396",
    level=Level.L5,
    topic="Type Hints",
    kind="function",
    entry="run_stack",
    prompt=(
        "Write a **generic** container and drive it.\n\n"
        "First `class Stack(Generic[T])` over `T = TypeVar(\"T\")`, with "
        "`push(item: T) -> None`, `pop() -> T` (raising `IndexError` when empty) and "
        "`__len__`.\n\n"
        "Then write `run_stack(ops)`: walk the list `ops`, and for each entry either "
        "pop (when the entry is the string `\"pop\"`) or push it. Return the tuple "
        "`(popped_values, remaining_length)` where `popped_values` is a **list** in "
        "the order they came off.\n\n"
        "`run_stack([1, 2, \"pop\"])` returns `([2], 1)`. Popping an empty stack "
        "propagates the `IndexError`."
    ),
    hint=(
        "`Generic[T]` in the base list is what makes `Stack[int]` legal to write; the "
        "class body itself is ordinary Python. Annotate the internal list as "
        "`list[T]` so the element type flows through."
    ),
    solution=(
        "from typing import Generic, TypeVar\n\n"
        'T = TypeVar("T")\n\n\n'
        "class Stack(Generic[T]):\n"
        "    def __init__(self) -> None:\n"
        "        self._items: list[T] = []\n\n"
        "    def push(self, item: T) -> None:\n"
        "        self._items.append(item)\n\n"
        "    def pop(self) -> T:\n"
        "        if not self._items:\n"
        '            raise IndexError("pop from empty stack")\n'
        "        return self._items.pop()\n\n"
        "    def __len__(self) -> int:\n"
        "        return len(self._items)\n\n\n"
        "def run_stack(ops):\n"
        "    stack: Stack[int] = Stack()\n"
        "    popped = []\n"
        "    for op in ops:\n"
        '        if op == "pop":\n'
        "            popped.append(stack.pop())\n"
        "        else:\n"
        "            stack.push(op)\n"
        "    return (popped, len(stack))"
    ),
    explanation=(
        "A `TypeVar` is a *link*, not a wildcard: it ties `push`'s argument to "
        "`pop`'s return value, so a checker knows `Stack[int]().pop()` is an `int` "
        "while `object` would have thrown that away. At runtime `Generic` does almost "
        "nothing — the subscript in `Stack[int]` is erased and no type is enforced — "
        "so this is a design tool, not a guard. Since 3.12 the same class is written "
        "`class Stack[T]:` with no `TypeVar` and no import; the older spelling is "
        "still what you will read in most code."
    ),
    starter=(
        "from typing import Generic, TypeVar\n\n"
        'T = TypeVar("T")\n\n\n'
        "class Stack(Generic[T]):\n    ...\n\n\n"
        "def run_stack(ops):\n    ..."
    ),
    cases=[
        Case(expected=([2], 1), args=([1, 2, "pop"],)),
        Case(expected=([], 0), args=([],)),
        Case(expected=([], 2), args=([3, 4],)),
        Case(expected=None, args=(["pop"],), raises=IndexError),
        Case(expected=None, args=([1, "pop", "pop"],), raises=IndexError),
    ],
)

q(
    qid="Q-397",
    level=Level.L5,
    topic="Concurrency",
    kind="function",
    entry="bounded_gather",
    prompt=(
        "Write `bounded_gather(values, limit)` — a synchronous function that squares "
        "every value concurrently, but never lets more than `limit` coroutines be "
        "inside the work section at once.\n\n"
        "Use an `asyncio.Semaphore(limit)` as an `async with`, have each coroutine "
        "`await asyncio.sleep(0.001)` while it holds the semaphore, and track the "
        "**peak** number of coroutines holding it simultaneously.\n\n"
        "Return the tuple `(results, peak)` — `results` a **list** of squares in "
        "input order, `peak` an `int`. For an empty input return `([], 0)`.\n\n"
        "Drive it all from `asyncio.run(...)`; `bounded_gather` itself is not "
        "`async`."
    ),
    hint=(
        "Keep a running `active` count and a `peak` in the enclosing coroutine and "
        "reach them with `nonlocal`. Increment right after acquiring and decrement "
        "before releasing — the peak then lands on `min(limit, len(values))`."
    ),
    solution=(
        "import asyncio\n\n\n"
        "def bounded_gather(values, limit):\n"
        "    async def main():\n"
        "        sem = asyncio.Semaphore(limit)\n"
        "        active = 0\n"
        "        peak = 0\n\n"
        "        async def work(value):\n"
        "            nonlocal active, peak\n"
        "            async with sem:\n"
        "                active += 1\n"
        "                peak = max(peak, active)\n"
        "                await asyncio.sleep(0.001)\n"
        "                active -= 1\n"
        "                return value * value\n\n"
        "        results = await asyncio.gather(*(work(v) for v in values))\n"
        "        return (results, peak)\n\n"
        "    return asyncio.run(main())"
    ),
    explanation=(
        "This is the shape of every real concurrent client: `gather` alone would fire "
        "ten thousand requests at once and get you rate-limited or out of sockets, so "
        "the semaphore turns 'all of them' into 'at most N of them' without changing "
        "the result or its order. Note that `active += 1` needs no lock here — a "
        "coroutine only yields at an `await`, so everything between two awaits is "
        "atomic, which is precisely the property threads do not give you (Q-391). "
        "`async with` releases the semaphore even when the body raises."
    ),
    starter="import asyncio\n\n\ndef bounded_gather(values, limit):\n    ...",
    cases=[
        Case(expected=([1, 4, 9, 16, 25], 2), args=([1, 2, 3, 4, 5], 2)),
        Case(expected=([], 0), args=([], 3)),
        Case(expected=([49], 1), args=([7], 5)),
        Case(expected=([1, 4], 2), args=([1, 2], 5)),
    ],
)

q(
    qid="Q-398",
    level=Level.L5,
    topic="Testing",
    kind="function",
    entry="run_suite",
    prompt=(
        "Write `run_suite(func, cases)` — a miniature test runner.\n\n"
        "`cases` is a list of `(args_tuple, expected)` pairs. For each one, call "
        "`func(*args_tuple)` and classify the outcome as the string `\"PASS\"` (the "
        "result equals `expected`), `\"FAIL\"` (it does not) or `\"ERROR\"` (the call "
        "raised).\n\n"
        "Return the tuple `(outcomes, summary)` where `outcomes` is the **list** of "
        "those strings in order and `summary` is a **plain `dict`** with the keys "
        "`\"PASS\"`, `\"FAIL\"` and `\"ERROR\"` — all three always present, counting "
        "`0` where nothing landed.\n\n"
        "A raising case must never stop the run."
    ),
    hint=(
        "`try` / `except Exception` / `else` gives you the three branches cleanly: "
        "the comparison belongs in `else`, so a `False` comparison is never confused "
        "with a raised one. Seed the summary with all three keys at zero before you "
        "start counting."
    ),
    solution=(
        "def run_suite(func, cases):\n"
        '    summary = {"PASS": 0, "FAIL": 0, "ERROR": 0}\n'
        "    outcomes = []\n"
        "    for args, expected in cases:\n"
        "        try:\n"
        "            got = func(*args)\n"
        "        except Exception:\n"
        '            outcome = "ERROR"\n'
        "        else:\n"
        '            outcome = "PASS" if got == expected else "FAIL"\n'
        "        outcomes.append(outcome)\n"
        "        summary[outcome] += 1\n"
        "    return (outcomes, summary)"
    ),
    explanation=(
        "Separating FAIL from ERROR is the distinction every real runner makes and "
        "beginners collapse: a wrong answer means your code is wrong, an exception "
        "usually means your *test* is wrong (bad arguments, missing fixture) and they "
        "want different first moves. Catching `Exception` rather than bare "
        "`except:` is what lets Ctrl-C still stop the suite, and running every case "
        "before reporting is why pytest shows you thirty failures at once instead of "
        "making you rerun thirty times."
    ),
    starter="def run_suite(func, cases):\n    ...",
    cases=[
        Case(expected=(["PASS", "FAIL"], {"PASS": 1, "FAIL": 1, "ERROR": 0}),
             args=(operator.add, [((1, 2), 3), ((1, 2), 4)])),
        Case(expected=(["ERROR"], {"PASS": 0, "FAIL": 0, "ERROR": 1}),
             args=(operator.truediv, [((1, 0), 0)])),
        Case(expected=([], {"PASS": 0, "FAIL": 0, "ERROR": 0}),
             args=(operator.add, [])),
        Case(expected=(["PASS"], {"PASS": 1, "FAIL": 0, "ERROR": 0}),
             args=(operator.mul, [((2, 3), 6)])),
    ],
)

q(
    qid="Q-399",
    level=Level.L5,
    topic="Debugging",
    kind="function",
    entry="last_frame",
    prompt=(
        "Write `last_frame(text)` that reads a traceback the way you do — bottom "
        "up — and reports where it actually broke.\n\n"
        "Frame lines look like `  File \"app.py\", line 6, in main` (always "
        "indented). The exception line is the last unindented line and looks like "
        "`KeyError: 'gamma'`.\n\n"
        "Return a **plain `dict`**:\n\n"
        "```python\n"
        "{'file': 'app.py', 'line': 6, 'func': 'main',\n"
        " 'type': 'KeyError', 'message': \"'gamma'\"}\n"
        "```\n\n"
        "from the **last** frame and the exception line. `line` is an `int`; the "
        "rest are strings. Return `None` if there is no frame or no exception line. "
        "Source-echo and `^^^^` marker lines are indented, so they must not be "
        "mistaken for either."
    ),
    hint=(
        "Two compiled patterns and one pass over `text.splitlines()`. Keep the most "
        "recent frame match rather than the first. The header line `Traceback (most "
        "recent call last):` is unindented too — make sure your exception pattern "
        "cannot match it."
    ),
    solution=(
        "import re\n\n"
        "FRAME_RE = re.compile(\n"
        "    r'^\\s+File \"(?P<file>[^\"]+)\", line (?P<line>\\d+), in (?P<func>.+)$'\n"
        ")\n"
        'EXC_RE = re.compile(r"^(?P<type>[A-Za-z_][\\w.]*): (?P<message>.*)$")\n\n\n'
        "def last_frame(text):\n"
        "    frame = None\n"
        "    exc = None\n"
        "    for raw in text.splitlines():\n"
        "        found = FRAME_RE.match(raw)\n"
        "        if found is not None:\n"
        "            frame = found\n"
        "            continue\n"
        '        if not raw.startswith(" "):\n'
        "            hit = EXC_RE.match(raw)\n"
        "            if hit is not None:\n"
        "                exc = hit\n"
        "    if frame is None or exc is None:\n"
        "        return None\n"
        "    return {\n"
        '        "file": frame["file"],\n'
        '        "line": int(frame["line"]),\n'
        '        "func": frame["func"],\n'
        '        "type": exc["type"],\n'
        '        "message": exc["message"],\n'
        "    }"
    ),
    explanation=(
        "Tracebacks are printed oldest-call-first, so 'the last frame wins' is the "
        "parsing rule that matches how you read one — and it is why log aggregators "
        "group errors by the bottom frame rather than the top. The indentation test "
        "is doing real work: it is the only thing separating the exception line from "
        "the echoed source and `~~~^^^` markers that sit between frames, and the "
        "`Traceback (most recent call last):` header is excluded for free because "
        "`Traceback` is not followed by `: `. In production, reach for the "
        "`traceback` module (`traceback.extract_tb`) instead of parsing text — but "
        "when all you have is a log file, this is the job."
    ),
    starter="import re\n\n\ndef last_frame(text):\n    ...",
    cases=[
        Case(
            expected={"file": "app.py", "line": 6, "func": "main",
                      "type": "KeyError", "message": "'gamma'"},
            args=(
                "Traceback (most recent call last):\n"
                '  File "app.py", line 9, in <module>\n'
                "    main()\n"
                '  File "app.py", line 6, in main\n'
                '    return totals["gamma"]\n'
                "           ~~~~~~^^^^^^^^^\n"
                "KeyError: 'gamma'\n",
            ),
        ),
        Case(
            expected={"file": "calc.py", "line": 2, "func": "divide",
                      "type": "ZeroDivisionError", "message": "division by zero"},
            args=(
                "Traceback (most recent call last):\n"
                '  File "calc.py", line 2, in divide\n'
                "    return a / b\n"
                "ZeroDivisionError: division by zero\n",
            ),
        ),
        Case(expected=None, args=("",)),
        Case(expected=None, args=("no traceback here\n",)),
    ],
)

q(
    qid="Q-400",
    level=Level.L5,
    topic="Functools",
    kind="custom",
    entry="run_cached",
    constraints=["no-builtin:lru_cache"],
    prompt=(
        "The last question of the course: rebuild `functools.lru_cache` from "
        "scratch.\n\n"
        "Write `memoize(maxsize)`, a decorator factory. The wrapper it returns "
        "caches results keyed on the positional arguments tuple, evicts the "
        "**least recently used** entry once the cache exceeds `maxsize`, and counts "
        "hits and misses. A *use* means a hit as well as a miss. Give the wrapper a "
        "`cache_info()` method returning the tuple "
        "`(hits, misses, maxsize, currsize)`, and preserve the wrapped function's "
        "metadata with `functools.wraps`.\n\n"
        "Then write `run_cached(maxsize, calls)`: define `square(n)` inside it, "
        "decorate it with `memoize(maxsize)`, call it once for each value in "
        "`calls` in order, and return the 4-tuple "
        "`(results, hits, misses, currsize)` — `results` a **list**.\n\n"
        "`run_cached(1, [5, 5, 5])` returns `([25, 25, 25], 2, 1, 1)`. You may not "
        "call `lru_cache`."
    ),
    hint=(
        "`collections.OrderedDict` gives you insertion order plus two methods that "
        "make LRU a two-liner: one moves a key to the most-recent end, the other "
        "pops from the least-recent end. Record the hit *before* moving the key, and "
        "evict only after inserting — check the size, do not pre-empt it."
    ),
    solution=(
        "from collections import OrderedDict\n"
        "from functools import wraps\n\n\n"
        "def memoize(maxsize):\n"
        "    def decorate(func):\n"
        "        cache = OrderedDict()\n"
        '        stats = {"hits": 0, "misses": 0}\n\n'
        "        @wraps(func)\n"
        "        def wrapper(*args):\n"
        "            if args in cache:\n"
        '                stats["hits"] += 1\n'
        "                cache.move_to_end(args)\n"
        "                return cache[args]\n"
        '            stats["misses"] += 1\n'
        "            result = func(*args)\n"
        "            cache[args] = result\n"
        "            if len(cache) > maxsize:\n"
        "                cache.popitem(last=False)\n"
        "            return result\n\n"
        "        def cache_info():\n"
        '            return (stats["hits"], stats["misses"], maxsize, len(cache))\n\n'
        "        wrapper.cache_info = cache_info\n"
        "        return wrapper\n\n"
        "    return decorate\n\n\n"
        "def run_cached(maxsize, calls):\n"
        "    @memoize(maxsize)\n"
        "    def square(n):\n"
        "        return n * n\n\n"
        "    results = [square(n) for n in calls]\n"
        "    hits, misses, _, currsize = square.cache_info()\n"
        "    return (results, hits, misses, currsize)"
    ),
    explanation=(
        "Three ideas meet here, and they are the three that make decorators worth "
        "learning. The closure is the storage: `cache` and `stats` live in "
        "`decorate`'s frame, one copy per decorated function, which is why you never "
        "needed a class. `OrderedDict.move_to_end` plus `popitem(last=False)` is the "
        "entire LRU policy — recency is just position, so eviction is O(1). And "
        "`@wraps` copies `__name__`, `__doc__` and `__wrapped__` across, without "
        "which every decorated function in your program reports itself as `wrapper` "
        "and `help()` goes blank. The real `lru_cache` adds thread safety, keyword "
        "arguments folded into the key, and a C implementation — but this is its "
        "shape, and you have now written it."
    ),
    starter=(
        "from collections import OrderedDict\n"
        "from functools import wraps\n\n\n"
        "def memoize(maxsize):\n    ...\n\n\n"
        "def run_cached(maxsize, calls):\n    ..."
    ),
    cases=[
        Case(expected=([1, 4, 1, 9, 4], 1, 4, 2), args=(2, [1, 2, 1, 3, 2])),
        Case(expected=([], 0, 0, 0), args=(128, [])),
        Case(expected=([25, 25, 25], 2, 1, 1), args=(1, [5, 5, 5])),
        Case(expected=([1, 1, 4, 4, 9], 2, 3, 3), args=(3, [1, 1, 2, 2, 3])),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-10",
    title="Log summariser",
    brief=(
        "Build `parse_log(lines)` — the tool you actually reach for when a service "
        "misbehaves.\n\n"
        "`lines` is a list of log lines, each shaped like:\n\n"
        "```\n"
        "2024-03-05 14:07:23 ERROR /srv/app/auth.py Login failed for user 7\n"
        "```\n\n"
        "that is: ISO date, space, `HH:MM:SS`, space, an uppercase level, space, a "
        "POSIX source path, space, then the message (which may contain spaces).\n\n"
        "Parse each line with **one compiled regex** and reduce the path to its "
        "filename with `pathlib.PurePosixPath`. Return a **plain `dict`**:\n\n"
        "```python\n"
        "{'total': 3,\n"
        " 'skipped': 0,\n"
        " 'by_level': {'ERROR': 2, 'INFO': 1},\n"
        " 'by_hour': {14: 2, 15: 1},\n"
        " 'by_file': {'auth.py': 2, 'db.py': 1},\n"
        " 'first_error': 'Login failed for user 7'}\n"
        "```\n\n"
        "Rules:\n\n"
        "- `total` counts lines that parsed; `skipped` counts non-blank lines that "
        "did not.\n"
        "- Blank or whitespace-only lines are ignored entirely — neither counted.\n"
        "- `by_hour` keys are **`int`** hours `0..23`, taken from the timestamp.\n"
        "- `by_level` and `by_file` contain only what was actually seen; all three "
        "sub-dicts are plain `dict`s, not `Counter`s.\n"
        "- `first_error` is the message of the first `ERROR` line, or `None` if "
        "there is none.\n"
        "- Nothing touches the filesystem, and nothing calls `now()`."
    ),
    hint=(
        "Named groups make the body readable: `date`, `time`, `level`, `path`, "
        "`message`. Strip each line first, skip it if it is empty, then `match` — "
        "anchoring at the start is what you want here. Count with three `Counter`s "
        "and convert them all to plain dicts in the return statement. The hour is "
        "`int(time[:2])`."
    ),
    solution=(
        "import re\n"
        "from collections import Counter\n"
        "from pathlib import PurePosixPath\n\n"
        "LINE_RE = re.compile(\n"
        '    r"^(?P<date>\\d{4}-\\d{2}-\\d{2}) "\n'
        '    r"(?P<time>\\d{2}:\\d{2}:\\d{2}) "\n'
        '    r"(?P<level>[A-Z]+) "\n'
        '    r"(?P<path>\\S+) "\n'
        '    r"(?P<message>.*)$"\n'
        ")\n\n\n"
        "def parse_log(lines):\n"
        "    levels = Counter()\n"
        "    hours = Counter()\n"
        "    files = Counter()\n"
        "    skipped = 0\n"
        "    first_error = None\n\n"
        "    for raw in lines:\n"
        "        line = raw.strip()\n"
        "        if not line:\n"
        "            continue\n"
        "        found = LINE_RE.match(line)\n"
        "        if found is None:\n"
        "            skipped += 1\n"
        "            continue\n"
        '        levels[found["level"]] += 1\n'
        '        hours[int(found["time"][:2])] += 1\n'
        '        files[PurePosixPath(found["path"]).name] += 1\n'
        '        if found["level"] == "ERROR" and first_error is None:\n'
        '            first_error = found["message"]\n\n'
        "    return {\n"
        '        "total": sum(levels.values()),\n'
        '        "skipped": skipped,\n'
        '        "by_level": dict(levels),\n'
        '        "by_hour": dict(hours),\n'
        '        "by_file": dict(files),\n'
        '        "first_error": first_error,\n'
        "    }"
    ),
    explanation=(
        "This is the whole notebook in one function: a compiled regex with named "
        "groups does the parsing, `Counter` does the aggregation, `PurePosixPath` "
        "does the path surgery without ever touching a disk, and the function stays "
        "**pure** — lines in, dict out. That purity is the design decision worth "
        "keeping. Every real version of this tool grows an `argparse` front end and "
        "an `open()`, and the moment those live inside the parsing function the "
        "whole thing becomes untestable. Keep the I/O in a thin shell at the edge "
        "and the logic in a function you can call with a list of strings, and you "
        "get a test suite that runs in milliseconds with no fixtures at all. The "
        "`skipped` counter is the other habit: real logs always contain lines your "
        "pattern does not cover, and counting them turns a silent gap into a number "
        "you can watch."
    ),
    entry="parse_log",
    starter=(
        "import re\n"
        "from collections import Counter\n"
        "from pathlib import PurePosixPath\n\n\n"
        "def parse_log(lines):\n    ..."
    ),
    cases=[
        Case(
            expected={
                "total": 3,
                "skipped": 0,
                "by_level": {"ERROR": 2, "INFO": 1},
                "by_hour": {14: 2, 15: 1},
                "by_file": {"auth.py": 2, "db.py": 1},
                "first_error": "Login failed for user 7",
            },
            args=([
                "2024-03-05 14:07:23 ERROR /srv/app/auth.py Login failed for user 7",
                "2024-03-05 14:09:01 INFO /srv/app/auth.py User 7 retried",
                "2024-03-05 15:00:00 ERROR /srv/app/db.py Connection reset",
            ],),
        ),
        Case(
            expected={
                "total": 0,
                "skipped": 0,
                "by_level": {},
                "by_hour": {},
                "by_file": {},
                "first_error": None,
            },
            args=([],),
        ),
        Case(
            expected={
                "total": 1,
                "skipped": 0,
                "by_level": {"INFO": 1},
                "by_hour": {0: 1},
                "by_file": {"boot.py": 1},
                "first_error": None,
            },
            args=(["2024-01-01 00:00:05 INFO /srv/app/boot.py Started"],),
        ),
        Case(
            expected={
                "total": 1,
                "skipped": 1,
                "by_level": {"WARN": 1},
                "by_hour": {1: 1},
                "by_file": {"cache.py": 1},
                "first_error": None,
            },
            args=([
                "not a log line",
                "",
                "2024-03-05 01:00:00 WARN /srv/app/cache.py Evicted 12 keys",
                "   ",
            ],),
        ),
    ],
)

NOTEBOOK = Notebook(
    number=10,
    slug="stdlib_regex_typing_concurrency_testing",
    title="Stdlib, Regex, Typing, Concurrency, Testing & Debugging",
    intro=(
        "The last notebook, and the hardest. Everything here is about the code "
        "*around* your code: the standard library you should not be rewriting, "
        "regular expressions, type hints, the three flavours of concurrency, and the "
        "two skills that decide how fast you fix things — writing tests and reading "
        "tracebacks.\n\n"
        "`collections`, `itertools` and `functools` are the three modules that most "
        "reliably delete lines from a codebase. Regex is where an afternoon "
        "disappears if you have never met greedy quantifiers or the difference "
        "between `match` and `search`. The concurrency questions are deliberately "
        "about *results*, not speed — the GIL decides whether threads help you at "
        "all, and knowing which side of that line your workload sits on is worth "
        "more than any API detail.\n\n"
        "Q-400 asks you to rebuild `functools.lru_cache`. It is the last question of "
        "the course on purpose: closures, decorators, `OrderedDict`, and an eviction "
        "policy, in about twenty lines. If you can write it, you can read the "
        "standard library."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
