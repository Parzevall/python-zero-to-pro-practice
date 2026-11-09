import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB23", title="Decorators", intro="""
    A decorator is a function that takes a function and returns a better one:
    logging, caching, retrying, checking arguments, registering plugins. You
    write the decorators, stack them, give them settings, and use them on
    plain functions, methods and classes. Starting data is given to you
    instead of `input()`.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", """
    The decorator `shout` is given. Write `greet(name)` that returns
    `"hello, "` followed by the name, decorated with `@shout`. Print
    `greet("ada")`.
""",
     given='''
        def shout(func):
            def wrapper(name):
                return func(name).upper()
            return wrapper
     ''',
     solution='''
        @shout
        def greet(name):
            return "hello, " + name
        print(greet("ada"))
     ''')

nb.q("Output-match", """
    `double_result` and `add` are given. Without the `@` syntax, replace `add`
    with its decorated version in one line, then print `add(2, 3)`.
""",
     given='''
        def double_result(func):
            def wrapper(a, b):
                return func(a, b) * 2
            return wrapper

        def add(a, b):
            return a + b
     ''',
     solution='''
        add = double_result(add)
        print(add(2, 3))
     ''')

nb.q("Puzzle", """
    The decorator `log_calls` forgets to use `functools.wraps`. Decorate a
    function `add(a, b)` that has the docstring `"Add two numbers."`, then
    print its `__name__` and its `__doc__` on separate lines.
""",
     given='''
        def log_calls(func):
            def wrapper(*args, **kwargs):
                print("calling", func.__name__)
                return func(*args, **kwargs)
            return wrapper
     ''',
     solution='''
        @log_calls
        def add(a, b):
            """Add two numbers."""
            return a + b
        print(add.__name__)
        print(add.__doc__)
     ''')

nb.q("Build", """
    `fib` is given and is slow for big numbers because it recomputes the same
    values. Decorate it with `functools.cache` and print `fib(60)`.
""",
     given='''
        from functools import cache

        def fib(n):
            return n if n < 2 else fib(n - 1) + fib(n - 2)
     ''',
     solution='''
        @cache
        def fib(n):
            return n if n < 2 else fib(n - 1) + fib(n - 2)
        print(fib(60))
     ''')

nb.q("Real-life", """
    A shop looks up prices with a cached function. Call `price_of` once for
    every SKU in `lookups`, then print the cache statistics of the function.
""",
     given='''
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def price_of(sku):
            return len(sku) * 1.5

        lookups = ["A1", "B22", "A1", "C333", "B22", "A1"]
     ''',
     solution='''
        for sku in lookups:
            price_of(sku)
        print(price_of.cache_info())
     ''')

# ------------------------------------------------------------ Combine
nb.q("Build", """
    Write a decorator `shout` that uppercases the string its function returns.
    Use `functools.wraps`. Decorate `greet(name)` (returns `"hello, "` plus the
    name) with it, print `greet("ada")`, then print `greet.__name__`.
""",
     solution='''
        from functools import wraps

        def shout(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).upper()
            return wrapper

        @shout
        def greet(name):
            return "hello, " + name

        print(greet("ada"))
        print(greet.__name__)
     ''')

nb.q("Real-life", """
    Write a decorator `count_calls` that counts how many times the function
    has been called and keeps the number in an attribute `wrapper.calls`
    (starting at 0). Decorate `ping()` (returns `"pong"`), call it three times,
    and print the count.
""",
     solution='''
        from functools import wraps

        def count_calls(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapper.calls += 1
                return func(*args, **kwargs)
            wrapper.calls = 0
            return wrapper

        @count_calls
        def ping():
            return "pong"

        ping()
        ping()
        ping()
        print(ping.calls)
     ''')

nb.q("Puzzle", """
    Two decorators are given. Stack them on `label(text)` (returns the text
    unchanged) with `@bold` on the top and `@italic` right above the `def`.
    Print `label("hi")`.
""",
     given='''
        def bold(func):
            def wrapper(text):
                return "<b>" + func(text) + "</b>"
            return wrapper

        def italic(func):
            def wrapper(text):
                return "<i>" + func(text) + "</i>"
            return wrapper
     ''',
     solution='''
        @bold
        @italic
        def label(text):
            return text
        print(label("hi"))
     ''')

nb.q("Real-life", """
    Write a decorator `log_call` that prints a line like
    `calling area with (3, 4) {}` (function name, the positional arguments
    tuple, then the keyword dict) before running the function, and returns
    the function's result. Decorate `area(width, height)` and print
    `area(3, 4)`, then `area(width=5, height=2)`.
