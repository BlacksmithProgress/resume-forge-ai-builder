# Contributing to resume-forge-ai-builder

Thanks for wanting to forge. This repo is a modular AI resume/CV generator
for Windows desktop. It ships a Python core, with optional native
accelerators in C++, C#, and Java for the heavier parsing and PDF
rasterization paths.

## Quick start (dev)

```powershell
git clone https://github.com/<you>/resume-forge-ai-builder.git
cd resume-forge-ai-builder
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m resume_forge.app
```

## Repo layout

```
src/resume_forge/          # Python package (core, handlers, services)
config/                    # YAML profiles, prompt packs, templates
native/cpp/                # PDF rasterizer + text extractor
native/csharp/             # Word/Outlook .docx interop
native/java/               # ATS keyword scorer (Lucene-backed)
tests/                     # pytest suite
docs/                      # architecture + prompt engineering notes
```

## How to add a feature module

Feature modules live under `src/resume_forge/features/`. Each module:

1. Exposes a `register(registry)` function.
2. Declares a `FEATURE_META` dict with `id`, `name`, `version`, `requires`.
3. Ships its own tests under `tests/features/`.

Example skeleton:

```python
FEATURE_META = {
    "id": "cover_letter_tone",
    "name": "Cover Letter Tone Shifter",
    "version": "0.4.1",
    "requires": ["llm.local", "templates"],
}

def register(registry):
    registry.add_handler("cover_letter.tone", ToneHandler)
```

## Style

- `ruff` + `black` + `mypy --strict` on `src/`.
- Native code: `clang-format` (C++), `dotnet format` (C#), `google-java-format` (Java).
- Commit messages: `feat(parser): ...`, `fix(pdf): ...`, `docs(prompts): ...`.

## Prompt packs

Any new prompt template must be added to `config/prompts/` as YAML, with a
matching golden test in `tests/prompts/`. Do not hardcode prompts in Python.

## Pull requests

- One feature per PR.
- Include a fixture resume under `tests/fixtures/resumes/`.
- If you touch the native bridges, run `python tools/build_native.py --all`.

## Code of conduct

Be a decent human. Roast code, not people.