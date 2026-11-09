import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB28", title="Testing, Debugging & Logging", intro="""
    How professionals trust their code: `assert` checks, `unittest`, pytest-style
    test functions, `doctest`, mocks that stand in for slow or random things,
    reading tracebacks, and `logging` instead of scattered `print()` calls. Every
    task is a **write** task. Test runners are told to stay quiet and the tasks
    ask you to print only the stable facts (passed or failed, counts, names).
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", """
    `slugify` turns a title into a URL piece. Pin it down with three `assert`
    statements: a plain title, a title with extra spaces around it, and a title
    that is already lower case. Then print `slugify ok`.
""",
     given='def slugify(title):\n    return "-".join(title.lower().split())',
     solution='assert slugify("Hello World") == "hello-world"\n'
              'assert slugify("  Big   News ") == "big-news"\n'
              'assert slugify("python") == "python"\n'
              'print("slugify ok")')

nb.q("Output-match", """
    The VAT helper below should add 20%. Check `add_vat(10)` against `12` with
    an `assert` that has the message `VAT should be 20%`, wrapped so that the
    failure is caught and only the message is printed.
""",
     given="def add_vat(price):\n    return price * 1.1",
     solution="try:\n"
              '    assert add_vat(10) == 12, "VAT should be 20%"\n'
              "except AssertionError as error:\n"
              "    print(error)")

nb.q("Output-match", """
    A teammate left a `breakpoint()` call in `checkout()`, which would freeze a
    script waiting for a debugger. Without editing `checkout`, make
    `breakpoint()` do nothing by setting the `PYTHONBREAKPOINT` environment
    variable to `0` from Python, then call `checkout()`.
""",
     given='def checkout():\n    breakpoint()\n    print("checkout finished")',
     solution='import os\nos.environ["PYTHONBREAKPOINT"] = "0"\ncheckout()')

nb.q("Puzzle", """
    `is_adult` is supposed to be `True` from age 18 upwards. One carefully
    chosen `assert` exposes the bug. Write it with a `try`/`except` so that
    instead of crashing the program prints `bug found at the boundary`.
""",
     given="def is_adult(age):\n    return age > 18",
     solution="try:\n"
              "    assert is_adult(18) is True\n"
              "except AssertionError:\n"
              '    print("bug found at the boundary")')

nb.q("Real-life", """
    `mailer` stands in for a real email service. Create it as a `Mock`, call
    `mailer.send("ana@example.com", "Welcome")` once, then print how many times
    `send` was called and the arguments it received (as a tuple).
""",
     solution="from unittest.mock import Mock\n"
              "mailer = Mock()\n"
              'mailer.send("ana@example.com", "Welcome")\n'
              "print(mailer.send.call_count)\n"
              "print(mailer.send.call_args.args)")

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    Configure logging so everything goes to standard output with the format
    `LEVEL:message` (use `%(levelname)s:%(message)s`) and the level `INFO`.
    Then log one `debug`, one `info` and one `warning` message with any text.
    Only the last two should appear.
""",
     solution="import logging, sys\n"
              'logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO,\n'
              '                    format="%(levelname)s:%(message)s")\n'
              'logging.debug("loading config")\n'
              'logging.info("server starting")\n'
              'logging.warning("disk almost full")')

nb.q("Build", """
    Write a `unittest.TestCase` called `ConvertTests` with two tests for
    `c_to_f`: one for `0` (32.0) and one for `100` (212.0). Run it with a
    `TextTestRunner` whose stream is a `StringIO`, then print whether the run
    was successful and how many tests ran, like the expected output.
""",
     given="def c_to_f(c):\n    return c * 9 / 5 + 32",
     solution="import io, unittest\n"
              "class ConvertTests(unittest.TestCase):\n"
              "    def test_freezing(self):\n"
              "        self.assertEqual(c_to_f(0), 32.0)\n"
              "    def test_boiling(self):\n"
              "        self.assertEqual(c_to_f(100), 212.0)\n"
              "suite = unittest.defaultTestLoader.loadTestsFromTestCase(ConvertTests)\n"
              "result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)\n"
              'print("successful:", result.wasSuccessful())\n'
              'print("tests run:", result.testsRun)')

