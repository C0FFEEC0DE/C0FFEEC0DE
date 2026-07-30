# ADR-0001 — Markdown is the single source of truth

Date: 2026-07-30 · Status: Accepted

## Context
The résumé must be authored by a human and also produce many machine outputs
(JSON Resume, plain text, PDF, HTML, llms.txt). Keeping two formats in sync by
hand is error-prone.

## Decision
The human edits `resume/resume.<lang>.md` (YAML front-matter + structured H2/H3
sections). `build/build.py` parses these and derives every other artifact. No
generated file is hand-edited.

## Consequences
- One place to edit content; the build guarantees consistency.
- The markdown format is opinionated (fixed section titles, a metadata line
  convention); a small parser (`build.py`) owns that contract.
- Adding an output format only requires a new renderer in `build.py`.