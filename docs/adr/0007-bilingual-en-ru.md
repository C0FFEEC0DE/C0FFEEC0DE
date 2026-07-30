# ADR-0007 — Bilingual EN/RU via paired markdown + client toggle

Date: 2026-07-30 · Status: Accepted

## Context
The audience is global recruiters (EN) and the user's local market (RU).

## Decision
Author two parallel sources (`resume.en.md`, `resume.ru.md`) with identical
structure. The build renders both into `index.html` as two blocks; `i18n.js`
toggles visibility, persists the choice in `localStorage`, and defaults to
`navigator.language`. Separate `resume.json` / `resume.ru.json` are emitted.

## Consequences
- Both languages are first-class (full machine output each), not a runtime
  machine translation.
- Editing content means updating two files; the structure keeps them aligned.
- No server; the toggle is client-side and cookie-free.