nb.q("Real-life", """
    `weather` is a fake weather service whose `get()` fails once with a
    `TimeoutError` and then succeeds. Loop twice and call `weather.get()`
    inside a `try`; print `timeout, retrying` on a failure and the data when it
    works.
""",
     given='from unittest.mock import Mock\n'
           'weather = Mock()\n'
           'weather.get.side_effect = [TimeoutError("slow"), "sunny, 21C"]',
     solution="for attempt in range(2):\n"
              "    try:\n"
              "        print(weather.get())\n"
              "    except TimeoutError:\n"
              '        print("timeout, retrying")')

nb.q("Puzzle", """
    `ratio` calls `average`, which can divide by zero. Call `ratio([])` inside
    a `try`, catch the error and use the `traceback` module on
    `error.__traceback__` to print the names of the functions the error passed
    through, outermost first, joined with ` -> `.
""",
     given="def average(values):\n    return sum(values) / len(values)\n\n"
           "def ratio(values):\n    return average(values) * 100",
     solution="import traceback\n"
              "try:\n"
              "    ratio([])\n"
              "except ZeroDivisionError as error:\n"
              "    frames = traceback.extract_tb(error.__traceback__)\n"
              '    print(" -> ".join(frame.name for frame in frames))')

nb.q("Build", """
    The docstring of `double` contains two examples. Use `doctest` to run them
    without printing anything yourself from the examples: build the test with
    `doctest.DocTestParser().get_doctest(double.__doc__, {"double": double},
    "double", None, 0)`, run it with a `doctest.DocTestRunner()` and print the
    number of attempted examples and the number of failed ones.
""",
     given='def double(n):\n    """\n    >>> double(4)\n    8\n    >>> double("ab")\n    \'abab\'\n    """\n    return n * 2',
     solution="import doctest\n"
              'test = doctest.DocTestParser().get_doctest(double.__doc__, {"double": double}, "double", None, 0)\n'
              "result = doctest.DocTestRunner().run(test)\n"
              'print("attempted:", result.attempted)\n'
              'print("failed:", result.failed)')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Build a logger hierarchy for a shop. Create the loggers `shop` and
    `shop.cart`. Give **only** `shop` a stream handler (to `sys.stdout`) with
    the format `%(name)s %(levelname)s %(message)s`, and set its level to
    `WARNING`. Then make `shop.cart` log one `info` and one `warning` message.
    The child has no handler of its own, so its record travels up to the parent.
""",
     solution="import logging, sys\n"
              'shop = logging.getLogger("shop")\n'
              "handler = logging.StreamHandler(sys.stdout)\n"
              'handler.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))\n'
              "shop.addHandler(handler)\n"
              "shop.setLevel(logging.WARNING)\n"
              'cart = logging.getLogger("shop.cart")\n'
              'cart.info("item added")\n'
              'cart.warning("stock is low")')

nb.q("Build", """
    Write a `CartTests` test case for the `Cart` class. Use `setUp` to create a
    fresh cart with `add("pen", 2)` already done. Write three tests: the total
    is 2 (`assertEqual`), adding a negative quantity raises `ValueError`
    (`assertRaises`), and removing something absent raises `KeyError`. Run the
    suite quietly and print `successful`, `failures` and `errors` counts.
""",
     given="class Cart:\n"
           "    def __init__(self):\n        self.items = {}\n"
           "    def add(self, name, qty):\n"
           "        if qty < 0:\n            raise ValueError('negative quantity')\n"
           "        self.items[name] = self.items.get(name, 0) + qty\n"
           "    def remove(self, name):\n        del self.items[name]\n"
           "    def total(self):\n        return sum(self.items.values())",
     solution="import io, unittest\n"
              "class CartTests(unittest.TestCase):\n"
              "    def setUp(self):\n"
              "        self.cart = Cart()\n"
              '        self.cart.add("pen", 2)\n'
              "    def test_total(self):\n"
              "        self.assertEqual(self.cart.total(), 2)\n"
              "    def test_negative_quantity(self):\n"
              "        with self.assertRaises(ValueError):\n"
              '            self.cart.add("pen", -1)\n'
              "    def test_remove_missing(self):\n"
              "        with self.assertRaises(KeyError):\n"
              '            self.cart.remove("book")\n'
              "suite = unittest.defaultTestLoader.loadTestsFromTestCase(CartTests)\n"
              "result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)\n"
              'print("successful:", result.wasSuccessful())\n'
              'print("failures:", len(result.failures))\n'
              'print("errors:", len(result.errors))')

nb.q("Real-life", """
    `describe(city)` calls `fetch_json`, which would hit the internet. Use
    `unittest.mock.patch` on **this module's** `fetch_json` (the path is
    `"__main__.fetch_json"`) with the return value `{"temp": 18}`, call
    `describe("Oslo")` while patched and print the result. Afterwards print
    what `patch` recorded: the single argument `fetch_json` was called with.
