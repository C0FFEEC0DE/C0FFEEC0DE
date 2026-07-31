# ADR-0020 — UI block layout (best-practices pass)

Date: 2026-07-30 · Status: Accepted (v2: 2026-07-31)

## Context

ADR-0008 locks low cognitive load as a first-class constraint and ADR-0018
locks the human, handcrafted feel. The *content* of the site is settled; this
ADR is about **how the blocks are arranged on the page**, reviewed against
mainstream UI-design best practices (visual hierarchy, one primary action,
Gestalt grouping, mobile-first responsive layout, scannability / the
Ladders–Nielsen recruiter scan pattern, and accessible landmarks).

The landing page has three regions:

1. **Hero** — greeting, identity (name / label / summary), a CTA cluster
   (Download PDF + AI/LLM résumé), and the dragon. The curl one-liner + copy
   button live in the footer machine zone (ADR-0006 / ADR-0020 v1).
2. **Contact section** — the only résumé content rendered on the landing page
   (ADR-0025). It is injected as `render_contact_fragment`.
3. **Footer** — the "made by hand" note + the machine zone (curl one-liner +
   copy button + machine-readable format links).

`render_body_fragment` is used only by the branded-PDF body now (ADR-0025);
the landing page shares only `_contact_section` with it, so contact stays in
lockstep while the page stays short.

### What the v2 review found

- **The hero's responsive behaviour is incomplete.** The CSS media query only
  changes `align-items` on the Bootstrap `.row`; the `col` / `col-auto` columns
  stay side-by-side on narrow viewports, so the identity text is cramped next to
  the dragon. Best practice is a real single-column stack with the dragon
  centered below the identity (mobile-first, text-first reading order).
- **The Contact section is an orphan landmark.** `<section id="resume">` sits
  between `</main>` and `<footer>`, and the skip-link jumps straight over the
  hero. Best practice: keep all primary content inside one `<main>` landmark,
  skip to the top of it, and let `#resume` remain a pinned in-page id.
- **The content column is not aligned across regions.** Topbar spans the full
  viewport, while `main` / `section` / `footer` each use Bootstrap `.container`
  independently. Best practice: one shared column (`--max` + `--gutter`) for
  topbar, main, and footer so the toggles align with the content edge and the
  page feels visually coherent.
- **The footer machine links are a prose paragraph.** The `resume.json` / `llms.txt`
  cluster is rendered as `·`-separated inline links inside a `<p>`. This is
  scannable for sighted users but is not a navigable list for screen-reader users.
  Best practice: wrap the links in a semantic `<ul>` under a (visually hidden)
  heading, while preserving the inline visual density with CSS-generated
  separators.

## Decision

1. **One shared content column.** Topbar, `<main>`, and footer are all
   constrained to the same `--max: 860px` column with `--gutter` horizontal
   padding. The topbar toggles align to the content column's right edge; the
   page stops looking like independent full-width bands.

2. **Contact moves into `<main>`.** The landing page keeps exactly one `<main>`
   landmark, with `id="main"`. The hero and the Contact section (`#resume`) both
   live inside it. The skip-link now targets `#main` ("Skip to content"), which
   is the textbook accessible target, instead of jumping over the hero to
   `#resume`. The `#resume` id is preserved because it is a pinned internal
   reference and renaming would churn tests for no gain.

3. **Hero uses CSS Grid for real mobile-first stacking.** On wide viewports
   the grid is `minmax(0, 1fr) auto` — identity on the left, dragon on the
   right, vertically centered. On narrow viewports (`max-width: 640px`) the grid
   collapses to a single column: identity full-width first, dragon centered and
   capped below it. This removes the implicit Bootstrap column behaviour and
   gives a predictable, text-first reading order.

4. **Footer machine zone uses semantic markup.** The curl one-liner and the
   machine-readable links are wrapped in `<section class="machine-zone" aria-labelledby="machine-heading">`.
   A visually hidden `<h2 id="machine-heading">` labels the section, and the
   links are an unordered list. CSS removes bullets and renders inline
   `·`-separators, so the visual surface is unchanged for sighted users while
   screen-reader users gain a heading and list navigation.

5. **No change to theme, color, font, dragon, bilingual, or no-JS behaviour.**
   The Forest palette, JetBrains Mono, language toggle, dragon share path, and
   the no-JS `prefers-color-scheme` fallback are all untouched. The only visual
   differences are the aligned column, the narrow-hero stack, and the unchanged
   inline footer links.

## Consequences

- Mobile visitors get a clean vertical path: identity → CTAs → dragon → Contact
  → footer. No side-by-side crowding at 390 px.
- Landmarks are correct: `header` (banner) → `main` (one, with hero + Contact)
  → `footer` (contentinfo).
- The skip-link no longer bypasses the hero; it lands at the start of the main
  content, matching the visible page order.
- Screen-reader users can navigate to "Machine-readable versions" by heading
  and browse the format list as list items.
- `render_contact_fragment` and `_contact_section` are untouched, so the branded
  PDF and the landing Contact block stay in lockstep (ADR-0025), and the
  contact-URL regression guard still passes.
- No JS change is required for the new layout; the existing `i18n.js`
  `data-i18n` machinery translates the new visually-hidden heading.
- A small CSS addition pins the mobile hero layout that was previously only
  half-implemented, and the ADR-0020 v2 tests add regression guards for the
  stack and the semantic footer list.

## Revision history
- **v1 (2026-07-30):** best-practices review of block arrangement; curl moved
  hero → footer; section order and uniform cards documented as deliberate;
  responsive hero stacking described but left partly implicit.
- **v2 (2026-07-31):** full best-practices implementation pass: shared content
  column, Contact moved into `<main>`, skip-link targets `#main`, hero uses a
  CSS grid that truly stacks on narrow screens, footer machine zone becomes a
  semantic list with a visually-hidden heading.
