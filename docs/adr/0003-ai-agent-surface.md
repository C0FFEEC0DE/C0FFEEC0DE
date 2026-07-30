# ADR-0003 — AI-agent surface: llms.txt + AGENTS.md + JSON-LD

Date: 2026-07-30 · Status: Accepted

## Context
LLM agents and crawlers need to ingest the résumé cheaply and reliably.

## Decision
Provide three complementary agent-facing artifacts:
- `llms.txt` — curated markdown index (llmstxt.org convention: H1, blockquote
  summary, link list), served as text/plain.
- `AGENTS.md` — short note telling agents what the site is and pointing at
  `resume.json` / `resume.txt`.
- JSON-LD `Person` embedded in `index.html` for search/agent parsing.

## Consequences
- Agents get a one-file index (`llms.txt`) plus a structured source (`resume.json`).
- llms.txt links use absolute URLs when `DOMAIN`/`PAGES_URL` is set; relative
  otherwise (see ADR-0005).