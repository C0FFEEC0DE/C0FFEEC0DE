# ADR-0002 — JSON Resume v1.0.0 as the machine-readable format

Date: 2026-07-30 · Status: Accepted

## Context
Robots/recruiters need a structured, schema-validated representation. A custom
schema would be non-standard and undiscoverable.

## Decision
Emit `resume.json` / `resume.ru.json` conforming to the [JSON Resume](https://jsonresume.org)
schema v1.0.0 (`basics, work, education, skills, projects, certificates,
languages, meta`). Front-matter maps to `basics`/`profiles`/`meta`; body sections
map to the arrays.

## Consequences
- Compatible with the existing JSON Resume ecosystem (validators, themes).
- Dates are ISO 8601 (`YYYY-MM`).
- Schema is extensible (`[k: string]: any`), so custom fields don't break it.