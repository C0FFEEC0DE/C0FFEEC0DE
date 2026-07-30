# ADR-0021 — Dragon share link revealed inline

Date: 2026-07-30 · Status: Accepted

## Context

ADR-0009 made the dragon deterministic from a URL seed (`?d=…`) so the same
link reproduces the same dragon — the seed *is* the share token. `src/share.js`
wires the "Share my dragon" button to copy that URL to the clipboard and reveal
a "Show QR" toggle; the QR (ADR-0010, lazy + SRI-locked) is the scan-to-share
path.

The gap: **the link itself is never shown.** The visitor must trust that the
clipboard write succeeded and cannot see, select, verify, or manually copy the
URL they are sharing. If `navigator.clipboard.writeText` is blocked (common in
non-secure contexts, sandboxed iframes, or older browsers) the fallback
`execCommand("copy")` can also fail silently — leaving the visitor with nothing
to share. The owner asked for the dragon link to be **expanded into a visible
link on button press** so it is concretely shareable, not just invisibly copied.

## Decision

On "Share my dragon" press, **reveal the share URL inline** in addition to the
existing clipboard copy and QR-toggle reveal. Concretely:

- A readonly `<input class="share-link" id="share-link">` lives in the dragon
  `.share-box`, `hidden` until the first share press.
- `share.js` sets its `value` to `shareUrl(seed)` (the same `?d=…` URL from
  ADR-0009), un-hides it, and calls `.select()` so the URL is immediately
  copyable with Ctrl/Cmd-C even if the clipboard write failed.
- The input carries a bilingual `aria-label` ("Your dragon share link" /
  "Ссылка на вашего дракона") via a new `data-i18n-aria` attribute, so the
  revealed link is accessible in both languages.

No backend, no tracking, no third-party share SDK — only the existing `?d=…`
URL, now visible. The QR remains the scan path; the clipboard copy remains the
one-tap path; the inline input is the visible/selectable/fallback path. Three
ways to leave with the same link, all client-side.

## Consequences

- The visitor sees the exact link they are sharing; a silent clipboard failure
  no longer leaves them empty (the URL is on screen, pre-selected).
- Low cognitive load (ADR-0008) is preserved: the link is hidden until the
  visitor asks to share, so the resting dragon box is unchanged; when revealed
  it is one small monospace line under the button, not a new card.
- The no-JS path is unchanged: with JS off the button has no listener, so the
  input stays `hidden` (same as the QR toggle). The `[hidden]{display:none}`
  rule (site.css) keeps it off-screen.
- A small, reusable `data-i18n-aria` handling is added to `i18n.js`'s
  `applyLang` (set `aria-label` from `STRINGS[key]`), so future bilingual
  aria-labels follow the language toggle without bespoke code. A Playwright
  test asserts the link is revealed and contains the `?d=` URL on button press.
- ADR-0009 (seed = share token) and ADR-0010 (lazy QR) are unchanged; this ADR
  only adds a visible rendering of the link ADR-0009 already produces.

## Revision history
- **v1 (current):** reveal the dragon share URL inline (readonly input) on
  "Share my dragon" press; add `data-i18n-aria` for its bilingual label.