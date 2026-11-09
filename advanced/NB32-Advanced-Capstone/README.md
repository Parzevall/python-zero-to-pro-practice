# NB32 · Advanced Capstone: Orderflow: an order-processing pipeline

The course finale. You will build **orderflow**, a small but real project of
seven files: typed models and a streaming CSV reader, a plugin registry
built from decorators, a context manager for output files, an async rate
fetcher with retries (talking to a fake in-process service, so no network),
a runner that wires everything together, a unittest suite and a `main.py`
you can run like a real program. Everything from NB21 to NB31 is fair game,
but only where it genuinely helps: a good design uses the right tool, not
every tool.

## You'll need

- NB21 to NB31: all advanced notebooks

## You'll practise

- Building a small real package (about 500 lines) step by step
- Tests, logging, type hints and clean structure on a real codebase
- Bringing the advanced topics together where they genuinely help

## The story

A small online shop exports its orders as a CSV file, and it is messy:
bad numbers, missing names, negative quantities, and a currency nobody has
a rate for. You are building **orderflow**, a package that streams the
orders, converts every total to US dollars with rates fetched from a
(fake, in-process) exchange service, runs the orders through pluggable
steps, writes the survivors to a JSON-lines file and prints a report.
The modules are flat files named `pipeline_*.py`. Some of them grow over
several milestones: keep extending the same file, because each demo uses
your latest version. Your code logs through the `logging` module; the demos
configure it to print to the terminal.

## How to work

This is a real project, not a notebook. Open this folder in your editor (VS Code: *File → Open Folder*) and a terminal in it.

1. Read the milestone below, then write the code in the file(s) it names.
2. Run `python demo_N.py` to watch your code run, or `python check.py N` to compare its output with the expected output and see the difference.
3. `python check.py` checks every milestone at once.
4. Stuck after a real attempt? `solution/` has the answer, and `python check.py --solution` runs it.

Each demo imports your modules fresh, so after editing a file just run it again.

## Files

