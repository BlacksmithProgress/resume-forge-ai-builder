"""Feature: rewrite the professional summary for a target role."""

from __future__ import annotations

from typing import Any

from resume_forge.registry import FeatureRegistry
from resume_forge.services.llm_adapter import LLMAdapter

FEATURE_META = {
    "id": "summary_rewriter",
    "name": "Summary Rewriter",
    "version": "0.5.0",
    "requires": ["llm.local"],
}


class SummaryRewriterHandler:
    def __init__(self, llm: LLMAdapter) -> None:
        self.llm = llm

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "summary": self.llm.rewrite_summary(
                current=payload.get("summary", ""),
                job_description=payload["job_description"],
                max_words=payload.get("max_words", 80),
            )
        }


def register(registry: FeatureRegistry) -> None:
    registry.add_feature(FEATURE_META)
    registry.add_handler("summary.rewrite", SummaryRewriterHandler)