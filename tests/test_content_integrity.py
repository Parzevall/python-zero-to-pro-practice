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
        # repr, not the values: args and kwargs legitimately hold lists and dicts,
        # which are unhashable and so cannot go into a set directly.
        seen = [
            (repr(c.args), repr(sorted(c.kwargs.items())), repr(c.expected))
            for c in q.cases
        ]
        assert len(seen) == len(set(seen)), f"{q.qid}: duplicate case - pad with real ones"


def test_every_question_declares_an_entry_point():
    # Every kind needs it: the solution test execs the solution and looks this
    # name up, and build.py renders it into the check() call.
    for q in all_questions():
        assert q.entry, f"{q.qid}: needs entry (the function or variable name)"
