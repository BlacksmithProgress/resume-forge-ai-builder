"""Startup wiring — logging, dirs, native bridge probe, feature registration."""

from __future__ import annotations

import logging
import logging.handlers
from dataclasses import dataclass
from pathlib import Path

from resume_forge.features import load_builtin_features
from resume_forge.native import probe_native_bridges
from resume_forge.registry import FeatureRegistry


@dataclass(slots=True)
class Bootstrap:
    log_dir: Path
    level: int = logging.INFO

    def run(self) -> FeatureRegistry:
        self._setup_dirs()
        self._setup_logging()
        registry = FeatureRegistry()
        load_builtin_features(registry)
        probe_native_bridges(registry)
        logging.getLogger("resume_forge").info(
            "bootstrap complete: %d features", len(registry.features)
        )
        return registry

    def _setup_dirs(self) -> None:
        for d in (self.log_dir, Path("cache"), Path("exports"), Path("workspace")):
            d.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self) -> None:
        handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "forge.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s")
        )
        root = logging.getLogger()
        root.setLevel(self.level)
        root.addHandler(handler)
        root.addHandler(logging.StreamHandler())