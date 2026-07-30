# ADR-0004 — Deploy via GitHub Pages + Actions (artifact)

Date: 2026-07-30 · Status: Accepted

## Context
The site must be hosted for free and rebuilt automatically on every push.

## Decision
Publish with the modern GitHub Pages artifact workflow: a two-job pipeline
(`build` → `deploy`) using `actions/configure-pages`,
`actions/upload-pages-artifact`, `actions/deploy-pages`. The repository Pages
source is set to "GitHub Actions", not a branch.

## Consequences
- Requires `pages: write` and `id-token: write` (OIDC) on the deploy job;
  `contents: read` everywhere else.
- No Jekyll; the build owns the exact `dist/` contents.
- A `CNAME` file in the build output is honored for custom domains (ADR-0005).