"""Notebook 02 - Strings (Q-037..Q-074)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-037",
    level=Level.L1,
    topic="Indexing",
    kind="function",
    entry="ends",
    prompt=(
        "Write `ends(text)` that returns the **tuple** `(first_character, "
        "last_character)` — both as one-character strings.\n\n"
        "`text` is never empty. Reach the last character without computing its "
        "position by hand."
    ),
    hint=(
        "Index `0` gets you the front. For the back, Python lets you count from the "
        "other end instead of writing `len(text) - 1`."
    ),
    solution="def ends(text):\n    return (text[0], text[-1])",
    explanation=(
        "A negative index counts backwards from the end, so `-1` is the last item and "
        "`len(text) - 1` is a longer spelling of the same thing. Indexing a string "
        "always hands back another *string* of length one — Python has no separate "
        "character type, which is why `text[0]` can be compared to `\"a\"` directly."
    ),
    starter="def ends(text):\n    ...",
    cases=[
        Case(expected=("p", "n"), args=("python",)),
        Case(expected=("a", "a"), args=("a",)),
        Case(expected=(" ", " "), args=("  x ",)),
        Case(expected=("h", "o"), args=("héllo",)),
    ],
)

q(
    qid="Q-038",
    level=Level.L1,
    topic="Indexing",
    kind="function",
    entry="middle_char",
    prompt=(
        "Write `middle_char(text)` that returns the single character sitting in the "
        "middle of `text`.\n\n"
        "`text` always has an **odd** length, so there is exactly one middle. "
        "`middle_char(\"abc\")` returns `'b'`."
    ),
    hint=(
        "An index has to be an `int`. `len(text) / 2` is not one — reach for the "
        "division operator that keeps you in integer territory."
    ),
    solution="def middle_char(text):\n    return text[len(text) // 2]",
    explanation=(
        "`text[len(text) / 2]` raises `TypeError: string indices must be integers` "
        "because `/` always produces a float, even for `6 / 2`. Floor division `//` is "
        "the index-arithmetic operator, and for an odd length it lands exactly on the "
        "middle: `5 // 2` is `2`, with two characters on each side."
    ),
    starter="def middle_char(text):\n    ...",
    cases=[
        Case(expected="b", args=("abc",)),
        Case(expected="a", args=("a",)),
        Case(expected="h", args=("python!",)),
        Case(expected="3", args=("12345",)),
    ],
)

q(
    qid="Q-039",
    level=Level.L1,
    topic="Slicing",
    kind="function",
    entry="first_n",
    prompt=(
        "Write `first_n(text, n)` that returns the first `n` characters of `text` as "
        "a string.\n\n"
        "If `text` is shorter than `n`, return the whole of it — do **not** add a "
        "guard clause for that, and do not raise."
    ),
    hint=(
        "One slice does all of this on its own. Try `\"hi\"[:5]` in a cell before you "
        "write any `if`."
    ),
    solution="def first_n(text, n):\n    return text[:n]",
    explanation=(
        "Slicing *clamps* its bounds instead of raising, which is the single biggest "
        "behavioural difference from indexing: `text[5]` on a 2-character string is an "
        "`IndexError`, while `text[:5]` is just the whole string. Leaving the start "
        "empty means 'from the beginning', so `text[:n]` reads as 'up to but not "
        "including position n'."
    ),
    starter="def first_n(text, n):\n    ...",
    cases=[
        Case(expected="pyt", args=("python", 3)),
        Case(expected="hi", args=("hi", 5)),
        Case(expected="", args=("python", 0)),
        Case(expected="", args=("", 3)),
    ],
)

q(
    qid="Q-040",
    level=Level.L1,
    topic="Slicing",
    kind="function",
    entry="drop_ends",
    prompt=(
        "Write `drop_ends(text)` that returns `text` with its first and last "
        "character removed.\n\n"
        "`drop_ends(\"python\")` is `'ytho'`. For a string of 0, 1 or 2 characters "
        "there is nothing left, so return `''` — again, without an `if`."
    ),
    hint=(
        "You need a slice with both ends given. The stop position is the one people "
        "get wrong: count it from the back rather than from the front."
    ),
    solution="def drop_ends(text):\n    return text[1:-1]",
    explanation=(
        "A slice's stop is *exclusive*, so `-1` as the stop means 'stop just before "
        "the last character' and drops exactly one. The short-string cases need no "
        "special handling because a slice whose start passes its stop yields `''` "
        "rather than an error."
    ),
    starter="def drop_ends(text):\n    ...",
    cases=[
        Case(expected="ytho", args=("python",)),
        Case(expected="", args=("ab",)),
        Case(expected="", args=("a",)),
        Case(expected="", args=("",)),
    ],
)

q(
    qid="Q-041",
    level=Level.L1,
    topic="Slicing",
    kind="function",
    entry="reverse",
    prompt=(
        "Write `reverse(text)` that returns `text` back to front, as a string.\n\n"
        "Use a slice — no loop, and no `reversed()` (which would give you an iterator, "
        "not a string)."
    ),
    hint=(
        "A slice takes a third number after a second colon. Making it negative changes "
        "the direction of travel."
    ),
    solution="def reverse(text):\n    return text[::-1]",
    explanation=(
        "`text[::-1]` is the canonical Python reversal: the step of `-1` walks "
        "backwards, and the omitted start and stop then mean 'the far end' and 'the "
        "near end' rather than their usual defaults. `reversed(text)` gives a lazy "
        "iterator, so it needs `\"\".join(reversed(text))` to become a string again."
    ),
    starter="def reverse(text):\n    ...",
    cases=[
        Case(expected="nohtyp", args=("python",)),
        Case(expected="", args=("",)),
        Case(expected="a", args=("a",)),
        Case(expected="racecar", args=("racecar",)),
        Case(expected="43 21", args=("12 34",)),
    ],
)

q(
    qid="Q-042",
    level=Level.L1,
    topic="F-strings",
    kind="function",
    entry="greet",
    prompt=(
        "Write `greet(name)` that returns the string `Hello, NAME!` with `name` "
        "substituted in.\n\n"
        "`greet(\"Ada\")` returns `'Hello, Ada!'`. Use an f-string, not `+` and not "
        "`.format()`."
    ),
    hint=(
        "An f-string is an ordinary string literal with an `f` before the opening "
        "quote. Anything inside `{}` is evaluated as an expression."
    ),
    solution='def greet(name):\n    return f"Hello, {name}!"',
    explanation=(
        "An f-string calls `str()` on whatever each `{}` holds, so it never raises the "
        "`TypeError` that `\"Hello, \" + 42` would. The `f` prefix is compiled, not "
        "interpreted at runtime — which is why a plain `\"{name}\"` with no `f` stays "
        "literal braces, and is the most common typo in this whole topic."
    ),
    starter="def greet(name):\n    ...",
    cases=[
        Case(expected="Hello, Ada!", args=("Ada",)),
        Case(expected="Hello, !", args=("",)),
        Case(expected="Hello, Ada Lovelace!", args=("Ada Lovelace",)),
        Case(expected="Hello, 世界!", args=("世界",)),
    ],
)

q(
    qid="Q-043",
    level=Level.L1,
    topic="F-strings",
    kind="function",
    entry="money",
    prompt=(
        "Write `money(amount)` that formats a number as a dollar amount with exactly "
        "two decimal places.\n\n"
        "`money(12.5)` returns `'$12.50'` and `money(0)` returns `'$0.00'`. No "
        "thousands separators. Use a format spec inside the f-string — do not call "
        "`round()`."
    ),
    hint=(
        "Inside the braces you can put a colon and then a format spec. The one you "
        "want fixes the number of digits after the point and is written `.Nf`."
    ),
    solution='def money(amount):\n    return f"${amount:.2f}"',
    explanation=(
        "`:.2f` both rounds *and* pads, which `round()` alone cannot do — "
        "`round(12.5, 2)` is `12.5` and prints without the trailing zero, so money "
        "columns come out ragged. Formatting is presentation: keep the full-precision "
        "number in your data and apply the spec only at the moment you display it."
    ),
    starter="def money(amount):\n    ...",
    cases=[
        Case(expected="$12.50", args=(12.5,)),
        Case(expected="$0.00", args=(0,)),
        Case(expected="$1234.57", args=(1234.567,)),
        Case(expected="$10.00", args=(9.999,)),
    ],
)

q(
    qid="Q-044",
    level=Level.L1,
    topic="Methods",
    kind="function",
    entry="normalize",
    prompt=(
        "Write `normalize(text)` that returns `text` with surrounding whitespace "
        "removed and every letter lowercased.\n\n"
        "`normalize(\"  Hello World \\n\")` returns `'hello world'`. Inner spaces are "
        "left alone."
    ),
    hint=(
        "Two methods, one after the other. They both return a new string, so the "
        "second one can be called straight onto the result of the first."
    ),
    solution="def normalize(text):\n    return text.strip().lower()",
    explanation=(
        "Chaining works because every string method returns a brand-new string rather "
        "than editing in place — `text.strip()` on its own line and thrown away is the "
        "classic beginner bug. Bare `.strip()` removes all whitespace, tabs and "
        "newlines included, which is exactly what you want for scrubbing input."
    ),
    starter="def normalize(text):\n    ...",
    cases=[
        Case(expected="hello world", args=("  Hello World \n",)),
        Case(expected="", args=("",)),
        Case(expected="", args=("   ",)),
        Case(expected="école", args=("ÉCOLE",)),
    ],
)

q(
    qid="Q-045",
    level=Level.L1,
    topic="Methods",
    kind="function",
    entry="words",
    prompt=(
        "Write `words(sentence)` that returns a **list of strings** — the whitespace-"
        "separated words of `sentence`, with no empty entries.\n\n"
        "Runs of several spaces count as one separator, and a blank sentence gives "
        "`[]`."
    ),
    hint=(
        "The splitting method takes an optional separator. Calling it with **no** "
        "argument switches on a different, smarter mode — that is the one you want."
    ),
    solution="def words(sentence):\n    return sentence.split()",
    explanation=(
        "`split()` with no argument treats any run of whitespace as a single "
        "separator and discards leading and trailing runs, so `\"  a  b \".split()` is "
        "`['a', 'b']`. `split(\" \")` is a completely different function: it splits on "
        "each individual space and happily produces empty strings — Q-061 shows that "
        "side by side."
    ),
    starter="def words(sentence):\n    ...",
    cases=[
        Case(expected=["the", "quick", "brown"], args=("the quick  brown",)),
        Case(expected=[], args=("",)),
        Case(expected=[], args=("   ",)),
        Case(expected=["one"], args=("one",)),
        Case(expected=["pad", "me"], args=("  pad  me  ",)),
    ],
)

q(
    qid="Q-046",
    level=Level.L1,
    topic="Methods",
    kind="function",
    entry="join_words",
    prompt=(
        "Write `join_words(words)` that glues a list of strings into one string, "
        "separated by a comma and a space.\n\n"
        "`join_words([\"a\", \"b\", \"c\"])` returns `'a, b, c'` — note there is no "
        "trailing comma, and an empty list gives `''`."
    ),
    hint=(
        "The method lives on the **separator**, not on the list. Read that sentence "
        "twice — the call reads backwards compared to most other languages."
    ),
    solution='def join_words(words):\n    return ", ".join(words)',
    explanation=(
        "`sep.join(parts)` looks inside out until you see why: `join` has to work for "
        "any iterable of strings, so it belongs to the one object that is always a "
        "string — the separator. It only accepts strings, so `\", \".join([1, 2])` "
        "raises `TypeError`; map with `str` first."
    ),
    starter="def join_words(words):\n    ...",
    cases=[
        Case(expected="a, b, c", args=(["a", "b", "c"],)),
        Case(expected="", args=([],)),
        Case(expected="solo", args=(["solo"],)),
        Case(expected="a, ", args=(["a", ""],)),
    ],
)

q(
    qid="Q-047",
    level=Level.L1,
    topic="Methods",
    kind="function",
    entry="substitute",
    prompt=(
        "Write `substitute(text, old, new)` that returns `text` with **every** "
        "occurrence of the substring `old` swapped for `new`.\n\n"
        "If `old` does not occur, return `text` unchanged. `new` may be `''`, which "
        "deletes the matches."
    ),
    hint=(
        "One method does all of this, replacing every occurrence by default. The "
        "result is a new string — make sure you return it rather than the original."
    ),
    solution="def substitute(text, old, new):\n    return text.replace(old, new)",
    explanation=(
        "`replace` substitutes *all* occurrences unless you pass a count as a third "
        "argument, and it returns a new string — `text.replace(...)` on a line by "
        "itself does nothing at all, which is the single most reported 'replace is "
        "broken' bug. A substring that is absent is not an error; you simply get the "
        "original back."
    ),
    starter="def substitute(text, old, new):\n    ...",
    cases=[
        Case(expected="bonono", args=("banana", "a", "o")),
        Case(expected="ba", args=("banana", "na", "")),
        Case(expected="abc", args=("abc", "z", "y")),
        Case(expected="", args=("", "a", "b")),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-048",
    level=Level.L2,
    topic="Slicing",
    kind="function",
    entry="every_other",
    prompt=(
        "Write `every_other(text)` that returns a string made of the characters at "
        "positions `0, 2, 4, ...` of `text`.\n\n"
        "`every_other(\"abcdef\")` returns `'ace'`. Use one slice, no loop."
    ),
    hint=(
        "The third number in a slice is the *step* — how far to jump each time. "
        "Leaving the first two out keeps the full range."
    ),
    solution="def every_other(text):\n    return text[::2]",
    explanation=(
        "A slice is `start:stop:step`, and the step defaults to `1`. `text[::2]` takes "
        "every second character starting at the front, whatever the length — the odd-"
        "length case needs no special handling because the slice simply runs out. "
        "`text[1::2]` gets the other half."
    ),
    starter="def every_other(text):\n    ...",
    cases=[
        Case(expected="ace", args=("abcdef",)),
        Case(expected="ace", args=("abcde",)),
        Case(expected="", args=("",)),
        Case(expected="a", args=("a",)),
        Case(expected="hlowrd", args=("hello world",)),
    ],
)

q(
    qid="Q-049",
    level=Level.L2,
    topic="Slicing",
    kind="function",
    entry="clip",
    prompt=(
        "Write `clip(text, width)` that shortens `text` to at most `width` characters "
        "for display.\n\n"
        "If `text` already fits, return it unchanged. Otherwise cut it short and end "
        "it with `...`, so that the **result** — ellipsis included — is exactly "
        "`width` characters long. `clip(\"hello world\", 8)` returns `'hello...'`.\n\n"
        "`width` is always at least `4`."
    ),
    hint=(
        "The three dots are part of the budget, not an addition to it. Work out how "
        "many real characters you are allowed to keep before you write the slice."
    ),
    solution=(
        "def clip(text, width):\n"
        "    if len(text) <= width:\n"
        "        return text\n"
        '    return text[:width - 3] + "..."'
    ),
    explanation=(
        "The off-by-three here is the whole exercise: an ellipsis appended to "
        "`text[:width]` gives a string of `width + 3`, which is how truncated table "
        "columns end up one cell wider than the header. Note `<=` rather than `<` — a "
        "string of exactly `width` fits and must not be mangled."
    ),
    starter="def clip(text, width):\n    ...",
    cases=[
        Case(expected="hello", args=("hello", 10)),
        Case(expected="hello...", args=("hello world", 8)),
        Case(expected="abcd", args=("abcd", 4)),
        Case(expected="a...", args=("abcde", 4)),
        Case(expected="", args=("", 5)),
    ],
)

q(
    qid="Q-050",
    level=Level.L2,
    topic="Indexing",
    kind="function",
    entry="char_at",
    prompt=(
        "Write `char_at(text, i, default=None)` that returns the character at "
        "position `i`, or `default` when `i` is out of range.\n\n"
        "Negative positions are legitimate and must work: `char_at(\"abc\", -1)` is "
        "`'c'`. Only genuinely out-of-range positions fall back to `default`."
    ),
    hint=(
        "Do not try to write the bounds test yourself — the `-3 <= i < 3` version is "
        "easy to get subtly wrong. Let the indexing attempt fail and catch the one "
        "exception it raises."
    ),
    solution=(
        "def char_at(text, i, default=None):\n"
        "    try:\n"
        "        return text[i]\n"
        "    except IndexError:\n"
        "        return default"
    ),
    explanation=(
        "Indexing raises `IndexError` — unlike slicing, which clamps silently — and "
        "catching it is both shorter and more correct than a hand-written bounds check "
        "that has to cover the negative range as well. This is the *easier to ask "
        "forgiveness than permission* style Python leans on; keep the `try` block down "
        "to the one operation that can fail."
    ),
    starter="def char_at(text, i, default=None):\n    ...",
    cases=[
        Case(expected="a", args=("abc", 0)),
        Case(expected="c", args=("abc", -1)),
        Case(expected=None, args=("abc", 5)),
        Case(expected=None, args=("abc", -5)),
        Case(expected="c", args=("abc", 2, "?")),
        Case(expected="?", args=("", 0, "?")),
    ],
)

q(
    qid="Q-051",
    level=Level.L2,
    topic="Immutability",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        's = "hello"\n'
        "s.upper()\n"
        "print(s)\n"
        "print(s.upper())\n"
        't = s.replace("l", "L")\n'
        "print(s, t)\n"
        "```\n\n"
        "Set `answer` to the three printed lines, e.g. "
        "`answer = \"a\\nb\\nc d\"`."
    ),
    hint=(
        "Ask what `s.upper()` on a line of its own actually changes. Strings cannot be "
        "modified at all — so where does the uppercase version go?"
    ),
    solution='answer = "hello\\nHELLO\\nhello heLLo"',
    explanation=(
        "Strings are immutable: no method can alter one, so every 'modifying' method "
        "returns a *new* string and leaves the original untouched. A bare "
        "`s.upper()` therefore computes a value and throws it away — the statement is "
        "legal, does nothing, and produces no warning, which is why it survives code "
        "review. Assign the result or pass it on."
    ),
    starter="answer = ...",
    cases=[Case(expected="hello\nHELLO\nhello heLLo")],
)

q(
    qid="Q-052",
    level=Level.L2,
    topic="F-strings",
    kind="function",
    entry="stat_line",
    prompt=(
        "Write `stat_line(label, count)` that returns one row of a report: `label` "
        "left-aligned in a 10-character field, then `count` right-aligned in a "
        "12-character field with thousands separators.\n\n"
        "`stat_line(\"widgets\", 1234567)` returns `'widgets      1,234,567'`. A label "
        "longer than 10 characters is **not** truncated — the field is a minimum, not "
        "a maximum."
    ),
    hint=(
        "Two format specs, one per field. Alignment is a single character (`<`, `>`, "
        "`^`) placed before the width; the grouping option is one more character after "
        "it."
    ),
    solution='def stat_line(label, count):\n    return f"{label:<10}{count:>12,}"',
    explanation=(
        "A width in a format spec is a *minimum*: it pads short values and leaves long "
        "ones intact, so columns can only ever get wider, never lose data. The `,` "
        "option inserts thousands separators and works on ints and floats alike, which "
        "saves hand-rolling the digit grouping that trips everyone up on negatives."
    ),
    starter="def stat_line(label, count):\n    ...",
    cases=[
        Case(expected="widgets      1,234,567", args=("widgets", 1234567)),
        Case(expected="a                    0", args=("a", 0)),
        Case(expected="verylonglabelhere           5", args=("verylonglabelhere", 5)),
        Case(expected="x               -1,000", args=("x", -1000)),
    ],
)

q(
    qid="Q-053",
    level=Level.L2,
    topic="F-strings",
    kind="function",
    entry="percent",
    prompt=(
        "Write `percent(part, whole)` that returns the share of `whole` taken by "
        "`part`, as a string with one decimal place and a trailing `%`.\n\n"
        "`percent(1, 4)` returns `'25.0%'`. Do **not** multiply by 100 yourself — the "
        "format spec does it. When `whole` is `0`, raise `ValueError`."
    ),
    hint=(
        "There is a presentation type that both scales by 100 and appends the sign. It "
        "is written where you would otherwise put `f`."
    ),
    solution=(
        "def percent(part, whole):\n"
        "    if whole == 0:\n"
        '        raise ValueError("whole must not be zero")\n'
        '    return f"{part / whole:.1%}"'
    ),
    explanation=(
        "`:.1%` multiplies by 100, rounds to one decimal and adds the `%` in one step, "
        "so a ratio stays a ratio right up to the moment it is shown — multiplying "
        "early is how `0.1 * 100` sneaks `10.000000000000002` into a report. The zero "
        "guard is the real design decision: `ZeroDivisionError` would leak the "
        "implementation, while `ValueError` names the caller's mistake."
    ),
    starter="def percent(part, whole):\n    ...",
    cases=[
        Case(expected="25.0%", args=(1, 4)),
        Case(expected="33.3%", args=(1, 3)),
        Case(expected="0.0%", args=(0, 5)),
        Case(expected="100.0%", args=(5, 5)),
        Case(expected=None, args=(1, 0), raises=ValueError),
    ],
)

q(
    qid="Q-054",
    level=Level.L2,
    topic="Methods",
    kind="function",
    entry="check_ends",
    prompt=(
        "Write `check_ends(text, prefix, suffix)` returning the tuple "
        "`(starts_with_prefix, ends_with_suffix)`.\n\n"
        "Both elements must be real `bool` values — the checker will not accept `1` "
        "for `True`."
    ),
    hint=(
        "Two methods named exactly after what they test. Neither needs slicing, and "
        "neither needs `len`."
    ),
    solution=(
        "def check_ends(text, prefix, suffix):\n"
        "    return (text.startswith(prefix), text.endswith(suffix))"
    ),
    explanation=(
        "`startswith`/`endswith` already return `bool`, so wrapping them in "
        "`bool(...)` or an `if` adds nothing. They beat the slice form "
        "`text[-len(suffix):] == suffix` because an empty suffix makes that slice "
        "`text[0:]` — the whole string — and silently gives the wrong answer. Both "
        "also accept a *tuple* of candidates, which is the tidy way to test several "
        "extensions at once."
    ),
    starter="def check_ends(text, prefix, suffix):\n    ...",
    cases=[
        Case(expected=(True, True), args=("report.csv", "report", ".csv")),
        Case(expected=(False, True), args=("report.csv", "data", ".csv")),
        Case(expected=(True, True), args=("", "", "")),
        Case(expected=(False, True), args=("a.txt", ".txt", ".txt")),
    ],
)

q(
    qid="Q-055",
    level=Level.L2,
    topic="Methods",
    kind="function",
    entry="locate",
    prompt=(
        "Write `locate(text, sub)` that returns the index where `sub` first appears "
        "in `text`, or `-1` when it does not appear at all.\n\n"
        "It must never raise, for any pair of strings."
    ),
    hint=(
        "There are two search methods with almost the same name. One signals failure "
        "by raising; you want the one that signals it with a sentinel value."
    ),
    solution="def locate(text, sub):\n    return text.find(sub)",
    explanation=(
        "`find` returns `-1` when there is no match while `index` raises `ValueError` "
        "— pick by whether 'absent' is normal or exceptional in your code. The `-1` is "
        "a trap in a truthiness test, because `-1` is truthy and `0` (a match at the "
        "very front!) is falsy, so always compare with `!= -1` explicitly. An empty "
        "`sub` is found at position `0`, since every string contains it."
    ),
    starter="def locate(text, sub):\n    ...",
    cases=[
        Case(expected=2, args=("hello", "l")),
        Case(expected=-1, args=("hello", "z")),
        Case(expected=0, args=("hello", "")),
        Case(expected=0, args=("hello", "hello")),
        Case(expected=2, args=("banana", "na")),
    ],
)

q(
    qid="Q-056",
    level=Level.L2,
    topic="Methods",
    kind="function",
    entry="count_sub",
    prompt=(
        "Write `count_sub(text, sub)` that returns how many times `sub` occurs in "
        "`text`, as an `int`.\n\n"
        "Two of the cases are the interesting ones: work out what `count_sub"
        "(\"aaaa\", \"aa\")` and `count_sub(\"abc\", \"\")` should be before you check."
    ),
    hint=(
        "A single method does the counting. The surprises come from how it advances "
        "after each match, and from what it considers a match of the empty string."
    ),
    solution="def count_sub(text, sub):\n    return text.count(sub)",
    explanation=(
        "`count` finds **non-overlapping** occurrences: after a match it resumes past "
        "the end of that match, so `\"aaaa\".count(\"aa\")` is `2`, not `3`. Counting "
        "the empty string returns `len(text) + 1`, because it is considered to sit in "
        "every gap including the ones before the first and after the last character — "
        "worth knowing before a user-supplied search term reaches this call."
    ),
    starter="def count_sub(text, sub):\n    ...",
    cases=[
        Case(expected=3, args=("banana", "a")),
        Case(expected=2, args=("aaaa", "aa")),
        Case(expected=0, args=("banana", "x")),
        Case(expected=4, args=("abc", "")),
    ],
)

q(
    qid="Q-057",
    level=Level.L2,
    topic="Methods",
    kind="function",
    entry="pad_id",
    prompt=(
        "Write `pad_id(number, width)` that renders an integer as a string padded on "
        "the left with zeros to at least `width` characters.\n\n"
        "`pad_id(7, 3)` returns `'007'`. A number that is already too long is returned "
        "in full. Use the dedicated string method, not an f-string."
    ),
    hint=(
        "The method is named after what it fills with. It lives on `str`, so the "
        "number has to become one first."
    ),
    solution="def pad_id(number, width):\n    return str(number).zfill(width)",
    explanation=(
        "`zfill` is sign-aware in a way that neither `rjust(width, \"0\")` nor a naive "
        "`\"0\" * n + s` is: it keeps a leading `-` or `+` at the front and pads after "
        "it, so `str(-7).zfill(4)` is `'-007'` and not `'00-7'`. The f-string "
        "equivalent is `f\"{number:0{width}d}\"`, which behaves the same and is what "
        "you would reach for inside a larger template."
    ),
    starter="def pad_id(number, width):\n    ...",
    cases=[
        Case(expected="007", args=(7, 3)),
        Case(expected="1234", args=(1234, 3)),
        Case(expected="0000", args=(0, 4)),
        Case(expected="-007", args=(-7, 4)),
    ],
)

q(
    qid="Q-058",
    level=Level.L2,
    topic="Methods",
    kind="function",
    entry="split_setting",
    prompt=(
        "Write `split_setting(line)` that parses one `key = value` configuration line "
        "into the tuple `(key, value)`, with surrounding whitespace stripped from "
        "both.\n\n"
        "Split on the **first** `=` only, so `'url=http://a=b'` gives "
        "`('url', 'http://a=b')`. A line with no `=` at all gives "
        "`(line_stripped, '')`.\n\n"
        "Use `str.partition`, which always returns a 3-tuple and so needs no length "
        "check."
    ),
    hint=(
        "`partition` hands back `(before, separator, after)`. When the separator is "
        "missing, look at what the second and third elements become — that is what "
        "makes the no-`=` case fall out for free."
    ),
    solution=(
        "def split_setting(line):\n"
        '    key, sep, value = line.partition("=")\n'
        "    return (key.strip(), value.strip())"
    ),
    explanation=(
        "`partition` splits once and *always* returns three items, so unpacking it can "
        "never raise — on a miss you get `(whole_string, '', '')`, which is exactly "
        "the fallback the prompt asks for. `split(\"=\")` would need a length check "
        "and would shatter a value that legitimately contains `=`; `split(\"=\", 1)` "
        "is closer but still returns a list of one or two items you must measure."
    ),
    starter="def split_setting(line):\n    ...",
    cases=[
        Case(expected=("name", "Ada"), args=("name = Ada",)),
        Case(expected=("debug", "true"), args=("debug=true",)),
        Case(expected=("novalue", ""), args=("novalue",)),
        Case(expected=("k", ""), args=("k=",)),
        Case(expected=("url", "http://a=b"), args=("url=http://a=b",)),
        Case(expected=("", "v"), args=("=v",)),
    ],
)

q(
    qid="Q-059",
    level=Level.L2,
    topic="Immutability",
    kind="custom",
    entry="stack_lines",
    constraints=["no-loops"],
    prompt=(
        "Here is working but wasteful code:\n\n"
        "```python\n"
        "def stack_lines(lines):\n"
        '    out = ""\n'
        "    for line in lines:\n"
        "        if out:\n"
        '            out = out + "\\n"\n'
        "        out = out + line\n"
        "    return out\n"
        "```\n\n"
        "Rewrite it as a single `return`, with no loop at all. Same behaviour: the "
        "lines separated by newlines, no trailing newline, `''` for an empty list."
    ),
    hint=(
        "Because strings cannot be modified, `out + line` builds a whole new string "
        "every pass. One method takes the entire sequence at once and allocates only "
        "the final result."
    ),
    solution='def stack_lines(lines):\n    return "\\n".join(lines)',
    explanation=(
        "Repeated `+=` on a string is quadratic: each pass copies everything "
        "accumulated so far, so a 10,000-line file does ~50 million character copies. "
        "`join` walks the sequence once to total the length, allocates exactly one "
        "buffer and fills it. It also removes the separator bookkeeping entirely — the "
        "`if out:` guard existed only to suppress a leading newline."
    ),
    starter="def stack_lines(lines):\n    ...",
    cases=[
        Case(expected="a\nb", args=(["a", "b"],)),
        Case(expected="", args=([],)),
        Case(expected="only", args=(["only"],)),
        Case(expected="a\n\nb", args=(["a", "", "b"],)),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-060",
    level=Level.L3,
    topic="Slicing",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'text = "abcdef"\n'
        "print(text[::-1])\n"
        "print(text[5:1:-1])\n"
        "print(repr(text[1:5:-1]))\n"
        "print(repr(text[10:20]))\n"
        "```\n\n"
        "Set `answer` to the four printed lines. The last two use `repr` so you can "
        "see what they really are — write them with the quotes included."
    ),
    hint=(
        "With a negative step the slice walks from `start` *down* towards `stop`. Ask "
        "what happens when `start` is already below `stop` — and, separately, whether "
        "a slice is allowed to run off the end."
    ),
    solution="answer = \"fedcba\\nfedc\\n''\\n''\"",
    explanation=(
        "A negative step reverses the direction of travel but not the exclusivity of "
        "`stop`, so `text[5:1:-1]` collects indices 5, 4, 3, 2 and stops before 1. "
        "When the range is empty in the direction you asked for, you get `''` rather "
        "than an error — and the same forgiveness applies to `text[10:20]` on a "
        "6-character string. That silence is the danger: an out-of-range slice hands "
        "you an empty string that then flows downstream as if it were real data."
    ),
    starter="answer = ...",
    cases=[Case(expected="fedcba\nfedc\n''\n''")],
)

q(
    qid="Q-061",
    level=Level.L3,
    topic="Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'print("xxhixx".strip("x"))\n'
        'print(repr("banana".strip("ban")))\n'
        'print("a  b".split())\n'
        'print("a  b".split(" "))\n'
        "```\n\n"
        "Set `answer` to the four printed lines. Lines 3 and 4 print lists — copy "
        "Python's own formatting, spaces and quotes included."
    ),
    hint=(
        "`strip` takes a *set of characters*, not a prefix. And calling `split` with "
        "an explicit separator switches off the whitespace-run behaviour you get from "
        "calling it bare."
    ),
    solution='answer = "hi\\n\'\'\\n[\'a\', \'b\']\\n[\'a\', \'\', \'b\']"',
    explanation=(
        "`strip(\"ban\")` removes any of `b`, `a` or `n` from both ends until it meets "
        "something else — `\"banana\"` is made of nothing but those three letters, so "
        "the whole string disappears. That is why stripping a file extension with "
        "`name.strip(\".csv\")` eventually eats a filename ending in `s`; use "
        "`removesuffix`. Bare `split()` collapses whitespace runs and drops empties, "
        "while `split(\" \")` splits on every single space and keeps the gap between "
        "two of them as `''`."
    ),
    starter="answer = ...",
    cases=[Case(expected="hi\n''\n['a', 'b']\n['a', '', 'b']")],
)

q(
    qid="Q-062",
    level=Level.L3,
    topic="Methods",
    kind="function",
    entry="trim_suffix",
    prompt=(
        "Write `trim_suffix(text, suffix)` that removes `suffix` from the end of "
        "`text` when it is there, and returns `text` unchanged when it is not.\n\n"
        "`trim_suffix(\"report.csv\", \".csv\")` is `'report'`; "
        "`trim_suffix(\"report.csv\", \".txt\")` is `'report.csv'`. An empty `suffix` "
        "removes nothing.\n\n"
        "Build it from a test and a slice. Do not use `rstrip`, and do not use "
        "`removesuffix` — the point is to see why the first is wrong and what the "
        "second has to do internally."
    ),
    hint=(
        "Test first, then cut. The empty-suffix case needs its own guard: think about "
        "what `text[:-0]` slices to before you decide you do not need it."
    ),
    solution=(
        "def trim_suffix(text, suffix):\n"
        "    if suffix and text.endswith(suffix):\n"
        "        return text[:-len(suffix)]\n"
        "    return text"
    ),
    explanation=(
        "`-0` is just `0`, so `text[:-len(suffix)]` with an empty suffix becomes "
        "`text[:0]` — the empty string — and silently destroys the input. That single "
        "edge case is the reason Python 3.9 added `removesuffix` as a builtin method. "
        "`rstrip(suffix)` is a different bug entirely: it strips *characters*, so "
        "`\"mississippi.csv\".rstrip(\".csv\")` leaves `'mississippi'` minus its "
        "trailing letters."
    ),
    starter="def trim_suffix(text, suffix):\n    ...",
    cases=[
        Case(expected="report", args=("report.csv", ".csv")),
        Case(expected="report.csv", args=("report.csv", ".txt")),
        Case(expected="bana", args=("banana", "na")),
        Case(expected="data", args=("data", "")),
        Case(expected="csv", args=("csv", ".csv")),
        Case(expected="", args=("aaa", "aaa")),
    ],
)

q(
    qid="Q-063",
    level=Level.L3,
    topic="Slicing",
    kind="function",
    entry="rotate",
    prompt=(
        "Write `rotate(text, n)` that rotates `text` to the **left** by `n` places, "
        "wrapping characters round from the front to the back.\n\n"
        "`rotate(\"abcdef\", 2)` is `'cdefab'`. `n` may be negative (rotate right), "
        "zero, or larger than the string — all of them wrap. An empty string returns "
        "`''`.\n\n"
        "No loop, and no `if` for the sign."
    ),
    hint=(
        "Two slices concatenated do the rotation itself. Everything else is making "
        "`n` land inside `0..len(text)-1` first — one operator does that for negatives "
        "and oversized values alike."
    ),
    solution=(
        "def rotate(text, n):\n"
        "    if not text:\n"
        "        return text\n"
        "    n %= len(text)\n"
        "    return text[n:] + text[:n]"
    ),
    explanation=(
        "`%` with a positive divisor always lands in `[0, len)`, so it normalises "
        "oversized and negative rotations in one step — no sign branch needed. The "
        "empty-string guard is not optional: `n % 0` raises `ZeroDivisionError`, which "
        "is the one input the modulo trick cannot absorb."
    ),
    starter="def rotate(text, n):\n    ...",
    cases=[
        Case(expected="cdefab", args=("abcdef", 2)),
        Case(expected="fabcde", args=("abcdef", -1)),
        Case(expected="abcdef", args=("abcdef", 0)),
        Case(expected="cdefab", args=("abcdef", 8)),
        Case(expected="", args=("", 3)),
        Case(expected="a", args=("a", 5)),
    ],
)

q(
    qid="Q-064",
    level=Level.L3,
    topic="F-strings",
    kind="function",
    entry="table_row",
    prompt=(
        "Write `table_row(name, qty, price)` that returns one fixed-width row of a "
        "table:\n\n"
        "- `name` left-aligned in 12 characters,\n"
        "- `qty` right-aligned in 4 characters,\n"
        "- `price` right-aligned in 10 characters with exactly 2 decimals.\n\n"
        "No separators between the fields, and no trailing spaces beyond the padding "
        "itself. `table_row(\"apple\", 3, 1.5)` returns "
        "`'apple          3      1.50'`."
    ),
    hint=(
        "One f-string, three fields. In a spec the order is fill, align, width, then "
        "precision and type — so a right-aligned two-decimal number in ten columns is "
        "written as one run of characters after the colon."
    ),
    solution=(
        "def table_row(name, qty, price):\n"
        '    return f"{name:<12}{qty:>4}{price:>10.2f}"'
    ),
    explanation=(
        "Width and precision are independent: `10.2f` means 'at least ten columns "
        "wide, exactly two digits after the point', so the decimal points line up down "
        "the column whatever the magnitude. Defaults differ by type — numbers "
        "right-align and strings left-align — so spelling the alignment out is what "
        "keeps a column stable when a value type changes."
    ),
    starter="def table_row(name, qty, price):\n    ...",
    cases=[
        Case(expected="apple          3      1.50", args=("apple", 3, 1.5)),
        Case(expected="dragonfruit!!  12      0.50", args=("dragonfruit!!", 12, 0.5)),
        Case(expected="x              0   1234.57", args=("x", 0, 1234.567)),
        Case(expected="kiwi         100     -2.00", args=("kiwi", 100, -2.0)),
    ],
)

q(
    qid="Q-065",
    level=Level.L3,
    topic="Methods",
    kind="function",
    entry="slugify",
    prompt=(
        "Write `slugify(text)` that turns a title into a URL slug: all lowercase, "
        "words joined by single hyphens.\n\n"
        "`slugify(\"  Mixed   CASE  text \")` returns `'mixed-case-text'`. Any run of "
        "whitespace is one separator, and there is never a leading or trailing hyphen. "
        "A blank input returns `''`."
    ),
    hint=(
        "Three steps, and none of them is a loop or a `replace`. Getting the "
        "whitespace right is free if you pick the right splitting call — see Q-045."
    ),
    solution='def slugify(text):\n    return "-".join(text.lower().split())',
    explanation=(
        "`split()` then `join` is the standard whitespace-normalising idiom, and it "
        "beats `text.replace(\" \", \"-\")` on every messy input: replace turns a "
        "double space into `--` and leaves a leading space as a leading hyphen. "
        "Because `split()` returns `[]` for a blank string, `join` gives `''` and the "
        "empty case needs no branch."
    ),
    starter="def slugify(text):\n    ...",
    cases=[
        Case(expected="hello-world", args=("Hello World",)),
        Case(expected="mixed-case-text", args=("  Mixed   CASE  text ",)),
        Case(expected="", args=("",)),
        Case(expected="one", args=("one",)),
        Case(expected="", args=("   ",)),
    ],
)

q(
    qid="Q-066",
    level=Level.L3,
    topic="Indexing",
    kind="function",
    entry="span",
    prompt=(
        "Write `span(text, sub)` that returns the tuple `(first_index, last_index)` — "
        "where `sub` first starts and where it last starts inside `text`.\n\n"
        "When `sub` occurs only once both numbers are the same. When `sub` does not "
        "occur at all, the function must raise `ValueError` — do not return `-1`, and "
        "do not raise it yourself.\n\n"
        "`span(\"banana\", \"a\")` returns `(1, 5)`."
    ),
    hint=(
        "A matched pair of methods searches from each end, and both already raise the "
        "exception the prompt wants. The counterparts that return `-1` are the ones to "
        "avoid here."
    ),
    solution="def span(text, sub):\n    return (text.index(sub), text.rindex(sub))",
    explanation=(
        "`index`/`rindex` raise `ValueError` on a miss while `find`/`rfind` return "
        "`-1`; choosing between the pairs is choosing whether 'not present' is a bug "
        "or a normal outcome. Letting the exception propagate is the implementation "
        "here — a `try` that re-raises the same error would add lines and lose the "
        "original message. Note `rindex` reports where the *last* match begins, not "
        "where it ends."
    ),
    starter="def span(text, sub):\n    ...",
    cases=[
        Case(expected=(1, 5), args=("banana", "a")),
        Case(expected=(2, 4), args=("banana", "na")),
        Case(expected=(0, 0), args=("abc", "abc")),
        Case(expected=(0, 3), args=("abc", "")),
        Case(expected=None, args=("abc", "z"), raises=ValueError),
        Case(expected=None, args=("", "a"), raises=ValueError),
    ],
)

q(
    qid="Q-067",
    level=Level.L3,
    topic="Methods",
    kind="custom",
    entry="initials",
    constraints=["needs-comprehension", "max-lines:2"],
    prompt=(
        "Here is working but unidiomatic code:\n\n"
        "```python\n"
        "def initials(full_name):\n"
        '    result = ""\n'
        "    parts = full_name.split()\n"
        "    for i in range(len(parts)):\n"
        '        result = result + parts[i][0].upper() + "."\n'
        "    return result\n"
        "```\n\n"
        "Rewrite it as a body of at most 2 lines using a comprehension and a join. "
        "Same behaviour: `initials(\"ada lovelace\")` is `'A.L.'`, and an empty or "
        "blank name gives `''`."
    ),
    hint=(
        "`range(len(parts))` exists only to index back into `parts` — iterate the list "
        "itself instead. Then remember that repeated `+` on a string reallocates every "
        "pass (Q-059)."
    ),
    solution=(
        "def initials(full_name):\n"
        '    return "".join([part[0].upper() + "." for part in full_name.split()])'
    ),
    explanation=(
        "`for i in range(len(seq))` is the clearest signal in a Python diff that "
        "someone is writing C: the index is never used for anything but `seq[i]`, so "
        "iterating the sequence directly is shorter and cannot go out of bounds. "
        "Pairing a comprehension with `join` also fixes the quadratic string building — "
        "the comprehension produces the pieces, `join` allocates the result once."
    ),
    starter="def initials(full_name):\n    ...",
    cases=[
        Case(expected="A.L.", args=("ada lovelace",)),
        Case(expected="G.B.M.H.", args=("grace brewster murray hopper",)),
        Case(expected="", args=("",)),
        Case(expected="P.", args=("plato",)),
        Case(expected="J.L.", args=("  jean   luc  ",)),
    ],
)

q(
    qid="Q-068",
    level=Level.L3,
    topic="Immutability",
    kind="function",
    entry="caesar",
    prompt=(
        "Write `caesar(text, shift)` that shifts every **lowercase ASCII letter** "
        "forward by `shift` places in the alphabet, wrapping `z` round to `a`. Every "
        "other character — spaces, digits, punctuation, uppercase — passes through "
        "untouched.\n\n"
        "`caesar(\"xyz\", 3)` is `'abc'`. `shift` may be `0` or negative. Return a "
        "string.\n\n"
        "Build the result by collecting the characters and joining once at the end, "
        "not by `+=` in the loop."
    ),
    hint=(
        "`ord(ch)` gives a character's code point and `chr(n)` turns one back. Subtract "
        "`ord(\"a\")` first so you are working in `0..25`, where `% 26` does the "
        "wrapping for you."
    ),
    solution=(
        "def caesar(text, shift):\n"
        "    out = []\n"
        "    for ch in text:\n"
        '        if "a" <= ch <= "z":\n'
        '            out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))\n'
        "        else:\n"
        "            out.append(ch)\n"
        '    return "".join(out)'
    ),
    explanation=(
        "Shifting in code-point space only works once you move into a zero-based "
        "alphabet — `(ord(ch) + shift) % 26` would land in the control characters. "
        "Because `%` follows the sign of its divisor, a negative `shift` wraps "
        "correctly with no extra branch. The list-then-join shape is the standard "
        "answer to immutability: a list *can* grow in place, so you pay one allocation "
        "at the end instead of one per character."
    ),
    starter="def caesar(text, shift):\n    ...",
    cases=[
        Case(expected="bcd", args=("abc", 1)),
        Case(expected="abc", args=("xyz", 3)),
        Case(expected="uryyb, jbeyq!", args=("hello, world!", 13)),
        Case(expected="abc", args=("abc", 0)),
        Case(expected="zab", args=("abc", -1)),
        Case(expected="", args=("", 5)),
    ],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-069",
    level=Level.L4,
    topic="Immutability",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output on CPython:\n\n"
        "```python\n"
        'a = "hello"\n'
        'b = "hello"\n'
        "print(a is b)\n\n"
        'c = "hel" + "lo"\n'
        "print(a is c)\n\n"
        'd = "".join(["hel", "lo"])\n'
        "print(a is d)\n"
        "print(a == d)\n"
        "```\n\n"
        "Set `answer` to the four printed lines."
    ),
    hint=(
        "Two of these strings are built while the module is being *compiled*, and one "
        "is built while it runs. Ask which of those the interpreter is able to fold "
        "into a single constant and reuse."
    ),
    solution='answer = "True\\nTrue\\nFalse\\nTrue"',
    explanation=(
        "CPython interns identifier-like string literals, so `a` and `b` are the same "
        "object; `\"hel\" + \"lo\"` is folded into that same constant at compile time, "
        "so `c` is too. `join` runs at runtime and must allocate a fresh string, so "
        "`a is d` is `False` even though the characters match. All of this is an "
        "*implementation detail* — the lesson is that `is` on strings answers a "
        "question about object identity that your program almost never means to ask. "
        "Compare strings with `==`; reserve `is` for `None` and sentinels."
    ),
    starter="answer = ...",
    cases=[Case(expected="True\nTrue\nFalse\nTrue")],
)

q(
    qid="Q-070",
    level=Level.L4,
    topic="F-strings",
    kind="function",
    entry="fmt_cell",
    prompt=(
        "Write `fmt_cell(value, width, align=\">\", fill=\" \")` that formats `value` "
        "into a field of `width` characters, where the alignment character and the "
        "padding character are both **decided at runtime**.\n\n"
        "`fmt_cell(\"ab\", 5)` is `'   ab'`, `fmt_cell(\"ab\", 5, \"<\")` is "
        "`'ab   '`, `fmt_cell(\"ab\", 5, \"^\")` is `' ab  '`, and "
        "`fmt_cell(\"7\", 3, \">\", \"0\")` is `'007'`.\n\n"
        "One f-string, one line. Do not build the spec by string concatenation, and do "
        "not use `ljust`/`rjust`/`center`."
    ),
    hint=(
        "A format spec can itself contain `{}` placeholders, filled from the same "
        "scope. So the part after the colon does not have to be written out literally."
    ),
    solution=(
        'def fmt_cell(value, width, align=">", fill=" "):\n'
        '    return f"{value:{fill}{align}{width}}"'
    ),
    explanation=(
        "Format specs nest one level deep, which is what makes a dynamic column width "
        "possible without assembling the spec as a string — the inner braces are "
        "evaluated first and the result is handed to the formatter. Order matters and "
        "is easy to reverse: the fill character comes *before* the alignment, so "
        "`{fill}{align}{width}` is right and `{align}{fill}{width}` would read `0` as "
        "the fill and then misparse. Note the last case: a value wider than the field "
        "is never truncated."
    ),
    starter='def fmt_cell(value, width, align=">", fill=" "):\n    ...',
    cases=[
        Case(expected="   ab", args=("ab", 5)),
        Case(expected="ab   ", args=("ab", 5, "<")),
        Case(expected=" ab  ", args=("ab", 5, "^")),
        Case(expected="007", args=("7", 3, ">", "0")),
        Case(expected="abcdef", args=("abcdef", 3)),
        Case(expected="**ab**", args=("ab", 6, "^", "*")),
    ],
)

q(
    qid="Q-071",
    level=Level.L4,
    topic="Methods",
    kind="function",
    entry="parse_query",
    prompt=(
        "Write `parse_query(qs)`, a parser for the query-string tail of a URL. Turn "
        "`\"a=1&b=2\"` into `{'a': '1', 'b': '2'}` — values stay **strings**, and are "
        "never converted.\n\n"
        "Rules:\n\n"
        "- an empty `qs` gives `{}`;\n"
        "- a pair may have an empty value: `\"a=\"` gives `{'a': ''}`;\n"
        "- only the first `=` separates, so `\"a=1=2\"` gives `{'a': '1=2'}`;\n"
        "- a repeated key keeps the **last** value;\n"
        "- a pair with no `=`, or with an empty key, raises `ValueError`."
    ),
    hint=(
        "Split the whole string on the pair separator first, then use Q-058's "
        "single-split method on each pair. The 3-tuple it returns tells you both "
        "things you need to validate: whether a separator was found, and what came "
        "before it."
    ),
    solution=(
        "def parse_query(qs):\n"
        "    result = {}\n"
        "    if not qs:\n"
        "        return result\n"
        '    for pair in qs.split("&"):\n'
        '        key, sep, value = pair.partition("=")\n'
        "        if not sep or not key:\n"
        '            raise ValueError(f"malformed pair: {pair!r}")\n'
        "        result[key] = value\n"
        "    return result"
    ),
    explanation=(
        "The empty-string guard is load-bearing: `\"\".split(\"&\")` is `['']`, not "
        "`[]`, so without it the empty query string becomes one malformed pair and "
        "raises. Checking `sep` rather than `value` is what distinguishes `\"a\"` "
        "(no separator, an error) from `\"a=\"` (a separator and a deliberately empty "
        "value) — the two look identical if you only inspect the value. Last-wins on "
        "duplicates is what plain dict assignment already does; real URL libraries "
        "collect a list instead, because `?tag=x&tag=y` usually means both."
    ),
    starter="def parse_query(qs):\n    ...",
    cases=[
        Case(expected={"a": "1", "b": "2"}, args=("a=1&b=2",)),
        Case(expected={}, args=("",)),
        Case(expected={"a": ""}, args=("a=",)),
        Case(expected={"a": "2"}, args=("a=1&a=2",)),
        Case(expected={"a": "1=2"}, args=("a=1=2",)),
        Case(expected=None, args=("a=1&b",), raises=ValueError),
        Case(expected=None, args=("=1",), raises=ValueError),
    ],
)

q(
    qid="Q-072",
    level=Level.L4,
    topic="Slicing",
    kind="custom",
    entry="chunks",
    constraints=["needs-comprehension", "max-lines:4"],
    prompt=(
        "Write `chunks(text, size)` that cuts `text` into consecutive pieces of "
        "`size` characters and returns them as a **list of strings**. The final piece "
        "may be shorter; an empty `text` gives `[]`.\n\n"
        "`chunks(\"abcdefg\", 3)` returns `['abc', 'def', 'g']`.\n\n"
        "Raise `ValueError` when `size` is zero or negative. Build the list with a "
        "comprehension, in a body of at most 4 lines."
    ),
    hint=(
        "`range` takes a step, and the start of each chunk is exactly one of those "
        "steps. Then rely on slicing's clamping (Q-039) so the short final piece needs "
        "no special case."
    ),
    solution=(
        "def chunks(text, size):\n"
        "    if size <= 0:\n"
        '        raise ValueError("size must be positive")\n'
        "    return [text[i:i + size] for i in range(0, len(text), size)]"
    ),
    explanation=(
        "The clamping that made Q-039 forgiving is what makes the last chunk correct "
        "for free: `text[6:9]` on a 7-character string is simply `'g'`. The guard is "
        "not defensive decoration — `range(0, n, 0)` raises `ValueError` anyway, but "
        "with the message `range() arg 3 must not be zero`, and a negative `size` "
        "would loop zero times and silently return `[]`, losing the whole input."
    ),
    starter="def chunks(text, size):\n    ...",
    cases=[
        Case(expected=["abc", "def", "g"], args=("abcdefg", 3)),
        Case(expected=["abc", "def"], args=("abcdef", 3)),
        Case(expected=[], args=("", 3)),
        Case(expected=["ab"], args=("ab", 5)),
        Case(expected=["a", "b", "c"], args=("abc", 1)),
        Case(expected=None, args=("abc", 0), raises=ValueError),
        Case(expected=None, args=("abc", -1), raises=ValueError),
    ],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-073",
    level=Level.L5,
    topic="Methods",
    kind="custom",
    entry="py_split",
    constraints=["no-builtin:split"],
    prompt=(
        "Reimplement the builtin: `py_split(text, sep=None, maxsplit=-1)` must agree "
        "with `text.split(sep, maxsplit)` on every input.\n\n"
        "Reproduce the whole contract — the two modes really are different "
        "functions:\n\n"
        "- **`sep=None`** (the default): split on *runs* of whitespace, discarding "
        "leading and trailing runs, so `\"  a   b  \"` gives `['a', 'b']` and a blank "
        "string gives `[]`. When `maxsplit` stops you early, the remainder keeps its "
        "trailing whitespace: `py_split(\"  a  b  c  \", None, 1)` is "
        "`['a', 'b  c  ']`.\n"
        "- **an explicit `sep`**: split at every occurrence and keep empty fields, so "
        "`\"a,,b\"` gives `['a', '', 'b']` and `\"\"` gives `['']`.\n"
        "- `maxsplit` caps the number of *splits*, not the number of pieces; `-1` "
        "means no limit.\n"
        "- an empty `sep` raises `ValueError`.\n\n"
        "You may use `str.find`, indexing, slicing and `str.isspace`. Do not call "
        "`str.split` or `str.rsplit`."
    ),
    hint=(
        "Write the two modes as two separate blocks — trying to unify them is what "
        "makes this hard. For the whitespace mode, alternate 'skip separators' and "
        "'consume a token'; check the `maxsplit` budget at the moment you are about to "
        "start a token, and take the rest of the string verbatim when it is spent."
    ),
    solution=(
        "def py_split(text, sep=None, maxsplit=-1):\n"
        "    if sep is None:\n"
        "        parts = []\n"
        "        i = 0\n"
        "        n = len(text)\n"
        "        while True:\n"
        "            while i < n and text[i].isspace():\n"
        "                i += 1\n"
        "            if i >= n:\n"
        "                return parts\n"
        "            if maxsplit >= 0 and len(parts) == maxsplit:\n"
        "                parts.append(text[i:])\n"
        "                return parts\n"
        "            start = i\n"
        "            while i < n and not text[i].isspace():\n"
        "                i += 1\n"
        "            parts.append(text[start:i])\n"
        '    if sep == "":\n'
        '        raise ValueError("empty separator")\n'
        "    parts = []\n"
        "    start = 0\n"
        "    while maxsplit < 0 or len(parts) < maxsplit:\n"
        "        found = text.find(sep, start)\n"
        "        if found < 0:\n"
        "            break\n"
        "        parts.append(text[start:found])\n"
        "        start = found + len(sep)\n"
        "    parts.append(text[start:])\n"
        "    return parts"
    ),
    explanation=(
        "The asymmetry is deliberate, not an accident of implementation: with an "
        "explicit separator every occurrence marks a boundary, so `\"\"` has one "
        "(empty) field and `\"a,,b\"` has three — losing those empties would make CSV "
        "parsing drop columns. With `sep=None` the separator is 'whitespace, however "
        "much of it', which is what you want for prose and command lines, and there "
        "empty fields are meaningless. The `maxsplit` remainder is the detail almost "
        "everyone gets wrong: it is the raw rest of the string, so trailing whitespace "
        "survives in whitespace mode even though the tokens before it were trimmed."
    ),
    starter="def py_split(text, sep=None, maxsplit=-1):\n    ...",
    cases=[
        Case(expected=["a", "b", "c"], args=("a b c",)),
        Case(expected=["a", "b"], args=("  a   b  ",)),
        Case(expected=[], args=("",)),
        Case(expected=[], args=("   ",)),
        Case(expected=["a", "b  c  "], args=("  a  b  c  ", None, 1)),
        Case(expected=["a  "], args=("  a  ", None, 0)),
        Case(expected=["a", "b", "", "c"], args=("a,b,,c", ",")),
        Case(expected=[""], args=("", ",")),
        Case(expected=["", ""], args=(",", ",")),
        Case(expected=["a", "b,c"], args=("a,b,c", ",", 1)),
        Case(expected=["a-b"], args=("a-b", "-", 0)),
        Case(expected=["a", "b"], args=("a<>b", "<>")),
        Case(expected=None, args=("abc", ""), raises=ValueError),
    ],
)

q(
    qid="Q-074",
    level=Level.L5,
    topic="Methods",
    kind="function",
    entry="wrap_text",
    prompt=(
        "Write `wrap_text(text, width)`, a word-wrapper: return a **list of lines**, "
        "each at most `width` characters, with words separated by single spaces.\n\n"
        "- Words are whitespace-separated; all original whitespace is discarded and "
        "rebuilt as single spaces.\n"
        "- A word only moves to the next line when adding it (plus the joining space) "
        "would exceed `width`.\n"
        "- A word longer than `width` is **not** broken — it gets a line of its own "
        "that overflows.\n"
        "- Blank or whitespace-only input gives `[]`.\n"
        "- `width` below `1` raises `ValueError`.\n\n"
        "`wrap_text(\"the quick brown fox\", 10)` returns "
        "`['the quick', 'brown fox']`. Do not import `textwrap`."
    ),
    hint=(
        "Carry one 'line being built' and decide per word whether it still fits. The "
        "arithmetic that catches people is the joining space: a word fits when "
        "`len(current) + 1 + len(word) <= width`, and the very first word on a line is "
        "the exception because there is no space to add."
    ),
    solution=(
        "def wrap_text(text, width):\n"
        "    if width < 1:\n"
        '        raise ValueError("width must be at least 1")\n'
        "    lines = []\n"
        '    current = ""\n'
        "    for word in text.split():\n"
        "        if not current:\n"
        "            current = word\n"
        "        elif len(current) + 1 + len(word) <= width:\n"
        '            current += " " + word\n'
        "        else:\n"
        "            lines.append(current)\n"
        "            current = word\n"
        "    if current:\n"
        "        lines.append(current)\n"
        "    return lines"
    ),
    explanation=(
        "Greedy wrapping — take every word that still fits — is what almost every "
        "terminal and editor does, and the `+ 1` for the joining space is the term "
        "that produces off-by-one ragged margins when it is forgotten. The "
        "first-word-on-a-line branch is not a special case bolted on: without it an "
        "over-long word would be compared against a budget it can never meet and would "
        "loop forever or emit an empty line. The trailing `if current` flush is the "
        "other classic omission, and it silently drops the last line of every "
        "document."
    ),
    starter="def wrap_text(text, width):\n    ...",
    cases=[
        Case(expected=["the quick", "brown fox"], args=("the quick brown fox", 10)),
        Case(expected=["hello world"], args=("hello world", 11)),
        Case(expected=["hello", "world"], args=("hello world", 10)),
        Case(expected=[], args=("", 10)),
        Case(expected=[], args=("   ", 10)),
        Case(expected=["supercalifragilistic"], args=("supercalifragilistic", 5)),
        Case(expected=["a", "b", "c"], args=("a b c", 1)),
        Case(expected=["one two", "three"], args=("  one \n two   three ", 8)),
        Case(expected=None, args=("x", 0), raises=ValueError),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-02",
    title="Word-frequency report",
    brief=(
        "Build `frequency_report(text, top=5)`. Given a paragraph, return a "
        "**single string** holding an aligned two-column frequency table — ready to "
        "`print()`.\n\n"
        "```python\n"
        'frequency_report("the cat sat on the mat the cat", top=3)\n'
        "# 'the  3\\ncat  2\\nmat  1'\n"
        "```\n\n"
        "Rules:\n\n"
        "1. Lowercase the text and split it on whitespace.\n"
        "2. Strip the characters `.,!?;:\"'()` from **both ends** of each word, then "
        "discard anything that is left empty.\n"
        "3. Order by count descending, and alphabetically ascending within an equal "
        "count.\n"
        "4. Keep only the first `top` entries.\n"
        "5. Each row is the word left-aligned, then **two** spaces, then the count "
        "right-aligned. Both column widths are the widest value *among the rows you "
        "actually show* — so `'apple apple banana'` with `top=2` gives "
        "`'apple   2\\nbanana  1'`.\n"
        "6. Rows are joined with `\\n`, with no trailing newline. Text with no words "
        "gives `''`.\n"
        "7. `top` below `1` raises `ValueError`."
    ),
    hint=(
        "Count into a dict, then `sorted(counts.items(), key=...)` with a key that "
        "negates the count so one sort handles both directions at once. Measure the "
        "column widths only *after* slicing to `top` — measuring the full table is the "
        "bug that leaves mysterious extra padding. Then let a nested format spec "
        "(Q-070) take those widths."
    ),
    solution=(
        "def frequency_report(text, top=5):\n"
        "    if top < 1:\n"
        '        raise ValueError("top must be at least 1")\n'
        "    counts = {}\n"
        "    for raw in text.lower().split():\n"
        "        word = raw.strip(\".,!?;:\\\"'()\")\n"
        "        if not word:\n"
        "            continue\n"
        "        counts[word] = counts.get(word, 0) + 1\n"
        "    rows = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top]\n"
        "    if not rows:\n"
        '        return ""\n'
        "    name_width = max(len(word) for word, _ in rows)\n"
        "    count_width = max(len(str(n)) for _, n in rows)\n"
        "    return \"\\n\".join(\n"
        '        f"{word:<{name_width}}  {n:>{count_width}}" for word, n in rows\n'
        "    )"
    ),
    explanation=(
        "Every piece of this notebook shows up here: `split`/`strip` to clean the "
        "words, a dict to count, and a nested format spec to lay out columns whose "
        "width is not known until runtime. The sort key `(-count, word)` is the idiom "
        "worth keeping — a tuple key sorts by each element in turn, and negating a "
        "number is how you reverse *one* field while leaving the tie-break ascending, "
        "which `reverse=True` could not do because it would flip the alphabetical "
        "order too. Measuring the widths after the `[:top]` slice is the rule that "
        "makes the table look deliberate rather than padded."
    ),
    entry="frequency_report",
    starter="def frequency_report(text, top=5):\n    ...",
    cases=[
        Case(expected="the  3\ncat  2\nmat  1",
             args=("the cat sat on the mat the cat",), kwargs={"top": 3}),
        Case(expected="apple   2\nbanana  1",
             args=("apple apple banana",), kwargs={"top": 2}),
        Case(expected="hello  3", args=("Hello, hello! HELLO?",)),
        Case(expected="", args=("",)),
        Case(expected="", args=("   ...   ",)),
        Case(expected="a  1", args=("a b",), kwargs={"top": 1}),
        Case(expected="be   2\nto   2\nnot  1\nor   1",
             args=("To be, or not to be.",), kwargs={"top": 4}),
        Case(expected=None, args=("a b",), kwargs={"top": 0}, raises=ValueError),
    ],
)

NOTEBOOK = Notebook(
    number=2,
    slug="strings",
    title="Strings",
    intro=(
        "Indexing and slicing, f-strings and their format specs, and the string "
        "methods you will actually reach for: `split`, `join`, `strip`, `replace`, "
        "`find`, `partition` and the rest.\n\n"
        "One idea sits underneath all of it: **strings are immutable**. Nothing here "
        "ever modifies a string — every method hands you a new one — and once that "
        "clicks, the `s.upper()` that 'does nothing', the quadratic `+=` loop and the "
        "existence of `join` all stop being separate facts."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
