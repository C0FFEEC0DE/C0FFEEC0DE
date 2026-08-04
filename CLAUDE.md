# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A résumé site authored from markdown, auto-built by a one-shot Python script,
served for **two surfaces** (ADR-0031): humans get a bilingual landing page plus
a single human-readable/ATS-safe PDF; LLM/AI agents get structured and narrative
artifacts (JSON Resume, llms.txt, AGENTS.md, cv.json, resume-for-agents.md,
agents.json, resume.txt). Deployed to GitHub Pages via Actions. Decisions are
recorded as ADRs in `docs/adr/` (0001→0037) — read the relevant one before
changing a settled area.

## Commands

Run all shell commands from the repo root (`/var/home/chaos_weaver/code/C0FFEEC0DE`).
The shell cwd can persist across calls; if a command fails with "No such file",
`cd` back to the repo root first.

```bash
python3 build/build.py            # build into dist/
python3 build/build.py --check    # build + validate, non-zero exit on failure (CI uses this)
python3 -m pytest build/test_build.py -q                       # build/pytest tests (the `dist` fixture sets PDF=1)
python3 -m pytest build/test_build.py::test_resume_json_valid -q   # single test
python3 scripts/validate_consistency.py                            # cross-output content check
cd tests/ui && npx playwright test          # UI tests — MUST run from tests/ui (see gotcha)
cd tests/ui && npx playwright test -g "footer machine formats"   # single UI test by name
cd tests/ui && npm run test:full             # build + UI tests in one
python3 -m compileall -q build scripts       # lint (syntax check all Python)
python3 -m http.server -d dist                # local preview at http://localhost:8000
python3 scripts/verify_deployed.py https://krasnobai.dev  # post-deploy smoke + freshness check
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

**Renderers, parsed once, shared deliberately** (changing one without the
others causes divergence bugs):
- `render_header_fragment` — name/label/summary; injected into the landing hero
  (`{{HEADER_EN}}` / `{{HEADER_RU}}` in `src/index.html`).
- `render_contact_fragment` — the compact Contact block injected into `#resume`.
- `render_resume_html(r, lang)` — the single human-readable/ATS-safe PDF body
  (Contact → Summary → Experience → Skills → Projects → Education → Certificates
  → Languages). It combines Forest palette/visual hierarchy with ATS-safe
  structure (single column, real text, standard fonts, dates on the role line,
  no tables/floats) (ADR-0031).
- `render_markdown(r)` / `render_text(r)` — clean markdown and plain-text
  mirrors derived from the same parsed data.
- `build_resume_for_agents(r, base)` / `build_agents_json(r, base)` — dedicated
  LLM/AI-agent outputs.

`src/index.html` is a template with `{{...}}` placeholders the build fills;
`build.py` resolves paths from its own `__file__`, so it always writes
`<repo>/dist/` regardless of cwd.

**Theming (ADR-0017 v5):** a fixed **Forest** light theme. `src/site.css`
declares `--c-*` tokens and a small local button/layout system. There is no
Bootstrap/CDN dependency, theme toggle, `data-theme` attribute, or dark
variant. `src/print.css` is a legacy reference stylesheet; the single PDF uses
inline CSS so it is self-contained.

**Dragon (ADR-0009, ADR-0026, ADR-0027, ADR-0028):** fully client-side —
`src/dragon.js` + `dragon-parts.js` seed a mulberry32 PRNG from `?d=` and draw a
16×16 pixel dragon to `<canvas>`. ADR-0026 hides the dragon behind a footer
click easter egg, so the default landing page is a pure business card.
`src/share.js` adds a shareable link (ADR-0021), a LinkedIn share button
(ADR-0022), and a "Save my dragon" button that downloads a token PNG with the
dragon + an English "have a nice day" caption (ADR-0027). Open Graph tags
(ADR-0028/0034) give LinkedIn the owner's name, role, impact figures, and a
1200×630 static card for the share preview. No backend, no tracking. The delight path must keep
working with JS off (it degrades to an empty canvas, not an error).

