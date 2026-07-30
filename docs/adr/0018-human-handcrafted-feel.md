# ADR-0018 — Human, handcrafted feel

Date: 2026-07-30 · Status: Accepted

## Context
The site is technically correct and low-cognitive-load (ADR-0008), but a
clean, neutral, system-sans interface reads as a sterile template — the
opposite of what the owner wants. The explicit ask: the site should look
"maximally human, maybe a little naive," leaving the sense of a living, cool
person who stands behind it or could have built it. Recruiters and visitors
should feel a person, not a CMS.

## Decision
Keep the **structure** low-cognitive-load (one accent, two surfaces, generous
space, one primary CTA, clear hierarchy) and put the **personality** into
typography, warmth, and small handcrafted signals — warmth without clutter.

Concretely, applied globally across every ADR-0017 theme:

1. **JetBrains Mono display headings.** `h1`/`h2`/`h3` (and the greeting) use
   self-hosted **JetBrains Mono** (`--c-head-font: "JetBrains Mono", …,
   monospace`). A monospace display face for a résumé whose persona is
   literally "C0FFEE C0DER" reads as "this person lives in a terminal" — the
   strongest on-brand, human signal. It is **self-hosted** (woff2 in the repo,
   `@font-face` in `site.css` + `print.css`), so nothing is fetched from a CDN:
   the page stays offline-fast, and WeasyPrint embeds the same font in the
   branded PDF (paths resolve against its `base_url`, the repo root). If the
   woff2 ever fails to load, the stack falls back to the platform monospace.
2. **Warm paper default.** The calm palette uses warm paper neutrals
   (off-white `#f7f4ee` background, warm dark-brown text) rather than cold
   gray, so the page feels handmade even before a theme is chosen.
3. **Soft rounding + warm shadow.** `--radius: 16px` and a warm, low shadow
   (`rgba(70,50,20,.07)`) soften every surface; nothing is sharp/corporate.
4. **Handwritten-margin greeting.** The time-based greeting is set in serif
   *italic* in the accent color, like a note scribbled in a margin.
5. **The dragon is the personality anchor.** The seeded pixel dragon
   (ADR-0009) and the friendly bilingual dragon copy are the strongest
   "a real person made this" signal; this ADR keeps them central.
6. **Plain, friendly copy.** Footer/greeting/dragon copy is warm and
   first-person ("Made by hand from markdown — not a template"), never
   corporate filler.

## Consequences
- The site feels like a person across all ten themes; personality lives in
  typography, warmth, and the mascot rather than in extra components, so
  cognitive load does not rise.
- The self-hosted woff2 is a latin subset (~21 KB per weight, 400 + 700), so
  the cost is tiny and one-time; no CDN, no privacy leak, no offline break.
- JetBrains Mono is **OFL-1.1**; the license (`src/jetbrains-mono-LICENSE.txt`)
  is retained in the repo and shipped to `dist/assets/` alongside the woff2, and
  a build test asserts both are present, so the OFL "accompany redistribution"
  obligation is met and a future edit that drops it is caught.
- The branded PDF (`print.css`) loads the same JetBrains Mono via `@font-face`
  with ROOT-relative paths, so the printable artifact matches the on-screen
  voice. If the WeasyPrint build lacks woff2 support it falls back to the
  platform monospace — still monospace, still on-brand.
- "Naive" is deliberately bounded: rounded, warm, hand-written-margin
  accents, and friendly copy — **not** clip-art, animation, or irregular
  layout, which would raise cognitive load and hurt ATS/agent legibility.
- This ADR is a style rule, not a code constraint; the build/Playwright suites
  assert the serif-heading and warm-default tokens exist and render, so a
  refactor that silently drops them is caught.