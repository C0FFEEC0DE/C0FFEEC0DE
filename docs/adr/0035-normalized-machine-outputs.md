# ADR-0035 — Normalized machine-readable outputs and semantic validation

Date: 2026-08-04 · Status: Accepted

## Context

Markdown emphasis leaked into JSON Resume skills, certificates, JSON-LD, plain
text, and the PDF. Optional certificate dates rendered as `None (None)`, Russian
plain text used the English `Present`, and `Person.seeks` pointed to a
`JobPosting` although Schema.org expects a `Demand`. Existing tests verified file
presence but did not reject these semantic defects.

## Decision

1. Normalize inline Markdown before structured parsing; formatting syntax never
   becomes résumé data.
2. Parse certificate issuer, optional date, and optional URL independently.
3. Pass the output language into text/markdown renderers so localized present
   labels remain correct.
4. Emit clean, de-duplicated `knowsAbout` values.
5. Represent availability as a Schema.org `Demand` with a descriptive name and
   area served; do not publish a candidate-authored `JobPosting`.
6. Validate all generated text/JSON/JSON-LD for forbidden placeholders and raw
   Markdown markers. Validate EN/RU structural parity and critical facts.
7. Keep JSON Resume custom `availability` metadata, while preserving standard
   field types and ISO-compatible dates.
8. Vendor the official JSON Resume v1.0.0 schema and validate the standard EN/RU
   subsets in every checked build; custom availability remains an explicit
   extension outside that subset.

## Consequences

- ATS, LLM, and search consumers receive the same clean facts as humans.
- Missing optional facts remain absent instead of becoming string placeholders.
- Tests fail on the exact regressions found during the public-site review.
- ADR-0031 is amended: discoverability is subordinate to semantic correctness.
