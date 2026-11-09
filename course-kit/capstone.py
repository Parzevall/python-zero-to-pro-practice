"""Builds a capstone as a real project folder (not a notebook).

    import sys; sys.path.insert(0, "..")
    from capstone import Capstone
    cap = Capstone("NB20", title="Pageturner Library", intro="...", story="...")
    cap.starter({"catalog.py": "...", "books.json": "..."})    # files the learner gets
    cap.solution({"shelves.py": "...", "library.py": "..."})   # FINAL version of every file the learner writes
    cap.milestone("Shelves", prompt="...", writes=["shelves.py"], demo="...")   # x5-6, in order
    cap.build()

Output: <tier>/NBxx-<name>/ containing README.md, the starter files, an empty
(commented) file for everything the learner writes, demo_1.py ... demo_N.py
(given, standalone, `python demo_3.py` shows milestone 3 working), check.py
(compares each demo's output with the expected output) and solution/.

A file may be written across several milestones (the learner keeps extending
it); solution() holds its final version and every demo must work with it.
Demos are real scripts: no top-level await (use asyncio.run), they run from
the project folder, and anything they write goes in a tempfile directory.
The build runs every demo twice in fresh folders and once more in a reused
folder, and fails on errors, nondeterminism, or features not taught yet.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
import checker  # noqa: E402

_spec = importlib.util.spec_from_file_location("plan_data", HERE / "plan_data.py")
plan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(plan)
PLAN = {n["nb"]: n for n in plan.NOTEBOOKS}


def clean(text: str | None) -> str:
    return textwrap.dedent(text or "").strip("\n").rstrip()


class BuildError(RuntimeError):
    pass


CHECK_PY = '''"""Check your milestones.

    python check.py            check every milestone
    python check.py 3          check milestone 3 and show the difference if it's wrong
    python check.py --solution run the reference solution instead of your code

