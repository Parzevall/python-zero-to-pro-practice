import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB24", title="Context Managers", intro="""
    The `with` statement is how Python promises "this gets cleaned up, no
    matter what". Here you look under the hood: write your own managers with
    `__enter__` / `__exit__` and with `@contextmanager`, decide what happens
    to exceptions, and use `contextlib` helpers. Files, timers, settings and
    a tiny database transaction are the examples.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", """
    `path` is a notes file. Read it with a `with` block and print its first
    line, then print whether the file object is closed once the block has ended.
""",
     given='import os, tempfile\n'
           'folder = tempfile.TemporaryDirectory()\n'
           'path = os.path.join(folder.name, "notes.txt")\n'
           'with open(path, "w") as f:\n'
           '    f.write("buy milk\\ncall Sam\\n")',
     solution='with open(path) as f:\n'
              '    first = f.readline().strip()\n'
              'print(first)\n'
              'print(f.closed)')

nb.q("Real-life", """
    Remove `"coupon"` from the `cart` dict, but the key may not be there.
    Use `contextlib.suppress` so a missing key is ignored, then print the cart.
""",
     given='cart = {"apples": 3, "bread": 1}',
     solution='from contextlib import suppress\n'
              'with suppress(KeyError):\n'
              '    del cart["coupon"]\n'
              'print(cart)')

nb.q("Output-match", """
    The function `noisy()` prints a line. Capture what it prints into a string
    with `redirect_stdout`, then print the captured text in upper case and its
    length (the length includes the newline).
""",
     given='def noisy():\n    print("low disk space")',
     solution='import io\n'
              'from contextlib import redirect_stdout\n'
              'buffer = io.StringIO()\n'
              'with redirect_stdout(buffer):\n'
              '    noisy()\n'
              'text = buffer.getvalue()\n'
              'print(text.upper().strip())\n'
              'print(len(text))')

nb.q("Build", """
    Write a class `Door` with `__enter__` and `__exit__` so that
    `with Door(): print("walking through")` prints `door opens`, then the
    line from inside the block, then `door closes`.
""",
     solution='class Door:\n'
              '    def __enter__(self):\n'
              '        print("door opens")\n'
              '        return self\n'
              '    def __exit__(self, exc_type, exc, tb):\n'
              '        print("door closes")\n'
              '        return False\n'
              '\n'
              'with Door():\n'
              '    print("walking through")')

nb.q("Real-life", """
    `get_title` should work with or without a lock. `lock` is either a real
    context manager or `None`. Use `contextlib.nullcontext` so one `with`
    line handles both cases, and print the title.
""",
     given='from contextlib import nullcontext\n'
           'class Lock:\n'
           '    def __enter__(self):\n        print("locked")\n'
           '    def __exit__(self, *args):\n        print("unlocked")\n\n'
           'lock = None\n'
           'def get_title():\n    return "Dune"',
     solution='manager = lock if lock is not None else nullcontext()\n'
              'with manager:\n'
              '    print(get_title())')

# ------------------------------------------------------- Combine
nb.q("Build", """
    With `@contextmanager`, write `banner(title)`: it prints `== title ==`
    on entering and `== end ==` on leaving. Use it around two prints of your
    choice.
""",
     solution='from contextlib import contextmanager\n'
              '\n'
              '@contextmanager\n'
              'def banner(title):\n'
              '    print("==", title, "==")\n'
              '    yield\n'
              '    print("== end ==")\n'
              '\n'
              'with banner("Report"):\n'
              '    print("sales: 120")\n'
              '    print("returns: 4")')

nb.q("Real-life", """
    Write a `Timer` class (context manager) that stores `elapsed` on itself:
    the clock reading on exit minus the reading on entry. `fake_clock()` plays
    the part of a real clock so the numbers are stable. Time a block and print
    the elapsed seconds.
""",
     given='ticks = iter([10.0, 12.5])\n'
           'def fake_clock():\n    return next(ticks)',
     solution='class Timer:\n'
              '    def __enter__(self):\n'
              '        self.start = fake_clock()\n'
              '        return self\n'
              '    def __exit__(self, exc_type, exc, tb):\n'
              '        self.elapsed = fake_clock() - self.start\n'
              '        return False\n'
              '\n'
              'with Timer() as t:\n'
              '    total = sum(range(1000))\n'
              'print("Elapsed:", t.elapsed)')

nb.q("Puzzle", """
    Write a class `Quiet` whose `__exit__` swallows any exception and
    remembers its type name in `self.seen`. Inside `with Quiet() as q:` raise
    `ValueError("boom")`, then print `survived` and the remembered name. Does
    the line after the raise still run inside the block?
