# ADR-0012 — Security: escape all generated/injected content

Date: 2026-07-30 · Status: Accepted

## Context
The repo is public and the build injects content into `index.html`. Even if
the threat model is "only the owner edits the markdown", a defensive posture
prevents stored-XSS if content is ever user-influenced.

## Decision
- Every field rendered into the resume HTML goes through `html.escape` (the
  visible body is safe).
- The JSON-LD block escapes `<`, `>`, `&` to `<`/`>`/`&` so a
  field cannot break out of the `<script type="application/ld+json">` context.
- Template placeholder substitution uses a single-pass `re.sub` (which does not
  re-scan replacement text) so a `{{JSONLD}}` token in resume content stays
  literal and is not re-expanded.
- Regression tests inject `<script>` and `{{JSONLD}}` payloads and assert they
  are escaped/neutralized.

## Consequences
- `--check` plus `pytest` (both run in CI) guard against regressions.
- A malicious/corrupted `resume/*.md` cannot inject markup into the live page.