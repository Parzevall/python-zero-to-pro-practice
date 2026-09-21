<p align="center">
  <img src="assets/header.svg" alt="Python Zero to Pro: 400 questions, one foundation" width="100%">
</p>

<p align="center">
  <strong>400 Python practice questions · 10 Jupyter notebooks · 10 mini-projects</strong><br>
  Every question is labelled by difficulty and ships with a hidden hint, a hidden solution, and a checker that grades your answer.
</p>

---

## What this is

This is a practice course for making your Python foundation solid. It isn't a
tutorial. It assumes you already know roughly what a loop is, and it's aimed at
the gap between "I can read Python" and "I can write Python without thinking
about it."

Core Python only. No numpy, no pandas, no frameworks. Just the standard library,
because that's the layer everything else sits on.

**A few things that make it different from a list of exercises:**

**Your answers get graded.** You write a function, call `check()`, and it runs
your code against real test cases. When something fails it shows you the exact
input that broke, what it expected, and what you actually returned. You debug
from evidence instead of guessing.

**Hints and solutions are separate.** They're two independent toggles, so you can
take a nudge on a question without spoiling the answer for yourself.

**68 questions check *how* you solved it, not just whether it works.** If a
question says "do this without a loop," that gets verified against your code's
syntax tree. It isn't on the honour system.

**58 questions are "what does this print?" traps.** Mutable default arguments,
late-binding closures, `0.1 + 0.2`, iterator exhaustion, `{1: 'a', True: 'b'}`.
These are the things that quietly break self-taught Python, and the cheapest
place to get them wrong is here.

**Every one of the 400 solutions is executed against its own test cases by the
test suite.** If a shipped solution were wrong, the build would fail. You can
trust the answers.

---

## Getting started

You need Python 3.10 or newer, and Jupyter. That's it.

```bash
git clone https://github.com/Parzevall/python-zero-to-pro-practice.git
cd python-zero-to-pro-practice

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install jupyterlab

jupyter lab notebooks/
```

Open `01_foundations_and_operators.ipynb`, run the first cell, and start solving.

There's genuinely nothing else to set up. The notebooks use the standard `python3`
kernel that ships with every Jupyter install, and the first cell finds the project
on its own whether you launched Jupyter from the repo root or from inside
`notebooks/`.

<details>
<summary><strong>Using VS Code, uv, or conda instead?</strong></summary>

<br>

**VS Code.** Install the Python and Jupyter extensions, open the folder, open any
notebook, and pick your interpreter when it asks. The collapsible hint and solution
blocks render natively.

**uv**, if you want it faster:
```bash
uv venv && uv pip install jupyterlab && uv run jupyter lab notebooks/
```

**conda**:
```bash
conda create -n pysprints python=3.12 jupyterlab -y
conda activate pysprints && jupyter lab notebooks/
```

**Editable install.** Not required, since the first cell sorts out the import path
for you. But if you'd like `import sprintcheck` to work from anywhere:
```bash
pip install -e .
```

**Running the tests.** Only needed if you're editing the questions themselves:
```bash
pip install pytest && python -m pytest -q
```
</details>

---

## How a question works

Each question is two cells. A markdown cell holds the prompt and two collapsed
toggles, and a code cell is where you write your answer.

> ### Q-047 · L3 Intermediate · Comprehensions
>
> Flatten `grid` (a list of lists) into one flat list using a single comprehension.
> No `for` statement, no `sum()`, no `itertools`.
>
> <details><summary>💡 Hint</summary><br>A nested comprehension's clauses read left to right, in the same order you'd write the nested for-loops.</details>
>
> <details><summary>✅ Solution</summary><br>Only shows when you click it.</details>

```python
def flatten(grid):
    ...            # your code here

check('Q-047', flatten)
```

Run the cell and you get one of these back:

```
PASSED  Q-047  (6/6 cases, 0.4ms)
```

```
FAILED  Q-047  3/6 cases passed
  flatten([[1], [], [2]])
    expected  [1, 2]
    got       [1, None, 2]
```

That second one is the whole point. You're told exactly which input broke, so you
can form a hypothesis instead of changing things at random and re-running.

### The three commands you'll use

