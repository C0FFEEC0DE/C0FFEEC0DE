// UI tests for the C0FFEEC0DE résumé landing page.
// Covers: minimal business-card layout, bilingual toggle, hidden dragon easter
// egg, share link, LinkedIn share, save-dragon token, Open Graph tags,
// accessibility, and seed reproducibility.
const { test, expect } = require("@playwright/test");

test("page loads and shows the name exactly once (no duplicated blocks)", async ({ page }) => {
  await page.goto("/");
  // exactly one <h1> is visible — the EN hero header (the RU one is hidden)
  await expect(page.locator(".hero [data-lang='en'] h1")).toBeVisible();
  await expect(page.locator(".hero [data-lang='ru'] h1")).toBeHidden();
  const visibleH1 = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("h1")).filter(
      (h) => h.offsetParent !== null || h.getClientRects().length > 0,
    ).length;
  });
  expect(visibleH1).toBe(1);
});

test("default language is English with role and location tags", async ({ page }) => {
  await page.goto("/");
  const enTags = page.locator(".hero [data-lang='en'] .tags");
  await expect(enTags).toContainText("Staff DevOps Engineer");
  await expect(enTags).toContainText("Belgrade, Serbia — work authorized");
  await expect(page.locator(".hero [data-lang='ru'] .tags")).toBeHidden();
});

test("EN/RU toggle swaps the hero header and contact row, one language at a time", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".hero [data-lang='en'] .lead")).toContainText("high-throughput platforms");
  // switch to RU
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(page.locator(".hero [data-lang='ru'] .tags")).toContainText("DevOps");
  await expect(page.locator(".hero [data-lang='ru'] .tags")).toContainText("Белград, Сербия — право на работу");
  await expect(page.locator(".hero [data-lang='en'] .tags")).toBeHidden();
  // contact row follows the same toggle
  await expect(page.locator("#resume [data-lang='ru']")).toBeVisible();
  await expect(page.locator("#resume [data-lang='en']")).toBeHidden();
  await expect(page.locator("#resume [data-lang='ru']")).toContainText("LinkedIn");
  await expect(page.locator("#resume [data-lang='ru']")).toContainText("Telegram");
  // switch back to EN
  await page.click(".lang-toggle button[data-lang='en']");
  await expect(page.locator(".hero [data-lang='en'] .tags")).toContainText("Staff DevOps Engineer");
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

test("the dragon is hidden by default and revealed by clicking the footer note", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#dragon-box")).toBeHidden();
  await page.click(".made");
  await expect(page.locator("#dragon-box")).toBeVisible();
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

test("the dragon is reproducible from a ?d= seed after reveal", async ({ page }) => {
  await page.goto("/?d=abc12345");
  await page.click(".made");
  await expect(page.locator("#dragon-id")).toHaveText("#abc12345");
  const gridA = await page.evaluate(() => {
    const c = document.getElementById("dragon");
    return c.getContext("2d").getImageData(0, 0, c.width, c.height).data.join(",");
  });
  // reload — same seed must produce the identical pixel buffer
  await page.goto("/?d=abc12345");
  await page.click(".made");
  const gridB = await page.evaluate(() => {
    const c = document.getElementById("dragon");
    return c.getContext("2d").getImageData(0, 0, c.width, c.height).data.join(",");
  });
  expect(gridA).toBe(gridB);
});

test("share button reveals the inline share link and LinkedIn + save buttons", async ({ page }) => {
  await page.goto("/");
  await page.click(".made");
  // the inline share link is hidden until the visitor shares
  await expect(page.locator("#share-link")).toBeHidden();
  await page.click(".share-btn");
  // the share URL is revealed inline and carries the ?d= seed
  const link = page.locator("#share-link");
  await expect(link).toBeVisible();
  await expect(link).toHaveValue(/[?&]d=/);
  await expect(link).toHaveAttribute("aria-label", "Your dragon share link");
  // no QR toggle is present
  await expect(page.locator(".qr-toggle")).toHaveCount(0);
  await expect(page.locator("#qr")).toHaveCount(0);
});

test("share reveals LinkedIn and save-dragon buttons pre-filled with the dragon URL", async ({ page }) => {
  await page.goto("/");
  await page.click(".made");
  await expect(page.locator("#share-li")).toBeHidden();
  await expect(page.locator("#save-dragon")).toBeHidden();
  await page.click(".share-btn");
  const li = page.locator("#share-li");
  const save = page.locator("#save-dragon");
  await expect(li).toBeVisible();
  await expect(save).toBeVisible();
  const href = await li.getAttribute("href");
  const u = new URL(href);
  expect(u.origin + u.pathname).toBe("https://www.linkedin.com/sharing/share-offsite/");
  const target = u.searchParams.get("url");
  expect(target).toMatch(/[?&]d=/);
  await expect(li).toHaveAttribute("target", "_blank");
  await expect(li).toHaveAttribute("rel", /noopener/);
  await expect(li).toHaveAttribute("rel", /noreferrer/);
  await expect(li).toHaveAttribute("aria-label", /new tab/);
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(li).toHaveAttribute("aria-label", /новой вкладке/);
});

test("save-dragon button downloads a token PNG named after the seed", async ({ page }) => {
  await page.goto("/");
  await page.click(".made");
  await page.click(".share-btn");
  await expect(page.locator("#save-dragon")).toBeVisible();

  const [download] = await Promise.all([
    page.waitForEvent("download"),
    page.click("#save-dragon"),
  ]);
  expect(download.suggestedFilename()).toMatch(/^dragon-[a-z0-9]+\.png$/);
});

test("the page is fixed light Forest and has no theme toggle", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".theme-toggle")).toHaveCount(0);
  const theme = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  expect(theme).toBeNull();
  const accent = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-accent").trim().toLowerCase(),
  );
  expect(accent).toBe("#2f7d3a");
});

