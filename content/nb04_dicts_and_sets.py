"""Notebook 04 - Dicts & Sets (Q-113..Q-150)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


# ---------------------------------------------------------------- L1 ----

q(
    qid="Q-113",
    level=Level.L1,
    topic="Dicts",
    kind="value",
    entry="prices",
    prompt=(
        "Create a dict named `prices` with exactly three entries: `\"pen\"` costs "
        "`2`, `\"pad\"` costs `5`, `\"ink\"` costs `3`.\n\n"
        "The keys are strings and the values are ints — the checker is strict about "
        "both."
    ),
    hint=(
        "A dict literal is written with braces, a colon between each key and its "
        "value, and a comma between the pairs."
    ),
    solution='prices = {"pen": 2, "pad": 5, "ink": 3}',
    explanation=(
        "A dict is a mapping from keys to values, and braces are its literal form. "
        "The classic slip is writing a comma where the colon belongs — that produces "
        "a *set* of six items instead, and the error only shows up later."
    ),
    starter="prices = ...",
    cases=[Case(expected={"pen": 2, "pad": 5, "ink": 3})],
)

q(
    qid="Q-114",
    level=Level.L1,
    topic="Dicts",
    kind="function",
    entry="price_of",
    prompt=(
        "Write `price_of(prices, name)` that returns the value stored under the key "
        "`name` in the dict `prices`, using square-bracket lookup.\n\n"
        "When `name` is not a key, do **not** return a fallback — let the lookup "
        "raise `KeyError`. Two of the test cases require exactly that."
    ),
    hint=(
        "This is a one-expression body. The failure behaviour the prompt asks for is "
        "what subscripting a dict already does, so you must not wrap it in anything."
    ),
    solution="def price_of(prices, name):\n    return prices[name]",
    explanation=(
        "Subscripting a dict with a key it does not hold raises `KeyError` — loudly, "
        "at the line that made the wrong assumption. Reaching for `.get()` to make "
        "that error go away is the classic mistake: it turns a missing key into a "
        "silent `None` that fails somewhere else entirely."
    ),
    starter="def price_of(prices, name):\n    ...",
    cases=[
        Case(expected=2, args=({"pen": 2, "pad": 5}, "pen")),
        Case(expected=0, args=({"free": 0, "pen": 2}, "free")),
        Case(expected=None, args=({"pen": 2}, "pad"), raises=KeyError),
        Case(expected=None, args=({}, "pen"), raises=KeyError),
    ],
)

q(
    qid="Q-115",
    level=Level.L1,
    topic="Dict Methods",
    kind="function",
    entry="price_or",
    prompt=(
        "Write `price_or(prices, name, fallback)` that returns the value stored "
        "under `name`, or `fallback` when `name` is not a key.\n\n"
        "It must never raise. A key that *is* present but holds `0` must give back "
        "`0`, not the fallback."
    ),
    hint=(
        "Dicts have a lookup method that takes the not-found value as a second "
        "argument. You should not need `try`, and you should not need `in`."
    ),
    solution="def price_or(prices, name, fallback):\n    return prices.get(name, fallback)",
    explanation=(
        "`.get(key, fallback)` is the non-raising lookup, and it decides on "
        "*presence*, never on truthiness. That is why it beats "
        "`prices[name] if prices[name] else fallback`, which would hand back the "
        "fallback for a genuine stored `0`."
    ),
    starter="def price_or(prices, name, fallback):\n    ...",
    cases=[
        Case(expected=2, args=({"pen": 2}, "pen", 99)),
        Case(expected=99, args=({"pen": 2}, "pad", 99)),
        Case(expected=0, args=({"free": 0}, "free", 99)),
        Case(expected=None, args=({}, "pen", None)),
    ],
)

q(
    qid="Q-116",
    level=Level.L1,
    topic="Dicts",
    kind="function",
    entry="stocked",
    prompt=(
        "Write `stocked(inventory, sku)` that returns `True` when `sku` is a key of "
        "the dict `inventory`, and `False` otherwise.\n\n"
        "Use the `in` operator and return a real `bool`. A key whose value is `0` is "
        "still a key."
    ),
    hint=(
        "`in` applied to a dict already asks about one of the two halves of an entry "
        "— and it is the same half you would subscript with. The comparison is "
        "already the answer; do not wrap it in an `if`."
    ),
    solution="def stocked(inventory, sku):\n    return sku in inventory",
    explanation=(
        "`in` on a dict tests **keys** only, and does it in constant time through the "
        "hash table. Do not confuse presence with truthiness: `{\"pen\": 0}` contains "
        "the key `\"pen\"` even though its value is falsy."
    ),
    starter="def stocked(inventory, sku):\n    ...",
    cases=[
        Case(expected=True, args=({"pen": 4, "pad": 1}, "pen")),
        Case(expected=False, args=({"pen": 4}, "ink")),
        Case(expected=True, args=({"pen": 0}, "pen")),
        Case(expected=False, args=({}, "pen")),
    ],
)

q(
    qid="Q-117",
    level=Level.L1,
    topic="Iteration",
    kind="function",
    entry="sku_list",
    prompt=(
        "Write `sku_list(inventory)` that returns the keys of the dict `inventory` "
        "as a **sorted list of strings**.\n\n"
        "`sku_list({\"pen\": 1, \"ink\": 2})` returns `['ink', 'pen']`. Return a "
        "`list` — a `dict_keys` view will not pass."
    ),
    hint=(
        "There is a dict method that hands you a view of the keys, and one builtin "
        "that turns any iterable into a list in order. Only one of the two is "
        "actually necessary here."
    ),
    solution="def sku_list(inventory):\n    return sorted(inventory)",
    explanation=(
        "Iterating a dict yields its keys, so `sorted(inventory)` already sees the "
        "keys and returns a real list — `sorted(inventory.keys())` is the same thing "
        "spelled longer. `list(inventory.keys())` would also give a list, but in "
        "insertion order rather than sorted."
    ),
    starter="def sku_list(inventory):\n    ...",
    cases=[
        Case(expected=["ink", "pen"], args=({"pen": 1, "ink": 2},)),
        Case(expected=[], args=({},)),
        Case(expected=["solo"], args=({"solo": 9},)),
        Case(expected=["a", "b", "c"], args=({"c": 1, "a": 2, "b": 3},)),
    ],
)

q(
    qid="Q-118",
    level=Level.L1,
    topic="Dicts",
    kind="function",
    entry="restock",
    prompt=(
        "Write `restock(inventory, sku, qty)` that stores `qty` under the key `sku` "
        "in the dict `inventory`, then returns that same dict.\n\n"
        "Assigning to a key that already exists must overwrite it — there is no "
        "separate 'add' and 'update' operation to choose between."
    ),
    hint=(
        "Square brackets on the left of an `=` write, the same way brackets on the "
        "right read. The one thing to remember is that the write happens in place, "
        "so the function still has to hand the dict back."
    ),
    solution="def restock(inventory, sku, qty):\n    inventory[sku] = qty\n    return inventory",
    explanation=(
        "A dict is mutable, so `inventory[sku] = qty` changes the object every "
        "caller shares — there is no copy and no return value from the assignment "
        "itself. One syntax covers insert and overwrite, which is convenient until "
        "you clobber an entry you meant to keep."
    ),
    starter="def restock(inventory, sku, qty):\n    ...",
    cases=[
        Case(expected={"pen": 4, "ink": 7}, args=({"pen": 4}, "ink", 7)),
        Case(expected={"pen": 9}, args=({"pen": 4}, "pen", 9)),
        Case(expected={"pen": 0}, args=({}, "pen", 0)),
    ],
)

q(
    qid="Q-119",
    level=Level.L1,
    topic="Sets",
    kind="value",
    entry="tags",
    prompt=(
        "Set `tags` to a set literal containing exactly these four items, written in "
        "this order: `\"new\"`, `\"sale\"`, `\"new\"`, `\"clearance\"`.\n\n"
        "Write all four out — do not tidy the duplicate away yourself. Then look at "
        "what the checker expects."
    ),
    hint=(
        "Braces make a set when they hold bare values rather than key/value pairs. "
        "Think about what a set does with a value it already holds."
    ),
    solution='tags = {"new", "sale", "new", "clearance"}',
    explanation=(
        "A set holds each value at most once, so the duplicate collapses at "
        "construction time with no error and no warning — which is exactly why "
        "`set(...)` is the standard way to dedupe. A set is also unordered: never "
        "assume the order you typed survives."
    ),
    starter="tags = ...",
    cases=[Case(expected={"new", "sale", "clearance"})],
)

q(
    qid="Q-120",
    level=Level.L1,
    topic="Sets",
    kind="function",
    entry="add_tag",
    prompt=(
        "Write `add_tag(tags, tag)` that adds `tag` to the set `tags` and returns "
        "that same set.\n\n"
        "Adding something the set already holds is not an error and must leave the "
        "set unchanged."
    ),
    hint=(
        "Sets have a one-argument method for putting a single element in. It mutates "
        "in place and gives back `None`, so returning its result would be a bug."
    ),
    solution="def add_tag(tags, tag):\n    tags.add(tag)\n    return tags",
    explanation=(
        "`.add()` is idempotent: adding a present element is a no-op, because the "
        "set is defined by membership rather than by counts. The mistake to avoid is "
        "`return tags.add(tag)` — like most in-place mutators it returns `None`, and "
        "you would hand back nothing at all."
    ),
    starter="def add_tag(tags, tag):\n    ...",
    cases=[
        Case(expected={"new", "sale"}, args=({"new"}, "sale")),
        Case(expected={"new"}, args=({"new"}, "new")),
        Case(expected={"new"}, args=(set(), "new")),
    ],
)

q(
    qid="Q-121",
    level=Level.L1,
    topic="Set Algebra",
    kind="function",
    entry="all_skus",
    prompt=(
        "Write `all_skus(a, b)` that returns a **set** holding every SKU that is in "
        "the set `a`, the set `b`, or both.\n\n"
        "Use the union operator, and do not mutate either argument."
    ),
    hint=(
        "One of the four set operators covers 'in either one'. It is a single "
        "character, and it builds a new set rather than changing `a`."
    ),
    solution="def all_skus(a, b):\n    return a | b",
    explanation=(
        "`|` is union and returns a fresh set, leaving both operands alone — unlike "
        "`a |= b` or `a.update(b)`, which modify `a` in place. `a.union(b)` is the "
        "method spelling and accepts any iterable, while `|` insists both sides are "
        "already sets."
    ),
    starter="def all_skus(a, b):\n    ...",
    cases=[
        Case(expected={"p1", "p2", "p3"}, args=({"p1", "p2"}, {"p2", "p3"})),
        Case(expected={"p1", "p9"}, args=({"p1"}, {"p9"})),
        Case(expected={"p1"}, args=({"p1"}, set())),
        Case(expected=set(), args=(set(), set())),
    ],
)

# ---------------------------------------------------------------- L2 ----

q(
    qid="Q-122",
    level=Level.L2,
    topic="Iteration",
    kind="function",
    entry="total_stock",
    prompt=(
        "Write `total_stock(inventory)` that returns the sum of all the values in "
        "the dict `inventory` as an `int`.\n\n"
        "An empty dict totals `0`."
    ),
    hint=(
        "Iterating a dict directly gives you the wrong half of each entry for this "
        "job. There is a method that hands you the other half as an iterable."
    ),
    solution="def total_stock(inventory):\n    return sum(inventory.values())",
    explanation=(
        "`.values()` is a live view of the values, and `sum` consumes it without "
        "building a list. Writing `sum(inventory)` instead adds up the *keys*, which "
        "silently gives a wrong number when the keys happen to be numeric and a "
        "`TypeError` when they are not."
    ),
    starter="def total_stock(inventory):\n    ...",
    cases=[
        Case(expected=12, args=({"pen": 4, "pad": 8},)),
        Case(expected=0, args=({},)),
        Case(expected=0, args=({"pen": 0, "pad": 0},)),
        Case(expected=5, args=({"solo": 5},)),
    ],
)

q(
    qid="Q-123",
    level=Level.L2,
    topic="Iteration",
    kind="function",
    entry="pairs",
    prompt=(
        "Write `pairs(inventory)` that returns a **list of `(key, value)` tuples**, "
        "sorted by key.\n\n"
        "`pairs({\"pen\": 4, \"ink\": 1})` returns `[('ink', 1), ('pen', 4)]`. Real "
        "tuples in a real list — a `dict_items` view will not pass."
    ),
    hint=(
        "One dict method yields both halves of each entry at once. Sorting an "
        "iterable of tuples already compares the first element first, so no `key=` "
        "argument is needed."
    ),
    solution="def pairs(inventory):\n    return sorted(inventory.items())",
    explanation=(
        "`.items()` yields `(key, value)` tuples, and `sorted` on tuples compares "
        "element 0 first and only consults element 1 on a tie. `sorted` always "
        "returns a list, which is what converts the view into the concrete type the "
        "prompt asks for."
    ),
    starter="def pairs(inventory):\n    ...",
    cases=[
        Case(expected=[("ink", 1), ("pen", 4)], args=({"pen": 4, "ink": 1},)),
        Case(expected=[], args=({},)),
        Case(expected=[("solo", 0)], args=({"solo": 0},)),
        Case(expected=[("a", 1), ("b", 2), ("c", 3)], args=({"c": 3, "a": 1, "b": 2},)),
    ],
)

q(
    qid="Q-124",
    level=Level.L2,
    topic="Dict Methods",
    kind="function",
    entry="merged",
    prompt=(
        "Write `merged(base, extra)` that returns a **new** dict holding every entry "
        "of both, with `extra` winning on any key they share.\n\n"
        "Neither argument may be modified — the checker calls each case twice."
    ),
    hint=(
        "Copy first, then fold the second dict into the copy with the bulk-write "
        "method. `dict(base)` is one way to get that copy."
    ),
    solution=(
        "def merged(base, extra):\n"
        "    out = dict(base)\n"
        "    out.update(extra)\n"
        "    return out"
    ),
    explanation=(
        "`.update()` writes in place and returns `None`, so it needs a copy to work "
        "on if the caller's dict must survive. The trap is calling "
        "`base.update(extra)` and returning `base`: it works once, then corrupts the "
        "caller's data on the next call. Python 3.9+ also spells this `base | extra`."
    ),
    starter="def merged(base, extra):\n    ...",
    cases=[
        Case(expected={"pen": 4, "pad": 2, "ink": 7}, args=({"pen": 4, "pad": 1}, {"pad": 2, "ink": 7})),
        Case(expected={"pen": 4}, args=({"pen": 4}, {})),
        Case(expected={"ink": 7}, args=({}, {"ink": 7})),
        Case(expected={}, args=({}, {})),
    ],
)

q(
    qid="Q-125",
    level=Level.L2,
    topic="Dict Methods",
    kind="function",
    entry="without",
    prompt=(
        "Write `without(inventory, sku, fallback)` that returns the tuple "
        "`(removed_value, remaining_dict)`.\n\n"
        "`remaining_dict` is a **new** dict — a copy of `inventory` with `sku` taken "
        "out — and `removed_value` is what was stored there, or `fallback` when "
        "`sku` was not present. `inventory` itself must not change."
    ),
    hint=(
        "The dict method that removes an entry also hands you its value, and it "
        "takes a second argument for the not-found case. Run it against a copy."
    ),
    solution=(
        "def without(inventory, sku, fallback):\n"
        "    remaining = dict(inventory)\n"
        "    removed = remaining.pop(sku, fallback)\n"
        "    return (removed, remaining)"
    ),
    explanation=(
        "`.pop(key)` removes and returns in one step, and raises `KeyError` when the "
        "key is missing *unless* you pass a default — the default is the whole "
        "difference between a crash and a no-op. A stored `0` still comes back as "
        "`0`, because `pop` reports presence, not truthiness."
    ),
    starter="def without(inventory, sku, fallback):\n    ...",
    cases=[
        Case(expected=(4, {"pad": 1}), args=({"pen": 4, "pad": 1}, "pen", None)),
        Case(expected=(None, {"pen": 4}), args=({"pen": 4}, "ink", None)),
        Case(expected=(0, {}), args=({"pen": 0}, "pen", -1)),
        Case(expected=(-1, {}), args=({}, "pen", -1)),
    ],
)

q(
    qid="Q-126",
    level=Level.L2,
    topic="Dict Methods",
    kind="function",
    entry="by_initial",
    prompt=(
        "Write `by_initial(words)` that returns a dict mapping each first letter to "
        "the **list** of words starting with it, in the order they appear.\n\n"
        "`by_initial([\"ant\", \"bee\", \"ape\"])` returns "
        "`{'a': ['ant', 'ape'], 'b': ['bee']}`. Use `setdefault` so you never have "
        "to test whether the letter is already a key. Assume no word is empty."
    ),
    hint=(
        "`setdefault` returns the value for a key, inserting the given value first "
        "if the key was missing. The value it returns is the very list you want to "
        "append to."
    ),
    solution=(
        "def by_initial(words):\n"
        "    groups = {}\n"
        "    for word in words:\n"
        "        groups.setdefault(word[0], []).append(word)\n"
        "    return groups"
    ),
    explanation=(
        "`setdefault` collapses 'look up, create if missing, then use' into one call, "
        "and it returns the *stored* value — so appending to it mutates what is in "
        "the dict. Note it always builds the default object even when the key "
        "already exists (Q-146); `collections.defaultdict` avoids that waste."
    ),
    starter="def by_initial(words):\n    ...",
    cases=[
        Case(expected={"a": ["ant", "ape"], "b": ["bee"]}, args=(["ant", "bee", "ape"],)),
        Case(expected={}, args=([],)),
        Case(expected={"x": ["xi"]}, args=(["xi"],)),
        Case(expected={"a": ["ant", "ant"]}, args=(["ant", "ant"],)),
    ],
)

q(
    qid="Q-127",
    level=Level.L2,
    topic="Set Algebra",
    kind="function",
    entry="in_both",
    prompt=(
        "Write `in_both(a, b)` that returns a **set** of the SKUs present in both "
        "sets.\n\n"
        "When they share nothing, return an empty set — not `None`, and not `{}`."
    ),
    hint=(
        "The operator for 'in this one *and* that one' is the same symbol Python "
        "uses for bitwise and. It builds a new set."
    ),
    solution="def in_both(a, b):\n    return a & b",
    explanation=(
        "`&` is intersection. The detail worth internalising is that the empty set "
        "has no literal — `{}` is an empty *dict*, so you must write `set()`. "
        "`a.intersection(b)` is the method form and accepts any iterable."
    ),
    starter="def in_both(a, b):\n    ...",
    cases=[
        Case(expected={"p2"}, args=({"p1", "p2"}, {"p2", "p3"})),
        Case(expected=set(), args=({"p1"}, {"p9"})),
        Case(expected={"p1", "p2"}, args=({"p1", "p2"}, {"p1", "p2"})),
        Case(expected=set(), args=(set(), {"p1"})),
    ],
)

q(
    qid="Q-128",
    level=Level.L2,
    topic="Set Algebra",
    kind="function",
    entry="discontinued",
    prompt=(
        "Write `discontinued(old, new)` that returns a **set** of the SKUs that were "
        "in `old` but are gone from `new`.\n\n"
        "The order of the two arguments is the whole question — difference is not "
        "symmetric."
    ),
    hint=(
        "One operator removes everything on its right from everything on its left. "
        "Decide which argument belongs on which side before you write it."
    ),
    solution="def discontinued(old, new):\n    return old - new",
    explanation=(
        "`-` keeps the elements of the left operand that are absent from the right, "
        "so `old - new` is 'dropped' and `new - old` is 'added' — swapping them is "
        "the single most common set-algebra bug. Elements only in `new` are simply "
        "ignored; the result is always a subset of `old`."
    ),
    starter="def discontinued(old, new):\n    ...",
    cases=[
        Case(expected={"p1"}, args=({"p1", "p2"}, {"p2", "p3"})),
        Case(expected=set(), args=({"p1"}, {"p1", "p2"})),
        Case(expected={"p1"}, args=({"p1"}, set())),
        Case(expected=set(), args=(set(), {"p1"})),
    ],
)

q(
    qid="Q-129",
    level=Level.L2,
    topic="Set Algebra",
    kind="function",
    entry="changed",
    prompt=(
        "Write `changed(old, new)` that returns a **set** of the SKUs that are in "
        "exactly one of the two sets — dropped or added, but not unchanged.\n\n"
        "Use the symmetric-difference operator; do not build it from two "
        "differences."
    ),
    hint=(
        "The fourth set operator is the caret, the same symbol as bitwise xor, and "
        "the analogy is exact: an element is in the result when it is in one side "
        "only."
    ),
    solution="def changed(old, new):\n    return old ^ new",
    explanation=(
        "`^` is symmetric difference: everything in the union that is not in the "
        "intersection. Unlike `-` it is symmetric, so argument order genuinely does "
        "not matter — which makes it the right tool for 'what differs' and the wrong "
        "one when you need to know *which way*."
    ),
    starter="def changed(old, new):\n    ...",
    cases=[
        Case(expected={"p1", "p3"}, args=({"p1", "p2"}, {"p2", "p3"})),
        Case(expected=set(), args=({"p1", "p2"}, {"p1", "p2"})),
        Case(expected={"p1", "p9"}, args=({"p1"}, {"p9"})),
        Case(expected={"p1"}, args=(set(), {"p1"})),
    ],
)

q(
    qid="Q-130",
    level=Level.L2,
    topic="Sets",
    kind="function",
    entry="unique_sorted",
    prompt=(
        "Write `unique_sorted(values)` that returns a **sorted list** of the "
        "distinct entries of the list `values`.\n\n"
        "`unique_sorted([3, 1, 3, 2])` returns `[1, 2, 3]`. Return a `list`, not a "
        "set."
    ),
    hint=(
        "Deduplicating and ordering are two separate steps, and the type that does "
        "the first one refuses to do the second. Do them in that order."
    ),
    solution="def unique_sorted(values):\n    return sorted(set(values))",
    explanation=(
        "`set()` drops duplicates in one pass, and `sorted` then imposes the order a "
        "set does not have. Skipping the `sorted` and returning the set — or worse, "
        "`list(set(values))` — gives an order that is not guaranteed and can differ "
        "between runs for strings, which is how flaky tests are born."
    ),
    starter="def unique_sorted(values):\n    ...",
    cases=[
        Case(expected=[1, 2, 3], args=([3, 1, 3, 2],)),
        Case(expected=[], args=([],)),
        Case(expected=[7], args=([7, 7, 7],)),
        Case(expected=["a", "b"], args=(["b", "a", "b"],)),
    ],
)

q(
    qid="Q-131",
    level=Level.L2,
    topic="Sets",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "print(type({}).__name__)\n"
        "print(type({1}).__name__)\n"
        "print(type(set()).__name__)\n"
        "print(len({}))\n"
        "```\n\n"
        "Set `answer` to the four printed lines, e.g. "
        "`answer = \"set\\nset\\nset\\n0\"`."
    ),
    hint=(
        "Braces are shared between two types, and one of them got there first. Ask "
        "what is inside each pair of braces, and what is inside none of them."
    ),
    solution='answer = "dict\\nset\\nset\\n0"',
    explanation=(
        "Empty braces are an empty **dict** — dicts claimed the literal first, so "
        "the empty set has no literal at all and must be written `set()`. Braces "
        "with bare values make a set; braces with `key: value` pairs make a dict."
    ),
    starter="answer = ...",
    cases=[Case(expected="dict\nset\nset\n0")],
)

q(
    qid="Q-132",
    level=Level.L2,
    topic="Hashability",
    kind="function",
    entry="count_groups",
    prompt=(
        "Write `count_groups(groups)` where `groups` is a list of lists of tags. "
        "Return a dict mapping each distinct **frozenset** of tags to how many times "
        "it occurs.\n\n"
        "Order within a group does not matter, so `[\"a\", \"b\"]` and "
        "`[\"b\", \"a\"]` count as the same group. The keys of your result must be "
        "`frozenset` objects — a `set` will not pass."
    ),
    hint=(
        "A list cannot be a dict key and neither can a set; there is one immutable "
        "set type that can. Build it from each group, then count with `.get`."
    ),
    solution=(
        "def count_groups(groups):\n"
        "    counts = {}\n"
        "    for group in groups:\n"
        "        key = frozenset(group)\n"
        "        counts[key] = counts.get(key, 0) + 1\n"
        "    return counts"
    ),
    explanation=(
        "A dict key must be hashable, and `set` is mutable and therefore unhashable "
        "— `frozenset` is its immutable twin, built exactly so a set of things can "
        "*be* a key. Converting through `frozenset` also makes order and duplicates "
        "irrelevant for free, which is what lets the two spellings collapse."
    ),
    starter="def count_groups(groups):\n    ...",
    cases=[
        Case(
            expected={frozenset({"a", "b"}): 2, frozenset({"c"}): 1},
            args=([["a", "b"], ["b", "a"], ["c"]],),
        ),
        Case(expected={}, args=([],)),
        Case(expected={frozenset(): 1}, args=([[]],)),
        Case(expected={frozenset({"a"}): 2}, args=([["a"], ["a", "a"]],)),
    ],
)

q(
    qid="Q-133",
    level=Level.L2,
    topic="Dicts",
    kind="function",
    entry="city_of",
    prompt=(
        "Write `city_of(people, name)` where `people` maps a name to a dict of that "
        "person's details. Return the value stored under `\"city\"` in that inner "
        "dict.\n\n"
        "`city_of({\"ada\": {\"city\": \"London\"}}, \"ada\")` returns `'London'`. "
        "An unknown name or a person with no `\"city\"` key must raise `KeyError` — "
        "do not catch anything."
    ),
    hint=(
        "Each subscript hands back another object; if that object is itself a dict, "
        "you can subscript the result directly. No temporary variable is needed."
    ),
    solution='def city_of(people, name):\n    return people[name]["city"]',
    explanation=(
        "Chained subscripts just apply left to right — `people[name]` produces the "
        "inner dict, which is then indexed again. When one fails, the `KeyError` "
        "names only the key that was missing, not the level, which is why deep "
        "nesting is worth flattening or wrapping in a helper (Q-142)."
    ),
    starter="def city_of(people, name):\n    ...",
    cases=[
        Case(expected="London", args=({"ada": {"city": "London", "age": 36}}, "ada")),
        Case(expected="Oslo", args=({"ada": {"city": "London"}, "bo": {"city": "Oslo"}}, "bo")),
        Case(expected=None, args=({"ada": {"city": "London"}}, "zed"), raises=KeyError),
        Case(expected=None, args=({"ada": {"age": 36}}, "ada"), raises=KeyError),
    ],
)

# ---------------------------------------------------------------- L3 ----

q(
    qid="Q-134",
    level=Level.L3,
    topic="Hashability",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'd = {1: "a", True: "b", 1.0: "c"}\n'
        "print(d)\n"
        "print(len(d))\n"
        'print(d[True])\n'
        "```\n\n"
        "Set `answer` to the three printed lines. Give the dict exactly as Python "
        "would print it, quotes and all."
    ),
    hint=(
        "A dict finds a key by hash first and equality second — the type is never "
        "consulted. Then ask which of the three keys is the one actually stored."
    ),
    solution="answer = \"{1: 'c'}\\n1\\nc\"",
    explanation=(
        "`1 == True == 1.0` and all three hash identically, so these are one key "
        "written three ways: each later entry overwrites the value. The stored **key "
        "object stays the one inserted first**, which is why it prints as `1` rather "
        "than `True` or `1.0` — mixing numeric types as keys loses data with no error."
    ),
    starter="answer = ...",
    cases=[Case(expected="{1: 'c'}\n1\nc")],
)

q(
    qid="Q-135",
    level=Level.L3,
    topic="Dict Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'd = {"a": 1}\n'
        'print(d.get("b"))\n'
        'print(d.get("b", 0))\n'
        "try:\n"
        '    print(d["b"])\n'
        "except KeyError as err:\n"
        '    print("KeyError", err)\n'
        "```\n\n"
        "Set `answer` to the three printed lines. The third one includes whatever "
        "`print` makes of the exception object."
    ),
    hint=(
        "Two of the three lookups refuse to fail. For the last line, think about "
        "what a `KeyError` carries as its argument and how that argument is "
        "displayed."
    ),
    solution='answer = "None\\n0\\nKeyError \'b\'"',
    explanation=(
        "`.get()` returns `None` for a missing key and never raises, while `d[k]` "
        "raises `KeyError` carrying the key itself — printed with `repr`, hence the "
        "quotes around `b`. Choosing `.get()` by reflex is how a missing key becomes "
        "a `None` that crashes three functions later, far from the real cause."
    ),
    starter="answer = ...",
    cases=[Case(expected="None\n0\nKeyError 'b'")],
)

q(
    qid="Q-136",
    level=Level.L3,
    topic="Iteration",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'd = {"a": 1, "b": 2}\n'
        "try:\n"
        "    for k in d:\n"
        '        d[k + "!"] = 0\n'
        "except RuntimeError as err:\n"
        "    print(type(err).__name__)\n"
        "print(len(d))\n"
        "```\n\n"
        "Set `answer` to the two printed lines. The second one requires counting how "
        "far the loop got before it stopped."
    ),
    hint=(
        "Iterating a dict walks its internal table, which is not safe to resize "
        "mid-walk — Python notices. Work out how many insertions happen before the "
        "iterator is asked for its next key."
    ),
    solution='answer = "RuntimeError\\n3"',
    explanation=(
        "A dict iterator checks the dict's size on every step and raises "
        "`RuntimeError: dictionary changed size during iteration` — so the first "
        "insertion succeeds and the *next* `next()` blows up, leaving three entries. "
        "Iterate over a snapshot (`list(d)` or `list(d.items())`) whenever the body "
        "adds or deletes keys."
    ),
    starter="answer = ...",
    cases=[Case(expected="RuntimeError\n3")],
)

q(
    qid="Q-137",
    level=Level.L3,
    topic="Dict Methods",
    kind="custom",
    entry="invert",
    constraints=["needs-comprehension", "max-lines:2"],
    prompt=(
        "Write `invert(d)` that returns a new dict with keys and values swapped.\n\n"
        "`invert({\"a\": 1})` returns `{1: 'a'}`. When two keys share a value, the "
        "one that appears **later** wins — do not try to prevent that.\n\n"
        "Write it as a single dict comprehension; the body is at most 2 lines."
    ),
    hint=(
        "A dict comprehension has the same `key: value` shape as a literal, fed by a "
        "`for` clause. The method that yields both halves of an entry at once is what "
        "you iterate."
    ),
    solution="def invert(d):\n    return {v: k for k, v in d.items()}",
    explanation=(
        "Unpacking `.items()` into `k, v` and writing them back in the other order is "
        "the whole trick. Inverting is lossy by nature — values need not be unique, "
        "and they must be hashable, so a dict whose values are lists cannot be "
        "inverted at all."
    ),
    starter="def invert(d):\n    ...",
    cases=[
        Case(expected={1: "a", 2: "b"}, args=({"a": 1, "b": 2},)),
        Case(expected={}, args=({},)),
        Case(expected={1: "b"}, args=({"a": 1, "b": 1},)),
        Case(expected={"x": 0}, args=({0: "x"},)),
    ],
)

q(
    qid="Q-138",
    level=Level.L3,
    topic="Iteration",
    kind="custom",
    entry="tally",
    constraints=["no-builtin:Counter", "max-lines:6"],
    prompt=(
        "Write `tally(items)` that returns a dict mapping each distinct item to the "
        "number of times it appears in the list `items`.\n\n"
        "`tally([\"a\", \"b\", \"a\"])` returns `{'a': 2, 'b': 1}`. Build it by hand "
        "— `collections.Counter` is off limits here, and so is a plain `count()` per "
        "item."
    ),
    hint=(
        "For each item you need its running total, which is `0` the first time you "
        "see it. The non-raising lookup with a default is what supplies that zero."
    ),
    solution=(
        "def tally(items):\n"
        "    counts = {}\n"
        "    for item in items:\n"
        "        counts[item] = counts.get(item, 0) + 1\n"
        "    return counts"
    ),
    explanation=(
        "`counts.get(item, 0) + 1` is the counting idiom: one lookup, a default for "
        "the first sighting, one write. The alternative people reach for — "
        "`items.count(item)` inside a loop — rescans the whole list for every element "
        "and turns a linear job into a quadratic one."
    ),
    starter="def tally(items):\n    ...",
    cases=[
        Case(expected={"a": 2, "b": 1}, args=(["a", "b", "a"],)),
        Case(expected={}, args=([],)),
        Case(expected={"x": 1}, args=(["x"],)),
        Case(expected={1: 3}, args=([1, 1, 1],)),
    ],
)

q(
    qid="Q-139",
    level=Level.L3,
    topic="Hashability",
    kind="function",
    entry="is_hashable",
    prompt=(
        "Write `is_hashable(value)` that returns `True` when `value` could be used "
        "as a dict key or a set element, and `False` when it could not.\n\n"
        "Do not list the types by hand — ask the object. Return a real `bool`."
    ),
    hint=(
        "There is a builtin that computes the very thing a dict needs, and it raises "
        "a specific exception on objects that cannot provide it. Catch that "
        "exception by name, not with a bare `except`."
    ),
    solution=(
        "def is_hashable(value):\n"
        "    try:\n"
        "        hash(value)\n"
        "    except TypeError:\n"
        "        return False\n"
        "    return True"
    ),
    explanation=(
        "Hashability is not a type whitelist: it is whether `hash()` works, which "
        "fails with `TypeError` for mutable containers because a hash that changed "
        "would lose the object inside its own dict. A tuple is hashable **only if "
        "everything in it is** — `(1, [2])` is not — which is why asking beats "
        "guessing."
    ),
    starter="def is_hashable(value):\n    ...",
    cases=[
        Case(expected=True, args=(1,)),
        Case(expected=True, args=("a",)),
        Case(expected=True, args=((1, 2),)),
        Case(expected=True, args=(frozenset({1}),)),
        Case(expected=False, args=([1],)),
        Case(expected=False, args=({"a": 1},)),
        Case(expected=False, args=({1, 2},)),
        Case(expected=False, args=((1, [2]),)),
    ],
)

q(
    qid="Q-140",
    level=Level.L3,
    topic="Dicts",
    kind="function",
    entry="first_key",
    prompt=(
        "Write `first_key(d)` that returns the key that was inserted **first**, or "
        "`None` when `d` is empty.\n\n"
        "Do not sort, and do not build a list of every key just to take one item. "
        "The dict already knows the answer."
    ),
    hint=(
        "Since Python 3.7 a dict remembers insertion order, so iterating it yields "
        "the first key first. You need an iterator and a way to ask it for one item "
        "without exploding on an empty one."
    ),
    solution="def first_key(d):\n    return next(iter(d), None)",
    explanation=(
        "Dicts preserve insertion order as a *language guarantee* since 3.7, so "
        "'first key' is well defined and `next(iter(d), None)` reads it in constant "
        "time. `list(d)[0]` copies every key to use one of them, and raises "
        "`IndexError` on an empty dict rather than returning the `None` the second "
        "argument to `next` supplies."
    ),
    starter="def first_key(d):\n    ...",
    cases=[
        Case(expected="z", args=({"z": 1, "a": 2},)),
        Case(expected=None, args=({},)),
        Case(expected="solo", args=({"solo": 0},)),
        Case(expected=3, args=({3: "c", 1: "a", 2: "b"},)),
    ],
)

q(
    qid="Q-141",
    level=Level.L3,
    topic="Set Algebra",
    kind="function",
    entry="relation",
    prompt=(
        "Write `relation(a, b)` that classifies two sets, returning exactly one of "
        "these strings:\n\n"
        "- `'equal'` — the same elements\n"
        "- `'subset'` — every element of `a` is in `b`, and `b` has more\n"
        "- `'superset'` — every element of `b` is in `a`, and `a` has more\n"
        "- `'disjoint'` — they share nothing\n"
        "- `'overlap'` — anything else\n\n"
        "Two empty sets are `'equal'`. An empty `a` against a non-empty `b` is "
        "`'subset'`. The order of your checks is the whole question."
    ),
    hint=(
        "`<` and `>` on sets mean *proper* subset and superset, not size. Equality "
        "and disjointness both compete with the others on the empty-set cases — so "
        "which test has to come first?"
    ),
    solution=(
        "def relation(a, b):\n"
        "    if a == b:\n"
        '        return "equal"\n'
        "    if a < b:\n"
        '        return "subset"\n'
        "    if a > b:\n"
        '        return "superset"\n'
        "    if a.isdisjoint(b):\n"
        '        return "disjoint"\n'
        '    return "overlap"'
    ),
    explanation=(
        "Comparison operators on sets test containment, not size, so `{1} < {1, 2}` "
        "is `True` while `{1} < {2}` is `False` — sets are only *partially* ordered, "
        "and that is why `not (a < b)` does not imply `a >= b`. The empty set is "
        "disjoint from everything and a subset of everything, so the checks must run "
        "most-specific-first or `set()` against `{1}` comes out `'disjoint'`."
    ),
    starter="def relation(a, b):\n    ...",
    cases=[
        Case(expected="equal", args=({1, 2}, {1, 2})),
        Case(expected="subset", args=({1}, {1, 2})),
        Case(expected="superset", args=({1, 2}, {1})),
        Case(expected="disjoint", args=({1}, {2})),
        Case(expected="overlap", args=({1, 2}, {2, 3})),
        Case(expected="equal", args=(set(), set())),
        Case(expected="subset", args=(set(), {1})),
    ],
)

q(
    qid="Q-142",
    level=Level.L3,
    topic="Dicts",
    kind="function",
    entry="dig",
    prompt=(
        "Write `dig(data, path, fallback)` that walks a nested structure: `path` is "
        "a list of keys to follow one level at a time.\n\n"
        "`dig({\"a\": {\"b\": 1}}, [\"a\", \"b\"], 0)` returns `1`. Return "
        "`fallback` when any step is missing **or** when a step lands on something "
        "that is not a dict. An empty `path` returns `data` itself. It must never "
        "raise."
    ),
    hint=(
        "Keep a 'current' value and reassign it once per key. Two things can go "
        "wrong at each step, and one of them is not about the key at all — check the "
        "type of what you are about to index."
    ),
    solution=(
        "def dig(data, path, fallback):\n"
        "    current = data\n"
        "    for key in path:\n"
        "        if not isinstance(current, dict) or key not in current:\n"
        "            return fallback\n"
        "        current = current[key]\n"
        "    return current"
    ),
    explanation=(
        "Chained `.get()` calls break the moment an intermediate value is missing, "
        "because `None.get` is an `AttributeError` — the type check is what makes "
        "the walk total. This helper is the readable alternative to a wall of "
        "`if \"a\" in data and \"b\" in data[\"a\"]`, and the same shape handles JSON "
        "from any API you do not control."
    ),
    starter="def dig(data, path, fallback):\n    ...",
    cases=[
        Case(expected=1, args=({"a": {"b": 1}}, ["a", "b"], 0)),
        Case(expected=0, args=({"a": {"b": 1}}, ["a", "z"], 0)),
        Case(expected=0, args=({"a": 1}, ["a", "b"], 0)),
        Case(expected={"b": 1}, args=({"a": {"b": 1}}, ["a"], 0)),
        Case(expected={"a": 1}, args=({"a": 1}, [], 0)),
        Case(expected=None, args=({}, ["a"], None)),
    ],
)

q(
    qid="Q-143",
    level=Level.L3,
    topic="Dict Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        'd = {"a": 1}\n'
        "keys = d.keys()\n"
        'd["b"] = 2\n'
        "print(list(keys))\n"
        "print(len(keys))\n"
        'print("a" in keys)\n'
        "```\n\n"
        "Set `answer` to the three printed lines. `keys` was taken *before* the "
        "insertion — that is the point."
    ),
    hint=(
        "`.keys()` is not a snapshot and not a list; it is a window onto the dict "
        "itself. Ask what a window shows after the thing behind it changes."
    ),
    solution='answer = "[\'a\', \'b\']\\n2\\nTrue"',
    explanation=(
        "`.keys()`, `.values()` and `.items()` return **live views**: they hold no "
        "data, so they reflect every later change to the dict and cost nothing to "
        "create. That is usually what you want, but it is why you must take "
        "`list(d.keys())` before a loop that mutates `d` (Q-136) — and views support "
        "set operations, so `d.keys() & other` works directly."
    ),
    starter="answer = ...",
    cases=[Case(expected="['a', 'b']\n2\nTrue")],
)

# ---------------------------------------------------------------- L4 ----

q(
    qid="Q-144",
    level=Level.L4,
    topic="Set Algebra",
    kind="custom",
    entry="split_skus",
    constraints=["no-loops", "max-lines:2"],
    prompt=(
        "Write `split_skus(a, b)` that returns the 3-tuple "
        "`(only_a, both, only_b)` — three **sets** partitioning the union of `a` and "
        "`b`.\n\n"
        "Every element of `a | b` must land in exactly one of the three. No loops, "
        "no comprehensions, no `if`: use set operators only, in a body of at most 2 "
        "lines."
    ),
    hint=(
        "Three of the four set operators, one per component. Each one is a single "
        "expression over the two arguments — nothing needs to be built up element by "
        "element."
    ),
    solution="def split_skus(a, b):\n    return (a - b, a & b, b - a)",
    explanation=(
        "Set operators do in one character what a loop with three branches does in "
        "ten lines, and they are implemented in C over the hash tables, so they are "
        "faster as well as shorter. The three parts are disjoint and their union is "
        "`a | b` — this is the standard 'what changed between two snapshots' "
        "decomposition."
    ),
    starter="def split_skus(a, b):\n    ...",
    cases=[
        Case(expected=({"p1"}, {"p2"}, {"p3"}), args=({"p1", "p2"}, {"p2", "p3"})),
        Case(expected=(set(), {"p1"}, set()), args=({"p1"}, {"p1"})),
        Case(expected=({"p1"}, set(), {"p9"}), args=({"p1"}, {"p9"})),
        Case(expected=(set(), set(), set()), args=(set(), set())),
        Case(expected=({"p1"}, set(), set()), args=({"p1"}, set())),
    ],
)

q(
    qid="Q-145",
    level=Level.L4,
    topic="Dict Methods",
    kind="custom",
    entry="merge_all",
    constraints=["needs-comprehension", "max-lines:2"],
    prompt=(
        "Write `merge_all(dicts)` that merges a list of dicts into one new dict, "
        "with later dicts winning on shared keys.\n\n"
        "`merge_all([{\"a\": 1}, {\"a\": 2, \"b\": 3}])` returns `{'a': 2, 'b': 3}`. "
        "An empty list gives `{}`. Write it as a single dict comprehension with two "
        "`for` clauses — no `update`, no loop statement."
    ),
    hint=(
        "A comprehension may chain `for` clauses, and they nest left to right like "
        "the loops they replace: the outer one walks the list, the inner one walks "
        "one dict's entries. Later writes to the same key simply overwrite."
    ),
    solution="def merge_all(dicts):\n    return {k: v for d in dicts for k, v in d.items()}",
    explanation=(
        "Chained `for` clauses read in the same order as the nested loops they stand "
        "for — the common error is writing them backwards, which raises `NameError` "
        "because the inner clause uses a name the outer one has not bound yet. "
        "'Later wins' is not a rule you implement here; it falls out of assigning to "
        "the same key twice."
    ),
    starter="def merge_all(dicts):\n    ...",
    cases=[
        Case(expected={"a": 2, "b": 3}, args=([{"a": 1}, {"a": 2, "b": 3}],)),
        Case(expected={}, args=([],)),
        Case(expected={"a": 1}, args=([{"a": 1}],)),
        Case(expected={}, args=([{}, {}],)),
        Case(expected={"a": 1, "b": 2, "c": 3}, args=([{"a": 1}, {"b": 2}, {"c": 3}],)),
    ],
)

q(
    qid="Q-146",
    level=Level.L4,
    topic="Dict Methods",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "calls = []\n\n\n"
        "def fresh():\n"
        "    calls.append(1)\n"
        "    return []\n\n\n"
        'd = {"a": [1]}\n'
        'd.setdefault("a", fresh()).append(2)\n'
        'd.setdefault("b", fresh()).append(3)\n'
        "print(d)\n"
        "print(len(calls))\n"
        "```\n\n"
        "Set `answer` to the two printed lines. The second one is the trap."
    ),
    hint=(
        "`setdefault` is a method call, not a lazy construct — think about when its "
        "arguments are evaluated relative to the lookup that decides whether the "
        "default is needed."
    ),
    solution="answer = \"{'a': [1, 2], 'b': [3]}\\n2\"",
    explanation=(
        "Python evaluates arguments **before** the call, so the default is built "
        "every time even when the key already exists — `fresh()` runs twice and the "
        "first list it made is discarded. Harmless for a literal `[]`, but a real "
        "bug when the default is expensive or has a side effect; "
        "`collections.defaultdict` defers construction to the miss."
    ),
    starter="answer = ...",
    cases=[Case(expected="{'a': [1, 2], 'b': [3]}\n2")],
)

q(
    qid="Q-147",
    level=Level.L4,
    topic="Iteration",
    kind="function",
    entry="invert_multi",
    prompt=(
        "Write `invert_multi(d)` that inverts a dict **without losing data**: return "
        "a dict mapping each value to the **sorted list** of all keys that held it.\n\n"
        "`invert_multi({\"a\": 1, \"b\": 1, \"c\": 2})` returns "
        "`{1: ['a', 'b'], 2: ['c']}`. Every value in the result is a list, even a "
        "one-element one. Assume keys are sortable among themselves."
    ),
    hint=(
        "This is Q-137 with the collision handled instead of ignored: group first, "
        "sort afterwards. `setdefault` gives you the list to append to."
    ),
    solution=(
        "def invert_multi(d):\n"
        "    groups = {}\n"
        "    for key, value in d.items():\n"
        "        groups.setdefault(value, []).append(key)\n"
        "    return {value: sorted(keys) for value, keys in groups.items()}"
    ),
    explanation=(
        "The plain inversion of Q-137 silently drops every key but the last for a "
        "repeated value; collecting into lists is the lossless version, and it is "
        "what building an index always looks like. Sorting at the end rather than "
        "inserting in order keeps the grouping pass linear, and makes the output "
        "deterministic regardless of the input dict's order."
    ),
    starter="def invert_multi(d):\n    ...",
    cases=[
        Case(expected={1: ["a", "b"], 2: ["c"]}, args=({"a": 1, "b": 1, "c": 2},)),
        Case(expected={}, args=({},)),
        Case(expected={1: ["solo"]}, args=({"solo": 1},)),
        Case(expected={0: ["a", "b", "c"]}, args=({"c": 0, "a": 0, "b": 0},)),
        Case(expected={"x": [1], "y": [2]}, args=({1: "x", 2: "y"},)),
    ],
)

q(
    qid="Q-148",
    level=Level.L4,
    topic="Hashability",
    kind="custom",
    entry="dedupe_records",
    constraints=["no-builtin:sorted", "max-lines:8"],
    prompt=(
        "Write `dedupe_records(records)` where `records` is a list of flat dicts. "
        "Return a **list** holding the first occurrence of each distinct record, in "
        "the order they first appear.\n\n"
        "Two records are the same when they have the same entries, whatever order "
        "the keys were written in. Dicts are unhashable, so you need a hashable "
        "stand-in for each one — and you may not build it with `sorted`."
    ),
    hint=(
        "You need a 'have I seen this?' container with fast membership, holding one "
        "immutable summary per record. The set type that can hold a collection of "
        "pairs regardless of their order is the one from Q-132."
    ),
    solution=(
        "def dedupe_records(records):\n"
        "    seen = set()\n"
        "    out = []\n"
        "    for record in records:\n"
        "        key = frozenset(record.items())\n"
        "        if key not in seen:\n"
        "            seen.add(key)\n"
        "            out.append(record)\n"
        "    return out"
    ),
    explanation=(
        "`frozenset(record.items())` is a canonical, hashable fingerprint: order "
        "vanishes, so two dicts written differently collapse to the same key. The "
        "`seen`-set pattern is what keeps this linear — scanning `out` with `in` "
        "instead would be quadratic, and would fail anyway since dicts compare by "
        "value but cannot be hashed. It needs values that are themselves hashable, "
        "so nested lists rule it out."
    ),
    starter="def dedupe_records(records):\n    ...",
    cases=[
        Case(
            expected=[{"a": 1, "b": 2}, {"a": 3}],
            args=([{"a": 1, "b": 2}, {"b": 2, "a": 1}, {"a": 3}],),
        ),
        Case(expected=[], args=([],)),
        Case(expected=[{"a": 1}], args=([{"a": 1}],)),
        Case(expected=[{}], args=([{}, {}],)),
        Case(expected=[{"a": 1}, {"a": 2}], args=([{"a": 1}, {"a": 2}],)),
    ],
)

# ---------------------------------------------------------------- L5 ----

q(
    qid="Q-149",
    level=Level.L5,
    topic="Dicts",
    kind="custom",
    entry="deep_merge",
    constraints=["needs-recursion", "max-lines:10"],
    prompt=(
        "Write `deep_merge(base, override)` that merges two nested dicts into a new "
        "one.\n\n"
        "When a key holds a dict in **both**, merge those two dicts the same way, all "
        "the way down. Otherwise `override`'s value wins whole — a dict replacing a "
        "number, or a number replacing a dict, is just a replacement. Neither "
        "argument may be modified at any depth, and nested dicts that came only from "
        "`base` must not be shared with the result.\n\n"
        "The function must call itself."
    ),
    hint=(
        "Start from a shallow copy of `base`, then walk `override`'s entries. For "
        "each one there are exactly two outcomes, and only one of them recurses — "
        "the condition is a type test on *both* sides."
    ),
    solution=(
        "def deep_merge(base, override):\n"
        "    out = dict(base)\n"
        "    for key, value in override.items():\n"
        "        old = out.get(key)\n"
        "        if isinstance(old, dict) and isinstance(value, dict):\n"
        "            out[key] = deep_merge(old, value)\n"
        "        else:\n"
        "            out[key] = value\n"
        "    return out"
    ),
    explanation=(
        "`dict(base)` is a **shallow** copy: the nested dicts are still shared, so "
        "writing into one would reach back into the caller's data — recursing returns "
        "a fresh dict at every merged level and closes that hole. This is how config "
        "layering (defaults, then environment, then flags) is implemented, and the "
        "bug to watch for is treating 'both are dicts' as 'either is a dict', which "
        "makes a scalar override silently vanish."
    ),
    starter="def deep_merge(base, override):\n    ...",
    cases=[
        Case(
            expected={"db": {"host": "prod", "port": 5432}, "debug": False},
            args=({"db": {"host": "dev", "port": 5432}, "debug": False}, {"db": {"host": "prod"}}),
        ),
        Case(expected={"a": 1, "b": 2}, args=({"a": 1}, {"b": 2})),
        Case(expected={"a": {"b": 1}}, args=({"a": 2}, {"a": {"b": 1}})),
        Case(expected={"a": 2}, args=({"a": {"b": 1}}, {"a": 2})),
        Case(expected={}, args=({}, {})),
        Case(
            expected={"x": {"y": {"z": 2, "w": 1}}},
            args=({"x": {"y": {"z": 1, "w": 1}}}, {"x": {"y": {"z": 2}}}),
        ),
    ],
)

q(
    qid="Q-150",
    level=Level.L5,
    topic="Iteration",
    kind="custom",
    entry="top_n",
    constraints=["no-builtin:Counter", "max-lines:8"],
    prompt=(
        "Write `top_n(items, n)` that returns the `n` most common entries of the "
        "list `items` as a **list of `(item, count)` tuples**, most common first.\n\n"
        "Ties are broken by first appearance in `items`: for "
        "`[\"b\", \"a\", \"a\", \"b\", \"c\"]` with `n=2` the answer is "
        "`[('b', 2), ('a', 2)]`. If `n` exceeds the number of distinct items, return "
        "them all. Build the counts yourself — no `collections.Counter`, and no "
        "`most_common`.\n\n"
        "Do not track the first-appearance position explicitly; two guarantees "
        "already give it to you."
    ),
    hint=(
        "Count into a dict in one pass, then sort by count descending. Two "
        "properties conspire to settle the ties for free: what order a dict's "
        "entries come out in, and what Python's sort does to items whose keys "
        "compare equal."
    ),
    solution=(
        "def top_n(items, n):\n"
        "    counts = {}\n"
        "    for item in items:\n"
        "        counts[item] = counts.get(item, 0) + 1\n"
        "    ranked = sorted(counts.items(), key=lambda kv: -kv[1])\n"
        "    return ranked[:n]"
    ),
    explanation=(
        "The dict yields its entries in first-insertion order, and `sorted` is "
        "**stable** — it never reorders items whose keys compare equal — so items "
        "with the same count keep the order they were first seen in, with no "
        "tie-break field at all. Sorting by `-count` rather than `reverse=True` "
        "matters: `reverse=True` would flip the equal-count runs and break the "
        "required tie order."
    ),
    starter="def top_n(items, n):\n    ...",
    cases=[
        Case(expected=[("b", 2), ("a", 2)], args=(["b", "a", "a", "b", "c"], 2)),
        Case(expected=[("a", 3), ("b", 2), ("c", 1)], args=(["a", "b", "a", "c", "b", "a"], 5)),
        Case(expected=[], args=([], 3)),
        Case(expected=[], args=(["a"], 0)),
        Case(expected=[("x", 1)], args=(["x"], 1)),
        Case(expected=[("a", 2)], args=(["a", "b", "a"], 1)),
    ],
)

# ------------------------------------------------------------ project ----

PROJECT = Project(
    pid="P-04",
    title="Inventory manager",
    brief=(
        "Build `inventory_report(north, south, threshold)`.\n\n"
        "`north` and `south` are dicts mapping a SKU to the quantity held in that "
        "warehouse. Return a dict:\n\n"
        "```python\n"
        "{\n"
        "    'stock': {'p1': 7, 'p2': 3},   # combined quantity per SKU\n"
        "    'low': ['p2'],                 # SKUs whose total is below threshold, sorted\n"
        "    'both': {'p1'},                # SKUs stocked in both warehouses\n"
        "    'north_only': set(),           # SKUs only in north\n"
        "    'south_only': {'p2'},          # SKUs only in south\n"
        "}\n"
        "```\n\n"
        "Rules: a SKU present in both warehouses has its quantities **added**; "
        "`'low'` is a sorted list of strings while the other three are **sets**; a "
        "SKU listed with a quantity of `0` still counts as stocked in that "
        "warehouse; neither input dict may be modified."
    ),
    hint=(
        "Do the two halves with the right tool for each: a dict pass for the "
        "combined stock, and set algebra over `north.keys()` and `south.keys()` for "
        "the three membership groups — key views support `&` and `-` directly. Keep "
        "`'low'` sorted so the output never depends on set or dict order."
    ),
    solution=(
        "def inventory_report(north, south, threshold):\n"
        "    stock = dict(north)\n"
        "    for sku, qty in south.items():\n"
        "        stock[sku] = stock.get(sku, 0) + qty\n"
        "    north_keys = set(north)\n"
        "    south_keys = set(south)\n"
        "    return {\n"
        "        'stock': stock,\n"
        "        'low': sorted(s for s, q in stock.items() if q < threshold),\n"
        "        'both': north_keys & south_keys,\n"
        "        'north_only': north_keys - south_keys,\n"
        "        'south_only': south_keys - north_keys,\n"
        "    }"
    ),
    explanation=(
        "This is the shape of most reconciliation work: dicts answer 'how much' and "
        "sets answer 'which ones', and mixing the two up is what makes such code "
        "sprawl. Note that membership comes from the keys alone — a SKU stocked at "
        "`0` is still stocked — so the set half must never be derived by filtering on "
        "quantity, and `'low'` is sorted because no ordering may be inherited from a "
        "set."
    ),
    entry="inventory_report",
    starter="def inventory_report(north, south, threshold):\n    ...",
    cases=[
        Case(
            expected={
                "stock": {"p1": 7, "p2": 3},
                "low": ["p2"],
                "both": {"p1"},
                "north_only": set(),
                "south_only": {"p2"},
            },
            args=({"p1": 4}, {"p1": 3, "p2": 3}, 5),
        ),
        Case(
            expected={
                "stock": {},
                "low": [],
                "both": set(),
                "north_only": set(),
                "south_only": set(),
            },
            args=({}, {}, 5),
        ),
        Case(
            expected={
                "stock": {"p1": 0, "p2": 2},
                "low": ["p1", "p2"],
                "both": {"p1"},
                "north_only": set(),
                "south_only": {"p2"},
            },
            args=({"p1": 0}, {"p1": 0, "p2": 2}, 5),
        ),
        Case(
            expected={
                "stock": {"p1": 4, "p9": 1},
                "low": ["p9"],
                "both": set(),
                "north_only": {"p1"},
                "south_only": {"p9"},
            },
            args=({"p1": 4}, {"p9": 1}, 2),
        ),
    ],
)

NOTEBOOK = Notebook(
    number=4,
    slug="dicts_and_sets",
    title="Dicts & Sets",
    intro=(
        "The two hash-backed containers: dicts for mapping keys to values, sets for "
        "asking whether something is there. Creation, lookup with and without a "
        "default, mutation, iteration over keys/values/items, nesting, and the four "
        "set operators.\n\n"
        "Both types are built on hashing, which is where the surprises come from — "
        "`True` and `1` are the same key, `{}` is not an empty set, and a set has no "
        "order you may rely on. Get these right and half of everyday Python is "
        "already written."
    ),
    questions=QUESTIONS,
    project=PROJECT,
)
