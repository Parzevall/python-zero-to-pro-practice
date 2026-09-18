"""Executes every reference solution against its own test cases.

If this file is green, all shipped solutions are correct. This is what makes
400 questions trustworthy without hand-verifying them.
"""

import linecache

import pytest

from content import all_notebooks
from sprintcheck import run_question

SOLUTION_FILE = "<solution>"


def _exec_solution(source: str, entry: str):
    """Run the stored solution and return whatever it binds to `entry`.

    For a `function` question that is a callable; for `value`/`predict` it is
    the value itself. Either way the source actually runs, so a solution that
    does not execute cannot ship.
    """
    # Do not delete: this is what makes `custom` questions testable at all.
    #
    # IPython registers each cell's source in linecache, and that is the only
    # reason inspect.getsource() works for a function a learner defines in a
    # notebook cell - which is what check_constraints() needs to read the AST.
    # An exec'd function has no source on disk, so without this seeding
    # inspect raises OSError, check_constraints() reports "could not read
    # source", and every custom question fails here no matter how it is
    # written. Seeding linecache under the same filename we compile with
    # reproduces the notebook faithfully, so constraints are enforced on
    # reference solutions exactly as they are on a learner's answer.
    linecache.cache[SOLUTION_FILE] = (
        len(source), None, source.splitlines(keepends=True), SOLUTION_FILE,
    )
    namespace: dict = {}
    exec(compile(source, SOLUTION_FILE, "exec"), namespace)
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
