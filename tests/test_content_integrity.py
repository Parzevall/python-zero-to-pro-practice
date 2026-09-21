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


def test_no_starter_shadows_the_grader_at_module_level():
    """A module-level `def check(...)` in a starter silently replaces the
    grader for every cell below it, so later questions fail with a nonsense
    error even when the answer is right. Nested defs and methods are fine."""
    import ast

    from content import all_notebooks

    reserved = {"check", "progress", "reset"}
    clashes = []
    for nb in all_notebooks():
        for item in list(nb.questions) + ([nb.project] if nb.project else []):
            qid = getattr(item, "qid", None) or item.pid
            for label in ("starter", "solution"):
                source = getattr(item, label, "")
                if not source.strip():
                    continue
                for node in ast.parse(source).body:          # top level only
                    name = getattr(node, "name", None)
                    if name in reserved:
                        clashes.append(f"{qid} {label}: defines {name}()")
                    if isinstance(node, ast.Assign):
                        for t in node.targets:
                            if isinstance(t, ast.Name) and t.id in reserved:
                                clashes.append(f"{qid} {label}: assigns {t.id}")
    assert not clashes, "grader names shadowed: " + "; ".join(clashes)
