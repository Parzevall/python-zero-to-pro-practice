import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB29", title="Performance & Memory", intro="""
    Measure first, then optimise. You will time code with `timeit` and
    `perf_counter`, profile it with `cProfile`, choose containers by their
    real cost, save memory with generators, `__slots__` and `array`, and see
    how Python frees objects (reference counting, the cycle collector and
    `weakref`). Timings differ on every machine, so the tasks print counts,
    results and yes/no comparisons with a huge margin instead of raw times.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", """
    `timeit.timeit(func, number=N)` runs `func` exactly `N` times. Prove it:
    time a lambda that appends `1` to the list `calls` 500 times, then print
    how many items `calls` holds.
""",
     given="calls = []",
     solution="import timeit\n"
              "timeit.timeit(lambda: calls.append(1), number=500)\n"
              "print(len(calls))")

nb.q("Real-life", """
    A mailing list has 100,000 subscriber numbers, stored both as a list and
    as a set. Use `timeit` (200 runs each, passing `globals=globals()`) to
    time the check `99_999 in ...` on both. Print `True` if the list version
    took more than 50 times longer than the set version.
""",
     given="numbers = list(range(100_000))\nnumber_set = set(numbers)",
     solution="import timeit\n"
              'list_time = timeit.timeit("99_999 in numbers", globals=globals(), number=200)\n'
              'set_time = timeit.timeit("99_999 in number_set", globals=globals(), number=200)\n'
              'print("Set at least 50x faster:", list_time > set_time * 50)')

nb.q("Puzzle", """
    `sys.getsizeof` only measures the container itself, not what it points to.
    Print `True` if `light` and `heavy` report the same size, then print the
    total number of numbers stored inside `heavy`.
""",
     given="light = [None, None]\nheavy = [list(range(1000)), list(range(1000))]",
     solution="import sys\n"
              "print(sys.getsizeof(light) == sys.getsizeof(heavy))\n"
              "print(len(heavy[0]) + len(heavy[1]))")

nb.q("Real-life", """
    Cache a slow recursive `fib(n)` with `functools.cache`. Print `fib(30)`,
    then print the cache statistics line (`cache_info()`).
""",
     solution="from functools import cache\n\n"
              "@cache\n"
              "def fib(n):\n"
              "    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n"
              "print(fib(30))\n"
              "print(fib.cache_info())")

nb.q("Build", """
    A `Session` object is created and a weak reference `ref` to it is made
    with `weakref.ref`. Print whether `ref()` is the session, delete the
    only normal reference, then print what `ref()` returns now.
""",
     given="class Session:\n    pass\n\nsession = Session()",
     solution="import weakref\n"
              "ref = weakref.ref(session)\n"
              "print(ref() is session)\n"
              "del session\n"
              "print(ref())")

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    A report needs the squares of the first 100,000 numbers, once as a list
    comprehension and once as a generator expression. Print `True` if the
    generator object is more than 100 times smaller than the list (use
    `sys.getsizeof`), and `True` if both give the same `sum`.
""",
     solution="import sys\n"
              "squares_list = [n * n for n in range(100_000)]\n"
              "squares_gen = (n * n for n in range(100_000))\n"
              "print(sys.getsizeof(squares_gen) * 100 < sys.getsizeof(squares_list))\n"
              "print(sum(squares_list) == sum(squares_gen))")

nb.q("Output-match", """
    A `Resource` prints `closed` the moment it is destroyed. Two names point
    at the same one. Delete `first` and print `still alive`, then delete
    `second` and print `done`. Python frees the object as soon as its last
    reference disappears.
""",
     given='class Resource:\n    def __del__(self):\n        print("closed")\n\nfirst = Resource()\nsecond = first',
     solution='del first\nprint("still alive")\ndel second\nprint("done")')

nb.q("Build", """
    Write a class `Point` that uses `__slots__ = ("x", "y")` and takes `x`
    and `y` in `__init__`. Print whether a `Point` has a `__dict__`, then
    try to set `p.z = 3` and print `no new attributes` when that fails.
""",
     solution="class Point:\n"
              '    __slots__ = ("x", "y")\n\n'
              "    def __init__(self, x, y):\n"
              "        self.x = x\n"
              "        self.y = y\n\n"
              "p = Point(1, 2)\n"
              'print(hasattr(p, "__dict__"))\n'
              "try:\n"
              "    p.z = 3\n"
              "except AttributeError:\n"
              '    print("no new attributes")')

