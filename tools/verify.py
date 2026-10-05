#!/usr/bin/env python3
"""Check every practice notebook before it reaches a learner.

    python tools/verify.py                      # every notebook
    python tools/verify.py beginner/NB01-*.ipynb
    python tools/verify.py --quick              # one run per program, not two

For every question it:

* runs the Solution and checks it prints exactly the Expected output,
* runs the Senior dev solution and checks it prints the same thing,
* checks Predict / Error / Fix / Refactor code behaves the way the question says,
* runs the main program twice with different hash seeds, so output that changes
  between runs (set order, randomness, the clock) is caught,
* checks the Solution only uses what this notebook or an earlier one teaches.
  Senior solutions are allowed to reach ahead, so they are not checked.

It never looks at your own answers. Standard library only.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIERS = ("beginner", "intermediate", "advanced")
CAPSTONES = {"NB08", "NB20", "NB32"}
TYPES = ("Write", "Predict", "Error", "Fix", "Refactor")
DROPDOWNS = ("Hint", "Expected output", "Solution", "Senior dev solution")
TIMEOUT = 30

HEADER_RE = re.compile(
    r"^#{2,3} (?P<nb>NB\d{2})-(?P<q>Q\d{2}|P) · L(?P<level>[1-5]) · (?P<topic>.+?) · "
    r"(?P<type>" + "|".join(TYPES) + r")(?: \[(?P<min>3\.\d+)\+\])?\s*$"
)
DETAILS_RE = re.compile(r"<details><summary><b>(.+?)</b></summary>\s*\n(.*?)\n\s*</details>", re.S)
FENCE_RE = re.compile(r"```(\w*)\n(.*?)\n```", re.S)
FILE_RE = re.compile(r"^(NB\d{2})-[A-Za-z0-9-]+\.ipynb$")
# The code a learner works from sits right under one of these bold lead lines.
# Other ```python blocks in a prompt are just illustrations.
SHOWN_RE = re.compile(
    r"\*\*(?:Starting code|What does this print\?|Which error does this raise\?|Buggy code|"
    r"Working code to refactor)[^\n]*\*\*\s*\n+```python\n(.*?)\n```", re.S)

# ----------------------------------------------------------------- running

# Runs a program the way a notebook cell would: in a fresh __main__ module,
# with top-level `await` allowed (Jupyter permits it, plain scripts do not).
RUNNER = r"""
import ast, asyncio, inspect, sys, types
src = sys.stdin.read()
module = types.ModuleType("__main__")
sys.modules["__main__"] = module
try:
    code = compile(src, "<cell>", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    if code.co_flags & inspect.CO_COROUTINE:
        asyncio.run(eval(code, module.__dict__))
    else:
        exec(code, module.__dict__)
except BaseException as exc:
    sys.stdout.flush()
    sys.stderr.write("\n\x00EXC:" + type(exc).__name__ + "\n")
"""


@dataclass
class Run:
    stdout: str
    error: str | None      # exception class name, if the program raised
    timed_out: bool = False
    stderr: str = ""

    @property
    def shown(self) -> str:
        """What the Expected output dropdown holds for this run."""
        out = self.stdout.rstrip("\n")
        if self.error:
            out = f"{out}\n{self.error}" if out else self.error
        return out


def run(source: str, seed: int = 0) -> Run:
    env = {**os.environ, "PYTHONHASHSEED": str(seed), "PYTHONIOENCODING": "utf-8",
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONWARNINGS": "ignore"}
    with tempfile.TemporaryDirectory() as cwd:
        try:
            proc = subprocess.run([sys.executable, "-c", RUNNER], input=source, text=True,
                                  capture_output=True, cwd=cwd, env=env, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            return Run("", None, timed_out=True)
    error = None
    stderr = proc.stderr
    marker = stderr.rfind("\x00EXC:")
    if marker != -1:
        error = stderr[marker + 5:].strip()
        stderr = stderr[:marker]
    return Run(proc.stdout, error, stderr=stderr)


# ------------------------------------------------------------- curriculum

# The notebook that first teaches each module. Anything not listed is an
# error, so a new import is always a deliberate decision.
MODULES = {
    "math": 1, "sys": 1, "keyword": 1,
    "copy": 5, "pprint": 6, "functools": 9, "operator": 10, "traceback": 12,
    **dict.fromkeys(["pathlib", "json", "csv", "tempfile", "os", "glob", "pickle", "shelve",
                     "configparser", "xml", "io", "errno", "fnmatch", "importlib", "runpy"], 13),
    **dict.fromkeys(["collections", "itertools", "datetime", "zoneinfo", "random", "statistics",
                     "string", "textwrap", "platform", "calendar", "time", "difflib",
                     "locale"], 15),
    **dict.fromkeys(["decimal", "fractions", "unicodedata", "struct", "cmath", "binascii",
                     "base64", "ipaddress"], 16),
    "re": 17, "heapq": 19, "bisect": 19, "graphlib": 19,
    **dict.fromkeys(["dataclasses", "enum", "abc", "numbers", "reprlib"], 21),
    "inspect": 23, "contextlib": 24,
    **dict.fromkeys(["types", "builtins", "ast", "tokenize"], 25),
    **dict.fromkeys(["typing", "annotationlib"], 26),
    **dict.fromkeys(["threading", "queue", "concurrent", "asyncio", "contextvars", "sched"], 27),
    **dict.fromkeys(["unittest", "doctest", "logging", "warnings", "pdb"], 28),
    **dict.fromkeys(["timeit", "cProfile", "pstats", "gc", "tracemalloc", "array", "weakref",
                     "dis"], 29),
    **dict.fromkeys(["socket", "socketserver", "http", "urllib", "selectors", "html"], 30),
    **dict.fromkeys(["argparse", "sqlite3", "subprocess", "tomllib", "shutil", "zipfile",
                     "hashlib", "hmac", "secrets", "uuid", "gzip", "tarfile", "compression",
                     "zlib", "shlex", "atexit", "signal"], 31),
}

CALLS = {
    "len": 2, "ord": 2, "chr": 2, "repr": 2, "format": 2,
    "range": 4, "enumerate": 4, "zip": 4, "reversed": 4,
    "list": 5, "sorted": 5, "sum": 5, "tuple": 5,
    "dict": 6, "set": 6, "frozenset": 6, "hash": 6,
    "callable": 9, "map": 10, "filter": 10, "any": 10, "all": 10,
    "open": 13,
    "issubclass": 14, "super": 14, "hasattr": 14, "getattr": 14, "setattr": 14,
    "delattr": 14, "vars": 14,
    "iter": 22, "next": 22, "eval": 25, "exec": 25, "compile": 25,
    "aiter": 27, "anext": 27,
}

METHODS = {
    **dict.fromkeys(
        ["upper", "lower", "strip", "lstrip", "rstrip", "split", "rsplit", "join", "replace",
         "find", "rfind", "startswith", "endswith", "format", "title", "capitalize", "casefold",
         "isdigit", "isalpha", "isalnum", "isspace", "isupper", "islower", "zfill", "center",
         "ljust", "rjust", "partition", "rpartition", "splitlines", "swapcase", "removeprefix",
         "removesuffix", "isdecimal", "isnumeric", "istitle", "expandtabs"], 2),
    **dict.fromkeys(["append", "extend", "insert", "pop", "remove", "sort", "reverse", "clear",
                     "copy"], 5),
    **dict.fromkeys(["items", "keys", "values", "get", "setdefault", "update", "popitem",
                     "fromkeys", "add", "discard", "union", "intersection", "difference",
                     "symmetric_difference", "issubset", "issuperset", "isdisjoint"], 6),
    **dict.fromkeys(["encode", "decode"], 16),
}

DECORATORS = {
    **dict.fromkeys(["cache", "lru_cache"], 11),
    **dict.fromkeys(["property", "setter", "getter", "deleter", "classmethod", "staticmethod",
                     "dataclass", "total_ordering", "abstractmethod", "unique"], 21),
    **dict.fromkeys(["contextmanager", "asynccontextmanager"], 24),
    **dict.fromkeys(["override", "overload", "runtime_checkable", "final"], 26),
}

DUNDER_DEFS = {
    **dict.fromkeys(["__init__", "__str__", "__repr__", "__eq__"], 14),
    "__next__": 22, "__enter__": 24, "__exit__": 24,
    **dict.fromkeys(["__get__", "__set__", "__delete__", "__set_name__", "__getattribute__",
                     "__init_subclass__", "__class_getitem__", "__instancecheck__",
                     "__subclasscheck__", "__subclasshook__", "__new__", "__prepare__"], 25),
    **dict.fromkeys(["__aenter__", "__aexit__", "__aiter__", "__anext__", "__await__"], 27),
}
DUNDER_ATTRS = dict.fromkeys(["__dict__", "__class__", "__bases__", "__mro__", "__module__",
                              "__slots__", "__qualname__"], 14)

TITLES = {1: "Variables & Operators", 2: "Strings", 3: "Conditionals", 4: "Loops",
          5: "Lists & Tuples", 6: "Dicts & Sets", 7: "Functions", 9: "Functions Advanced",
          10: "Comprehensions", 11: "Recursion", 12: "Exceptions", 13: "Files & Modules",
          14: "OOP Basics", 15: "Stdlib", 16: "Numbers & Bytes", 17: "Regex",
          18: "Idioms & Matching", 19: "Data Structures", 21: "OOP Advanced",
          22: "Generators", 23: "Decorators", 24: "Context Managers", 25: "Metaprogramming",
          26: "Type Hints", 27: "Concurrency", 28: "Testing", 29: "Performance",
          30: "Networking", 31: "Real-World Programs"}


def _decorator_name(node: ast.expr) -> str:
    while isinstance(node, ast.Call):
        node = node.func
    if isinstance(node, ast.Attribute):
        return node.attr
    return getattr(node, "id", "")


def features(tree: ast.AST) -> list[tuple[int, str]]:
    """(notebook that teaches it, description) for every feature in the tree."""
    found: list[tuple[int, str]] = []
    add = found.append

    for node in ast.walk(tree):
        match node:
            case ast.JoinedStr():
                add((2, "f-string"))
            case ast.Subscript():
                add((2, "indexing/slicing"))
            case ast.If() | ast.IfExp():
                add((3, "if / conditional expression"))
            case ast.Match():
                add((3, "match"))
            case ast.MatchSequence() | ast.MatchMapping() | ast.MatchClass() | ast.MatchStar():
                add((18, "structural match pattern"))
            case ast.For() | ast.While() | ast.Break() | ast.Continue():
                add((4, "loop"))
            case ast.List():
                add((5, "list"))
            case ast.Starred(ctx=ast.Store()):
                add((5, "starred unpacking"))
            case ast.Delete():
                add((5, "del"))
            case ast.Dict() | ast.Set():
                add((6, "dict/set literal"))
            case ast.Global():
                add((7, "global"))
            case ast.Try():
                add((12 if node.finalbody or node.orelse else 7, "try/except"))
            case ast.TryStar():
                add((12, "except*"))
            case ast.Raise() | ast.Assert():
                add((12, "raise/assert"))
            case ast.Lambda():
                add((9, "lambda"))
            case ast.Nonlocal():
                add((9, "nonlocal"))
            case ast.ListComp() | ast.SetComp() | ast.DictComp() | ast.GeneratorExp():
                add((10, "comprehension / generator expression"))
            case ast.With():
                add((13, "with"))
            case ast.Yield() | ast.YieldFrom():
                add((22, "yield"))
            case ast.NamedExpr():
                add((18, "walrus :="))
            case ast.AnnAssign():
                add((21, "annotation"))
            case ast.AsyncFunctionDef() | ast.Await() | ast.AsyncWith() | ast.AsyncFor():
                add((27, "async/await"))
            case ast.ClassDef():
                has_methods = any(isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef))
                                  for b in node.body)
                add((14 if has_methods else 12, "class"))
                if any(k.arg == "metaclass" for k in node.keywords):
                    add((25, "metaclass"))
                for deco in node.decorator_list:
                    name = _decorator_name(deco)
                    add((DECORATORS.get(name, 23), f"@{name}"))
            case ast.Import(names=names):
                for alias in names:
                    root = alias.name.split(".")[0]
                    add((MODULES.get(root, 99), f"import {root}"))
            case ast.ImportFrom(module=module):
                root = (module or "").split(".")[0]
                add((MODULES.get(root, 99), f"import {root}"))
            case ast.Attribute(attr=attr) if attr.startswith("__") and attr.endswith("__"):
                add((DUNDER_ATTRS.get(attr, 9), f".{attr}"))
            case ast.Attribute(attr=attr) if attr in METHODS:
                add((METHODS[attr], f".{attr}()"))
            case ast.Call(func=ast.Name(id=name)) if name in CALLS:
                add((CALLS[name], f"{name}()"))

        if isinstance(node, ast.Call) and any(k.arg == "key" for k in node.keywords):
            add((10, "key= function"))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add((7, "def"))
            args = node.args
            if args.defaults or any(d is not None for d in args.kw_defaults):
                add((7, "default argument"))
            if args.vararg or args.kwarg or args.kwonlyargs or args.posonlyargs:
                add((9, "*args / **kwargs / keyword-only / positional-only"))
            if node.returns or any(a.annotation for a in
                                   args.args + args.kwonlyargs + args.posonlyargs):
                add((21, "annotation"))
            if node.name.startswith("__") and node.name.endswith("__"):
                add((DUNDER_DEFS.get(node.name, 21), f"def {node.name}"))
            for deco in node.decorator_list:
                name = _decorator_name(deco)
                add((DECORATORS.get(name, 23), f"@{name}"))
            for sub in ast.walk(node):
                if sub is not node and isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add((9, "nested def"))
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
                        and sub.func.id == node.name):
                    add((11, "recursion"))
    return found


def too_early(source: str, notebook: int, program: str = "") -> list[str]:
    """Features in `source` a learner at `notebook` has not been taught yet.

    `program` is the whole question's code: a module the program writes itself
    (say `inventory.py`) can be imported even though it is not in MODULES."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []  # running it reports this; an Error question may want a SyntaxError
    out = set()
    for nb, what in features(tree):
        if nb == 99:
            root = what.removeprefix("import ")
            if any(mark in program for mark in (f"{root}.py", f'"{root}"', f"'{root}'")):
                continue
            out.add(f"{what} (module not in the curriculum map in tools/verify.py)")
        elif nb > notebook:
            out.add(f"{what} (taught in NB{nb:02d} {TITLES.get(nb, '')})".rstrip())
    return sorted(out)


# ----------------------------------------------------------------- parsing

@dataclass
class Question:
    qid: str
    level: int
    topic: str
    type: str
    min_version: str | None
    shown: str | None             # code in the prompt: given / to predict / buggy / to refactor
    expected: str | None
    solution: str | None
    senior: str | None
    answer_cell: str | None
    dropdowns: list[str] = field(default_factory=list)


def _fence(body: str, lang: str) -> str | None:
    for found_lang, code in FENCE_RE.findall(body):
        if found_lang == lang:
            return code
    return None


def parse_question(markdown: str, answer_cell: str | None) -> Question | None:
    first, _, rest = markdown.partition("\n")
    head = HEADER_RE.match(first.strip())
    if not head:
        return None
    before_details = rest.split("<details>", 1)[0]
    blocks = {summary.strip(): body for summary, body in DETAILS_RE.findall(rest)}
    expected_body = blocks.get("Expected output", "")
    expected = _fence(expected_body, "text")
    return Question(
        qid=f"{head['nb']}-{head['q']}", level=int(head["level"]), topic=head["topic"],
        type=head["type"], min_version=head["min"],
        shown=(m[1] if (m := SHOWN_RE.search(before_details)) else None),
        expected=expected,
        solution=_fence(blocks.get("Solution", ""), "python"),
        senior=_fence(blocks.get("Senior dev solution", ""), "python"),
        answer_cell=answer_cell,
        dropdowns=[s.strip() for s, _ in DETAILS_RE.findall(rest)],
    )


def load(path: Path) -> tuple[list[dict], list[Question]]:
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    questions = []
    for i, cell in enumerate(cells):
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell["source"])
        nxt = cells[i + 1] if i + 1 < len(cells) else None
        answer = "".join(nxt["source"]) if nxt and nxt["cell_type"] == "code" else None
        q = parse_question(source, answer)
        if q:
            questions.append(q)
    return cells, questions