test("the single PDF download link resolves", async ({ page }) => {
  await page.goto("/");
  const href = "Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf";
  const res = await page.request.get(href);
  expect(res.status(), `${href} should be reachable`).toBe(200);
  expect((await res.headers())["content-type"] || "").toContain("pdf");
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
  expect(cv.human_pdf).toBe(cv.ats_pdf);
  const agentsMd = await page.request.get("resume-for-agents.md");
  expect(agentsMd.status()).toBe(200);
  expect(await agentsMd.text()).toContain("Aleksandr Krasnobai");
  const agentsJson = await (await page.request.get("agents.json")).json();
  expect(agentsJson.schema).toBe("agents.json");
});

test("Open Graph meta tags use the résumé name, role, and summary", async ({ page }) => {
  await page.goto("/");
  const title = await page.locator("meta[property='og:title']").getAttribute("content");
  expect(title).toContain("Aleksandr Krasnobai");
  expect(title).toContain("Staff DevOps Engineer");
  const desc = await page.locator("meta[property='og:description']").getAttribute("content");
  expect(desc).toContain("high-throughput platforms");
  const img = await page.locator("meta[property='og:image']").getAttribute("content");
  expect(img).toMatch(/dragon-og\.png$/);
  const res = await page.request.get(img);
  expect(res.status()).toBe(200);
  expect((await res.headers())["content-type"] || "").toContain("png");
});

test("red anarchy symbol favicon is linked and served", async ({ page }) => {
  await page.goto("/");
  const link = page.locator("link[rel='icon']");
  await expect(link).toHaveAttribute("type", "image/svg+xml");
  await expect(link).toHaveAttribute("href", "assets/favicon.svg");
  const res = await page.request.get("assets/favicon.svg");
  expect(res.status()).toBe(200);
  expect((await res.headers())["content-type"] || "").toContain("svg");
  const svg = await res.text();
  expect(svg).toContain("#c62828");
  expect(svg).toContain("<rect");
});

test("skip-link and document structure are accessible", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".skip-link")).toHaveAttribute("href", "#main");
  await expect(page.locator("#main")).toHaveAttribute("id", "main");
  await expect(page.locator("#resume")).toHaveAttribute("id", "resume");
  await expect(page.locator("main #resume")).toHaveCount(1);
  await expect(page.locator("main")).toHaveCount(1);
  await expect(page.locator(".lang-toggle")).toHaveAttribute("role", "group");
});

