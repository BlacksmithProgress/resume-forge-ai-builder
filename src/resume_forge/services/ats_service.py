"""ATSService — score a resume against a job description."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from resume_forge.config.loader import Settings
from resume_forge.models.job import ATSReport, JobDescription
from resume_forge.models.resume import Resume
from resume_forge.parsers.docx_parser import parse_docx
from resume_forge.parsers.pdf_parser import parse_pdf

STOPWORDS = frozenset(
    """a an the and or but if then than of to in on for with without at by
    from into over under this that these those you your we our they their
    is are was were be been being have has had do does did will would can
    could should may might must as it its""".split()
)


class ATSService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def score(self, resume: Path, job: Path) -> ATSReport