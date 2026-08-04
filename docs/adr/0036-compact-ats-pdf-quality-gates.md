# ADR-0036 — Compact ATS PDF and release quality gates

Date: 2026-08-04 · Status: Accepted (v2)

## Context

The single PDF was selectable and single-column but expanded to seven pages,
placed the summary alone on page one, split low-signal job detail across pages,
and had no maximum-page or placeholder regression guard.

## Decision

1. Target no more than four US-letter pages for the canonical English PDF.
2. Use compact spacing while preserving readable type, a single column, real
   text, standard headings, and clickable contact/project links.
3. Prefer page breaks between roles and prevent orphaned headings; a long role
   may split only when it cannot fit as one unit.
4. Write PDF title, author, subject, and keywords metadata.
5. Extract the generated PDF in tests and require key facts, valid reading order,
   no raw Markdown/placeholders, and a page count of four or fewer.
6. Add content-quality checks for undefined `100%` claims, unsupported direct
   management wording, malformed optional fields, and accidental EN/RU drift.
7. Before publishing, require repository/agent documentation and the ADR index
   to match the implemented source-of-truth, dependency, output, and deployment
   behavior.
8. After GitHub Pages deployment, run a retrying public smoke test that checks
   endpoint availability, artifact signatures, and live résumé version freshness.

## Consequences

- The same PDF remains human-readable and ATS-safe, but now has a measurable
  compactness contract.
- Content growth must displace lower-value material instead of silently adding
  pages.
- Deployment success includes public artifact verification, not only a
  successful Pages API response. A stale CDN response is retried before failing.
- ADR-0014 and ADR-0031 remain in force and are tightened by these gates.

## Revision history

- **v2 (2026-08-04):** add documentation synchronization and post-deploy public
  verification to the release gate.
- **v1 (2026-08-04):** compact PDF target, schema validation, extraction, and
  evidence-quality checks.
