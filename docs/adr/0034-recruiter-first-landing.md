# ADR-0034 — Recruiter-first landing page and neutral identity

Date: 2026-08-04 · Status: Accepted (v2)

## Context

The contact-only landing page required a recruiter to download a PDF before
seeing evidence behind the Staff title. Its machine-format links dominated the
mobile footer, the PDF CTA used an emoji that can render as a missing glyph, and
the social card showed only an abstract dragon. A red anarchy favicon expressed
personality but introduced avoidable ambiguity for infrastructure, security, and
compliance hiring contexts.

## Decision

1. Keep the page compact and calm: identity, one scale signal in the summary,
   contacts, then the CTA. Do not render a separate KPI/metric-card strip;
   detailed achievements remain in the PDF and machine-readable résumé.
2. Keep the PDF as the primary CTA and add GitHub as a secondary CTA.
3. Replace the emoji with a self-hosted inline document SVG.
4. Replace the anarchy favicon with a neutral, self-hosted pixel `AK` monogram.
5. Replace the square dragon-only Open Graph image with a 1200×630 card carrying
   the candidate name, role, impact figures, domain, and a restrained dragon mark.
6. Keep the dragon as a hidden easter egg, but remove defensive “not a template”
   copy from the visible footer.
7. Put machine-readable links inside an accessible `<details>` disclosure.
8. Support `?lang=ru` as a durable Russian entry URL and publish canonical and
   `hreflang` links for English/Russian discovery.

## Consequences

- Recruiters see enough scale to orient themselves without a product-style KPI
  strip or repeated claims.
- The primary action remains unambiguous while source work is one click away.
- The identity stays handcrafted without introducing political interpretation.
- ADR-0025 and ADR-0032 are superseded.

## Revision history

- **v2 (2026-08-04):** remove the three metric cards after production review;
  retain one scale signal in the summary and keep detailed evidence in the
  résumé artifacts.
- **v1 (2026-08-04):** recruiter-first CTA, selected evidence cards, neutral
  identity, durable RU URL, and collapsed machine links.
