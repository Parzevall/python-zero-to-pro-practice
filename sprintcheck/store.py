"""Persists which questions have been solved, so progress survives restarts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

PROGRESS_FILE = Path(__file__).resolve().parent.parent / ".sprintcheck_progress.json"


def _load() -> dict[str, dict]:
    if not PROGRESS_FILE.exists():
        return {}
    try:
        return json.loads(PROGRESS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict[str, dict]) -> None:
    try:
        PROGRESS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True))
    except OSError:
        pass  # progress is a convenience; never let it break a check()


def record(qid: str, passed: bool) -> None:
    data = _load()
    entry = data.setdefault(qid, {"attempts": 0, "solved": False})
    entry["attempts"] += 1
    entry["solved"] = entry["solved"] or passed
    entry["last"] = datetime.now().isoformat(timespec="seconds")
    _save(data)


def clear(qid: str | None = None) -> None:
    if qid is None:
        _save({})
        return
    data = _load()
    data.pop(qid, None)
    _save(data)


def render() -> str:
    from content import all_notebooks

    data = _load()
    lines = ["", "  Notebook                                    solved   attempted", "  " + "-" * 62]
    total_solved = total_q = 0
    for nb in all_notebooks():
        qids = [q.qid for q in nb.questions]
        solved = sum(1 for q in qids if data.get(q, {}).get("solved"))
        attempted = sum(1 for q in qids if q in data)
        total_solved += solved
        total_q += len(qids)
        bar = "#" * round(20 * solved / len(qids)) if qids else ""
        lines.append(f"  {nb.number:02d} {nb.title[:36]:<36} {solved:>3}/{len(qids):<3} {attempted:>5}  {bar}")
    lines.append("  " + "-" * 62)
    pct = (100 * total_solved / total_q) if total_q else 0
    lines.append(f"  {'TOTAL':<39} {total_solved:>3}/{total_q:<3}        {pct:.0f}%")
    return "\n".join(lines)
