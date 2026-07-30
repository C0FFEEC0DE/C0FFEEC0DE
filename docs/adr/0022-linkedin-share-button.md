# ADR-0022 — LinkedIn share button (pre-filled link)

Date: 2026-07-30 · Status: Accepted

## Context

ADR-0009 made the dragon deterministic from a URL seed (`?d=…`) so the same
link reproduces the same dragon — the seed *is* the share token. ADR-0021 added
the inline visible share link (clipboard + selectable input + QR) so the
visitor can leave with the link three ways. The owner asked for one more,
lower-friction path: open LinkedIn's composer with the dragon link already
pasted in, so the only step left is to press **Publish** ("Опубликовать").

LinkedIn provides a documented share endpoint that does exactly this:
`https://www.linkedin.com/sharing/share-offsite/?url={url}`. Only the `url`
parameter is supported (LinkedIn dropped `title`/`summary`/`source` years ago),
and the target URL must be HTTPS (the production site is). The page preview in
the post is built by LinkedIn from the shared page's Open Graph / meta tags,
not from URL parameters.

## Decision

Add a **"Share on LinkedIn"** anchor to the dragon `.share-box`, revealed on
"Share my dragon" press (same reveal moment as the ADR-0021 inline link and QR
toggle), so the resting dragon box keeps its low cognitive load (ADR-0008).

Concretely:

- An `<a class="share-li" id="share-li" target="_blank" rel="noopener noreferrer" hidden data-i18n="share_li">`
  lives in `.share-box`, `hidden` until the first share press.
- `share.js` sets its `href` on init to
  `https://www.linkedin.com/sharing/share-offsite/?url=` + the
  `encodeURIComponent`-encoded `shareUrl(seed)` (the same `?d=…` URL from
  ADR-0009), and un-hides it in the "Share my dragon" click handler.
- The label is bilingual via the existing `data-i18n` path: EN "Share on
  LinkedIn" / RU "Поделиться в LinkedIn".
- `target="_blank"` + `rel="noopener noreferrer"` so LinkedIn opens in a new
  tab without a `window.opener` reference back to the résumé page.

No backend, no LinkedIn SDK, no tracking, no third-party script — only a link
to LinkedIn's own share endpoint, built client-side from the existing seed.
The clipboard copy, the inline input, and the QR all remain (ADR-0021
unchanged); this adds a fourth, channel-specific path for visitors who want to
post the dragon straight to LinkedIn.

## Consequences

- One click on "Share on LinkedIn" opens LinkedIn's composer with the dragon
  link pre-filled; the visitor only adds an optional message and publishes.
- Low cognitive load (ADR-0008) is preserved: the button is `hidden` until the
  visitor presses "Share my dragon", so the resting dragon box is unchanged.
- The no-JS path is unchanged: with JS off the anchor has no `href` set and
  stays `hidden` (`[hidden]{display:none!important}`), so there is no broken
  or empty link in the no-JS render. A no-JS Playwright test asserts the anchor
  is `hidden` and has no `href` with scripts blocked.
- `target="_blank"` is announced to assistive tech via a bilingual `aria-label`
  (`data-i18n-aria="share_li_aria"`, the second use of the ADR-0021 path) ending
  "(opens in a new tab)" / "(откроется в новой вкладке)", plus a visible ↗ cue
  on the button text. `rel="noopener noreferrer"` guards both reverse tabnabbing
  and referer leakage; a Playwright test asserts both tokens and that the
  aria-label follows the EN/RU toggle.
- The shared page's LinkedIn preview card depends on Open Graph / meta tags on
  the shared page, not on this button. The page currently exposes `<title>`
  and a meta description only; richer `og:` tags (and a static `og:image`, since
  the dragon is canvas-rendered and cannot serve as one) are a future
  enhancement, not part of this ADR.
- ADR-0009 (seed = share token), ADR-0010 (lazy QR), and ADR-0021 (inline link)
  are unchanged; this ADR only adds a channel-specific link to the URL they
  already produce. A Playwright test asserts the button is hidden before share,
  visible after, and that its `href` decodes to the LinkedIn share endpoint
  carrying the `?d=` URL with `target="_blank"`.

## Revision history
- **v1 (current):** add a hidden "Share on LinkedIn" anchor revealed on share
  press; `share.js` pre-fills its href with the encoded dragon URL.