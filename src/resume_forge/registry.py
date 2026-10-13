"""Feature registry — every feature module registers handlers here."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol


class Handler(Protocol):
    """A feature handler is anything callable with a typed payload."""

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(slots=True)
class Feature:
    id: str
    name: str
    version: str
    requires: tuple[str, ...] = ()
    handlers: dict[str, Handler] = field(default_factory=dict)


class FeatureRegistry:
    def __init__(self) -> None:
        self.features: dict[str, Feature] = {}
        self._handlers: dict[str, Handler] = {}

    def add_feature(self, meta: dict[str, Any]) -> Feature:
        feat = Feature(
            id=meta["id"],
            name=meta["name"],
            version=meta["version"],
            requires=tuple(meta.get("requires", ())),
        )
        self.features[feat.id] = feat
        return feat

    def add_handler(self, key: str, handler: Handler) -> None:
        if key in self._handlers:
            raise KeyError(f"handler already registered: {key}")
        self._handlers[key] = handler

    def resolve(self, key: str) -> Handler:
        try:
            return self._handlers[key]
        except KeyError as exc:
            raise LookupError(f"no handler for {key!r}") from exc

    def missing_deps(self) -> list[tuple[str, str]]:
        have = set(self.features)
        return [
            (f.id, dep)
            for f in self.features.values()
            for dep in f.requires
            if dep not in have and dep not in {"llm.local", "llm.remote", "templates"}
        ]