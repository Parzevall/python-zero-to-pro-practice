"""Format v3 builder: 19 progressive Write questions + a story project (Q20),
or a capstone notebook that is one big story project built in milestones.

Source file (course-kit/src/nbXX.py), built with `cd course-kit/src && python3 nbXX.py`:

    import sys; sys.path.insert(0, "..")
    from builder import Notebook
    nb = Notebook("NB01", intro="...")
    nb.q("Build", "prompt text", solution="...", given="...")     # x19, in ramp order
    nb.project("Cafe Closing Time", story="...", given="...",
               steps=[("prompt", "solution"), ...])               # Q20
    nb.build()

Capstone (NB08/NB20/NB32): no nb.q() calls, just nb.project(...) with 4-6 steps.

Expected output is never typed by hand: build() runs given + solutions and
fills it in. build() also fails if a solution uses something not taught yet (checker.too_early),
crashes, times out, or prints different output on two runs.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
import checker as verify  # noqa: E402

_spec = importlib.util.spec_from_file_location("plan_data", HERE / "plan_data.py")
plan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(plan)
PLAN = {n["nb"]: n for n in plan.NOTEBOOKS}
ORDER = [n["nb"] for n in plan.NOTEBOOKS]

KINDS = {"Build", "Output-match", "Puzzle", "Real-life"}
RAMP = [  # (first question, last question, section heading)
    (1, 5, "Warm-up · one line each"),
    (6, 10, "Combine · 2 to 4 lines"),
    (11, 15, "Small real tasks · 5 to 8 lines"),
    (16, 19, "Puzzles & builds · 8 to 15 lines"),
]
SEP = "\x1e--STEP--\x1e"


def clean(text: str | None) -> str:
    return textwrap.dedent(text or "").strip("\n").rstrip()


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": text.splitlines(keepends=True)}


def fence(body: str, lang: str = "python") -> str:
    return f"```{lang}\n{body}\n```"


def solution_box(sol: str) -> str:
    return f"<details><summary><b>Solution</b></summary>\n\n{fence(sol)}\n\n</details>"


class BuildError(RuntimeError):
    pass


class Notebook:
    def __init__(self, nb_id: str, intro: str = "", title: str | None = None):
        self.id = nb_id
        self.info = PLAN[nb_id]
        self.number = int(nb_id[2:])
        self.title = title or self.info["name"].replace("-", " ")
        self.intro = clean(intro)
        self.questions: list[dict] = []
        self.proj: dict | None = None

    # ---------------------------------------------------------- authoring
    def q(self, kind: str, prompt: str, *, solution: str, given: str = "") -> None:
        if kind not in KINDS:
            raise BuildError(f"{self.id}: kind must be one of {sorted(KINDS)}, got {kind!r}")
        self.questions.append(dict(kind=kind, prompt=clean(prompt), solution=clean(solution),
                                   given=clean(given)))

    def project(self, title: str, *, story: str, steps: list[tuple], given: str = "",
                given_files: dict[str, str] | None = None) -> None:
        """steps: (prompt, solution) or (prompt, solution, {"file.py": code}).
        Files become `%%writefile` cells; each file name may be written only once.
        given_files: starter files (data, or a teammate's module) the learner runs first."""
        norm = []
        for step in steps:
            prompt, sol, files = (*step, {}) if len(step) == 2 else step
            if not clean(sol):
                raise BuildError(f"{self.id}: every step needs a solution that prints something")
            norm.append((clean(prompt), clean(sol), {k: clean(v) for k, v in files.items()}))
        names = list(given_files or {}) + [n for _, _, f in norm for n in f]
        if len(names) != len(set(names)):
            raise BuildError(f"{self.id}: a file is written twice ({names}); write each file once")
        self.proj = dict(title=title, story=clean(story), given=clean(given), steps=norm,
                         given_files={k: clean(v) for k, v in (given_files or {}).items()})

    # ------------------------------------------------------------ checking
    def _run(self, label: str, parts: list[str]) -> list[str]:
        """Run parts joined by step separators; return each part's output."""
        program = f"\nprint({SEP!r})\n".join(parts)
        a, b = verify.run(program, 0), verify.run(program, 1)
        if a.timed_out:
            raise BuildError(f"{self.id} {label}: timed out")
        if a.error:
            raise BuildError(f"{self.id} {label}: raised {a.error}\n{a.stderr[-800:]}")
        if a.stdout != b.stdout:
            raise BuildError(f"{self.id} {label}: output differs between runs (set order? randomness?)")
        outs = a.stdout.split(SEP + "\n")
        return [o.rstrip("\n") or "(prints nothing)" for o in outs]

    def _taught(self, label: str, source: str, program: str) -> None:
        bad = verify.too_early(source, self.number, program)
        if bad:
            raise BuildError(f"{self.id} {label}: uses things not taught yet: {', '.join(bad)}")

    # ------------------------------------------------------------ rendering
    def _question(self, n: int, item: dict) -> list[dict]:
        parts = [item["given"], item["solution"]] if item["given"] else [item["solution"]]
        program = "\n".join(parts)
        self._taught(f"Q{n:02d}", item["solution"], program)
        expected = self._run(f"Q{n:02d}", [program])[0]
        text = (f"### Q{n:02d} · {item['kind']}\n\n{item['prompt']}\n\n"
                f"**Expected output:**\n\n{fence(expected, 'text')}\n\n{solution_box(item['solution'])}")
        cell = f"{item['given']}\n\n# your code here\n" if item["given"] else "# your code here\n"
        return [md(text), code(cell)]

    @staticmethod
    def _writer(files: dict[str, str]) -> str:
        """Code that creates files the way a %%writefile cell would."""
        lines = ["import importlib as _il"]
        for name, body in files.items():
            lines.append(f"open({name!r}, 'w', encoding='utf-8').write({(body + chr(10))!r})")
        lines.append("_il.invalidate_caches()")
        return "\n".join(lines) if files else ""

    def _project(self, capstone: bool) -> list[dict]:
        p = self.proj
        all_files = dict(p["given_files"])
        for _, _, f in p["steps"]:
            all_files.update(f)
        program = "\n".join([p["given"], *[s for _, s, _ in p["steps"]], *all_files.values(),
                             *all_files])  # names count, so the learner's own modules may be imported
        for i, (_, s, files) in enumerate(p["steps"], 1):
            self._taught(f"project step {i}", s, program)
            for name, body in files.items():
                if name.endswith(".py"):
                    self._taught(f"project step {i} {name}", body, program)
        parts = ["\n".join(x for x in (self._writer(p["given_files"]), p["given"]) if x)]
        parts += ["\n".join(x for x in (self._writer(f), s) if x) for _, s, f in p["steps"]]
        outs = self._run("project", parts)[1:]
        word = "Milestone" if capstone else "Step"
        head = "##" if capstone else "## Q20 · Story project:"
        cells = [md(f"---\n\n{head} {p['title']}\n\n{p['story']}")]
        if all_files:
            cells.append(md("**About files:** a cell that starts with `%%writefile name.py` saves its "
                            "contents as a real file next to this notebook, which other cells can then "
                            "`import`. If you change a module after importing it, restart the kernel "
                            "and run the cells again from the top."))
        if p["given_files"] or p["given"]:
            cells.append(md("**Run these cells first.** They set up the starting files and data "
                            "for every step below."))
            for name, body in p["given_files"].items():
                cells.append(code(f"%%writefile {name}\n{body}\n"))
            if p["given"]:
                cells.append(code(p["given"] + "\n"))
        for i, ((prompt, sol, files), out) in enumerate(zip(p["steps"], outs), 1):
            shown = "\n\n".join([fence(f"# --- {n} ---\n{b}") for n, b in files.items()] + [fence(sol)])
            box = f"<details><summary><b>Solution</b></summary>\n\n{shown}\n\n</details>"
            text = (f"{'##' if capstone else '###'} {word} {i}\n\n{prompt}\n\n"
                    f"**Expected output:**\n\n{fence(out, 'text')}\n\n{box}")
            cells.append(md(text))
            for name in files:
                cells.append(code(f"%%writefile {name}\n# your code here\n"))
            cells.append(code("# your code here\n"))
        return cells

    def render(self) -> dict:
        info = self.info
        capstone = not self.questions
        if capstone and not self.proj:
            raise BuildError(f"{self.id}: no questions and no project")
        if not capstone and len(self.questions) != 19:
            raise BuildError(f"{self.id}: need exactly 19 questions + project, got {len(self.questions)}")
        if not self.proj:
            raise BuildError(f"{self.id}: missing project (Q20)")
        pos = ORDER.index(self.id)
        nxt = PLAN[ORDER[pos + 1]] if pos + 1 < len(ORDER) else None
        size = (f"one story project in {len(self.proj['steps'])} milestones" if capstone
                else "20 questions · the last one is a story project")
        prereqs = "\n".join(f"- {x}" for x in info["prereq"])
        covers = "\n".join(f"- {x}" for x in info["covers"])
        how = ("## How it works\n\n"
               "Write your code in the cell under each question, run it, and compare with "
               "**Expected output**. Open **Solution** only after a real attempt.\n\n"
               + ("Each milestone builds on the one before, so run the cells in order."
                  if capstone else
                  "Questions get longer as you go: one-liners first, a small story project last. "
                  "Every solution only uses what this notebook and the ones before it teach."))
        cells = [md(f"# {self.id} · {self.title}\n\n`{info['tier']}/` · {size}\n\n{self.intro}"),
                 md(f"## You'll need\n\n{prereqs}\n\n## You'll practise\n\n{covers}"),
                 md(how)]
        for first, last, heading in ([] if capstone else RAMP):
            cells.append(md(f"---\n\n## {heading}"))
            for n in range(first, last + 1):
                cells += self._question(n, self.questions[n - 1])
        cells += self._project(capstone)
        tail = (f"Next up: **{nxt['nb']} · {nxt['name'].replace('-', ' ')}** in `{nxt['tier']}/`."
                if nxt else "That's the whole course. Well played.")
        cells.append(md(f"---\n\n## Done\n\n{tail}"))
        for i, c in enumerate(cells):
            c["id"] = f"{self.id.lower()}-{i:03d}"
        return {"cells": cells,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                            "name": "python3"},
                             "language_info": {"name": "python"}},
                "nbformat": 4, "nbformat_minor": 5}

    @property
    def path(self) -> Path:
        return REPO / self.info["tier"] / f"{self.id}-{self.info['name']}.ipynb"

    def build(self) -> None:
        try:
            nb = self.render()
        except BuildError as e:
            print(f"BUILD FAILED: {e}")
            sys.exit(1)
        self.path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        what = (f"capstone, {len(self.proj['steps'])} milestones" if not self.questions
                else "19 questions + story project")
        print(f"OK wrote {self.path.relative_to(REPO)} ({what})")