""",
     solution='class Quiet:\n'
              '    def __enter__(self):\n'
              '        self.seen = None\n'
              '        return self\n'
              '    def __exit__(self, exc_type, exc, tb):\n'
              '        self.seen = exc_type.__name__\n'
              '        return True\n'
              '\n'
              'with Quiet() as q:\n'
              '    raise ValueError("boom")\n'
              '    print("never printed")\n'
              'print("survived")\n'
              'print(q.seen)')

nb.q("Real-life", """
    Write `@contextmanager` function `temporarily(settings, key, value)`: it
    sets `settings[key]` to `value` for the duration of the block and puts
    the old value back afterwards. Print the settings inside and after.
""",
     given='settings = {"theme": "light", "font": 12}',
     solution='from contextlib import contextmanager\n'
              '\n'
              '@contextmanager\n'
              'def temporarily(settings, key, value):\n'
              '    old = settings[key]\n'
              '    settings[key] = value\n'
              '    try:\n'
              '        yield settings\n'
              '    finally:\n'
              '        settings[key] = old\n'
              '\n'
              'with temporarily(settings, "theme", "dark"):\n'
              '    print(settings)\n'
              'print(settings)')

nb.q("Real-life", """
    `Connection` has a `close()` method but is not a context manager. Use
    `contextlib.closing` to wrap `Connection("db1")`, print its `name` inside
    the block, and let the block end.
""",
     given='class Connection:\n'
           '    def __init__(self, name):\n        self.name = name\n'
           '    def close(self):\n        print("closing", self.name)',
     solution='from contextlib import closing\n'
              'with closing(Connection("db1")) as conn:\n'
              '    print("using", conn.name)')

# ------------------------------------------------------- Small real tasks
nb.q("Real-life", """
    Write every name in `names` to its own file inside `folder`
    (`<name>.txt`, containing the name). Open all the files at once with
    `ExitStack`, write through them, and after the `with` block print the
    list of `closed` flags, one per file.
""",
     given='import os, tempfile\n'
           'folder = tempfile.TemporaryDirectory()\n'
           'names = ["ada", "grace", "linus"]',
     solution='from contextlib import ExitStack\n'
              'with ExitStack() as stack:\n'
              '    files = [stack.enter_context(open(os.path.join(folder.name, name + ".txt"), "w"))\n'
              '             for name in names]\n'
              '    for name, f in zip(names, files):\n'
              '        f.write(name)\n'
              'print([f.closed for f in files])')

nb.q("Real-life", """
    `read_price(prices, item)` should treat a **missing item** as "no price"
    but must **not** hide real bugs. Use `suppress(KeyError)` inside it, then
    call it once with a known item and once with an unknown item. Finally call
    `read_price(prices, 7)` too: print the name of the error that escapes,
    caught with a normal `try`.
""",
     given='prices = {"tea": 2.5, "cake": 4.0}\n'
           'def lookup(prices, item):\n'
           '    return prices[item.lower()]',
     solution='from contextlib import suppress\n'
              '\n'
              'def read_price(prices, item):\n'
              '    price = None\n'
              '    with suppress(KeyError):\n'
              '        price = lookup(prices, item)\n'
              '    return price\n'
              '\n'
              'print(read_price(prices, "Tea"))\n'
              'print(read_price(prices, "Pizza"))\n'
              'try:\n'
              '    read_price(prices, 7)\n'
              'except AttributeError as e:\n'
              '    print(type(e).__name__)')

nb.q("Real-life", """
    A `Transaction` class: on entering, it prints `begin`; on leaving it
    prints `commit` if all went well or `rollback: <error message>` if an
    exception happened, and in the second case it must **not** swallow the
    exception. Run a failing block (raise `RuntimeError("disk full")`) inside
    a normal `try`, and print `caught` afterwards. Also run a clean block.