nb.q("Puzzle", """
    Store the sensor readings (all between 0 and 65535) in an `array` with
    typecode `"H"`. Print the bytes per item, the number of items, and the
    total bytes (items times item size). Then try to append `70000`, which
    does not fit, and print `too big` when that fails.
""",
     given="readings = [n % 1000 for n in range(100_000)]",
     solution="from array import array\n"
              'packed = array("H", readings)\n'
              "print(packed.itemsize, len(packed), packed.itemsize * len(packed))\n"
              "try:\n"
              "    packed.append(70000)\n"
              "except OverflowError:\n"
              '    print("too big")')

nb.q("Output-match", """
    Build one text line from the integers in `temps` separated by `, `
    using `join` (not repeated `+=`), print it, then print its length.
""",
     given="temps = [12, 15, 11, 19, 14]",
     solution='line = ", ".join(str(t) for t in temps)\nprint(line)\nprint(len(line))')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Write `has_duplicate_slow(items)` using two nested loops over positions
    and `has_duplicate_fast(items)` using a set. Time one call of each on
    `ids` with `timeit.timeit(lambda: ..., number=1)`. Print both results
    and then `True` if the fast version is at least 10 times faster.
""",
     given="ids = list(range(3000)) + [1500]",
     solution="import timeit\n\n"
              "def has_duplicate_slow(items):\n"
              "    for i in range(len(items)):\n"
              "        for j in range(i + 1, len(items)):\n"
              "            if items[i] == items[j]:\n"
              "                return True\n"
              "    return False\n\n"
              "def has_duplicate_fast(items):\n"
              "    return len(set(items)) < len(items)\n\n"
              "slow_time = timeit.timeit(lambda: has_duplicate_slow(ids), number=1)\n"
              "fast_time = timeit.timeit(lambda: has_duplicate_fast(ids), number=1)\n"
              "print(has_duplicate_slow(ids), has_duplicate_fast(ids))\n"
              'print("Fast at least 10x faster:", slow_time > fast_time * 10)')

nb.q("Real-life", """
    Profile `fib(20)` with `cProfile.Profile().runcall(...)`. Wrap the
    profiler in `pstats.Stats` and loop over `stats.stats.items()`: each key
    is `(file, line, name)` and each value starts with `(primitive_calls,
    total_calls, ...)`. Print how many times `fib` was called in total.
""",
     given="def fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)",
     solution="import cProfile\nimport pstats\n\n"
              "profiler = cProfile.Profile()\n"
              "profiler.runcall(fib, 20)\n"
              "stats = pstats.Stats(profiler)\n"
              "for (filename, line, name), values in stats.stats.items():\n"
              '    if name == "fib":\n'
              '        print("fib calls:", values[1])')

nb.q("Real-life", """
    A job queue is drained from the front. Write `drain_list(items)` using
    `list.pop(0)` and `drain_deque(items)` using a `collections.deque` and
    `popleft()`; both return the items in the order they were taken. Print
    the first three items of the deque result, `True` if both orders are
    equal, and `True` if the deque version is more than 5 times faster.
""",
     given="jobs = list(range(40_000))",
     solution="import timeit\nfrom collections import deque\n\n"
              "def drain_list(items):\n"
              "    pending = list(items)\n"
              "    order = []\n"
              "    while pending:\n"
              "        order.append(pending.pop(0))\n"
              "    return order\n\n"
              "def drain_deque(items):\n"
              "    pending = deque(items)\n"
              "    order = []\n"
              "    while pending:\n"
              "        order.append(pending.popleft())\n"
              "    return order\n\n"
              "list_time = timeit.timeit(lambda: drain_list(jobs), number=1)\n"
              "deque_time = timeit.timeit(lambda: drain_deque(jobs), number=1)\n"
              "print(drain_deque(jobs)[:3])\n"
              "print(drain_list(jobs) == drain_deque(jobs))\n"
              "print(list_time > deque_time * 5)")

nb.q("Real-life", """
    `tax_rate(country)` is a slow lookup, counted in `lookups["count"]`.
    Cache it with `functools.lru_cache(maxsize=None)`, call it for every
    country in `orders`, and print how many real lookups happened, then
    the `hits` and `misses` from `cache_info()`. Finally clear the cache
    and print its `currsize`.
