# pythonsprints

400 labeled Python questions across 10 notebooks, each with a hidden hint, a
hidden solution, and an automatic checker. Core Python only — no numpy, no
pandas. The goal is a foundation layer with no soft spots.

## Start

```bash
uv pip install --python ~/.venvs/ds/bin/python -e .
~/.venvs/ds/bin/jupyter lab notebooks/
```

Pick the kernel **Python 3.13 (ds)**. Open `01_foundations_and_operators.ipynb`.

## How a question works

A markdown cell holds the prompt with two collapsed toggles (Hint, Solution),
then a code cell where you answer:

```python
def swap(a, b):
    ...            # your code

check('Q-003', swap)
```

`check()` prints PASS, or FAIL with the exact failing input, what was expected,
and what you returned. `progress()` shows a per-notebook dashboard; it is stored
in `.sprintcheck_progress.json` and is safe to delete.

## Difficulty labels

Questions run easiest to hardest down each notebook. Every notebook ends on L5.

| Label | Meaning |
|-------|---------|
| L1 Extremely Easy | one concept, one line |
| L2 Easy | one concept applied, a small edge case |
| L3 Intermediate | 2-3 concepts, or a non-obvious edge case |
| L4 Somewhat Difficult | a design choice, correctness needs care |
| L5 Hard | multi-concept, subtle failure modes |

## Two rules that matter more than pace

1. Open the **Hint** before the **Solution**, and only after a real attempt. A
   solution you read is worth roughly nothing; one you reached after a hint sticks.
2. When `check()` fails, read the failing case before changing anything.
   Debugging from evidence is the actual skill.

## Working on the content

Notebooks are generated from `content/` — the source of truth, holding each
question's prompt, solution and test cases on one object. `build.py` will **not**
overwrite a notebook you have answered questions in unless you pass `--force`.

```bash
python build.py                 # generate any missing notebooks
python -m pytest -q             # prove every solution passes its own cases
```

## Progress

All 10 notebooks complete — 400 questions, 10 mini-projects.

| Notebook | Qs | Focus |
|---|---|---|
| 01 Foundations & Operators | 36 | types, casting, all five operator families |
| 02 Strings | 38 | indexing, slicing, f-strings, methods |
| 03 Lists & Tuples | 38 | mutability, copying, unpacking |
| 04 Dicts & Sets | 38 | dict methods, set algebra, hashability |
| 05 Control Flow & Loops | 36 | incl. 6 questions on `else`-on-loop |
| 06 Functions, Scope & Closures | 42 | args, defaults, LEGB, closures |
| 07 Comprehensions, Functional & Recursion | 42 | incl. 12 recursion questions |
| 08 OOP | 44 | dunder methods, properties, inheritance |
| 09 Iterators, Generators, Decorators, Context Managers & Exceptions | 44 | the hard middle of the language |
| 10 Stdlib, Regex, Typing, Concurrency, Testing & Debugging | 42 | the practical layer |

58 of them are "what does this print?" gotchas and 68 carry enforced constraints
("solve it without a loop", "make it recursive") checked against your code's AST,
not the honour system.
