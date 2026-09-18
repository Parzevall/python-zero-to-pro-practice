# pythonsprints — Design Spec

**Date:** 2026-09-18
**Status:** Approved (design), pending implementation plan

## 1. Goal

Build Python fluency to a rock-solid foundation level within days, by solving
400 labeled practice questions across 10 Jupyter notebooks. Every P0 topic from
the Programming Foundations syllabus is covered, each question is labeled with
its difficulty inside its topic notebook, and each ships a hidden hint, a hidden
solution with reasoning, and an automatic correctness check.

**Success criteria:**

- 400 questions exist, each with prompt, difficulty label, hint, solution,
  explanation, and executable test cases.
- Every reference solution passes its own checker (enforced at build time).
- Every P0 topic meets its minimum question quota.
- The learner can run all 10 notebooks in `~/.venvs/ds` with zero setup beyond
  one editable install.

## 2. Environment

Target interpreter: `/home/topg/.venvs/ds/bin/python` (Python 3.13.14, uv-created).

Verified present: JupyterLab 4.6.1, notebook 7.6.0, ipykernel 7.3.0,
ipywidgets 8.1.8, numpy 2.5.1, pandas 3.0.3, matplotlib 3.11.0, requests 2.34.2.
Kernel `Python 3.13 (ds)` is registered at
`~/.local/share/jupyter/kernels/ds`.

**Gap:** `pytest` is not installed, and P0 requires it. Phase 0 runs:

```
uv pip install --python ~/.venvs/ds/bin/python pytest
```

No other dependency is added. The question content itself is pure standard
library — numpy/pandas are not used, because the objective is core Python.

## 3. Architecture

### 3.1 Generated notebooks, single source of truth

Notebooks are generated, not hand-authored. Each question is one `Question`
object holding prompt, level, topic, starter code, hint, solution, explanation,
and test cases together. `build.py` renders that object into the notebook, and `sprintcheck` reads the
same object directly at runtime:

```
content/nb07_comprehensions.py   <-- ONE Question object
        |
        +-- build.py ------------> notebooks/07_comprehensions.ipynb  (learner opens)
        +-- sprintcheck.registry -> imports content/ live at check() time
```

`registry.py` imports the content modules rather than being code-generated from
them. Generating a third artifact would add a drift class the design exists to
eliminate, and the content package ships in the repo regardless.

**Rationale:** at 400 questions, hand-authored notebook JSON would let the
solution, the hint and the test cases drift apart silently. Because both
artifacts derive from one object, the build can execute every reference solution
against its own cases and fail if any one does not pass. That is the property
that makes 400 questions trustworthy without hand-verification.

**Accepted cost:** one indirection layer the learner rarely opens.

### 3.2 Protecting the learner's answers

`build.py` **skips** any notebook file that already exists and prints a warning.
Overwriting requires an explicit `--force`. The repo is a git repo from Phase 0,
so solved work is recoverable. `build.py --check` verifies that generated output
would match the content source, without writing anything — used by CI/tests.

### 3.3 Repository layout

```
pythonsprints/
|-- README.md                 how to start; suggested daily plan
|-- pyproject.toml            editable install so `import sprintcheck` works
|-- build.py                  content/ -> notebooks/ + registry
|-- content/                  SOURCE OF TRUTH
|   |-- __init__.py
|   |-- schema.py             Question, Case, Level, Topic definitions
|   |-- nb01_foundations.py
|   |-- ... (nb02 .. nb10)
|-- sprintcheck/
|   |-- __init__.py           public API: check(), progress(), reset()
|   |-- runner.py             case execution, diffing, formatting
|   |-- registry.py           lazily imports content/ -> qid -> Question
|   |-- inspect_source.py     AST helpers for `custom` constraint cases
|-- notebooks/                GENERATED ONCE - the learner works here
|   |-- 01_foundations_and_operators.ipynb
|   |-- ... (02 .. 10)
|-- tests/
|   |-- test_content_integrity.py
|   |-- test_solutions_pass.py
|   |-- test_coverage.py
|-- .sprintcheck_progress.json   GENERATED at runtime, gitignored
```

## 4. Notebook map

Split is **by topic**, with difficulty ramping L1 -> L5 *inside* each notebook.
Every notebook ends on L5 questions so the learner is always stretched.

