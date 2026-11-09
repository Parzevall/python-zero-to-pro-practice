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
    1: "Books loaded: 5\nSkipped: ISBN 111 is already in the catalog\nSkipped: record 666 is missing 'title'\nEmma by Jane Austen (1815)\nPersuasion by Jane Austen (1817)\n{'Frank Herbert': ['Dune'], 'William Gibson': ['Neuromancer'], 'Jane Austen': ['Emma', 'Persuasion'], 'Dan Simmons': ['Hyperion']}",
    2: 'Ana (standard) 2 14\nBo (premium) 4 21\nBlocked: Ana already has 2 books',
    3: 'Due: 2026-03-17\nFine: 250\nUnknownMember - Zed is not a member\nBookNotFound - no book with ISBN 999\nFineOwed - Ana owes 250 cents',
    4: "True\nTrue\n250 premium\n{'member': 'Bo', 'isbn': '333', 'title': 'Emma', 'due': '2026-03-26'}\nStorageError: no saved state",
    5: '2026-03-02 ok     Ana joined\n2026-03-02 ok     Bo joined as premium\n2026-03-02 ok     Cy joined\n2026-03-03 ok     Ana took 111, due 2026-03-17\n2026-03-03 ok     Ana took 222, due 2026-03-17\n2026-03-03 FAILED LimitReached: Ana already has 2 books\n2026-03-04 FAILED NoCopiesLeft: Neuromancer has no copies left\n2026-03-04 ok     Bo took 111, due 2026-03-25\n2026-03-05 FAILED BookNotFound: no book with ISBN 999\n2026-03-06 FAILED UnknownMember: Dee is not a member\n2026-03-20 ok     Ana returned 111, fine 75\n2026-03-20 FAILED FineOwed: Ana owes 75 cents\n2026-03-21 FAILED NotBorrowed: Cy has not borrowed 555\n2026-03-21 ok     Ana paid 75\n2026-03-21 ok     Ana took 444, due 2026-04-04\n2026-03-22 ok     Bo returned 111, fine 0\n2026-03-22 FAILED LibraryError: unknown action dance',
    6: "=== PAGETURNER LIBRARY: MARCH REPORT ===\nEvents ok: 10 failed: 7\nFailures: [('LimitReached', 1), ('NoCopiesLeft', 1), ('BookNotFound', 1), ('UnknownMember', 1), ('FineOwed', 1), ('NotBorrowed', 1), ('LibraryError', 1)]\nOn loan:\n  Neuromancer -> Ana (due 2026-03-17)\n  Persuasion -> Ana (due 2026-04-04)\nOverdue on 2026-04-10: [('Ana', '222', 24), ('Ana', '444', 6)]\nFines:\n  Ana $0.00\n  Bo  $0.00\n  Cy  $0.00\nMost borrowed: Dune\nCSV rows: 2",
}
TITLES = {
    1: 'Shelves',
    2: 'Members',
    3: 'Library',
    4: 'Saving and the CSV report',
    5: 'A month of events',
    6: 'The finale',
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
