# ADR-0028 — Open Graph tags for social share previews

Date: 2026-07-31 · Status: Accepted (v2: 2026-08-04)

## Context

ADR-0022 added a "Share on LinkedIn" button that opens LinkedIn's composer
with the dragon URL pre-filled. LinkedIn builds the post preview by scraping
the shared page for Open Graph (`og:*`) meta tags. The page previously only had
a generic `<title>` and `<meta name="description">`, so the preview showed
the GitHub handle and a generic description rather than the owner's
name, role, and summary.

## Decision

Add Open Graph meta tags to the landing page `<head>`, populated at build time
from the English résumé front-matter:

- `og:title` — `"{name} — {label}"` (e.g. "Aleksandr Krasnobai — Staff DevOps Engineer").
- `og:description` — the short `basics.summary` (e.g. "Staff DevOps Engineer — 18 years keeping high-throughput platforms running...").
- `og:url` — the canonical site URL (`DOMAIN` or `PAGES_URL`).
- `og:type` — `profile`.
- `og:image` — `/assets/og-card.png`, a static 1200×630 PNG generated from the
  committed `src/og-card.svg` source.
- `og:image:width` / `og:image:height` — `1200` / `630`.
- `og:image:alt` — concise owner name and role text.
- `og:locale` — `en_US`.
- `profile:first_name` / `profile:last_name` — split from `basics.name`.

All values are HTML-escaped before injection. The tags are rendered into
`src/index.html` via a `{{OG_TAGS}}` placeholder replaced by `build/build.py`.

Because the dragon is drawn on a `<canvas>` at runtime, the same canvas cannot
serve as an `og:image`. The current static card instead matches the neutral,
evidence-first recruiter surface introduced by ADR-0034.

## Consequences

- LinkedIn (and other Open Graph consumers) now show the owner's name, role,
  summary, and selected impact evidence when the site is shared.
- The Open Graph image is static and intentionally independent of a visitor's
  seeded dragon; it acts as a stable professional preview.
- No backend or external image service is required; the PNG is copied from
  `src/` to `dist/assets/` during the build.
- `--check` fails if `dist/assets/og-card.png` is missing, so the image cannot
  be accidentally dropped.
- Build and UI tests assert the tags exist, use the expected content, and that
  the image file is served.

## Revision history
- **v2 (2026-08-04):** ADR-0034 replaces the old square dragon preview with an
  exact 1200×630 neutral recruiter card; the superseded raster is removed.
- **v1 (2026-07-31):** add build-time Open Graph tags and a static dragon OG
  image; supersede ADR-0010 (QR code) with a simpler share surface.