| # | File | Q | ID block | P0 topics |
|---|------|---|----------|-----------|
| 01 | `01_foundations_and_operators.ipynb` | 36 | Q-001..Q-036 | interpreter, venv, pip, variables, primitive types, dynamic typing, casting, arithmetic/comparison/logical/identity/membership operators |
| 02 | `02_strings.ipynb` | 38 | Q-037..Q-074 | indexing, slicing, f-strings, string methods |
| 03 | `03_lists_and_tuples.ipynb` | 38 | Q-075..Q-112 | lists, tuples, mutability, copying, packing/unpacking |
| 04 | `04_dicts_and_sets.ipynb` | 38 | Q-113..Q-150 | dicts, sets, hashability, views, set algebra |
| 05 | `05_control_flow_and_loops.ipynb` | 36 | Q-151..Q-186 | if/elif/else, for, while, range, break, continue, else-on-loop |
| 06 | `06_functions_scope_closures.ipynb` | 42 | Q-187..Q-228 | definition, arguments, defaults, *args, **kwargs, return, local/global/nonlocal, closures, lambda |
| 07 | `07_comprehensions_functional_recursion.ipynb` | 42 | Q-229..Q-270 | list/dict/set/nested comprehensions, map, filter, zip, enumerate, sorted, any, all, recursion |
| 08 | `08_oop.ipynb` | 44 | Q-271..Q-314 | classes, instances, self, attributes, methods, inheritance, polymorphism, encapsulation, composition, dunder methods, operator overloading, class vs static methods, properties |
| 09 | `09_iterators_generators_decorators_context_exceptions.ipynb` | 44 | Q-315..Q-358 | iterator protocol, generators, yield, decorators, custom context managers, try/except/else/finally, raising, custom exceptions |
| 10 | `10_stdlib_regex_typing_concurrency_testing.ipynb` | 42 | Q-359..Q-400 | modules, packages, imports, file I/O, `with`, collections, itertools, functools, os, sys, pathlib, json, re, datetime, math, random, type hints, threading, multiprocessing, asyncio, the GIL, pytest + fixtures, pdb and tracebacks |

**Total: 400.**

Mini-projects use a separate ID namespace (`P-01` .. `P-10`) and are **not**
counted in the 400.

## 5. Difficulty labels and distribution

| Level | Label | Meaning |
|-------|-------|---------|
| L1 | Extremely Easy | One concept, one line, no edge cases. Builds recall. |
| L2 | Easy | One concept applied, a small edge case to notice. |
| L3 | Intermediate | Combines 2-3 concepts, or a non-obvious edge case. |
| L4 | Somewhat Difficult | Design choice required; multiple valid approaches; correctness needs care. |
| L5 | Hard | Multi-concept, subtle failure modes, or a real algorithmic/semantic trap. |

Each question header renders as:

```
### Q-047 - L3 Intermediate - Comprehensions
```

### 5.1 Exact per-notebook distribution

This table is asserted by `tests/test_coverage.py`.

| NB | L1 | L2 | L3 | L4 | L5 | Total |
|----|----|----|----|----|----|-------|
| 01 | 12 | 11 |  8 |  3 |  2 | 36 |
| 02 | 11 | 12 |  9 |  4 |  2 | 38 |
| 03 | 10 | 12 | 10 |  4 |  2 | 38 |
| 04 |  9 | 12 | 10 |  5 |  2 | 38 |
| 05 |  9 | 11 |  9 |  4 |  3 | 36 |
| 06 |  6 | 10 | 13 |  9 |  4 | 42 |
| 07 |  5 | 10 | 13 |  9 |  5 | 42 |
| 08 |  4 |  9 | 14 | 11 |  6 | 44 |
| 09 |  2 |  7 | 13 | 15 |  7 | 44 |
| 10 |  2 |  6 | 11 | 16 |  7 | 42 |
| **Sum** | **70** | **100** | **110** | **80** | **40** | **400** |

Questions appear in the notebook in ascending level order, so the ramp is
visible as the learner scrolls.

## 6. Question rendering

Each question occupies exactly two cells: one markdown cell (prompt + hidden
hint + hidden solution) and one code cell (starter + `check()` call).

````markdown
### Q-047 - L3 Intermediate - Comprehensions

Flatten `grid` (a list of lists) into a single flat list using one
comprehension. No `for` statement, no `sum()`, no `itertools`.

<details><summary>Hint</summary>

A nested comprehension's clauses read left-to-right in the same order you would
write the nested for-loops.

</details>

<details><summary>Solution</summary>

```python
def flatten(grid):
    return [x for row in grid for x in row]
```

**Why:** `for row in grid` binds first, then `for x in row` runs inside it.
Reversing the two clauses is the most common mistake here - `row` would not be
defined yet.

</details>
````

```python
def flatten(grid):
    ...            # your code here

check('Q-047', flatten)
```

**Why `<details>` and not ipywidgets:** hints and solutions live in markdown, so
they never execute, never leak names into the learner's namespace, survive
kernel restarts, and render identically in JupyterLab, VS Code, nbviewer and
GitHub. Hint and solution are independent toggles, so a hint can be taken
without revealing the answer.

## 7. The `sprintcheck` checker

### 7.1 Public API

```python
check(qid, *args)   # run the stored cases for qid; print PASS or FAIL detail
progress()          # per-notebook dashboard of solved / attempted
reset(qid=None)     # clear progress for one question or all
```

