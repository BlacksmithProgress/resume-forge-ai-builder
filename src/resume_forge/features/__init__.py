"""Built-in feature modules — each self-registers via FEATURE_META + register()."""

from __future__ import annotations

from importlib import import_module

from resume_forge.registry import FeatureRegistry

BUILTIN_MODULES = [
    "resume_forge.features.tailor_bullets",
    "resume_forge.features.keyword_injector",
    "resume_forge.features.cover_letter",
    "resume_forge.features.summary_rewriter",
]


def load_builtin_features(registry: FeatureRegistry) -> None:
    for path in BUILTIN_MODULES:
        mod = import_module(path)
        mod.register(registry)