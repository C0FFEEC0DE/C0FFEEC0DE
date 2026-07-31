# ADR-0008 — Low-cognitive-load design as a first-class constraint

Date: 2026-07-30 · Status: Accepted (v2: 2026-07-31)

## Context
The user explicitly wants the site to impose minimal cognitive load on visitors.

## Decision
Constrain the design: single column, one first fold (name + label + summary),
one primary CTA, and the dragon as a hidden footer easter egg (ADR-0026), a
calm two-surface palette with a single accent, light/dark via
`prefers-color-scheme` + toggle, no autoplay/flashing, generous whitespace,
scannable sections (chips for skills, lists for experience). All text/surface
pairs meet WCAG AA (4.5:1).

## Consequences
- The dragon is the only "delight" element. Its placement was later narrowed by
  ADR-0026 to a hidden easter egg revealed from the footer, so it never competes
  with content on the initial view.
- `prefers-reduced-motion` disables the gentle dragon bob.
- Contrast is verified at build time (see ADR-0012 notes / tests).

## Revision history
- **v1 (2026-07-30):** initial low-cognitive-load constraint; dragon in the hero.
- **v2 (2026-07-31):** updated to reflect ADR-0026: the dragon is now a hidden
  footer easter egg, and the hero holds only identity.