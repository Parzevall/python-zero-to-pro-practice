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


def test_raises_case_passes_when_the_expected_exception_is_raised():
    q = make("function", [Case(expected=1, args=("1",)),
                          Case(expected=None, args=("x",), raises=ValueError),
                          Case(expected=2, args=("2",))], entry="parse")
    assert run_question(q, lambda t: int(t)).passed


def test_raises_case_fails_when_nothing_is_raised():
    q = make("function", [Case(expected=None, args=("x",), raises=ValueError)], entry="parse")
    result = run_question(q, lambda t: 0)
    assert not result.passed
    assert "ValueError to be raised" in result.failures[0]


def test_raises_case_fails_on_the_wrong_exception_type():
    q = make("function", [Case(expected=None, args=("x",), raises=ValueError)], entry="parse")
    result = run_question(q, lambda t: 1 / 0)
    assert not result.passed
    assert "ZeroDivisionError" in result.failures[0]


def test_a_mutating_solution_does_not_corrupt_the_stored_case():
    """check() twice on the same answer must grade identically."""
    q = make("function", [Case(expected=[1, 2, 3], args=([3, 1, 2],)),
                          Case(expected=[], args=([],)),
                          Case(expected=[5], args=([5],))], entry="sort_in_place")

    def sort_in_place(xs):
        xs.sort()
        return xs

    assert run_question(q, sort_in_place).passed
    assert run_question(q, sort_in_place).passed          # second run
    assert q.cases[0].args == ([3, 1, 2],), "stored case was mutated"