""",
     solution='''
        from functools import wraps

        def log_call(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print("calling", func.__name__, "with", args, kwargs)
                return func(*args, **kwargs)
            return wrapper

        @log_call
        def area(width, height):
            return width * height

        print(area(3, 4))
        print(area(width=5, height=2))
     ''')

nb.q("Build", """
    Write a decorator **factory** `repeat(times)`: the decorated function runs
    `times` times in a row and the decorator returns the list of all the
    results. Decorate `roll_dice()` that returns a number from the iterator
    `rolls` (use `next(rolls)`) with `@repeat(4)` and print the result.
""",
     given="rolls = iter([4, 1, 6, 3, 2, 5])",
     solution='''
        def repeat(times):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    return [func(*args, **kwargs) for _ in range(times)]
                return wrapper
            return decorator

        @repeat(4)
        def roll_dice():
            return next(rolls)

        print(roll_dice())
     ''')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    `flaky_download()` fails with a `ConnectionError` on its first two calls
    and works on the third. Write a decorator factory `retry(times)` that
    calls the function up to `times` times, printing `attempt N failed` after
    each `ConnectionError`, and returns the first success (re-raise the error
    if the last attempt fails too). Use it with `times=3` and print the result.
""",
     given='''
        calls = 0

        def flaky_download():
            global calls
            calls += 1
            if calls < 3:
                raise ConnectionError("network down")
            return "file contents"
     ''',
     solution='''
        from functools import wraps

        def retry(times):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    for attempt in range(1, times + 1):
                        try:
                            return func(*args, **kwargs)
                        except ConnectionError:
                            print(f"attempt {attempt} failed")
                            if attempt == times:
                                raise
                return wrapper
            return decorator

        download = retry(3)(flaky_download)
        print(download())
     ''')

nb.q("Real-life", """
    Write a decorator factory `require_role(role)` for functions that take the
    `user` dict as first argument: if `user["role"]` is not the required role
    it raises `PermissionError`. Protect `delete_account(user)` (returns
    `"deleted"`) with `"admin"`, then call it for both users and print the
    result, or `denied for NAME` when it raises.
""",
     given='''
        users = [{"name": "Ada", "role": "admin"}, {"name": "Bob", "role": "guest"}]
     ''',
     solution='''
        from functools import wraps

        def require_role(role):
            def decorator(func):
                @wraps(func)
                def wrapper(user, *args, **kwargs):
                    if user["role"] != role:
                        raise PermissionError(user["name"])
                    return func(user, *args, **kwargs)
                return wrapper
            return decorator

        @require_role("admin")
        def delete_account(user):
            return "deleted"

        for user in users:
            try:
                print(delete_account(user))
            except PermissionError:
                print("denied for", user["name"])
     ''')

nb.q("Build", """
    Build a command registry. Write a decorator factory `command(name)` that
    stores the function in the dict `COMMANDS` under that name and returns the
    function unchanged. Register `hello` and `bye` (each returns a short
    string), then run every command typed in `typed` by looking it up in the
    dict and printing its result. Unknown commands print `unknown: NAME`.
""",
     given='''
        COMMANDS = {}
        typed = ["hello", "dance", "bye"]
     ''',
     solution='''
        def command(name):
            def decorator(func):
                COMMANDS[name] = func
                return func
            return decorator

        @command("hello")
        def hello():
            return "Hello there!"

        @command("bye")
        def bye():
            return "See you!"

        for word in typed:
            if word in COMMANDS:
                print(COMMANDS[word]())
            else:
                print("unknown:", word)
     ''')

nb.q("Real-life", """
    Decorators work on methods too, because `self` is just the first argument.
    Write `log_call` that prints `NAME(ARGS)` for each call, using only the
    arguments after `self`, and decorate the `deposit` and `withdraw` methods
    of the class `Account` (given). Make a deposit of 50 and a withdrawal of
    20, then print the balance.
""",
     given='''
        class Account:
            def __init__(self):
                self.balance = 0

            def deposit(self, amount):
                self.balance += amount

            def withdraw(self, amount):
                self.balance -= amount
     ''',
     solution='''
        from functools import wraps

        def log_call(func):
            @wraps(func)
            def wrapper(self, *args):
                print(f"{func.__name__}{args}")
                return func(self, *args)
            return wrapper

        class Account:
            def __init__(self):
                self.balance = 0

            @log_call
            def deposit(self, amount):
                self.balance += amount

            @log_call
            def withdraw(self, amount):
                self.balance -= amount

        account = Account()
        account.deposit(50)
        account.withdraw(20)
        print(account.balance)
     ''')