test("mobile: single-column business card layout", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const hero = await page.locator(".hero").boundingBox();
  const contact = await page.locator("#resume").boundingBox();
  const cta = await page.locator(".cta-section").boundingBox();
  expect(hero).not.toBeNull();
  expect(contact).not.toBeNull();
  expect(cta).not.toBeNull();
  // vertical reading order: hero → contact → CTA
  expect(contact.y).toBeGreaterThanOrEqual(hero.y + hero.height - 2);
  expect(cta.y).toBeGreaterThanOrEqual(contact.y + contact.height - 2);
  // identity uses most of the viewport width
  expect(hero.width).toBeGreaterThan(300);
});

test("footer machine formats are a semantic list with eight links and no extra text", async ({ page }) => {
  await page.goto("/");
  const items = page.locator(".machine-links li");
  await expect(items).toHaveCount(8);
  const hrefs = await page.locator(".machine-links a").evaluateAll((els) => els.map((a) => a.getAttribute("href")));
  expect(hrefs).toEqual([
    "resume.json",
    "resume.min.json",
    "resume-for-agents.md",
    "resume.txt",
    "Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf",
    "llms.txt",
    "AGENTS.md",
    "https://github.com/C0FFEEC0DE",
  ]);
  for (const href of hrefs) {
    const res = await page.request.get(href);
    expect(res.status(), `${href} should be reachable from machine-links`).toBe(200);
  }
  // the verbose footer line and "Machine-readable versions" heading were removed
  const footer = page.locator("footer");
  await expect(footer).not.toContainText("Built from markdown");
  await expect(footer).not.toContainText("Machine-readable versions");
  await expect(page.locator("footer .curl")).toHaveCount(0);
});

test("hero has one primary CTA: download PDF", async ({ page }) => {
  await page.goto("/");
  const cta = page.locator(".cta-section a");
  await expect(cta).toHaveCount(1);
  await expect(page.locator(".cta-section a.btn-primary")).toHaveAttribute(
    "href",
    "Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf",
  );
  await expect(page.locator(".cta-section a")).toContainText("Download résumé (PDF)");
  await page.click(".lang-toggle button[data-lang='ru']");
  await expect(page.locator(".cta-section a")).toContainText("Скачать резюме (PDF)");
});

test("there is no palette picker — Forest is the single fixed theme", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#palette-select")).toHaveCount(0);
  await expect(page.locator(".palette-pick")).toHaveCount(0);
  const pal = await page.evaluate(() => document.documentElement.getAttribute("data-palette"));
  expect(pal).toBeNull();
  const accent = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-accent").trim().toLowerCase(),
  );
  expect(accent).toBe("#2f7d3a");
});

test("headings use system sans-serif (ADR-0018 v2)", async ({ page }) => {
  await page.goto("/");
  const ff = await page.evaluate(() => getComputedStyle(document.querySelector("h1")).fontFamily);
  expect(ff.toLowerCase()).toMatch(/segoe|roboto|helvetica|arial|system-ui|-apple-system/);
  expect(ff.toLowerCase()).not.toMatch(/jetbrains/);
});

test("printing keeps a light palette", async ({ page, context }) => {
  await page.goto("/");
  await page.emulateMedia({ media: "print" });
  const printText = await page.evaluate(
    () => getComputedStyle(document.documentElement).getPropertyValue("--c-text").trim().toLowerCase(),
  );
  expect(printText).toBe("#1f2a1f");
  await page.emulateMedia({ media: "screen" });
});

// ADR-0019: the no-JS path is browser-tested by blocking all script resources
// (the page's JS is entirely in external files), so data-theme is never set
// and the CSS bare :root light block is the only thing that applies.
async function blockScripts(page) {
  await page.route("**/*", (route) => {
    if (route.request().resourceType() === "script") route.abort();
    else route.continue();
  });
}

test("no-JS: forest light is the default when scripts are blocked", async ({ page }) => {
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

test("no-JS: prefers-color-scheme dark is ignored (fixed light theme)", async ({ page }) => {
  await blockScripts(page);
  await page.emulateMedia({ colorScheme: "dark" });
  await page.goto("/");
  const dt = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
  expect(dt).toBeNull();
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  expect(bg.replace(/\s/g, "")).toBe("rgb(244,246,242)");
});

test("no-JS: the LinkedIn share anchor is hidden and has no href", async ({ page }) => {
  blockScripts(page);
  await page.goto("/");
  const li = page.locator("#share-li");
  await expect(li).toBeHidden();
  expect(await li.getAttribute("href")).toBeNull();
});
