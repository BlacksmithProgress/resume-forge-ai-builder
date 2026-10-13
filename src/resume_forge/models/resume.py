"""Resume document model — the canonical in-memory shape."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class ContactBlock(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    links: list[str] = Field(default_factory=list)


class ExperienceEntry(BaseModel):
    company: str
    title: str
    start: date | None = None
    end: date | None = None
    location: str | None = None
    bullets: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)


class EducationEntry(BaseModel):
    institution: str
    degree: str
    field: str | None = None
    start: date | None = None
    end: date | None = None
    details: list[str] = Field(default_factory=list)


class SkillGroup(BaseModel):
    category: str
    items: list[str]


class Resume(BaseModel):
    contact: ContactBlock
    summary: str | None = None
    experience: list[ExperienceEntry] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    skills: list[SkillGroup] = Field(default_factory=list)
    projects: list[dict[str, str]] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    source_format: Literal["pdf", "docx", "txt", "html", "md"] = "docx"