""",
     given='RATES = {"DE": 0.19, "FR": 0.20, "ES": 0.21}\n'
           'lookups = {"count": 0}\n'
           'orders = ["DE", "FR", "DE", "DE", "FR", "ES", "DE"]\n\n'
           "def tax_rate(country):\n"
           '    lookups["count"] += 1\n'
           "    return RATES[country]",
     solution="from functools import lru_cache\n\n"
              "tax_rate = lru_cache(maxsize=None)(tax_rate)\n"
              "for country in orders:\n"
              "    tax_rate(country)\n"
              'print("Real lookups:", lookups["count"])\n'
              "info = tax_rate.cache_info()\n"
              'print("Hits:", info.hits, "Misses:", info.misses)\n'
              "tax_rate.cache_clear()\n"
              'print("Size after clear:", tax_rate.cache_info().currsize)')

nb.q("Real-life", """
    Image loading is expensive, so `load(name)` should reuse an image that
    is still in use but must not keep unused ones alive. Back it with a
    `weakref.WeakValueDictionary` named `cache` and record every real
    creation in `created`. Load `"logo"` twice, print whether both are the
    same object and how many were created. Delete both names and print the
    cache size. Load `"logo"` once more and print how many were created.
""",
     given="class Image:\n    def __init__(self, name):\n        self.name = name\n\ncreated = []",
     solution="import weakref\n\n"
              "cache = weakref.WeakValueDictionary()\n\n"
              "def load(name):\n"
              "    image = cache.get(name)\n"
              "    if image is None:\n"
              "        image = Image(name)\n"
              "        created.append(name)\n"
              "        cache[name] = image\n"
              "    return image\n\n"
              'a = load("logo")\n'
              'b = load("logo")\n'
              "print(a is b, len(created))\n"
              "del a, b\n"
              "print(len(cache))\n"
              'load("logo")\n'
              "print(len(created))")

# ------------------------------------------------------------ Puzzles & builds
nb.q("Build", """
    Write a `Timer` class that works in a `with` block: `__enter__` stores
    `time.perf_counter()` and returns the timer, `__exit__` stores
    `self.elapsed`. Use it to time `fib(27)` (plain) and `fib_cached(27)`
    (with `functools.cache`). Print `True` if the results are equal and
    `True` if the cached run was more than 100 times faster.
""",
     given="def fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)",
     solution="import time\nfrom functools import cache\n\n"
              "class Timer:\n"
              "    def __enter__(self):\n"
              "        self.start = time.perf_counter()\n"
              "        return self\n\n"
              "    def __exit__(self, *exc_info):\n"
              "        self.elapsed = time.perf_counter() - self.start\n\n"
              "@cache\n"
              "def fib_cached(n):\n"
              "    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)\n\n"
              "with Timer() as slow:\n"
              "    result_slow = fib(27)\n"
              "with Timer() as fast:\n"
              "    result_fast = fib_cached(27)\n"
              "print(result_slow == result_fast)\n"
              "print(slow.elapsed > fast.elapsed * 100)")

nb.q("Real-life", """
    Count the `ERROR` lines of a log file with 50,000 lines in two ways:
    `count_errors_list(path)` reads everything with `readlines()`,
    `count_errors_stream(path)` loops over the open file line by line. Write
    the log into a temporary directory (every 10th line is an `ERROR`).
    Measure each function's peak memory with `tracemalloc` and print both
    counts, then `True` if the streaming peak times 20 is still smaller than
    the list peak.
