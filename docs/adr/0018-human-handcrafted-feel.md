# ADR-0018 — Human, handcrafted feel

Date: 2026-07-30 · Status: Accepted

## Context
The site is technically correct and low-cognitive-load (ADR-0008), but a
clean, neutral, system-sans interface reads as a sterile template — the
opposite of what the owner wants. The explicit ask: the site should look
"maximally human, maybe a little naive," leaving the sense of a living, cool
person who stands behind it or could have built it. Recruiters and visitors
should feel a person, not a CMS.

For the minimal business-card redesign the owner chose to keep the warmth and
the small handcrafted signals, but to move the typography to a **system
sans-serif**. A monospace display face, while on-brand for the owner's GitHub handle,
added visual noise to a page whose sole job is to hand a recruiter a
name, a role, and a PDF. The human feel is now conveyed by color, copy, rounded
surfaces, and a hidden dragon easter egg (ADR-0026) rather than by a display
font.

## Decision
Keep the **structure** low-cognitive-load (one accent, two surfaces, generous
space, one primary CTA, clear hierarchy) and put the **personality** into color,
warmth, friendly copy, and small handcrafted signals — warmth without clutter.

Concretely, applied globally across the single Forest theme (ADR-0017 v4):

1. **System sans-serif typography.** Headings, body, and UI text all use the
   system sans-serif stack (`-apple-system`, `"Segoe UI"`, `Roboto`,
   `"Helvetica Neue"`, `Arial`, sans-serif). No self-hosted display font, no
   `@font-face` weight, no extra HTTP weight. The page loads instantly and
   matches the visitor's OS, which is itself a low-friction, human-friendly
   choice.
2. **Warm paper default.** The Forest palette uses warm paper neutrals
   (off-white `#f4f6f2` background, warm dark-green text) rather than cold gray,
   so the page feels handmade rather than corporate.
3. **Soft rounding + warm shadow.** `--radius: 16px` and a warm, low shadow
   (`rgba(20, 40, 20, .07)`) soften every surface; nothing is sharp/corporate.
4. **Handwritten-margin greeting.** The time-based greeting is set in *italic*
   in the accent color, like a note scribbled in a margin.
5. **The dragon is a hidden personality anchor.** The seeded pixel dragon
   (ADR-0009) is no longer front-and-center; it is a small easter egg
   (ADR-0026). The friendly dragon copy and share mechanic are preserved for
   anyone who discovers it, keeping the "a real person made this" signal alive
   without cluttering the business card.
6. **Plain, friendly copy.** Footer/greeting/dragon copy is warm and
   first-person ("Made by hand from markdown — not a template"), never
   corporate filler.

## Consequences
- The site still feels like a person; personality now lives in color, copy,
  rounding, and the hidden dragon rather than in a display typeface, so
  cognitive load does not rise.
- No font files are fetched or self-hosted, removing a network/weight concern
  and the OFL redistribution obligation entirely.
- The branded PDF (`print.css`) uses the same system sans-serif stack, so the
  printable artifact matches the live page's voice.
- "Naive" is deliberately bounded: rounded, warm, hand-written-margin
  accents, friendly copy, and a hidden mascot — **not** clip-art, animation,
  or irregular layout, which would raise cognitive load and hurt ATS/agent
  legibility.
- This ADR is a style rule, not a code constraint; the build/Playwright suites
  assert the warm Forest tokens and the hidden dragon behavior render correctly,
  so a refactor that silently drops them is caught.

## Revision history
- **v2 (current):** system sans-serif replaces JetBrains Mono for the minimal
  business-card redesign; dragon moved to hidden easter egg (ADR-0026).
- **v1:** JetBrains Mono display headings + self-hosted woff2 across all
  themes; dragon kept central in the hero.
