"""Resources: a safe output file and a stopwatch that takes a clock."""
import json
import logging
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Iterator

from pipeline_models import Enriched

log = logging.getLogger("orderflow.resources")


class FakeClock:
    """Moves forward by a fixed step on every call, so timings are repeatable."""

    def __init__(self, step: float = 0.5) -> None:
        self.now = 0.0
        self.step = step

    def __call__(self) -> float:
        self.now += self.step
        return self.now


class JsonlSink:
    """Writes one JSON object per line; a failed run leaves no half-written file."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.count = 0

    def __enter__(self) -> "JsonlSink":
        self._file = open(self.path, "w", encoding="utf-8")
        log.info("opened %s", self.path.name)
        return self

    def write(self, item: Enriched) -> None:
        self._file.write(json.dumps(asdict(item), sort_keys=True) + "\n")
        self.count += 1

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._file.close()
        if exc_type is None:
            log.info("closed %s with %d records", self.path.name, self.count)
        else:
            self.path.unlink()
            log.error("rolled back %s after %s", self.path.name, exc_type.__name__)
        return False


@contextmanager
def stopwatch(label: str, clock: Callable[[], float]) -> Iterator[None]:
    started = clock()
    try:
        yield
    finally:
        log.info("%s took %.2fs", label, clock() - started)


def read_jsonl(path: Path) -> Iterator[dict]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)
