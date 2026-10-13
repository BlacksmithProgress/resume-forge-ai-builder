"""PDF parser — pdfplumber first, C++ rasterizer fallback for scanned PDFs."""

from __future__ import annotations

import logging
from pathlib import Path

import pdfplumber

from resume_forge.models.resume import Resume
from resume_forge.parsers.heuristics import split_sections
from resume_forge.parsers.normalize import normalize_contact

log = logging.getLogger(__name__)


def parse_pdf(path: Path) -> Resume:
    """Extract text, split into sections, build a Resume.

    Falls back to the native rasterizer + OCR path when the text layer is
    under 200 chars (scanned resumes).
    """
    text_parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    text = "\n".join(text_parts).strip()

    if len(text) < 200:
        log.info("pdf text layer thin (%d chars), trying native OCR", len(text))
        from resume_forge.native.cpp_bridge import rasterize_and_ocr

        text = rasterize_and_ocr(path)

    sections = split_sections(text)
    contact = normalize_contact(sections.get("header", ""))
    return Resume(
        contact=contact,
        summary=sections.get("summary"),
        source_format="pdf",
    )