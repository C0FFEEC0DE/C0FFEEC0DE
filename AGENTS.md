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
pip install pyyaml weasyprint pytest
python build/build.py --check          # build + validate
python -m pytest build/test_build.py -q
python -m http.server -d dist           # local preview
```
`DOMAIN` env emits `dist/CNAME` + absolute URLs; `PDF=0` skips the PDF.

## Where things live
- `resume/resume.{en,ru}.md` — the only content you should edit. Fictional demo data.
- `build/build.py` — the parser + renderers. Read the ADRs before changing the format.
- `src/` — the landing page template + CSS + client JS (dragon, i18n, share).
- `docs/adr/` — architecture decisions; respect them, supersede don't silently reverse.
- `dist/` — generated, gitignored. Never hand-edit.

## Conventions to keep
- Markdown format contract is in `resume/resume.en.md` (front-matter + fixed `##` sections).
- The dragon must stay offline (no CDN); Bootstrap CSS is the only CDN dependency (SRI-locked).
- All generated/injected content is escaped — see `docs/adr/0012-security-escaping.md`.
- The fixed light Forest palette must meet WCAG AA (4.5:1); the build checks this automatically.

## Don't
- Don't commit `dist/`, secrets, or real personal data yet (content is demo).
- Don't add a Jekyll config — Pages deploys from the artifact, not a branch.
- Don't enable release/deploy automation beyond the Pages workflow in this profile.