""",
     given='def fetch_json(url):\n    raise RuntimeError("no internet in tests")\n\n'
           'def describe(city):\n    data = fetch_json("https://weather.example/" + city)\n'
           '    return city + ": " + str(data["temp"]) + " C"',
     solution="from unittest.mock import patch\n"
              'with patch("__main__.fetch_json", return_value={"temp": 18}) as fake:\n'
              '    print(describe("Oslo"))\n'
              "print(fake.call_args.args[0])")

nb.q("Real-life", """
    `Session` expires `ttl` seconds after it was created, based on a clock
    function passed in. Test it without waiting: create a `Mock` clock with
    `side_effect=[100, 105, 130]` (the first reading is used when the session is
    created), build a `Session` with `ttl=20` using it, then print
    `is_expired()` twice. The two calls read the clock at 105 and 130.
""",
     given="class Session:\n"
           "    def __init__(self, ttl, clock):\n"
           "        self.ttl = ttl\n        self.clock = clock\n        self.created = clock()\n"
           "    def is_expired(self):\n"
           "        return self.clock() - self.created > self.ttl",
     solution="from unittest.mock import Mock\n"
              "clock = Mock(side_effect=[100, 105, 130])\n"
              "session = Session(20, clock)\n"
              "print(session.is_expired())\n"
              "print(session.is_expired())")

nb.q("Build", """
    pytest runs plain `test_` functions, injects fixtures and repeats a test
    for many cases (`parametrize`). Imitate that by hand. Write a function
    `make_cart()` (the fixture) returning a fresh `Cart`, and a function
    `check_total(cart, items, expected)` (the test) that adds the `items`
    `(name, qty)` pairs and asserts the total. Run it for every case in
    `cases`, each with a fresh cart, and print `PASS case-number` or
    `FAIL case-number` (numbering from 1) using `try`/`except AssertionError`.
    The given `Cart.add` has a bug (adding the same item twice overwrites
    instead of adding up), so one case is expected to FAIL: your runner should
    report it, not hide it.
""",
     given="class Cart:\n"
           "    def __init__(self):\n        self.items = {}\n"
           "    def add(self, name, qty):\n        self.items[name] = qty\n"
           "    def total(self):\n        return sum(self.items.values())\n\n"
           'cases = [([("pen", 2)], 2), ([("pen", 2), ("ink", 3)], 5), ([("pen", 2), ("pen", 3)], 5)]',
     solution="def make_cart():\n    return Cart()\n\n"
              "def check_total(cart, items, expected):\n"
              "    for name, qty in items:\n"
              "        cart.add(name, qty)\n"
              "    assert cart.total() == expected\n\n"
              "for number, (items, expected) in enumerate(cases, start=1):\n"
              "    try:\n"
              "        check_total(make_cart(), items, expected)\n"
              '        print("PASS", number)\n'
              "    except AssertionError:\n"
              '        print("FAIL", number)')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    `median` has bugs. Write a helper `report(label, ok)` that prints
    `PASS label` or `FAIL label`. Use it for four checks of the buggy function:
    `median([3])` is 3, `median([1, 3, 2])` is 2, `median([4, 1, 3, 2])` is 2.5,
    and `median([5, 1, 9])` is 5. Then write a corrected `median` (it must sort,
    and average the two middle values for an even count) and print a line
    `--- after the fix ---` followed by the same four checks.
""",
     given="def median(values):\n    middle = len(values) // 2\n    return values[middle]",
     solution="def report(label, ok):\n"
              '    print("PASS" if ok else "FAIL", label)\n\n'
              "def run_checks():\n"
              '    report("single", median([3]) == 3)\n'
              '    report("odd unsorted", median([1, 3, 2]) == 2)\n'
              '    report("even", median([4, 1, 3, 2]) == 2.5)\n'
              '    report("another odd", median([5, 1, 9]) == 5)\n\n'
              "run_checks()\n\n"
              "def median(values):\n"
              "    ordered = sorted(values)\n"
              "    middle = len(ordered) // 2\n"
              "    if len(ordered) % 2 == 1:\n"
              "        return ordered[middle]\n"
              "    return (ordered[middle - 1] + ordered[middle]) / 2\n\n"
              'print("--- after the fix ---")\n'
              "run_checks()")

