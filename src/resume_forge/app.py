"""Entry point — Typer CLI + Windows-friendly bootstrap.

Runtime: Python 3.11+, Windows 10/11 primary, Linux/macOS best-effort.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import typer
from rich.console import Console

from resume_forge.bootstrap import Bootstrap
from resume_forge.config.loader import load_settings
from resume_forge.services.export_service import ExportService
from resume_forge.services.forge_service import ForgeService

app = typer.Typer(
    name="resume-forge",
    help="Forge tailored resumes from a master CV using local or remote LLMs.",
    no_args_is_help=True,
)
console = Console()
log = logging.getLogger("resume_forge")


@app.command()
def forge(
    master: Path = typer.Option(..., "--master", "-m", exists=True, dir_okay=False),
    job: Path = typer.Option(..., "--job", "-j", exists=True, dir_okay=False),
    out: Path = typer.Option(Path("exports"), "--out", "-o"),
    profile: str = typer.Option("balanced", "--profile", "-p"),
    allow_network: bool = typer.Option(False, "--allow-network"),
) -> None:
    """Tailor a master resume against a job description and export."""
    settings = load_settings(allow_network=allow_network)
    forge_svc = ForgeService(settings)
    result = forge_svc.run(master=master, job=job, profile=profile)
    ExportService(settings).write(result, out)
    console.print(f"[green]forged[/green] → {out / result.slug}.docx")


@app.command()
def score(
    resume: Path = typer.Option(..., "--resume", "-r", exists=True, dir_okay=False),
    job: Path = typer.Option(..., "--job", "-j", exists=True, dir_okay=False),
) -> None:
    """Score a resume against a job description (ATS-style)."""
    from resume_forge.services.ats_service import ATSService

    settings = load_settings(allow_network=False)
    report = ATSService(settings).score(resume=resume, job=job)
    console.print_json(report.model_dump_json(indent=2))


def main() -> None:
    Bootstrap(log_dir=Path("logs")).run()
    try:
        app()
    except KeyboardInterrupt:
        console.print("[yellow]interrupted[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()