# ----------------------------------------------------------------- checking

def _version_ok(q: Question) -> bool:
    if not q.min_version:
        return True
    major, minor = map(int, q.min_version.split("."))
    return sys.version_info >= (major, minor)


def _ends_with_bare_expression(source: str) -> bool:
    """Jupyter displays a cell's last expression, a script does not. Solutions
    must print, so they behave the same in both."""
    try:
        body = ast.parse(source).body
    except SyntaxError:
        return False
    return bool(body) and isinstance(body[-1], ast.Expr) and not isinstance(body[-1].value, (ast.Call, ast.Await, ast.Constant))


FORBIDDEN = [
    (re.compile(r"\binput\s*\("), "input() - use given values instead"),
    (re.compile(r"\basyncio\.run\s*\("), "asyncio.run() fails inside Jupyter - use top-level await"),
    (re.compile(r"\b(multiprocessing|ProcessPoolExecutor)\b"), "multiprocessing does not work reliably from a notebook"),
]


def check_question(q: Question, notebook: int, quick: bool) -> list[str]:
    errs: list[str] = []
    e = errs.append

    if list(q.dropdowns) != list(DROPDOWNS):
        e(f"dropdowns are {q.dropdowns}, expected {list(DROPDOWNS)}")
        return errs
    if q.expected is None or not q.expected.strip():
        e("Expected output is missing or empty")
        return errs
    if q.answer_cell is None:
        e("no code cell after the question")

    needs_shown = q.type in ("Predict", "Error", "Fix", "Refactor")
    if needs_shown and not q.shown:
        e(f"a {q.type} question needs a python code block in the prompt")
        return errs
    if q.type in ("Write", "Fix", "Refactor") and not q.solution:
        e("Solution has no python code block")
        return errs
    if q.type in ("Write", "Fix", "Refactor") and not q.senior:
        e("Senior dev solution has no python code block")
        return errs

    # what the learner's cell starts with
    if q.answer_cell is not None:
        cell = q.answer_cell.strip()
        if q.type == "Write" and q.shown and not cell.startswith(q.shown.strip()):
            e("answer cell does not start with the given code")
        if q.type in ("Fix", "Refactor") and cell != q.shown.strip():
            e("answer cell should hold an exact copy of the code to fix/refactor")
        if q.type in ("Predict", "Error") and not cell.startswith("#"):
            e("answer cell for a Predict/Error question should be a comment prompt")

    # prerequisite gate: solution + every piece of code the learner must read
    gated = {"Solution": q.solution, "shown code": q.shown}
    for label, src in gated.items():
        if src:
            program = "\n".join(filter(None, [q.shown, q.solution]))
            for problem in too_early(src, notebook, program):
                e(f"{label} uses {problem}")
    for label, src in {"Solution": q.solution, "Senior": q.senior, "shown code": q.shown}.items():
        for pattern, why in FORBIDDEN:
            if src and pattern.search(src):
                e(f"{label} uses {why}")
    for label, src in {"Solution": q.solution, "Senior": q.senior}.items():
        if src and q.type in ("Write", "Fix", "Refactor") and _ends_with_bare_expression(src):
            e(f"{label} ends with a bare expression - print() it so a script shows it too")

    if not _version_ok(q):
        return errs  # structure checked; cannot run on this Python

    given = q.shown if (q.type == "Write" and q.shown) else ""
    join = lambda code: f"{given}\n{code}" if given else code  # noqa: E731

    def expect(label: str, program: str, *, must_raise: bool = False) -> Run:
        result = run(program, seed=0)
        if result.timed_out:
            e(f"{label} timed out after {TIMEOUT}s")
            return result
        if result.error and not must_raise:
            e(f"{label} raised {result.error}: {result.stderr.strip().splitlines()[-1:] }")
        if must_raise and not result.error:
            e(f"{label} was supposed to raise an error but did not")
        if result.shown != q.expected.rstrip("\n"):
            e(f"{label} output does not match Expected output\n"
              f"      expected: {q.expected.rstrip()!r}\n      got:      {result.shown!r}")
        if not quick:
            again = run(program, seed=1)
            if again.shown != result.shown:
                e(f"{label} output changes between runs (set order? randomness? time?)")
        return result

    if q.type == "Write":
        expect("Solution", join(q.solution))
        expect("Senior solution", join(q.senior))
    elif q.type == "Fix":
        expect("Solution", q.solution)
        expect("Senior solution", q.senior)
        buggy = run(q.shown)
        if not buggy.timed_out and not buggy.error and buggy.shown == q.expected.rstrip("\n"):
            e("the buggy code already prints the Expected output - there is no visible bug")
    elif q.type == "Refactor":
        expect("Code to refactor", q.shown)
        expect("Solution", q.solution)
        expect("Senior solution", q.senior)
    elif q.type == "Predict":
        expect("Code to predict", q.shown)
    elif q.type == "Error":
        expect("Code to predict", q.shown, must_raise=True)
    if q.type in ("Predict", "Error") and q.senior:
        result = run(q.senior)
        if result.error or result.timed_out:
            e(f"Senior code does not run cleanly ({result.error or 'timeout'})")
    return errs


