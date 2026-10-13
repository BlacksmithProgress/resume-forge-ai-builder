"""ForgeService — end-to-end pipeline: parse → tailor → score → assemble."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

from resume_forge.config.loader import Settings
from resume_forge.models.job import JobDescription
from resume_forge.models.resume import Resume
from resume_forge.parsers.docx_parser import parse_docx
from resume_forge.parsers.pdf_parser import parse_pdf
from resume_forge.services.ats_service import ATSService
from resume_forge.services.llm_adapter import LLMAdapter

log = logging.getLogger(__name__)


@dataclass(slots=True)
class ForgeResult:
    slug: str
    resume: Resume
    job: JobDescription
    ats_score: float


class ForgeService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.llm = LLMAdapter(settings.llm, allow_network=settings.allow_network)
        self.ats = ATSService(settings)

    def run(self, master: Path, job: Path, profile: str) -> ForgeResult:
        resume = self._parse(master)
        jd = JobDescription(raw_text=job.read_text(encoding="utf-8"))
        log.info("forging profile=%s master=%s job=%s", profile, master.name, job.name)

        resume.summary = self.llm.rewrite_summary(
            current=resume.summary or "", job_description=jd.raw_text
        )
        for entry in resume.experience:
            entry.bullets = [
                self.llm.rewrite_bullet(b, jd.raw_text, tone=profile) for b in entry.bullets
            ]

        report = self.ats.score_resume(resume, jd)
        slug = _slugify(resume.contact.full_name)
        return ForgeResult(slug=slug, resume=resume, job=jd, ats_score=report.score)

    def _parse(self, path: Path) -> Resume:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return parse_pdf(path)
        if suffix in {".docx", ".doc"}:
            return parse_docx(path)
        raise ValueError(f"unsupported master format: {suffix}")


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "resume"