""",
     solution='class Transaction:\n'
              '    def __enter__(self):\n'
              '        print("begin")\n'
              '        return self\n'
              '    def __exit__(self, exc_type, exc, tb):\n'
              '        if exc_type is None:\n'
              '            print("commit")\n'
              '        else:\n'
              '            print("rollback:", exc)\n'
              '        return False\n'
              '\n'
              'with Transaction():\n'
              '    print("saving")\n'
              'try:\n'
              '    with Transaction():\n'
              '        raise RuntimeError("disk full")\n'
              'except RuntimeError:\n'
              '    print("caught")')

nb.q("Real-life", """
    `report()` prints a few log lines to the screen. Capture its output with
    `redirect_stdout`, then print how many lines it produced and only the
    lines containing `ERROR`, each prefixed with `> `.
""",
     given='def report():\n'
           '    print("INFO start")\n'
           '    print("ERROR disk")\n'
           '    print("INFO retry")\n'
           '    print("ERROR net")',
     solution='import io\n'
              'from contextlib import redirect_stdout\n'
              'buffer = io.StringIO()\n'
              'with redirect_stdout(buffer):\n'
              '    report()\n'
              'lines = buffer.getvalue().splitlines()\n'
              'print(len(lines), "lines")\n'
              'for line in lines:\n'
              '    if "ERROR" in line:\n'
              '        print("> " + line)')

nb.q("Real-life", """
    Copy `source.txt` to `copy.txt` inside `folder`, changing every line to
    upper case. Open both files in **one** `with` statement using the
    parenthesised multi-item form. Then print the contents of the copy.
""",
     given='import os, tempfile\n'
           'folder = tempfile.TemporaryDirectory()\n'
           'src = os.path.join(folder.name, "source.txt")\n'
           'dst = os.path.join(folder.name, "copy.txt")\n'
           'with open(src, "w") as f:\n'
           '    f.write("alpha\\nbeta\\ngamma\\n")',
     solution='with (\n'
              '    open(src) as reader,\n'
              '    open(dst, "w") as writer,\n'
              '):\n'
              '    for line in reader:\n'
              '        writer.write(line.upper())\n'
              'with open(dst) as f:\n'
              '    print(f.read())')

# ------------------------------------------------------- Puzzles & builds
nb.q("Puzzle", """
    Write class `Tracer(name, log, swallow=False)`: `__enter__` appends
    `"enter <name>"` to `log`; `__exit__` appends `"exit <name>"` and returns
    `swallow`. Run
    `with Tracer("a", log, swallow=True), Tracer("b", log), Tracer("c", log):`
    with a body that appends `"body"` and then raises `ValueError`. Print the
    log, one entry per line, then print `done` (the error must not escape).
""",
     given="log = []",
     solution='class Tracer:\n'
              '    def __init__(self, name, log, swallow=False):\n'
              '        self.name = name\n'
              '        self.log = log\n'
              '        self.swallow = swallow\n'
              '    def __enter__(self):\n'
              '        self.log.append("enter " + self.name)\n'
              '        return self\n'
              '    def __exit__(self, exc_type, exc, tb):\n'
              '        self.log.append("exit " + self.name)\n'
              '        return self.swallow\n'
              '\n'
              'with Tracer("a", log, swallow=True), Tracer("b", log), Tracer("c", log):\n'
              '    log.append("body")\n'
              '    raise ValueError\n'
              'for entry in log:\n'
              '    print(entry)\n'
              'print("done")')

nb.q("Real-life", """
    Write `@contextmanager` `recovering(log)`: if the block raises
    `ValueError`, append `"recovered: <message>"` to `log` and let the program
    carry on; any other error must still escape. Run a block that raises
    `ValueError("bad row")`, a clean block, and a block that raises
    `KeyError("x")` (catch that one with a normal `try`). Print the log and
    which blocks reached the line after them.
""",
     given="log = []",
     solution='from contextlib import contextmanager\n'
              '\n'
              '@contextmanager\n'
              'def recovering(log):\n'
              '    try:\n'
              '        yield\n'
              '    except ValueError as e:\n'
              '        log.append("recovered: " + str(e))\n'
              '\n'
              'with recovering(log):\n'
              '    raise ValueError("bad row")\n'
              'print("after block 1")\n'
              'with recovering(log):\n'
              '    log.append("fine")\n'
              'print("after block 2")\n'
              'try:\n'
              '    with recovering(log):\n'
              '        raise KeyError("x")\n'
              'except KeyError:\n'
              '    print("block 3 escaped")\n'
              'print(log)')

nb.q("Puzzle", """
    `acquire(name)` returns a resource and prints `got <name>`, except for
    `"printer"` which raises `RuntimeError`. Each resource has `release()`
    that prints `released <name>`. Using one `ExitStack` and
    `stack.callback(...)`, acquire `["disk", "network", "printer", "camera"]`
    in order inside a `try`, registering a release right after each success.
    When the error happens, print `failed: <message>` after the cleanups run.
    In which order do the releases happen?
