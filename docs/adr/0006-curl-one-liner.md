# ADR-0006 — curl one-liner over explicit plain-text paths

Date: 2026-07-30 · Status: Accepted

## Context
The user wants the résumé downloadable via a one-line shell command, and easy
to parse by robots.

## Decision
Serve distinct, explicit paths rather than content-negotiation on `/`:
- `resume.txt` — flat plain text (both languages), the curl target.
- `resume.json` — JSON Resume.
- `resume.pdf` — printable PDF.
The browser gets a styled `index.html` at `/`; curl gets a meaningful file at
`/resume.txt`.

## Consequences
- The one-liner `curl -sL <host>/resume.txt` just works; no server-side logic.
- GitHub Pages serves `.txt`/`.json` with sane content types out of the box.