nb.q("Puzzle", """
    A **class decorator** takes a class and returns a class. Write
    `register(cls)` that stores the class in the dict `PLUGINS` under its
    lowercase class name and returns the class. Decorate `Csv` and `Json`
    (each has a method `extension()` returning `".csv"` / `".json"`), then
    print every plugin name with its extension, in sorted name order.
""",
     given="PLUGINS = {}",
     solution='''
        def register(cls):
            PLUGINS[cls.__name__.lower()] = cls
            return cls

        @register
        class Csv:
            def extension(self):
                return ".csv"

        @register
        class Json:
            def extension(self):
                return ".json"

        for name in sorted(PLUGINS):
            print(name, PLUGINS[name]().extension())
     ''')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Real-life", """
    Write a decorator `validate` that checks every argument against the type
    annotation of its parameter, using `inspect.signature(func).bind(...)`.
    On a mismatch it raises `TypeError` with a message like
    `qty must be int, got str`. Decorate `order(item: str, qty: int)` (returns
    a short sentence), then call it with `("pen", 3)` and `("pen", "3")`,
    printing the result or the error message.
""",
     solution='''
        import inspect
        from functools import wraps

        def validate(func):
            sig = inspect.signature(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound = sig.bind(*args, **kwargs)
                for name, value in bound.arguments.items():
                    expected = sig.parameters[name].annotation
                    if not isinstance(value, expected):
                        raise TypeError(
                            f"{name} must be {expected.__name__}, got {type(value).__name__}")
                return func(*args, **kwargs)
            return wrapper

        @validate
        def order(item: str, qty: int):
            return f"{qty} x {item}"

        for qty in (3, "3"):
            try:
                print(order("pen", qty))
            except TypeError as error:
                print(error)
     ''')

nb.q("Real-life", """
    Use `functools.singledispatch` to write `describe(value)` with a default
    version that returns `"something: "` plus `repr(value)`, a version for
    `int` (`"number N"`), one for `str` (`"text of N chars"`) and one for
    `list` (`"list of N items"`). Print the description of every value in
    `things`.
""",
     given='things = [42, "hello", [1, 2, 3], 2.5, None]',
     solution='''
        from functools import singledispatch

        @singledispatch
        def describe(value):
            return "something: " + repr(value)

        @describe.register
        def _(value: int):
            return f"number {value}"

        @describe.register
        def _(value: str):
            return f"text of {len(value)} chars"

        @describe.register
        def _(value: list):
            return f"list of {len(value)} items"

        for thing in things:
            print(describe(thing))
     ''')

nb.q("Puzzle", """
    A decorator can also be a **class**. Write `class CountCalls` whose
    `__init__(self, func)` stores the function and sets `self.calls = 0`, and
    whose `__call__(self, *args, **kwargs)` counts the call and runs the
    function. Use it with `@CountCalls` on `fizz(n)` (returns `"fizz"` when `n`
    is divisible by 3, otherwise the number as text). Call `fizz` for 1 to 9,
    print the results on one line separated by spaces, then print the call
    count.
""",
     solution='''
        class CountCalls:
            def __init__(self, func):
                self.func = func
                self.calls = 0

            def __call__(self, *args, **kwargs):
                self.calls += 1
                return self.func(*args, **kwargs)

        @CountCalls
        def fizz(n):
            return "fizz" if n % 3 == 0 else str(n)

        results = [fizz(n) for n in range(1, 10)]
        print(" ".join(results))
        print(fizz.calls)
     ''')

nb.q("Real-life", """
    Write a rate limiter `limit(max_calls)`: the decorated function may run
    at most `max_calls` times, and any further call raises `RuntimeError`
    with the message `rate limit reached`. Give the wrapper a `reset()` helper
    (stored as `wrapper.reset`) that starts the counter again. Protect
    `send_sms(number)` (returns `"sent to NUMBER"`) with a limit of 2, send to
    all numbers in `numbers`, printing the result or the error message, then
    reset and send one more.
""",
     given='numbers = ["555-0101", "555-0102", "555-0103"]',
     solution='''
        from functools import wraps

        def limit(max_calls):
            def decorator(func):
                used = 0

                @wraps(func)
                def wrapper(*args, **kwargs):
                    nonlocal used
                    if used >= max_calls:
                        raise RuntimeError("rate limit reached")
                    used += 1
                    return func(*args, **kwargs)

                def reset():
                    nonlocal used
                    used = 0

                wrapper.reset = reset
                return wrapper
            return decorator

        @limit(2)
        def send_sms(number):
            return "sent to " + number

        for number in numbers:
            try:
                print(send_sms(number))
            except RuntimeError as error:
                print(error)
        send_sms.reset()
        print(send_sms("555-0199"))
     ''')

# ------------------------------------------------------------ Q20 story project
nb.project("Mini Web Router", story="""
    You're building the heart of a tiny web framework, like a mini Flask.
    Page functions get **registered** for URL patterns with a `@route`
    decorator, a dispatcher finds the right one for each request, patterns
    can contain parameters such as `/user/<name>`, and **middleware**
    decorators add behaviour like a login check. Each step builds on the
    previous one.
