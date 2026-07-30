/* i18n.js — language toggle (EN/RU), light/dark theme, time-based greeting,
   curl one-liner text + copy. Persists choices in localStorage; cookie-free. */
(function () {
  "use strict";

  const STRINGS = {
    en: {
      greeting_morning: "Good morning —",
      greeting_afternoon: "Good afternoon —",
      greeting_evening: "Good evening —",
      lead: "Backend and infrastructure engineer who turns flaky systems into boring, dependable ones.",
      download: "Download résumé (PDF)",
      ai_resume: "Résumé for AI / LLM",
      copy: "Copy",
      share: "Share my dragon",
      share_li: "Share on LinkedIn ↗",
      share_li_aria: "Share on LinkedIn (opens in a new tab)",
      share_link_label: "Your dragon share link",
      dragon_line: "This is your little dragon — it's yours. Share the link so each colleague gets their own.",
      curl_label: "Or grab it from your terminal:",
      showqr: "Show QR",
      branded: "designed PDF",
      made: "Made by hand from markdown — not a template. The little dragon is yours.",
      footer: "Built from markdown · JSON Resume + llms.txt · a tiny dragon for the road.",
    },
    ru: {
      greeting_morning: "Доброе утро —",
      greeting_afternoon: "Добрый день —",
      greeting_evening: "Добрый вечер —",
      lead: "Бэкенд- и инфраструктурный инженер, превращающий нестабильные системы в скучно-надёжные.",
      download: "Скачать резюме (PDF)",
      ai_resume: "Резюме для AI / LLM",
      copy: "Копировать",
      share: "Поделиться дракончиком",
      share_li: "Поделиться в LinkedIn ↗",
      share_li_aria: "Поделиться в LinkedIn (откроется в новой вкладке)",
      share_link_label: "Ссылка на вашего дракона",
      dragon_line: "Это твой дракончик — он твой. Поделись ссылкой, и у каждого коллеги появится свой.",
      curl_label: "Или заберите из терминала:",
      showqr: "Показать QR",
      branded: "дизайн-PDF",
      made: "Сделано вручную из markdown — не шаблон. Дракончик — ваш.",
      footer: "Собрано из markdown · JSON Resume + llms.txt · маленький дракончик на удачу.",
    },
  };

  function pickInitialLang() {
    const saved = localStorage.getItem("lang");
    if (saved && STRINGS[saved]) return saved;
    return (navigator.language || "en").toLowerCase().startsWith("ru") ? "ru" : "en";
  }

  function greetingKey(lang) {
    const h = new Date().getHours();
    if (lang === "ru") return h < 12 ? "greeting_morning" : h < 18 ? "greeting_afternoon" : "greeting_evening";
    return h < 12 ? "greeting_morning" : h < 18 ? "greeting_afternoon" : "greeting_evening";
  }

  function applyLang(lang) {
    const s = STRINGS[lang];
    document.documentElement.lang = lang;
    document.documentElement.setAttribute("data-lang", lang);

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      let val = key === "greeting" ? s[greetingKey(lang)] : s[key];
      if (val !== undefined) el.textContent = val;
      if (key === "greeting") el.hidden = false;
    });

    // bilingual aria-labels (e.g. the dragon share-link input) follow the toggle
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const val = s[el.getAttribute("data-i18n-aria")];
      if (val !== undefined) el.setAttribute("aria-label", val);
    });

    document.querySelectorAll(".lang-block").forEach((b) => {
      b.hidden = b.getAttribute("data-lang") !== lang;
    });
    document.querySelectorAll(".lang-toggle button").forEach((b) => {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });

    // curl one-liner derived from current location (works on custom domain + project pages)
    const base = location.origin + location.pathname.replace(/[^/]*$/, "");
    const curl = document.getElementById("curl-line");
    if (curl) curl.textContent = `curl -sL ${base}resume.txt`;
    localStorage.setItem("lang", lang);
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    // keep Bootstrap's native dark/light components in sync with our toggle
    document.documentElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem("theme", theme);
  }

  function initTheme() {
    const saved = localStorage.getItem("theme");
    if (saved) return applyTheme(saved);
    const dark = window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(dark ? "dark" : "light");
  }

  // (ADR-0017 was reduced to a single Forest theme, so there is no palette
  // picker; light/dark is the only color axis. data-theme is set in initTheme.)

  function init() {
    initTheme();
    applyLang(pickInitialLang());

    document.querySelectorAll(".lang-toggle button").forEach((b) => {
      b.addEventListener("click", () => applyLang(b.getAttribute("data-lang")));
    });
    const themeBtn = document.querySelector(".theme-toggle");
    if (themeBtn) themeBtn.addEventListener("click", () => {
      applyTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });

    const copyBtn = document.querySelector(".copy-curl");
    if (copyBtn) copyBtn.addEventListener("click", () => {
      const line = document.getElementById("curl-line");
      if (line) {
        try { navigator.clipboard.writeText(line.textContent); }
        catch { /* clipboard may be blocked; ignore */ }
        const orig = copyBtn.textContent;
        copyBtn.textContent = "✓";
        setTimeout(() => { copyBtn.textContent = orig; }, 1200);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();