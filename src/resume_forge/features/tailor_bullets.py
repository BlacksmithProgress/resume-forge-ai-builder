"""Feature: rewrite experience bullets to match a target job description."""

from __future__ import annotations

from typing import Any

from resume_forge.registry import FeatureRegistry
from resume_forge.services.llm_adapter import LLMAdapter

FEATURE_META = {
    "id": "tailor_bullets",
    "name": "Experience Bullet Tailor",
    "version": "0.6.0",
    "requires": ["llm.local", "templates"],
}


class TailorBulletsHandler:
    def __init__(self, llm: LLMAdapter) -> None:
        self.llm = llm

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        bullets: list[str] = payload["bullets"]
        jd: str = payload["job_description"]
        rewritten = [
            self.llm.rewrite_bullet(b, jd, tone=payload.get("tone", "impactful"))
            for b in bullets
        ]
        return {"bullets": rewritten}


def register(registry: FeatureRegistry) -> None:
    registry.add_feature(FEATURE_META)
    registry.add_handler("bullets.tailor", TailorBulletsHandler)