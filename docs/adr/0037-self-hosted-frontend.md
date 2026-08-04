# ADR-0037 — Self-hosted, dependency-light frontend

Date: 2026-08-04 · Status: Accepted

## Context

The landing page used Bootstrap CSS from jsDelivr for a handful of button and
group styles. This made the first render dependent on a third party despite the
site otherwise having no tracking, backend, remote fonts, or required runtime
services.

## Decision

1. Remove Bootstrap and implement the small required button/group reset in the
   existing self-hosted stylesheet.
2. Keep all CSS, JavaScript, SVG, and raster assets first-party.
3. Add a restrictive meta Content Security Policy suitable for a static site,
   plus referrer policy and canonical metadata.
4. Preserve the no-JS English fallback, reduced-motion handling, WCAG AA palette,
   keyboard focus visibility, and responsive layout down to 320px.

## Consequences

- The résumé renders correctly without a CDN and leaks no routine asset requests
  to third parties.
- The page has fewer failure modes and a simpler security policy.
- A small amount of button CSS is now maintained locally and covered by UI tests.
- Superseded framework compatibility code and the old social-preview raster are
  removed rather than retained as live source assets.
