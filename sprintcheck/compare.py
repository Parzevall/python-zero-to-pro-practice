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
