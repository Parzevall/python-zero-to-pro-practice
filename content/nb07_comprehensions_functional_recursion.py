"""Notebook 07 - Comprehensions, Functional & Recursion (Q-229..Q-270)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-229",
    level=Level.L1,
    topic="Comprehensions",
    kind="function",
    entry="squares",
    prompt=(
        "Write `squares(n)` that returns a **list** of the squares of `0` through "
        "`n - 1`, in order.\n\n"
        "`squares(4)` returns `[0, 1, 4, 9]`. Build it with a list comprehension — "
        "and note the checker wants a `list`, so round brackets will not do."
    ),
    hint=(
        "A list comprehension reads `[expression for name in iterable]`. `range(n)` "
        "already produces the numbers you need to square."
    ),
    solution="def squares(n):\n    return [i * i for i in range(n)]",
    explanation=(
        "A comprehension is a single *expression* that produces the whole list, which "
        "is why it can be returned directly instead of being built up with `.append()` "
        "in a loop. Swapping the brackets for parentheses gives a generator expression "
        "instead — a different type that the checker rejects, and a distinction Q-244 "
        "makes painful."
    ),
    starter="def squares(n):\n    ...",
    cases=[
        Case(expected=[0, 1, 4, 9], args=(4,)),
        Case(expected=[0], args=(1,)),
        Case(expected=[], args=(0,)),
        Case(expected=[0, 1, 4, 9, 16, 25], args=(6,)),
    ],
)

q(
    qid="Q-230",
    level=Level.L1,
    topic="Comprehensions",
    kind="function",
    entry="evens",
    prompt=(
        "Write `evens(nums)` that returns a **list** of the even numbers in `nums`, "
        "keeping the order they appear in.\n\n"
        "Use one list comprehension with an `if` filter clause — no `filter()`, no "
        "loop body."
    ),
    hint=(
        "The filter clause goes at the very end, after the `for`. A number is even "
        "when `n % 2` is `0`."
    ),
    solution="def evens(nums):\n    return [n for n in nums if n % 2 == 0]",
    explanation=(
        "A trailing `if` *drops* items, so the result can be shorter than the input — "
        "that is the whole difference between it and the `if`/`else` you will meet in "
        "Q-236, which sits in front of the `for` and only swaps values. Note `-2 % 2` "
        "is `0` in Python, so negatives need no special case."
    ),
    starter="def evens(nums):\n    ...",
    cases=[
        Case(expected=[2, 4], args=([1, 2, 3, 4],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=([1, 3, 5],)),
        Case(expected=[0, -2], args=([0, -2, 7],)),
    ],
)

q(
    qid="Q-231",
    level=Level.L1,
    topic="Comprehensions",
    kind="function",
    entry="shout",
    prompt=(
        "Write `shout(words)` that returns a **list of strings**: every word "
        "uppercased with a `!` stuck on the end.\n\n"
        "`shout(['hi'])` returns `['HI!']`. Use a list comprehension."
    ),
    hint=(
        "`.upper()` returns a new string rather than changing the original — strings "
        "cannot be changed at all. Concatenate the `!` onto what it hands back."
    ),
    solution='def shout(words):\n    return [w.upper() + "!" for w in words]',
    explanation=(
        "The expression slot of a comprehension can be any expression at all, method "
        "calls included, so there is never a reason to loop just to transform. Because "
        "strings are immutable, `w.upper()` cannot modify `words` — the comprehension "
        "builds a brand-new list and leaves the input untouched."
    ),
    starter="def shout(words):\n    ...",
    cases=[
        Case(expected=["HI!", "THERE!"], args=(["hi", "there"],)),
        Case(expected=[], args=([],)),
        Case(expected=["A!"], args=(["a"],)),
        Case(expected=["MIXED!", "CASE!"], args=(["Mixed", "CASE"],)),
    ],
)

q(
    qid="Q-232",
    level=Level.L1,
    topic="Built-ins",
    kind="function",
    entry="pair_up",
    prompt=(
        "Write `pair_up(names, scores)` that returns a **list of `(name, score)` "
        "tuples**, pairing them by position.\n\n"
        "Use `zip`. The lists may be different lengths — just let `zip` do whatever it "
        "does, and read the test cases carefully. The result must be a `list`, not a "
        "`zip` object."
    ),
    hint=(
        "`zip` is lazy: it hands back an iterator, not a list. One builtin call turns "
        "that into the list the checker wants."
    ),
    solution="def pair_up(names, scores):\n    return list(zip(names, scores))",
    explanation=(
        "`zip` stops as soon as its *shortest* input runs out, silently discarding the "
        "tail of the longer one — the classic way a row of data goes missing with no "
        "error at all. Since Python 3.10 `zip(a, b, strict=True)` raises `ValueError` "
        "instead, which is what you want whenever equal lengths are a real invariant."
    ),
    starter="def pair_up(names, scores):\n    ...",
    cases=[
        Case(expected=[("a", 1), ("b", 2)], args=(["a", "b"], [1, 2])),
        Case(expected=[], args=([], [])),
        Case(expected=[("a", 1)], args=(["a", "b", "c"], [1])),
        Case(expected=[("a", 1)], args=(["a"], [1, 2, 3])),
    ],
)

q(
    qid="Q-233",
    level=Level.L1,
    topic="Recursion",
    kind="custom",
    entry="factorial",
    constraints=["needs-recursion", "no-loops", "max-lines:4"],
    prompt=(
        "Write `factorial(n)` for a non-negative integer `n`, returning an `int`.\n\n"
        "`factorial(0)` is `1`, `factorial(5)` is `120`. Solve it **recursively**: no "
        "`for`, no `while`, no `math.factorial`, and at most 4 lines of body.\n\n"
        "Start by deciding which `n` needs no multiplication at all — that is your "
        "base case, and without one the function never stops."
    ),
    hint=(
        "Two lines of thought. Which input has an answer you already know outright? "
        "And for every other input, how do you express the answer in terms of the "
        "answer for a *smaller* input?"
    ),
    solution=(
        "def factorial(n):\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)"
    ),
    explanation=(
        "The base case is `n <= 1`, which returns `1` outright; every other call "
        "multiplies by `n` and hands `n - 1` onward, so the argument strictly "
        "decreases and is guaranteed to reach the base case. Leaving the base case out "
        "is the classic mistake, and Python's answer is a `RecursionError` at around "
        "1000 frames deep rather than a hang."
    ),
    starter="def factorial(n):\n    ...",
    cases=[
        Case(expected=1, args=(0,)),
        Case(expected=1, args=(1,)),
        Case(expected=120, args=(5,)),
        Case(expected=3628800, args=(10,)),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-234",
    level=Level.L2,
    topic="Comprehensions",
    kind="function",
    entry="lengths",
    prompt=(
        "Write `lengths(words)` that returns a **dict** mapping each word to its "
        "length.\n\n"
        "`lengths(['a', 'bbb'])` returns `{'a': 1, 'bbb': 3}`. Use a dict "
        "comprehension."
    ),
    hint=(
        "A dict comprehension differs from a set comprehension by one character: the "
        "colon. Its shape is `{key_expr: value_expr for name in iterable}`."
    ),
    solution="def lengths(words):\n    return {w: len(w) for w in words}",
    explanation=(
        "Both halves of the entry are ordinary expressions, so the key can be computed "
        "too — `{w.lower(): len(w) for w in words}` is just as valid. Duplicate keys do "
        "not error: the last one silently wins, which is why the result can come out "
        "shorter than the input and why a dict comprehension quietly deduplicates."
    ),
    starter="def lengths(words):\n    ...",
    cases=[
        Case(expected={"a": 1, "bbb": 3}, args=(["a", "bbb"],)),
        Case(expected={}, args=([],)),
        Case(expected={"x": 1}, args=(["x", "x"],)),
        Case(expected={"hi": 2, "there": 5, "!": 1}, args=(["hi", "there", "!"],)),
    ],
)

q(
    qid="Q-235",
    level=Level.L2,
    topic="Comprehensions",
    kind="function",
    entry="initials",
    prompt=(
        "Write `initials(words)` that returns a **set** of the first characters of "
        "the words, lowercased.\n\n"
        "`initials(['Apple', 'avocado'])` returns `{'a'}`. Words are never empty. Use "
        "a set comprehension; the checker rejects a list."
    ),
    hint=(
        "Curly braces with a single expression and no colon build a set. Do the "
        "lowercasing inside the comprehension so the deduplication actually sees "
        "matching values."
    ),
    solution='def initials(words):\n    return {w[0].lower() for w in words}',
    explanation=(
        "A set comprehension deduplicates as it builds, but only on the *final* value "
        "— lowercase after taking the character and `'A'` and `'a'` stay two separate "
        "entries. The odd corner is the empty case: `{}` is an empty dict, never an "
        "empty set, so `set()` is the only way to spell one."
    ),
    starter="def initials(words):\n    ...",
    cases=[
        Case(expected={"a", "b"}, args=(["Apple", "avocado", "Bee"],)),
        Case(expected=set(), args=([],)),
        Case(expected={"x"}, args=(["x"],)),
        Case(expected={"z"}, args=(["Zed", "zip", "Zoo"],)),
    ],
)

q(
    qid="Q-236",
    level=Level.L2,
    topic="Comprehensions",
    kind="function",
    entry="parities",
    prompt=(
        "Write `parities(nums)` that returns a **list of strings** — `'even'` or "
        "`'odd'` for each number, in order.\n\n"
        "The result is always the same length as the input, so this is *not* a filter. "
        "Use a conditional expression in the value slot of one comprehension."
    ),
    hint=(
        "The conditional expression is spelled `A if condition else B` and it goes "
        "**before** the `for`, where the value lives. An `if` after the `for` would "
        "throw items away instead."
    ),
    solution=(
        'def parities(nums):\n'
        '    return ["even" if n % 2 == 0 else "odd" for n in nums]'
    ),
    explanation=(
        "Position is the entire distinction: in front of the `for` an `if`/`else` "
        "chooses a *value* and the length is preserved; behind the `for` a bare `if` "
        "chooses whether the item survives at all. People reach for the filter form "
        "and then discover there is nowhere to put an `else` — that is the signal you "
        "wanted the ternary."
    ),
    starter="def parities(nums):\n    ...",
    cases=[
        Case(expected=["odd", "even", "odd"], args=([1, 2, 3],)),
        Case(expected=[], args=([],)),
        Case(expected=["even"], args=([0],)),
        Case(expected=["odd", "even"], args=([-3, -2],)),
    ],
)

q(
    qid="Q-237",
    level=Level.L2,
    topic="Built-ins",
    kind="function",
    entry="numbered",
    prompt=(
        "Write `numbered(items)` that returns a **list of strings** of the form "
        "`'1. first'`, `'2. second'`, numbering from **1**.\n\n"
        "Use `enumerate` with its `start` argument rather than adding 1 by hand."
    ),
    hint=(
        "`enumerate` yields `(index, value)` pairs, which a comprehension can unpack "
        "straight into two names. Its second argument decides where the count begins."
    ),
    solution=(
        "def numbered(items):\n"
        '    return [f"{i}. {item}" for i, item in enumerate(items, start=1)]'
    ),
    explanation=(
        "`for i in range(len(items))` is the tell of someone still thinking in C: it "
        "hands you an index and then makes you fetch the item yourself. `enumerate` "
        "gives both at once, works on anything iterable (including generators, where "
        "`len` would fail outright), and `start=1` removes the off-by-one arithmetic."
    ),
    starter="def numbered(items):\n    ...",
    cases=[
        Case(expected=["1. a", "2. b"], args=(["a", "b"],)),
        Case(expected=[], args=([],)),
        Case(expected=["1. only"], args=(["only"],)),
        Case(expected=["1. x", "2. y", "3. z"], args=(["x", "y", "z"],)),
    ],
)

q(
    qid="Q-238",
    level=Level.L2,
    topic="Built-ins",
    kind="function",
    entry="doubled",
    prompt=(
        "Write `doubled(nums)` that returns a **list** with every number doubled, "
        "built with `map`.\n\n"
        "The checker is strict on type: a `map` object is not a list and will not "
        "pass."
    ),
    hint=(
        "`map(fn, iterable)` applies `fn` to each item — but it does not apply "
        "anything until something asks it to. One more call is needed to get a real "
        "list out."
    ),
    solution="def doubled(nums):\n    return list(map(lambda n: n * 2, nums))",
    explanation=(
        "In Python 3 `map` and `filter` are **lazy iterators**, not lists: nothing is "
        "computed until you iterate, and once you have, they are exhausted and yield "
        "nothing the second time. That laziness is why `print(map(...))` shows "
        "`<map object at 0x...>` instead of your data, and why `list()` is nearly "
        "always the next thing you write."
    ),
    starter="def doubled(nums):\n    ...",
    cases=[
        Case(expected=[2, 4], args=([1, 2],)),
        Case(expected=[], args=([],)),
        Case(expected=[0, -6], args=([0, -3],)),
        Case(expected=[10], args=([5],)),
    ],
)

q(
    qid="Q-239",
    level=Level.L2,
    topic="Sorting",
    kind="function",
    entry="by_length",
    prompt=(
        "Write `by_length(words)` that returns a **new list** of the words ordered "
        "shortest first.\n\n"
        "Words of equal length must keep the order they had in the input, and the "
        "input list itself must not be modified."
    ),
    hint=(
        "One builtin returns a new list; the list *method* with a similar name sorts "
        "in place and returns `None`. Pass the length function itself as `key` — do "
        "not call it."
    ),
    solution="def by_length(words):\n    return sorted(words, key=len)",
    explanation=(
        "`sorted(xs)` returns a new list and leaves `xs` alone; `xs.sort()` mutates and "
        "returns `None`, so `return words.sort()` is the classic way to hand a caller "
        "`None`. `key=len` passes the function object — `key=len(words)` would call it "
        "once on the whole list and pass an integer, which is a `TypeError` later."
    ),
    starter="def by_length(words):\n    ...",
    cases=[
        Case(expected=["a", "bb", "ccc"], args=(["ccc", "a", "bb"],)),
        Case(expected=[], args=([],)),
        Case(expected=["bb", "aa"], args=(["bb", "aa"],)),
        Case(expected=["x"], args=(["x"],)),
    ],
)

q(
    qid="Q-240",
    level=Level.L2,
    topic="Sorting",
    kind="function",
    entry="top_n",
    prompt=(
        "Write `top_n(nums, n)` that returns a **list** of the `n` largest numbers, "
        "highest first.\n\n"
        "If `n` is larger than the list, return everything, still highest first. `n` "
        "is never negative."
    ),
    hint=(
        "Sort the whole thing in the direction you want with a keyword argument, then "
        "take a slice off the front. Slicing past the end of a list is not an error."
    ),
    solution="def top_n(nums, n):\n    return sorted(nums, reverse=True)[:n]",
    explanation=(
        "`reverse=True` reverses the *ordering*, which is not the same as sorting and "
        "then calling `.reverse()` — equal items keep their original relative order "
        "either way, which Q-248 makes visible. Slicing is forgiving by design: "
        "`[1, 2][:99]` is `[1, 2]`, so the short-list case needs no guard."
    ),
    starter="def top_n(nums, n):\n    ...",
    cases=[
        Case(expected=[5, 4, 3], args=([3, 1, 4, 1, 5], 3)),
        Case(expected=[], args=([], 2)),
        Case(expected=[1], args=([1], 5)),
        Case(expected=[2, 2], args=([2, 2, 2], 2)),
        Case(expected=[], args=([9, 8], 0)),
    ],
)

q(
    qid="Q-241",
    level=Level.L2,
    topic="Built-ins",
    kind="function",
    entry="checks",
    prompt=(
        "Write `checks(nums)` that returns the tuple "
        "`(is any number positive, are all numbers positive)` — two `bool`s.\n\n"
        "Use `any` and `all` over generator expressions. Think hard about the empty "
        "list before you look at the cases."
    ),
    hint=(
        "Both builtins take one iterable of truthy/falsy things, so the comparison "
        "`n > 0` belongs inside the expression you pass them. They disagree "
        "spectacularly when there is nothing to inspect."
    ),
    solution=(
        "def checks(nums):\n"
        "    return (any(n > 0 for n in nums), all(n > 0 for n in nums))"
    ),
    explanation=(
        "Both short-circuit — `any` stops at the first truthy item, `all` at the first "
        "falsy one — so feeding them a generator expression rather than a list means "
        "the rest is never computed. On an empty input `any` is `False` and `all` is "
        "`True`: 'all zero of them qualify' is vacuously true, and Q-247 is where that "
        "bites."
    ),
    starter="def checks(nums):\n    ...",
    cases=[
        Case(expected=(True, False), args=([1, -1],)),
        Case(expected=(True, True), args=([1, 2],)),
        Case(expected=(False, False), args=([-1, -2],)),
        Case(expected=(False, True), args=([],)),
        Case(expected=(False, False), args=([0],)),
    ],
)

q(
    qid="Q-242",
    level=Level.L2,
    topic="Recursion",
    kind="custom",
    entry="sum_list",
    constraints=["needs-recursion", "no-loops", "no-builtin:sum", "max-lines:4"],
    prompt=(
        "Write `sum_list(nums)` that adds up a list of numbers **recursively**.\n\n"
        "An empty list sums to `0`. No `for`, no `while`, no `sum()`, at most 4 lines "
        "of body.\n\n"
        "The shape to reach for: the total is the first item plus the total of "
        "everything after it."
    ),
    hint=(
        "Slicing gives you 'everything after the first item' in one expression. The "
        "base case is the list that has no first item at all."
    ),
    solution=(
        "def sum_list(nums):\n"
        "    if not nums:\n"
        "        return 0\n"
        "    return nums[0] + sum_list(nums[1:])"
    ),
    explanation=(
        "The base case is the empty list, whose sum is `0` — the identity for addition, "
        "not an arbitrary choice — and every call hands on a strictly shorter slice, so "
        "it always gets there. The hidden cost is that `nums[1:]` *copies* the tail "
        "each time, making this O(n^2); passing an index along instead is the standard "
        "fix, and Q-267 shows the other way out."
    ),
    starter="def sum_list(nums):\n    ...",
    cases=[
        Case(expected=6, args=([1, 2, 3],)),
        Case(expected=0, args=([],)),
        Case(expected=5, args=([5],)),
        Case(expected=-1, args=([-1, 1, -1],)),
    ],
)

q(
    qid="Q-243",
    level=Level.L2,
    topic="Recursion",
    kind="custom",
    entry="reverse_text",
    constraints=["needs-recursion", "no-loops"],
    prompt=(
        "Write `reverse_text(s)` that returns the string `s` reversed, "
        "**recursively**.\n\n"
        "`reverse_text('abc')` returns `'cba'` and the empty string reverses to "
        "itself. No loops, and `s[::-1]` on its own will not satisfy the checker — the "
        "function has to call itself."
    ),
    hint=(
        "Peel one character off the front and reverse what remains. Then the only "
        "decision left is which side of the join that peeled character goes on."
    ),
    solution=(
        "def reverse_text(s):\n"
        "    if not s:\n"
        '        return ""\n'
        "    return reverse_text(s[1:]) + s[0]"
    ),
    explanation=(
        "The base case is the empty string, which is already its own reverse; each call "
        "drops exactly one character so the length strictly decreases and termination "
        "is guaranteed. Putting `s[0]` first instead of last gives you the string back "
        "unchanged — a neat demonstration that recursion is about *where* you combine, "
        "not just that you recursed."
    ),
    starter="def reverse_text(s):\n    ...",
    cases=[
        Case(expected="cba", args=("abc",)),
        Case(expected="", args=("",)),
        Case(expected="a", args=("a",)),
        Case(expected="ba", args=("ab",)),
        Case(expected="racecar", args=("racecar",)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-244",
    level=Level.L3,
    topic="Generators",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "gen = (n * n for n in range(4))\n"
        "print(list(gen))\n"
        "print(list(gen))\n"
        "print(sum(n for n in range(4)))\n"
        "```\n\n"
        "Set `answer` to the three printed lines, e.g. `answer = \"[]\\n[]\\n0\"`."
    ),
    hint=(
        "A generator is not a container — it is a cursor that moves forward and never "
        "rewinds. Ask what is left to walk over the second time."
    ),
    solution='answer = "[0, 1, 4, 9]\\n[]\\n6"',
    explanation=(
        "A generator expression is **one-shot**: the first `list(gen)` drains it, and "
        "every later pass finds an exhausted iterator and produces an empty list "
        "without any error to warn you. That silence is the classic bug — assign a "
        "genexp to a name, use it twice, and the second use quietly sees nothing. If "
        "you need it more than once, materialise a list."
    ),
    starter="answer = ...",
    cases=[Case(expected="[0, 1, 4, 9]\n[]\n6")],
)

q(
    qid="Q-245",
    level=Level.L3,
    topic="Built-ins",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'print(list(zip([1, 2, 3], "xy")))\n'
        'print(dict(zip(["a", "b"], [1, 2, 3])))\n'
        "print(list(zip()))\n"
        "```\n\n"
        "Set `answer` to the three printed lines, spelled exactly as Python would "
        "print them."
    ),
    hint=(
        "A string is an iterable of characters, so `zip` is happy to take one. Then "
        "ask what `zip` does the moment any one of its inputs runs dry."
    ),
    solution="answer = \"[(1, 'x'), (2, 'y')]\\n{'a': 1, 'b': 2}\\n[]\"",
    explanation=(
        "`zip` stops at the **shortest** input and drops the rest without a word, which "
        "is how a column of data disappears from a report and nobody notices for a "
        "month. With no arguments at all it yields nothing. `zip(..., strict=True)` "
        "(3.10+) raises `ValueError` on a length mismatch and is the right default "
        "whenever equal lengths are an invariant rather than a hope."
    ),
    starter="answer = ...",
    cases=[Case(expected="[(1, 'x'), (2, 'y')]\n{'a': 1, 'b': 2}\n[]")],
)

q(
    qid="Q-246",
    level=Level.L3,
    topic="Comprehensions",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'n = "outer"\n'
        "squares = [n * n for n in range(3)]\n"
        "print(squares)\n"
        "print(n)\n"
        "```\n\n"
        "Set `answer` to the two printed lines. The second one is the whole question."
    ),
    hint=(
        "In Python 3 a comprehension runs in a scope of its own, rather like a "
        "function body. Ask which `n` the loop is binding, and whether anything "
        "outside can see it."
    ),
    solution='answer = "[0, 1, 4]\\nouter"',
    explanation=(
        "In Python 3 a comprehension gets its own scope, so its loop variable never "
        "leaks and the outer `n` survives untouched — in Python 2 this printed `2` and "
        "quietly clobbered your variable. The consequence people forget is the other "
        "direction: the comprehension can still *read* outer names, so a stray "
        "reference to an outer variable inside one compiles fine and silently uses the "
        "wrong value."
    ),
    starter="answer = ...",
    cases=[Case(expected="[0, 1, 4]\nouter")],
)

q(
    qid="Q-247",
    level=Level.L3,
    topic="Built-ins",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "print(any([]), all([]))\n"
        'print(any([0, ""]), all([1, "x"]))\n'
        "print(all([1, 0, 1]))\n"
        "```\n\n"
        "Set `answer` to the three printed lines. `print` with two arguments separates "
        "them with a single space."
    ),
    hint=(
        "Read each as a claim about the items: 'at least one qualifies' versus 'none "
        "fails'. Now apply both claims to a collection with no items in it."
    ),
    solution='answer = "False True\\nFalse True\\nFalse"',
    explanation=(
        "`all([])` is `True` because it asserts that *no* item fails, and an empty "
        "collection has no failing item — vacuous truth, the same reason `any([])` is "
        "`False`. This is why `if all(checks):` sails straight through when `checks` "
        "came back empty because of an earlier bug; guard the emptiness separately when "
        "'nothing to check' is not the same as 'everything passed'."
    ),
    starter="answer = ...",
    cases=[Case(expected="False True\nFalse True\nFalse")],
)

q(
    qid="Q-248",
    level=Level.L3,
    topic="Sorting",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'words = ["bb", "a", "cc", "d"]\n'
        "print(sorted(words, key=len))\n"
        "print(sorted(words, key=len, reverse=True))\n"
        "```\n\n"
        "Set `answer` to the two printed lines. Pay attention to the order of the "
        "items that tie on length."
    ),
    hint=(
        "Python's sort is *stable*. Work out what that guarantees for two items the "
        "key cannot tell apart — and then whether `reverse=True` changes that "
        "guarantee."
    ),
    solution="answer = \"['a', 'd', 'bb', 'cc']\\n['bb', 'cc', 'a', 'd']\"",
    explanation=(
        "Stability means items with equal keys keep their input order, and "
        "`reverse=True` is explicitly *not* 'sort then reverse the list' — it flips "
        "the comparison while ties stay in input order, so `'bb'` still precedes "
        "`'cc'`. That guarantee is what lets you sort by a secondary key first and a "
        "primary key second to get a multi-key ordering out of two plain sorts."
    ),
    starter="answer = ...",
    cases=[Case(expected="['a', 'd', 'bb', 'cc']\n['bb', 'cc', 'a', 'd']")],
)

q(
    qid="Q-249",
    level=Level.L3,
    topic="Nested Comprehensions",
    kind="custom",
    entry="flatten_grid",
    constraints=["needs-comprehension", "no-loops"],
    prompt=(
        "Write `flatten_grid(rows)`, where `rows` is a list of lists. Return a single "
        "**flat list** of every value, row by row.\n\n"
        "`flatten_grid([[1, 2], [3]])` returns `[1, 2, 3]`. Use **one** comprehension "
        "with two `for` clauses — no `for` statement, no `sum(rows, [])`, no "
        "`itertools`."
    ),
    hint=(
        "Two `for` clauses sit side by side inside the brackets. Write out the "
        "equivalent nested `for` statements first: the clauses go in exactly that same "
        "order, outer one first."
    ),
    solution=(
        "def flatten_grid(rows):\n"
        "    return [value for row in rows for value in row]"
    ),
    explanation=(
        "The clauses read left to right in the same order you would nest the loops, so "
        "`for row in rows` must come first — writing the inner one first is the "
        "classic mistake and gives `NameError: name 'row' is not defined`. This only "
        "flattens one level; arbitrary nesting needs the recursion of Q-257."
    ),
    starter="def flatten_grid(rows):\n    ...",
    cases=[
        Case(expected=[1, 2, 3], args=([[1, 2], [3]],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=([[], []],)),
        Case(expected=[1, 2, 3], args=([[1], [2], [3]],)),
        Case(expected=["a", "b"], args=([["a"], [], ["b"]],)),
    ],
)

q(
    qid="Q-250",
    level=Level.L3,
    topic="Nested Comprehensions",
    kind="custom",
    entry="transpose",
    constraints=["needs-comprehension", "no-builtin:zip"],
    prompt=(
        "Write `transpose(rows)` that turns a rectangular list of lists on its side: "
        "columns become rows. Return a **list of lists**.\n\n"
        "`transpose([[1, 2, 3], [4, 5, 6]])` returns `[[1, 4], [2, 5], [3, 6]]`. Every "
        "row has the same length; an empty input returns `[]`. Do **not** use `zip` — "
        "build it with a comprehension inside a comprehension."
    ),
    hint=(
        "The output has one entry per *column*, so the outer loop runs over column "
        "indices. The inner comprehension collects that one index from each row."
    ),
    solution=(
        "def transpose(rows):\n"
        "    if not rows:\n"
        "        return []\n"
        "    return [[row[i] for row in rows] for i in range(len(rows[0]))]"
    ),
    explanation=(
        "A nested comprehension in the *value* slot is a different thing from the two "
        "`for` clauses of Q-249: here the inner brackets build a whole list per outer "
        "item, which is why the result is a list of lists rather than flat. `zip(*rows)` "
        "does the same job in one call but yields **tuples**, so `list(zip(*rows))` "
        "would fail this question's type check outright."
    ),
    starter="def transpose(rows):\n    ...",
    cases=[
        Case(expected=[[1, 4], [2, 5], [3, 6]], args=([[1, 2, 3], [4, 5, 6]],)),
        Case(expected=[], args=([],)),
        Case(expected=[[1]], args=([[1]],)),
        Case(expected=[[1], [2]], args=([[1, 2]],)),
        Case(expected=[["a", "c"], ["b", "d"]], args=([["a", "b"], ["c", "d"]],)),
    ],
)

q(
    qid="Q-251",
    level=Level.L3,
    topic="Comprehensions",
    kind="function",
    entry="invert",
    prompt=(
        "Write `invert(d)` that returns a **dict** with keys and values swapped.\n\n"
        "`invert({'a': 1})` returns `{1: 'a'}`. The values are hashable and distinct, "
        "so no two keys collide. Use a dict comprehension over `.items()`."
    ),
    hint=(
        "`.items()` yields `(key, value)` pairs, and a comprehension's `for` clause can "
        "unpack a pair into two names directly. Then write them back in the other "
        "order."
    ),
    solution="def invert(d):\n    return {v: k for k, v in d.items()}",
    explanation=(
        "Unpacking in the `for` clause (`for k, v in d.items()`) is what keeps this to "
        "one readable line instead of indexing a tuple. The promise in the prompt is "
        "doing real work: repeated values collapse into one key with the last one "
        "winning, so inverting a non-injective dict loses entries silently — when that "
        "is possible, map each value to a *list* of keys instead, as Q-270 does."
    ),
    starter="def invert(d):\n    ...",
    cases=[
        Case(expected={1: "a"}, args=({"a": 1},)),
        Case(expected={}, args=({},)),
        Case(expected={1: "a", 2: "b"}, args=({"a": 1, "b": 2},)),
        Case(expected={"y": "x"}, args=({"x": "y"},)),
    ],
)

q(
    qid="Q-252",
    level=Level.L3,
    topic="Sorting",
    kind="function",
    entry="rank",
    prompt=(
        "Write `rank(players)`, where `players` is a list of `(name, score)` tuples. "
        "Return a **list of names** ordered by score **descending**, with ties broken "
        "by name **ascending** (A to Z).\n\n"
        "Do it in a single `sorted` call — the two fields sort in opposite directions, "
        "so `reverse=True` alone cannot be the answer."
    ),
    hint=(
        "A `key` may return a tuple, and tuples compare element by element. If one "
        "field is numeric, there is an arithmetic trick that reverses just that field."
    ),
    solution=(
        "def rank(players):\n"
        "    ordered = sorted(players, key=lambda p: (-p[1], p[0]))\n"
        "    return [name for name, score in ordered]"
    ),
    explanation=(
        "Returning a tuple from `key` gives you lexicographic multi-key sorting for "
        "free, and negating the numeric field flips *only* that field — `reverse=True` "
        "would flip the name order too and put `'cy'` before `'bo'`. Negation only "
        "works on numbers; for a descending string field, sort twice and lean on "
        "stability (secondary key first, primary key second)."
    ),
    starter="def rank(players):\n    ...",
    cases=[
        Case(expected=["al", "bo", "cy"], args=([("bo", 3), ("al", 5), ("cy", 3)],)),
        Case(expected=[], args=([],)),
        Case(expected=["z"], args=([("z", 1)],)),
        Case(expected=["a", "b"], args=([("b", 2), ("a", 2)],)),
    ],
)

q(
    qid="Q-253",
    level=Level.L3,
    topic="Generators",
    kind="custom",
    entry="running_max",
    constraints=["needs-generator"],
    prompt=(
        "Write `running_max(nums)` that returns a **list** where each element is the "
        "largest value seen so far.\n\n"
        "`running_max([1, 3, 2, 5])` returns `[1, 3, 3, 5]`. Produce the values from "
        "an inner **generator function** — one that uses `yield` — and turn it into "
        "the list with `list(...)` before returning."
    ),
    hint=(
        "A function containing `yield` returns a generator when you call it; nothing "
        "in its body runs until something iterates. Define that helper inside "
        "`running_max` so it can see `nums`, then materialise it."
    ),
    solution=(
        "def running_max(nums):\n"
        "    def scan():\n"
        "        best = None\n"
        "        for n in nums:\n"
        "            best = n if best is None else max(best, n)\n"
        "            yield best\n"
        "    return list(scan())"
    ),
    explanation=(
        "`yield` suspends the function and keeps its whole frame alive, so `best` "
        "persists between values without any object or `nonlocal` bookkeeping — that "
        "is the entire appeal of generators for running state. They are lazy and "
        "one-shot, which is why the `list(...)` matters: returning the generator itself "
        "would hand the caller something that empties the first time it is read."
    ),
    starter="def running_max(nums):\n    ...",
    cases=[
        Case(expected=[1, 3, 3, 5], args=([1, 3, 2, 5],)),
        Case(expected=[], args=([],)),
        Case(expected=[4], args=([4],)),
        Case(expected=[3, 3, 3], args=([3, 2, 1],)),
        Case(expected=[-5, -1, -1], args=([-5, -1, -2],)),
    ],
)

q(
    qid="Q-254",
    level=Level.L3,
    topic="Built-ins",
    kind="function",
    entry="only_numbers",
    prompt=(
        "Write `only_numbers(tokens)` that returns a **list** of the tokens made "
        "entirely of digits, in order, using `filter`.\n\n"
        "`only_numbers(['1', 'a', '22'])` returns `['1', '22']`. A `filter` object is "
        "not a list and will not pass. Note that `'-1'` is not all digits."
    ),
    hint=(
        "`str.isdigit` accessed on the class itself is a plain function taking the "
        "string as its argument — exactly the shape `filter` wants. Then one more call "
        "to get a list."
    ),
    solution="def only_numbers(tokens):\n    return list(filter(str.isdigit, tokens))",
    explanation=(
        "Passing the unbound `str.isdigit` rather than a `lambda t: t.isdigit()` works "
        "because a method looked up on the class takes its receiver as the first "
        "argument — the same reason `key=str.lower` sorts case-insensitively. Like "
        "`map`, `filter` is a lazy iterator; and `filter(None, xs)` with `None` as the "
        "predicate is the special form that keeps every truthy item."
    ),
    starter="def only_numbers(tokens):\n    ...",
    cases=[
        Case(expected=["1", "22"], args=(["1", "a", "22"],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=(["abc"],)),
        Case(expected=["0"], args=(["0", "-1", "3.5"],)),
    ],
)

q(
    qid="Q-255",
    level=Level.L3,
    topic="Recursion",
    kind="custom",
    entry="depth",
    constraints=["needs-recursion"],
    prompt=(
        "Write `depth(value)` returning an `int`: how deeply lists are nested.\n\n"
        "A non-list has depth `0`. A list has depth one more than the deepest thing "
        "inside it, so `depth([])` is `1`, `depth([1, 2])` is `1` and "
        "`depth([1, [2, [3]]])` is `3`.\n\n"
        "Must be recursive. Careful with the empty list — `max()` on nothing raises."
    ),
    hint=(
        "The base case is 'this is not a list at all'. For a list, ask every item how "
        "deep it is and keep the largest; `max` takes a `default=` keyword for when "
        "there is nothing to compare."
    ),
    solution=(
        "def depth(value):\n"
        "    if not isinstance(value, list):\n"
        "        return 0\n"
        "    return 1 + max((depth(item) for item in value), default=0)"
    ),
    explanation=(
        "The base case is the non-list, returning `0`; every recursive call moves one "
        "level inward and the nesting is finite, so it terminates. `max(..., default=0)` "
        "is what saves the empty list: without it, `max(())` raises `ValueError` and "
        "`depth([])` blows up on the simplest possible input — the edge case that costs "
        "most people their first attempt."
    ),
    starter="def depth(value):\n    ...",
    cases=[
        Case(expected=0, args=(1,)),
        Case(expected=1, args=([],)),
        Case(expected=1, args=([1, 2],)),
        Case(expected=3, args=([1, [2, [3]]],)),
        Case(expected=3, args=([[], [[]]],)),
        Case(expected=0, args=("abc",)),
    ],
)

q(
    qid="Q-256",
    level=Level.L3,
    topic="Recursion",
    kind="custom",
    entry="binary_search",
    constraints=["needs-recursion", "no-loops"],
    prompt=(
        "Write `binary_search(values, target, lo=0, hi=None)` over a **sorted** list. "
        "Return the index of `target`, or `-1` if it is absent.\n\n"
        "It must be recursive and halve the search range each call — no loops. `hi` "
        "defaults to `None` so the first call can fill in the last index itself; the "
        "checker only ever passes the first two arguments."
    ),
    hint=(
        "Two base cases: the range has collapsed to nothing, or the midpoint is the "
        "answer. Otherwise recurse on one side — and make sure the midpoint itself is "
        "excluded from the next range."
    ),
    solution=(
        "def binary_search(values, target, lo=0, hi=None):\n"
        "    if hi is None:\n"
        "        hi = len(values) - 1\n"
        "    if lo > hi:\n"
        "        return -1\n"
        "    mid = (lo + hi) // 2\n"
        "    if values[mid] == target:\n"
        "        return mid\n"
        "    if values[mid] < target:\n"
        "        return binary_search(values, target, mid + 1, hi)\n"
        "    return binary_search(values, target, lo, mid - 1)"
    ),
    explanation=(
        "Two base cases stop it: `lo > hi` means the range is empty, and a hit at `mid` "
        "returns immediately. Termination hinges on `mid + 1` and `mid - 1` — recursing "
        "on `mid` itself leaves the range the same size and recurses forever, which is "
        "*the* classic binary-search bug. `hi=None` rather than `hi=len(values) - 1` is "
        "deliberate: default arguments are evaluated once at definition time, so they "
        "cannot depend on another argument."
    ),
    starter="def binary_search(values, target, lo=0, hi=None):\n    ...",
    cases=[
        Case(expected=2, args=([1, 3, 5, 7, 9], 5)),
        Case(expected=0, args=([1, 3, 5, 7, 9], 1)),
        Case(expected=4, args=([1, 3, 5, 7, 9], 9)),
        Case(expected=-1, args=([1, 3, 5, 7, 9], 4)),
        Case(expected=-1, args=([], 1)),
        Case(expected=0, args=([2], 2)),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-257",
    level=Level.L4,
    topic="Recursion",
    kind="custom",
    entry="flatten",
    constraints=["needs-recursion"],
    prompt=(
        "Write `flatten(items)` that turns **arbitrarily** nested lists into a single "
        "flat **list** of non-list values, left to right.\n\n"
        "`flatten([1, [2, [3, [4]]]])` returns `[1, 2, 3, 4]`. Strings are values, "
        "never containers: `flatten(['ab'])` is `['ab']`, not `['a', 'b']`.\n\n"
        "Must be recursive. Q-249 only handled one level — this one handles any depth."
    ),
    hint=(
        "Walk the items. Each one is either a list, in which case you already have a "
        "function that flattens lists, or it is not, in which case it goes straight "
        "into the output. `isinstance(x, list)` is the test you want — not 'is it "
        "iterable'."
    ),
    solution=(
        "def flatten(items):\n"
        "    out = []\n"
        "    for item in items:\n"
        "        if isinstance(item, list):\n"
        "            out.extend(flatten(item))\n"
        "        else:\n"
        "            out.append(item)\n"
        "    return out"
    ),
    explanation=(
        "The base case is implicit: an item that is not a list is appended and the "
        "recursion stops there, and an empty list simply never enters the branch. It "
        "terminates because each recursive call descends one level into a finite "
        "structure. Testing `isinstance(item, list)` rather than 'does it have "
        "`__iter__`' is the load-bearing detail — a string is iterable and yields "
        "one-character strings that are themselves iterable, so the general test "
        "recurses until the stack gives out."
    ),
    starter="def flatten(items):\n    ...",
    cases=[
        Case(expected=[1, 2, 3, 4], args=([1, [2, [3, [4]]]],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=([[], [[]]],)),
        Case(expected=["ab", "cd"], args=(["ab", ["cd"]],)),
        Case(expected=[1, 2], args=([1, 2],)),
        Case(expected=[1, 2, 3], args=([[1], [2, [3]]],)),
    ],
)

q(
    qid="Q-258",
    level=Level.L4,
    topic="Recursion",
    kind="custom",
    entry="leaf_paths",
    constraints=["needs-recursion"],
    prompt=(
        "Write `leaf_paths(tree, prefix='')` where `tree` is a dict whose values are "
        "either dicts or plain leaf values. Return a **list of strings**: the dotted "
        "path to every leaf, in insertion order.\n\n"
        "`leaf_paths({'a': {'b': 1}})` returns `['a.b']`, and "
        "`leaf_paths({'x': 1, 'y': 2})` returns `['x', 'y']`. A branch with no leaves "
        "contributes nothing. The checker only passes the first argument."
    ),
    hint=(
        "Carry the path built so far down through the recursion as the second "
        "argument. At each entry, decide whether the value is another dict to descend "
        "into or a leaf to record."
    ),
    solution=(
        "def leaf_paths(tree, prefix=\"\"):\n"
        "    out = []\n"
        "    for key, value in tree.items():\n"
        "        path = f\"{prefix}{key}\"\n"
        "        if isinstance(value, dict):\n"
        "            out.extend(leaf_paths(value, path + \".\"))\n"
        "        else:\n"
        "            out.append(path)\n"
        "    return out"
    ),
    explanation=(
        "The base case is a non-dict value, which is appended and ends that branch; the "
        "recursion terminates because every call descends one level into a finite tree. "
        "Threading the prefix down as an argument — an *accumulator* — is the standard "
        "way to give a recursive call the context it cannot see. Note the accumulator "
        "is a string, which is immutable and so cannot be shared by accident; a "
        "mutable default like `out=[]` would be evaluated once at definition time and "
        "leak results from one call into the next."
    ),
    starter="def leaf_paths(tree, prefix=\"\"):\n    ...",
    cases=[
        Case(expected=["a.b"], args=({"a": {"b": 1}},)),
        Case(expected=[], args=({},)),
        Case(expected=["x", "y"], args=({"x": 1, "y": 2},)),
        Case(expected=["a.b.c", "d"], args=({"a": {"b": {"c": 1}}, "d": 2},)),
        Case(expected=[], args=({"a": {}},)),
    ],
)

q(
    qid="Q-259",
    level=Level.L4,
    topic="Recursion",
    kind="custom",
    entry="permutations_of",
    constraints=["needs-recursion", "no-builtin:permutations"],
    prompt=(
        "Write `permutations_of(items)` returning a **list of lists** — every ordering "
        "of `items`.\n\n"
        "Produce them in this order: take each item in turn as the first element and "
        "permute the rest. So `permutations_of([1, 2])` is `[[1, 2], [2, 1]]` and "
        "`permutations_of([1, 2, 3])` starts `[[1, 2, 3], [1, 3, 2], [2, 1, 3], ...]`.\n\n"
        "`permutations_of([])` is `[[]]` — one arrangement, the empty one. Must be "
        "recursive; no `itertools.permutations`."
    ),
    hint=(
        "For each position `i`, the remaining items are `items[:i] + items[i+1:]`. "
        "Prepend `items[i]` to every ordering of that remainder. The base case is the "
        "one that decides whether anything survives at all — think carefully about "
        "what an empty input should return."
    ),
    solution=(
        "def permutations_of(items):\n"
        "    if not items:\n"
        "        return [[]]\n"
        "    result = []\n"
        "    for i, item in enumerate(items):\n"
        "        rest = items[:i] + items[i + 1:]\n"
        "        for tail in permutations_of(rest):\n"
        "            result.append([item] + tail)\n"
        "    return result"
    ),
    explanation=(
        "The base case must be `[[]]` — a list containing *one* arrangement, the empty "
        "one — and not `[]`. Returning `[]` is the classic bug: the innermost loop then "
        "iterates over nothing, nothing is ever appended, and the whole result comes "
        "back empty with no error to explain why. Termination is easy to see because "
        "`rest` is always one shorter; the cost is not, since the output is `n!` long "
        "and 12 items already means half a billion lists."
    ),
    starter="def permutations_of(items):\n    ...",
    cases=[
        Case(expected=[[]], args=([],)),
        Case(expected=[[1]], args=([1],)),
        Case(expected=[[1, 2], [2, 1]], args=([1, 2],)),
        Case(
            expected=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
            args=([1, 2, 3],),
        ),
        Case(expected=[["a", "b"], ["b", "a"]], args=(["a", "b"],)),
    ],
)

q(
    qid="Q-260",
    level=Level.L4,
    topic="Recursion",
    kind="custom",
    entry="hanoi",
    constraints=["needs-recursion"],
    prompt=(
        "Tower of Hanoi. Write "
        "`hanoi(n, source='A', target='C', spare='B')` returning a **list of "
        "`(from, to)` tuples** — the moves that transfer `n` disks from `source` to "
        "`target`, one disk at a time, never putting a larger disk on a smaller "
        "one.\n\n"
        "`hanoi(0)` is `[]`, `hanoi(1)` is `[('A', 'C')]`, and `hanoi(2)` is "
        "`[('A', 'B'), ('A', 'C'), ('B', 'C')]`.\n\n"
        "Must be recursive. Do not simulate the pegs — just emit the moves."
    ),
    hint=(
        "To move `n` disks to the target you must first get the top `n - 1` out of the "
        "way onto the spare, move the bottom disk, then bring those `n - 1` back on "
        "top. Each of those two sub-jobs is the same problem with the peg roles "
        "swapped."
    ),
    solution=(
        "def hanoi(n, source=\"A\", target=\"C\", spare=\"B\"):\n"
        "    if n == 0:\n"
        "        return []\n"
        "    return (\n"
        "        hanoi(n - 1, source, spare, target)\n"
        "        + [(source, target)]\n"
        "        + hanoi(n - 1, spare, target, source)\n"
        "    )"
    ),
    explanation=(
        "The base case is `n == 0`, which needs no moves at all; both recursive calls "
        "use `n - 1`, so the count strictly decreases and the recursion bottoms out. "
        "The whole difficulty is that the three pegs swap roles between the two calls — "
        "getting `source`, `target` and `spare` in the right order is the entire "
        "puzzle, and it is why this is far easier to write recursively than to reason "
        "about move by move. The move count is exactly `2**n - 1`."
    ),
    starter="def hanoi(n, source=\"A\", target=\"C\", spare=\"B\"):\n    ...",
    cases=[
        Case(expected=[], args=(0,)),
        Case(expected=[("A", "C")], args=(1,)),
        Case(expected=[("A", "B"), ("A", "C"), ("B", "C")], args=(2,)),
        Case(
            expected=[
                ("A", "C"), ("A", "B"), ("C", "B"),
                ("A", "C"),
                ("B", "A"), ("B", "C"), ("A", "C"),
            ],
            args=(3,),
        ),
        Case(
            expected=[("X", "Z"), ("X", "Y"), ("Z", "Y")],
            args=(2, "X", "Y", "Z"),
        ),
    ],
)

q(
    qid="Q-261",
    level=Level.L4,
    topic="Nested Comprehensions",
    kind="custom",
    entry="group_by_initial",
    constraints=["needs-comprehension", "no-loops"],
    prompt=(
        "Write `group_by_initial(words)` that returns a **dict** mapping each distinct "
        "first letter to the **list** of words beginning with it, in their original "
        "order.\n\n"
        "`group_by_initial(['ant', 'bee', 'ape'])` returns "
        "`{'a': ['ant', 'ape'], 'b': ['bee']}`. Words are non-empty and already "
        "lowercase.\n\n"
        "Comprehensions only — no `for` statement, no `defaultdict`, no `setdefault`."
    ),
    hint=(
        "Grouping needs two things: the set of distinct keys, and for each key the "
        "items that match it. `dict.fromkeys(...)` gives you distinct keys while "
        "preserving first-appearance order, which a `set` would not."
    ),
    solution=(
        "def group_by_initial(words):\n"
        "    return {\n"
        "        first: [w for w in words if w[0] == first]\n"
        "        for first in dict.fromkeys(w[0] for w in words)\n"
        "    }"
    ),
    explanation=(
        "A dict comprehension whose *value* is itself a list comprehension is the "
        "comprehension-only way to group, and the outer iterable has to supply each "
        "key exactly once — `dict.fromkeys` deduplicates while keeping insertion order, "
        "where a set comprehension would scramble it. Be honest about the cost: this "
        "rescans `words` once per distinct key, so the loop-plus-`defaultdict` version "
        "is one pass and the right answer at scale."
    ),
    starter="def group_by_initial(words):\n    ...",
    cases=[
        Case(expected={"a": ["ant", "ape"], "b": ["bee"]}, args=(["ant", "bee", "ape"],)),
        Case(expected={}, args=([],)),
        Case(expected={"x": ["x"]}, args=(["x"],)),
        Case(
            expected={"d": ["dog", "deer"], "c": ["cat"]},
            args=(["dog", "deer", "cat"],),
        ),
    ],
)

q(
    qid="Q-262",
    level=Level.L4,
    topic="Sorting",
    kind="function",
    entry="sort_records",
    prompt=(
        "Write `sort_records(records)` where each record is a dict with `'name'` and "
        "`'age'`. Return a **new list of those same dicts**, ordered by age "
        "descending, ties broken by name ascending.\n\n"
        "The input list must not be reordered, and the dicts themselves are returned "
        "unchanged."
    ),
    hint=(
        "Same tuple-key technique as Q-252, but the fields come out of a dict rather "
        "than a tuple. Reach into the record inside the `key` function."
    ),
    solution=(
        "def sort_records(records):\n"
        '    return sorted(records, key=lambda r: (-r["age"], r["name"]))'
    ),
    explanation=(
        "`sorted` copies the list, so the caller's order survives — but the copy is "
        "shallow and holds the *same* dict objects, so mutating one afterwards is "
        "visible from both lists. The `key` function is called exactly once per record "
        "and the results are compared, never the records themselves; that is what lets "
        "you sort dicts at all, since dicts have no ordering of their own and "
        "`sorted(records)` alone is a `TypeError`."
    ),
    starter="def sort_records(records):\n    ...",
    cases=[
        Case(
            expected=[{"name": "cy", "age": 40}, {"name": "al", "age": 30},
                      {"name": "bo", "age": 30}],
            args=([{"name": "al", "age": 30}, {"name": "cy", "age": 40},
                   {"name": "bo", "age": 30}],),
        ),
        Case(expected=[], args=([],)),
        Case(expected=[{"name": "solo", "age": 1}], args=([{"name": "solo", "age": 1}],)),
        Case(
            expected=[{"name": "a", "age": 5}, {"name": "b", "age": 5}],
            args=([{"name": "b", "age": 5}, {"name": "a", "age": 5}],),
        ),
    ],
)

q(
    qid="Q-263",
    level=Level.L4,
    topic="Built-ins",
    kind="function",
    entry="merge_rows",
    prompt=(
        "Write `merge_rows(headers, rows)` — `headers` is a list of column names and "
        "`rows` a list of lists of values. Return a **list of dicts**, one per row, "
        "mapping header to value.\n\n"
        "A row shorter than `headers` simply has fewer entries in its dict — that is "
        "`zip`'s behaviour, and the point of the exercise. Use a comprehension."
    ),
    hint=(
        "`dict()` accepts an iterable of pairs, and `zip` produces exactly that. One "
        "comprehension over `rows` is all you need."
    ),
    solution=(
        "def merge_rows(headers, rows):\n"
        "    return [dict(zip(headers, row)) for row in rows]"
    ),
    explanation=(
        "`dict(zip(keys, values))` is the standard one-line way to build a record from "
        "parallel sequences. It is also quietly lossy in exactly the way Q-245 warns "
        "about: a short row loses its trailing columns and a long one loses its extra "
        "values, both without a murmur. In a real CSV reader that is the difference "
        "between a loud `ValueError` from `strict=True` and a report that is wrong for "
        "six months."
    ),
    starter="def merge_rows(headers, rows):\n    ...",
    cases=[
        Case(
            expected=[{"a": 1, "b": 2}, {"a": 3, "b": 4}],
            args=(["a", "b"], [[1, 2], [3, 4]]),
        ),
        Case(expected=[{"a": 1}], args=(["a", "b"], [[1]])),
        Case(expected=[], args=(["a"], [])),
        Case(expected=[{}], args=([], [[1, 2]])),
    ],
)

q(
    qid="Q-264",
    level=Level.L4,
    topic="Generators",
    kind="custom",
    entry="first_over",
    constraints=["no-loops"],
    prompt=(
        "Write `first_over(nums, limit)` that returns the first number in `nums` "
        "strictly greater than `limit`, or `None` when there is none.\n\n"
        "No loops. Use a **generator expression** and `next(...)` so that nothing "
        "after the match is ever examined — and give `next` a default, or an empty "
        "result becomes an exception."
    ),
    hint=(
        "`next(iterator, default)` pulls exactly one value and hands back `default` "
        "instead of raising when there is nothing left. Feed it a filtered generator "
        "expression."
    ),
    solution=(
        "def first_over(nums, limit):\n"
        "    return next((n for n in nums if n > limit), None)"
    ),
    explanation=(
        "This is where laziness earns its keep: a list comprehension would evaluate "
        "every element before you looked at the first, whereas the generator stops the "
        "instant `next` is satisfied — the difference between O(1) and O(n) work, and "
        "the difference between finishing and hanging on an infinite source. The "
        "second argument to `next` is not optional in practice: without it an empty "
        "match raises `StopIteration`, which inside a generator is especially nasty "
        "because it silently ends *that* generator instead of propagating."
    ),
    starter="def first_over(nums, limit):\n    ...",
    cases=[
        Case(expected=5, args=([1, 5, 9], 4)),
        Case(expected=None, args=([1, 2], 10)),
        Case(expected=None, args=([], 0)),
        Case(expected=3, args=([3], 1)),
        Case(expected=1, args=([-1, 0, 1], 0)),
    ],
)

q(
    qid="Q-265",
    level=Level.L4,
    topic="Comprehensions",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "nums = [1, 2, 3, 4]\n"
        "print([n for n in nums if n % 2 == 0])\n"
        "print([n if n % 2 == 0 else 0 for n in nums])\n"
        "print([n for n in nums if n % 2 == 0 if n > 2])\n"
        "```\n\n"
        "Set `answer` to the three printed lines. Two of them are the same length as "
        "`nums` or shorter — decide which, and why, before you write anything."
    ),
    hint=(
        "One `if` sits in front of the `for` and one sits behind it, and they are not "
        "the same construct at all. The third line has two trailing `if`s — work out "
        "how they combine."
    ),
    solution='answer = "[2, 4]\\n[0, 2, 0, 4]\\n[4]"',
    explanation=(
        "An `if` **after** the `for` is a filter and shortens the output; an "
        "`if`/`else` **before** it is a conditional expression that substitutes values "
        "and preserves length — and that form *requires* the `else`, which is why "
        "people trying to filter with it get a `SyntaxError`. Stacked trailing `if`s "
        "simply chain, so the third line means `and`: even *and* greater than 2."
    ),
    starter="answer = ...",
    cases=[Case(expected="[2, 4]\n[0, 2, 0, 4]\n[4]")],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-266",
    level=Level.L5,
    topic="Recursion",
    kind="custom",
    entry="count_paths",
    constraints=["needs-recursion"],
    prompt=(
        "Write `count_paths(rows, cols)` returning an `int`: the number of distinct "
        "routes from the top-left cell of a `rows` x `cols` grid to the bottom-right "
        "one, moving only right or down.\n\n"
        "`count_paths(2, 2)` is `2`, `count_paths(3, 3)` is `6`, and a grid with a "
        "zero dimension has `0` routes.\n\n"
        "It must be recursive **and memoised**: one of the cases is `count_paths(18, "
        "18)`, and the naive version would still be running tomorrow."
    ),
    hint=(
        "Every route into the last cell arrives from the one above or the one to the "
        "left, so the count is the sum of two smaller grids. A single-row or "
        "single-column grid has exactly one route. For the memoisation, "
        "`functools.lru_cache` is one decorator line."
    ),
    solution=(
        "from functools import lru_cache\n\n\n"
        "@lru_cache(maxsize=None)\n"
        "def count_paths(rows, cols):\n"
        "    if rows <= 0 or cols <= 0:\n"
        "        return 0\n"
        "    if rows == 1 or cols == 1:\n"
        "        return 1\n"
        "    return count_paths(rows - 1, cols) + count_paths(rows, cols - 1)"
    ),
    explanation=(
        "Base cases: a degenerate grid has `0` routes, and a single row or column has "
        "exactly `1`; each call shrinks one dimension, so it terminates. Without "
        "memoisation this recomputes the same subgrid an exponential number of times — "
        "`count_paths(18, 18)` is roughly 2**34 calls — while caching by argument "
        "collapses it to one evaluation per `(rows, cols)` pair, so O(rows * cols). "
        "`lru_cache` only works because the function is *pure*: same arguments, same "
        "answer, no side effects, and hashable arguments."
    ),
    starter="from functools import lru_cache\n\n\ndef count_paths(rows, cols):\n    ...",
    cases=[
        Case(expected=1, args=(1, 1)),
        Case(expected=2, args=(2, 2)),
        Case(expected=6, args=(3, 3)),
        Case(expected=28, args=(3, 7)),
        Case(expected=0, args=(0, 5)),
        Case(expected=2333606220, args=(18, 18)),
    ],
)

q(
    qid="Q-267",
    level=Level.L5,
    topic="Recursion",
    kind="custom",
    entry="flatten_iterative",
    constraints=["no-recursion"],
    prompt=(
        "Rewrite Q-257 **without recursion**: `flatten_iterative(items)` takes "
        "arbitrarily nested lists and returns a flat **list** of non-list values, left "
        "to right — identical results, but keeping your own explicit stack and a "
        "`while` loop.\n\n"
        "The function must not call itself. Strings are still values, not containers. "
        "No `itertools`, no `deque`.\n\n"
        "This is the technique for input deeper than Python's recursion limit."
    ),
    hint=(
        "A list makes a fine stack: `.pop()` takes from the right. That means you have "
        "to push items in the *opposite* order to the one you want to visit them in — "
        "which is the only subtle part of the whole exercise."
    ),
    solution=(
        "def flatten_iterative(items):\n"
        "    out = []\n"
        "    stack = list(items)[::-1]\n"
        "    while stack:\n"
        "        item = stack.pop()\n"
        "        if isinstance(item, list):\n"
        "            stack.extend(reversed(item))\n"
        "        else:\n"
        "            out.append(item)\n"
        "    return out"
    ),
    explanation=(
        "Every recursion is a loop plus a stack — the call stack was doing exactly this "
        "bookkeeping for you, one frame per pending sublist. The loop ends because each "
        "iteration removes an item and only ever pushes that item's own children, so a "
        "finite structure drains. Reversing before pushing is what preserves left-to-"
        "right order, since popping from the right returns the last thing pushed. Doing "
        "this by hand is how you survive input deeper than `sys.getrecursionlimit()`, "
        "which Python defaults to around 1000."
    ),
    starter="def flatten_iterative(items):\n    ...",
    cases=[
        Case(expected=[1, 2, 3, 4], args=([1, [2, [3, [4]]]],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=([[], [[]]],)),
        Case(expected=[1, 2, 3], args=([1, [2], 3],)),
        Case(expected=["ab", "cd"], args=(["ab", ["cd"]],)),
        Case(expected=[1, 2, 3, 4], args=([[1, 2], [[3], [4]]],)),
    ],
)

q(
    qid="Q-268",
    level=Level.L5,
    topic="Recursion",
    kind="custom",
    entry="evaluate",
    constraints=["needs-recursion", "no-builtin:eval"],
    prompt=(
        "Write `evaluate(node)` for a tiny expression tree. A node is either a number, "
        "or a 3-element list `[left, op, right]` where `op` is `'+'`, `'-'` or `'*'` "
        "and `left`/`right` are themselves nodes.\n\n"
        "Return the numeric result: `evaluate([[1, '+', 2], '*', 3])` is `9`.\n\n"
        "Must be recursive. No `eval()`."
    ),
    hint=(
        "The base case is the node that is not a list — it is already the answer. "
        "Otherwise unpack the three parts, evaluate each side the same way, and combine "
        "them according to the operator."
    ),
    solution=(
        "def evaluate(node):\n"
        "    if not isinstance(node, list):\n"
        "        return node\n"
        "    left, op, right = node\n"
        "    a = evaluate(left)\n"
        "    b = evaluate(right)\n"
        '    if op == "+":\n'
        "        return a + b\n"
        '    if op == "-":\n'
        "        return a - b\n"
        "    return a * b"
    ),
    explanation=(
        "The base case is a bare number, and each recursive call descends into a "
        "strictly smaller subtree, so a finite tree always bottoms out. This is exactly "
        "how a recursive-descent interpreter works, and it makes the key point about "
        "precedence: the *tree shape* decides the order of evaluation, so "
        "`[[1, '+', 2], '*', 3]` and `[1, '+', [2, '*', 3]]` give different answers "
        "from the same symbols. Precedence is a parsing problem, resolved before "
        "evaluation ever begins."
    ),
    starter="def evaluate(node):\n    ...",
    cases=[
        Case(expected=3, args=(3,)),
        Case(expected=3, args=([1, "+", 2],)),
        Case(expected=9, args=([[1, "+", 2], "*", 3],)),
        Case(expected=7, args=([1, "+", [2, "*", 3]],)),
        Case(expected=0, args=([2, "-", [3, "-", 1]],)),
        Case(expected=7, args=([[1, "*", 1], "+", [2, "*", 3]],)),
    ],
)

q(
    qid="Q-269",
    level=Level.L5,
    topic="Generators",
    kind="custom",
    entry="pipeline",
    constraints=["needs-comprehension", "no-loops"],
    prompt=(
        "Write `pipeline(rows)`. Each row is a string like `'name,42'`. Return a "
        "**list of ints**: for every row whose number is strictly greater than `10`, "
        "that number doubled, in order.\n\n"
        "`pipeline(['a,5', 'b,20', 'c,11'])` returns `[40, 22]`.\n\n"
        "Build it as a chain of **generator expressions** — parse, then filter, then "
        "transform, each a separate named stage — and materialise once at the end with "
        "`list(...)`. No `for` statement."
    ),
    hint=(
        "`row.split(',')` gives you the two fields. Each stage is a genexp that reads "
        "from the previous stage's name, so nothing is computed until the final "
        "`list(...)` pulls on the chain."
    ),
    solution=(
        "def pipeline(rows):\n"
        '    numbers = (int(row.split(",")[1]) for row in rows)\n'
        "    big = (n for n in numbers if n > 10)\n"
        "    return list(n * 2 for n in big)"
    ),
    explanation=(
        "Chained generator expressions are a pull-based pipeline: nothing runs until "
        "`list(...)` asks, and then each value is drawn all the way through the chain "
        "one at a time, so peak memory is constant no matter how long `rows` is. The "
        "trap is the one from Q-244 — each stage is single-use, so reading `numbers` "
        "again after the pipeline has run yields an empty result, and a chain built "
        "over a file handle that has since closed fails at consumption time rather "
        "than at the line that looks like it did the work."
    ),
    starter="def pipeline(rows):\n    ...",
    cases=[
        Case(expected=[40, 22], args=(["a,5", "b,20", "c,11"],)),
        Case(expected=[], args=([],)),
        Case(expected=[], args=(["a,10"],)),
        Case(expected=[22], args=(["a,11"],)),
        Case(expected=[200], args=(["x,-3", "y,100"],)),
    ],
)

q(
    qid="Q-270",
    level=Level.L5,
    topic="Nested Comprehensions",
    kind="custom",
    entry="word_index",
    constraints=["needs-comprehension", "no-loops"],
    prompt=(
        "Build an inverted index. `word_index(docs)` takes a dict mapping document id "
        "to a list of words, and returns a **dict** mapping each distinct word to the "
        "**sorted list** of document ids containing it.\n\n"
        "`word_index({'d1': ['a', 'b'], 'd2': ['b']})` returns "
        "`{'a': ['d1'], 'b': ['d1', 'd2']}`. A word appearing twice in one document "
        "still lists that id once.\n\n"
        "Comprehensions only — no `for` statement, no `defaultdict`."
    ),
    hint=(
        "Two comprehensions, one inside the other. The outer one needs the set of "
        "every distinct word across every document — that itself is a nested set "
        "comprehension with two `for` clauses. The inner one asks which documents "
        "contain a given word."
    ),
    solution=(
        "def word_index(docs):\n"
        "    return {\n"
        "        word: sorted(\n"
        "            doc_id for doc_id, words in docs.items() if word in words\n"
        "        )\n"
        "        for word in {w for words in docs.values() for w in words}\n"
        "    }"
    ),
    explanation=(
        "Three ideas stack here: a nested set comprehension flattens every document's "
        "words into the distinct key set (and deduplicates a repeated word for free), "
        "a filtered generator expression finds the matching ids, and `sorted` fixes "
        "their order — because the set the keys came from has none. Read the cost "
        "honestly: this rescans every document once per distinct word, where a real "
        "inverted index is built in a single pass. Comprehensions buy clarity here, "
        "not speed."
    ),
    starter="def word_index(docs):\n    ...",
    cases=[
        Case(
            expected={"a": ["d1"], "b": ["d1", "d2"]},
            args=({"d1": ["a", "b"], "d2": ["b"]},),
        ),
        Case(expected={}, args=({},)),
        Case(expected={}, args=({"d1": []},)),
        Case(
            expected={"x": ["d1", "d2"], "y": ["d3"]},
            args=({"d1": ["x"], "d2": ["x"], "d3": ["y"]},),
        ),
        Case(expected={"k": ["a", "b"]}, args=({"b": ["k"], "a": ["k", "k"]},)),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-07",
    title="Records pipeline",
    brief=(
        "Build `summarise(records, min_score)` using **comprehensions only** — no "
        "`for` statement anywhere.\n\n"
        "`records` is a list of dicts, each with `'name'`, `'team'` and `'score'`, "
        "where the score arrives as a **string** the way it would from a CSV:\n\n"
        "```python\n"
        "[{'name': 'ana', 'team': 'red', 'score': '30'}, ...]\n"
        "```\n\n"
        "Return a dict mapping team to a list of `(name, score)` tuples with the score "
        "as an `int`:\n\n"
        "```python\n"
        "{'red': [('cy', 50), ('ana', 30)], 'blue': [('bob', 10), ('dee', 10)]}\n"
        "```\n\n"
        "Rules: drop any record whose parsed score is below `min_score`; each team's "
        "list is ordered by score descending, ties broken by name ascending; a team "
        "with no surviving records does not appear as a key at all.\n\n"
        "That is the whole pipeline — parse, filter, group, sort — and every stage is "
        "a comprehension."
    ),
    hint=(
        "Do it in two steps rather than one heroic expression. First a list "
        "comprehension that parses and filters into flat `(team, name, score)` tuples. "
        "Then a dict comprehension over the distinct teams, whose value selects from "
        "an already-sorted version of that flat list — sort once, outside the grouping, "
        "and each group inherits the order."
    ),
    solution=(
        "def summarise(records, min_score):\n"
        "    parsed = [\n"
        '        (r["team"], r["name"], int(r["score"]))\n'
        "        for r in records\n"
        '        if int(r["score"]) >= min_score\n'
        "    ]\n"
        "    ordered = sorted(parsed, key=lambda p: (-p[2], p[1]))\n"
        "    return {\n"
        "        team: [(name, score) for t, name, score in ordered if t == team]\n"
        "        for team in {t for t, _, _ in parsed}\n"
        "    }"
    ),
    explanation=(
        "The shape is the one every data pipeline has: parse the strings, filter on a "
        "threshold, group by a key, order within each group. Sorting *once* before the "
        "grouping and letting each group's filter preserve that order is the move worth "
        "keeping — it is one sort instead of one per team, and it works because "
        "comprehensions preserve the order of what they iterate. Deriving the key set "
        "from `parsed` rather than from `records` is what makes empty teams vanish for "
        "free, with no post-hoc cleanup."
    ),
    entry="summarise",
    starter="def summarise(records, min_score):\n    ...",
    cases=[
        Case(
            expected={"red": [("cy", 50), ("ana", 30)], "blue": [("bob", 10), ("dee", 10)]},
            args=(
                [
                    {"name": "ana", "team": "red", "score": "30"},
                    {"name": "bob", "team": "blue", "score": "10"},
                    {"name": "cy", "team": "red", "score": "50"},
                    {"name": "dee", "team": "blue", "score": "10"},
                ],
                10,
            ),
        ),
        Case(
            expected={"red": [("cy", 50)]},
            args=(
                [
                    {"name": "ana", "team": "red", "score": "30"},
                    {"name": "bob", "team": "blue", "score": "10"},
                    {"name": "cy", "team": "red", "score": "50"},
                ],
                40,
            ),
        ),
        Case(expected={}, args=([], 0)),
        Case(
            expected={},
            args=([{"name": "ana", "team": "red", "score": "30"}], 100),
        ),
        Case(
            expected={"solo": [("ana", 7)]},
            args=([{"name": "ana", "team": "solo", "score": "7"}], 0),
        ),
    ],
)

NOTEBOOK = Notebook(
    number=7,
    slug="comprehensions_functional_recursion",
    title="Comprehensions, Functional & Recursion",
    intro=(
        "Comprehensions in all four flavours, the functional built-ins that go with "
        "them — `map`, `filter`, `zip`, `enumerate`, `sorted`, `any`, `all` — "
        "generator expressions, and recursion.\n\n"
        "Two halves, and both matter. The comprehension half is what makes Python "
        "code read like Python: the traps are position (a filter behind the `for`, a "
        "ternary in front of it) and laziness (a generator you can only walk once, a "
        "`map` object that is not a list).\n\n"
        "The recursion half is the one people skip. Do not be the person who never "
        "quite got recursion — it is one idea (solve a smaller version, and know when "
        "to stop) and thirteen questions here drill it from `factorial` up to memoised "
        "search, an explicit-stack rewrite and a tree walker. For every one of them, "
        "name the base case out loud before you write a line."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
