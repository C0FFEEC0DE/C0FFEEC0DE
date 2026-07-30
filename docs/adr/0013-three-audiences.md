# ADR-0013 — Three explicit resume audiences: human, LLM-agent, ATS

Date: 2026-07-30 · Status: Accepted (landing-page render narrowed by ADR-0025)

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

A single "PDF" cannot satisfy all three. A branded PDF is ATS-hostile; an ATS PDF is
ugly to humans; neither is structured for agents.

## Decision
Generate **distinct outputs per audience**, all derived from the same markdown source:
- Human: `index.html` (landing) + `resume-branded.pdf`.
- LLM-agent: `resume.json`/`resume.ru.json` (JSON Resume), `resume.min.json`
  (token-cheap metadata tier), `resume.txt`, `resume.md`, `llms.txt`, `AGENTS.md`,
  JSON-LD, and `/.well-known/cv.json` discovery (see ADR-0015).
- ATS: `resume.pdf` — the **default** downloadable PDF, an explicitly ATS-optimized
  plain render (see ADR-0014).

## Consequences
- More outputs to build/test, but each is correct for its audience.
- The download button serves the ATS-safe `resume.pdf` by default (safest to forward);
  the branded PDF is a secondary link.
- Adding a future format (e.g. `.docx`, VitaeFlow `.vf.pdf`) is a new renderer only.