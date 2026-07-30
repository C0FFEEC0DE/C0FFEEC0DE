# ADR-0023 — Custom domain set to krasnobai.dev

Date: 2026-07-30 · Status: Accepted

## Context

ADR-0005 deferred the custom domain and made it env-driven. The owner also owns
the project domains `opendevops.run` and `opensre.run`, but `opendevops.run` is a
**project** (the Fusion DevOps platform). A résumé is a permanent personal
career asset that should outlive any single project: tying its canonical URL to
a project domain means a rebrand, sale, or sunset of that project forces the
résumé URL to move — breaking every shared `?d=` dragon link, the `curl`
one-liner, and every printed/PDF reference.

The owner purchased a **personal-name domain** instead: `krasnobai.dev` (the
surname, `.dev` for the developer signal). It is available, short, memorable
(`curl -sL krasnobai.dev/resume.txt`), HTTPS-only (`.dev` is HSTS-preloaded —
fine, GitHub Pages issues a free cert), and aligns with the owner's existing
identity (LinkedIn handle `aleksandrkrasnobai`).

## Decision

The résumé site's canonical domain is **`krasnobai.dev`** — a personal-name apex
domain owned by the owner and not tied to any project.

- `resume/resume.{en,ru}.md` set `basics.url = https://krasnobai.dev` and
  `meta.canonical = https://krasnobai.dev/resume.json` (the `TODO` on the
  personal-site URL is resolved and removed).
- The build remains **env-driven** (ADR-0005's mechanism is retained, not
  superseded): CI sets `vars.DOMAIN=krasnobai.dev` (and `vars.PAGES_URL` as the
  `github.io` fallback), so `build/build.py` emits `dist/CNAME` (apex) and
  absolute `https://krasnobai.dev/...` URLs in `llms.txt` / `sitemap.xml`.
- DNS: apex **A** records to the GitHub Pages IPs (`185.199.108-111.153`);
  Pages custom domain = `krasnobai.dev` + Enforce HTTPS.

## Consequences

- The résumé URL is portable and permanent; it does not depend on the fate of
  `opendevops.run` / `opensre.run`. The `opendevops.run` **project** entries in
  the résumé body are unaffected — they are portfolio projects, distinct from
  the site's own domain.
- Flipping the domain is still a config change (the `DOMAIN` env / repo
  variable), not a code change — ADR-0005's mechanism is retained.
- The "deferred" aspect of ADR-0005 is resolved; the env-driven mechanism stays.
- The `curl` one-liner, sitemap, `llms.txt`, and dragon share URLs all become
  `https://krasnobai.dev/...`. The local preview (`localhost:8000`) and the
  default `github.io` path still work when `DOMAIN` is unset.
- A build test pins the CNAME/absolute-URL behavior with `DOMAIN=krasnobai.dev`.

## Revision history
- **v1 (current):** choose `krasnobai.dev` (personal-name apex) over a `.run`
  subdomain; wire `url`/`canonical` + CI repo variables.