# ADR-0020 — UI block layout (best-practices pass)

Date: 2026-07-30 · Status: Accepted (v5: 2026-08-04)

## Context

ADR-0008 locks low cognitive load as a first-class constraint, ADR-0018 locks the
human, handcrafted feel, and ADR-0026 hides the dragon behind a footer easter
egg. The *content* of the site is settled; this ADR is about **how the blocks
are arranged on the page**, reviewed against mainstream UI-design best practices
(visual hierarchy, one primary action, Gestalt grouping, mobile-first responsive
layout, scannability / the Ladders–Nielsen recruiter scan pattern, and accessible
landmarks).

The landing page has four visible regions:

1. **Hero** — greeting and identity (name / label / summary). The dragon no
   longer lives here by default; it is revealed from the footer (ADR-0026).
2. **Contact section** — a compact email + LinkedIn + Telegram block injected
   as `render_contact_fragment`.
3. **CTA section** — a primary PDF action and a secondary GitHub evidence link
   immediately after the contact row (ADR-0034 v2).
4. **Footer** — the "made by hand" note + a compact, inline list of
   machine-readable format links collapsed under a native disclosure control.

The full résumé body is rendered only for the single PDF and the markdown/
plain-text outputs (ADR-0031/0034). The landing page shares
`_contact_section` with the PDF, so contact stays in lockstep while the page
stays short.

### What the v2 review found

- **The hero's responsive behaviour is incomplete.** The CSS media query only
  changes `align-items` on the Bootstrap `.row`; the `col` / `col-auto` columns
  stay side-by-side on narrow viewports, so the identity text is cramped next
  to the dragon. Best practice is a real single-column stack with the dragon
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
- **The footer machine links are a prose paragraph.** The `resume.json` /
  `llms.txt` cluster is rendered as `·`-separated inline links inside a `<p>`.
  This is scannable for sighted users but is not a navigable list for
  screen-reader users. Best practice: wrap the links in a semantic `<ul>` under
  a (visually hidden) heading, while preserving the inline visual density with
  CSS-generated separators.

### What the v3 simplification changed

The v2 machine zone added a `<section class="machine-zone">` with a visually
hidden "Machine-readable versions" heading, a curl one-liner + copy button,
and the format list. A further pass found that heading + one-liner made the
footer too verbose for an intentionally minimal business card. The v3 footer
keeps only:

- the handcrafted `.made` note, and
- the `.machine-links` `<ul>` as an inline, semantic list.

The curl one-liner is no longer shown on the page, but `resume.txt` is still
served and the command from ADR-0006 still works for anyone who knows the URL.

## Decision

1. **One shared content column.** Topbar, `<main>`, and footer are all
   constrained to the same `--max: 640px` column with `--gutter` horizontal
   padding. The topbar toggles align to the content column's right edge; the
   page stops looking like independent full-width bands.

2. **Contact moves into `<main>`.** The landing page keeps exactly one `<main>`
   landmark, with `id="main"`. The hero and the Contact section (`#resume`) both
   live inside it. The skip-link now targets `#main` ("Skip to content"), which
   is the textbook accessible target, instead of jumping over the hero to
   `#resume`. The `#resume` id is preserved because it is a pinned internal
   reference and renaming would churn tests for no gain.

3. **Hero is text-only and stacks naturally.** The hero holds only identity
   (name / label / summary). The dragon was moved out of the hero by ADR-0026
   and now lives in a separate hidden section below the CTA; it is revealed by
   clicking the footer "made" note. This keeps the first fold minimal and avoids
   any side-by-side crowding on narrow viewports.

4. **Footer is minimal.** The footer contains the `.made` handcrafted note and
   a native `<details>` disclosure containing the `.machine-links` inline
   `<ul>`. There is no `<section
   class="machine-zone">`, no visually-hidden "Machine-readable versions"
   heading, no curl one-liner, and no copy button. The list remains semantic
   and visually compact (CSS removes bullets and renders `·`-separators), so
   screen-reader users can still browse it as a list.

5. **No change to theme, color, font, bilingual, or no-JS behaviour.** The
   Forest palette, system sans-serif, language toggle, dragon functionality
   (seeding, sharing, saving), and the no-JS `prefers-color-scheme` fallback are
   all untouched. The only visual differences are the aligned content column,
   the minimal text-only hero, and the simplified footer.

## Consequences

- Mobile visitors get a clean vertical path: identity → Contact → CTA → footer.
  No side-by-side crowding at 390 px.
- Landmarks are correct: `header` (banner) → `main` (one, with hero + Contact +
  CTA + the hidden dragon container) → `footer` (contentinfo).
- The skip-link no longer bypasses the hero; it lands at the start of the main
  content, matching the visible page order.
- Screen-reader users can still navigate the machine-readable format list as a
  `<ul>`, but there is no longer a dedicated "Machine-readable versions"
  heading above it.
- The curl one-liner from ADR-0006 is no longer advertised in the UI. The file
  `resume.txt` is still served and the command still works; only the on-page
  copy button and label were removed.
- `render_contact_fragment` and `_contact_section` are untouched, so the single
  PDF and the landing Contact block stay in lockstep (ADR-0025/0031), and the
  contact-URL regression guard still passes.
- No JS change is required for the v3 footer; the existing `i18n.js`
  `data-i18n` machinery is unaffected.
- A small CSS addition pins the narrow-viewport layout, and the ADR-0020 v2/v3
  tests add regression guards for the single-column mobile layout and the
  semantic footer list. The v3 tests assert the machine zone and curl one-liner
  are gone from the footer.

## Revision history

- **v5 (2026-08-04):** ADR-0034 v2 removes the separate metric-card strip;
  detailed evidence remains in the PDF and machine outputs while the landing
  flows directly from contacts to the two CTAs.
- **v4 (2026-08-04):** amended by ADR-0034/0037: add selected impact evidence,
  keep PDF primary with GitHub secondary, collapse machine formats under
  `<details>`, and replace framework layout classes with self-hosted CSS.
- **v1 (2026-07-30):** best-practices review of block arrangement; curl moved
  hero → footer; section order and uniform cards documented as deliberate;
  responsive hero stacking described but left partly implicit.
- **v2 (2026-07-31):** full best-practices implementation pass: shared content
  column, Contact moved into `<main>`, skip-link targets `#main`, hero uses a
  CSS grid that truly stacks on narrow screens, footer machine zone becomes a
  semantic list with a visually-hidden heading.
- **v3 (2026-07-31):** simplify the footer further: drop the machine-zone
  section, the "Machine-readable versions" heading, and the on-page curl
  one-liner + copy button. Keep the `.machine-links` inline list and the
  handcrafted `.made` note. ADR-0006 still honored because `resume.txt` remains
  served.
