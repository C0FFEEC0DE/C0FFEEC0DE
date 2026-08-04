# ADR-0013 — Three explicit resume audiences: human, LLM-agent, ATS

Date: 2026-07-30 · Status: Accepted (landing-page render narrowed by ADR-0025; human+ATS PDFs merged by ADR-0031)

## Context
Research (2026) shows a resume serves three audiences with conflicting needs:
- **Humans** (recruiters, 6-second scan): scannable, branded, one accent, quantified
  bullets front-loaded in the top third.
- **LLM agents / crawlers**: structured JSON with discovery, token-cheap summaries,
  and hiring signals (availability, work model). The 2026 trend is JSON as source of
  truth with rendering derived (JSON Resume, cv.json, Open Talent Protocol, Barba-CV).
- **ATS parsers** (~75% auto-reject before a human sees them): single column, standard
  fonts (Arial/Helvetica), standard section headings, dates on the title line, plain
  `•` bullets, **real selectable text**, no tables/columns/text-boxes/graphics.

Until ADR-0031, a single PDF could not satisfy both humans and ATS, so we kept two
PDFs. ADR-0031 merges the human and ATS PDFs into one file that is visually designed
*and* structurally ATS-safe, leaving the audience split as humans/ATS (one PDF) versus
LLM/AI agents (structured/narrative files).

## Decision
Generate **distinct outputs per audience**, all derived from the same markdown source:
- Human + ATS: `index.html` (landing) + `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf`.
  The single PDF is visually designed (Forest palette) and structurally ATS-safe
  (single column, real text, standard fonts, dates on the title line) (ADR-0031).
- LLM / AI agent: `resume.json`/`resume.ru.json` (JSON Resume), `resume.min.json`
  (token-cheap metadata tier), `resume-for-agents.md`, `agents.json`, `resume.txt`,
  `resume.md`, `llms.txt`, `AGENTS.md`, JSON-LD, and `/.well-known/cv.json`
  discovery (see ADR-0015 and ADR-0031).

## Consequences
- The download button serves one PDF that works for both humans and ATS.
- LLM/AI agents get a richer, convention-compliant ingestion surface while
  humans/ATS keep a single, unambiguous file.
- Adding a future format (e.g. `.docx`, VitaeFlow `.vf.pdf`) is a new renderer only.

## Version history
- **v1 (2026-07-30):** the human-facing PDF was `resume-branded.pdf` and the
  ATS PDF was `resume.pdf`.
- **v2 (2026-07-31):** the PDF filenames changed to the `Name_Surname_Role`
  pattern per ADR-0030. The ATS PDF is now
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` and the branded PDF is
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer_branded.pdf`; the audience split
  remains unchanged.
- **v3 (2026-08-03):** ADR-0031 merges the human and ATS PDFs into a single
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf`. LLM/AI-agent outputs are
  expanded with `resume-for-agents.md`, `agents.json`, and an enhanced
  `sitemap.xml`.