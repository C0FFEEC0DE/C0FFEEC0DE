# UI tests (Playwright)

End-to-end UI tests for the landing page, run against the **built** `dist/`.
Playwright starts a local static server (`python3 -m http.server`) rooted at
the repo and serving `dist/`, then drives a real Chromium browser.

These cover the things the Python build tests cannot: that the rendered page
shows the name **once** (the duplication regression), that the EN/RU toggle
swaps both the hero header and the résumé body, that the pixel dragon renders
and is reproducible from `?d=`, and that share/QR, the curl one-liner, the
theme toggle, the PDF links, and the machine-readable endpoints all behave.

## Prerequisites

- Node.js 18+ and npm
- Python 3 with `pyyaml` (+ `weasyprint` for PDFs) — same as the build
- Playwright's Chromium browser (installed on first run)

## Run locally

From this directory:

```bash
npm install                 # one-time: fetch @playwright/test
npx playwright install --with-deps chromium   # one-time: fetch the browser
npm run test:full          # builds dist/ (python build) then runs all UI tests
# or, if dist/ is already built:
npm test
```

The Playwright config (`playwright.config.js`) sets `reuseExistingServer`
locally, so if something is already serving `dist/` on `:8000` it is reused.

## What is tested

| Spec | What it asserts |
|---|---|
| no duplicated blocks | exactly one visible `<h1>`; RU hero header hidden by default |
| English default | the EN label is shown, the RU label hidden |
| bilingual toggle | RU toggle swaps hero header **and** résumé body; one language at a time |
| aria-pressed | language buttons reflect the active language |
| dragon renders | the canvas has non-transparent pixels; `#dragon-id` shows the seed |
| seed reproducible | `?d=abc12345` shows `#abc12345` and is byte-identical on reload |
| share / QR | share reveals the Show-QR button; opening it makes `#qr` visible |
| curl one-liner | points at `resume.txt` and reflects the current origin |
| theme toggle | flips `data-theme` between `light` and `dark` |
| PDF links | `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` and `Aleksandr_Krasnobai_Staff_DevOps_Engineer_branded.pdf` resolve (200, `application/pdf`) |
| machine endpoints | `resume.json`, `resume.min.json`, `.well-known/cv.json` are served and valid |
| accessibility | skip-link target, single `<main>`, labelled language group |

## CI

`.github/workflows/playwright.yml` builds `dist/` and runs this suite on every
push/pull request to `main` (independent of the Pages deploy).