nb.q("Real-life", """
    A payment API is flaky. Write a decorator `retry(times)` that calls the
    function up to `times` times. When a `ConnectionError` happens it logs a
    `warning` through the logger `payments` with the text
    `attempt 1 failed: down` (attempt number and error text) and tries again;
    after the last failed attempt the error is raised. Logs must go to a
    `StringIO` through a handler with the format `%(levelname)s %(message)s`.
    Decorate a function `charge()` that calls the mock `api` and prints the
    result, then print everything the log collected.
""",
     given='from unittest.mock import Mock\n'
           'api = Mock(side_effect=[ConnectionError("down"), ConnectionError("down"), "paid"])',
     solution="import io, logging\n"
              "stream = io.StringIO()\n"
              "handler = logging.StreamHandler(stream)\n"
              'handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))\n'
              'log = logging.getLogger("payments")\n'
              "log.addHandler(handler)\n"
              "log.setLevel(logging.INFO)\n"
              "log.propagate = False\n\n"
              "def retry(times):\n"
              "    def decorator(func):\n"
              "        def wrapper(*args, **kwargs):\n"
              "            for attempt in range(1, times + 1):\n"
              "                try:\n"
              "                    return func(*args, **kwargs)\n"
              "                except ConnectionError as error:\n"
              '                    log.warning("attempt %d failed: %s", attempt, error)\n'
              "                    if attempt == times:\n"
              "                        raise\n"
              "        return wrapper\n"
              "    return decorator\n\n"
              "@retry(3)\n"
              "def charge():\n"
              "    return api()\n\n"
              "print(charge())\n"
              "print(stream.getvalue().strip())")

nb.q("Puzzle", """
    A plain `Mock` accepts **any** call, so a typo in a test passes for the
    wrong reason. Create `lazy = Mock()` and call `lazy.sned("x")` (typo) and
    print `plain mock accepted the typo`. Then create `strict =
    Mock(spec=Mailer)`, try the same typo inside a `try`/`except
    AttributeError` and print `spec mock rejected the typo`. Finally call
    `strict.send("x")` and assert with `assert_called_once_with("x")`, printing
    `send verified`.
""",
     given="class Mailer:\n    def send(self, text):\n        print('really sending', text)",
     solution="from unittest.mock import Mock\n"
              "lazy = Mock()\n"
              'lazy.sned("x")\n'
              'print("plain mock accepted the typo")\n\n'
              "strict = Mock(spec=Mailer)\n"
              "try:\n"
              '    strict.sned("x")\n'
              "except AttributeError:\n"
              '    print("spec mock rejected the typo")\n'
              'strict.send("x")\n'
              'strict.send.assert_called_once_with("x")\n'
              'print("send verified")')

nb.q("Build", """
    Write a `ListHandler` (a `logging.Handler` subclass whose `emit` stores each
    record in `self.records`) and attach it to the logger `audit` at level
    `INFO`, with propagation off. The function `old_total` is deprecated: it
    should emit a `DeprecationWarning` with the text `use new_total` through
    `warnings.warn`. Call it inside `warnings.catch_warnings(record=True)` with
    `warnings.simplefilter("always")`, then log `"total computed"` at `info`
    and `"deprecated call seen"` at `warning`. Print the warning's category
    name and message, then every collected record as `LEVEL: message`.
""",
     given="def old_total(prices):\n    return sum(prices)",
     solution="import logging, warnings\n\n"
              "class ListHandler(logging.Handler):\n"
              "    def __init__(self):\n"
              "        super().__init__()\n"
              "        self.records = []\n"
              "    def emit(self, record):\n"
              "        self.records.append(record)\n\n"
              'audit = logging.getLogger("audit")\n'
              "collector = ListHandler()\n"
              "audit.addHandler(collector)\n"
              "audit.setLevel(logging.INFO)\n"
              "audit.propagate = False\n\n"
              "def old_total(prices):\n"
              '    warnings.warn("use new_total", DeprecationWarning)\n'
              "    return sum(prices)\n\n"
              "with warnings.catch_warnings(record=True) as caught:\n"
              '    warnings.simplefilter("always")\n'
              "    total = old_total([2, 3])\n"
              'audit.info("total computed")\n'
              'audit.warning("deprecated call seen")\n'
              "print(caught[0].category.__name__, str(caught[0].message))\n"
              "for record in collector.records:\n"
              '    print(record.levelname + ": " + record.getMessage())')

