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
