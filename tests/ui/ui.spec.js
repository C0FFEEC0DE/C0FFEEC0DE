// UI tests for the C0FFEEC0DE résumé landing page.
// Covers: the no-duplication fix, bilingual toggle, the dragon token,
// share/QR, curl one-liner, theme toggle, accessibility, and seed reproducibility.
const { test, expect } = require("@playwright/test");

test("page loads and shows the name exactly once (no duplicated blocks)", async ({ page }) => {
  await page.goto("/");
  // exactly one <h1> is visible — the EN hero header (the RU one is hidden)
  await expect(page.locator(".hero-text [data-lang='en'] h1")).toBeVisible();
  await expect(page.locator(".hero-text [data-lang='ru'] h1")).toBeHidden();
  const visibleH1 = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("h1")).filter(
      (h) => h.offsetParent !== null || h.getClientRects().length > 0,
    ).length;
  });
  expect(visibleH1).toBe(1);
});

test("default language is English with the English label", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".hero-text [data-lang='en'] .label")).toHaveText(
    "Senior DevOps / SRE Engineer",
  );
  await expect(page.locator(".hero-text [data-lang='ru'] .label")).toBeHidden();
});

test("EN/RU toggle swaps the hero header and résumé body, one language at a time", async ({ page }) => {
  await page.goto("/");
  // switch to RU
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(page.locator(".hero-text [data-lang='ru'] .label")).toContainText("SRE");
  await expect(page.locator(".hero-text [data-lang='en'] .label")).toBeHidden();
  // résumé body follows the same toggle (ADR-0025: the landing #resume block
  // shows Contact only — the full body lives in the branded PDF)
  await expect(page.locator("#resume [data-lang='ru']")).toBeVisible();
  await expect(page.locator("#resume [data-lang='en']")).toBeHidden();
  await expect(page.locator("#resume [data-lang='ru']")).toContainText("LinkedIn");
  // switch back to EN
  await page.click(".lang-toggle button[data-lang='en']");
  await expect(page.locator(".hero-text [data-lang='en'] .label")).toHaveText(
    "Senior DevOps / SRE Engineer",
  );
  await expect(page.locator("#resume [data-lang='en']")).toBeVisible();
  await expect(page.locator("#resume [data-lang='ru']")).toBeHidden();
});

test("language toggle buttons reflect aria-pressed correctly", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".lang-toggle button[data-lang='en']")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator(".lang-toggle button[data-lang='ru']")).toHaveAttribute("aria-pressed", "false");
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(page.locator(".lang-toggle button[data-lang='ru']")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator(".lang-toggle button[data-lang='en']")).toHaveAttribute("aria-pressed", "false");
});

test("the dragon renders pixels onto the canvas and shows a seed id", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#dragon-id")).toHaveText(/^#\w{4,}$/);
  const nonTransparent = await page.evaluate(() => {
    const c = document.getElementById("dragon");
    const ctx = c.getContext("2d");
    const d = ctx.getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 3; i < d.length; i += 4) if (d[i] > 0) n++;
    return n;
  });
  expect(nonTransparent).toBeGreaterThan(0);
});

test("the dragon is reproducible from a ?d= seed", async ({ page }) => {
  await page.goto("/?d=abc12345");
  await expect(page.locator("#dragon-id")).toHaveText("#abc12345");
  const gridA = await page.evaluate(() => {
    const c = document.getElementById("dragon");
    return c.getContext("2d").getImageData(0, 0, c.width, c.height).data.join(",");
  });
  // reload — same seed must produce the identical pixel buffer
  await page.goto("/?d=abc12345");
  const gridB = await page.evaluate(() => {
    const c = document.getElementById("dragon");
    return c.getContext("2d").getImageData(0, 0, c.width, c.height).data.join(",");
  });
  expect(gridA).toBe(gridB);
});

test("share button reveals the QR toggle, and the QR becomes visible", async ({ page }) => {
  await page.goto("/");
  // the Show QR button and the inline share link are hidden until the visitor shares
  await expect(page.locator(".qr-toggle")).toBeHidden();
  await expect(page.locator("#share-link")).toBeHidden();
  await page.click(".share-btn");
  await expect(page.locator(".qr-toggle")).toBeVisible();
  // ADR-0021: the share URL is revealed inline and carries the ?d= seed
  const link = page.locator("#share-link");
  await expect(link).toBeVisible();
  await expect(link).toHaveValue(/[?&]d=/);
  await expect(link).toHaveAttribute("aria-label", "Your dragon share link");
  // opening the QR makes the #qr box visible (img on success, fallback text on CDN failure)
  await page.click(".qr-toggle");
  await expect(page.locator("#qr")).toBeVisible();
});

