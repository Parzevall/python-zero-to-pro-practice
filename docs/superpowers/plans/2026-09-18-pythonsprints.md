# pythonsprints Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 10 Jupyter notebooks holding 400 difficulty-labeled Python practice questions, each with a hidden hint, a hidden solution, and an automatic correctness check.

**Architecture:** Questions are authored as `Question` dataclass objects in `content/`, which is the single source of truth. `build.py` renders them into notebooks; `sprintcheck` imports the same objects at runtime to grade the learner's answers. Because the reference solution and its test cases live on one object, the test suite can execute every solution against its own cases and prove all 400 are correct.

**Tech Stack:** Python 3.13.14 (`/home/topg/.venvs/ds/bin/python`), `nbformat` (already installed, 5.10.4), `pytest` (installed in Task 1), standard library only for question content.

**Spec:** `docs/superpowers/specs/2026-09-18-pythonsprints-design.md`

## Global Constraints

- Interpreter is always `/home/topg/.venvs/ds/bin/python`. Never `python3`, never a new venv.
- Question content imports **standard library only**. No numpy, pandas, requests. The goal is core Python.
- Question IDs are `Q-NNN`, zero-padded to 3 digits, globally unique, contiguous `Q-001`..`Q-400`. Mini-projects use `P-NN` and are NOT part of the 400.
- Difficulty labels are exactly: `L1 Extremely Easy`, `L2 Easy`, `L3 Intermediate`, `L4 Somewhat Difficult`, `L5 Hard`.
- Every question header renders exactly as `### Q-047 - L3 Intermediate - Comprehensions`.
- Hints and solutions live in **markdown cells** inside `<details>` blocks, never in code cells.
- `build.py` never overwrites an existing notebook without `--force`.
- Commit after every task. The repo is already `git init`ed.
- Per-notebook difficulty counts are fixed by spec section 5.1 and asserted by tests. Do not improvise them.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `pyproject.toml` | Editable-install metadata so `import sprintcheck` works in notebooks |
| `content/schema.py` | `Level`, `Case`, `Question`, `Project`, `Notebook` dataclasses. No logic beyond validation. |
| `content/nb01_foundations.py` .. `nb10_*.py` | The questions themselves. One module per notebook, each exporting `NOTEBOOK`. |
| `sprintcheck/compare.py` | Value comparison + failure formatting. Pure functions, no I/O. |
| `sprintcheck/constraints.py` | AST inspection for `custom` questions (no-loops, needs-recursion, ...) |
| `sprintcheck/registry.py` | Lazily imports `content/`, exposes `get(qid) -> Question` |
| `sprintcheck/store.py` | Read/write `.sprintcheck_progress.json`, render dashboard |
| `sprintcheck/__init__.py` | Public API: `check()`, `progress()`, `reset()`. Thin orchestration only. |
| `build.py` | Renders `Notebook` objects to `.ipynb` via nbformat. `--force`, `--check`. |
| `tests/test_content_integrity.py` | Field completeness, ID contiguity, case-count floors |
| `tests/test_solutions_pass.py` | **Every reference solution passes its own cases** |
| `tests/test_coverage.py` | Difficulty distribution + P0 topic quotas + build drift |

Split is by responsibility, not layer: comparison logic, AST logic, storage and orchestration each change for different reasons, and each stays small enough to hold in context.

---

## Task 1: Scaffold, schema, and integrity test

