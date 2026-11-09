import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB12", title="Exceptions", intro="""
    An exception is Python's way of saying "I can't carry on from here".
    You have met `ValueError`, `KeyError` and `ZeroDivisionError` already, and
    NB07 showed a first `try` / `except`. This notebook goes deep: catching
    the right errors, raising your own, chaining them and reporting several
    at once.

    Exceptions form a family tree (`KeyError` and `IndexError` are both kinds
    of `LookupError`, which is a kind of `Exception`). An `except` clause
    catches the class you name **and everything below it**. Custom exceptions
    use the one-line form `class MyError(Exception): pass`; classes with
    methods come in NB14.

    Every solution here **catches and reports** its errors, so no cell ends in
    a crash. To catch several classes in one clause, put them in a tuple:
    `except (KeyError, IndexError):`.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "A bill is split between friends. Print `total / people`, but when `people` is zero print `cannot divide by zero` instead of crashing.",
     given="total = 120\npeople = 0",
     solution='try:\n    print(total / people)\nexcept ZeroDivisionError:\n    print("cannot divide by zero")')

nb.q("Real-life", "A cinema customer asks for a seat number that may not exist. Print the seat at index `wanted`, or `no such seat` if the index is out of range.",
     given='seats = ["A1", "A2", "A3"]\nwanted = 5',
     solution='try:\n    print(seats[wanted])\nexcept IndexError:\n    print("no such seat")')

nb.q("Build", "Look up `\"pear\"` in the price dictionary, catching the error through its **parent class** `LookupError` (not `KeyError`). Store the error as `e` and print the name of its actual class.",
     given='prices = {"apple": 0.5, "banana": 0.25}',
     solution='try:\n    print(prices["pear"])\nexcept LookupError as e:\n    print(type(e).__name__)')

nb.q("Output-match", "Convert `text` with `int()`. When it fails, import `traceback` and print the one-line summary from `traceback.format_exception_only(e)` (it returns a list; take its first item and `strip()` the newline).",
     given='text = "4x"',
     solution='import traceback\ntry:\n    int(text)\nexcept ValueError as e:\n    print(traceback.format_exception_only(e)[0].strip())')

nb.q("Output-match", "Convert `text` with `int()`. When it fails, print the error\'s `args` tuple (not the error itself).",
     given='text = "4x"',
     solution="try:\n    int(text)\nexcept ValueError as e:\n    print(e.args)")

# ------------------------------------------------------------ Combine
nb.q("Real-life", "A survey form contains mixed answers. Add up the answers that are whole numbers, skip (and count) the ones that are not, and print the total and the skipped count on separate lines.",
     given='answers = ["12", "x", "7", "3.5", "40"]',
     solution='total = 0\nskipped = 0\nfor answer in answers:\n    try:\n        total += int(answer)\n    except ValueError:\n        skipped += 1\nprint(total)\nprint(skipped)')

nb.q("Output-match", """
    Divide 100 by each divisor. Use all four parts of the statement:
    `try` does the division, `except ZeroDivisionError` prints `bad divisor`,
    `else` prints `result` and the value, and `finally` prints `checked` and
    the divisor (it runs every time).
""",
     given="divisors = [4, 0, 8]",
     solution='for divisor in divisors:\n    try:\n        result = 100 / divisor\n    except ZeroDivisionError:\n        print("bad divisor")\n    else:\n        print("result", result)\n    finally:\n        print("checked", divisor)')

nb.q("Puzzle", """
    Write `read_sensor()` that prints `reading` and then does
    `return "OK"` inside a `try`, with a `finally` block that prints
    `cleanup`. Print the value of calling it, and see which line comes first.
""",
     solution='def read_sensor():\n    try:\n        print("reading")\n        return "OK"\n    finally:\n        print("cleanup")\nprint(read_sensor())')

