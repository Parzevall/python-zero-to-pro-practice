"""Check your milestones.

    python check.py            check every milestone
    python check.py 3          check milestone 3 and show the difference if it's wrong
    python check.py --solution run the reference solution instead of your code

Each milestone has a demo script (demo_1.py, demo_2.py, ...) that uses your
modules. This runs it and compares what it prints with the expected output.
"""

import difflib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    1: "First: Order(id=1001, customer='ana', sku='KB-01', qty=2, price=45.5, currency='USD')\nWARNING orderflow.models: rejected line 4: bad number (invalid literal for int() with base 10: 'abc')\nWARNING orderflow.models: rejected line 7: missing customer\nWARNING orderflow.models: rejected line 8: qty and price must be positive\nThen 7 more orders\nRejected: line 4: bad number (invalid literal for int() with base 10: 'abc') | bad number (invalid literal for int() with base 10: 'abc')\nRejected: line 7: missing customer | missing customer\nRejected: line 8: qty and price must be positive | qty and price must be positive",
    2: "INFO orderflow.registry: loaded plugin pipeline_steps\n['drop_tiny', 'tag_bulk', 'tag_big']\nINFO orderflow.registry: step drop_tiny dropped order 1\n2 ['bulk', 'big']\n3 []\nDropped: [1]\nValueError: step 'tag_big' is already registered",
    3: 'INFO orderflow.resources: opened good.jsonl\nINFO orderflow.resources: closed good.jsonl with 2 records\nCount: 2\n[1, 2]\nINFO orderflow.resources: opened bad.jsonl\nERROR orderflow.resources: rolled back bad.jsonl after RuntimeError\nCaught: disk on fire | file exists: False\nINFO orderflow.resources: empty block took 0.50s',
    4: "WARNING orderflow.source: attempt 1/3 failed: GBP service busy\nWARNING orderflow.source: attempt 2/3 failed: GBP service busy\nEUR 1.1\nGBP 1.3\nJPY UnknownCurrency\nUSD 1.0\nCalls: {'EUR': 1, 'GBP': 3, 'JPY': 1, 'USD': 1}\nHighest concurrency: 2",
    5: "WARNING orderflow.models: rejected line 4: bad number (invalid literal for int() with base 10: 'abc')\nWARNING orderflow.models: rejected line 7: missing customer\nWARNING orderflow.models: rejected line 8: qty and price must be positive\nINFO orderflow.resources: read took 0.50s\nWARNING orderflow.source: attempt 1/3 failed: GBP service busy\nINFO orderflow.resources: rates took 0.50s\nINFO orderflow.resources: opened out.jsonl\nWARNING orderflow.source: skipping order 1009: no rate for JPY\nINFO orderflow.registry: step drop_tiny dropped order 1011\nINFO orderflow.resources: closed out.jsonl with 6 records\nINFO orderflow.runner: steps used: ['drop_tiny', 'tag_bulk', 'tag_big']\nRead: 11 Written: 6\n[1001, 1002, 1004, 1005, 1008, 1010]",
    6: 'Success: True\nTests run: 13\nFailures: 0 Errors: 0',
    7: "WARNING orderflow.models: rejected line 4: bad number (invalid literal for int() with base 10: 'abc')\nWARNING orderflow.models: rejected line 7: missing customer\nWARNING orderflow.models: rejected line 8: qty and price must be positive\nINFO orderflow.resources: read took 0.50s\nWARNING orderflow.source: attempt 1/3 failed: GBP service busy\nINFO orderflow.resources: rates took 0.50s\nINFO orderflow.resources: opened out.jsonl\nWARNING orderflow.source: skipping order 1009: no rate for JPY\nINFO orderflow.registry: step drop_tiny dropped order 1011\nINFO orderflow.resources: closed out.jsonl with 6 records\nINFO orderflow.runner: steps used: ['drop_tiny', 'tag_bulk', 'tag_big']\n=== ORDERFLOW REPORT ===\nRows read: 11, rejected: 3\nSkipped (no rate): [1009]\nDropped by steps: [1011]\nWritten: 6\nTags: {'big': 2, 'bulk': 1}\nRevenue by customer (USD):\n  ana  3 order(s)    239.97\n  bo   2 order(s)    483.99\n  dee  1 order(s)    273.00\n\nLines in output file: 6 | matches report: True",
}
TITLES = {
    1: 'Models and the streaming reader',
    2: 'The plugin registry',
    3: 'Resources that clean up after themselves',
    4: 'Async rates with retries',
    5: 'Enrich and run: the runner',
    6: 'A real test suite',
    7: 'The finale: main.py',
}


def run_demo(n, folder):
    try:
        proc = subprocess.run([sys.executable, f"demo_{n}.py"], cwd=folder, text=True,
                              capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "", "timed out after 120 seconds (an endless loop?)"
    return proc.stdout.rstrip("\n"), proc.stderr.strip()


def main():
    args = sys.argv[1:]
    use_solution = "--solution" in args
    picked = [int(a) for a in args if a.isdigit()]
    numbers = picked or sorted(EXPECTED)
    folder = HERE
    if use_solution:
        tmp = tempfile.mkdtemp()
        for path in HERE.iterdir():
            if path.is_file() and path.name != "check.py":
                shutil.copy(path, tmp)
        for path in (HERE / "solution").iterdir():
            shutil.copy(path, tmp)
        folder = tmp
    passed = 0
    for n in numbers:
        out, err = run_demo(n, folder)
        ok = out == EXPECTED[n]
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  Milestone {n}: {TITLES[n]}")
        if not ok and (picked or use_solution):
            if err:
                print("\n  Your code raised an error. The last lines:\n")
                print(textwrap_indent("\n".join(err.splitlines()[-8:])))
            print("\n  Difference (- expected, + yours):\n")
            diff = difflib.unified_diff(EXPECTED[n].splitlines(), out.splitlines(),
                                        "expected", "yours", lineterm="", n=1)
            print(textwrap_indent("\n".join(list(diff)[2:]) or "(no output)"))
            print()
    print(f"\n{passed} of {len(numbers)} passed.")
    if not picked and passed < len(numbers):
        print("Run  python check.py N  to see what's different for milestone N.")


def textwrap_indent(text):
    return "\n".join("    " + line for line in text.splitlines())


if __name__ == "__main__":
    main()