**Regression guards (ADR-0019):** a pure-Python build test computes the WCAG AA
contrast ratio for the light theme — text/muted/accent against both `--c-bg` and
`--c-surface`, plus button-text-on-accent — and fails below 4.5:1. Playwright
no-JS tests block script resources to verify the fixed Forest-light default
renders without JavaScript. Theme/font changes that drift these are caught.

## Invariants and gotchas

- **Playwright must run from `tests/ui/`, not the repo root.** `npx playwright`
  from root installs the wrong `playwright` package and fails. The config's
  `webServer` serves `dist/` on :8000, so build `dist/` first (or use
  `npm run test:full`).
- **`## Summary` body section overwrites the front-matter `basics.summary`**
  (build.py `parse_resume` line ~103). The body one is what renders in the hero
  `.lead`. Keep them in sync, and keep the summary short — ADR-0008 (low
  cognitive load) is first-class: the page front-loads identity, one concise
  scale signal in the summary, contacts, and the two audience CTAs. Detailed
  evidence stays in the PDF and machine outputs. The dragon is a hidden footer
  easter egg (ADR-0026), and the
  verbose curl one-liner was removed from the footer in ADR-0020 v3 (the file
  `resume.txt` is still served, so the ADR-0006 command still works, but it is
  no longer displayed on the page).
  One accent, one CTA cluster, generous space. Don't dump metrics/credentials
  into the summary — they belong in Experience/Certificates.
- **The single PDF is both human-readable and ATS-safe** (ADR-0031). It uses the
  Forest palette *and* ATS-safe structure; don't strip the styling or add
  multi-column/float/table layouts.
- **The source `basics.profiles` must stay `[GitHub, LinkedIn, Telegram]`**
  in that order (ADR-0024 v3, which supersedes ADR-0016). The landing page's
  visible Contact row is narrower: it shows LinkedIn + Telegram + email, while
  GitHub appears in the footer machine-links list. All three profiles still
  render in `resume.json`, `resume.ru.json`, `resume.txt`, `resume.md`,
  `resume-for-agents.md`, `llms.txt`, and JSON-LD `sameAs`. `t.me/` links are
  fine in those machine-readable outputs; only the landing-page Contact subset
  is intentional.
- **Tests pin specific résumé data** (name, company, label, fluency, etc.). When
  you change résumé content, update the assertions in `build/test_build.py` and
  `tests/ui/ui.spec.js` — or make them data-agnostic so they survive content
  edits.
- **All generated/injected content is HTML-escaped** (ADR-0012). The
  `resume_md_attacked` fixture feeds hostile markdown (script tags, etc.) to
  confirm escaping holds — don't introduce raw injection.
- **Keep `build/build.py`'s module docstring in sync with `check()`**: the
  docstring `Output:` list and the `DOMAIN` example must name every file
  `check()` asserts (incl. `resume.min.json`, `.well-known/cv.json`,
  `resume-for-agents.md`, `agents.json`,
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf`) and use the real site
  domain (`krasnobai.dev`), or the docstring silently rots against the build it
  documents.
- The résumé content is canonical as of ADR-0029 and evidence-governed by
  ADR-0033: `resume/resume.en.md` and
  `resume/resume.ru.md` hold the single source of truth for all outputs. The
  landing page uses a short one-line `basics.summary`; the full professional
  intro lives in `meta.intro` and renders into `resume.txt`, `resume.md`,
  `llms.txt`, `resume-for-agents.md`, and the single PDF. The single PDF opens
  with Work Experience after a brief Summary section (ADR-0031).
- **Machine outputs are normalized and schema-checked** (ADR-0035). Dates use
  ISO `YYYY-MM`, markdown decoration must not leak into structured fields,
  unknown certificate metadata is omitted, and JSON-LD must describe a Person/
  ProfilePage without inventing a vacancy.
- **Agent-facing files inherit the same evidence policy.** `resume.json` is the
  canonical factual source; `resume-for-agents.md`, `llms.txt`, `AGENTS.md`,
  `agents.json`, and `.well-known/cv.json` are generated mirrors. Never hand-edit
  `dist/` or add inferred facts to make an agent payload look more complete.

## Workflow note

Deploy is out of scope by default in this profile. Follow
discover → design → implement → verify → review → docs → cleanup; run a deploy
only when the user explicitly asks.
