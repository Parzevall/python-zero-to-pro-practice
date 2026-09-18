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