nb.q("Real-life", """
    A file importer processes uploads. Write `import_file(name, size_kb)`:
    in a `try` it raises `ValueError("empty file")` when the size is 0 and
    `OverflowError("too big")` when it is above 500; otherwise nothing is
    raised. Print `imported` in `else`, the error message in the matching
    `except`, and `closed` + the name in `finally`. Call it for each upload.
""",
     given='uploads = [("a.csv", 40), ("b.csv", 0), ("c.csv", 900)]',
     solution='def import_file(name, size_kb):\n    try:\n        if size_kb == 0:\n            raise ValueError("empty file")\n        if size_kb > 500:\n            raise OverflowError("too big")\n    except ValueError as e:\n        print(e)\n    except OverflowError as e:\n        print(e)\n    else:\n        print("imported")\n    finally:\n        print("closed", name)\nfor name, size_kb in uploads:\n    import_file(name, size_kb)')

nb.q("Real-life", """
    A profile form must reject unrealistic ages. Write `set_age(age)` that
    raises `ValueError` with a message that includes the age when it is below
    0 or above 120, and otherwise returns the age. Loop over the ages; print
    `age set to` and the value for good ones, or the error message for bad
    ones.
""",
     given="ages = [30, -5, 200]",
     solution='def set_age(age):\n    if age < 0 or age > 120:\n        raise ValueError(f"age {age} is not realistic")\n    return age\nfor age in ages:\n    try:\n        print("age set to", set_age(age))\n    except ValueError as e:\n        print(e)')

# ------------------------------------------------------------ Small real tasks
nb.q("Build", """
    Write `get(container, key)` that returns `container[key]`, or the text
    `missing` when the lookup fails because of a missing dict key **or** an
    out-of-range list index. Use one `except` line with both classes in a
    tuple. Print a hit and a miss for a dict, then a hit and a
    miss for a list.
""",
     given='stock = {"apple": 12}\nrows = [10, 20]',
     solution='def get(container, key):\n    try:\n        return container[key]\n    except (KeyError, IndexError):\n        return "missing"\nprint(get(stock, "apple"))\nprint(get(stock, "pear"))\nprint(get(rows, 1))\nprint(get(rows, 5))')

nb.q("Real-life", """
    Define `InsufficientFunds` as a custom exception (one-line class based on
    `Exception`). Write `withdraw(balance, amount)` that raises it with a
    message saying how much the balance is short by, or returns the new
    balance. Process every withdrawal, printing `balance` and the new amount,
    or `declined:` and the message.
""",
     given="balance = 100\nrequests = [30, 90, 50]",
     solution='class InsufficientFunds(Exception): pass\n\ndef withdraw(balance, amount):\n    if amount > balance:\n        raise InsufficientFunds(f"short by {amount - balance}")\n    return balance - amount\n\nfor amount in requests:\n    try:\n        balance = withdraw(balance, amount)\n        print("balance", balance)\n    except InsufficientFunds as e:\n        print("declined:", e)')

nb.q("Build", """
    A low-level `ValueError` is not a helpful message for a shop owner.
    Define `BadPrice(Exception)`. Write two functions that convert text to a
    float and raise `BadPrice("price is not a number")` when it fails:
    `strict(text)` raises it with `from e`, while `careless(text)` raises it
    inside the `except` block without `from`. Call each with `"abc"` and print
    its `__cause__` (the explicit link) and the name of its `__context__`
    class (the automatic link).
""",
     solution='class BadPrice(Exception): pass\n\ndef strict(text):\n    try:\n        return float(text)\n    except ValueError as e:\n        raise BadPrice("price is not a number") from e\n\ndef careless(text):\n    try:\n        return float(text)\n    except ValueError:\n        raise BadPrice("price is not a number")\n\nfor func in (strict, careless):\n    try:\n        func("abc")\n    except BadPrice as e:\n        print(e.__cause__)\n        print(type(e.__context__).__name__)')

nb.q("Real-life", """
    Check stock for each wanted item, printing the name and the quantity, or
    the name and `not stocked` for unknown items. Do it twice with the same
    output: first the **look before you leap** way (test with `in`), then the
    **easier to ask forgiveness** way (`try` / `except KeyError`).
""",
     given='stock = {"apple": 5, "pear": 0}\nwanted = ["apple", "kiwi", "pear"]',
     solution='for item in wanted:\n    if item in stock:\n        print(item, stock[item])\n    else:\n        print(item, "not stocked")\nfor item in wanted:\n    try:\n        print(item, stock[item])\n    except KeyError:\n        print(item, "not stocked")')

