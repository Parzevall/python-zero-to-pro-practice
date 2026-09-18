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
