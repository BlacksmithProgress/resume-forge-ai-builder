"""DOCX parser — python-docx for the happy path, C# interop for legacy .doc."""

from __future__ import annotations

from pathlib import Path

from docx import Document

from resume_forge.models.resume import Resume
from resume_forge.parsers.heuristics import split_sections
from resume_forge.parsers.normalize import normalize_contact


def parse_docx(path: Path) -> Resume:
    doc = Document(str(path))
    lines = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(lines)
    sections = split_sections(text)
    return Resume(
        contact=normalize_contact(sections.get("header", "")),
        summary=sections.get("summary"),
        source_format="docx",
    )