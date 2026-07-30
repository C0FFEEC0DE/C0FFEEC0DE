# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A résumé site authored from markdown, auto-built by a one-shot Python script,
served for **three audiences** (ADR-0013): humans (bilingual landing page +
branded PDF), machines (JSON Resume, llms.txt, AGENTS.md, cv.json, resume.txt),
and ATS (a neutral single-column PDF). Deployed to GitHub Pages via Actions.
Decisions are recorded as ADRs in `docs/adr/` (0001→0023) — read the relevant
one before changing a settled area.

## Commands

Run all shell commands from the repo root (`/var/home/chaos_weaver/code/C0FFEEC0DE`).
The shell cwd can persist across calls; if a command fails with "No such file",
`cd` back to the repo root first.

```bash
python3 build/build.py            # build into dist/
python3 build/build.py --check    # build + validate, non-zero exit on failure (CI uses this)
python3 -m pytest build/test_build.py -q                       # build/pytest tests (the `dist` fixture sets PDF=1)
python3 -m pytest build/test_build.py::test_resume_json_valid -q   # single test
cd tests/ui && npx playwright test          # UI tests — MUST run from tests/ui (see gotcha)
cd tests/ui && npx playwright test -g "curl one-liner"   # single UI test by name
cd tests/ui && npm run test:full             # build + UI tests in one
python3 -m compileall -q build src           # lint (syntax check all Python)
python3 -m http.server -d dist                # local preview at http://localhost:8000
```

Environment variables (all optional): `DOMAIN=krasnobai.dev` (emits
`dist/CNAME` + absolute URLs in llms.txt/sitemap), `PAGES_URL=https://user.github.io/C0FFEEC0DE`
(fallback absolute base when DOMAIN unset), `PDF=0` (skip PDF if WeasyPrint
system libs are missing).

## Architecture

**One markdown source → one build → many outputs.** `resume/resume.en.md` and
`resume/resume.ru.md` are the single source of truth (ADR-0001). Each has YAML
front-matter (`basics`, `profiles`, `availability`, `meta`) + body H2 sections
(`Summary`, `Experience`, `Skills`, `Projects`, `Education`, `Certificates`,
`Languages`, `Contact`). `build/build.py` parses them with `parse_resume` and
renders every output. `--check` validates required fields and that all linked
files exist in `dist/`.

**Three renderers, parsed once, shared deliberately** (changing one without the
others causes divergence bugs):
- `render_header_fragment` — name/label/summary; injected into the landing hero
  (`{{HEADER_EN}}` / `{{HEADER_RU}}` in `src/index.html`).
- `render_body_fragment` — the résumé sections (Contact → Experience → Skills →
  Projects → Education → Certificates → Languages). Used by **both** the landing
  `#resume` block (`{{RESUME_EN_HTML}}`) **and** the branded-PDF body (via
  `render_html_fragment`). Keep these two in lockstep (ADR-0013).
- `render_ats_html` — the ATS `resume.pdf`. Uses **neutral** colors and a
  standard font on purpose (ADR-0014) — do NOT "align" it to the Forest theme.

`src/index.html` is a template with `{{...}}` placeholders the build fills;
`build.py` resolves paths from its own `__file__`, so it always writes
`<repo>/dist/` regardless of cwd.

**Theming (ADR-0017):** a single **Forest** theme, light + dark via `data-theme`
on `:root`. `src/site.css` declares `--c-*` tokens and maps them once to
Bootstrap 5.3 component vars at `:root`. `src/i18n.js` sets `data-theme` on load
(from localStorage or `prefers-color-scheme`) and the ◐ toggle flips it. The
no-JS fallback is a scoped `@media (prefers-color-scheme: dark)` rule that
applies only before JS sets `data-theme`. `src/print.css` is the branded-PDF
stylesheet (Forest palette, self-hosted JetBrains Mono resolved against
WeasyPrint's `base_url` = repo root).

**Dragon (ADR-0009):** fully client-side — `src/dragon.js` + `dragon-parts.js`
seed a mulberry32 PRNG from `?d=` and draw a 16×16 pixel dragon to `<canvas>`;
`src/share.js` adds share-link + lazy-loaded, SRI-locked QR. No backend, no
tracking. The delight path must keep working with JS off (it degrades to an
empty canvas, not an error).

**Regression guards (ADR-0019):** a pure-Python build test computes the WCAG AA
contrast ratio for both modes — text/muted/accent against both `--c-bg` and
`--c-surface`, plus button-text-on-accent — and fails below 4.5:1. Playwright
no-JS tests block script resources to verify the Forest-light default and the
no-JS dark path render without JavaScript. Theme/font/print changes that drift
these are caught.

## Invariants and gotchas

- **Playwright must run from `tests/ui/`, not the repo root.** `npx playwright`
  from root installs the wrong `playwright` package and fails. The config's
  `webServer` serves `dist/` on :8000, so build `dist/` first (or use
  `npm run test:full`).
- **`## Summary` body section overwrites the front-matter `basics.summary`**
  (build.py `parse_resume` line ~103). The body one is what renders in the hero
  `.lead`. Keep them in sync, and keep the summary short — ADR-0008 (low
  cognitive load) is first-class: the hero holds identity + the two audience
  CTAs + the dragon only; the curl one-liner lives in the footer (ADR-0020).
  One accent, one CTA cluster, generous space. Don't dump metrics/credentials
  into the summary — they belong in Experience/Certificates.
- **ATS `resume.pdf` is intentionally NOT Forest** (ADR-0014); the branded PDF
  IS Forest. Don't "fix" the mismatch.
- **Contact profiles must stay exactly `[GitHub, LinkedIn, Telegram]`** in that
  order, with the Telegram URL a `https://t.me/...` link (ADR-0016, enforced by
  `test_contact_profiles_required_set`).
- **Tests pin specific résumé data** (name, company, label, fluency, etc.). When
  you change résumé content, update the assertions in `build/test_build.py` and
  `tests/ui/ui.spec.js` — or make them data-agnostic (e.g. `t.me/` substring)
  so they survive content edits.
- **All generated/injected content is HTML-escaped** (ADR-0012). The
  `resume_md_attacked` fixture feeds hostile markdown (script tags, etc.) to
  confirm escaping holds — don't introduce raw injection.
- The résumé currently holds **real data with literal `TODO` placeholders** for
  fields the owner's public LinkedIn hides (email, phone, Telegram, the Grid
  Dynamics start date/title, prior roles, education degree/dates). TODOs render
  literally; the site is **not live-ready** until they are filled. There is no
  build guard yet against deploying with visible TODOs.

## Workflow note

Release/deploy automation is intentionally disabled in this profile. Follow
discover → design → implement → verify → review → docs → cleanup; deploy only
when explicitly asked.