"""Notebook 05 - Control Flow & Loops (Q-151..Q-186)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-151",
    level=Level.L1,
    topic="Conditionals",
    kind="function",
    entry="sign",
    prompt=(
        "Write `sign(n)` that returns the string `'positive'` when `n` is greater "
        "than zero, `'negative'` when it is less than zero, and `'zero'` when it is "
        "exactly zero.\n\n"
        "Use one `if`/`elif`/`else` chain — three separate `if` statements would also "
        "work, but that is not what this question is for."
    ),
    hint=(
        "There are three outcomes and they cannot overlap, so you need two tests and "
        "a catch-all. Decide which of the three deserves to be the catch-all."
    ),
    solution=(
        "def sign(n):\n"
        "    if n > 0:\n"
        '        return "positive"\n'
        "    elif n < 0:\n"
        '        return "negative"\n'
        "    else:\n"
        '        return "zero"'
    ),
    explanation=(
        "`elif` is not decoration: it tells Python the branches are alternatives, so "
        "at most one runs and the later tests are skipped entirely once an earlier one "
        "matches. Three independent `if` statements re-test a value that has already "
        "been classified, and that is where 'it returned the wrong label' bugs grow."
    ),
    starter="def sign(n):\n    ...",
    cases=[
        Case(expected="positive", args=(5,)),
        Case(expected="negative", args=(-3,)),
        Case(expected="zero", args=(0,)),
        Case(expected="positive", args=(0.5,)),
        Case(expected="zero", args=(0.0,)),
    ],
)

q(
    qid="Q-152",
    level=Level.L1,
    topic="Conditionals",
    kind="function",
    entry="parity",
    prompt=(
        "Write `parity(n)` that returns `'even'` for an even integer and `'odd'` for "
        "an odd one.\n\n"
        "`n` may be negative. Test with `%`, not by looking at the last character of "
        "`str(n)`."
    ),
    hint=(
        "`%` by 2 has only two possible results for an integer. You only need to test "
        "for one of them — the `else` covers the other."
    ),
    solution=(
        "def parity(n):\n"
        "    if n % 2 == 0:\n"
        '        return "even"\n'
        '    return "odd"'
    ),
    explanation=(
        "Because Python's `%` takes the sign of the divisor, `-3 % 2` is `1` and never "
        "`-1`, so `n % 2 == 1` is a safe odd-test here — in C or Java it is a bug on "
        "every negative input. Comparing against `0` is the habit worth keeping, since "
        "it stays correct in every language."
    ),
    starter="def parity(n):\n    ...",
    cases=[
        Case(expected="even", args=(4,)),
        Case(expected="odd", args=(7,)),
        Case(expected="even", args=(0,)),
        Case(expected="odd", args=(-3,)),
    ],
)

q(
    qid="Q-153",
    level=Level.L1,
    topic="Conditionals",
    kind="function",
    entry="describe",
    prompt=(
        "Write `describe(items)` that returns `'has items'` when `items` holds "
        "anything and `'empty'` when it does not.\n\n"
        "Test `items` directly in the condition — no `len()`, no `== []`, no "
        "`is None`. It may be a list, a string, a dict, or a number."
    ),
    hint=(
        "`if` does not need a comparison; it asks the value itself whether it counts "
        "as true. Every container already knows the answer for its own emptiness."
    ),
    solution=(
        "def describe(items):\n"
        "    if items:\n"
        '        return "has items"\n'
        '    return "empty"'
    ),
    explanation=(
        "Empty containers, empty strings and every numeric zero are falsy; everything "
        "else is truthy. That is why `[0]` reports as non-empty — a container is judged "
        "on whether it holds anything, never on what it holds — and why `if items:` "
        "works on types that have no `len()` at all."
    ),
    starter="def describe(items):\n    ...",
    cases=[
        Case(expected="has items", args=([1, 2],)),
        Case(expected="empty", args=([],)),
        Case(expected="empty", args=("",)),
        Case(expected="has items", args=([0],)),
        Case(expected="empty", args=({},)),
        Case(expected="empty", args=(0,)),
    ],
)

q(
    qid="Q-154",
    level=Level.L1,
    topic="Conditionals",
    kind="function",
    entry="bigger",
    prompt=(
        "Write `bigger(a, b)` that returns the larger of the two values, and returns "
        "`a` when they are equal.\n\n"
        "Write the body as a **conditional expression** — one `return` line, no `if` "
        "statement and no `max()`."
    ),
    hint=(
        "Python's conditional expression puts the value first and the test in the "
        "middle: result-when-true, then the condition, then the fallback. Read it "
        "aloud as an English sentence and the word order is the same."
    ),
    solution="def bigger(a, b):\n    return a if a >= b else b",
    explanation=(
        "A conditional expression *evaluates to* a value, so it can sit anywhere a "
        "value can — inside a call, a comprehension, or an f-string — which an `if` "
        "statement cannot. Both `else` and the branch values are mandatory: there is no "
        "one-armed form, because an expression must always produce something."
    ),
    starter="def bigger(a, b):\n    ...",
    cases=[
        Case(expected=5, args=(3, 5)),
        Case(expected=5, args=(5, 3)),
        Case(expected=4, args=(4, 4)),
        Case(expected=-1, args=(-1, -2)),
    ],
)

q(
    qid="Q-155",
    level=Level.L1,
    topic="For Loops",
    kind="function",
    entry="total",
    prompt=(
        "Write `total(numbers)` that adds up a list of numbers and returns the sum, "
        "using a `for` loop and a running accumulator.\n\n"
        "An empty list totals `0`. Do not call `sum()` — that is the point of the "
        "exercise."
    ),
    hint=(
        "You need somewhere to keep the running answer, and it has to exist *before* "
        "the loop starts — otherwise there is nothing to add the first item to."
    ),
    solution=(
        "def total(numbers):\n"
        "    running = 0\n"
        "    for n in numbers:\n"
        "        running += n\n"
        "    return running"
    ),
    explanation=(
        "The accumulator must be initialised outside the loop, and its starting value "
        "is also the answer for an empty input — `0` for a sum, `1` for a product. "
        "Initialising it *inside* the loop is the classic beginner slip: the total "
        "resets on every pass and you end up with the last element."
    ),
    starter="def total(numbers):\n    ...",
    cases=[
        Case(expected=6, args=([1, 2, 3],)),
        Case(expected=0, args=([],)),
        Case(expected=0, args=([-1, 1],)),
        Case(expected=5.0, args=([2.5, 2.5],)),
        Case(expected=7, args=([7],)),
    ],
)

q(
    qid="Q-156",
    level=Level.L1,
    topic="For Loops",
    kind="function",
    entry="shout",
    prompt=(
        "Write `shout(words)` that returns a **new list** with every string "
        "uppercased, in the same order.\n\n"
        "Build the result with a `for` loop and `.append()`. The input list must come "
        "back unchanged."
    ),
    hint=(
        "Start from an empty list and grow it. The loop variable is a fresh name bound "
        "to each element — rebinding it does not touch the list you are reading from."
    ),
    solution=(
        "def shout(words):\n"
        "    out = []\n"
        "    for word in words:\n"
        "        out.append(word.upper())\n"
        "    return out"
    ),
    explanation=(
        "`for word in words` binds `word` to each element in turn, so assigning to "
        "`word` would only move that one label and never write back into the list. "
        "Building a separate output list is also what keeps the function safe to call "
        "on data someone else still owns."
    ),
    starter="def shout(words):\n    ...",
    cases=[
        Case(expected=["A", "B"], args=(["a", "b"],)),
        Case(expected=[], args=([],)),
        Case(expected=["MIXED CASE"], args=(["Mixed Case"],)),
        Case(expected=["HI", "HI"], args=(["hi", "HI"],)),
    ],
)

q(
    qid="Q-157",
    level=Level.L1,
    topic="Range",
    kind="function",
    entry="first_n",
    prompt=(
        "Write `first_n(n)` that returns the list `[0, 1, ..., n - 1]`.\n\n"
        "`first_n(5)` gives `[0, 1, 2, 3, 4]` and `first_n(0)` gives `[]`. The result "
        "must be a real `list`, not a `range` object."
    ),
    hint=(
        "The one-argument form of `range` already counts from zero and stops just "
        "short of its argument. What it hands back is not a list yet — one builtin "
        "call fixes that."
    ),
    solution="def first_n(n):\n    return list(range(n))",
    explanation=(
        "`range(n)` is half-open: it includes the start and excludes the stop, which "
        "is why `len(range(n))` is exactly `n` and why indices line up with `range` "
        "with no off-by-one arithmetic. It is also lazy — it stores only start, stop "
        "and step — so `range(10**12)` costs nothing until you materialise it."
    ),
    starter="def first_n(n):\n    ...",
    cases=[
        Case(expected=[0, 1, 2, 3, 4], args=(5,)),
        Case(expected=[0], args=(1,)),
        Case(expected=[], args=(0,)),
        Case(expected=[], args=(-3,)),
    ],
)

q(
    qid="Q-158",
    level=Level.L1,
    topic="While Loops",
    kind="function",
    entry="countdown",
    prompt=(
        "Write `countdown(n)` that returns `[n, n - 1, ..., 1]` using a **`while` "
        "loop** — no `range`, no `reversed`.\n\n"
        "`countdown(3)` gives `[3, 2, 1]`. For `n` of `0` or less, return `[]`."
    ),
    hint=(
        "A `while` loop needs three things you must write yourself: a counter before "
        "the loop, a condition that will eventually go false, and a step inside the "
        "body that moves the counter toward that condition."
    ),
    solution=(
        "def countdown(n):\n"
        "    out = []\n"
        "    while n > 0:\n"
        "        out.append(n)\n"
        "        n -= 1\n"
        "    return out"
    ),
    explanation=(
        "A `for` loop gets its stopping condition from the iterable; a `while` loop "
        "does not, so forgetting the `n -= 1` is not a wrong answer but a hang. Check "
        "the condition against the *first* value too: here `n <= 0` means the body "
        "never runs, which is exactly the empty-list case."
    ),
    starter="def countdown(n):\n    ...",
    cases=[
        Case(expected=[3, 2, 1], args=(3,)),
        Case(expected=[1], args=(1,)),
        Case(expected=[], args=(0,)),
        Case(expected=[], args=(-2,)),
    ],
)

q(
    qid="Q-159",
    level=Level.L1,
    topic="Break/Continue",
    kind="function",
    entry="first_negative",
    prompt=(
        "Write `first_negative(numbers)` that returns the first negative number in "
        "the list, or `None` if there is not one.\n\n"
        "Stop scanning as soon as you find it — do not walk the rest of the list."
    ),
    hint=(
        "A `return` inside a loop leaves the function immediately, which is the "
        "shortest way to stop early. `break` would only leave the loop, and you would "
        "still need to say what to hand back."
    ),
    solution=(
        "def first_negative(numbers):\n"
        "    for n in numbers:\n"
        "        if n < 0:\n"
        "            return n\n"
        "    return None"
    ),
    explanation=(
        "Returning from inside the loop is the idiomatic early exit in a function: it "
        "replaces a `break` plus a result variable plus a check afterwards. The trailing "
        "`return None` is what the function does when the loop finishes without finding "
        "anything — leave it off and Python returns `None` anyway, but a reader has to "
        "guess whether you meant to."
    ),
    starter="def first_negative(numbers):\n    ...",
    cases=[
        Case(expected=-2, args=([1, -2, 3, -4],)),
        Case(expected=None, args=([1, 2],)),
        Case(expected=None, args=([],)),
        Case(expected=-1, args=([-1],)),
        Case(expected=-5, args=([0, 0, -5],)),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-160",
    level=Level.L2,
    topic="Conditionals",
    kind="function",
    entry="grade",
    prompt=(
        "Write `grade(score)` that returns a letter for a numeric score:\n\n"
        "- `'A'` for 90 and above\n"
        "- `'B'` for 80 to 89\n"
        "- `'C'` for 70 to 79\n"
        "- `'F'` below 70\n\n"
        "Use a single `if`/`elif` ladder with one test per branch — no chained "
        "comparisons, no `and`."
    ),
    hint=(
        "Each branch only has to test its lower bound, because reaching it already "
        "proves every earlier bound failed. That is only true if the branches are in "
        "the right order — work out which order that is."
    ),
    solution=(
        "def grade(score):\n"
        "    if score >= 90:\n"
        '        return "A"\n'
        "    elif score >= 80:\n"
        '        return "B"\n'
        "    elif score >= 70:\n"
        '        return "C"\n'
        "    else:\n"
        '        return "F"'
    ),
    explanation=(
        "An `elif` ladder over overlapping thresholds only works from the most "
        "restrictive end inward — put `>= 70` first and every passing score becomes a "
        "`C`, with no error to tell you. The falling-through structure is what lets "
        "each branch test a single bound instead of `80 <= score < 90`."
    ),
    starter="def grade(score):\n    ...",
    cases=[
        Case(expected="A", args=(95,)),
        Case(expected="A", args=(90,)),
        Case(expected="B", args=(85,)),
        Case(expected="C", args=(70,)),
        Case(expected="F", args=(69,)),
        Case(expected="F", args=(0,)),
    ],
)

q(
    qid="Q-161",
    level=Level.L2,
    topic="Conditionals",
    kind="function",
    entry="fizzbuzz_word",
    prompt=(
        "Write `fizzbuzz_word(n)` for one integer:\n\n"
        "- `'FizzBuzz'` when `n` divides by both 3 and 5\n"
        "- `'Fizz'` when it divides by 3 only\n"
        "- `'Buzz'` when it divides by 5 only\n"
        "- otherwise the number as a string, e.g. `'7'`\n\n"
        "Return a string in every case."
    ),
    hint=(
        "One of the four conditions is strictly stronger than two of the others, so "
        "in an `elif` ladder its position is forced. Work out which, and the rest of "
        "the ordering does not matter."
    ),
    solution=(
        "def fizzbuzz_word(n):\n"
        "    if n % 3 == 0 and n % 5 == 0:\n"
        '        return "FizzBuzz"\n'
        "    elif n % 3 == 0:\n"
        '        return "Fizz"\n'
        "    elif n % 5 == 0:\n"
        '        return "Buzz"\n'
        "    return str(n)"
    ),
    explanation=(
        "The combined test has to come first, because any number divisible by 15 also "
        "passes the `% 3` test and would be claimed by that branch — the ordering *is* "
        "the algorithm. Watch `0`: it divides by everything, so it is `'FizzBuzz'`, "
        "which is the case most hand-written FizzBuzz loops never see because they "
        "start at 1."
    ),
    starter="def fizzbuzz_word(n):\n    ...",
    cases=[
        Case(expected="FizzBuzz", args=(15,)),
        Case(expected="Fizz", args=(3,)),
        Case(expected="Buzz", args=(5,)),
        Case(expected="7", args=(7,)),
        Case(expected="FizzBuzz", args=(0,)),
        Case(expected="Fizz", args=(-9,)),
    ],
)

q(
    qid="Q-162",
    level=Level.L2,
    topic="Range",
    kind="function",
    entry="backwards",
    prompt=(
        "Write `backwards(start, stop)` that returns a list counting **down** from "
        "`start`, stopping just before `stop`.\n\n"
        "`backwards(5, 0)` gives `[5, 4, 3, 2, 1]`. Use a single `range` with a "
        "negative step — no `reversed`, no slicing."
    ),
    hint=(
        "The third argument to `range` is the step, and it is allowed to be negative. "
        "The half-open rule does not flip when it is: `stop` is still excluded."
    ),
    solution="def backwards(start, stop):\n    return list(range(start, stop, -1))",
    explanation=(
        "With a negative step `range` keeps going while the value is *greater* than "
        "`stop`, so `range(0, 5, -1)` is simply empty rather than an error — a silent "
        "empty loop is the usual symptom of a step with the wrong sign. `stop` stays "
        "exclusive in both directions, which is why counting down to `1` means passing "
        "`0` as the stop."
    ),
    starter="def backwards(start, stop):\n    ...",
    cases=[
        Case(expected=[5, 4, 3, 2, 1], args=(5, 0)),
        Case(expected=[], args=(3, 3)),
        Case(expected=[], args=(0, 5)),
        Case(expected=[2, 1, 0], args=(2, -1)),
    ],
)

q(
    qid="Q-163",
    level=Level.L2,
    topic="Range",
    kind="function",
    entry="every_kth",
    prompt=(
        "Write `every_kth(start, stop, step)` that returns "
        "`list(range(start, stop, step))` — the full three-argument form.\n\n"
        "The body is one line; the work is predicting the cases, including what the "
        "checker expects when `step` is `0`."
    ),
    hint=(
        "Three of the cases are ordinary. The last one asks what `range` does with a "
        "step that can never make progress — it does not return an empty sequence, and "
        "it does not loop forever either."
    ),
    solution="def every_kth(start, stop, step):\n    return list(range(start, stop, step))",
    explanation=(
        "A step of `0` would describe an infinite sequence, so `range` refuses up "
        "front with `ValueError` rather than hanging — failing at construction time is "
        "much kinder than failing during iteration. Note the arguments are positional "
        "only: `range(stop=5)` is a `TypeError`, unusual for a builtin."
    ),
    starter="def every_kth(start, stop, step):\n    ...",
    cases=[
        Case(expected=[0, 3, 6, 9], args=(0, 10, 3)),
        Case(expected=[1], args=(1, 2, 5)),
        Case(expected=[], args=(0, 0, 1)),
        Case(expected=[10, 5], args=(10, 0, -5)),
        Case(expected=None, args=(0, 5, 0), raises=ValueError),
    ],
)

q(
    qid="Q-164",
    level=Level.L2,
    topic="For Loops",
    kind="function",
    entry="positions",
    prompt=(
        "Write `positions(items, target)` that returns a list of **every index** at "
        "which `target` appears, in increasing order.\n\n"
        "`positions(['a', 'b', 'a'], 'a')` gives `[0, 2]`. Return `[]` when it never "
        "appears. Use `enumerate` rather than indexing with `range(len(...))`."
    ),
    hint=(
        "`enumerate` hands you a pair on each pass — the counter and the element — so "
        "you can unpack two loop variables at once and never touch the list by index."
    ),
    solution=(
        "def positions(items, target):\n"
        "    found = []\n"
        "    for index, value in enumerate(items):\n"
        "        if value == target:\n"
        "            found.append(index)\n"
        "    return found"
    ),
    explanation=(
        "`enumerate` exists so you stop writing `for i in range(len(items))` and then "
        "`items[i]` on every line — it is faster, reads better, and works on any "
        "iterable including ones with no length. Pass `start=1` when you want "
        "human-facing numbering; changing the counter's base is not the same as "
        "changing the index."
    ),
    starter="def positions(items, target):\n    ...",
    cases=[
        Case(expected=[0, 2], args=(["a", "b", "a"], "a")),
        Case(expected=[], args=([1, 2], 3)),
        Case(expected=[], args=([], "x")),
        Case(expected=[0, 1, 2], args=([0, 0, 0], 0)),
        Case(expected=[1], args=([9, 4, 9, 9], 4)),
    ],
)

q(
    qid="Q-165",
    level=Level.L2,
    topic="While Loops",
    kind="function",
    entry="digits",
    prompt=(
        "Write `digits(n)` that returns how many decimal digits a non-negative "
        "integer has, using a `while` loop and arithmetic only.\n\n"
        "`digits(100)` is `3` and `digits(0)` is `1`. No `str()`, no `len()`, no "
        "`math.log10`."
    ),
    hint=(
        "Floor-dividing by 10 chops one digit off the right-hand end. Count how many "
        "chops you can make — and decide what your counter should start at so that "
        "zero comes out right."
    ),
    solution=(
        "def digits(n):\n"
        "    count = 1\n"
        "    while n >= 10:\n"
        "        n //= 10\n"
        "        count += 1\n"
        "    return count"
    ),
    explanation=(
        "Starting the counter at `1` rather than `0` is what makes `0` — a number with "
        "no divisions left to do but still one digit on the page — come out correct "
        "without a special case. The loop condition must also shrink `n` every pass: "
        "`n /= 10` instead of `n //= 10` turns this into a float that approaches zero "
        "forever and never reaches it."
    ),
    starter="def digits(n):\n    ...",
    cases=[
        Case(expected=1, args=(0,)),
        Case(expected=1, args=(7,)),
        Case(expected=2, args=(10,)),
        Case(expected=3, args=(100,)),
        Case(expected=5, args=(99999,)),
    ],
)

q(
    qid="Q-166",
    level=Level.L2,
    topic="Break/Continue",
    kind="function",
    entry="sum_until_stop",
    prompt=(
        "Write `sum_until_stop(items)` that walks a list and returns a running total "
        "of the numbers in it, with two rules:\n\n"
        "- a `None` entry is skipped and the walk carries on;\n"
        "- the string `'stop'` ends the walk immediately, and nothing after it counts.\n\n"
        "Use `continue` for the first rule and `break` for the second. An empty list "
        "totals `0`."
    ),
    hint=(
        "One of the two keywords abandons the current pass and starts the next; the "
        "other abandons the loop entirely. Test for `None` with an identity check, not "
        "with truthiness — `0` is a legitimate number here."
    ),
    solution=(
        "def sum_until_stop(items):\n"
        "    running = 0\n"
        "    for item in items:\n"
        "        if item is None:\n"
        "            continue\n"
        '        if item == "stop":\n'
        "            break\n"
        "        running += item\n"
        "    return running"
    ),
    explanation=(
        "`continue` jumps to the next iteration and `break` leaves the loop, and both "
        "only ever affect the innermost loop containing them. The `is None` test "
        "matters more than it looks: `if not item: continue` would silently drop every "
        "`0` from the total, which is the bug this shape of code is famous for."
    ),
    starter="def sum_until_stop(items):\n    ...",
    cases=[
        Case(expected=3, args=([1, 2, "stop", 4],)),
        Case(expected=3, args=([1, None, 2],)),
        Case(expected=0, args=([],)),
        Case(expected=0, args=(["stop"],)),
        Case(expected=1, args=([1, None, "stop", 5],)),
        Case(expected=3, args=([0, 3],)),
    ],
)

q(
    qid="Q-167",
    level=Level.L2,
    topic="Loop Else",
    kind="function",
    entry="is_prime",
    prompt=(
        "Write `is_prime(n)` returning a `bool`. A prime has no divisor other than 1 "
        "and itself; anything below 2 is not prime.\n\n"
        "Structure it with a **`for`/`else`**: `break` out of the loop when you find a "
        "divisor, and let the loop's `else` clause handle the case where you never "
        "did. Trial division up to the square root is enough."
    ),
    hint=(
        "A loop may carry an `else` clause, and it runs only when the loop finished "
        "its iterable without hitting a `break`. Read it as *no-break*, not as "
        "*otherwise* — that is the one mental substitution that makes it click."
    ),
    solution=(
        "def is_prime(n):\n"
        "    if n < 2:\n"
        "        return False\n"
        "    for d in range(2, int(n ** 0.5) + 1):\n"
        "        if n % d == 0:\n"
        "            break\n"
        "    else:\n"
        "        return True\n"
        "    return False"
    ),
    explanation=(
        "`for`/`else` is Python's answer to the 'did I find it?' flag variable: the "
        "`else` block runs exactly when the search fell through without breaking. "
        "Almost everyone reads it as pairing with the `if` inside the loop, which is "
        "why the feature has a reputation for being confusing — the keyword should "
        "have been `nobreak`."
    ),
    starter="def is_prime(n):\n    ...",
    cases=[
        Case(expected=True, args=(2,)),
        Case(expected=True, args=(3,)),
        Case(expected=False, args=(4,)),
        Case(expected=False, args=(1,)),
        Case(expected=False, args=(0,)),
        Case(expected=False, args=(9,)),
        Case(expected=True, args=(97,)),
        Case(expected=False, args=(91,)),
    ],
)

q(
    qid="Q-168",
    level=Level.L2,
    topic="For Loops",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "nums = [1, 2, 2, 3]\n"
        "for n in nums:\n"
        "    if n % 2 == 0:\n"
        "        nums.remove(n)\n"
        "print(nums)\n"
        "print(len(nums))\n"
        "```\n\n"
        "Set `answer` to the two printed lines, e.g. `answer = \"[1, 2, 3]\\n3\"`. "
        "Print the list exactly as Python would."
    ),
    hint=(
        "A list iterator holds a position, not a copy. Follow that position by hand, "
        "one number at a time, and note what sits at it after a removal shifts "
        "everything left."
    ),
    solution='answer = "[1, 2, 3]\\n3"',
    explanation=(
        "Iterating a list walks an internal index, so deleting an element shifts the "
        "tail left and the iterator skips straight over whatever moved into the slot "
        "it just visited — here the second `2` is never examined. Nothing raises, which "
        "is what makes it dangerous; iterate over a copy (`for n in nums[:]`) or build "
        "a new list instead."
    ),
    starter="answer = ...",
    cases=[Case(expected="[1, 2, 3]\n3")],
)

q(
    qid="Q-169",
    level=Level.L2,
    topic="While Loops",
    kind="function",
    entry="collatz_steps",
    prompt=(
        "Write `collatz_steps(n)` for a positive integer `n`. Repeatedly halve it when "
        "it is even and replace it with `3 * n + 1` when it is odd, until it reaches "
        "`1`. Return **how many steps** that took.\n\n"
        "`collatz_steps(1)` is `0` — already there. `collatz_steps(3)` is `7`."
    ),
    hint=(
        "The loop condition is the finish line, not a counter: keep going *while* the "
        "value is not yet `1`. Count one step per transformation, and use integer "
        "division so the value stays an `int`."
    ),
    solution=(
        "def collatz_steps(n):\n"
        "    steps = 0\n"
        "    while n != 1:\n"
        "        if n % 2 == 0:\n"
        "            n //= 2\n"
        "        else:\n"
        "            n = 3 * n + 1\n"
        "        steps += 1\n"
        "    return steps"
    ),
    explanation=(
        "This is the honest use of `while`: the number of iterations is unknown before "
        "you start, so no `range` could express it. It also shows the risk — nobody has "
        "proved the sequence reaches `1` for every input, so the loop's termination "
        "rests on a conjecture, and a `while` whose exit you cannot argue for is a hang "
        "waiting to happen."
    ),
    starter="def collatz_steps(n):\n    ...",
    cases=[
        Case(expected=0, args=(1,)),
        Case(expected=1, args=(2,)),
        Case(expected=7, args=(3,)),
        Case(expected=8, args=(6,)),
        Case(expected=111, args=(27,)),
    ],
)

q(
    qid="Q-170",
    level=Level.L2,
    topic="Conditionals",
    kind="function",
    entry="labels",
    prompt=(
        "Write `labels(numbers)` that returns a list of strings — `'neg'`, `'zero'` "
        "or `'pos'` for each number, in order.\n\n"
        "Build it as a **single list comprehension** whose element expression is a "
        "conditional expression. No `if` statements, no `append`."
    ),
    hint=(
        "A conditional expression can have another conditional expression as its "
        "`else` branch, which is how you get three outcomes from a construct that "
        "only offers two. Parenthesise it inside the comprehension for readability."
    ),
    solution=(
        "def labels(numbers):\n"
        '    return ["neg" if n < 0 else ("zero" if n == 0 else "pos") for n in numbers]'
    ),
    explanation=(
        "Chained conditional expressions are the expression-level equivalent of an "
        "`if`/`elif` ladder and obey the same ordering rule — each test only sees the "
        "values the earlier ones rejected. Two levels read fine; beyond that the "
        "statement form is clearer, and a lookup table is clearer still."
    ),
    starter="def labels(numbers):\n    ...",
    cases=[
        Case(expected=["neg", "zero", "pos"], args=([-1, 0, 1],)),
        Case(expected=[], args=([],)),
        Case(expected=["pos"], args=([5],)),
        Case(expected=["zero", "zero"], args=([0, 0],)),
        Case(expected=["neg", "pos"], args=([-0.5, 0.5],)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-171",
    level=Level.L3,
    topic="Loop Else",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def find(items, target):\n"
        "    for item in items:\n"
        "        if item == target:\n"
        '            print("found")\n'
        "            break\n"
        "    else:\n"
        '        print("missing")\n'
        "\n"
        "find([1, 2, 3], 2)\n"
        "find([1, 2, 3], 9)\n"
        "find([], 9)\n"
        "```\n\n"
        "Set `answer` to the three printed lines, separated by `\\n`."
    ),
    hint=(
        "That `else` is attached to the `for`, not to the `if` — the indentation is "
        "the only clue and it is easy to misread. Ask what has to *not* happen for it "
        "to run, and then check the empty-list call against that rule."
    ),
    solution='answer = "found\\nmissing\\nmissing"',
    explanation=(
        "A loop's `else` runs when the loop exhausts its iterable without a `break` — "
        "and an iterable that was empty to begin with was exhausted immediately, so "
        "the third call prints `missing` too. Expecting the `else` to be skipped on an "
        "empty sequence is the single most common misprediction here."
    ),
    starter="answer = ...",
    cases=[Case(expected="found\nmissing\nmissing")],
)

q(
    qid="Q-172",
    level=Level.L3,
    topic="Range",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "r = range(3)\n"
        "print(r)\n"
        "print(r == [0, 1, 2])\n"
        "print(list(r) == [0, 1, 2])\n"
        "print(r[-1])\n"
        "```\n\n"
        "Set `answer` to the four printed lines. The first one is not `[0, 1, 2]` — "
        "give it character for character."
    ),
    hint=(
        "`range` is its own type, not a list-producing function. Ask what such an "
        "object could usefully print, and whether an object of one type can ever "
        "compare equal to a list."
    ),
    solution='answer = "range(0, 3)\\nFalse\\nTrue\\n2"',
    explanation=(
        "A `range` is a lazy sequence storing only start, stop and step, so it prints "
        "as its own constructor call and is never `==` to a list, whatever it would "
        "produce. It is still a real sequence — indexable, sliceable, reversible, and "
        "`in` on it is O(1) arithmetic — which is why `list(...)` is needed only when "
        "you genuinely want the elements in memory."
    ),
    starter="answer = ...",
    cases=[Case(expected="range(0, 3)\nFalse\nTrue\n2")],
)

q(
    qid="Q-173",
    level=Level.L3,
    topic="For Loops",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "for i in range(3):\n"
        "    pass\n"
        "print(i)\n"
        "\n"
        "total = 0\n"
        "for i in []:\n"
        "    total += 1\n"
        "print(i)\n"
        "print(total)\n"
        "```\n\n"
        "Set `answer` to the three printed lines."
    ),
    hint=(
        "Ask two separate questions: does a loop create a scope of its own, and does "
        "entering a loop over an empty iterable touch the loop variable at all?"
    ),
    solution='answer = "2\\n2\\n0"',
    explanation=(
        "Python has no block scope: the loop variable is an ordinary local that "
        "outlives the loop, holding whatever the final iteration left in it. A loop "
        "over an empty iterable never assigns it, so the *old* value survives — which "
        "is how stale data from a previous loop silently leaks into the code after it, "
        "or how you get a `NameError` on a loop that simply never ran."
    ),
    starter="answer = ...",
    cases=[Case(expected="2\n2\n0")],
)

q(
    qid="Q-174",
    level=Level.L3,
    topic="Loop Else",
    kind="function",
    entry="scan",
    prompt=(
        "Write `scan(codes, allowed)` that returns the first entry of `codes` that is "
        "not in `allowed`, or the string `'all ok'` when every entry is allowed.\n\n"
        "Structure it with a `for`/`else` — `break` on the offender, and return the "
        "verdict from the `else`. An empty `codes` list is `'all ok'`."
    ),
    hint=(
        "After a `break`, the loop variable still holds the element you broke on — "
        "there is no need for a second variable to carry it out of the loop. Put the "
        "success answer in the `else` and the failure answer after the loop."
    ),
    solution=(
        "def scan(codes, allowed):\n"
        "    for code in codes:\n"
        "        if code not in allowed:\n"
        "            break\n"
        "    else:\n"
        '        return "all ok"\n'
        "    return code"
    ),
    explanation=(
        "This is the shape `for`/`else` was designed for: a search with two distinct "
        "endings, expressed without a `found = False` flag that some later edit will "
        "forget to reset. It leans on the loop variable surviving the loop — deliberate "
        "here, and the same rule that causes the surprise in Q-173."
    ),
    starter="def scan(codes, allowed):\n    ...",
    cases=[
        Case(expected="all ok", args=(["a", "b"], ["a", "b"])),
        Case(expected="x", args=(["a", "x", "y"], ["a"])),
        Case(expected="all ok", args=([], ["a"])),
        Case(expected="x", args=(["x"], [])),
        Case(expected="all ok", args=(["a", "a"], ["a"])),
    ],
)

q(
    qid="Q-175",
    level=Level.L3,
    topic="Break/Continue",
    kind="custom",
    entry="take_until",
    constraints=["no-builtin:sum", "max-lines:8"],
    prompt=(
        "Write `take_until(numbers, limit)` that returns how many items you can take "
        "from the **front** of the list before the running total would exceed "
        "`limit`.\n\n"
        "That is the largest `k` for which the first `k` items sum to `limit` or less. "
        "Stop as soon as the total goes over — do not keep scanning. No `sum()`, and "
        "at most 8 lines of body."
    ),
    hint=(
        "Keep two counters, not one: the running total decides when to stop, and a "
        "separate count is the answer. The order of 'add', 'test' and 'count' inside "
        "the body is the whole question."
    ),
    solution=(
        "def take_until(numbers, limit):\n"
        "    running = 0\n"
        "    count = 0\n"
        "    for n in numbers:\n"
        "        running += n\n"
        "        if running > limit:\n"
        "            break\n"
        "        count += 1\n"
        "    return count"
    ),
    explanation=(
        "The increment has to come *after* the test, otherwise the item that broke the "
        "budget is counted anyway — a classic off-by-one that only shows up on the "
        "boundary case where the total lands exactly on the limit. Breaking early is "
        "not just an optimisation here: with negative numbers in the list, continuing "
        "would give a different and wrong answer."
    ),
    starter="def take_until(numbers, limit):\n    ...",
    cases=[
        Case(expected=3, args=([1, 2, 3, 4], 6)),
        Case(expected=0, args=([5], 4)),
        Case(expected=0, args=([], 10)),
        Case(expected=3, args=([1, 1, 1], 10)),
        Case(expected=1, args=([2, 2, 2], 3)),
        Case(expected=2, args=([0, 0], 0)),
        Case(expected=0, args=([10, -20, 5], 5)),
    ],
)

q(
    qid="Q-176",
    level=Level.L3,
    topic="While Loops",
    kind="function",
    entry="gcd",
    prompt=(
        "Write `gcd(a, b)` returning the greatest common divisor of two non-negative "
        "integers, using Euclid's algorithm in a `while` loop.\n\n"
        "Repeatedly replace `(a, b)` with `(b, a % b)` until `b` is `0`; the answer is "
        "then `a`. `gcd(10, 0)` is `10`. Do not import `math`."
    ),
    hint=(
        "The loop condition can be the value itself rather than a comparison. Tuple "
        "assignment lets you do both replacements at once, which is what keeps the old "
        "`a` available for the remainder."
    ),
    solution=(
        "def gcd(a, b):\n"
        "    while b:\n"
        "        a, b = b, a % b\n"
        "    return a"
    ),
    explanation=(
        "`while b:` uses truthiness to mean 'while there is a remainder left', and the "
        "simultaneous assignment is what makes the step safe — computing `a = b` first "
        "would destroy the `a` that `a % b` still needs. Each remainder is strictly "
        "smaller than the previous divisor, which is the argument that this loop "
        "terminates; every `while` you write deserves one."
    ),
    starter="def gcd(a, b):\n    ...",
    cases=[
        Case(expected=6, args=(12, 18)),
        Case(expected=6, args=(18, 12)),
        Case(expected=1, args=(7, 13)),
        Case(expected=10, args=(10, 0)),
        Case(expected=5, args=(0, 5)),
        Case(expected=25, args=(100, 75)),
    ],
)

q(
    qid="Q-177",
    level=Level.L3,
    topic="For Loops",
    kind="custom",
    entry="squares_of_evens",
    constraints=["needs-comprehension", "max-lines:2"],
    prompt=(
        "Write `squares_of_evens(n)` that returns the squares of the even numbers in "
        "`range(n)`, in order.\n\n"
        "`squares_of_evens(6)` gives `[0, 4, 16]`. Write it as a **single list "
        "comprehension** with a filter clause — no `for` statement, no `append`, body "
        "of at most 2 lines."
    ),
    hint=(
        "A comprehension has three slots: what to produce, what to iterate, and an "
        "optional condition that decides which items survive. Note that the filter "
        "goes at the end, not before the `for`."
    ),
    solution="def squares_of_evens(n):\n    return [x * x for x in range(n) if x % 2 == 0]",
    explanation=(
        "A trailing `if` in a comprehension *filters* — items failing it produce "
        "nothing at all — whereas a conditional expression in the leading slot "
        "produces a value for every item. Confusing the two is why `[x if x % 2 == 0 "
        "for x in r]` is a `SyntaxError`: a filter there has nowhere to put the "
        "rejected items."
    ),
    starter="def squares_of_evens(n):\n    ...",
    cases=[
        Case(expected=[0, 4, 16], args=(6,)),
        Case(expected=[0], args=(1,)),
        Case(expected=[], args=(0,)),
        Case(expected=[0], args=(2,)),
        Case(expected=[0, 4, 16, 36], args=(7,)),
    ],
)

q(
    qid="Q-178",
    level=Level.L3,
    topic="While Loops",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "x = 0.0\n"
        "count = 0\n"
        "while x != 1.0:\n"
        "    x += 0.1\n"
        "    count += 1\n"
        "    if count > 20:\n"
        "        break\n"
        "print(count)\n"
        "print(x == 1.0)\n"
        "```\n\n"
        "Set `answer` to the two printed lines. The first is a number — say exactly "
        "which."
    ),
    hint=(
        "Ask whether ten additions of `0.1` land on precisely `1.0` in binary "
        "floating point. Then work out on which pass the guard actually fires — the "
        "test runs after the increment."
    ),
    solution='answer = "21\\nFalse"',
    explanation=(
        "`0.1` is not exactly representable in binary, so the accumulated value steps "
        "*past* `1.0` without ever equalling it and the `!=` condition never goes "
        "false — without the guard this loop runs forever. Never drive a loop with "
        "`==`/`!=` on floats: compare with `<`/`>=`, or count integer iterations and "
        "derive the float from the counter."
    ),
    starter="answer = ...",
    cases=[Case(expected="21\nFalse")],
)

q(
    qid="Q-179",
    level=Level.L3,
    topic="Conditionals",
    kind="function",
    entry="overlap",
    prompt=(
        "Write `overlap(a_lo, a_hi, b_lo, b_hi)` returning `True` when two **inclusive** "
        "ranges share at least one point, and `False` otherwise.\n\n"
        "Ranges that merely touch at an endpoint do overlap. Each range is given "
        "low-then-high. Return a `bool`, and do not enumerate the points."
    ),
    hint=(
        "Listing the ways two ranges can overlap gives you four or five cases. "
        "Listing the ways they can *miss* gives you two. Solve the easier problem and "
        "negate it."
    ),
    solution=(
        "def overlap(a_lo, a_hi, b_lo, b_hi):\n"
        "    return not (a_hi < b_lo or b_hi < a_lo)"
    ),
    explanation=(
        "Two intervals miss only when one ends entirely before the other begins, so "
        "negating a two-term `or` beats enumerating the overlap cases — and it is "
        "symmetric by construction, so no argument order can catch it out. Inclusive "
        "bounds are why the comparison is strict `<`: with half-open ranges you would "
        "want `<=`, and mixing the two up is the classic interval off-by-one."
    ),
    starter="def overlap(a_lo, a_hi, b_lo, b_hi):\n    ...",
    cases=[
        Case(expected=True, args=(1, 5, 4, 9)),
        Case(expected=False, args=(1, 3, 4, 9)),
        Case(expected=True, args=(1, 5, 5, 9)),
        Case(expected=False, args=(4, 9, 1, 3)),
        Case(expected=True, args=(1, 10, 2, 3)),
        Case(expected=True, args=(1, 1, 1, 1)),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-180",
    level=Level.L4,
    topic="Loop Else",
    kind="function",
    entry="find_in_grid",
    prompt=(
        "Write `find_in_grid(grid, target)` where `grid` is a list of rows (lists). "
        "Return the `(row, col)` tuple of the **first** occurrence, scanning row by "
        "row left to right, or `None` when the target is absent.\n\n"
        "The constraint: break out of **both** loops with `break`, never with "
        "`return` from inside them, and never with a flag variable. Use `for`/`else` "
        "on both loops to route the control flow. Rows may be empty; the grid may be "
        "empty."
    ),
    hint=(
        "`break` only escapes the loop it sits in, so escaping two takes two breaks. "
        "Put the inner loop's `else` to work as the 'this row had nothing' path — what "
        "should that path do to the outer loop?"
    ),
    solution=(
        "def find_in_grid(grid, target):\n"
        "    for r, row in enumerate(grid):\n"
        "        for c, value in enumerate(row):\n"
        "            if value == target:\n"
        "                break\n"
        "        else:\n"
        "            continue\n"
        "        break\n"
        "    else:\n"
        "        return None\n"
        "    return (r, c)"
    ),
    explanation=(
        "This is the canonical double-break idiom: the inner `else` means 'no match in "
        "this row', so it `continue`s the outer loop and skips the outer `break` that "
        "would otherwise fire on every row. The outer `else` then means 'no row "
        "matched'. It is worth writing once to understand `for`/`else` properly — and "
        "in real code, extract the search into a function and `return`, which is why "
        "this idiom stays a curiosity."
    ),
    starter="def find_in_grid(grid, target):\n    ...",
    cases=[
        Case(expected=(1, 0), args=([[1, 2], [3, 4]], 3)),
        Case(expected=(0, 0), args=([[1, 2], [3, 4]], 1)),
        Case(expected=None, args=([[1, 2], [3, 4]], 9)),
        Case(expected=None, args=([], 1)),
        Case(expected=(1, 0), args=([[], [5]], 5)),
        Case(expected=(0, 0), args=([[1, 1]], 1)),
        Case(expected=None, args=([[], []], 1)),
    ],
)

q(
    qid="Q-181",
    level=Level.L4,
    topic="While Loops",
    kind="function",
    entry="run_lengths",
    prompt=(
        "Write `run_lengths(text)` that compresses a string into a list of "
        "`(character, count)` tuples, one per run of identical consecutive "
        "characters.\n\n"
        "`run_lengths('aaabb')` gives `[('a', 3), ('b', 2)]`. An empty string gives "
        "`[]`. Use an index-driven `while` loop — no `itertools.groupby`."
    ),
    hint=(
        "Two indices, not one: the outer marks where the current run starts, and an "
        "inner scan walks forward while the character stays the same. The run's length "
        "is the distance between them."
    ),
    solution=(
        "def run_lengths(text):\n"
        "    runs = []\n"
        "    i = 0\n"
        "    while i < len(text):\n"
        "        j = i\n"
        "        while j < len(text) and text[j] == text[i]:\n"
        "            j += 1\n"
        "        runs.append((text[i], j - i))\n"
        "        i = j\n"
        "    return runs"
    ),
    explanation=(
        "The outer loop terminates because `j` is always at least `i + 1` when the "
        "inner scan stops — the first character of a run always matches itself — so "
        "`i = j` strictly advances. Order matters in the inner condition: testing "
        "`j < len(text)` first is what stops `text[j]` from raising, and `and` "
        "short-circuits so the index is never evaluated out of bounds."
    ),
    starter="def run_lengths(text):\n    ...",
    cases=[
        Case(expected=[("a", 3), ("b", 2)], args=("aaabb",)),
        Case(expected=[], args=("",)),
        Case(expected=[("a", 1), ("b", 1), ("c", 1)], args=("abc",)),
        Case(expected=[("a", 2), ("b", 1), (" ", 1), ("a", 2)], args=("aab aa",)),
        Case(expected=[("z", 4)], args=("zzzz",)),
    ],
)

q(
    qid="Q-182",
    level=Level.L4,
    topic="For Loops",
    kind="custom",
    entry="longest_run",
    constraints=["no-builtin:max", "max-lines:12"],
    prompt=(
        "Write `longest_run(items)` that returns the length of the longest stretch of "
        "**equal consecutive** items in a list.\n\n"
        "`longest_run([1, 1, 2, 2, 2, 3])` is `3`. An empty list gives `0`. One pass "
        "over the list, no `max()`, at most 12 lines of body."
    ),
    hint=(
        "Track the current streak and the best streak seen so far. The awkward part is "
        "the very first item, which has no predecessor — pick a starting 'previous' "
        "value that can never equal a real element."
    ),
    solution=(
        "def longest_run(items):\n"
        "    best = 0\n"
        "    current = 0\n"
        "    previous = object()\n"
        "    for item in items:\n"
        "        if item == previous:\n"
        "            current += 1\n"
        "        else:\n"
        "            current = 1\n"
        "        if current > best:\n"
        "            best = current\n"
        "        previous = item\n"
        "    return best"
    ),
    explanation=(
        "A bare `object()` is the standard sentinel: it is equal to nothing but "
        "itself, so the first comparison is guaranteed to fail — unlike `None` or `-1`, "
        "which are real values a caller might legitimately pass. Updating `best` inside "
        "the loop rather than only at the end is what handles the case where the "
        "longest run is the final one and no 'else' branch ever closes it out."
    ),
    starter="def longest_run(items):\n    ...",
    cases=[
        Case(expected=3, args=([1, 1, 2, 2, 2, 3],)),
        Case(expected=0, args=([],)),
        Case(expected=1, args=([1],)),
        Case(expected=1, args=([1, 2, 3],)),
        Case(expected=4, args=(["a", "a", "a", "a"],)),
        Case(expected=3, args=([1, 1, 2, 1, 1, 1],)),
    ],
)

q(
    qid="Q-183",
    level=Level.L4,
    topic="Loop Else",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "def drain(items, limit):\n"
        "    while items:\n"
        "        item = items.pop()\n"
        "        if item > limit:\n"
        '            print("big:", item)\n'
        "            break\n"
        "    else:\n"
        '        print("all small")\n'
        "\n"
        "drain([1, 2, 3], 10)\n"
        "drain([1, 9, 3], 5)\n"
        "drain([], 5)\n"
        "```\n\n"
        "Set `answer` to the three printed lines. Mind the exact spacing `print` puts "
        "between its two arguments."
    ),
    hint=(
        "`else` works on `while` by the same rule it works on `for`. `.pop()` with no "
        "argument takes from the **end** of the list, so walk each call from the right."
    ),
    solution='answer = "all small\\nbig: 9\\nall small"',
    explanation=(
        "A `while`'s `else` runs when the condition goes false — here when the list "
        "empties — and is skipped only when a `break` cut the loop short, which makes "
        "it the natural home for 'the search ran out'. Two things catch people: an "
        "empty list satisfies the else path immediately, and `.pop()` defaults to the "
        "last element, so `[1, 9, 3]` hits the `9` on the second pass rather than the "
        "first."
    ),
    starter="answer = ...",
    cases=[Case(expected="all small\nbig: 9\nall small")],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-184",
    level=Level.L5,
    topic="Loop Else",
    kind="custom",
    entry="first_common",
    constraints=["no-builtin:any", "no-builtin:all", "max-lines:14"],
    prompt=(
        "Write `first_common(seqs)` where `seqs` is a list of lists. Return the first "
        "element of `seqs[0]` that also appears in **every** other list, or `None` if "
        "there is no such element.\n\n"
        "Edge cases that are part of the specification: an empty `seqs` gives `None`; "
        "a `seqs` of exactly one list gives that list's first element (there is "
        "nothing to contradict it), or `None` when that list is empty.\n\n"
        "Use nested loops with `for`/`else` on the inner one. No `any()`, no `all()`, "
        "no sets, at most 14 lines of body."
    ),
    hint=(
        "Every candidate needs a verdict of 'survived all the other lists', which is "
        "exactly 'the inner loop finished without breaking'. The single-list case then "
        "falls out on its own — think about how many times an inner loop over an empty "
        "slice runs."
    ),
    solution=(
        "def first_common(seqs):\n"
        "    if not seqs:\n"
        "        return None\n"
        "    for candidate in seqs[0]:\n"
        "        for other in seqs[1:]:\n"
        "            if candidate not in other:\n"
        "                break\n"
        "        else:\n"
        "            return candidate\n"
        "    return None"
    ),
    explanation=(
        "`for`/`else` is how you express a universally quantified test without `all()`: "
        "reaching the `else` *means* no counterexample was found. The vacuous case is "
        "the elegant part — with one list the inner loop runs zero times, so the `else` "
        "fires immediately and the first element wins, which is the mathematically "
        "correct answer for 'true of every list in an empty collection'."
    ),
    starter="def first_common(seqs):\n    ...",
    cases=[
        Case(expected=2, args=([[1, 2, 3], [3, 2], [2, 5]],)),
        Case(expected=1, args=([[1, 2]],)),
        Case(expected=None, args=([],)),
        Case(expected=None, args=([[1, 2], [3]],)),
        Case(expected="b", args=([["a", "b"], ["b", "a"], ["b"]],)),
        Case(expected=None, args=([[], [1]],)),
        Case(expected=None, args=([[]],)),
    ],
)

q(
    qid="Q-185",
    level=Level.L5,
    topic="While Loops",
    kind="function",
    entry="josephus",
    prompt=(
        "Write `josephus(n, k)`. `n` people numbered `1..n` stand in a circle. "
        "Starting the count at person 1, every `k`-th person is removed; counting then "
        "resumes with the next survivor and wraps around the shrinking circle. Return "
        "the number of the last person left.\n\n"
        "`josephus(5, 2)` is `3`. `josephus(1, k)` is always `1`. Both `n` and `k` are "
        "at least 1. Simulate it with a `while` loop over a list."
    ),
    hint=(
        "Keep one index into the surviving list and advance it by `k - 1` each round, "
        "taking it modulo the *current* length so it wraps. After a removal, the same "
        "index already points at the next person to start counting from."
    ),
    solution=(
        "def josephus(n, k):\n"
        "    people = list(range(1, n + 1))\n"
        "    index = 0\n"
        "    while len(people) > 1:\n"
        "        index = (index + k - 1) % len(people)\n"
        "        people.pop(index)\n"
        "    return people[0]"
    ),
    explanation=(
        "The wrap-around is pure `%` against the current length, which is why the list "
        "shrinking under you is a feature here rather than the hazard it was in Q-168 — "
        "you control the index yourself instead of letting an iterator hold it. "
        "Termination is easy to argue: every pass removes exactly one element, so the "
        "loop runs `n - 1` times whatever `k` is."
    ),
    starter="def josephus(n, k):\n    ...",
    cases=[
        Case(expected=1, args=(1, 3)),
        Case(expected=3, args=(5, 2)),
        Case(expected=4, args=(7, 3)),
        Case(expected=2, args=(2, 1)),
        Case(expected=6, args=(6, 1)),
        Case(expected=5, args=(5, 1)),
        Case(expected=4, args=(10, 3)),
    ],
)

q(
    qid="Q-186",
    level=Level.L5,
    topic="While Loops",
    kind="custom",
    entry="to_base",
    constraints=["no-builtin:divmod", "max-lines:12"],
    prompt=(
        "Write `to_base(n, base)` that renders a non-negative integer in the given "
        "base as an **uppercase string**, using digits `0-9` then `A-F`.\n\n"
        "`to_base(255, 16)` is `'FF'`, `to_base(5, 2)` is `'101'`, `to_base(0, 2)` is "
        "`'0'`. Raise `ValueError` when `n` is negative or `base` is outside `2..16`.\n\n"
        "No `divmod`, no `bin`/`oct`/`hex`, no `int(..., base)`. At most 12 lines."
    ),
    hint=(
        "Repeated division by the base peels one digit off the right, so the digits "
        "come out in reverse order — decide up front whether you will prepend or "
        "reverse at the end. A string of digit characters indexed by the remainder "
        "saves you an `if` ladder."
    ),
    solution=(
        'DIGITS = "0123456789ABCDEF"\n\n\n'
        "def to_base(n, base):\n"
        "    if n < 0 or not 2 <= base <= 16:\n"
        '        raise ValueError(f"bad arguments: {n!r}, {base!r}")\n'
        "    if n == 0:\n"
        '        return "0"\n'
        '    out = ""\n'
        "    while n > 0:\n"
        "        out = DIGITS[n % base] + out\n"
        "        n //= base\n"
        "    return out"
    ),
    explanation=(
        "Zero needs its own branch because the loop is driven by `n > 0` and so "
        "produces nothing at all for it — an empty string, not `'0'`. Validating the "
        "arguments before the loop rather than inside it is the other half: a `base` "
        "of `1` would make `n //= base` a no-op and hang forever, so the guard is not "
        "politeness, it is the termination proof."
    ),
    starter="def to_base(n, base):\n    ...",
    cases=[
        Case(expected="101", args=(5, 2)),
        Case(expected="0", args=(0, 2)),
        Case(expected="FF", args=(255, 16)),
        Case(expected="10", args=(10, 10)),
        Case(expected="7", args=(7, 8)),
        Case(expected="FFF", args=(4095, 16)),
        Case(expected="1010", args=(10, 2)),
        Case(expected=None, args=(-1, 2), raises=ValueError),
        Case(expected=None, args=(5, 1), raises=ValueError),
        Case(expected=None, args=(5, 17), raises=ValueError),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-05",
    title="Guessing game engine",
    brief=(
        "Build `play(secret, guesses)` — the *engine* of a number-guessing game, with "
        "no `input()` anywhere.\n\n"
        "`secret` is the number to find and `guesses` is the list of numbers a player "
        "would have typed, in order. Walk them and return:\n\n"
        "```python\n"
        "{'feedback': ['too low', 'too high', 'correct'], 'won': True, 'attempts': 3}\n"
        "```\n\n"
        "Rules: append `'too low'`, `'too high'` or `'correct'` for each guess you "
        "process; stop immediately after a correct guess, so anything later in the "
        "list is ignored and does not count; `'won'` is a `bool`; `'attempts'` is how "
        "many guesses you actually processed. No guesses at all gives "
        "`{'feedback': [], 'won': False, 'attempts': 0}`."
    ),
    hint=(
        "The three outcomes are an `if`/`elif`/`else` on one comparison pair, and "
        "'stop immediately' is a `break` from the `for` loop. Derive `'attempts'` from "
        "the feedback list rather than keeping a third counter that can drift out of "
        "step with it."
    ),
    solution=(
        "def play(secret, guesses):\n"
        "    feedback = []\n"
        "    won = False\n"
        "    for guess in guesses:\n"
        "        if guess < secret:\n"
        '            feedback.append("too low")\n'
        "        elif guess > secret:\n"
        '            feedback.append("too high")\n'
        "        else:\n"
        '            feedback.append("correct")\n'
        "            won = True\n"
        "            break\n"
        "    return {\n"
        '        "feedback": feedback,\n'
        '        "won": won,\n'
        '        "attempts": len(feedback),\n'
        "    }"
    ),
    explanation=(
        "Splitting the engine from the I/O is what makes a game testable at all: "
        "`input()` in the middle of this loop would leave nothing a checker could call, "
        "whereas a pure function taking the guesses as data can be run a thousand times "
        "in a millisecond. The real interactive program is then a thin shell that "
        "collects a guess, calls the engine, and prints — the same separation that "
        "turns 'it works on my machine' into a test suite."
    ),
    entry="play",
    starter="def play(secret, guesses):\n    ...",
    cases=[
        Case(expected={"feedback": ["too low", "too high", "correct"], "won": True, "attempts": 3},
             args=(7, [3, 9, 7])),
        Case(expected={"feedback": ["too low", "too low"], "won": False, "attempts": 2},
             args=(7, [1, 2])),
        Case(expected={"feedback": [], "won": False, "attempts": 0},
             args=(7, [])),
        Case(expected={"feedback": ["correct"], "won": True, "attempts": 1},
             args=(7, [7, 1, 2])),
        Case(expected={"feedback": ["too low", "correct"], "won": True, "attempts": 2},
             args=(0, [-1, 0])),
    ],
)

NOTEBOOK = Notebook(
    number=5,
    slug="control_flow_and_loops",
    title="Control Flow & Loops",
    intro=(
        "Branching with `if`/`elif`/`else` and conditional expressions, repetition "
        "with `for` and `while`, counting with all three forms of `range`, and early "
        "exits with `break` and `continue`.\n\n"
        "Then the clause almost nobody knows exists: `else` on a loop. It runs when "
        "the loop finished *without* a `break`, it fires on empty sequences, and once "
        "you can read it you can delete every `found = False` flag you have ever "
        "written. The predict questions here — mutating a list while iterating it, the "
        "loop variable outliving its loop, `0.1` never reaching `1.0` — are the ones "
        "that turn into production bugs."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
