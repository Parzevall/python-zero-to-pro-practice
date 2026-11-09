"""Checks used by builder.py when it builds a notebook.

* run(): runs a program the way a notebook cell would, in a fresh process with
  its own temporary folder, and reports what it printed and any exception.
* too_early(): lists features a solution uses that the course hasn't taught
  yet at that notebook (imports, built-ins, methods, syntax).

Standard library only.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass

TIMEOUT = 30

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


