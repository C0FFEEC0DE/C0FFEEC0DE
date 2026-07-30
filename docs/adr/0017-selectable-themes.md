# ADR-0017 — Single Forest theme

Date: 2026-07-30 · Status: Accepted

## Context
ADR-0008 locks low cognitive load as a first-class constraint. This ADR first
shipped a *selectable* multi-palette system (originally ten, then thirteen —
Calm, Gold, Synthwave, Vapor, Phosphor, Amber, Forest, Ocean, Rose, Sand,
Slate, Mono, Nord) chosen live via a `<select>` in the top bar, so the owner
could try looks before settling. After living with them, the owner asked to
**keep only the Forest theme** and drop the picker. A picker with one option
is pointless UI and adds cognitive load, so the whole selection mechanism is
removed: Forest becomes the bare `:root` default with no `data-palette` axis.

## Decision
Ship a **single** theme — **Forest** — with a light and a dark variant:

- **Forest light** — paper-neutral greens (`--c-bg #f4f6f2`, `--c-surface #fff`,
  `--c-text #1f2a1f`, `--c-muted #5b6b5b`), one green accent `#2f7d3a`,
  `--c-accent-soft #dcebd9`, `--c-line #e0e6dd`, soft rounding, warm low shadow.
- **Forest dark** — `--c-bg #131a14`, `--c-surface #1d251e`, `--c-text #e6eee6`,
  `--c-muted #97a897`, light accent `#7cc68a` (dark text on it for AA).

Mechanics:
- `:root` carries the Forest light tokens plus the full Bootstrap component-var
  mappings (`--bs-body-bg`, `--bs-body-color`, `--bs-link-color`, the `--bs-*-rgb`
  triplets, `--bs-font-sans-serif`). `:root[data-theme="dark"]` re-declares every
  mode-sensitive `--c-*` token and the dark triplets, so dark mode fully overrides
  light (no light color leaks through). `--c-head-font` is mode-independent and
  lives only in the light block.
- `data-theme` (light/dark) is the **only** color axis. It is set on load by
  `i18n.js` (from `localStorage("theme")` or `prefers-color-scheme`) and toggled
  by the ◐ button. There is no `data-palette` attribute anywhere.
- The no-JS path: `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]):not([data-theme="dark"]) { …forest dark… } }`
  applies Forest dark before JS runs; once JS sets `data-theme` it stops
  matching. With JS off and a light OS, the bare `:root` Forest light applies.

## Consequences
- The top bar is simpler (language toggle + ◐ only); no picker, no `data-palette`
  axis, no palette allow-list or `applyPalette`/`initPalette` in `i18n.js`.
  Cognitive load drops, matching ADR-0008.
- The theme is no longer user-switchable live; changing it is a source edit to
  the `:root` / `:root[data-theme="dark"]` blocks in `src/site.css`. The
  thirteen-palette history is preserved in git, so re-adding a theme is a
  matter of restoring a palette block + an `<option>` + the `PALETTES`
  allow-list — but that is now opt-in, not the default.
- A build test asserts the picker is gone, no `data-palette` remains, and
  the Forest light + dark blocks exist with the dark block re-declaring every
  mode-sensitive color token; Playwright asserts the ◐ toggle flips the accent
  between `#2f7d3a` (light) and `#7cc68a` (dark).
- Contrast is **machine-enforced** (ADR-0019): the build computes the WCAG ratio
  for the Forest theme in both modes across text/muted/accent on both
  `--c-bg` and `--c-surface`, plus button-on-accent, and fails below 4.5:1.
- **Print is theme-agnostic.** `@media print` forces the Forest light tokens
  with `!important`, so Ctrl+P always renders dark-on-light even when dark mode
  is active. The live page is not the real print path (the branded PDF is — see
  ADR-0014), but this keeps an impromptu browser print readable. A Playwright
  test pins this by emulating print media under dark mode.
- **The branded PDF matches the theme.** `src/print.css` (rendered via
  WeasyPrint into `resume-branded.pdf`) uses the Forest palette (accent
  `#2f7d3a`, text `#1f2a1f`, muted `#5b6b5b`, line `#e0e6dd`), so the
  downloadable PDF matches the on-screen Forest theme rather than the old calm
  blue/brown. A build test pins this so the PDF can't drift back to the
  pre-reduction calm colors.

## Revision history
- **v3 (current):** reduced to the single Forest theme; picker and
  `data-palette` axis removed per owner preference.
- **v2:** added Vapor (vaporwave), Phosphor (green CRT), Amber (amber CRT) —
  thirteen palettes; added a machine-enforced contrast guard (ADR-0019) and an
  accent-distinctness guard.
- **v1:** ten selectable palettes (Calm, Gold, Synthwave, Forest, Ocean, Rose,
  Sand, Slate, Mono, Nord) with a live picker; contrast hand-verified AA.