""",
     solution="import os\nimport tempfile\nimport tracemalloc\n\n"
              "def count_errors_list(path):\n"
              "    with open(path) as f:\n"
              "        lines = f.readlines()\n"
              '    return sum(1 for line in lines if " ERROR " in line)\n\n'
              "def count_errors_stream(path):\n"
              "    with open(path) as f:\n"
              '        return sum(1 for line in f if " ERROR " in line)\n\n'
              "def peak_of(func, path):\n"
              "    tracemalloc.start()\n"
              "    result = func(path)\n"
              "    peak = tracemalloc.get_traced_memory()[1]\n"
              "    tracemalloc.stop()\n"
              "    return result, peak\n\n"
              "with tempfile.TemporaryDirectory() as folder:\n"
              '    path = os.path.join(folder, "server.log")\n'
              '    with open(path, "w") as f:\n'
              "        for i in range(50_000):\n"
              '            level = "ERROR" if i % 10 == 0 else "INFO"\n'
              '            f.write(f"2024-05-01 12:00:00 {level} request {i} finished\\n")\n'
              "    list_count, list_peak = peak_of(count_errors_list, path)\n"
              "    stream_count, stream_peak = peak_of(count_errors_stream, path)\n"
              "print(list_count, stream_count)\n"
              "print(stream_peak * 20 < list_peak)")

nb.q("Puzzle", """
    A lying benchmark: `slow_square` is cached, so timing it 1000 times
    only measures the cache. Time `slow_square(12)` 1000 times with
    `timeit` and print `Naive calls:` and the number of real calls. Reset
    the counter, then time an honest version (a function that calls
    `slow_square.cache_clear()` first, then `slow_square(12)`), also 1000
    times, and print `Honest calls:` and the count.
""",
     given='from functools import lru_cache\n\ncalls = {"n": 0}\n\n'
           "@lru_cache(maxsize=None)\n"
           "def slow_square(n):\n"
           '    calls["n"] += 1\n'
           "    return n * n",
     solution="import timeit\n\n"
              "timeit.timeit(lambda: slow_square(12), number=1000)\n"
              'print("Naive calls:", calls["n"])\n\n'
              'calls["n"] = 0\n\n'
              "def honest():\n"
              "    slow_square.cache_clear()\n"
              "    return slow_square(12)\n\n"
              "timeit.timeit(honest, number=1000)\n"
              'print("Honest calls:", calls["n"])')

nb.q("Puzzle", """
    Reference cycles need the garbage collector. Each `Node` adds to
    `freed["n"]` when destroyed. Write `build_cyclic(n)`: a root with `n`
    children, each child pointing back with `child.parent = root`; and
    `build_weak(n)`, the same but `child.parent = weakref.ref(root)`.
    With `gc.disable()` at the top: build and delete a cyclic tree of 1000
    children and print `freed["n"]`; call `gc.collect()` and print it again.
    Then reset the counter, build and delete a weak tree of 1000 children
    and print `freed["n"]` without collecting.
""",
     given='freed = {"n": 0}\n\n'
           "class Node:\n"
           "    def __init__(self):\n"
           "        self.parent = None\n"
           "        self.children = []\n\n"
           "    def __del__(self):\n"
           '        freed["n"] += 1',
     solution="import gc\nimport weakref\n\n"
              "gc.disable()\n\n"
              "def build_cyclic(n):\n"
              "    root = Node()\n"
              "    for _ in range(n):\n"
              "        child = Node()\n"
              "        child.parent = root\n"
              "        root.children.append(child)\n"
              "    return root\n\n"
              "def build_weak(n):\n"
              "    root = Node()\n"
              "    for _ in range(n):\n"
              "        child = Node()\n"
              "        child.parent = weakref.ref(root)\n"
              "        root.children.append(child)\n"
              "    return root\n\n"
              "tree = build_cyclic(1000)\n"
              "del tree\n"
              'print(freed["n"])\n'
              "gc.collect()\n"
              'print(freed["n"])\n'
              'freed["n"] = 0\n'
              "tree = build_weak(1000)\n"
              "del tree\n"
              'print(freed["n"])')

# ------------------------------------------------------------ Q20 story project
nb.project("Speed Up the Monday Report", story="""
    Every Monday the shop's sales report takes forever. You inherit the
    script: a list of `(customer_id, amount)` orders and a list of VIP
    customer ids. Do not guess: **measure, change one thing, measure again.**
    Each step builds on the variables and functions of the step before.
