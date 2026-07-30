# ADR-0019 — Automated contrast + no-JS regression guards

Date: 2026-07-30 · Status: Accepted

## Context
ADR-0017 ships the theme (originally many palettes, now reduced to a single
Forest theme), and ADR-0018 the human feel. The `@a` review verified WCAG AA
contrast by hand, and the `@cr` review flagged that the no-JS
`prefers-color-scheme: dark` path is only statically guarded (Playwright runs
with JS on, so no-JS behavior was never exercised in a browser). Both were
called out as residual risks:

1. **Contrast was reviewer-verified, not machine-enforced.** A future color
   edit (a tweaked accent, a swapped background) could silently drop a pair
   below 4.5:1 and pass every existing test, because nothing computed ratios.
2. **The no-JS path was untested in a browser.** The static test only asserts
   the CSS *selector* is scoped to no-JS; it cannot prove the rendered page is
   forest-light by default or forest-dark under `prefers-color-scheme: dark`
   when JavaScript does not run.

## Decision
Add two regression guards that close those gaps without introducing a runtime
dependency or a new build tool:

1. **Automated WCAG contrast test** (`build/test_build.py`).
   - A small parser brace-matches `src/site.css` and extracts the theme's
     light and dark `--c-*` vars from the top-level `:root` (light) and
     `:root[data-theme="dark"]` (dark) blocks. Top-level only, so the
     `@media print :root` and the no-JS media `:root:not(…)` (both nested inside
     `@media`) are skipped — they are not the canonical theme definitions.
   - For each mode it computes sRGB relative-luminance contrast for seven
     pairs — body text/bg, muted/bg, accent/bg (link + greeting + skill text),
     **and the same three pairs against `--c-surface`** (because most text
     actually renders inside `.block { background: var(--c-surface) }`:
     summary, meta, role, contact links), plus filled-button text/accent
     (white in light, `#15171c` in dark) — and asserts each is ≥ 4.5:1
     (WCAG 2.1 AA for normal text; button text is not large/bold, so 4.5
     applies, not 3).
   - A companion test pins the button-text-color assumption (white light /
     `#15171c` dark) for the global rule, so the contrast guard's `BTN_FG`
     assumption holds and never silently tests the wrong foreground.
   - This runs in the pure-Python build suite — no Node, no browser, no extra
     dependency — so it executes on every CI build and every local `pytest`.

2. **No-JS Playwright tests** (`tests/ui/ui.spec.js`).
   - A `blockScripts` helper aborts every `resourceType === "script"` request.
     The page's executable JS lives entirely in external files
     (`dragon.js`, `share.js`, `i18n.js`), so aborting them is equivalent to JS
     being disabled; inline content is only JSON-LD (non-executable).
   - Three tests: (a) scripts blocked + light OS → `data-theme` stays `null`
     and the body background is the forest-light value, proving the bare
     `:root` default applies; (b) scripts blocked + dark OS → `data-theme`
     stays `null` and the background is the forest-dark value, proving the
     no-JS scoped media query applies forest dark; (c) the ◐ toggle is still
     present in the DOM (it is HTML) but clicking it does nothing without JS.

## Consequences
- A color edit that breaks AA contrast fails `pytest` immediately, with a
  message naming the mode, pair, and computed ratio — no re-review needed for
  routine color tweaks. The hand-computed table from the `@a` review remains
  the rationale, but the test is now the enforcement.
- The no-JS path is exercised in a real browser, so a regression that makes
  the dark media query over-apply (or stop applying) is caught, not just
  inferred from selector text.
- Both guards are deterministic and fast (the contrast test is pure Python; the
  no-JS tests add three short Playwright runs). Neither changes the shipped
  site — they are test-only.
- Limitation: the contrast test checks the seven pairs the design uses as text;
  it does not check `--c-accent-soft` (a background tint, not text) or
  decorative shadows. If a future component uses an accent-tint as *text*, a
  new pair must be added to the guard. The button-text-color test pins the one
  assumption the contrast guard depends on.
- Limitation: blocking scripts is a faithful no-JS simulation for *this* page
  because all executable JS is external; if inline executable `<script>` is
  ever added, the no-JS tests would need revisiting (they would still pass,
  but would no longer represent a truly scriptless render).