# NB20 · Intermediate Capstone: Pageturner Library

The intermediate finale. This time the program is a real project: a
**library system** split across several Python files that you write in your
editor, building on a starter module written by a teammate that you must read,
fix and extend. You'll use classes and inheritance, custom exceptions, JSON
saving and loading, a CSV report, `datetime`, `Counter` and `match`.
Everything from NB09 to NB19 is fair game.

## You'll need

- NB09 to NB19: all intermediate notebooks

## You'll practise

- Building one real program (about 300 lines) split across several Python modules
- Reading and extending a teammate's starter module
- Classes, exceptions, files/JSON and the standard library working together

## The story

*Pageturner* is a small town library whose records live in a spreadsheet and
a lot of sticky notes. Your teammate Dana started a Python catalog module
(`catalog.py`) before going on holiday, and she left it unreviewed: it
works, but it has a few rough edges. You'll read it, extend it, and build the
rest of the program around it in separate modules: members, lending rules
with fines, saving to JSON, a CSV report, and finally a whole month of
activity (`events.json`) processed end to end by `main.py`.

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
| `catalog.py` | starter file: read it |
| `books.json` | starter file: read it |
| `events.json` | starter file: read it |
| `shelves.py` | **you write it** (milestone 1) |
| `members.py` | **you write it** (milestone 2) |
| `library.py` | **you write it** (milestone 3, 5) |
| `storage.py` | **you write it** (milestone 4) |
| `main.py` | **you write it** (milestone 6) |
| `demo_1.py` … `demo_6.py` | shows each milestone working (don't edit) |
| `check.py` | checks your milestones |
| `solution/` | the reference answer (look only after a real attempt) |

## Milestone 1 · Shelves

Read `catalog.py` carefully before changing anything. Dana's `Catalog.add` silently
overwrites a book with the same ISBN, and her `search` is case-sensitive. In a new file
`shelves.py` write a custom error `DuplicateBook` (a `LibraryError`) and a subclass
`SmartCatalog(Catalog)` that raises it on duplicates (reuse the parent's `add` with
`super()`), searches case-insensitively, and has `by_author()` returning a dict of
author to sorted list of titles. Add `load_catalog(path)` that reads a JSON list of
book records into a `SmartCatalog` and returns it together with a list of messages
about the records it had to skip: duplicates and records with a missing field. The
demo loads `books.json` and prints the number of books, each skipped message, the
titles found by searching "AUSTEN", and `by_author()`.

**You write:** `shelves.py` · **Check:** `python check.py 1`

**Expected output** (`python demo_1.py`):

```text
Books loaded: 5
Skipped: ISBN 111 is already in the catalog
Skipped: record 666 is missing 'title'
Emma by Jane Austen (1815)
Persuasion by Jane Austen (1817)
{'Frank Herbert': ['Dune'], 'William Gibson': ['Neuromancer'], 'Jane Austen': ['Emma', 'Persuasion'], 'Dan Simmons': ['Hyperion']}
```

## Milestone 2 · Members

Create `members.py`. It imports `LibraryError` from `catalog` and defines two errors,
`LimitReached` and `FineOwed`, then a `Member` class with the class attributes
`limit = 2` and `loan_days = 14`, a name, a `loans` dict (ISBN to due date) and
`fines` in cents. Give it `kind()` returning `"standard"`, `check()` which raises
`FineOwed` when fines are above zero and `LimitReached` when the member already has
`limit` loans, and `__str__`. Add `PremiumMember(Member)` with limit 4, 21 loan days
and kind `"premium"`. The demo creates one member of each kind and prints them with
their limits, then fills a standard member's loans with two fake entries and prints
the message from the error that `check()` raises.

**You write:** `members.py` · **Check:** `python check.py 2`

**Expected output** (`python demo_2.py`):

```text
Ana (standard) 2 14
Bo (premium) 4 21
Blocked: Ana already has 2 books
```

## Milestone 3 · Library

Create `library.py` with a `Library` class that holds a catalog, a dict of members
and a `history` list of `(date text, "out" or "back", member, isbn)` tuples. Define
the errors `UnknownMember`, `NoCopiesLeft` and `NotBorrowed`, and a fine of 25 cents
per late day. Methods: `join(name, premium=False)`, `member(name)`,
`checkout(name, isbn, today)` (member check, then copy check, then update `on_loan`,
the member's loans and the history, and return the due date),
`give_back(name, isbn, today)` (returns the fine in cents and adds it to the member),
`pay(name)` and `overdue(today)` returning sorted `(name, isbn, days late)` tuples.
The demo checks out Dune for Ana on 2026-03-03 and prints the due date, returns it
ten days late and prints the fine, then tries three failing checkouts (an unknown
member, an unknown book, a member who owes a fine) and prints each error class name
and message.

**You write:** `library.py` · **Check:** `python check.py 3`

**Expected output** (`python demo_3.py`):

```text
Due: 2026-03-17
Fine: 250
UnknownMember - Zed is not a member
BookNotFound - no book with ISBN 999
FineOwed - Ana owes 250 cents
```

## Milestone 4 · Saving and the CSV report

Create `storage.py` with a `StorageError` and four functions. `save_state(library,
path)` writes books (with their `on_loan` counts), members (name, premium flag,
fines, loans as ISO date text) and the history to a JSON file with indent 2.
`load_state(path)` rebuilds an equal `Library`, turning date text back into `date`
objects and the history lists back into tuples; a missing file must raise
`StorageError` (use `from None`). `write_loans_csv(library, path)` writes a CSV with
the columns member, isbn, title, due, sorted by member, and `read_loans_csv` reads it
back with `DictReader`. The demo builds a library with a few loans, saves and reloads
it inside a temporary folder and prints whether the history and Bo's loans match,
writes the CSV and prints its rows, and finally loads a missing file and prints the
error.

**You write:** `storage.py` · **Check:** `python check.py 4`

**Expected output** (`python demo_4.py`):

```text
True
True
250 premium
{'member': 'Bo', 'isbn': '333', 'title': 'Emma', 'due': '2026-03-26'}
StorageError: no saved state
```

## Milestone 5 · A month of events

`events.json` holds a month of library activity: a list of `[date text, action,
member, ...]` records. Extend `library.py` with a function `run_events(library,
events)`. For each event convert the date with `date.fromisoformat` and use `match`
on the remaining items: `["join", name]`, `["join", name, "premium"]`, `["out", name,
isbn]`, `["back", name, isbn]`, `["pay", name]`, and a default case that raises
`LibraryError` for an unknown action. Wrap the handling in `try`/`except
LibraryError` so one bad event never stops the run. Return a list of `(date text,
ok, message)` tuples, where the message of a failure is the error class name and its
text. The demo loads the events, runs them on a fresh library and prints every
outcome as one line: the date, `ok` or `FAILED`, and the message.

**You write:** `library.py` · **Check:** `python check.py 5`

**Expected output** (`python demo_5.py`):

```text
2026-03-02 ok     Ana joined
2026-03-02 ok     Bo joined as premium
2026-03-02 ok     Cy joined
2026-03-03 ok     Ana took 111, due 2026-03-17
2026-03-03 ok     Ana took 222, due 2026-03-17
2026-03-03 FAILED LimitReached: Ana already has 2 books
2026-03-04 FAILED NoCopiesLeft: Neuromancer has no copies left
2026-03-04 ok     Bo took 111, due 2026-03-25
2026-03-05 FAILED BookNotFound: no book with ISBN 999
2026-03-06 FAILED UnknownMember: Dee is not a member
2026-03-20 ok     Ana returned 111, fine 75
2026-03-20 FAILED FineOwed: Ana owes 75 cents
2026-03-21 FAILED NotBorrowed: Cy has not borrowed 555
2026-03-21 ok     Ana paid 75
2026-03-21 ok     Ana took 444, due 2026-04-04
2026-03-22 ok     Bo returned 111, fine 0
2026-03-22 FAILED LibraryError: unknown action dance
```

## Milestone 6 · The finale

The finale: write `main.py`, which runs the whole program from scratch. Define a
function `main()` and end the file with `if __name__ == "__main__": main()`. It
loads the catalog from `books.json`, creates a new `Library`, runs all the events from
`events.json`, saves the state to a JSON file in a temporary folder, loads it back
into `reloaded` and uses only `reloaded` for the report. Print a title line, then:
the number of events that succeeded and failed, the failures counted by error class
name (use `Counter`, print its `most_common()` result), the books still on loan as
`title -> member (due date)` lines, the overdue list as of 2026-04-10, each member's
fines in dollars with 2 decimals (alphabetical), and the title of the most borrowed
book from the history. Write the loans CSV in the temporary folder too and print how
many data rows it has. Find the data files next to `main.py` (with `Path(__file__)`),
not in the current folder. The demo just calls `main()`.

**You write:** `main.py` · **Check:** `python check.py 6`

**Expected output** (`python demo_6.py`):

```text
=== PAGETURNER LIBRARY: MARCH REPORT ===
Events ok: 10 failed: 7
Failures: [('LimitReached', 1), ('NoCopiesLeft', 1), ('BookNotFound', 1), ('UnknownMember', 1), ('FineOwed', 1), ('NotBorrowed', 1), ('LibraryError', 1)]
On loan:
  Neuromancer -> Ana (due 2026-03-17)
  Persuasion -> Ana (due 2026-04-04)
Overdue on 2026-04-10: [('Ana', '222', 24), ('Ana', '444', 6)]
Fines:
  Ana $0.00
  Bo  $0.00
  Cy  $0.00
Most borrowed: Dune
CSV rows: 2
```

## Done

On to the advanced tier: **NB21 · OOP Advanced** in `advanced/`.