def check_notebook(path: Path, quick: bool, jobs: int) -> tuple[int, list[str]]:
    problems: list[str] = []
    p = problems.append
    name = FILE_RE.match(path.name)
    if not name:
        return 0, [f"file name should look like NB01-Topic-Names.ipynb, got {path.name}"]
    nb_id = name[1]
    number = int(nb_id[2:])

    raw = json.loads(path.read_text(encoding="utf-8"))
    cells, questions = load(path)
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "code" and (cell.get("outputs") or cell.get("execution_count")):
            p(f"cell {i}: code cell has saved output - clear it before committing")
    if raw.get("metadata", {}).get("kernelspec", {}).get("name") != "python3":
        p("kernelspec must be the portable 'python3'")
    first = "".join(cells[0]["source"]) if cells else ""
    if not first.startswith(f"# {nb_id} · "):
        p(f"first cell should be the title '# {nb_id} · ...'")
    if not any("## Prerequisites" in "".join(c["source"]) for c in cells if c["cell_type"] == "markdown"):
        p("no '## Prerequisites' section")

    ordinary = [q for q in questions if not q.qid.endswith("-P")]
    projects = [q for q in questions if q.qid.endswith("-P")]
    if len(projects) != 1 or questions[-1:] != projects:
        p("needs exactly one mini-project, as the last question")
    for i, q in enumerate(ordinary, 1):
        if q.qid != f"{nb_id}-Q{i:02d}":
            p(f"question {i} is labelled {q.qid}, expected {nb_id}-Q{i:02d}")
            break
    levels = [q.level for q in ordinary]
    if levels != sorted(levels):
        p("questions must run from L1 up to L5 without going back down")
    if nb_id not in CAPSTONES and sorted(set(levels)) != [1, 2, 3, 4, 5]:
        p(f"every level L1-L5 should appear, found {sorted(set(levels))}")

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda q: (q, check_question(q, number, quick)), questions))
    for q, errs in results:
        for err in errs:
            p(f"{q.qid}: {err}")
    return len(questions), problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--quick", action="store_true", help="run each program once, not twice")
    parser.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 4)
    args = parser.parse_args()

    paths = args.paths or sorted(p for tier in TIERS for p in (ROOT / tier).glob("NB*.ipynb"))
    if not paths:
        print("no notebooks found")
        return 1
    total_q = total_bad = 0
    for path in paths:
        count, problems = check_notebook(path, args.quick, args.jobs)
        total_q += count
        label = path.relative_to(ROOT) if path.is_absolute() and path.is_relative_to(ROOT) else path
        if problems:
            total_bad += 1
            print(f"FAIL  {label}  ({count} questions, {len(problems)} problems)")
            for problem in problems:
                print(f"      - {problem}")
        else:
            print(f"ok    {label}  ({count} questions)")
    print(f"\n{len(paths) - total_bad}/{len(paths)} notebooks clean, {total_q} questions checked")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
