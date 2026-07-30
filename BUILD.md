# BUILD — how the C0FFEEC0DE résumé site works

This is the technical documentation for the `C0FFEEC0DE` repo (the one that builds
the résumé site at **<https://krasnobai.dev>**). The repo's `README.md` is a short
profile storefront; this file is the contributor-facing detail: source format,
build, outputs, deploy, and the reasoning (ADRs).

## Overview

A résumé repository that is:

- **Authored in markdown** — edit `resume/resume.en.md` / `resume/resume.ru.md`, CI rebuilds everything.
- **Bilingual (EN/RU)** with a one-click toggle.
- **Machine-readable** for robots: JSON Resume `resume.json`, an `llms.txt` index, an `AGENTS.md`, and a flat `resume.txt`.
- **Human-readable** for people: a warm, low-cognitive-load landing page on GitHub Pages with a single **Forest** theme (light/dark) and a handcrafted feel.
- **Downloadable via a curl one-liner** and a printable PDF.
- **Carries a tiny pixel-art dragon** generated per visitor and shareable by link + QR — a small "thank you for stopping by" with a viral loop.

The repo holds **real owner data** (Aleksandr Krasnobai) sourced from LinkedIn plus the local project repos, with **`TODO` placeholders** for the fields LinkedIn hides from public view (phone, the Grid Dynamics start date and exact title, prior roles, education degree/dates). Fill the `TODO`s in `resume/resume.en.md` and `resume/resume.ru.md` before going live — the structure stays identical.

## Repository layout

```
resume/
  resume.en.md          # human source — English (structured markdown format)
  resume.ru.md          # human source — Russian (same structure)
src/
  index.html            # landing page template (Bootstrap 5.3 shell + placeholders)
  site.css              # single Forest theme, light/dark (ADR-0017) + human feel (ADR-0018) on Bootstrap
  jetbrains-mono-*.woff2# self-hosted JetBrains Mono (headings) — no CDN fetch
  print.css             # self-contained Forest print styles for the branded PDF
  i18n.js               # EN/RU toggle + light/dark + greeting + curl line
  dragon-parts.js       # pixel-art palettes + option lists
  dragon.js             # seeded PRNG → composes a dragon → draws <canvas>
  share.js              # seed/URL + share link + lazy-loaded QR
build/
  build.py              # one-shot builder; `--check` validates
  test_build.py         # pytest suite (incl. automated WCAG contrast guard — ADR-0019)
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
dates: 2012 — 2016 · location: Munich
- course

## Certificates
- **Name** — issuer (2024)

## Languages
- **English** (C1)
```

Section titles are recognized: `Summary`, `Experience`, `Projects`, `Education`, `Skills`, `Certificates`, `Languages`, `Contact`. Unknown sections are ignored. Dates use ` — ` (em dash) between start and end; `present` ends an open-ended role.

## Build

```bash
pip install pyyaml markdown weasyprint   # weasyprint only needed for the PDF
python build/build.py            # builds into dist/
python build/build.py --check    # build + validate, non-zero exit on failure
python -m pytest build/test_build.py -q
python -m http.server -d dist     # local preview at http://localhost:8000
```

Environment variables (all optional):
- `DOMAIN` — e.g. `krasnobai.dev`; emits `dist/CNAME` and absolute URLs in `llms.txt`.
- `PAGES_URL` — fallback absolute base when `DOMAIN` is unset (e.g. `https://user.github.io/C0FFEEC0DE`).
- `PDF=0` — skip PDF generation (useful if WeasyPrint system libs are missing).

## What gets generated

The build produces **three audiences** from one markdown source (see `docs/adr/0013-three-audiences.md`):

| File | Audience | Purpose |
|---|---|---|
| `index.html` | humans | bilingual landing page with the dragon |
| `resume-branded.pdf` | humans | designed, scannable PDF |
| `resume.pdf` | **ATS** | ATS-optimized: single column, standard font/headings, dates on the title line, real selectable text (the **default download**) |
| `resume.json` / `resume.ru.json` | machines | JSON Resume v1.0.0 (EN/RU) + optional `availability` hiring signals |
| `resume.min.json` | LLMs | token-cheap metadata tier (~100 tokens) for agent screening |
| `.well-known/cv.json` | LLMs | discovery manifest ([cv.json](https://cvjson.com) convention) |
| `resume.txt` | curl / machines | flat plain text, both languages |
| `resume.md` | humans / machines | clean markdown mirror |
| `llms.txt` | LLMs | curated index ([llmstxt.org](https://llmstxt.org)) |
| `AGENTS.md` | AI agents | what this site is + where data lives |
| `robots.txt`, `sitemap.xml` | crawlers | standard (sitemap only when a base URL is known) |
| `CNAME` | GitHub Pages | only when `DOMAIN` is set |

## Curl one-liner

```bash
curl -sL https://krasnobai.dev/resume.txt          # plain text to stdout
curl -sL https://krasnobai.dev/resume.json          # JSON Resume
curl -sL https://krasnobai.dev/resume.pdf -o r.pdf  # PDF
```

Before the custom domain is bound, the same paths work on the default Pages URL, e.g. `https://<user>.github.io/C0FFEEC0DE/resume.txt`.

## The dragon

Each visitor gets a deterministic pixel-art dragon seeded from the URL (`?d=…`). The same link always shows the same dragon, so sharing the link shares *your* dragon. A "Share" button copies the link; "Show QR" renders a scannable code (the QR lib loads lazily, SRI-locked, so the page stays light and the delight never breaks). The dragon is generated entirely client-side — no backend, no tracking.

## Themes & feel

The site uses a **single Forest theme** (ADR-0017) with a light and a dark variant — a calm green palette (paper-neutral greens, one green accent, soft 16px rounding, warm low shadow). The ◐ toggle in the top bar flips light/dark and persists in `localStorage`. The theme is pure CSS custom properties (`--c-*` mapped once to Bootstrap's component vars) — no JS color math — and its colors are chosen for WCAG AA in both modes (machine-enforced by the build — ADR-0019). To change the theme, edit the `:root` (light) and `:root[data-theme="dark"]` blocks in `src/site.css`.

The whole site is tuned for a **human, handcrafted feel** (ADR-0018): self-hosted **JetBrains Mono** display headings (a coder's font for a coder's résumé — nothing fetched from a CDN, offline-safe), warm paper neutrals, soft 16px rounding, an italic "margin-note" greeting, and the dragon as the personality anchor. Structure stays low-cognitive-load (one accent, one CTA, generous space); the personality lives in typography and warmth, not extra components.

Theme contrast and the no-JS fallback are **regression-guarded** (ADR-0019): a pure-Python test computes the WCAG ratio for the theme in both modes (text, muted, accent, button-on-accent, against both the page bg and the block surface) and fails the build below 4.5:1, and Playwright tests block scripts to verify the Forest-light default and the no-JS dark path render correctly without JavaScript.

## Deploying (GitHub Pages)

The workflow (`.github/workflows/deploy.yml`) builds and deploys on every push to `main`. Once:
1. In the repo, **Settings → Pages → Build and deployment → Source = GitHub Actions**.
2. Push to `main`; the first run publishes at `https://<user>.github.io/C0FFEEC0DE/`.

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

MIT — the demo content and code are yours to adapt. The QR dependency is loaded from CDN under its own license.