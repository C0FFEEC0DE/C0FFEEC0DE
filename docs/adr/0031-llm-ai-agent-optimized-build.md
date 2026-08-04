# ADR-0031 — LLM / AI-agent optimized résumé build

Date: 2026-08-03 · Status: Accepted

## Context

The site already serves three audiences (ADR-0013), but the split between
"human" and "machine" outputs is under-optimized for modern LLM agents and
recruiter AI crawlers. Current pain points:

1. Two PDFs (`resume.pdf` and `resume-branded.pdf`) confuse the download surface;
   the branded one is attractive to humans but has layout elements that ATS
   parsers dislike, while the plain ATS one looks poor when forwarded by email.
2. `llms.txt` and `AGENTS.md` are present (ADR-0003) but do not fully follow the
   emerging best-practice conventions for AI-agent ingestion (clear hierarchy,
   structured instructions, an OpenAI-style function spec, and a dedicated
   markdown file the agent can read end-to-end).
3. JSON-LD exists but is minimal; there is no `Person` + `ProfilePage` +
   `JobPosting`-ready structured data, and no sitemap entry that tells crawlers
   which files are authoritative.
4. The same single-column résumé should be both attractive to humans and safe for
   ATS parsers, eliminating the need to choose between two files.

## Decision

### 1. One human-readable, ATS-safe PDF

Replace the dual-PDF output with a single PDF that is:

- Visually designed (Forest palette, clean typography, generous spacing) so it is
  comfortable for a human to read and forward.
- Structurally ATS-safe: single column, real selectable text, standard fonts, no
  tables/floats/columns, dates on the same line as role/company, standard section
  headings, minimal graphics.

The single PDF is named from the owner and role per ADR-0030:
`Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf`.

### 2. Dedicated LLM / AI-agent build

Create a separate, intentionally machine-optimized set of artifacts derived from
the same markdown source:

- `resume-for-agents.md` — a single markdown document written for LLM ingestion:
  front-loaded summary, structured headings, keyword-rich skills matrix,
  achievements with metrics, explicit availability signals, and a short
  "Instructions for AI agents" block.
- `llms.txt` — llmstxt.org-compliant index that points agents at the cheapest
  entry point first (`resume.min.json`), then the full JSON Resume, then the
  agent résumé, then the human PDF.
- `AGENTS.md` — concise instructions: prefer `resume.json`, do not hallucinate,
  contact is in `basics`, availability is in `availability`.
- `.well-known/cv.json` — cv.json discovery manifest with explicit
  `agent_readable` and `human_readable` links.
- JSON-LD in `index.html` — expanded `Person` + `ProfilePage` schema with
  `sameAs`, `knowsAbout`, `workExperience`, and `availability`.
- `agents.json` — OpenAI-style structured output schema manifest so agents can
  call the résumé as a function (name, role, summary, skills, availability,
  contact).
- `sitemap.xml` — lists the canonical landing page and every machine-readable
  endpoint so crawlers discover them without guessing paths.

### 3. Machine-readable source of truth remains JSON Resume

`resume.json` / `resume.ru.json` stay the canonical structured source. All agent
artifacts are derived from them; they are not hand-maintained. The human PDF is
also derived from the same source, so no audience can drift.

### 4. Landing page stays a minimal business card

The page keeps its low-cognitive-load design (ADR-0008). The only visible résumé
CTA downloads the single human/ATS PDF. All LLM-facing links move to the footer
machine-links list and to the dedicated `/resume-for-agents.md` path.

## Consequences

- Recruiters and visitors have exactly one PDF to download. It looks good in
  email and parses safely through ATS.
- LLM agents get a richer, convention-compliant ingestion surface:
  `llms.txt` → `resume.min.json` → `resume.json` → `resume-for-agents.md`.
- The build emits one more file (`resume-for-agents.md` and `agents.json`), but
  the total maintenance burden drops because the two-PDF rendering path is gone.
- Tests must update to expect one PDF instead of two.
- ADR-0013 and ADR-0014 are amended by this decision: the audience split is now
  "human/ATS" (one PDF) vs. "LLM/AI-agent" (structured files), not "ATS PDF vs.
  branded PDF".

## Version history
- **v1 (2026-08-03):** merge ATS and branded PDFs into one human-readable,
  ATS-safe PDF; add dedicated LLM/AI-agent outputs and conventions.
