# ADR-0005 — Custom domain is deferred and env-driven

Date: 2026-07-30 · Status: Accepted
> **Update:** the deferral is resolved by ADR-0023 — the custom domain is now
> `krasnobai.dev` (a personal-name apex, not a `.run` subdomain). The env-driven
> mechanism decided here is retained unchanged.

## Context
The user will buy a `.run` domain later (owns `opendevops.run`, `opensre.run`);
the exact subdomain is undecided. The site must work today on the default Pages
URL and switch to a custom domain with zero code changes.

## Decision
The build reads `DOMAIN` (env / repo variable). When set it emits `dist/CNAME`
and uses absolute `https://DOMAIN/...` URLs in `llms.txt`/sitemap. When unset
it serves at `https://<user>.github.io/C0FFEEC0DE/` and emits no CNAME; an
optional `PAGES_URL` can supply absolute URLs.

## Consequences
- Flipping the domain is a config change, not a code change.
- Sitemap is only emitted when a base URL is known (it requires absolute URLs).
- DNS steps are documented in the README for when the domain is chosen.