nb.q("Real-life", """
    Write `average(scores)` that starts with an `assert` that the list is not
    empty (message `no scores`) and returns the average. Call it for both
    lists; print the average, or the assertion message when it fails.
""",
     given="class_a = [70, 80, 90]\nclass_b = []",
     solution='def average(scores):\n    assert len(scores) > 0, "no scores"\n    return sum(scores) / len(scores)\nfor scores in (class_a, class_b):\n    try:\n        print(average(scores))\n    except AssertionError as e:\n        print(e)')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Real-life", """
    A download helper must try again. Write `retry(func, attempts)` that calls
    `func()` and returns its result. Each time `ConnectionError` is raised
    it prints `attempt`, the number and the message. On the last attempt it
    adds a note `gave up after N attempts` to the error and **re-raises** it
    (a bare `raise`). Call `retry(flaky, 2)` and print the error's first note
    when it escapes; then reset `calls["n"]` to 0 and print `retry(flaky, 3)`.
""",
     given='calls = {"n": 0}\n\ndef flaky():\n    calls["n"] += 1\n    if calls["n"] < 3:\n        raise ConnectionError("server busy")\n    return "data received"',
     solution='def retry(func, attempts):\n    for attempt in range(1, attempts + 1):\n        try:\n            return func()\n        except ConnectionError as e:\n            print("attempt", attempt, "failed:", e)\n            if attempt == attempts:\n                e.add_note(f"gave up after {attempts} attempts")\n                raise\n\ntry:\n    print(retry(flaky, 2))\nexcept ConnectionError as e:\n    print(e.__notes__[0])\ncalls["n"] = 0\nprint(retry(flaky, 3))')

nb.q("Puzzle", """
    `risky(err)` raises whatever exception it is given. Call it for each
    error in the list inside one `try` with four `except` clauses that print
    the **most specific** label: `key` for `KeyError`, `lookup` for any other
    `LookupError`, `math` for `ArithmeticError`, and `other` for everything
    else. Order the clauses so every error gets its best label.
""",
     given='def risky(err):\n    raise err\n\nerrors = [KeyError("a"), IndexError(3), ZeroDivisionError("zero"), ValueError("v")]',
     solution='for err in errors:\n    try:\n        risky(err)\n    except KeyError:\n        print("key")\n    except LookupError:\n        print("lookup")\n    except ArithmeticError:\n        print("math")\n    except Exception:\n        print("other")')

nb.q("Puzzle", """
    `stop()` simulates the user pressing Ctrl+C by raising
    `KeyboardInterrupt`. Show three outcomes, each printing one line. (1)
    Call `stop()` inside `except Exception`; when this does not catch it,
    an outer `except KeyboardInterrupt` prints `only the outer handler saw it`.
    (2) Call it inside `except BaseException as e` and print the class name.
    (3) Call it inside `except (Exception, KeyboardInterrupt)` and print `both kinds caught`.
""",
     given="def stop():\n    raise KeyboardInterrupt",
     solution='try:\n    try:\n        stop()\n    except Exception:\n        print("Exception caught it")\nexcept KeyboardInterrupt:\n    print("only the outer handler saw it")\ntry:\n    stop()\nexcept BaseException as e:\n    print(type(e).__name__)\ntry:\n    stop()\nexcept (Exception, KeyboardInterrupt):\n    print("both kinds caught")')

nb.q("Real-life", """
    A config file is checked before an app starts, and the user wants **every**
    problem at once. Write `validate(config)` that collects errors in a list:
    a `ValueError` for each value that is not valid (`port` must be digits;
    `host` must not be empty) and a `KeyError("timeout")` if the key
    `timeout` is missing. If the list is not empty it raises
    `ExceptionGroup("config problems", errors)`. Handle the group with
    `except* ValueError` (print `bad value:` and each message) and
    `except* KeyError` (print `missing:` and each key).