""",
     given='class Resource:\n'
           '    def __init__(self, name):\n        self.name = name\n'
           '    def release(self):\n        print("released", self.name)\n\n'
           'def acquire(name):\n'
           '    if name == "printer":\n'
           '        raise RuntimeError("printer is offline")\n'
           '    print("got", name)\n'
           '    return Resource(name)',
     solution='from contextlib import ExitStack\n'
              'try:\n'
              '    with ExitStack() as stack:\n'
              '        for name in ["disk", "network", "printer", "camera"]:\n'
              '            resource = acquire(name)\n'
              '            stack.callback(resource.release)\n'
              'except RuntimeError as e:\n'
              '    print("failed:", e)')

nb.q("Build", """
    Build a tiny pretty-printer for nested outlines. `indent()` is a
    `@contextmanager` that raises the current depth by one while its block
    runs (keep the depth in a dict or list so the function `say(text)` can
    see it). `say(text)` prints the text with two spaces per level of depth.
    Print an outline: `project`, then (indented) `src`, then (deeper) `main.py`
    and `utils.py`, then (back at depth 1) `README`.
""",
     solution='from contextlib import contextmanager\n'
              '\n'
              'state = {"depth": 0}\n'
              '\n'
              '@contextmanager\n'
              'def indent():\n'
              '    state["depth"] += 1\n'
              '    try:\n'
              '        yield\n'
              '    finally:\n'
              '        state["depth"] -= 1\n'
              '\n'
              'def say(text):\n'
              '    print("  " * state["depth"] + text)\n'
              '\n'
              'say("project")\n'
              'with indent():\n'
              '    say("src")\n'
              '    with indent():\n'
              '        say("main.py")\n'
              '        say("utils.py")\n'
              '    say("README")\n'
              'say("(end)")')

# ------------------------------------------------------------ Q20 project
nb.project("Bank Vault Transactions", story="""
    *Pixel Credit Union* keeps its accounts in a plain dict, and a crash halfway
    through a transfer once left money in neither account. You'll build a small
    transaction manager so changes to the "database" **roll back** whenever
    something goes wrong. Each step builds on the one before.
