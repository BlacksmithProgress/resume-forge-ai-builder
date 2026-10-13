"""Settings loader — layered YAML + env overrides, pydantic-validated."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

CONFIG_ROOT = Path(__file__).resolve().parents[3] / "config"


class LLMSettings(BaseModel):
    provider: str = "local"
    model_path: Path | None = None
    context_tokens: int = Field(default=8192, ge=1024, le=131072)
    temperature: float = Field(default=0.4, ge=0.0, le=2.0)
    max_output_tokens: int = Field(default=2048, ge=128, le=16384)


class ExportSettings(BaseModel):
    default_format: str = "docx"
    page_size: str = "letter"
    font_family: str = "Calibri"
    font_size_pt: float = 10.5
    ats_safe_mode: bool = True


class Settings(BaseModel):
    llm: LLMSettings = LLMSettings()
    export: ExportSettings = ExportSettings()
    allow_network: bool = False
    workspace: Path = Path("workspace")
    prompt_pack: str = "default"


def load_settings(allow_network: bool = False, config_dir: Path | None = None) -> Settings:
    root = config_dir or CONFIG_ROOT
    base_path = root / "settings.yaml"
    raw: dict = {}
    if base_path.exists():
        raw = yaml.safe_load(base_path.read_text(encoding="utf-8")) or {}

    env_provider = os.environ.get("RESUME_FORGE_LLM_PROVIDER")
    if env_provider:
        raw.setdefault("llm", {})["provider"] = env_provider

    settings = Settings.model_validate(raw)
    settings.allow_network = allow_network or bool(os.environ.get("RESUME_FORGE_ALLOW_NET"))
    return settings