Each milestone has a demo script (demo_1.py, demo_2.py, ...) that uses your
modules. This runs it and compares what it prints with the expected output.
"""

import difflib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = __EXPECTED__
TITLES = __TITLES__


def run_demo(n, folder):
    try:
        proc = subprocess.run([sys.executable, f"demo_{n}.py"], cwd=folder, text=True,
                              capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "", "timed out after 120 seconds (an endless loop?)"
    return proc.stdout.rstrip("\\n"), proc.stderr.strip()


def main():
    args = sys.argv[1:]
    use_solution = "--solution" in args
    picked = [int(a) for a in args if a.isdigit()]
    numbers = picked or sorted(EXPECTED)
    folder = HERE
    if use_solution:
        tmp = tempfile.mkdtemp()
        for path in HERE.iterdir():
            if path.is_file() and path.name != "check.py":
                shutil.copy(path, tmp)
        for path in (HERE / "solution").iterdir():
            shutil.copy(path, tmp)
        folder = tmp
    passed = 0
    for n in numbers:
        out, err = run_demo(n, folder)
        ok = out == EXPECTED[n]
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  Milestone {n}: {TITLES[n]}")
        if not ok and (picked or use_solution):
            if err:
                print("\\n  Your code raised an error. The last lines:\\n")
                print(textwrap_indent("\\n".join(err.splitlines()[-8:])))
            print("\\n  Difference (- expected, + yours):\\n")
            diff = difflib.unified_diff(EXPECTED[n].splitlines(), out.splitlines(),
                                        "expected", "yours", lineterm="", n=1)
            print(textwrap_indent("\\n".join(list(diff)[2:]) or "(no output)"))
            print()
    print(f"\\n{passed} of {len(numbers)} passed.")
    if not picked and passed < len(numbers):
        print("Run  python check.py N  to see what's different for milestone N.")


def textwrap_indent(text):
    return "\\n".join("    " + line for line in text.splitlines())


if __name__ == "__main__":
    main()
'''


class Capstone:
    def __init__(self, nb_id: str, *, title: str, intro: str, story: str):
        self.id = nb_id
        self.info = PLAN[nb_id]
        self.number = int(nb_id[2:])
        self.title = title
        self.intro = clean(intro)
        self.story = clean(story)
        self.starter_files: dict[str, str] = {}
        self.solution_files: dict[str, str] = {}
        self.milestones: list[dict] = []

    def starter(self, files: dict[str, str]) -> None:
        self.starter_files = {k: clean(v) for k, v in files.items()}

    def solution(self, files: dict[str, str]) -> None:
        self.solution_files = {k: clean(v) for k, v in files.items()}

    def milestone(self, title: str, *, prompt: str, writes: list[str], demo: str) -> None:
        self.milestones.append(dict(title=title, prompt=clean(prompt), writes=list(writes),
                                    demo=clean(demo)))

    # ------------------------------------------------------------ checking
    def _validate(self) -> None:
        if not 4 <= len(self.milestones) <= 7:
            raise BuildError(f"{self.id}: want 4-7 milestones, got {len(self.milestones)}")
        written = {f for m in self.milestones for f in m["writes"]}
        for f in written:
            if f not in self.solution_files and f not in self.starter_files:
                raise BuildError(f"{self.id}: '{f}' is written in a milestone but has no solution")
        for f in self.solution_files:
            if f not in written:
                raise BuildError(f"{self.id}: solution file '{f}' isn't written in any milestone")
        for i, m in enumerate(self.milestones, 1):
            try:
                compile(m["demo"], f"demo_{i}.py", "exec")
            except SyntaxError as e:
                raise BuildError(f"{self.id}: demo_{i}.py doesn't compile: {e}") from None
        program = "\n".join([*self.solution_files.values(), *self.starter_files.values(),
                             *(m["demo"] for m in self.milestones),
                             *self.solution_files, *self.starter_files])
        sources = {**{n: b for n, b in self.solution_files.items() if n.endswith(".py")},
                   **{f"demo_{i}.py": m["demo"] for i, m in enumerate(self.milestones, 1)}}
        for name, body in sources.items():
            bad = checker.too_early(body, self.number, program)
            if bad:
                raise BuildError(f"{self.id} {name}: uses things not taught yet: {', '.join(bad)}")

    def _stage(self, folder: Path, solution: bool) -> None:
        for name, body in self.starter_files.items():
            (folder / name).write_text(body + "\n", encoding="utf-8")
        if solution:
            for name, body in self.solution_files.items():
                (folder / name).write_text(body + "\n", encoding="utf-8")
        for i, m in enumerate(self.milestones, 1):
            (folder / f"demo_{i}.py").write_text(m["demo"] + "\n", encoding="utf-8")

    def _run_all(self, folder: Path, seed: int) -> list[str]:
        env = {**os.environ, "PYTHONHASHSEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1",
               "PYTHONIOENCODING": "utf-8", "PYTHONWARNINGS": "ignore"}
        outs = []
        for i in range(1, len(self.milestones) + 1):
            try:
                proc = subprocess.run([sys.executable, f"demo_{i}.py"], cwd=folder, env=env,
                                      text=True, capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                raise BuildError(f"{self.id} demo_{i}.py: timed out") from None
            if proc.returncode != 0:
                raise BuildError(f"{self.id} demo_{i}.py failed:\n{proc.stderr[-1500:]}")
            outs.append(proc.stdout.rstrip("\n"))
        return outs

    def expected(self) -> list[str]:
        runs = []
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for folder, seed in ((Path(a), 0), (Path(b), 1)):
                self._stage(folder, solution=True)
                runs.append(self._run_all(folder, seed))
            runs.append(self._run_all(Path(a), 2))  # same folder again: demos must not depend on leftovers
        for i, (x, y, z) in enumerate(zip(*runs), 1):
            if not x == y == z:
                raise BuildError(f"{self.id} demo_{i}.py: output differs between runs "
                                 "(set order, randomness, or files left over from an earlier run?)")
        return runs[0]

    # ------------------------------------------------------------ rendering
    def _readme(self, outs: list[str]) -> str:
        info = self.info
        owners: dict[str, list[int]] = {}
        for i, m in enumerate(self.milestones, 1):
            for f in m["writes"]:
                owners.setdefault(f, []).append(i)
        rows = []
        for name in self.starter_files:
            what = "starter file: read it"
            if name in owners:
                what += f"; you extend it in milestone {', '.join(map(str, owners[name]))}"
            rows.append(f"| `{name}` | {what} |")
        for name, ms in owners.items():
            if name not in self.starter_files:
                rows.append(f"| `{name}` | **you write it** (milestone {', '.join(map(str, ms))}) |")
        rows.append(f"| `demo_1.py` … `demo_{len(self.milestones)}.py` | shows each milestone working (don't edit) |")
        rows.append("| `check.py` | checks your milestones |")
        rows.append("| `solution/` | the reference answer (look only after a real attempt) |")
        prereqs = "\n".join(f"- {x}" for x in info["prereq"])
        covers = "\n".join(f"- {x}" for x in info["covers"])
        parts = [
            f"# {self.id} · {info['tier'].title()} Capstone: {self.title}",
            self.intro,
            f"## You'll need\n\n{prereqs}\n\n## You'll practise\n\n{covers}",
            f"## The story\n\n{self.story}",
            "## How to work\n\n"
            "This is a real project, not a notebook. Open this folder in your editor "
            "(VS Code: *File → Open Folder*) and a terminal in it.\n\n"
            "1. Read the milestone below, then write the code in the file(s) it names.\n"
            "2. Run `python demo_N.py` to watch your code run, or `python check.py N` to "
            "compare its output with the expected output and see the difference.\n"
            "3. `python check.py` checks every milestone at once.\n"
            "4. Stuck after a real attempt? `solution/` has the answer, and "
            "`python check.py --solution` runs it.\n\n"
            "Each demo imports your modules fresh, so after editing a file just run it again.",
            "## Files\n\n| File | What it is |\n|---|---|\n" + "\n".join(rows),
        ]
        for i, (m, out) in enumerate(zip(self.milestones, outs), 1):
            files = ", ".join(f"`{f}`" for f in m["writes"])
            parts.append(f"## Milestone {i} · {m['title']}\n\n{m['prompt']}\n\n"
                         f"**You write:** {files} · **Check:** `python check.py {i}`\n\n"
                         f"**Expected output** (`python demo_{i}.py`):\n\n```text\n{out}\n```")
        parts.append("## Done\n\n" + ("That's the whole course. Well played."
                                      if self.id == "NB32" else
                                      "On to the advanced tier: **NB21 · OOP Advanced** in `advanced/`."))
        return "\n\n".join(parts) + "\n"

    @property
    def path(self) -> Path:
        return REPO / self.info["tier"] / f"{self.id}-{self.info['name']}"

    def build(self) -> None:
        try:
            self._validate()
            outs = self.expected()
        except BuildError as e:
            print(f"BUILD FAILED: {e}")
            sys.exit(1)
        out = self.path
        if out.exists():
            shutil.rmtree(out)
        (out / "solution").mkdir(parents=True)
        self._stage(out, solution=False)
        owners: dict[str, list[int]] = {}
        for i, m in enumerate(self.milestones, 1):
            for f in m["writes"]:
                owners.setdefault(f, []).append(i)
        for name, ms in owners.items():
            if name not in self.starter_files:
                where = ", ".join(map(str, ms))
                (out / name).write_text(f"# {name}: you write this (milestone {where}). See README.md.\n",
                                        encoding="utf-8")
        for name, body in self.solution_files.items():
            (out / "solution" / name).write_text(body + "\n", encoding="utf-8")
        expected = "{\n" + "".join(f"    {i}: {o!r},\n" for i, o in enumerate(outs, 1)) + "}"
        titles = "{\n" + "".join(f"    {i}: {m['title']!r},\n" for i, m in enumerate(self.milestones, 1)) + "}"
        check = CHECK_PY.replace("__EXPECTED__", expected).replace("__TITLES__", titles)
        (out / "check.py").write_text(check, encoding="utf-8")
        (out / "README.md").write_text(self._readme(outs), encoding="utf-8")
        lines = sum(len(b.splitlines()) for b in self.solution_files.values())
        print(f"OK wrote {out.relative_to(REPO)}/ ({len(self.milestones)} milestones, "
              f"{lines} solution lines)")
