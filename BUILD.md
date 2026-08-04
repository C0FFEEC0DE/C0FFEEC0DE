# BUILD — how the C0FFEEC0DE résumé site works

This is the technical documentation for the `C0FFEEC0DE` repo (the one that builds
the résumé site at **<https://krasnobai.dev>**). The repo's `README.md` is a short
profile storefront; this file is the contributor-facing detail: source format,
build, outputs, deploy, and the reasoning (ADRs).

## Overview

A résumé repository that is:

- **Authored in markdown** — edit `resume/resume.en.md` / `resume/resume.ru.md`, CI rebuilds everything.
- **Bilingual (EN/RU)** with a one-click toggle.
- **Machine-readable** for robots: JSON Resume `resume.json`, an `llms.txt` index, an `AGENTS.md`, `.well-known/cv.json`, `resume-for-agents.md`, `agents.json`, and a flat `resume.txt`.
- **Human-readable** for people: a warm, low-cognitive-load landing page on GitHub Pages with a fixed **Forest** light theme and a handcrafted feel.
- **Downloadable via a curl one-liner** and a single human-readable, ATS-safe PDF.
- **Carries a tiny pixel-art dragon** generated per visitor and shareable by link — a small "thank you for stopping by".

The repo holds the owner's canonical résumé data. Unknown facts are omitted
rather than represented by placeholders; do not infer dates, credential IDs,
legal status, or measurement definitions.

## Repository layout

```
resume/
  resume.en.md          # human source — English (structured markdown format)
  resume.ru.md          # human source — Russian (same structure)
src/
  index.html            # dependency-light landing page template + placeholders
  site.css              # self-hosted Forest theme + local button/layout styles
  og-card.svg/.png      # exact 1200×630 social-share source and raster card
  i18n.js               # EN/RU toggle + greeting
  dragon-parts.js       # pixel-art palettes + option lists
  dragon.js             # seeded PRNG → composes a dragon → draws <canvas>
  share.js              # seed/URL + share link + save-dragon token PNG
  print.css             # legacy self-contained Forest print styles (kept for reference; the single PDF uses inline CSS)
build/
  build.py              # one-shot builder; `--check` validates
  jsonresume-schema-v1.0.0.json # vendored official JSON Resume schema
  test_build.py         # pytest suite (incl. automated WCAG contrast guard — ADR-0019)
scripts/
  validate_consistency.py # canonical content ↔ generated-output guard
  verify_deployed.py      # public endpoint, asset, PDF, and freshness smoke test
tests/ui/               # Playwright UI tests (served from dist/, incl. no-JS path tests — ADR-0019)
.github/workflows/deploy.yml     # build → deploy to GitHub Pages
.github/workflows/playwright.yml # build → run UI tests on push/PR
dist/                   # generated (gitignored)
```

## The markdown source format

Each `resume/<lang>.md` has a YAML front-matter (maps to JSON Resume `basics`, `profiles`, `meta`) and a body of fixed `##` sections:

```markdown
---
basics:
  name: "Your Name"
  label: "Your Title"
  email: "you@example.com"
  url: "https://yoursite"
  location: {city: "City", region: "ST", countryCode: "XX"}
profiles:
  - {network: "GitHub",   username: "you", url: "https://github.com/you"}
  - {network: "LinkedIn", username: "you", url: "https://www.linkedin.com/in/you"}
  - {network: "Telegram", username: "you", url: "https://t.me/you"}
meta: {canonical: "https://yoursite/resume.json", version: "0.1.0", lastModified: "2026-07-30"}
---

## Summary
One short paragraph.

## Experience
### Senior Engineer — Acme
dates: 2022-03 — present · location: Berlin · url: https://acme.example
- highlight bullet
- highlight bullet

## Skills
- **Languages**: Python, Go, Rust
- **Infra**: Kubernetes, Terraform

## Projects
### project-name
dates: 2024-01 — present · url: https://example
- highlight

## Education
### B.Sc. — University
dates: 2012-09 — 2016-06 · location: Munich
- course

## Certificates
- **Name** — issuer (2024)

## Languages
- **English** (C1)
```

Section titles are recognized: `Summary`, `Experience`, `Projects`, `Education`, `Skills`, `Certificates`, `Languages`, `Contact`. Unknown sections are ignored. Dates use ISO `YYYY-MM`, separated by ` — ` (em dash); `present` ends an open-ended role. Optional facts such as certificate dates, issuers, URLs, and credential IDs are omitted when unknown.

## Build

```bash
pip install pyyaml weasyprint pypdf jsonschema pytest
python build/build.py            # builds into dist/
python build/build.py --check    # build + validate, non-zero exit on failure
python -m pytest build/test_build.py -q
python scripts/validate_consistency.py
npm test --prefix tests/ui
python -m http.server -d dist     # local preview at http://localhost:8000
```

Environment variables (all optional):
- `DOMAIN` — e.g. `krasnobai.dev`; emits `dist/CNAME` and absolute URLs in `llms.txt`.
- `PAGES_URL` — fallback absolute base when `DOMAIN` is unset (e.g. `https://user.github.io/C0FFEEC0DE`).
- `PDF=0` — skip PDF generation (useful if WeasyPrint system libs are missing).

## What gets generated

The build produces **two surfaces** from one markdown source (see `docs/adr/0031-llm-ai-agent-optimized-build.md`):

| File | Audience | Purpose |
|---|---|---|
| `index.html` | humans | bilingual landing page with the dragon |
| `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` | humans + **ATS** | one human-readable, ATS-safe PDF: single column, system font, dates on the title line, real selectable text (the **default download**) |
| `resume.json` / `resume.ru.json` | machines | JSON Resume v1.0.0 (EN/RU) + optional `availability` hiring signals |
| `resume.min.json` | LLMs / agents | token-cheap metadata tier (~100 tokens) for screening |
| `.well-known/cv.json` | LLMs / agents | discovery manifest ([cv.json](https://cvjson.com) convention) |
| `resume-for-agents.md` | LLMs / agents | narrative, keyword-rich résumé optimized for summarisation |
| `agents.json` | LLMs / agents | OpenAI-style structured-output function spec |
| `resume.txt` | curl / machines | flat plain text, both languages |
| `resume.md` | humans / machines | clean markdown mirror |
| `llms.txt` | LLMs / agents | curated index ([llmstxt.org](https://llmstxt.org)) |
| `AGENTS.md` | AI agents | what this site is + source-of-truth hierarchy |
| `robots.txt`, `sitemap.xml` | crawlers | standard (sitemap only when a base URL is known) |
| `CNAME` | GitHub Pages | only when `DOMAIN` is set |

## Curl one-liner

```bash
curl -sL https://krasnobai.dev/resume.txt                             # plain text to stdout
curl -sL https://krasnobai.dev/resume.json                            # JSON Resume
curl -sL https://krasnobai.dev/resume-for-agents.md                  # LLM/AI-agent résumé
curl -sL https://krasnobai.dev/Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf -o r.pdf  # single PDF
```

Before the custom domain is bound, the same paths work on the default Pages URL, e.g. `https://<user>.github.io/C0FFEEC0DE/resume.txt`.

## The dragon

Each visitor gets a deterministic pixel-art dragon seeded from the URL (`?d=…`). The same link always shows the same dragon, so sharing the link shares *your* dragon. A "Share" button reveals the shareable link and a LinkedIn share button; "Save my dragon" downloads a token PNG. The dragon is generated entirely client-side — no backend, no tracking.

## Themes & feel

The site uses a **fixed light Forest theme** (ADR-0017 v5) — a calm green palette (paper-neutral greens, one green accent, soft 16px rounding, warm low shadow). The theme and small button system are entirely self-hosted CSS, with no framework or runtime CDN. Colors are chosen for WCAG AA and machine-enforced by the build (ADR-0019). To change the palette, edit the `:root` block in `src/site.css`.

The whole site is tuned for a **human, handcrafted feel** (ADR-0018): system sans-serif everywhere, warm paper neutrals, soft rounding, three concise impact signals, and the dragon as a hidden personality anchor. The PDF remains the primary CTA; GitHub is a secondary evidence link.

Theme contrast is **regression-guarded** (ADR-0019): a pure-Python test computes the WCAG ratio for the light theme (text, muted, accent, button-on-accent, against both the page bg and the block surface) and fails the build below 4.5:1. Playwright tests also block scripts to verify the fixed Forest-light default renders correctly without JavaScript.

## Deploying (GitHub Pages)

The workflow (`.github/workflows/deploy.yml`) builds and deploys on every push to `main`. Once:
1. In the repo, **Settings → Pages → Build and deployment → Source = GitHub Actions**.
2. Push to `main`; the first run publishes at `https://<user>.github.io/C0FFEEC0DE/`.

After GitHub Pages reports a successful deployment, the workflow runs
`scripts/verify_deployed.py` against the deployed URL. The smoke test retries
during CDN propagation, verifies the landing page and public machine endpoints,
checks the PDF/PNG signatures, and compares the live résumé version and
`lastModified` value with the committed markdown source. Run the same check
manually with `python scripts/verify_deployed.py https://krasnobai.dev`.

### Custom domain

This site uses the apex domain **`krasnobai.dev`** — a personal-name domain, not a project subdomain (see ADR-0023 for the rationale).

1. Add DNS **A** records at your registrar for the `krasnobai.dev` apex pointing to GitHub Pages: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. (Add a `www` **CNAME** → `C0FFEEC0DE.github.io.` too if you want `www.krasnobai.dev`.)
2. Set the repository **variable** `DOMAIN = krasnobai.dev` (Settings → Secrets and variables → Actions → Variables, or `gh variable set DOMAIN --body krasnobai.dev`). The build then emits `dist/CNAME`.
3. In **Settings → Pages → Custom domain**, enter `krasnobai.dev` and enable **Enforce HTTPS** (`.dev` is HSTS-preloaded, so HTTPS is required; GitHub issues the certificate automatically — give it a few minutes after DNS propagates).

## Decisions

Architectural choices (source-of-truth format, JSON Resume, GitHub Pages deploy,
the dragon, security posture, etc.) are recorded as ADRs in [`docs/adr/`](docs/adr/README.md).
Repo-level guidance for AI agents working here is in [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md).

## License

MIT — the code is yours to adapt. Personal résumé content remains the owner's data.
