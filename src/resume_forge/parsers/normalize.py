"""Contact normalization — email/phone/link extraction from raw header text."""

from __future__ import annotations

import re

from resume_forge.models.resume import ContactBlock

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
URL_RE = re.compile(r"https?://\S+|(?:www\.|linkedin\.com/|github\.com/)\S+", re.I)


def normalize_contact(header: str) -> ContactBlock:
    lines = [ln.strip() for ln in header.splitlines() if ln.strip()]
    name = lines[0] if lines else "Unknown Candidate"
    email = (EMAIL_RE.search(header) or [None])[0] if EMAIL_RE.search(header) else None
    phone_match = PHONE_RE.search(header)
    links = URL_RE.findall(header)
    location = _guess_location(header)
    return ContactBlock(
        full_name=name,
        email=email,
        phone=phone_match.group(0) if phone_match else None,
        location=location,
        links=links,
    )


def _guess_location(header: str) -> str | None:
    m = re.search(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)?),\s*([A-Z]{2})\b", header)
    return m.group(0) if m else None