""",
     given='''
        session = {"user": None}
     ''',
     steps=[
         ("Create the dict `ROUTES` and a decorator factory `route(pattern)` that stores the "
          "function in `ROUTES` under the pattern and returns the function unchanged. Register "
          "`home()` for `\"/\"` (returns `\"Welcome!\"`) and `about()` for `\"/about\"` (returns "
          "`\"We sell good stuff.\"`). Print the patterns in sorted order.",
          '''
          from functools import wraps

          ROUTES = {}

          def route(pattern):
              def decorator(func):
                  ROUTES[pattern] = func
                  return func
              return decorator

          @route("/")
          def home():
              return "Welcome!"

          @route("/about")
          def about():
              return "We sell good stuff."

          print(sorted(ROUTES))
          '''),
         ("Write `dispatch(path)` that returns the result of the handler registered for exactly "
          "that path, or `\"404 Not Found\"` if there is none. Print the answer for `/`, "
          "`/about` and `/contact`, one per line.",
          '''
          def dispatch(path):
              if path in ROUTES:
                  return ROUTES[path]()
              return "404 Not Found"

          for path in ["/", "/about", "/contact"]:
              print(dispatch(path))
          '''),
         ("Add path parameters. Register `user(name)` for `\"/user/<name>\"` and "
          "`post(name, post_id)` for `\"/user/<name>/post/<post_id>\"`; they return "
          "`\"Profile of NAME\"` and `\"Post POST_ID by NAME\"`. Rewrite `dispatch(path)`: split "
          "the path and each pattern on `\"/\"`; a pattern matches when it has the same number "
          "of parts and every part is equal or is written like `<something>`. The "
          "`<something>` parts are passed to the handler as keyword arguments. Print the "
          "dispatch of `/about`, `/user/ada`, `/user/ada/post/7` and `/nothing/here`.",
          '''
          @route("/user/<name>")
          def user(name):
              return "Profile of " + name

          @route("/user/<name>/post/<post_id>")
          def post(name, post_id):
              return f"Post {post_id} by {name}"

          def dispatch(path):
              parts = path.split("/")
              for pattern, handler in ROUTES.items():
                  pattern_parts = pattern.split("/")
                  if len(pattern_parts) != len(parts):
                      continue
                  params = {}
                  for expected, actual in zip(pattern_parts, parts):
                      if expected.startswith("<") and expected.endswith(">"):
                          params[expected[1:-1]] = actual
                      elif expected != actual:
                          break
                  else:
                      return handler(**params)
              return "404 Not Found"

          for path in ["/about", "/user/ada", "/user/ada/post/7", "/nothing/here"]:
              print(dispatch(path))
          '''),
         ("Add middleware. Write a decorator `require_login(func)` (use `wraps`) that returns "
          "`\"401 Please log in\"` when `session[\"user\"]` is `None` and otherwise runs the "
          "function. Register `admin()` for `\"/admin\"` with `@route` on top and "
          "`@require_login` below it; it returns `\"Admin panel for \" + session[\"user\"]`. "
          "Print `dispatch(\"/admin\")`, set `session[\"user\"] = \"ada\"`, print it again.",
          '''
          def require_login(func):
              @wraps(func)
              def wrapper(*args, **kwargs):
                  if session["user"] is None:
                      return "401 Please log in"
                  return func(*args, **kwargs)
              return wrapper

          @route("/admin")
          @require_login
          def admin():
              return "Admin panel for " + session["user"]

          print(dispatch("/admin"))
          session["user"] = "ada"
          print(dispatch("/admin"))
          '''),
         ("Count the traffic. Write a `hits` decorator that counts how often each handler runs "
          "in a dict `HITS` keyed by the handler's name. Since `route` registers whatever it "
          "is given, simply apply it in a loop to re-register every handler of `ROUTES` "
          "wrapped: for each `pattern, handler` in a copy of `ROUTES.items()`, set "
          "`ROUTES[pattern] = hits(handler)`. Dispatch `/`, `/`, `/user/bob`, `/admin` and "
          "`/`, then print each handler name with its count in sorted name order.",
          '''
          HITS = {}

          def hits(func):
              @wraps(func)
              def wrapper(*args, **kwargs):
                  HITS[func.__name__] = HITS.get(func.__name__, 0) + 1
                  return func(*args, **kwargs)
              return wrapper

          for pattern, handler in list(ROUTES.items()):
              ROUTES[pattern] = hits(handler)

          for path in ["/", "/", "/user/bob", "/admin", "/"]:
              dispatch(path)
          for name in sorted(HITS):
              print(name, HITS[name])
          '''),
     ])

nb.build()
