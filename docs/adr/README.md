# Architecture Decision Records

Decisions shaping the C0FFEEC0DE résumé site, in Michael Nygard's ADR format
(Context · Decision · Consequences). New decisions append a number; a
superseded record is marked **Superseded by ADR-00xx** and a new one is added.
Records are numbered 0001→0037.

| # | Title | Status |
|---|---|---|
| 0001 | Markdown is the single source of truth | Accepted |
| 0002 | JSON Resume v1.0.0 as the machine-readable format | Accepted |
| 0003 | AI-agent surface: llms.txt + AGENTS.md + JSON-LD | Accepted |
| 0004 | Deploy via GitHub Pages + Actions (artifact) | Accepted |
| 0005 | Custom domain is deferred and env-driven | Accepted |
| 0006 | curl one-liner over explicit plain-text paths | Accepted |
| 0007 | Bilingual EN/RU via paired markdown + client toggle | Accepted |
| 0008 | Low-cognitive-load design as a first-class constraint | Accepted |
| 0009 | Procedural pixel-art dragon, seeded from the URL | Accepted |
| 0010 | QR via lazy-loaded, SRI-locked CDN dependency | Superseded by ADR-0028 |
| 0011 | Pure-Python build with minimal dependencies | Accepted |
| 0012 | Security: escape all generated/injected content | Accepted |
| 0013 | Three explicit resume audiences: human, LLM-agent, ATS | Accepted (amended by ADR-0031) |
| 0014 | `resume.pdf` is the ATS-optimized render | Accepted (amended by ADR-0031) |
| 0015 | AI-agent discoverability: cv.json well-known + metadata tier | Accepted |
| 0016 | Contact profiles: GitHub, LinkedIn, Telegram | Superseded by ADR-0024 |
| 0017 | Single Forest theme | Accepted (v5) |
| 0018 | Human, handcrafted feel | Accepted |
| 0019 | Automated contrast + no-JS regression guards | Accepted |
| 0020 | UI block layout (best-practices pass) | Accepted (v4) |
| 0021 | Dragon share link revealed inline | Accepted |
| 0022 | LinkedIn share button (pre-filled link) | Accepted |
| 0023 | Custom domain set to krasnobai.dev | Accepted |
| 0024 | Contact profiles: GitHub, LinkedIn, Telegram | Accepted |
| 0025 | Landing page shows Contact only; full résumé lives in the PDF | Superseded by ADR-0034 |
| 0026 | Dragon as a hidden easter egg | Accepted |
| 0027 | Save dragon as a token PNG | Accepted |
| 0028 | Open Graph tags for social share previews | Accepted (v2) |
| 0029 | New résumé material as the canonical source of truth | Accepted |
| 0030 | Downloadable résumé PDFs use `Name_Surname_Role` filenames | Accepted |
| 0031 | LLM / AI-agent optimized résumé build | Accepted |
| 0032 | Favicon: red pixel anarchy symbol | Superseded by ADR-0034 |
| 0033 | Evidence-first, concise résumé content | Accepted |
| 0034 | Recruiter-first landing page and neutral identity | Accepted |
| 0035 | Normalized machine-readable outputs and semantic validation | Accepted |
| 0036 | Compact ATS PDF and release quality gates | Accepted (v2) |
| 0037 | Self-hosted, dependency-light frontend | Accepted |
