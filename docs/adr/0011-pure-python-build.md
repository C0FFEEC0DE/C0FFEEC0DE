# ADR-0011 — Pure-Python build with minimal dependencies

Date: 2026-07-30 · Status: Accepted

## Context
The build runs in CI and locally; it should be easy to reason about and fast to
install, with a small supply-chain surface.

## Decision
`build/build.py` is pure Python (stdlib + `pyyaml`) with its own markdown
parser for the structured format. The only heavy dependency is `weasyprint`
for the PDF, and only if `PDF != 0`. `pytest` runs the test suite.

## Consequences
- CI installs just `pyyaml weasyprint pytest`.
- If WeasyPrint's system libs are missing, set `PDF=0` to skip the PDF and the
  rest of the site still deploys.
- The parser is small and owned by this repo (no `markdown`/`pandoc` runtime
  dependency for the core build).