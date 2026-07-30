# ADR-0008 — Low-cognitive-load design as a first-class constraint

Date: 2026-07-30 · Status: Accepted

## Context
The user explicitly wants the site to impose minimal cognitive load on visitors.

## Decision
Constrain the design: single column, one first fold (name + label + summary +
one CTA + dragon), a calm two-surface palette with a single accent, light/dark
via `prefers-color-scheme` + toggle, no autoplay/flashing, generous whitespace,
scannable sections (chips for skills, lists for experience). All text/surface
pairs meet WCAG AA (4.5:1).

## Consequences
- The dragon is the only "delight" element, confined to the hero so it never
  competes with content.
- `prefers-reduced-motion` disables the gentle dragon bob.
- Contrast is verified at build time (see ADR-0012 notes / tests).