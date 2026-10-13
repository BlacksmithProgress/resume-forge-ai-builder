# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | ✅        |
| 0.5.x   | ⚠️ security-only |
| < 0.5   | ❌        |

## Reporting a vulnerability

Do **not** open a public issue. Email `security@resume-forge-ai.invalid`
with:

- A description of the issue.
- A minimal repro (resume file, config, command).
- Impact assessment (data leak, RCE, prompt injection, template sandbox
  escape).

We aim to acknowledge within 72 hours and patch within 14 days for
high-severity issues.

## Threat model

resume-forge-ai-builder processes untrusted resume files (PDF, DOCX, TXT,
HTML) and untrusted user prompts. In scope:

- **Template sandbox escape** — Jinja templates are rendered in a
  `SandboxedEnvironment`; escaping it is a vulnerability.
- **Prompt injection via resume content** — a resume that hijacks the
  LLM to leak the user's other documents or call out to the network.
- **Native bridge memory safety** — the C++ PDF rasterizer must not
  crash on malformed input; ASAN builds are run in CI.
- **Local model cache poisoning** — GGUF/ONNX files under
  `models/` are hash-verified on load.

Out of scope:

- Model hallucination in generated bullet points (that's a quality
  issue, not a security one — open a normal issue).
- Denial of service via a 500MB resume (rate-limit yourself).

## Hardening defaults

- Network egress is **off** unless `--allow-network` is passed.
- The LLM adapter runs local-first; remote providers require an explicit
  API key in `config/providers.yaml`.
- All exports are written under `exports/` with `..` rejected in
  filenames.