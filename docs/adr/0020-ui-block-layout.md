# ADR-0020 — UI block layout (best-practices pass)

Date: 2026-07-30 · Status: Accepted

## Context

ADR-0008 locks low cognitive load as a first-class constraint and ADR-0018
locks the human, handcrafted feel. The *content* of the site is settled; this
ADR is about **how the blocks are arranged on the page**, reviewed against
mainstream UI-design best practices (visual hierarchy, one primary action,
Gestalt grouping, mobile-first responsive layout, scannability / the
Ladders–Nielsen recruiter scan pattern).

The landing page has three regions:

1. **Hero** — greeting, identity (name / label / summary), a CTA cluster
   (Download PDF + AI/LLM résumé), the curl one-liner + copy button, and the
   dragon.
2. **Résumé section** — `render_body_fragment` sections in order
   *Contact → Experience → Skills → Projects → Education → Certificates →
   Languages*, each a uniform `.block` card.
3. **Footer** — the "made by hand" note + a cluster of machine-readable links
   (resume.json, resume.min.json, resume.txt, branded PDF, llms.txt, AGENTS.md).

`render_body_fragment` is shared by the landing résumé section **and** the
branded-PDF body (ADR-0013), so any change to its section order or contact
rendering affects both outputs. A regression test (ADR-0016) pins the contact
URLs into `render_body_fragment`, so Contact cannot be moved out of it without
splitting the shared fragment — which this ADR deliberately avoids.

### What the review found

- **The hero carries two competing action clusters** — the audience CTA
  buttons (human PDF + AI/LLM) *and* the curl one-liner + copy. Two action
  groups in the first fold split the visitor's focal path and work against
  "one primary action" (Hick's law / ADR-0008). The curl line is an
  *operator/machine* affordance, not a human primary action.
- **The résumé section order is already the best-practice order.** Contact
  first (reachability — a recruiter can reach you without scrolling), then
  substance in descending professional weight (Experience carries the most
  detail and the most recruiter fixation), then credentials (Education,
  Certificates), then Languages last. This matches the widely-cited scan
  pattern; no reorder is wanted.
- **Uniform `.block` cards are a feature, not a defect.** Identical chrome
  (border, radius, shadow) across sections gives a predictable mental model
  (Gestalt consistency) and lowers cognitive load. Hierarchy is carried by
  heading scale and section order, not by differential card weight.
- **The hero's responsive behaviour is implicit.** It works (Bootstrap's row
  wraps the `col` / `col-auto` pair, so the identity column stacks above the
  dragon on narrow viewports) but is not pinned: `align-items-center` keeps
  vertically centering the stacked lines, and the dragon is not explicitly
  centered or capped on mobile.

## Decision

1. **One primary action zone in the hero.** The hero holds identity (greeting,
   name, label, summary) + exactly the two audience CTAs (human PDF + AI/LLM
   résumé) + the dragon. The **curl one-liner + copy button moves to the
   footer**, joining the existing machine-readable link cluster. The hero
   first fold now answers *who · what · how to get it* with a single focal
   action group; all operator/machine affordances live together in the
   footer "machine zone". The two audience buttons stay in the hero (the
   Playwright "hero has two audience links" guard is preserved — the curl
   block was never inside `.cta`).

2. **Footer as the machine/operator zone.** The curl one-liner + copy sits
   with `resume.json`, `resume.min.json`, `resume.txt`, the branded PDF,
   `llms.txt`, and `AGENTS.md`, so every non-human-primary affordance is
   grouped, discoverable, and out of the hero's focal path. The curl label is
   kept bilingual via the existing `data-i18n` machinery; `i18n.js` selects
   `#curl-line` / `.copy-curl` document-wide, so the move needs no JS change.

3. **Résumé section order is deliberately preserved** as
   *Contact → Experience → Skills → Projects → Education → Certificates →
   Languages*, with the rationale recorded here so future reorders are
   informed: Contact first for reachability, then substance in descending
   professional weight, credentials demoted, Languages last. No change to
   `render_body_fragment`'s order.

4. **Uniform content cards are kept.** Each section stays a `.block` card
   with identical chrome; hierarchy is carried by heading scale + order, not
   by card weight. We deliberately do **not** visually promote one section
   over another via card styling — consistency lowers cognitive load
   (ADR-0008).

5. **Responsive hero stacking is pinned.** A media query makes the narrow
   viewport a single column — identity + CTAs first, dragon below (text-first
   reading order, mobile-first). The dragon is centered and capped; the row
   switches to `align-items: flex-start` when stacked so a short identity block
   is not vertically centered against the dragon. Reduced-motion is already
   respected by the dragon bob (ADR-0009); this adds no new motion.

## Consequences

- The hero is calmer: one identity block + one CTA cluster + the dragon. The
  curl affordance is one scroll away in the footer, grouped with the other
  machine links — exactly where an operator/agent looking for machine formats
  would look.
- `render_body_fragment` is untouched, so the branded PDF and the landing
  résumé section stay in lockstep (ADR-0013), the contact-URL regression guard
  (ADR-0016) still passes, and the "no header in the body" / "one h1 per
  language" guards are unaffected.
- No JS change: `i18n.js` already selects the curl elements document-wide.
- The Playwright curl test (`#curl-line` contains `curl -sL … resume.txt` and
  the current origin) is document-wide and unaffected; the "two audience
  links" test is unaffected (curl was never in `.cta`).
- A small responsive addition to `site.css` pins the mobile hero layout that
  was previously only implicit.

## Revision history
- **v1 (current):** best-practices review of block arrangement; curl moved
  hero → footer; section order and uniform cards documented as deliberate;
  responsive hero stacking pinned.