test("share reveals a LinkedIn button pre-filled with the dragon URL", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#share-li")).toBeHidden();
  await page.click(".share-btn");
  const li = page.locator("#share-li");
  await expect(li).toBeVisible();
  const href = await li.getAttribute("href");
  const u = new URL(href);
  expect(u.origin + u.pathname).toBe("https://www.linkedin.com/sharing/share-offsite/");
  const target = u.searchParams.get("url");
  expect(target).toMatch(/[?&]d=/);
  await expect(li).toHaveAttribute("target", "_blank");
  await expect(li).toHaveAttribute("rel", /noopener/);
  await expect(li).toHaveAttribute("rel", /noreferrer/);
  // target="_blank" is announced to AT via a bilingual aria-label (data-i18n-aria)
  await expect(li).toHaveAttribute("aria-label", /new tab/);
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(li).toHaveAttribute("aria-label", /новой вкладке/);
});

test("the curl one-liner points at resume.txt and reflects the current origin", async ({ page }) => {
  await page.goto("/");
  const curl = await page.locator("#curl-line").textContent();
  expect(curl).toContain("curl -sL");
  expect(curl).toContain("resume.txt");
  expect(curl).toContain("localhost:8000");
});

test("theme toggle flips the data-theme attribute between light and dark", async ({ page }) => {
  await page.goto("/");
  const before = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  await page.click(".theme-toggle");
  const after = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  expect(["light", "dark"]).toContain(before);
  expect(["light", "dark"]).toContain(after);
  expect(after).not.toBe(before);
});

test("the PDF download links resolve (default ATS + branded)", async ({ page }) => {
  await page.goto("/");
  for (const href of ["resume.pdf", "resume-branded.pdf"]) {
    const res = await page.request.get(href);
    expect(res.status(), `${href} should be reachable`).toBe(200);
    expect((await res.headers())["content-type"] || "").toContain("pdf");
  }
});

test("machine-readable endpoints are served", async ({ page }) => {
  await page.goto("/");
  const json = await (await page.request.get("resume.json")).json();
  expect(json.basics.name).toBe("Aleksandr Krasnobai");
  expect(json.work.length).toBeGreaterThan(0);
  const min = await (await page.request.get("resume.min.json")).json();
  expect(min.name).toBe("Aleksandr Krasnobai");
  expect(min.availability.status).toBe("open");
  const cv = await (await page.request.get(".well-known/cv.json")).json();
  expect(cv.schema).toBe("cv.json");
});

test("skip-link and document structure are accessible", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".skip-link")).toHaveAttribute("href", "#resume");
  await expect(page.locator("#resume")).toHaveAttribute("id", "resume");
  // the page has exactly one <main> and a labelled language group
  await expect(page.locator("main")).toHaveCount(1);
  await expect(page.locator(".lang-toggle")).toHaveAttribute("role", "group");
});

test("hero has two audience links: human PDF + AI/LLM résumé", async ({ page }) => {
  await page.goto("/");
  const cta = page.locator(".hero-text .cta a");
  await expect(cta).toHaveCount(2);
  await expect(page.locator(".hero-text .cta a.btn-primary")).toHaveAttribute("href", "resume.pdf");
  await expect(page.locator(".hero-text .cta a.ai-link")).toHaveAttribute("href", "resume.json");
  // the branded PDF is not a hero button (it lives in the footer)
  const brandedInHero = await page.locator(".hero-text .cta a[href='resume-branded.pdf']").count();
  expect(brandedInHero).toBe(0);
});

test("the AI/LLM résumé link label is bilingual and resolves to valid JSON", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".hero-text .cta a.ai-link")).toContainText("Résumé for AI / LLM");
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(page.locator(".hero-text .cta a.ai-link")).toContainText("Резюме для AI / LLM");
  const res = await page.request.get("resume.json");
  expect(res.status()).toBe(200);
  const json = await res.json();
  expect(json.basics.name).toBe("Aleksandr Krasnobai");
});