### 7.2 Case kinds

| Kind | Used for | Learner calls |
|------|----------|---------------|
| `function` | most questions | `check('Q-047', flatten)` |
| `value` | "assign X to ..." | `check('Q-003', x)` |
| `output` | print / formatting drills | `check('Q-012', greet)` - runner captures stdout during the call |
| `predict` | gotcha "what does this print?" | `check('Q-088', "[1, 1]")` |
| `custom` | constraint questions - must use a comprehension, must be recursive, refactor drills | `check('Q-231', fn)` - inspects source via AST |

### 7.3 Output contract

Pass:

```
Q-047 PASSED  (6/6 cases, 0.4ms)
```

Fail - shows at most the first 3 failing cases, each with input, expected, got:

```
Q-047 FAILED  3/6 cases
  flatten([[1], [], [2]])
    expected  [1, 2]
    got       [1, None, 2]
```

Exceptions raised by learner code are caught and reported as a failing case with
the exception type and message, never as a traceback that halts the notebook.

**Comparison rules.** `function` and `value` cases compare with `==` after an
exact type check, so `1` does not pass for `True` and `[1,2]` does not pass for
`(1,2)`. Float expectations compare with `math.isclose`. `output` and `predict`
cases normalize before comparing: strip leading/trailing whitespace on the whole
string and on each line, and collapse runs of internal spaces - so a `predict`
answer is judged on content, not on how the learner spaced it.

### 7.4 Progress persistence

`check()` appends `{qid, passed, timestamp}` to `.sprintcheck_progress.json` at
repo root. `progress()` renders solved/total per notebook. The file is
gitignored and safe to delete.

### 7.5 Import bootstrap

`pyproject.toml` declares `sprintcheck` and `content` as packages; Phase 0 runs
`uv pip install --python ~/.venvs/ds/bin/python -e .`, so notebooks import it
directly. Each notebook's first cell also contains a `sys.path` fallback so a
notebook still works if the editable install is missing.

## 8. Question kinds beyond straight exercises

Woven through the 400 (not additional to them):

- **Gotcha / "what does this print?"** - approximately 45 questions, `predict`
  kind, present in every notebook. Covers: mutable default arguments,
  late-binding closures, `is` vs `==` on small integers, shallow vs deep copy,
  iterator exhaustion, mutation during iteration, class attributes vs instance
  attributes, truthiness surprises, integer/float equality, `list` aliasing.
- **Pythonic refactor drills** - approximately 30 questions, `custom` kind.
  Working-but-unidiomatic code is given; the learner rewrites it idiomatically
  and the AST check enforces the idiom.

Additional to the 400:

- **Mini-projects** - one per notebook, `P-01` .. `P-10`, 30-60 minutes each,
  checker-backed, combining that notebook's topics. Planned: CSV report tool,
  text tokenizer / word-frequency, inventory manager, matrix/grid utilities,
  number-guessing state machine, argument-validating decorator toolkit,
  pipeline of comprehensions over records, bank-account class hierarchy,
  retry + LRU-cache decorators with a paginated cursor generator, log-parsing
  CLI with pytest tests.

## 9. Test suite

`tests/` runs under pytest against the content source, not the notebooks.

- `test_content_integrity.py` - every `Question` has all required fields
  non-empty; IDs are unique and exactly contiguous `Q-001`..`Q-400`; hint and
  solution are non-empty and distinct. Case-count floor by kind: `function` and
  `custom` require at least 3 cases; `output`, `value` and `predict` are
  single-answer by nature and require at least 1. No question may contain two
  identical cases - padding a floor with repeats adds no coverage.
- `test_solutions_pass.py` - **executes every reference solution against its own
  cases and asserts a pass.** This is the core guarantee.
- `test_coverage.py` - the per-notebook difficulty distribution in section 5.1
  holds exactly; every P0 topic from section 4 is tagged by at least the minimum
  number of questions; `build.py --check` reports no drift.

## 10. Build order

**Phase 0 - pipeline proof.** Install pytest. Scaffold repo, `pyproject.toml`,
`content/schema.py`, `sprintcheck` runner, `build.py`, and the three test
modules. Author **NB01 complete (36 questions, Q-001..Q-036)** and generate it.
Test suite green. **Checkpoint: the learner opens NB01 and confirms the format
before the remaining 364 questions are written.**

**Phases 1-9 - one notebook per phase**, in order NB02 .. NB10. Each phase:
author the content module, run `build.py`, run the test suite to green, commit.

The Phase 0 checkpoint is deliberate: changing the question format costs 36
rewrites now versus 400 later.

## 11. Out of scope

- No numpy / pandas / data-science content. This is core Python only (P1 Data
  Structures & Algorithms is a separate future track).
- No auto-grading server, no web UI, no spaced-repetition scheduler.
- No solution-hiding beyond `<details>` - the learner is trusted not to peek.
