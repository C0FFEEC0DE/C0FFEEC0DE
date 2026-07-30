// Playwright config for the C0FFEEC0DE résumé landing page.
// The tests run against the built dist/ — Playwright starts a static server
// (python http.server) rooted at the repo, serving dist/. Build dist first:
//   npm run build   (or: python3 build/build.py --check)
//   npx playwright test
const path = require("path");
const { defineConfig } = require("@playwright/test");

const repoRoot = path.resolve(__dirname, "..", "..");

module.exports = defineConfig({
  testDir: ".",
  fullyParallel: false,        // single browser, one page — keep it simple
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: process.env.CI
    ? [["github"], ["html", { open: "never" }]]
    : "list",
  use: {
    baseURL: "http://localhost:8000",
    headless: true,
    screenshot: "only-on-failure",
    trace: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { browserName: "chromium" } },
  ],
  webServer: {
    // build.py resolves paths from __file__, so it always writes <repo>/dist
    // regardless of cwd. Serve that directory on a free port.
    command: "python3 -m http.server 8000 --directory dist",
    cwd: repoRoot,
    url: "http://localhost:8000",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});