test("there is no palette picker — Forest is the single theme", async ({ page }) => {
  await page.goto("/");
  // the picker was removed when ADR-0017 was reduced to one theme
  await expect(page.locator("#palette-select")).toHaveCount(0);
  await expect(page.locator(".palette-pick")).toHaveCount(0);
  // no data-palette attribute is ever set; the bare :root is Forest
  const pal = await page.evaluate(() => document.documentElement.getAttribute("data-palette"));
  expect(pal).toBeNull();
  const accent = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-accent").trim().toLowerCase(),
  );
  expect(accent).toBe("#2f7d3a"); // forest light accent
});

test("the light/dark toggle switches the Forest accent between its two values", async ({ page }) => {
  await page.addInitScript(() => { localStorage.setItem("theme", "light"); });
  await page.goto("/");
  const accentLight = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-accent").trim().toLowerCase(),
  );
  expect(accentLight).toBe("#2f7d3a"); // forest light accent
  await page.click(".theme-toggle");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  const accentDark = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-accent").trim().toLowerCase(),
  );
  // forest-dark accent is #7cc68a — assert the EXACT value so a light leak fails
  expect(accentDark).toBe("#7cc68a");
  expect(accentDark).not.toBe(accentLight);
});

test("headings use JetBrains Mono (ADR-0018 human/coder feel)", async ({ page }) => {
  await page.goto("/");
  const ff = await page.evaluate(() => getComputedStyle(document.querySelector("h1")).fontFamily);
  expect(ff.toLowerCase()).toMatch(/jetbrains|mono/);
});

test("the self-hosted JetBrains Mono woff2 is served from assets", async ({ page }) => {
  await page.goto("/");
  for (const w of ["jetbrains-mono-400.woff2", "jetbrains-mono-700.woff2"]) {
    const res = await page.request.get(`assets/${w}`);
    expect(res.status(), `${w} should be served`).toBe(200);
    expect((await res.headers())["content-type"] || "").toMatch(/font|octet/);
  }
});

test("printing forces a light palette even when a dark theme is active", async ({ page, context }) => {
  await page.addInitScript(() => { localStorage.setItem("theme", "dark"); });
  await page.goto("/");
  // on screen: forest dark text is light
  const screenText = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-text").trim().toLowerCase(),
  );
  expect(screenText).not.toBe("#1f2a1f");
  // under print media the !important light override kicks in (@cr print-leak fix)
  await page.emulateMedia({ media: "print" });
  const printText = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-text").trim().toLowerCase(),
  );
  expect(printText).toBe("#1f2a1f");
  await page.emulateMedia({ media: "screen" });
});

// ADR-0019: the no-JS path is browser-tested by blocking all script resources
// (the page's JS is entirely in external files), so data-theme is never set
// and the CSS no-JS rules are the only thing that applies.
async function blockScripts(page) {
  await page.route("**/*", (route) => {
    if (route.request().resourceType() === "script") route.abort();
    else route.continue();
  });
}

test("no-JS: forest light is the default when scripts are blocked (light OS)", async ({ page }) => {
  await blockScripts(page);
  await page.emulateMedia({ colorScheme: "light" });
  await page.goto("/");
  // no JS ran → data-theme is not set
  const dt = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  expect(dt).toBeNull();
  // the bare :root forest-light block applies → bg #f4f6f2 = rgb(244,246,242)
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  expect(bg.replace(/\s/g, "")).toBe("rgb(244,246,242)");
});

test("no-JS: prefers-color-scheme dark yields forest dark", async ({ page }) => {
  await blockScripts(page);
  await page.emulateMedia({ colorScheme: "dark" });
  await page.goto("/");
  // no JS → the no-JS scoped media query applies forest dark
  const dt = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  expect(dt).toBeNull();
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  // forest dark bg #131a14 = rgb(19,26,20)
  expect(bg.replace(/\s/g, "")).toBe("rgb(19,26,20)");
});

test("no-JS: the theme toggle is present but inert without JS", async ({ page }) => {
  await blockScripts(page);
  await page.goto("/");
  // the toggle is HTML, so it is in the DOM; clicking it cannot apply without JS
  await expect(page.locator(".theme-toggle")).toHaveCount(1);
  await page.click(".theme-toggle");
  const dt = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  expect(dt).toBeNull();
});

test("no-JS: the LinkedIn share anchor is hidden and has no href", async ({ page }) => {
  blockScripts(page);
  await page.goto("/");
  // ADR-0022: with JS off, share.js never sets href and never un-hides the anchor,
  // so there is no broken/empty link in the no-JS render.
  const li = page.locator("#share-li");
  await expect(li).toBeHidden();
  expect(await li.getAttribute("href")).toBeNull();
});