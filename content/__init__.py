"""Discovers the nbNN_*.py content modules and exposes their Notebook objects."""

from __future__ import annotations

import importlib
import pkgutil

from content.schema import Notebook


def all_notebooks() -> list[Notebook]:
    """Every Notebook defined under content/, ordered by notebook number."""
    found: list[Notebook] = []
    for info in pkgutil.iter_modules(__path__):
        if not info.name.startswith("nb"):
            continue
        module = importlib.import_module(f"content.{info.name}")
        notebook = getattr(module, "NOTEBOOK", None)
        if notebook is not None:
            found.append(notebook)
    return sorted(found, key=lambda nb: nb.number)


def all_questions():
    return [q for nb in all_notebooks() for q in nb.questions]
