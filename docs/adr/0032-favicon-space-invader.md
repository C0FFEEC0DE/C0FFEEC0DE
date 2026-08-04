# ADR-0032 — Favicon: red pixel Space Invader

Date: 2026-08-04 · Status: Accepted

## Context

The landing page previously shipped without a favicon. Browsers then show a
default blank document icon in tabs and bookmarks, which makes the site harder
to identify in a crowded tab bar and slightly weakens the "handcrafted" first
impression established by ADR-0018.

The owner wants the favicon to be a **red Space Invader** in a pixel-art style.
This continues the site's retro-gaming, handcrafted personality (the dragon is
already a pixel-art easter egg — ADR-0009/0026) without adding a new CDN request
or changing the page's visible UI.

## Decision

1. Add a self-hosted SVG favicon at `src/favicon.svg`.
   - The icon is a 32×32 pixel-art Space Invader rendered with `<rect>` blocks.
   - The invader is **red** (`#c62828`) on the same light Forest background
     (`#f4f6f2`) used by the page, so the tab icon is recognizable but does not
     clash with the Forest palette.
   - SVG is chosen over PNG so it stays crisp at any tab/bookmark size and is
     trivial to edit by hand in the repo.

2. Link the favicon in `src/index.html` with:
   ```html
   <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
   ```

3. The build copies `.svg` files from `src/` to `dist/assets/` alongside CSS, JS,
   and PNG assets, so no extra manual step is needed at deploy time.

## Consequences

- Every browser tab / bookmark for `krasnobai.dev` now shows a red Space Invader.
- No external request is added; the favicon is self-hosted and tiny (~1 KB SVG).
- The pixel-art invader fits the existing dragon/playful tone of the site.
- A Playwright test asserts the favicon link resolves with HTTP 200.
- Future favicon changes (color, shape) require editing `src/favicon.svg` only.

## Version history
- **v1 (2026-08-04):** add red pixel Space Invader SVG favicon, self-hosted in
  `assets/favicon.svg`, linked from `index.html`.
