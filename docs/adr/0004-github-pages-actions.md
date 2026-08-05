# ADR-0004 — Deploy via GitHub Pages + Actions (artifact)

Date: 2026-07-30 · Status: Accepted (v2)

## Context
The site must be hosted for free and rebuilt automatically on every push.

## Decision
Publish with the modern GitHub Pages artifact workflow: a two-job pipeline
(`build` → `deploy`) using `actions/upload-pages-artifact@v5`
(with `include-hidden-files: true` so `.well-known/cv.json` is published) and
`actions/deploy-pages@v4`. The repository Pages source is set to "GitHub
Actions", not a branch.

Before uploading the artifact, the pipeline:
1. Runs `pytest` on `build/test_build.py`.
2. Runs `python build/build.py --check` to validate all generated artifacts.
3. Runs `python scripts/validate_consistency.py` to cross-check every `dist/`
   output against the canonical `resume/resume.en.md`.

After deployment, the pipeline runs `python scripts/verify_deployed.py <URL>`
to retry the public endpoint, verify artifact signatures, and confirm that the
live `resume.json` version and `lastModified` match the committed source.

## Consequences
- Requires `pages: write` and `id-token: write` (OIDC) on the deploy job;
  `contents: read` everywhere else.
- No Jekyll; the build owns the exact `dist/` contents.
- A `CNAME` file in the build output is honored for custom domains (ADR-0005).
- A stale CDN response or missed artifact now fails the release rather than
  passing silently.

## Revision history
- **v2 (2026-08-04):** add `include-hidden-files: true`, `validate_consistency.py`,
  and `verify_deployed.py` to the artifact workflow description.
- **v1 (2026-07-30):** initial GitHub Pages artifact workflow decision.
