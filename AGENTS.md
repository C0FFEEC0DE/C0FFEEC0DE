# AGENTS.md

Guidance for AI agents working **in this repository** (the deployed site has its
own generated `dist/AGENTS.md` for visitors). Keep this file short and accurate.

## What this is
A résumé site built from markdown. Humans edit `resume/*.md`; `build/build.py`
regenerates everything (HTML, JSON Resume, plain text, a single human-readable/
ATS-safe PDF, `resume-for-agents.md`, `agents.json`, `llms.txt`, `AGENTS.md`,
sitemap). Deployed to GitHub Pages by `.github/workflows/deploy.yml`.

## Build & test
```bash
pip install pyyaml weasyprint pypdf jsonschema pytest
python build/build.py --clean --check  # build + validate all release artifacts
python -m pytest build/test_build.py -q
python scripts/validate_consistency.py
npm test --prefix tests/ui
python -m http.server -d dist           # local preview
```
`DOMAIN` env emits `dist/CNAME` + absolute URLs; `PDF=0` skips the PDF.

## Where things live
- `resume/resume.{en,ru}.md` — canonical owner-provided résumé content. Keep EN/RU structurally aligned.
- `build/build.py` — the parser + renderers. Read the ADRs before changing the format.
- `build/jsonresume-schema-v1.0.0.json` — vendored official schema used by `--check`.
- `src/` — the landing page template + CSS + client JS (dragon, i18n, share).
- `docs/adr/` — architecture decisions; respect them, supersede don't silently reverse.
- `dist/` — generated, gitignored. Never hand-edit.

## Conventions to keep
- Markdown format contract is in `resume/resume.en.md` (front-matter + fixed `##` sections).
- Unknown facts are omitted, never guessed or represented by placeholders. Preserve evidence-first wording (ADR-0033).
- The browser path is self-hosted: no required runtime CDN, remote font, backend, or tracker (ADR-0037).
- JSON Resume EN/RU must pass the vendored v1.0.0 schema; the PDF must stay selectable, ATS-safe, and at most four pages.
- All generated/injected content is escaped — see `docs/adr/0012-security-escaping.md`.
- The fixed light Forest palette must meet WCAG AA (4.5:1); the build checks this automatically.

## Don't
- Don't commit `dist/`, secrets, tokens, or inferred personal facts.
- Don't add a Jekyll config — Pages deploys from the artifact, not a branch.
- Don't enable release/deploy automation beyond the Pages workflow in this profile.
- Don't deploy unless the user explicitly asks. After an authorized deploy, run `python scripts/verify_deployed.py https://krasnobai.dev`.
