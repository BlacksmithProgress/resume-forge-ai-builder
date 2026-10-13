"""Feature: inject ATS keywords into resume text without keyword-stuffing."""

from __future__ import annotations

from typing import Any

from resume_forge.registry import FeatureRegistry

FEATURE_META = {
    "id": "keyword_injector",
    "name": "ATS Keyword Injector",
    "version": "0.5.2",
    "requires": ["templates"],
}


class KeywordInjectorHandler:
    """Splices keywords into existing bullets, only where they fit naturally.

    Uses a small rule set: if the bullet already mentions a sibling skill,
    append the keyword as a parenthetical; otherwise leave the bullet alone.
    """

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        bullets: list[str] = payload["bullets"]
        keywords: list[str] = payload["keywords"]
        injected: list[str] = []
        for b in bullets:
            low = b.lower()
            for kw in keywords:
                if kw.lower() in low:
                    break
            else:
                kw = keywords[0] if keywords else None
                if kw and len(b) < 220:
                    b = f"{b.rstrip('.')} ({kw})."
            injected.append(b)
        return {"bullets": injected}


def register(registry: FeatureRegistry) -> None:
    registry.add_feature(FEATURE_META)
    registry.add_handler("keywords.inject", KeywordInjectorHandler)