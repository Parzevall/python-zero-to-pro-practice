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
