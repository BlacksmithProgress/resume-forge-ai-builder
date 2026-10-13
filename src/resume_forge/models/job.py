"""Job description model + keyword extraction shape."""

from __future__ import annotations

from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    title: str | None = None
    company: str | None = None
    raw_text: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    keywords: dict[str, int] = Field(default_factory=dict)
    seniority: str | None = None


class ATSReport(BaseModel):
    score: float = Field(ge=0.0, le=100.0)
    matched_keywords: list[str]
    missing_keywords: list[str]
    density_warnings: list[str]
    formatting_flags: list[str]
    recommendations: list[str]