""",
     given="import timeit\n\n"
           "vip_ids = list(range(0, 3000, 7))\n"
           "orders = [(i * 37 % 3000, 5 + (i * 13 % 90)) for i in range(20_000)]\n"
           'calls = {"discount": 0}',
     steps=[
         ("Write `vip_total_slow(orders, vip_ids)` that adds up the amounts of "
          "all orders whose customer is in the **list** `vip_ids`. Print the "
          "number of orders and the VIP total.",
          "def vip_total_slow(orders, vip_ids):\n"
          "    total = 0\n"
          "    for customer_id, amount in orders:\n"
          "        if customer_id in vip_ids:\n"
          "            total += amount\n"
          "    return total\n\n"
          'print("Orders:", len(orders))\n'
          'print("VIP total:", vip_total_slow(orders, vip_ids))'),
         ("Write `vip_total_fast` that gives the same answer using a set. Time "
          "one call of each with `timeit.timeit(..., number=1)`. Print `True` if "
          "the totals are equal and `True` if the fast one is at least 10 times "
          "faster.",
          "def vip_total_fast(orders, vip_ids):\n"
          "    vip_set = set(vip_ids)\n"
          "    return sum(amount for customer_id, amount in orders if customer_id in vip_set)\n\n"
          "slow_time = timeit.timeit(lambda: vip_total_slow(orders, vip_ids), number=1)\n"
          "fast_time = timeit.timeit(lambda: vip_total_fast(orders, vip_ids), number=1)\n"
          "print(vip_total_slow(orders, vip_ids) == vip_total_fast(orders, vip_ids))\n"
          "print(fast_time * 10 < slow_time)"),
         ("Each order gets a discount from `discount_for(amount)`, which is slow "
          "and counted in `calls[\"discount\"]`. Cache it with `functools.lru_cache`, "
          "compute the discount of every order amount, and print the real calls, "
          "then the total discount rounded to 2 decimals.",
          "from functools import lru_cache\n\n"
          "def discount_for(amount):\n"
          '    calls["discount"] += 1\n'
          "    return amount * 0.05 if amount >= 50 else 0\n\n"
          "discount_for = lru_cache(maxsize=None)(discount_for)\n"
          "total_discount = sum(discount_for(amount) for customer_id, amount in orders)\n"
          'print("Real calls:", calls["discount"])\n'
          'print("Total discount:", round(total_discount, 2))'),
         ("Build the report text: one line per order like `order 0: customer 0, "
          "amount 5` as a **list** of lines, then join them with newlines. Print "
          "the number of lines, the first line and the text length.",
          "lines = [f\"order {i}: customer {cid}, amount {amount}\" for i, (cid, amount) in enumerate(orders)]\n"
          'report = "\\n".join(lines)\n'
          'print("Lines:", len(lines))\n'
          "print(lines[0])\n"
          'print("Length:", len(report))'),
         ("Memory check: write `report_lines(orders)` as a generator that yields "
          "the same lines one at a time. With `tracemalloc`, measure the peak of "
          "building the full list of lines versus counting the lines from the "
          "generator. Print `True` if the counts are equal and `True` if the "
          "generator peak times 10 is smaller than the list peak.",
          "import tracemalloc\n\n"
          "def report_lines(orders):\n"
          "    for i, (cid, amount) in enumerate(orders):\n"
          '        yield f"order {i}: customer {cid}, amount {amount}"\n\n'
          "def peak_of(func):\n"
          "    tracemalloc.start()\n"
          "    result = func()\n"
          "    peak = tracemalloc.get_traced_memory()[1]\n"
          "    tracemalloc.stop()\n"
          "    return result, peak\n\n"
          "list_count, list_peak = peak_of(lambda: len(list(report_lines(orders))))\n"
          "stream_count, stream_peak = peak_of(lambda: sum(1 for line in report_lines(orders)))\n"
          "print(list_count == stream_count)\n"
          "print(stream_peak * 10 < list_peak)"),
     ])

nb.build()
