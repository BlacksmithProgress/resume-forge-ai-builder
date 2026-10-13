"""Feature: generate a tailored cover letter from resume + JD."""

from __future__ import annotations

from typing import Any

from resume_forge.registry import FeatureRegistry
from resume_forge.services.llm_adapter import LLMAdapter

FEATURE_META = {
    "id": "cover_letter",
    "name": "Cover Letter Composer",
    "version": "0.4.1",
    "requires": ["llm.local", "templates"],
}


class CoverLetterHandler:
    def __init__(self, llm: LLMAdapter) -> None:
        self.llm = llm

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "cover_letter": self.llm.compose_cover_letter(
                resume_summary=payload["summary"],
                job_description=payload["job_description"],
                tone=payload.get("tone", "professional"),
            )
        }


def register(registry: FeatureRegistry) -> None:
    registry.add_feature(FEATURE_META)
    registry.add_handler("cover_letter.generate", CoverLetterHandler)