# ------------------------------------------------------------ Q20 project
BANK = '''
class InsufficientFunds(Exception):
    pass


class Account:
    def __init__(self, owner, balance=0, history=[]):
        self.owner = owner
        self.balance = balance
        self.history = history

    def deposit(self, amount):
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount >= self.balance:
            raise InsufficientFunds(self.owner)
        self.balance -= amount
        self.history.append(("withdraw", amount))

    def apply_interest(self, rate):
        self.balance = self.balance + self.balance * rate


def send_sms(owner, text):
    raise RuntimeError("no SMS gateway in tests")


def notify_low_balance(account, limit=50):
    if account.balance < limit:
        send_sms(account.owner, "Low balance: " + str(account.balance))
        return True
    return False
'''

nb.project("Bug Hunt at Pocket Bank", story="""
    A teammate wrote the banking module in the first cell below, then went on
    holiday. Customers already complain. You'll write tests that **expose** the
    bugs, fix them, prove the fixes, add logging and test the SMS alert
    without sending a real message. Each step builds on the one before.
""",
     given=BANK,
     steps=[
         ("""
          Write `BankTests` (a `unittest.TestCase`) with four tests that each
          expose one problem: (1) depositing a negative amount should raise
          `ValueError`; (2) withdrawing exactly the whole balance of 100 should
          work and leave 0; (3) two accounts created without a history must not
          share one (deposit into one, the other's history stays empty); (4)
          `apply_interest(0.1)` on a balance of 33.33 should give 36.66
          (rounded to 2 decimals). Write a function `run(test_class)` that runs
          a test class quietly and returns the result. Call it and print
          `successful`, the sorted names of the failed or errored tests
          (`test.id().split(".")[-1]`), and the counts.
          """,
          "import io, unittest\n\n"
          "class BankTests(unittest.TestCase):\n"
          "    def test_negative_deposit(self):\n"
          '        account = Account("ana", 10)\n'
          "        with self.assertRaises(ValueError):\n"
          "            account.deposit(-5)\n"
          "    def test_withdraw_everything(self):\n"
          '        account = Account("ana", 100)\n'
          "        account.withdraw(100)\n"
          "        self.assertEqual(account.balance, 0)\n"
          "    def test_separate_histories(self):\n"
          '        first = Account("ana")\n'
          '        second = Account("bo")\n'
          "        first.deposit(10)\n"
          "        self.assertEqual(second.history, [])\n"
          "    def test_interest_rounded(self):\n"
          '        account = Account("ana", 33.33)\n'
          "        account.apply_interest(0.1)\n"
          "        self.assertEqual(account.balance, 36.66)\n\n"
          "def run(test_class):\n"
          "    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)\n"
          "    return unittest.TextTestRunner(stream=io.StringIO()).run(suite)\n\n"
          "result = run(BankTests)\n"
          'print("successful:", result.wasSuccessful())\n'
          "bad = sorted(test.id().split('.')[-1] for test, _ in result.failures + result.errors)\n"
          'print("failing:", bad)\n'
          'print("tests run:", result.testsRun, "problems:", len(bad))'),
         ("""
          Fix the module by writing a corrected `Account` class (same
          interface). It must reject non-positive deposits with `ValueError`, allow
          withdrawing up to the full balance (raise `InsufficientFunds` only
          when the amount is **more** than the balance), give every account its
          own list (`history=None` default), and round the balance to 2 decimals
          after interest. Re-run `BankTests` with `run` and print `successful`
          and the number of problems.
          """,
          "class Account:\n"
          "    def __init__(self, owner, balance=0, history=None):\n"
          "        self.owner = owner\n"
          "        self.balance = balance\n"
          "        self.history = [] if history is None else history\n\n"
          "    def deposit(self, amount):\n"
          "        if amount <= 0:\n"
          '            raise ValueError("deposit must be positive")\n'
          "        self.balance += amount\n"
          '        self.history.append(("deposit", amount))\n\n'
          "    def withdraw(self, amount):\n"
          "        if amount > self.balance:\n"
          "            raise InsufficientFunds(self.owner)\n"
          "        self.balance -= amount\n"
          '        self.history.append(("withdraw", amount))\n\n'
          "    def apply_interest(self, rate):\n"
          "        self.balance = round(self.balance + self.balance * rate, 2)\n\n"
          "result = run(BankTests)\n"
          'print("successful:", result.wasSuccessful())\n'
          'print("problems:", len(result.failures) + len(result.errors))'),
         ("""
          Add logging. Write `transfer(source, target, amount)` that withdraws
          from `source` and deposits into `target`. Use a logger called
          `bank.transfer` with a handler writing to `sys.stdout` (format
          `%(levelname)s %(name)s: %(message)s`, level `INFO`, propagation
          off). A good transfer logs an `info` line `ana -> bo: 30`; when
          `InsufficientFunds` is raised it logs a `warning` line
          `ana cannot send 500` and returns `False` (it returns `True` on
          success). Try one transfer of 30 and one of 500 between accounts with
          balances 100 and 20, then print both balances.
          """,
          "import logging, sys\n"
          'log = logging.getLogger("bank.transfer")\n'
          "handler = logging.StreamHandler(sys.stdout)\n"
          'handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))\n'
          "log.addHandler(handler)\n"
          "log.setLevel(logging.INFO)\n"
          "log.propagate = False\n\n"
          "def transfer(source, target, amount):\n"
          "    try:\n"
          "        source.withdraw(amount)\n"
          "    except InsufficientFunds:\n"
          '        log.warning("%s cannot send %s", source.owner, amount)\n'
          "        return False\n"
          "    target.deposit(amount)\n"
          '    log.info("%s -> %s: %s", source.owner, target.owner, amount)\n'
          "    return True\n\n"
          'ana = Account("ana", 100)\n'
          'bo = Account("bo", 20)\n'
          "transfer(ana, bo, 30)\n"
          "transfer(ana, bo, 500)\n"
          'print("balances:", ana.balance, bo.balance)'),
         ("""
          Test the SMS alert without sending anything. `notify_low_balance`
          calls the module's `send_sms`. Use `unittest.mock.patch` on
          `"__main__.send_sms"` to check two situations with `Account("cy",
          20)` and `Account("di", 500)`: the low account returns `True` and
          the SMS function was called once with `("cy", "Low balance: 20")`; the
          rich account returns `False` and the SMS function was never called.
          Print the return value and the call information for each.
          """,
          "from unittest.mock import patch\n"
          'with patch("__main__.send_sms") as fake_sms:\n'
          '    low = Account("cy", 20)\n'
          "    print(notify_low_balance(low))\n"
          "    print(fake_sms.call_args.args)\n"
          "    print(fake_sms.call_count)\n"
          'with patch("__main__.send_sms") as fake_sms:\n'
          '    rich = Account("di", 500)\n'
          "    print(notify_low_balance(rich))\n"
          "    print(fake_sms.called)"),
         ("""
          Finish with a regression suite. Write `AlertTests` (a `TestCase`)
          whose `setUp` starts a patcher for `"__main__.send_sms"` (stop it with
          `self.addCleanup`), with two tests: a low balance sends exactly one
          SMS, a balance of 50 (exactly the limit) sends none. Then load
          **both** `BankTests` and `AlertTests` into one suite (use
          `unittest.TestSuite` and `loadTestsFromTestCase`), run it quietly and
          print `All green: True` style output plus the total number of tests.
          """,
          "class AlertTests(unittest.TestCase):\n"
          "    def setUp(self):\n"
          '        patcher = patch("__main__.send_sms")\n'
          "        self.fake_sms = patcher.start()\n"
          "        self.addCleanup(patcher.stop)\n"
          "    def test_low_balance_sends_one(self):\n"
          '        notify_low_balance(Account("cy", 10))\n'
          "        self.assertEqual(self.fake_sms.call_count, 1)\n"
          "    def test_limit_sends_none(self):\n"
          '        notify_low_balance(Account("cy", 50))\n'
          "        self.fake_sms.assert_not_called()\n\n"
          "loader = unittest.defaultTestLoader\n"
          "suite = unittest.TestSuite()\n"
          "suite.addTests(loader.loadTestsFromTestCase(BankTests))\n"
          "suite.addTests(loader.loadTestsFromTestCase(AlertTests))\n"
          "result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)\n"
          'print("All green:", result.wasSuccessful())\n'
          'print("Total tests:", result.testsRun)'),
     ])

nb.build()
