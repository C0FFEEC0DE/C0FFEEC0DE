# ADR-0029 — New résumé material as the canonical source of truth

Date: 2026-07-31 · Status: Accepted

## Context

The résumé source files (`resume/resume.en.md` and `resume/resume.ru.md`) still
contained literal `TODO` placeholders and a concise, single-role narrative that
did not reflect the owner's full career depth. The owner provided a complete
professional profile: ~18 years of IT experience, progression from technical
engineer through DevOps/SRE to Staff DevOps Engineer, a long list of cloud /
DevOps / AI-agentic skills, 10 roles, education details, certifications, and
language fluency. They also asked to remove any mention of the internal
"MacSys" platform name from the public résumé.

## Decision

Replace the placeholder-heavy résumé content with the provided material and
designate `resume/resume.en.md` + `resume/resume.ru.md` as the single source of
truth for every output:

- `basics.label` becomes **Staff DevOps Engineer**.
- `basics.summary` is a short one-line identity statement used in the landing
  page hero, Open Graph `og:description`, and JSON Resume metadata. Keeping it
  short preserves the low-cognitive-load business-card fold (ADR-0008).
- The full professional intro (the long paragraph) is stored in
  `meta.intro` and rendered into:
  - `resume.txt` header,
  - `resume.md` header,
  - `llms.txt` blockquote,
  - the branded PDF as a "Summary" section.
- The ATS PDF intentionally **does not** render a Summary section (per
  ADR-0014) so it opens directly with Work Experience.
- Experience is listed in reverse chronological order, 10 entries, with the
  current Grid Dynamics Staff DevOps Engineer role first and the Self-employed
  offensive-security research role second.
- Skills are grouped by domain; technologies stay in English in both language
  files because they are universal identifiers.
- The internal platform name **MacSys** is replaced by a generic
  "internal self-service platform" description in the US retail client role.
- Education, certificates, and languages match the provided material.

## Consequences

- All résumé outputs (landing page, JSON Resume, plain text, markdown, both
  PDFs, llms.txt, AGENTS.md) now derive from the same canonical markdown
  sources, so they cannot drift.
- The landing page keeps a short hero lead while longer-form context is
  available to humans who download the branded PDF and to machines reading
  `llms.txt` / `resume.json`.
- Tests that pinned the old label, summary, and fluency levels were updated to
  match the new canonical data.
- No ADR supersedes ADR-0001 (markdown source of truth), ADR-0014 (ATS PDF
  structure), or ADR-0028 (Open Graph tags); this ADR only updates the
  *content* flowing through those existing pipelines.

## Revision history
- **v1 (2026-07-31):** canonical résumé rewrite from the owner-provided
  material; introduce `meta.intro` for full-form summary while keeping
  `basics.summary` short for the landing page and social previews.