""",
     given='config = {"port": "80a", "host": ""}',
     solution='def validate(config):\n    errors = []\n    if not config["port"].isdigit():\n        errors.append(ValueError("port must be digits"))\n    if config["host"] == "":\n        errors.append(ValueError("host is empty"))\n    if "timeout" not in config:\n        errors.append(KeyError("timeout"))\n    if errors:\n        raise ExceptionGroup("config problems", errors)\n\ntry:\n    validate(config)\nexcept* ValueError as group:\n    for e in group.exceptions:\n        print("bad value:", e)\nexcept* KeyError as group:\n    for e in group.exceptions:\n        print("missing:", e.args[0])')

nb.project("Robust Record Parser", story="""
    A school exports student records as comma-separated lines (name, age,
    score). Some lines are broken. You are building a parser that never
    crashes and reports every bad line with its line number.
""",
     given='lines = [\n    "Ada,36,91.5",\n    "Grace,x,88",\n    "Linus,29",\n    "",\n    "Alan,41,95",\n    "Edsger,200,70",\n    "Margaret,85,abc",\n]',
     steps=[
         ("Define `RecordError(Exception)` and two children, `FieldCountError` and `BadValue` (one-line classes). Write `parse_line(line)` that splits on commas and returns a dict with `name`, `age` (int) and `score` (float). Raise `FieldCountError` when there are not exactly 3 fields, and `BadValue` when the age or score is not a number (raise it `from` the original error) or the age is outside 0 to 120. Print the result for the first line.",
          'class RecordError(Exception): pass\nclass FieldCountError(RecordError): pass\nclass BadValue(RecordError): pass\n\n'
          'def parse_line(line):\n    parts = line.split(",")\n    if len(parts) != 3:\n        raise FieldCountError(f"expected 3 fields, got {len(parts)}")\n'
          '    name, age_text, score_text = parts\n    try:\n        age = int(age_text)\n        score = float(score_text)\n    except ValueError as e:\n        raise BadValue(f"not a number in {line!r}") from e\n'
          '    if not 0 <= age <= 120:\n        raise BadValue(f"age {age} out of range")\n    return {"name": name, "age": age, "score": score}\n\nprint(parse_line(lines[0]))'),
         ("Write `parse_all(lines)` returning `(records, problems)`. Skip blank lines. Number the lines from 1; for each `RecordError`, add `(line_number, message)` to the problems. Print how many records and how many problems you got.",
          'def parse_all(lines):\n    records = []\n    problems = []\n    for number, line in enumerate(lines, 1):\n        if line.strip() == "":\n            continue\n        try:\n            records.append(parse_line(line))\n        except RecordError as e:\n            problems.append((number, str(e)))\n    return records, problems\n\nrecords, problems = parse_all(lines)\nprint(len(records), "records,", len(problems), "problems")'),
         ("Print a report: one line per problem like `line 2: message`, then one line per good record with the name and score.",
          'for number, message in problems:\n    print(f"line {number}: {message}")\nfor record in records:\n    print(record["name"], record["score"])'),
         ("Look at the chain behind a bad value. Parse `lines[1]` inside a `try`; when `BadValue` is raised, print its message, then the class name of its `__cause__` and the cause itself.",
          'try:\n    parse_line(lines[1])\nexcept BadValue as e:\n    print(e)\n    print(type(e.__cause__).__name__, e.__cause__)'),
         ("Write `check_all(lines)` that tries every non-blank line, adds the note `line N` to each `RecordError` (with `add_note`), and raises `ExceptionGroup(\"bad lines\", errors)` if there were any. Handle it with `except* FieldCountError` (print `count:`, the message and the first note) and `except* BadValue` (print `value:`, the message and the first note).",
          'def check_all(lines):\n    errors = []\n    for number, line in enumerate(lines, 1):\n        if line.strip() == "":\n            continue\n        try:\n            parse_line(line)\n        except RecordError as e:\n            e.add_note(f"line {number}")\n            errors.append(e)\n    if errors:\n        raise ExceptionGroup("bad lines", errors)\n\n'
          'try:\n    check_all(lines)\nexcept* FieldCountError as group:\n    for e in group.exceptions:\n        print("count:", e, e.__notes__[0])\nexcept* BadValue as group:\n    for e in group.exceptions:\n        print("value:", e, e.__notes__[0])'),
     ])

nb.build()