| File | What it is |
|---|---|
| `orders.csv` | starter file: read it |
| `pipeline_models.py` | **you write it** (milestone 1, 2) |
| `pipeline_registry.py` | **you write it** (milestone 2) |
| `pipeline_steps.py` | **you write it** (milestone 2) |
| `pipeline_resources.py` | **you write it** (milestone 3) |
| `pipeline_source.py` | **you write it** (milestone 4, 5) |
| `pipeline_runner.py` | **you write it** (milestone 5) |
| `test_pipeline.py` | **you write it** (milestone 6) |
| `main.py` | **you write it** (milestone 7) |
| `demo_1.py` … `demo_7.py` | shows each milestone working (don't edit) |
| `check.py` | checks your milestones |
| `solution/` | the reference answer (look only after a real attempt) |

## Milestone 1 · Models and the streaming reader

Create `pipeline_models.py`. It needs a base error `PipelineError` and `BadRecord(PipelineError)`
that remembers the `line` and a `reason` (message `line N: reason`). Add a frozen, slotted
dataclass `Order` (id, customer, sku, qty, price, currency) with a `total` property rounded to
2 decimals. Write `parse_order(row, line)` which strips and lowercases the customer, uppercases
sku and currency, and raises `BadRecord` for a missing customer, a number that does not parse,
or a non-positive qty or price. Then write the generator `read_orders(lines, rejects=None)`
using `csv.DictReader`: it yields valid orders one at a time and logs a warning for each bad
row, appending the error to `rejects`. `demo_1.py` reads `orders.csv` and shows the stream is
lazy (the first order, then the rest) and then lists each rejected error with its reason.
Run it with `python check.py 1`.

**You write:** `pipeline_models.py` · **Check:** `python check.py 1`

**Expected output** (`python demo_1.py`):

```text
First: Order(id=1001, customer='ana', sku='KB-01', qty=2, price=45.5, currency='USD')
WARNING orderflow.models: rejected line 4: bad number (invalid literal for int() with base 10: 'abc')
WARNING orderflow.models: rejected line 7: missing customer
WARNING orderflow.models: rejected line 8: qty and price must be positive
Then 7 more orders
Rejected: line 4: bad number (invalid literal for int() with base 10: 'abc') | bad number (invalid literal for int() with base 10: 'abc')
Rejected: line 7: missing customer | missing customer
Rejected: line 8: qty and price must be positive | qty and price must be positive
```

## Milestone 2 · The plugin registry

Extend `pipeline_models.py` with a mutable dataclass `Enriched` (an `order`, a `usd_total` and a
`tags` list that defaults to empty) and a `TypedDict` `CustomerTotals` with `orders` and
`revenue`. Then create `pipeline_registry.py` with a decorator factory `step(name, *, order)`
that stores the decorated function in a module-level dict (refuse a duplicate name with
`ValueError`), `registered()` returning the names sorted by order, `load_plugins(*module_names)`
that imports each module with `importlib` and logs it, and the generator
`run_steps(items, names=None, dropped=None)`: each item goes through the chosen steps in order,
a step that returns `None` drops the item (log it and append it to `dropped`), and unknown step
names raise `KeyError`. In `pipeline_steps.py` register `drop_tiny` (order 10, drops items
under 20 dollars), `tag_bulk` (20, tag "bulk" when qty is at least 3) and `tag_big` (30, tag
"big" at 100 dollars or more). `demo_2.py` loads the plugins, runs three hand-made items
through the steps and tries to register `"tag_big"` twice.

**You write:** `pipeline_models.py`, `pipeline_registry.py`, `pipeline_steps.py` · **Check:** `python check.py 2`

**Expected output** (`python demo_2.py`):

```text
INFO orderflow.registry: loaded plugin pipeline_steps
['drop_tiny', 'tag_bulk', 'tag_big']
INFO orderflow.registry: step drop_tiny dropped order 1
2 ['bulk', 'big']
3 []
Dropped: [1]
ValueError: step 'tag_big' is already registered
```

## Milestone 3 · Resources that clean up after themselves

Create `pipeline_resources.py` for things that must be cleaned up. Write a `FakeClock` class:
calling an instance adds a fixed step (default 0.5) to its time and returns it, so timings are
repeatable. Write the class-based context manager `JsonlSink(path)`: on entering it opens the
file and returns itself, `write(item)` appends `json.dumps(asdict(item), sort_keys=True)` as a
line and counts it, and on exit it closes the file; if the block failed it also deletes the
half-written file, logs an error and lets the exception continue. Write a `@contextmanager`
`stopwatch(label, clock)` that logs `label took X.XXs` even if the block fails, and a generator
`read_jsonl(path)` yielding one dict per line. `demo_3.py` writes two items through a sink in a
temporary folder and reads them back, raises `RuntimeError` inside a second sink to show its
file is gone, and times an empty block with a `FakeClock`.

**You write:** `pipeline_resources.py` · **Check:** `python check.py 3`

**Expected output** (`python demo_3.py`):

```text
INFO orderflow.resources: opened good.jsonl
INFO orderflow.resources: closed good.jsonl with 2 records
Count: 2
[1, 2]
INFO orderflow.resources: opened bad.jsonl
ERROR orderflow.resources: rolled back bad.jsonl after RuntimeError
Caught: disk on fire | file exists: False
INFO orderflow.resources: empty block took 0.50s
```

## Milestone 4 · Async rates with retries

Create `pipeline_source.py`, the async part. Define `TransientError` and `UnknownCurrency` (both
`PipelineError`s), and a decorator `retry(times)` for async functions: it catches only
`TransientError`, logs `attempt N/M failed: ...` and re-raises on the last attempt (use
`functools.wraps`, and `ParamSpec`/`TypeVar` so type checkers keep the signature).
`FakeRateSource` is the fake service: its rates are USD 1.0, EUR 1.10, GBP 1.30;
`flaky={"GBP": 2}` makes the first two GBP calls fail transiently; an unknown currency raises
`UnknownCurrency`; it counts calls per currency in a `Counter` and records the highest number of
calls running at the same time (`await asyncio.sleep(0)` inside gives other tasks a turn).
Write `fetch_rate(source, currency)` with `@retry(times=3)`, then
`async fetch_rates(currencies, source, limit=2)` which fetches every distinct currency
concurrently with an `asyncio.Semaphore` and `gather(..., return_exceptions=True)` and returns a
dict of currency to rate, or to the `PipelineError` that happened. `demo_4.py` runs it with
`asyncio.run(main())` on USD, EUR, GBP and JPY with a flaky GBP and prints the results, the calls
per currency and the highest concurrency.

**You write:** `pipeline_source.py` · **Check:** `python check.py 4`

**Expected output** (`python demo_4.py`):

```text
WARNING orderflow.source: attempt 1/3 failed: GBP service busy
WARNING orderflow.source: attempt 2/3 failed: GBP service busy
EUR 1.1
GBP 1.3
JPY UnknownCurrency
USD 1.0
Calls: {'EUR': 1, 'GBP': 3, 'JPY': 1, 'USD': 1}
Highest concurrency: 2
```

## Milestone 5 · Enrich and run: the runner

First extend `pipeline_source.py` with the generator `enrich(orders, rates, skipped=None)`: it
yields `Enriched` objects with the total converted to dollars (2 decimals), and logs and skips
any order with no usable rate, appending it to `skipped`. Then create `pipeline_runner.py`, which
wires every module together. A `Report` dataclass holds the number of rows read, the list of
rejected errors, the ids skipped for a missing rate, the ids dropped by steps and the list of
written `Enriched` items. Give it `totals()` (customer to a `CustomerTotals` with order count
and revenue, rounded to 2 decimals) and `render()` returning the report text: a title line
`=== ORDERFLOW REPORT ===`, rows read and rejected, the skipped ids, the dropped ids, the
written count, the tag counts (a sorted dict) and a revenue line per customer, alphabetical,
with the amount right-aligned to 8 wide. Then write `async run_pipeline(source_path,
output_path, rate_source, clock, steps=None)`: read all orders (timed with
`stopwatch("read", clock)`), fetch the distinct currencies (timed as `rates`), enrich, run the
steps and write the survivors inside a `JsonlSink`, and return the `Report`. `demo_5.py` runs it
on `orders.csv` into a temporary folder and prints the number read, the number written and the
written order ids.

**You write:** `pipeline_source.py`, `pipeline_runner.py` · **Check:** `python check.py 5`

**Expected output** (`python demo_5.py`):

```text
WARNING orderflow.models: rejected line 4: bad number (invalid literal for int() with base 10: 'abc')
WARNING orderflow.models: rejected line 7: missing customer
WARNING orderflow.models: rejected line 8: qty and price must be positive
INFO orderflow.resources: read took 0.50s
WARNING orderflow.source: attempt 1/3 failed: GBP service busy
INFO orderflow.resources: rates took 0.50s
INFO orderflow.resources: opened out.jsonl
WARNING orderflow.source: skipping order 1009: no rate for JPY
INFO orderflow.registry: step drop_tiny dropped order 1011
INFO orderflow.resources: closed out.jsonl with 6 records
INFO orderflow.runner: steps used: ['drop_tiny', 'tag_bulk', 'tag_big']
Read: 11 Written: 6
[1001, 1002, 1004, 1005, 1008, 1010]
```

## Milestone 6 · A real test suite

Write `test_pipeline.py`, a `unittest` suite that covers every module: parsing (normalisation,
`BadRecord` carries its line number, `read_orders` returns a generator and skips bad rows,
`Order` is frozen), the registry (built-in order, duplicate names refused, drop and tag
behaviour, unknown step), the sink (success, and the file is gone after a failure) and, in an
`IsolatedAsyncioTestCase`, the retry decorator (recovers; gives up after 3 attempts), the
concurrency limit with an unknown currency, and a full run in a temporary directory. Use
in-memory rows and `tempfile`, not `orders.csv`, so the suite does not depend on other files, and
finish with the usual `if __name__ == "__main__": unittest.main()`. This is a real script now,
so `python -m unittest test_pipeline` works from the project folder. `demo_6.py` loads your
suite, runs it with a `TextTestRunner` that writes to a `StringIO` and prints whether the run
was successful, how many tests ran and the number of failures and errors.

**You write:** `test_pipeline.py` · **Check:** `python check.py 6`

**Expected output** (`python demo_6.py`):

```text
Success: True
Tests run: 13
Failures: 0 Errors: 0
```

## Milestone 7 · The finale: main.py

Write `main.py`, the entry point. Define `main(source="orders.csv", output="orders_out.jsonl")`
which builds a `FakeRateSource` with `flaky={"GBP": 1}`, runs `run_pipeline` with
`asyncio.run` (never a top-level `await`) and a `FakeClock`, prints the report text and returns
the `Report`. Import `pipeline_steps` so the built-in steps are registered. Close the file with
`if __name__ == "__main__":`, set up `logging.basicConfig` to print to stdout there and call
`main()`, so `python main.py` runs the real thing while importing the module does nothing.
`demo_7.py` imports your `main` function and calls it on `orders.csv` with the output going to a
temporary folder, so the report is printed, and then shows the output file has one line per
written order.

**You write:** `main.py` · **Check:** `python check.py 7`

**Expected output** (`python demo_7.py`):

```text
WARNING orderflow.models: rejected line 4: bad number (invalid literal for int() with base 10: 'abc')
WARNING orderflow.models: rejected line 7: missing customer
WARNING orderflow.models: rejected line 8: qty and price must be positive
INFO orderflow.resources: read took 0.50s
WARNING orderflow.source: attempt 1/3 failed: GBP service busy
INFO orderflow.resources: rates took 0.50s
INFO orderflow.resources: opened out.jsonl
WARNING orderflow.source: skipping order 1009: no rate for JPY
INFO orderflow.registry: step drop_tiny dropped order 1011
INFO orderflow.resources: closed out.jsonl with 6 records
INFO orderflow.runner: steps used: ['drop_tiny', 'tag_bulk', 'tag_big']
=== ORDERFLOW REPORT ===
Rows read: 11, rejected: 3
Skipped (no rate): [1009]
Dropped by steps: [1011]
Written: 6
Tags: {'big': 2, 'bulk': 1}
Revenue by customer (USD):
  ana  3 order(s)    239.97
  bo   2 order(s)    483.99
  dee  1 order(s)    273.00

Lines in output file: 6 | matches report: True
```

## Done

That's the whole course. Well played.
