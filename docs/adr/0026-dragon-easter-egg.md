# ADR-0026 — Dragon as a hidden easter egg

Date: 2026-07-31 · Status: Accepted

## Context
ADR-0009 introduced a seeded, shareable pixel-art dragon as the page's personality anchor. The owner wants the new landing page to be an extremely minimal business card, so the dragon can no longer dominate the hero. At the same time, the seeding/sharing mechanic is still valuable as a viral, human touch — it should be preserved, just not visible by default.

## Decision
Hide the dragon behind a small easter egg. The default render of the landing page shows **no dragon, no share box, no QR**. The dragon canvas and its share controls live in the DOM but are hidden (`hidden` attribute + CSS) until the visitor triggers the easter egg.

Trigger: click the footer "handmade" note (the small crafted-by-hand line). This keeps the reveal mechanism on-brand with the human/handcrafted story and avoids adding any extra UI chrome to the business card.

Implementation:
- `src/index.html` keeps the dragon markup inside a hidden container.
- `src/site.css` styles the container as hidden by default and provides the revealed state.
- `src/i18n.js` attaches a click listener to the `.made` element that removes `hidden` from the dragon container and runs the normal dragon init path.
- `src/dragon.js` and `src/share.js` are still loaded so the same seeding (`?d=`) and sharing behavior works once the dragon is revealed.

## Consequences
- The landing page is visually a pure business card, satisfying the minimal-scope decision.
- The dragon remains a shareable, seeded easter egg — visitors who discover it still get their own dragon and a shareable URL.
- Playwright tests must assert the dragon is hidden by default and becomes visible after the easter-egg trigger is clicked.
- The no-JS path degrades to "no dragon visible, no broken links" (the hidden container stays hidden and the share anchor has no `href` until JS reveals it).