| | |
|---|---|
| `check('Q-047', flatten)` | Grade your answer |
| `progress()` | See what you've solved, per notebook |
| `reset('Q-047')` | Forget an attempt |

Progress gets saved to `.sprintcheck_progress.json`. It survives kernel restarts,
it's git-ignored so it stays on your machine, and you can delete it any time.

---

## The difficulty labels

Questions run easiest to hardest down each notebook, and every notebook finishes on
L5, so you're always stretched a bit before moving on.

| Label | What it means |
|---|---|
| **L1** Extremely Easy | One concept, one line. Builds recall. |
| **L2** Easy | One concept applied, with a small edge case to spot. |
| **L3** Intermediate | Two or three concepts together, or a non-obvious edge case. |
| **L4** Somewhat Difficult | There's a design choice to make, and correctness needs care. |
| **L5** Hard | Several concepts at once, subtle failure modes, or a real trap. |

Across all 400 questions that works out to **70 / 100 / 110 / 80 / 40** from L1 to L5.

---

## The notebooks

| # | Notebook | Qs | What's in it |
|---|---|---|---|
| 01 | Foundations & Operators | 36 | Types, dynamic typing, casting, all five operator families |
| 02 | Strings | 38 | Indexing, slicing, f-strings, the methods worth knowing cold |
| 03 | Lists & Tuples | 38 | Mutability, aliasing vs copying, unpacking, nesting |
| 04 | Dicts & Sets | 38 | Dict methods, set algebra, hashability, ordering guarantees |
| 05 | Control Flow & Loops | 36 | Six questions on `else`-on-loop alone, because almost nobody knows it |
| 06 | Functions, Scope & Closures | 42 | Arguments, defaults, `*args`, LEGB, closures, lambda |
| 07 | Comprehensions, Functional & Recursion | 42 | Twelve recursion questions, from factorial up to Tower of Hanoi |
| 08 | OOP | 44 | Dunder methods, properties, inheritance, composition |
| 09 | Iterators, Generators, Decorators, Context Managers & Exceptions | 44 | The hard middle of the language |
| 10 | Stdlib, Regex, Typing, Concurrency, Testing & Debugging | 42 | The practical layer you actually use day to day |

Every notebook ends with a mini-project, around 30 to 60 minutes, that makes you
combine its topics: a receipt calculator, a word-frequency report, matrix utilities,
an inventory manager, a game engine, a validator toolkit, a records pipeline, a
bank-account hierarchy, a retry plus LRU-cache decorator pair, and a log parser.

---

## How to get the most out of it

Two habits matter more than how fast you go.

**Open the hint before the solution, and only after a real attempt.** A solution you
read is worth close to nothing. A solution you got to yourself after a nudge sticks.
If you open the answer without trying first, you've read a tutorial, not practised.

**When `check()` fails, read the failing case before you touch anything.** The output
names the exact input that broke. Working out what that implies is the skill you're
here to build. Guessing and re-running isn't.

On pace: one notebook a day is ambitious but doable. Finishing slowly beats skimming
quickly, and the gotcha questions in particular reward sitting with them for a minute.
Being wrong about `0.1 + 0.2` in a notebook costs you nothing. Being wrong about it in
production costs you an afternoon.

---

## Working on the content

The notebooks are generated rather than hand-edited. `content/` is the source of
truth: each question is a single object holding its prompt, hint, solution,
explanation and test cases together, so an answer and its tests can't drift apart.

```bash
python build.py                 # generate any missing notebooks
python build.py --check         # report drift, write nothing
python build.py --force         # regenerate (careful: discards written answers)
python -m pytest -q             # verify all 400 solutions pass their own cases
```

`build.py` won't overwrite a notebook that already exists unless you pass `--force`,
so your answers are safe from an accidental rebuild.

```
content/       question source of truth  (edit here)
sprintcheck/   the grader
build.py       content/ -> notebooks/
notebooks/     generated, and what you actually open
tests/         proves every solution is correct
```

The test suite checks more than correctness. It also asserts that question IDs stay
contiguous, that the difficulty spread holds exactly, that no question repeats a test
case, and that no starter code shadows the grader's own function names.

---

<p align="center"><sub>Built for deliberate practice. Every solution verified by an automated test suite.</sub></p>