**Files:**
- Create: `pyproject.toml`, `content/__init__.py`, `content/schema.py`, `sprintcheck/__init__.py`
- Test: `tests/test_content_integrity.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `Level` (IntEnum 1-5), `LEVEL_LABELS: dict[int, str]`, `Case(args: tuple, kwargs: dict, expected: Any)`, `Question`, `Project`, `Notebook`. Every later task depends on these exact field names.

- [ ] **Step 1: Install pytest into the ds venv**

```bash
uv pip install --python /home/topg/.venvs/ds/bin/python pytest
/home/topg/.venvs/ds/bin/python -c "import pytest, nbformat; print(pytest.__version__, nbformat.__version__)"
```
Expected: two version numbers, no ImportError.

- [ ] **Step 2: Write `pyproject.toml`**

```toml
[project]
name = "pythonsprints"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["content", "sprintcheck"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 3: Write the failing integrity test**

Create `tests/test_content_integrity.py`:

```python
import re
import pytest
from content import all_notebooks

QID_RE = re.compile(r"^Q-\d{3}$")
MIN_CASES = {"function": 3, "custom": 3, "output": 1, "value": 1, "predict": 1}


def all_questions():
    return [q for nb in all_notebooks() for q in nb.questions]


def test_at_least_one_notebook_exists():
    assert all_notebooks(), "no content modules found"


def test_qids_wellformed_unique_and_contiguous():
    qids = [q.qid for q in all_questions()]
    assert all(QID_RE.match(q) for q in qids), "malformed qid"
    assert len(qids) == len(set(qids)), "duplicate qid"
    numbers = sorted(int(q[2:]) for q in qids)
    assert numbers == list(range(1, len(numbers) + 1)), "qids not contiguous from 001"


@pytest.mark.parametrize("field", ["prompt", "hint", "solution", "explanation", "topic"])
def test_required_fields_nonempty(field):
    for q in all_questions():
        assert getattr(q, field).strip(), f"{q.qid}: empty {field}"


def test_hint_is_not_the_solution():
    for q in all_questions():
        assert q.hint.strip() != q.solution.strip(), f"{q.qid}: hint duplicates solution"


def test_case_count_floor_by_kind():
    for q in all_questions():
        floor = MIN_CASES[q.kind]
        assert len(q.cases) >= floor, f"{q.qid} ({q.kind}): {len(q.cases)} cases, need {floor}"


def test_no_question_repeats_a_case():
    """Three copies of one case satisfies a floor without adding coverage."""
    for q in all_questions():
        seen = [(c.args, tuple(sorted(c.kwargs.items())), repr(c.expected)) for c in q.cases]
        assert len(seen) == len(set(seen)), f"{q.qid}: duplicate case - pad with real ones"


def test_every_question_declares_an_entry_point():
    # Every kind needs it: the solution test execs the solution and looks this
    # name up, and build.py renders it into the check() call.
    for q in all_questions():
        assert q.entry, f"{q.qid}: needs entry (the function or variable name)"
```

- [ ] **Step 4: Run it to verify it fails**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_content_integrity.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'content'`.

- [ ] **Step 5: Write `content/schema.py`**

```python
"""Dataclasses that define a question. This module holds no logic beyond
field validation - the questions themselves live in the nbNN_*.py modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any


class Level(IntEnum):
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4
    L5 = 5


LEVEL_LABELS: dict[int, str] = {
    1: "Extremely Easy",
    2: "Easy",
    3: "Intermediate",
    4: "Somewhat Difficult",
    5: "Hard",
}

KINDS = frozenset({"function", "value", "output", "predict", "custom"})


@dataclass(frozen=True)
class Case:
    """One input/expected pair.

    function/custom: call entry(*args, **kwargs), compare result to expected.
    output:          call entry(*args, **kwargs), compare captured stdout.
    value/predict:   args/kwargs unused; expected is the sole right answer.
    """

    expected: Any
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)

    def call_repr(self, entry: str) -> str:
        parts = [repr(a) for a in self.args]
        parts += [f"{k}={v!r}" for k, v in self.kwargs.items()]
        return f"{entry}({', '.join(parts)})"


@dataclass
class Question:
    qid: str
    level: Level
    topic: str
    prompt: str
    hint: str
    solution: str
    explanation: str
    kind: str
    cases: list[Case]
    entry: str = ""
    starter: str = ""
    constraints: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise ValueError(f"{self.qid}: unknown kind {self.kind!r}")
        if self.kind == "custom" and not self.constraints:
            raise ValueError(f"{self.qid}: kind='custom' requires constraints")

    @property
    def header(self) -> str:
        return f"{self.qid} - L{int(self.level)} {LEVEL_LABELS[int(self.level)]} - {self.topic}"


@dataclass
class Project:
    pid: str
    title: str
    brief: str
    hint: str
    solution: str
    explanation: str
    entry: str
    cases: list[Case]
    starter: str = ""


@dataclass
class Notebook:
    number: int
    slug: str
    title: str
    intro: str
    questions: list[Question]
    project: Project | None = None

    @property
    def filename(self) -> str:
        return f"{self.number:02d}_{self.slug}.ipynb"
```

- [ ] **Step 6: Write `content/__init__.py`**

```python
"""Discovers the nbNN_*.py content modules and exposes their Notebook objects."""

from __future__ import annotations

import importlib
import pkgutil

from content.schema import Notebook


def all_notebooks() -> list[Notebook]:
    """Every Notebook defined under content/, ordered by notebook number."""
    found: list[Notebook] = []
    for info in pkgutil.iter_modules(__path__):
        if not info.name.startswith("nb"):
            continue
        module = importlib.import_module(f"content.{info.name}")
        notebook = getattr(module, "NOTEBOOK", None)
        if notebook is not None:
            found.append(notebook)
    return sorted(found, key=lambda nb: nb.number)


def all_questions():
    return [q for nb in all_notebooks() for q in nb.questions]
```

- [ ] **Step 7: Install editable and run the test**

```bash
uv pip install --python /home/topg/.venvs/ds/bin/python -e .
/home/topg/.venvs/ds/bin/python -m pytest tests/test_content_integrity.py -q
```
Expected: FAIL on `test_at_least_one_notebook_exists` only ("no content modules found"). Every other test passes vacuously. This is the correct state — content arrives in Task 7.

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml content/ sprintcheck/ tests/
git commit -m "feat: add question schema and content integrity tests"
```

---

## Task 2: Value comparison and failure formatting

**Files:**
- Create: `sprintcheck/compare.py`
- Test: `tests/test_compare.py`

**Interfaces:**
- Consumes: `content.schema.Case`.
- Produces: `matches(got, expected) -> bool` and `format_failure(call_repr, expected, got) -> str`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_compare.py`:

```python
import math

from sprintcheck.compare import matches, format_failure


def test_equal_values_match():
    assert matches([1, 2], [1, 2])
    assert matches("abc", "abc")
    assert matches({"a": 1}, {"a": 1})


def test_type_mismatch_does_not_match():
    # These compare == in Python, but a learner who returned the wrong
    # container or a bool-for-int has not solved the question.
    assert not matches(1, True)
    assert not matches(True, 1)
    assert not matches([1, 2], (1, 2))
    assert not matches(1, 1.0)


def test_floats_compare_with_tolerance():
    assert matches(0.1 + 0.2, 0.3)
    assert not matches(0.31, 0.3)
    assert matches(float("inf"), float("inf"))
    assert matches(float("nan"), float("nan"))


def test_nested_floats_compare_with_tolerance():
    assert matches([0.1 + 0.2, 1.0], [0.3, 1.0])
    assert matches({"x": 0.1 + 0.2}, {"x": 0.3})


def test_format_failure_shows_call_expected_and_got():
    text = format_failure("flatten([[1], [], [2]])", [1, 2], [1, None, 2])
    assert "flatten([[1], [], [2]])" in text
    assert "expected" in text and "[1, 2]" in text
    assert "got" in text and "[1, None, 2]" in text
```

- [ ] **Step 2: Run it to verify it fails**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_compare.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'sprintcheck.compare'`.

- [ ] **Step 3: Write `sprintcheck/compare.py`**

```python
"""Value comparison for graded answers.

Strict on type, tolerant on float. A learner who returns a tuple where a list
was asked for has not solved the question, so `==` alone is too permissive.
"""

from __future__ import annotations

import math
from typing import Any

REL_TOL = 1e-9
ABS_TOL = 1e-12


def matches(got: Any, expected: Any) -> bool:
    if type(got) is not type(expected):
        return False
    if isinstance(expected, float):
        if math.isnan(expected):
            return math.isnan(got)
        return math.isclose(got, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL)
    if isinstance(expected, (list, tuple)):
        return len(got) == len(expected) and all(
            matches(g, e) for g, e in zip(got, expected)
        )
    if isinstance(expected, dict):
        return got.keys() == expected.keys() and all(
            matches(got[k], expected[k]) for k in expected
        )
    if isinstance(expected, (set, frozenset)):
        return got == expected
    return got == expected


def normalize_text(text: str) -> str:
    """Whitespace-insensitive form, for `output` and `predict` answers.

    Judges content, not how the learner spaced it.
    """
    lines = [" ".join(line.split()) for line in text.strip().splitlines()]
    return "\n".join(line for line in lines).strip()


def format_failure(call_repr: str, expected: Any, got: Any) -> str:
    return f"  {call_repr}\n    expected  {expected!r}\n    got       {got!r}"


def format_error(call_repr: str, exc: BaseException) -> str:
    return f"  {call_repr}\n    raised    {type(exc).__name__}: {exc}"
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_compare.py -q`
Expected: PASS, 5 tests.

- [ ] **Step 5: Commit**

```bash
git add sprintcheck/compare.py tests/test_compare.py
git commit -m "feat: add strict-type tolerant-float value comparison"
```

---

## Task 3: AST constraints for `custom` questions

**Files:**
- Create: `sprintcheck/constraints.py`
- Test: `tests/test_constraints.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `check_constraints(func, rules: list[str]) -> list[str]` returning human-readable violation messages (empty list means satisfied). Rule vocabulary: `no-loops`, `needs-comprehension`, `needs-recursion`, `needs-generator`, `needs-with`, `no-builtin:NAME`, `max-lines:N`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_constraints.py`:

```python
from sprintcheck.constraints import check_constraints


def comp(grid):
    return [x for row in grid for x in row]


def looped(grid):
    out = []
    for row in grid:
        for x in row:
            out.append(x)
    return out


def recursive(n):
    return 1 if n <= 1 else n * recursive(n - 1)


def uses_sum(rows):
    return sum(rows, [])


def gen(n):
    for i in range(n):
        yield i


def test_no_loops_passes_comprehension_and_fails_loop():
    assert check_constraints(comp, ["no-loops"]) == []
    assert check_constraints(looped, ["no-loops"])


def test_needs_comprehension():
    assert check_constraints(comp, ["needs-comprehension"]) == []
    assert check_constraints(looped, ["needs-comprehension"])


def test_needs_recursion():
    assert check_constraints(recursive, ["needs-recursion"]) == []
    assert check_constraints(comp, ["needs-recursion"])


def test_no_builtin():
    assert check_constraints(uses_sum, ["no-builtin:sum"])
    assert check_constraints(comp, ["no-builtin:sum"]) == []


def test_needs_generator():
    assert check_constraints(gen, ["needs-generator"]) == []
    assert check_constraints(comp, ["needs-generator"])


def test_max_lines():
    assert check_constraints(comp, ["max-lines:2"]) == []
    assert check_constraints(looped, ["max-lines:2"])


def test_unreadable_source_is_reported_not_crashed():
    violations = check_constraints(len, ["no-loops"])
    assert violations and "source" in violations[0].lower()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_constraints.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'sprintcheck.constraints'`.

- [ ] **Step 3: Write `sprintcheck/constraints.py`**

```python
"""AST checks for questions that constrain *how* the answer is written.

Used by `custom` questions - "solve this without a loop", "make this
recursive", "rewrite it as a comprehension". The functional cases still run;
these constraints are an additional gate on top of them.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Callable

LOOP_NODES = (ast.For, ast.AsyncFor, ast.While)
COMP_NODES = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def _tree(func: Callable) -> ast.AST:
    source = textwrap.dedent(inspect.getsource(func))
    return ast.parse(source)


def _has(tree: ast.AST, node_types) -> bool:
    return any(isinstance(node, node_types) for node in ast.walk(tree))


def _calls_name(tree: ast.AST, name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == name:
                return True
    return False


def _body_line_count(tree: ast.AST) -> int:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lines = {
                child.lineno
                for child in ast.walk(node)
                if hasattr(child, "lineno") and child.lineno > node.body[0].lineno - 1
            }
            return len(lines)
    return 0


def check_constraints(func: Callable, rules: list[str]) -> list[str]:
    """Return a list of violation messages. Empty list means all rules hold."""
    try:
        tree = _tree(func)
    except (OSError, TypeError):
        return ["could not read source for this function (define it in a notebook cell)"]

    violations: list[str] = []
    func_name = getattr(func, "__name__", "")

    for rule in rules:
        name, _, arg = rule.partition(":")
        if name == "no-loops" and _has(tree, LOOP_NODES):
            violations.append("uses a for/while statement - solve it without one")
        elif name == "needs-comprehension" and not _has(tree, COMP_NODES):
            violations.append("no comprehension found - the answer should use one")
        elif name == "needs-recursion" and not _calls_name(tree, func_name):
            violations.append(f"{func_name} never calls itself - make it recursive")
        elif name == "needs-generator" and not _has(tree, (ast.Yield, ast.YieldFrom)):
            violations.append("no yield found - this should be a generator")
        elif name == "needs-with" and not _has(tree, (ast.With, ast.AsyncWith)):
            violations.append("no with-statement found - use a context manager")
        elif name == "no-builtin" and _calls_name(tree, arg):
            violations.append(f"calls {arg}() - this question asks you to do it manually")
        elif name == "max-lines":
            count = _body_line_count(tree)
            if count > int(arg):
                violations.append(f"body is {count} lines - keep it to {arg} or fewer")
    return violations
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_constraints.py -q`
Expected: PASS, 7 tests.

- [ ] **Step 5: Commit**

```bash
git add sprintcheck/constraints.py tests/test_constraints.py
git commit -m "feat: add AST constraint checks for custom questions"
```

---

## Task 4: The `check()` API, registry, and progress

**Files:**
- Create: `sprintcheck/registry.py`, `sprintcheck/store.py`
- Modify: `sprintcheck/__init__.py`
- Test: `tests/test_check_api.py`

**Interfaces:**
- Consumes: `compare.matches`, `compare.normalize_text`, `compare.format_failure`, `compare.format_error`, `constraints.check_constraints`, `content.all_notebooks`.
- Produces: `check(qid, *args) -> bool`, `progress() -> None`, `reset(qid=None) -> None`, `run_question(question, submission) -> Result`. `Result` is a dataclass with `passed: bool`, `total: int`, `n_passed: int`, `failures: list[str]`, `elapsed_ms: float`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_check_api.py`:

```python
import pytest

from content.schema import Case, Level, Question
from sprintcheck import run_question


def make(kind, cases, **kw):
    return Question(
        qid="Q-999", level=Level.L1, topic="T", prompt="p", hint="h",
        solution="s", explanation="e", kind=kind, cases=cases, **kw,
    )


def test_function_all_cases_pass():
    q = make("function", [Case(expected=2, args=(1,)), Case(expected=3, args=(2,)),
                          Case(expected=4, args=(3,))], entry="inc")
    result = run_question(q, lambda n: n + 1)
    assert result.passed and result.n_passed == 3 and result.total == 3


def test_function_reports_each_failing_case():
    q = make("function", [Case(expected=2, args=(1,)), Case(expected=99, args=(2,)),
                          Case(expected=4, args=(3,))], entry="inc")
    result = run_question(q, lambda n: n + 1)
    assert not result.passed and result.n_passed == 2
    assert len(result.failures) == 1 and "expected" in result.failures[0]


def test_learner_exception_becomes_a_failure_not_a_crash():
    q = make("function", [Case(expected=1, args=(0,)), Case(expected=2, args=(1,)),
                          Case(expected=3, args=(2,))], entry="boom")
    result = run_question(q, lambda n: 1 / 0)
    assert not result.passed
    assert "ZeroDivisionError" in result.failures[0]


def test_value_kind_compares_the_submission_directly():
    q = make("value", [Case(expected=42)])
    assert run_question(q, 42).passed
    assert not run_question(q, 41).passed


def test_predict_kind_ignores_whitespace_differences():
    q = make("predict", [Case(expected="[1, 1]")])
    assert run_question(q, "  [1,   1]  ").passed
    assert not run_question(q, "[1]").passed


def test_output_kind_captures_stdout():
    q = make("output", [Case(expected="hi", args=("hi",)), Case(expected="yo", args=("yo",)),
                        Case(expected="ok", args=("ok",))], entry="say")
    assert run_question(q, lambda s: print(s)).passed


def test_custom_kind_fails_when_constraint_violated_even_if_output_correct():
    q = make(
        "custom",
        [Case(expected=[1, 2], args=([[1], [2]],)), Case(expected=[], args=([],)),
         Case(expected=[3], args=([[3]],))],
        entry="flatten", constraints=["no-loops"],
    )

    def looped(grid):
        out = []
        for row in grid:
            for x in row:
                out.append(x)
        return out

    result = run_question(q, looped)
    assert not result.passed
    assert any("for/while" in f for f in result.failures)
```

- [ ] **Step 2: Run it to verify it fails**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_check_api.py -q`
Expected: FAIL — `ImportError: cannot import name 'run_question'`.

- [ ] **Step 3: Write `sprintcheck/registry.py`**

```python
"""Maps question ids to Question objects by importing the content package."""

from __future__ import annotations

from functools import cache

from content import all_notebooks
from content.schema import Level, Project, Question


@cache
def _index() -> dict[str, Question]:
    """Questions AND mini-projects - build.py renders a check() call for both,
    so both have to be addressable by id."""
    index: dict[str, Question] = {}
    for nb in all_notebooks():
        for q in nb.questions:
            index[q.qid] = q
        if nb.project is not None:
            index[nb.project.pid] = as_question(nb.project)
    return index


def as_question(project: Project) -> Question:
    """Adapt a Project to the Question shape the grader consumes."""
    return Question(
        qid=project.pid, level=Level.L5, topic="Mini-project",
        prompt=project.brief, hint=project.hint, solution=project.solution,
        explanation=project.explanation, kind="function",
        cases=project.cases, entry=project.entry,
    )


def get(qid: str) -> Question:
    try:
        return _index()[qid]
    except KeyError:
        raise KeyError(f"unknown question id {qid!r}") from None
```

- [ ] **Step 4: Write `sprintcheck/store.py`**

Named `store`, not `progress`: `progress` is already the public function name, and
a submodule sharing that name would shadow itself at import time.

```python
"""Persists which questions have been solved, so progress survives restarts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

PROGRESS_FILE = Path(__file__).resolve().parent.parent / ".sprintcheck_progress.json"


def _load() -> dict[str, dict]:
    if not PROGRESS_FILE.exists():
        return {}
    try:
        return json.loads(PROGRESS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict[str, dict]) -> None:
    try:
        PROGRESS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True))
    except OSError:
        pass  # progress is a convenience; never let it break a check()


def record(qid: str, passed: bool) -> None:
    data = _load()
    entry = data.setdefault(qid, {"attempts": 0, "solved": False})
    entry["attempts"] += 1
    entry["solved"] = entry["solved"] or passed
    entry["last"] = datetime.now().isoformat(timespec="seconds")
    _save(data)


def clear(qid: str | None = None) -> None:
    if qid is None:
        _save({})
        return
    data = _load()
    data.pop(qid, None)
    _save(data)


def render() -> str:
    from content import all_notebooks

    data = _load()
    lines = ["", "  Notebook                                    solved   attempted", "  " + "-" * 62]
    total_solved = total_q = 0
    for nb in all_notebooks():
        qids = [q.qid for q in nb.questions]
        solved = sum(1 for q in qids if data.get(q, {}).get("solved"))
        attempted = sum(1 for q in qids if q in data)
        total_solved += solved
        total_q += len(qids)
        bar = "#" * round(20 * solved / len(qids)) if qids else ""
        lines.append(f"  {nb.number:02d} {nb.title[:36]:<36} {solved:>3}/{len(qids):<3} {attempted:>5}  {bar}")
    lines.append("  " + "-" * 62)
    pct = (100 * total_solved / total_q) if total_q else 0
    lines.append(f"  {'TOTAL':<39} {total_solved:>3}/{total_q:<3}        {pct:.0f}%")
    return "\n".join(lines)
```

- [ ] **Step 5: Write `sprintcheck/__init__.py`**

```python
"""Grading for pythonsprints.

    from sprintcheck import check, progress, reset

    check('Q-047', flatten)   # grade your answer
    progress()                # see how far you've got
    reset('Q-047')            # forget an attempt
"""

from __future__ import annotations

import contextlib
import io
import time
from dataclasses import dataclass, field
from typing import Any

from content.schema import Question
from sprintcheck import store
from sprintcheck.compare import (
    format_error,
    format_failure,
    matches,
    normalize_text,
)
from sprintcheck.constraints import check_constraints
from sprintcheck.registry import get

MAX_SHOWN_FAILURES = 3


@dataclass
class Result:
    passed: bool
    n_passed: int
    total: int
    failures: list[str] = field(default_factory=list)
    elapsed_ms: float = 0.0


def run_question(question: Question, submission: Any) -> Result:
    start = time.perf_counter()
    failures: list[str] = []

    if question.kind == "custom":
        failures += check_constraints(submission, question.constraints)

    n_passed = 0
    for case in question.cases:
        call = case.call_repr(question.entry or "answer")
        try:
            if question.kind in {"value", "predict"}:
                got = submission
                call = "your answer"
            elif question.kind == "output":
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    submission(*case.args, **case.kwargs)
                got = buffer.getvalue()
            else:
                got = submission(*case.args, **case.kwargs)
        except Exception as exc:  # learner code, not ours
            failures.append(format_error(call, exc))
            continue

        if question.kind in {"output", "predict"}:
            ok = normalize_text(str(got)) == normalize_text(str(case.expected))
        else:
            ok = matches(got, case.expected)

        if ok:
            n_passed += 1
        else:
            failures.append(format_failure(call, case.expected, got))

    elapsed = (time.perf_counter() - start) * 1000
    passed = n_passed == len(question.cases) and not failures
    return Result(passed, n_passed, len(question.cases), failures, elapsed)


def check(qid: str, *args: Any) -> bool:
    """Grade an answer. Pass your function, or your value for value/predict."""
    question = get(qid)
    if not args:
        print(f"{qid}: pass your answer, e.g. check('{qid}', {question.entry or 'my_value'})")
        return False

    result = run_question(question, args[0])
    store.record(qid, result.passed)

    if result.passed:
        print(f"PASSED  {qid}  ({result.total}/{result.total} cases, {result.elapsed_ms:.1f}ms)")
        return True

    print(f"FAILED  {qid}  {result.n_passed}/{result.total} cases passed")
    for line in result.failures[:MAX_SHOWN_FAILURES]:
        print(line)
    hidden = len(result.failures) - MAX_SHOWN_FAILURES
    if hidden > 0:
        print(f"  ... and {hidden} more")
    return False


def progress() -> None:
    print(store.render())


def reset(qid: str | None = None) -> None:
    store.clear(qid)
    print(f"reset {qid}" if qid else "reset all progress")
```

- [ ] **Step 6: Run the test to verify it passes**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_check_api.py -q`
Expected: PASS, 7 tests.

- [ ] **Step 7: Commit**

```bash
git add sprintcheck/ tests/test_check_api.py
git commit -m "feat: add check() grading API with progress persistence"
```

---

## Task 5: Notebook renderer

**Files:**
- Create: `build.py`
- Test: `tests/test_build.py`

**Interfaces:**
- Consumes: `content.all_notebooks`, `content.schema.Notebook`, `nbformat`.
- Produces: `render(notebook) -> nbformat.NotebookNode`, `write(notebook, out_dir, force=False) -> str`, CLI `python build.py [--force] [--check] [--only NN]`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_build.py`:

```python
import nbformat

from build import render
from content.schema import Case, Level, Notebook, Question


def sample_notebook():
    q = Question(
        qid="Q-001", level=Level.L1, topic="Variables",
        prompt="Return the number 7.", hint="Just return it.",
        solution="def seven():\n    return 7", explanation="Literal return.",
        kind="function", entry="seven",
        cases=[Case(expected=7), Case(expected=7), Case(expected=7)],
        starter="def seven():\n    ...",
    )
    return Notebook(number=1, slug="demo", title="Demo", intro="Intro text.", questions=[q])


def test_render_produces_a_valid_notebook():
    nb = render(sample_notebook())
    nbformat.validate(nb)


def test_kernel_is_the_ds_kernel():
    nb = render(sample_notebook())
    assert nb.metadata.kernelspec.name == "ds"


def test_question_header_uses_the_exact_label_format():
    nb = render(sample_notebook())
    md = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
    assert "### Q-001 - L1 Extremely Easy - Variables" in md


def test_hint_and_solution_are_separate_collapsed_details_in_markdown():
    nb = render(sample_notebook())
    md = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
    code = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
    assert md.count("<details>") == 2
    assert "<summary>Hint</summary>" in md and "<summary>Solution</summary>" in md
    # the answer must never leak into an executable cell
    assert "return 7" not in code


def test_code_cell_has_starter_and_check_call():
    nb = render(sample_notebook())
    code = [c.source for c in nb.cells if c.cell_type == "code"]
    assert any("check('Q-001', seven)" in c for c in code)
    assert any("def seven():" in c for c in code)


def test_cells_have_no_execution_output():
    nb = render(sample_notebook())
    for cell in nb.cells:
        if cell.cell_type == "code":
            assert cell.outputs == [] and cell.execution_count is None


def test_write_refuses_to_clobber_without_force(tmp_path):
    from build import write
    nb = sample_notebook()
    write(nb, tmp_path)
    (tmp_path / nb.filename).write_text("LEARNER ANSWERS")
    write(nb, tmp_path)
    assert (tmp_path / nb.filename).read_text() == "LEARNER ANSWERS"
    write(nb, tmp_path, force=True)
    assert (tmp_path / nb.filename).read_text() != "LEARNER ANSWERS"
```

- [ ] **Step 2: Run it to verify it fails**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_build.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'build'`.

- [ ] **Step 3: Write `build.py`**

```python
#!/usr/bin/env python
"""Render content/ Notebook objects into runnable .ipynb files.

Never overwrites an existing notebook without --force: once you have started
answering questions, that file is yours.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from content import all_notebooks
from content.schema import LEVEL_LABELS, Notebook, Project, Question

ROOT = Path(__file__).resolve().parent
NOTEBOOK_DIR = ROOT / "notebooks"

KERNELSPEC = {"display_name": "Python 3.13 (ds)", "language": "python", "name": "ds"}

BOOTSTRAP = '''\
# Run me first. Adds the repo to the path if the editable install is missing.
import sys, pathlib
if not any(pathlib.Path(p).name == "pythonsprints" for p in sys.path):
    sys.path.insert(0, str(pathlib.Path.cwd().parent))
from sprintcheck import check, progress, reset
print("sprintcheck ready - solve a question, then call check('Q-001', your_answer)")'''

LEGEND = """\
**How to use this notebook**

1. Read the question. Write your answer in the code cell beneath it.
2. Run the cell. `check(...)` tells you PASS or FAIL, and shows the failing case.
3. Stuck? Open **Hint** first. Open **Solution** only after a genuine attempt.
4. Call `progress()` any time to see how far you have got.

**Difficulty labels** — questions run easiest to hardest down the notebook.

| | |
|---|---|
| L1 Extremely Easy | one concept, one line |
| L2 Easy | one concept applied, a small edge case |
| L3 Intermediate | 2-3 concepts combined, or a non-obvious edge case |
| L4 Somewhat Difficult | a design choice, correctness needs care |
| L5 Hard | multi-concept, subtle failure modes |
"""


def _details(summary: str, body: str) -> str:
    return f"<details><summary>{summary}</summary>\n\n{body}\n\n</details>"


def question_cells(q: Question) -> list:
    parts = [f"### {q.header}", "", q.prompt.strip(), ""]
    parts.append(_details("Hint", q.hint.strip()))
    parts.append("")
    solution_body = f"```python\n{q.solution.strip()}\n```\n\n**Why:** {q.explanation.strip()}"
    parts.append(_details("Solution", solution_body))

    starter = q.starter.strip() or f"# your answer here\n{q.entry} = ..."
    if q.kind in {"value", "predict"}:
        call = f"check('{q.qid}', {q.entry or 'answer'})"
    else:
        call = f"check('{q.qid}', {q.entry})"
    return [
        new_markdown_cell("\n".join(parts)),
        new_code_cell(f"{starter}\n\n{call}"),
    ]


def project_cells(p: Project) -> list:
    header = f"## Mini-project {p.pid} - {p.title}"
    body = "\n".join([header, "", p.brief.strip(), "",
                      _details("Hint", p.hint.strip()), "",
                      _details("Solution", f"```python\n{p.solution.strip()}\n```\n\n"
                                           f"**Why:** {p.explanation.strip()}")])
    starter = p.starter.strip() or f"# build it here\ndef {p.entry}(...):\n    ..."
    return [new_markdown_cell(body), new_code_cell(f"{starter}\n\ncheck('{p.pid}', {p.entry})")]


def render(notebook: Notebook) -> nbformat.NotebookNode:
    cells = [
        new_markdown_cell(f"# {notebook.number:02d} - {notebook.title}\n\n"
                          f"{notebook.intro.strip()}\n\n---\n\n{LEGEND}"),
        new_code_cell(BOOTSTRAP),
    ]
    current_level = None
    for q in sorted(notebook.questions, key=lambda x: (int(x.level), x.qid)):
        if int(q.level) != current_level:
            current_level = int(q.level)
            cells.append(new_markdown_cell(
                f"---\n\n## L{current_level} - {LEVEL_LABELS[current_level]}"))
        cells.extend(question_cells(q))
    if notebook.project:
        cells.append(new_markdown_cell("---"))
        cells.extend(project_cells(notebook.project))
    cells.append(new_markdown_cell("---\n\n## Your progress"))
    cells.append(new_code_cell("progress()"))

    nb = new_notebook(cells=cells)
    nb.metadata.kernelspec = KERNELSPEC
    nb.metadata.language_info = {"name": "python", "version": "3.13.14"}
    return nb


def write(notebook: Notebook, out_dir: Path, force: bool = False) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / notebook.filename
    if path.exists() and not force:
        return f"SKIP    {path.name} (exists; use --force to regenerate)"
    nbformat.write(render(notebook), path)
    return f"WROTE   {path.name}"


def drifted(notebook: Notebook, out_dir: Path) -> bool:
    path = out_dir / notebook.filename
    if not path.exists():
        return True
    existing = nbformat.read(path, as_version=4)
    fresh = render(notebook)
    return [c.source for c in existing.cells] != [c.source for c in fresh.cells]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite existing notebooks")
    parser.add_argument("--check", action="store_true", help="report drift, write nothing")
    parser.add_argument("--only", type=int, help="only this notebook number")
    args = parser.parse_args()

    books = [nb for nb in all_notebooks() if args.only in (None, nb.number)]
    if not books:
        print("no matching content modules")
        return 1

    if args.check:
        bad = [nb.filename for nb in books if drifted(nb, NOTEBOOK_DIR)]
        print("\n".join(f"DRIFT   {name}" for name in bad) or "all notebooks match content/")
        return 1 if bad else 0

    for nb in books:
        print(write(nb, NOTEBOOK_DIR, force=args.force))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_build.py -q`
Expected: PASS, 7 tests.

- [ ] **Step 5: Commit**

```bash
git add build.py tests/test_build.py
git commit -m "feat: add notebook renderer with clobber protection"
```

---

## Task 6: The guarantee — every solution passes its own cases

**Files:**
- Create: `tests/test_solutions_pass.py`, `tests/test_coverage.py`

**Interfaces:**
- Consumes: `content.all_notebooks`, `sprintcheck.run_question`.
- Produces: nothing importable. This is the safety net for Tasks 7 onward.

- [ ] **Step 1: Write `tests/test_solutions_pass.py`**

This is the core guarantee of the whole project: it executes each stored reference solution against that question's own cases.

```python
"""Executes every reference solution against its own test cases.

If this file is green, all shipped solutions are correct. This is what makes
400 questions trustworthy without hand-verifying them.
"""

import pytest

from content import all_notebooks
from sprintcheck import run_question


def _exec_solution(source: str, entry: str):
    """Run the stored solution and return whatever it binds to `entry`.

    For a `function` question that is a callable; for `value`/`predict` it is
    the value itself. Either way the source actually runs, so a solution that
    does not execute cannot ship.
    """
    namespace: dict = {}
    exec(compile(source, "<solution>", "exec"), namespace)
    if entry not in namespace:
        raise AssertionError(f"solution does not define {entry!r}")
    return namespace[entry]


def _question_params():
    return [
        pytest.param(nb.number, q, id=q.qid)
        for nb in all_notebooks()
        for q in nb.questions
    ]


@pytest.mark.parametrize("number,question", _question_params())
def test_reference_solution_passes_its_own_cases(number, question):
    # Every kind really executes its stored solution. Comparing
    # cases[0].expected against itself would have proved nothing.
    submission = _exec_solution(question.solution, question.entry)
    result = run_question(question, submission)
    assert result.passed, (
        f"{question.qid} reference solution failed its own cases:\n"
        + "\n".join(result.failures)
    )


def _project_params():
    return [
        pytest.param(nb.project, id=nb.project.pid)
        for nb in all_notebooks()
        if nb.project is not None
    ]


@pytest.mark.parametrize("project", _project_params())
def test_reference_project_solution_passes(project):
    from content.schema import Level, Question

    fn = _exec_solution(project.solution, project.entry)
    stand_in = Question(
        qid=project.pid, level=Level.L5, topic="Project", prompt=project.brief,
        hint=project.hint, solution=project.solution, explanation=project.explanation,
        kind="function", cases=project.cases, entry=project.entry,
    )
    result = run_question(stand_in, fn)
    assert result.passed, f"{project.pid} failed:\n" + "\n".join(result.failures)
```

- [ ] **Step 2: Write `tests/test_coverage.py`**

```python
"""Asserts the spec's difficulty curve and P0 topic quotas hold."""

from collections import Counter

import pytest

from content import all_notebooks

# spec section 5.1 - (L1, L2, L3, L4, L5) per notebook
EXPECTED_DISTRIBUTION = {
    1: (12, 11, 8, 3, 2),   2: (11, 12, 9, 4, 2),   3: (10, 12, 10, 4, 2),
    4: (9, 12, 10, 5, 2),   5: (9, 11, 9, 4, 3),    6: (6, 10, 13, 9, 4),
    7: (5, 10, 13, 9, 5),   8: (4, 9, 14, 11, 6),   9: (2, 7, 13, 15, 7),
    10: (2, 6, 11, 16, 7),
}

# spec section 4 - minimum questions tagged with each P0 topic
TOPIC_QUOTAS = {
    1: {"Variables": 2, "Primitive Types": 2, "Casting": 3, "Arithmetic": 4,
        "Comparison": 2, "Logical": 2, "Identity": 1, "Membership": 2,
        "Environment": 2, "Dynamic Typing": 2},
}


def notebooks_by_number():
    return {nb.number: nb for nb in all_notebooks()}


@pytest.mark.parametrize("number,expected", sorted(EXPECTED_DISTRIBUTION.items()))
def test_difficulty_distribution_matches_spec(number, expected):
    books = notebooks_by_number()
    if number not in books:
        pytest.skip(f"notebook {number:02d} not authored yet")
    counts = Counter(int(q.level) for q in books[number].questions)
    actual = tuple(counts.get(level, 0) for level in range(1, 6))
    assert actual == expected, f"nb{number:02d} L1-L5 = {actual}, spec says {expected}"


@pytest.mark.parametrize("number,quotas", sorted(TOPIC_QUOTAS.items()))
def test_p0_topic_quotas_met(number, quotas):
    books = notebooks_by_number()
    if number not in books:
        pytest.skip(f"notebook {number:02d} not authored yet")
    counts = Counter(q.topic for q in books[number].questions)
    shortfall = {t: (counts.get(t, 0), need) for t, need in quotas.items()
                 if counts.get(t, 0) < need}
    assert not shortfall, f"nb{number:02d} topic shortfall (have, need): {shortfall}"


def test_every_notebook_ends_on_a_hard_question():
    for nb in all_notebooks():
        levels = [int(q.level) for q in nb.questions]
        assert max(levels) == 5, f"nb{nb.number:02d} has no L5 question"


def test_generated_notebooks_match_content():
    from build import NOTEBOOK_DIR, drifted

    for nb in all_notebooks():
        if not (NOTEBOOK_DIR / nb.filename).exists():
            continue
        assert not drifted(nb, NOTEBOOK_DIR), (
            f"{nb.filename} is out of date with content/ - "
            f"run `python build.py --force --only {nb.number}` "
            f"(this will discard answers written in that notebook)"
        )
```

- [ ] **Step 3: Run the whole suite**

Run: `/home/topg/.venvs/ds/bin/python -m pytest -q`
Expected: the engine tests pass; coverage tests all SKIP (no content yet); `test_at_least_one_notebook_exists` still FAILS. That single failure is the correct signal that content is missing.

- [ ] **Step 4: Commit**

```bash
git add tests/test_solutions_pass.py tests/test_coverage.py
git commit -m "test: assert every reference solution passes its own cases"
```

---

## Task 7: NB01 content — L1 and L2 (Q-001..Q-023)

**Files:**
- Create: `content/nb01_foundations.py`

**Interfaces:**
- Consumes: `content.schema.{Case, Level, Notebook, Question}`.
- Produces: module-level `NOTEBOOK: Notebook` with `number=1, slug="foundations_and_operators"`. Task 8 appends to the same `QUESTIONS` list.

**Required question roster.** Author exactly these. `kind` and `topic` are fixed; the wording is yours to make clear.

| qid | L | topic | kind | what it asks |
|-----|---|-------|------|--------------|
| Q-001 | 1 | Variables | value | Bind `name`, `age`, `height` to a str, int and float; submit a tuple of the three |
| Q-002 | 1 | Primitive Types | function | `kinds(values)` -> list of `type(v).__name__` for each |
| Q-003 | 1 | Variables | function | `swap(a, b)` -> `(b, a)` using tuple unpacking |
| Q-004 | 1 | Arithmetic | function | `basics(a, b)` -> `(a+b, a-b, a*b, a/b)` |
| Q-005 | 1 | Arithmetic | function | `split(a, b)` -> `(a // b, a % b)` |
| Q-006 | 1 | Arithmetic | function | `power(base, exp)` using `**` |
| Q-007 | 1 | Casting | function | `to_int(text)` -> int from a numeric string |
| Q-008 | 1 | Casting | function | `label(n)` -> `"value: 42"` via `str()` |
| Q-009 | 1 | Comparison | function | `is_bigger(a, b)` -> bool |
| Q-010 | 1 | Logical | function | `both_and_either(a, b)` -> `(a and b, a or b, not a)` on bools |
| Q-011 | 1 | Membership | function | `has_vowel(word)` using `in` |
| Q-012 | 1 | Environment | output | `show_version()` prints `3.13` using `sys.version_info` |
| Q-013 | 2 | Primitive Types | function | `truthy(values)` -> list of `bool(v)` (covers `0`, `""`, `[]`, `None`) |
| Q-014 | 2 | Casting | function | `safe_int(text, default)` -> int or default on `ValueError` |
| Q-015 | 2 | Arithmetic | function | `to_time(seconds)` -> `(h, m, s)` using `divmod` |
| Q-016 | 2 | Arithmetic | function | `two_ways(x)` -> `(round(x), int(x))` showing truncation vs rounding |
| Q-017 | 2 | Dynamic Typing | function | `rebind()` -> list of type names as one name is reassigned |
| Q-018 | 2 | Comparison | function | `in_range(lo, x, hi)` using a chained comparison |
| Q-019 | 2 | Logical | function | `first_truthy(a, b)` -> `a or b`, returns the operand not a bool |
| Q-020 | 2 | Identity | function | `same_and_equal(a, b)` -> `(a is b, a == b)` |
| Q-021 | 2 | Membership | function | `missing_keys(d, keys)` using `not in` |
| Q-022 | 2 | Environment | function | `setting(name, fallback)` via `os.environ.get` |
| Q-023 | 2 | Arithmetic | function | `floor_negative(a, b)` -> `a // b` for negative operands |

- [ ] **Step 1: Write the module header and the first question**

Create `content/nb01_foundations.py`:

```python
"""Notebook 01 - Foundations & Operators (Q-001..Q-036)."""

from content.schema import Case, Level, Notebook, Project, Question

QUESTIONS: list[Question] = []


def q(**kwargs) -> None:
    QUESTIONS.append(Question(**kwargs))


q(
    qid="Q-001",
    level=Level.L1,
    topic="Variables",
    kind="value",
    entry="me",
    prompt=(
        "Create three variables — `name` (a string), `age` (a whole number) and "
        "`height` (a number with a decimal point) — then set `me` to the tuple "
        "`(name, age, height)`.\n\n"
        "Use exactly `\"Ada\"`, `36` and `1.7` so the checker can verify the types."
    ),
    hint="A tuple is written with commas: `me = name, age, height`. Note `36` and `36.0` are different types.",
    solution='name = "Ada"\nage = 36\nheight = 1.7\nme = (name, age, height)',
    explanation=(
        "Python infers each type from the literal you write: quotes make a `str`, "
        "a bare whole number makes an `int`, and a decimal point makes a `float`. "
        "The checker is strict about type, so `36.0` would not pass for `age`."
    ),
    starter='name = ...\nage = ...\nheight = ...\nme = ...',
    cases=[Case(expected=("Ada", 36, 1.7))],
)
```

- [ ] **Step 2: Run the integrity test on the one question**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_content_integrity.py -q`
Expected: PASS. `test_at_least_one_notebook_exists` will still fail until Step 4 adds `NOTEBOOK`.

- [ ] **Step 3: Author Q-002 through Q-023**

Follow the roster table. Each `q(...)` call must supply every field shown in Q-001. Rules that apply to all of them:

- `function`/`custom` questions need **at least 3 cases**, including the boring case *and* at least one edge case (empty input, zero, negative, or a type boundary). `output`/`value`/`predict` need at least 1. No question may repeat an identical case to pad a floor.
- `explanation` states *why*, never restates the code. One to three sentences.
- `hint` points at the concept; it must never contain the answer expression.
- `starter` gives the signature with an `...` body so the learner has somewhere to type.

Worked example for an `output` question (Q-012), since it is the only kind with a non-obvious shape:

```python
q(
    qid="Q-012",
    level=Level.L1,
    topic="Environment",
    kind="output",
    entry="show_version",
    prompt=(
        "Write `show_version()` so it prints the major and minor version of the "
        "running interpreter as `3.13` — read it from `sys.version_info`, do not "
        "hard-code the string."
    ),
    hint="`sys.version_info` is a named tuple: `.major` and `.minor` are ints. An f-string joins them.",
    solution=(
        "import sys\n\n\n"
        "def show_version():\n"
        "    print(f\"{sys.version_info.major}.{sys.version_info.minor}\")"
    ),
    explanation=(
        "`sys.version_info` is the reliable way to branch on Python version, because "
        "it compares as a tuple of ints. `sys.version` is a human-readable string and "
        "should never be parsed."
    ),
    starter="import sys\n\n\ndef show_version():\n    ...",
    cases=[Case(expected="3.13")],
)
```

- [ ] **Step 4: Append the `NOTEBOOK` object at the bottom of the file**

```python
NOTEBOOK = Notebook(
    number=1,
    slug="foundations_and_operators",
    title="Foundations & Operators",
    intro=(
        "Variables, the primitive types, dynamic typing, casting, and all five "
        "families of operator: arithmetic, comparison, logical, identity and "
        "membership.\n\n"
        "These are the questions everything else is built from. Do not skim them — "
        "the traps at the bottom of this notebook (`0.1 + 0.2`, `is` vs `==`, "
        "`True` being an `int`) are the ones that bite people three years in."
    ),
    questions=QUESTIONS,
    project=None,  # Task 8 sets this
)
```

- [ ] **Step 5: Run integrity and solution tests**

Run: `/home/topg/.venvs/ds/bin/python -m pytest tests/test_content_integrity.py tests/test_solutions_pass.py -q`
Expected: PASS, 23 solution tests green.

- [ ] **Step 6: Commit**

```bash
git add content/nb01_foundations.py
git commit -m "content: add NB01 L1-L2 questions (Q-001..Q-023)"
```

---

## Task 8: NB01 content — L3, L4, L5 and the mini-project

**Files:**
- Modify: `content/nb01_foundations.py`

**Interfaces:**
- Consumes: the `q()` helper and `QUESTIONS` list from Task 7.
- Produces: `NOTEBOOK.project` set to a `Project` with `pid="P-01"`.

**Required question roster:**

| qid | L | topic | kind | what it asks |
|-----|---|-------|------|--------------|
| Q-024 | 3 | Arithmetic | predict | What does `0.1 + 0.2 == 0.3` print, and `0.1 + 0.2`? Answer: `False` and `0.30000000000000004` |
| Q-025 | 3 | Identity | predict | `a = 256; b = 256; a is b` then the same with `257` — answer `True` then `False` |
| Q-026 | 3 | Casting | function | `parse_number(text)` -> `int` if integral, else `float`; type must be exact |
| Q-027 | 3 | Arithmetic | function | `wrap(index, length)` -> `index % length`, correct for negative index |
| Q-028 | 3 | Logical | custom | `xor(a, b)` without `^` or `!=`; constraints `["no-builtin:bool", "max-lines:3"]` |
| Q-029 | 3 | Comparison | function | `newest(records)` -> max by `(year, month)` tuple comparison |
| Q-030 | 3 | Dynamic Typing | function | `describe(value)` dispatching on `isinstance`, with `bool` checked before `int` |
| Q-031 | 3 | Comparison | custom | Refactor `if x == True:` / `if len(items) > 0:` into idiomatic truthiness; constraints `["no-builtin:len"]` |
| Q-032 | 4 | Casting | function | `to_number(text)` handling whitespace, `1_000`, `"12."`, rejecting `"True"` and `""` with `ValueError` |
| Q-033 | 4 | Arithmetic | function | `divide(a, b)` matching Python's floor/modulo sign rules for negatives, `(None, None)` on zero divisor |
| Q-034 | 4 | Primitive Types | predict | `True + True`, `isinstance(True, int)`, `{1: 'a', True: 'b'}` — answer `2`, `True`, `{1: 'b'}` |
| Q-035 | 5 | Comparison | custom | `almost_equal(a, b, rel_tol, abs_tol)` matching `math.isclose` semantics incl. inf/nan; constraints `["no-builtin:isclose"]` |
| Q-036 | 5 | Arithmetic | function | `py_round(x, ndigits=0)` reproducing banker's rounding: `0.5 -> 0`, `1.5 -> 2`, `2.5 -> 2`, `-0.5 -> 0` |

- [ ] **Step 1: Author Q-024 through Q-036**

Append `q(...)` calls to `content/nb01_foundations.py` **above** the `NOTEBOOK = ...` line.

Worked example for a `predict` question (Q-025), the only remaining non-obvious kind:

```python
q(
    qid="Q-025",
    level=Level.L3,
    topic="Identity",
    kind="predict",
    entry="answer",
    prompt=(
        "Without running it, predict the output:\n\n"
        "```python\n"
        "a = 256\nb = 256\nprint(a is b)\n\n"
        "c = 257\nd = 257\nprint(c is d)\n"
        "```\n\n"
        "Set `answer` to the two printed lines, e.g. `answer = \"True\\nFalse\"`."
    ),
    hint="CPython pre-creates a fixed pool of small integer objects at startup. Where does that pool stop?",
    solution='answer = "True\\nFalse"',
    explanation=(
        "CPython caches ints from -5 to 256, so `a` and `b` are literally the same "
        "object. 257 is outside the cache, so two separate objects are built and "
        "`is` is False — even though `==` is True for both. This is exactly why you "
        "compare values with `==` and only use `is` for `None`, `True` and `False`. "
        "The cache is an implementation detail: never write code that depends on it."
    ),
    starter='answer = ...',
    cases=[Case(expected="True\nFalse")],
)
```

- [ ] **Step 2: Define the mini-project and attach it**

Replace `project=None` in the `NOTEBOOK` definition with `project=PROJECT`, and define `PROJECT` above it:

```python
PROJECT = Project(
    pid="P-01",
    title="Receipt calculator",
    brief=(
        "Build `make_receipt(lines, tax_rate)`.\n\n"
        "`lines` is a list of `(name, qty_text, unit_price_text)` triples where the "
        "two numbers arrive as **strings**, the way they would from a form or a CSV. "
        "Return a dict:\n\n"
        "```python\n"
        "{'subtotal': 24.97, 'tax': 2.06, 'total': 27.03, 'items': 3}\n"
        "```\n\n"
        "Rules: quantities are whole numbers, prices have two decimals, every money "
        "value in the result is rounded to 2 decimal places, `items` is the total "
        "quantity (not the number of lines), and a malformed number raises "
        "`ValueError`. Tax is applied to the rounded subtotal."
    ),
    hint=(
        "Round once at each boundary, not continuously — compute the exact subtotal, "
        "round it, then derive tax from the rounded value. Rounding as you go makes "
        "the total disagree with the parts."
    ),
    solution=(
        "def make_receipt(lines, tax_rate):\n"
        "    subtotal = 0.0\n"
        "    items = 0\n"
        "    for name, qty_text, price_text in lines:\n"
        "        qty = int(qty_text)\n"
        "        price = float(price_text)\n"
        "        subtotal += qty * price\n"
        "        items += qty\n"
        "    subtotal = round(subtotal, 2)\n"
        "    tax = round(subtotal * tax_rate, 2)\n"
        "    return {\n"
        "        'subtotal': subtotal,\n"
        "        'tax': tax,\n"
        "        'total': round(subtotal + tax, 2),\n"
        "        'items': items,\n"
        "    }"
    ),
    explanation=(
        "This is the shape of most real input handling: strings in, numbers out, "
        "money rounded at defined boundaries. `int()` and `float()` already raise "
        "`ValueError` on junk, so the requirement is satisfied by not catching it — "
        "letting an exception propagate is a design choice, not an omission."
    ),
    entry="make_receipt",
    starter="def make_receipt(lines, tax_rate):\n    ...",
    cases=[
        Case(expected={"subtotal": 24.97, "tax": 2.06, "total": 27.03, "items": 3},
             args=([("pen", "2", "4.99"), ("pad", "1", "14.99")], 0.0825)),
        Case(expected={"subtotal": 0.0, "tax": 0.0, "total": 0.0, "items": 0},
             args=([], 0.0825)),
        Case(expected={"subtotal": 10.0, "tax": 0.0, "total": 10.0, "items": 10},
             args=([("nail", "10", "1.00")], 0.0)),
    ],
)
```

- [ ] **Step 3: Run the full suite**

Run: `/home/topg/.venvs/ds/bin/python -m pytest -q`
Expected: PASS everywhere. `test_difficulty_distribution_matches_spec[1-...]` now runs (not skips) and asserts NB01 is exactly `(12, 11, 8, 3, 2)`. Notebooks 2-10 still skip.

- [ ] **Step 4: Commit**

```bash
git add content/nb01_foundations.py
git commit -m "content: add NB01 L3-L5 questions and the P-01 mini-project"
```

---

## Task 9: Generate NB01, write the README, and open the gate

**Files:**
- Create: `README.md`, `notebooks/01_foundations_and_operators.ipynb`

**Interfaces:**
- Consumes: everything above.
- Produces: the artifact the learner opens. **This task ends in a human review gate.**

- [ ] **Step 1: Generate the notebook**

```bash
cd /home/topg/Projects/pythonsprints
/home/topg/.venvs/ds/bin/python build.py --only 1
```
Expected: `WROTE   01_foundations_and_operators.ipynb`

- [ ] **Step 2: Execute the notebook headlessly to prove every cell runs**

```bash
/home/topg/.venvs/ds/bin/jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=ds \
  --output /tmp/nb01_smoke.ipynb \
  notebooks/01_foundations_and_operators.ipynb