""",
     given='import copy\n'
           'from contextlib import ExitStack, contextmanager\n\n'
           'class Database:\n'
           '    def __init__(self, data):\n'
           '        self.data = data\n\n'
           'bank = Database({"ada": 100, "grace": 50})',
     steps=[
         ("Write a `Transaction` class (context manager) that takes a `Database`. On entering, it saves "
          "a deep copy of `db.data`. On a clean exit it prints `commit`. If the block raised, it "
          "restores the saved data **in place** (clear the dict and update it, so other references "
          "stay valid), prints `rollback`, and lets the exception continue. Test it: one block that "
          "sets `ada` to 70 cleanly, and one that sets `ada` to 0 and then raises `RuntimeError` "
          "(catch it with a normal `try`). Print `bank.data` after each.",
          'class Transaction:\n'
          '    def __init__(self, db):\n'
          '        self.db = db\n'
          '    def __enter__(self):\n'
          '        self.saved = copy.deepcopy(self.db.data)\n'
          '        return self.db\n'
          '    def __exit__(self, exc_type, exc, tb):\n'
          '        if exc_type is None:\n'
          '            print("commit")\n'
          '        else:\n'
          '            self.db.data.clear()\n'
          '            self.db.data.update(self.saved)\n'
          '            print("rollback")\n'
          '        return False\n'
          '\n'
          'with Transaction(bank) as db:\n'
          '    db.data["ada"] = 70\n'
          'print(bank.data)\n'
          'try:\n'
          '    with Transaction(bank) as db:\n'
          '        db.data["ada"] = 0\n'
          '        raise RuntimeError("crash")\n'
          'except RuntimeError:\n'
          '    pass\n'
          'print(bank.data)'),
         ("Add `class InsufficientFunds(Exception): pass` and a function `transfer(db, source, target, "
          "amount)`. Inside a `Transaction`, it first **subtracts** the amount from the source, then "
          "adds it to the target; if the source balance went negative it raises `InsufficientFunds` "
          "**after** the subtraction. Run a transfer of 20 from `ada` to `grace`, then a transfer of "
          "500 from `grace` to `ada` (catch the error and print `refused`). Print the balances after "
          "each.",
          'class InsufficientFunds(Exception):\n'
          '    pass\n'
          '\n'
          'def transfer(db, source, target, amount):\n'
          '    with Transaction(db):\n'
          '        db.data[source] -= amount\n'
          '        if db.data[source] < 0:\n'
          '            raise InsufficientFunds(source)\n'
          '        db.data[target] += amount\n'
          '\n'
          'transfer(bank, "ada", "grace", 20)\n'
          'print(bank.data)\n'
          'try:\n'
          '    transfer(bank, "grace", "ada", 500)\n'
          'except InsufficientFunds:\n'
          '    print("refused")\n'
          'print(bank.data)'),
         ("Transactions can nest. Show it: in an outer `Transaction`, deposit 10 into `ada`; then "
          "start an inner `Transaction` that deposits 1000 into `grace` and raises "
          "`RuntimeError`, catching that error **inside** the outer block so the outer one still "
          "commits. Print the balances at the end: the outer deposit stays, the inner one is gone.",
          'with Transaction(bank) as outer:\n'
          '    outer.data["ada"] += 10\n'
          '    try:\n'
          '        with Transaction(bank) as inner:\n'
          '            inner.data["grace"] += 1000\n'
          '            raise RuntimeError("inner failed")\n'
          '    except RuntimeError:\n'
          '        print("inner caught")\n'
          'print(bank.data)'),
         ("Add an audit trail. Write a `@contextmanager` function `audited(log, label)` that appends "
          "`label + \": start\"` to `log` before the block and `label + \": ok\"` after it. If the "
          "block raised, it should append `label + \": failed\"` and re-raise (use `try`/`except "
          "Exception`/`raise`). Run two transfers (a good 10 from `ada` to `grace`, and a bad 900 "
          "from `ada` to `grace`) each wrapped in `audited` using the parenthesised form together "
          "with a `Transaction`. Print the log.",
          'log = []\n'
          '\n'
          '@contextmanager\n'
          'def audited(log, label):\n'
          '    log.append(label + ": start")\n'
          '    try:\n'
          '        yield\n'
          '    except Exception:\n'
          '        log.append(label + ": failed")\n'
          '        raise\n'
          '    else:\n'
          '        log.append(label + ": ok")\n'
          '\n'
          'for label, amount in [("t1", 10), ("t2", 900)]:\n'
          '    try:\n'
          '        with (\n'
          '            audited(log, label),\n'
          '            Transaction(bank) as db,\n'
          '        ):\n'
          '            db.data["ada"] -= amount\n'
          '            if db.data["ada"] < 0:\n'
          '                raise InsufficientFunds("ada")\n'
          '            db.data["grace"] += amount\n'
          '    except InsufficientFunds:\n'
          '        pass\n'
          'for entry in log:\n'
          '    print(entry)\n'
          'print(bank.data)'),
         ("Finally, an all-or-nothing change across **two** databases. Write `update_all(databases, "
          "changes)` where `changes` is a list of `(account, delta)` pairs, one per database. Use an "
          "`ExitStack` and `enter_context(Transaction(db))` for each database, then apply each "
          "change; a balance that would go below zero raises `InsufficientFunds`. Make a second "
          "`Database({\"ada\": 5})` called `savings`. Run one update that works "
          "(`+10` on each) and one where the second database fails (`-5` on `bank`'s ada, `-50` on "
          "`savings`' ada), and print both databases after each run to prove that the failed run "
          "changed neither.",
          'def update_all(databases, changes):\n'
          '    with ExitStack() as stack:\n'
          '        for db in databases:\n'
          '            stack.enter_context(Transaction(db))\n'
          '        for db, (account, delta) in zip(databases, changes):\n'
          '            db.data[account] += delta\n'
          '            if db.data[account] < 0:\n'
          '                raise InsufficientFunds(account)\n'
          '\n'
          'savings = Database({"ada": 5})\n'
          'update_all([bank, savings], [("ada", 10), ("ada", 10)])\n'
          'print(bank.data, savings.data)\n'
          'try:\n'
          '    update_all([bank, savings], [("ada", -5), ("ada", -50)])\n'
          'except InsufficientFunds:\n'
          '    print("batch refused")\n'
          'print(bank.data, savings.data)'),
     ])

nb.build()
