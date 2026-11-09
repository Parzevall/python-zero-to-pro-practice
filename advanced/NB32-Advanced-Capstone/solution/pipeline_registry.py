"""A tiny plugin system: steps register themselves with a decorator."""
import importlib
import logging
from typing import Callable, Iterable, Iterator

from pipeline_models import Enriched

log = logging.getLogger("orderflow.registry")

Step = Callable[[Enriched], Enriched | None]
_STEPS: dict[str, tuple[int, Step]] = {}


def step(name: str, *, order: int) -> Callable[[Step], Step]:
    """Register a function as a pipeline step; lower order runs first."""
    def register(func: Step) -> Step:
        if name in _STEPS:
            raise ValueError(f"step {name!r} is already registered")
        _STEPS[name] = (order, func)
        return func
    return register


def registered() -> list[str]:
    return [name for name, _ in sorted(_STEPS.items(), key=lambda kv: kv[1][0])]


def load_plugins(*module_names: str) -> None:
    for module_name in module_names:
        importlib.import_module(module_name)
        log.info("loaded plugin %s", module_name)


def run_steps(items: Iterable[Enriched], names: list[str] | None = None,
              dropped: list[Enriched] | None = None) -> Iterator[Enriched]:
    """Stream items through the chosen steps; a step returning None drops the item."""
    chosen = names if names is not None else registered()
    unknown = [n for n in chosen if n not in _STEPS]
    if unknown:
        raise KeyError(f"unknown steps: {unknown}")
    for item in items:
        current: Enriched | None = item
        for name in chosen:
            current = _STEPS[name][1](current)
            if current is None:
                log.info("step %s dropped order %s", name, item.order.id)
                if dropped is not None:
                    dropped.append(item)
                break
        else:
            yield item
