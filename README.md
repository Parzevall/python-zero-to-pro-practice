# Python Zero to Pro · Practice

**570 hands-on Python questions · 33 notebooks · beginner → intermediate → advanced**

Every notebook is 20 questions that start as one-liners and grow into small
programs, ending in a story project. Each tier ends with a capstone: one bigger
program built in milestones.

---

## What this is

A practice course for making your Python solid, from your very first `print()` to
asyncio, descriptors and real-world programs. It isn't a tutorial: you learn by
writing code, every single question.

**Nothing is used before it's taught.** Every notebook lists what you'll need and
what you'll practise, and every solution sticks to what that notebook and the ones
before it cover. A notebook-1 question never needs a loop.

---

## Getting started

You need Python 3.12 or newer (3.14 for a couple of the newest-feature questions), and Jupyter.

```bash
git clone https://github.com/Parzevall/python-zero-to-pro-practice.git
cd python-zero-to-pro-practice

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install jupyterlab

jupyter lab
```

Open `beginner/NB00-Start-Here.ipynb` and work down from there. There's no setup
cell and nothing to import: each question is plain text plus an empty cell for
your code.

<details>
<summary><strong>Using VS Code, uv, or conda instead?</strong></summary>

<br>

**VS Code.** Install the Python and Jupyter extensions, open the folder, open any
notebook, and pick your interpreter when it asks.

**uv:**
```bash
uv venv && uv pip install jupyterlab && uv run jupyter lab
```

**conda:**
```bash
conda create -n zero-to-pro python=3.13 jupyterlab -y
conda activate zero-to-pro && jupyter lab
```
</details>

---

## How to use it

1. Read the question and write your code in the cell beneath it.
2. Run it and compare with the **Expected output** shown under the question.
3. Open **Solution** only after a real attempt.

Each notebook climbs in four steps, then finishes with a story:

| Questions | Size | Feel |
|---|---|---|
| Q1-5 | one line | warm-up |
| Q6-10 | 2-4 lines | combine two ideas |
| Q11-15 | 5-8 lines | small real tasks |
| Q16-19 | 8-15 lines | puzzles and builds |
| Q20 | a story project | everything in the notebook, step by step |

Each tier ends with a capstone: one bigger program built in milestones.
NB08 is a notebook. **NB20 and NB32 are real project folders**: you write `.py`
modules in your editor, run the given `demo_N.py` scripts, and `python check.py`
tells you which milestones pass. Each folder's README has the story and steps.

---

## The notebooks

### `beginner/`: no Python needed

| # | Notebook | Story project |
|---|---|---|
| NB00 | [Start Here](beginner/NB00-Start-Here.ipynb) | Business Card |
| NB01 | [Variables Types Operators](beginner/NB01-Variables-Types-Operators.ipynb) | Café Closing Time |
| NB02 | [Strings](beginner/NB02-Strings.ipynb) | Username Generator |
| NB03 | [Conditionals](beginner/NB03-Conditionals.ipynb) | Tax Day |
| NB04 | [Loops](beginner/NB04-Loops.ipynb) | Guessing Game Replay |
| NB05 | [Lists Tuples](beginner/NB05-Lists-Tuples.ipynb) | Class Gradebook |
| NB06 | [Dicts Sets](beginner/NB06-Dicts-Sets.ipynb) | Corner Shop Orders |
| NB07 | [Functions Basics](beginner/NB07-Functions-Basics.ipynb) | Text Statistics Toolkit |
| NB08 | [Beginner Capstone](beginner/NB08-Beginner-Capstone.ipynb) | **Capstone:** Byte Bank |

### `intermediate/`: writing real programs

| # | Notebook | Story project |
|---|---|---|
| NB09 | [Functions Advanced](intermediate/NB09-Functions-Advanced.ipynb) | Event System |
| NB10 | [Comprehensions Functional Sorting](intermediate/NB10-Comprehensions-Functional-Sorting.ipynb) | Sales Report |
| NB11 | [Recursion](intermediate/NB11-Recursion.ipynb) | Folder Size Calculator |
| NB12 | [Exceptions](intermediate/NB12-Exceptions.ipynb) | Robust Record Parser |
| NB13 | [Modules Files JSON CSV](intermediate/NB13-Modules-Files-JSON-CSV.ipynb) | Contacts Manager |
| NB14 | [OOP Basics](intermediate/NB14-OOP-Basics.ipynb) | Parking Lot |
| NB15 | [Stdlib Essentials](intermediate/NB15-Stdlib-Essentials.ipynb) | Web Log Analytics |
| NB16 | [Numbers Bits Bytes Unicode](intermediate/NB16-Numbers-Bits-Bytes-Unicode.ipynb) | Invoice Engine |
| NB17 | [Regex](intermediate/NB17-Regex.ipynb) | Log Redactor |
| NB18 | [Pythonic Idioms Pattern Matching](intermediate/NB18-Pythonic-Idioms-Pattern-Matching.ipynb) | Cave Text Adventure |
| NB19 | [Data Structures Algorithms](intermediate/NB19-Data-Structures-Algorithms.ipynb) | Route Planner |
| NB20 | [Intermediate Capstone](intermediate/NB20-Intermediate-Capstone/) | **Capstone:** Pageturner Library |

### `advanced/`: how Python works, and how seniors use it

| # | Notebook | Story project |
|---|---|---|
| NB21 | [OOP Advanced](advanced/NB21-OOP-Advanced.ipynb) | Money Library |
| NB22 | [Iterators Generators](advanced/NB22-Iterators-Generators.ipynb) | Streaming Sales Report |
| NB23 | [Decorators](advanced/NB23-Decorators.ipynb) | Mini Web Router |
| NB24 | [Context Managers](advanced/NB24-Context-Managers.ipynb) | Bank Vault Transactions |
| NB25 | [Descriptors Metaprogramming](advanced/NB25-Descriptors-Metaprogramming.ipynb) | Mini ORM |
| NB26 | [Type Hints](advanced/NB26-Type-Hints.ipynb) | Typed Repository Layer |
| NB27 | [Concurrency Asyncio](advanced/NB27-Concurrency-Asyncio.ipynb) | Async Site Crawler |
| NB28 | [Testing Debugging Logging](advanced/NB28-Testing-Debugging-Logging.ipynb) | Bug Hunt at Pocket Bank |
| NB29 | [Performance Memory](advanced/NB29-Performance-Memory.ipynb) | Speed Up the Monday Report |
| NB30 | [Networking HTTP APIs](advanced/NB30-Networking-HTTP-APIs.ipynb) | Todo Service |
| NB31 | [Real World Programs](advanced/NB31-Real-World-Programs.ipynb) | Expense Tracker CLI |
| NB32 | [Advanced Capstone](advanced/NB32-Advanced-Capstone/) | **Capstone:** Orderflow: an order-processing pipeline |

---

## `course-kit/`: everything that isn't a notebook

You never need this folder to do the course. It holds the sources the notebooks
are built from, the checks every question passes, and tool files.

```
course-kit/src/nbXX.py       the questions for each notebook
course-kit/builder.py        turns a source file into a notebook
course-kit/capstone.py       turns a capstone source into a project folder (NB20, NB32)
course-kit/checker.py        runs solutions, checks nothing is used before it's taught
course-kit/plan_data.py      what each notebook covers, in order
course-kit/WRITING-BRIEF.md  rules for writing a notebook
```

To change a question, edit its source and rebuild:

```bash
cd course-kit/src && python3 nb01.py
```

The build runs every solution twice, fills in the expected output itself, and
refuses to write the notebook if a solution crashes, prints different output
between runs, or uses something not taught yet.
