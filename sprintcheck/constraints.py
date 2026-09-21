"""AST checks for questions that constrain *how* the answer is written.

Used by `custom` questions - "solve this without a loop", "make this
recursive", "rewrite it as a comprehension". The functional cases still run;
these constraints are an additional gate on top of them.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Callable

LOOP_NODES = (ast.For, ast.AsyncFor, ast.While)
COMP_NODES = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def _tree(func: Callable) -> ast.AST:
    source = textwrap.dedent(inspect.getsource(func))
    return ast.parse(source)


def _has(tree: ast.AST, node_types) -> bool:
    return any(isinstance(node, node_types) for node in ast.walk(tree))


def _calls_name(tree: ast.AST, name: str) -> bool:
    """True if `name` is called, bare (`sum(...)`) or dotted (`math.sum(...)`).

    The dotted form matters: forbidding `lru_cache` is pointless if
    `functools.lru_cache(...)` slips through, and a learner reaching for the
    dotted spelling is doing exactly what the question forbids.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == name:
            return True
        if isinstance(func, ast.Attribute) and func.attr == name:
            return True
    return False


def _body_line_count(tree: ast.AST) -> int:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lines = {
                child.lineno
                for child in ast.walk(node)
                if hasattr(child, "lineno") and child.lineno > node.body[0].lineno - 1
            }
            return len(lines)
    return 0


def check_constraints(func: Callable, rules: list[str]) -> list[str]:
    """Return a list of violation messages. Empty list means all rules hold."""
    try:
        tree = _tree(func)
    except (OSError, TypeError):
        return ["could not read source for this function (define it in a notebook cell)"]

    violations: list[str] = []
    func_name = getattr(func, "__name__", "")

    for rule in rules:
        name, _, arg = rule.partition(":")
        if name == "no-loops" and _has(tree, LOOP_NODES):
            violations.append("uses a for/while statement - solve it without one")
        elif name == "needs-comprehension" and not _has(tree, COMP_NODES):
            violations.append("no comprehension found - the answer should use one")
        elif name == "no-recursion" and _calls_name(tree, func_name):
            violations.append(f"{func_name} calls itself - solve it iteratively, without recursion")
        elif name == "needs-recursion" and not _calls_name(tree, func_name):
            violations.append(f"{func_name} never calls itself - make it recursive")
        elif name == "needs-generator" and not _has(tree, (ast.Yield, ast.YieldFrom)):
            violations.append("no yield found - this should be a generator")
        elif name == "needs-with" and not _has(tree, (ast.With, ast.AsyncWith)):
            violations.append("no with-statement found - use a context manager")
        elif name == "no-builtin" and _calls_name(tree, arg):
            violations.append(f"calls {arg}() - this question asks you to do it manually")
        elif name == "max-lines":
            count = _body_line_count(tree)
            if count > int(arg):
                violations.append(f"body is {count} lines - keep it to {arg} or fewer")
    return violations
