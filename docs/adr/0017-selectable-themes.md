# ADR-0017 — Single fixed Forest theme

Date: 2026-07-30 · Status: Accepted (v5: 2026-08-04)

## Context
ADR-0008 locks low cognitive load as a first-class constraint. This ADR first
shipped a *selectable* multi-palette system (originally ten, then thirteen —
Calm, Gold, Synthwave, Vapor, Phosphor, Amber, Forest, Ocean, Rose, Sand,
Slate, Mono, Nord) chosen live via a `<select>` in the top bar, so the owner
could try looks before settling. After living with them, the owner asked to
**keep only the Forest theme** and drop the picker. A picker with one option
is pointless UI and adds cognitive load, so the whole selection mechanism is
removed: Forest becomes the bare `:root` default with no `data-palette` axis.

Later, for the minimal business-card redesign, the owner asked to fix the page
in the **light Forest** mode and remove the dark variant and the toggle
entirely. A one-page résumé business card does not need a theme switch; the
light palette is readable, friendly, and keeps the layout simple.

## Decision
Ship a **single, fixed light Forest theme**. There is no dark variant and no
visitor-facing theme switch:

- **Forest light** — paper-neutral greens (`--c-bg #f4f6f2`, `--c-surface #fff`,
  `--c-text #1f2a1f`, `--c-muted #5b6b5b`), one green accent `#2f7d3a`,
  `--c-accent-soft #dcebd9`, `--c-line #e0e6dd`, soft rounding, warm low shadow.

Mechanics:
- `:root` carries the Forest light tokens consumed by the self-hosted layout and
  button system. There are no framework compatibility variables and no
  `:root[data-theme="dark"]` block (ADR-0037).
- The `data-theme` attribute is **not set anywhere** — not by `i18n.js`, not by
  the page. The bare `:root` is the only source of color.
- The no-JS `@media (prefers-color-scheme: dark)` fallback is removed: with a
  fixed light theme, the OS preference is intentionally ignored. The page is
  always Forest light, both with and without JavaScript.
- The theme-toggle button (◐) is removed from the top bar.

## Consequences
- The top bar is now just the language toggle. Cognitive load drops further,
  matching ADR-0008.
- `src/site.css` shrinks: one `:root` block, no dark overrides, no no-JS dark
  media query, no dark-mode button text rules.
- `src/i18n.js` no longer reads/writes `localStorage("theme")` and no longer
  flips `data-theme` / `data-bs-theme`.
- Contrast is still machine-enforced (ADR-0019), but now only the light mode
  pairs are checked: text/muted/accent on `--c-bg` and `--c-surface`, plus
  button-text-on-accent.
- **Print is trivially theme-agnostic.** `@media print` already forces the
  Forest light tokens with `!important`; because the live page never leaves
  light, the print override is now a defensive guard rather than a mode flip.
- **The branded PDF matches the live page.** `src/print.css` keeps the Forest
  palette (accent `#2f7d3a`, text `#1f2a1f`, muted `#5b6b5b`, line `#e0e6dd`).
- The dark-mode Playwright tests are removed. The remaining no-JS tests assert
  that scripts blocked still yield the same Forest light background and that
  no `data-theme` attribute is injected.

## Revision history
- **v5 (2026-08-04):** remove obsolete framework-variable mappings after the
  frontend became fully self-hosted (ADR-0037); theme colors and behavior stay
  unchanged.
- **v4:** fixed light Forest theme only; dark variant, toggle, and
  no-JS dark query removed per owner preference for the minimal business card.
- **v3:** reduced to the single Forest theme; picker and `data-palette` axis
  removed per owner preference.
- **v2:** added Vapor (vaporwave), Phosphor (green CRT), Amber (amber CRT) —
  thirteen palettes; added a machine-enforced contrast guard (ADR-0019) and an
  accent-distinctness guard.
- **v1:** ten selectable palettes (Calm, Gold, Synthwave, Forest, Ocean, Rose,
  Sand, Slate, Mono, Nord) with a live picker; contrast hand-verified AA.
