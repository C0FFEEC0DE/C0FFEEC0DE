# ADR-0027 — Save dragon as a token PNG

Date: 2026-07-31 · Status: Accepted

## Context

ADR-0009 made the dragon deterministic from a URL seed, and ADR-0021 made that
URL visible and selectable. Visitors can already copy the link or show a QR
code, but there is no way to keep the dragon as an image. The owner wanted a
small, on-brand way to download the current dragon as a collectible token,
without adding backend complexity or changing the live canvas.

## Decision

Add a **"Save my dragon"** button to the dragon share box.

- The button is hidden until the visitor reveals the dragon (ADR-0026) and
  presses "Share my dragon" (ADR-0021), keeping the resting UI minimal.
- On click, `src/share.js` creates a temporary canvas and calls
  `window.DRAGON.drawToken(canvas, seed, "have a nice day")`. `drawToken`
  renders the same 16×16 pixel dragon from the live canvas onto a larger,
  token-sized canvas with a white card background, a colored border, and the
  caption at the bottom.
- The caption is added **only to the downloaded PNG**, not to the live dragon
  canvas. This keeps the on-page pixel art unchanged while giving the saved file
  a polite, collectible feel.
- The caption is **English-only** by request. The landing page's primary
  language is English, and a short universal phrase keeps the token simple and
  avoids layout concerns with longer localized strings.
- Generation is entirely **client-side** using the existing `canvas` element and
  `toDataURL("image/png")`. No backend, no external image service, no tracking —
  consistent with the no-backend design of ADR-0009.
- The browser download is triggered by a temporary `<a download>` element with
  filename `dragon-{seed}.png`, named after the seed so the saved token can be
  matched back to its URL.

## Consequences

- Visitors can keep a tangible, shareable image of their dragon in addition to
  the shareable URL.
- No extra privacy or network risk: the token is drawn from the same offline
  pixel data already on the page.
- The live dragon canvas and the token canvas are separate, so the on-page
  rendering stays pixel-perfect and unchanged.
- A Playwright test asserts that clicking "Save my dragon" triggers a download
  whose suggested filename matches `dragon-[a-z0-9]+.png`.
- ADR-0009 (seed = dragon identity) and ADR-0021 (visible share link) are
  unchanged; this ADR only adds a new download rendering path.

## Revision history
- **v1 (2026-07-31):** add a client-side "Save my dragon" button that downloads
  a token PNG with the dragon + English "have a nice day" caption.
