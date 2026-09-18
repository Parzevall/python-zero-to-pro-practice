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
