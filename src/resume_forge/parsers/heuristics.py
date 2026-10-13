"""Section splitter — regex + heading heuristics for messy resumes."""

from __future__ import annotations

import re

HEADING_PATTERNS: dict[str, re.Pattern[str]] = {
    "summary": re.compile(r"^\s*(summary|profile|objective|about)\b", re.I | re.M),
    "experience": re.compile(r"^\s*(experience|employment|work history)\b", re.I | re.M),
    "education": re.compile(r"^\s*(education|academic)\b", re.I | re.M),
    "skills": re.compile(r"^\s*(skills|technical skills|competencies)\b", re.I | re.M),
    "projects": re.compile(r"^\s*(projects|selected work)\b", re.I | re.M),
    "certifications": re.compile(r"^\s*(certifications?|licenses?)\b", re.I | re.M),
}


def split_sections(text: str) -> dict[str, str]:
    """Return a dict of section-name → raw text. Header is everything before
    the first recognized heading."""
    hits: list[tuple[int, str]] = []
    for name, pat in HEADING_PATTERNS.items():
        for m in pat.finditer(text):
            hits.append((m.start(), name))
    hits.sort()
    if not hits:
        return {"header": text.strip()}

    out: dict[str, str] = {"header": text[: hits[0][0]].strip()}
    for i, (pos, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(text)
        out[name] = text[pos:end].strip()
    return out