```
Expected: exit 0. Every cell runs — the unanswered `check()` calls print the "pass your answer" prompt rather than raising. If any cell raises, fix the renderer or the starter code before continuing.

- [ ] **Step 3: Verify no solution text leaked into an executable cell**

```bash
/home/topg/.venvs/ds/bin/python - <<'PY'
import nbformat
nb = nbformat.read("notebooks/01_foundations_and_operators.ipynb", as_version=4)
code = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
md   = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
assert md.count("<details>") == 2 * 36 + 2, md.count("<details>")  # 36 Qs + P-01
leaked = [ln for ln in code.splitlines() if "return " in ln and "..." not in ln]
print("code-cell return statements (should be empty):", leaked)
print("questions rendered:", md.count("### Q-"))
PY
```
Expected: `questions rendered: 36`, and an empty leak list.

- [ ] **Step 4: Write `README.md`**

```markdown
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

Each question has a markdown cell (prompt, collapsed hint, collapsed solution)
and a code cell where you answer:

```python
def flatten(grid):
    ...            # your code

check('Q-047', flatten)
```

`check()` prints PASS, or FAIL with the exact failing input, what was expected,
and what you returned.

Call `progress()` at any time for a per-notebook dashboard. Progress is stored
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

## Suggested pace

One notebook a day is aggressive but doable. Two rules that matter more than pace:

1. Open the **Hint** before the **Solution**, and only after a real attempt. A
   solution you read is worth roughly nothing; a solution you reached after a
   hint sticks.
2. When `check()` fails, read the failing case before changing anything. Debugging
   from evidence is the actual skill.

## Working on the content

Notebooks are generated from `content/` — that is the source of truth, holding
each question's prompt, solution and test cases on one object. `build.py` will
**not** overwrite a notebook you have answered questions in unless you pass
`--force`.

```bash
python build.py                    # generate any missing notebooks
python build.py --check            # report drift, write nothing
python -m pytest -q                # prove all 400 solutions pass their own cases
```
```

- [ ] **Step 5: Run the complete suite one final time**

```bash
/home/topg/.venvs/ds/bin/python -m pytest -q
/home/topg/.venvs/ds/bin/python build.py --check
```
Expected: all tests pass; `--check` reports `all notebooks match content/`.

- [ ] **Step 6: Commit**

```bash
git add README.md notebooks/
git commit -m "feat: generate NB01 and document the workflow"
```

- [ ] **Step 7: STOP — human review gate**

Do not begin Task 10. Report to the user:

- the command to open it (`~/.venvs/ds/bin/jupyter lab notebooks/`)
- how many questions rendered, and the L1-L5 counts
- that nbconvert executed every cell without error
- the specific things to judge: **question wording clarity, hint usefulness, whether the explanation teaches, the difficulty of the L5 pair, and whether `check()` failure output is actually helpful when you get one wrong**

Wait for explicit approval before Task 10. Format changes cost 36 rewrites now and 400 later — this gate exists to spend that difference wisely.

---

## Task 10 (repeated for notebooks 02..10): Author one notebook

Run this task nine times, once per notebook, in ascending order. Do not start it before the Task 9 gate is cleared.

**Files (per run, `NN` = notebook number):**
- Create: `content/nbNN_<slug>.py`
- Modify: `tests/test_coverage.py` (add that notebook's entry to `TOPIC_QUOTAS`)
- Create: `notebooks/NN_<slug>.ipynb` (generated)

**Interfaces:**
- Consumes: `content.schema.{Case, Level, Notebook, Project, Question}`.
- Produces: module-level `NOTEBOOK: Notebook`.

**Per-notebook parameters** (from spec sections 4 and 5.1 — these are fixed):

| NN | slug | title | ID block | L1 | L2 | L3 | L4 | L5 | total |
|----|------|-------|----------|----|----|----|----|----|-------|
| 02 | `strings` | Strings | Q-037..Q-074 | 11 | 12 | 9 | 4 | 2 | 38 |
| 03 | `lists_and_tuples` | Lists & Tuples | Q-075..Q-112 | 10 | 12 | 10 | 4 | 2 | 38 |
| 04 | `dicts_and_sets` | Dicts & Sets | Q-113..Q-150 | 9 | 12 | 10 | 5 | 2 | 38 |
| 05 | `control_flow_and_loops` | Control Flow & Loops | Q-151..Q-186 | 9 | 11 | 9 | 4 | 3 | 36 |
| 06 | `functions_scope_closures` | Functions, Scope & Closures | Q-187..Q-228 | 6 | 10 | 13 | 9 | 4 | 42 |
| 07 | `comprehensions_functional_recursion` | Comprehensions, Functional & Recursion | Q-229..Q-270 | 5 | 10 | 13 | 9 | 5 | 42 |
| 08 | `oop` | OOP | Q-271..Q-314 | 4 | 9 | 14 | 11 | 6 | 44 |
| 09 | `iterators_generators_decorators_context_exceptions` | Iterators, Generators, Decorators, Context Managers & Exceptions | Q-315..Q-358 | 2 | 7 | 13 | 15 | 7 | 44 |
| 10 | `stdlib_regex_typing_concurrency_testing` | Stdlib, Regex, Typing, Concurrency, Testing & Debugging | Q-359..Q-400 | 2 | 6 | 11 | 16 | 7 | 42 |

**Mini-projects** (`pid` is `P-NN`):

| NN | project |
|----|---------|
| 02 | Word-frequency report from a paragraph, formatted as an aligned table |
| 03 | Matrix utilities: transpose, rotate, and a deep-vs-shallow copy demonstration |
| 04 | Inventory manager: merge stock dicts, find low stock, set-algebra on SKUs |
| 05 | Number-guessing game loop with input validation and `else`-on-loop |
| 06 | Argument-validating decorator toolkit built from closures |
| 07 | Records pipeline: parse, filter, group and sort with comprehensions only |
| 08 | Bank-account hierarchy with `__repr__`, `__eq__`, properties and overdraft rules |
| 09 | `retry` + `lru_cache` decorators plus a paginated cursor generator |
| 10 | Log-parsing CLI using `pathlib`, `re` and `argparse`, with its own pytest suite |

**Per-run steps:**

- [ ] **Step 1: Draft the roster table before writing any code**

Write out all N questions as a table (qid, level, topic, kind, one-line description), exactly as Task 7 does. Check three things against the table before proceeding: the level counts match the row above; every P0 topic listed for this notebook in spec section 4 appears; the gotcha and refactor targets below are hit.

Per-notebook minimums, so the spec's "~45 gotchas, ~30 refactors" totals land:
- at least 4 `predict` (gotcha) questions
- at least 3 `custom` (refactor or constraint) questions

- [ ] **Step 2: Add the topic quota entry to `tests/test_coverage.py`**

Add a `TOPIC_QUOTAS[NN]` dict naming every P0 topic for this notebook with its minimum count, derived from the roster. This makes the test fail if a topic gets dropped during authoring.

- [ ] **Step 3: Write `content/nbNN_<slug>.py`**

Same structure as `nb01_foundations.py`: module docstring, `QUESTIONS` list, `q()` helper, one `q(...)` call per roster row, then `PROJECT`, then `NOTEBOOK`. Every question needs prompt, hint, solution, explanation, starter and cases. `function`/`custom` need at least 3 cases including an edge case; `output`/`value`/`predict` need at least 1. Never repeat an identical case to pad a floor.

- [ ] **Step 4: Run the suite**

Run: `/home/topg/.venvs/ds/bin/python -m pytest -q`
Expected: PASS. Specifically `test_reference_solution_passes_its_own_cases` must be green for every new qid, and `test_difficulty_distribution_matches_spec[NN-...]` must now run rather than skip.

- [ ] **Step 5: Generate and smoke-execute the notebook**

```bash
/home/topg/.venvs/ds/bin/python build.py --only NN
/home/topg/.venvs/ds/bin/jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=ds --output /tmp/nbNN_smoke.ipynb \
  notebooks/NN_<slug>.ipynb
```
Expected: `WROTE` then exit 0.

- [ ] **Step 6: Commit**

```bash
git add content/nbNN_<slug>.py tests/test_coverage.py notebooks/NN_<slug>.ipynb
git commit -m "content: add notebook NN <title> (Q-XXX..Q-YYY)"
```

---

## Final verification (after notebook 10)

- [ ] **Step 1: Prove all 400 exist and all solutions pass**

```bash
/home/topg/.venvs/ds/bin/python -m pytest -q
/home/topg/.venvs/ds/bin/python -c "
from content import all_questions
from collections import Counter
qs = all_questions()
print('questions:', len(qs))
print('by level :', dict(sorted(Counter(int(q.level) for q in qs).items())))
print('by kind  :', dict(Counter(q.kind for q in qs)))
"
```
Expected: `questions: 400`, levels `{1: 70, 2: 100, 3: 110, 4: 80, 5: 40}`, and roughly 45 `predict` / 30 `custom`.

- [ ] **Step 2: Confirm no notebook drifted**

Run: `/home/topg/.venvs/ds/bin/python build.py --check`
Expected: `all notebooks match content/`.

- [ ] **Step 3: Commit and report to the user**
