# ADR-0009 — Procedural pixel-art dragon, seeded from the URL

Date: 2026-07-30 · Status: Accepted

## Context
A small, shareable, mood-lifting mascot gives the page viral potential. It must
work on a static host (no backend) and be reproducible on a shared link.

## Decision
Generate a 16×16 pixel-art dragon entirely client-side: hash the seed string
→ `mulberry32` PRNG → pick palette + parts (body, eyes, wings, horns, accessory)
→ draw shapes onto a 16×16 grid → `<canvas>`. The seed is the `?d=` query param,
persisted in `localStorage`; same seed ⇒ same dragon.

## Consequences
- Sharing the URL shares *your* dragon — the viral loop.
- No tracking, no backend, fully offline (the dragon itself has no CDN).
- The sprite is intentionally simple; the PRNG gives wide variety without art
  assets.