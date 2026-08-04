/* i18n.js — language toggle (EN/RU), time-based greeting, curl one-liner text +
   copy, and the hidden dragon easter-egg reveal. Persists only the language
   choice in localStorage; cookie-free. The theme is fixed light Forest
   (ADR-0017 v4), so there is no theme code here. */
(function () {
  "use strict";

  const STRINGS = {
    en: {
      greeting_morning: "Good morning —",
      greeting_afternoon: "Good afternoon —",
      greeting_evening: "Good evening —",
      download: "Download résumé (PDF)",
      github: "View GitHub",
      machine: "Machine-readable résumé",
      copy: "Copy",
      share: "Share my dragon",
      share_li: "Share on LinkedIn ↗",
      share_li_aria: "Share on LinkedIn (opens in a new tab)",
      save_dragon: "Save my dragon",
      share_link_label: "Your dragon share link",
      dragon_line: "This is your little dragon — it's yours. Share the link so each colleague gets their own.",
      branded: "designed PDF",
      made: "Built from Markdown. A little dragon is hiding nearby.",
    },
    ru: {
      greeting_morning: "Доброе утро —",
      greeting_afternoon: "Добрый день —",
      greeting_evening: "Добрый вечер —",
      download: "Скачать резюме (PDF)",
      github: "Открыть GitHub",
      machine: "Машиночитаемое резюме",
      copy: "Копировать",
      share: "Поделиться дракончиком",
      share_li: "Поделиться в LinkedIn ↗",
      share_li_aria: "Поделиться в LinkedIn (откроется в новой вкладке)",
      save_dragon: "Сохранить дракончика",
      share_link_label: "Ссылка на вашего дракона",
      dragon_line: "Это твой дракончик — он твой. Поделись ссылкой, и у каждого коллеги появится свой.",
      branded: "дизайн-PDF",
      made: "Собрано из Markdown. Где-то рядом спрятался дракончик.",
    },
  };

  function pickInitialLang() {
    const requested = new URLSearchParams(location.search).get("lang");
    if (requested && STRINGS[requested]) return requested;
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

    const url = new URL(location.href);
    if (lang === "ru") url.searchParams.set("lang", "ru");
    else url.searchParams.delete("lang");
    history.replaceState(null, "", url.pathname + url.search + url.hash);

    const base = location.origin + location.pathname.replace(/[^/]*$/, "");
    const curl = document.getElementById("curl-line");
    if (curl) curl.textContent = `curl -sL ${base}resume.txt`;
    localStorage.setItem("lang", lang);
  }

  function revealDragon() {
    const box = document.getElementById("dragon-box");
    if (!box || !box.hidden) return;
    box.hidden = false;
    // share.js already drew the dragon on load (even while hidden), so we only
    // need to reveal the container.
  }

  function init() {
    applyLang(pickInitialLang());

    document.querySelectorAll(".lang-toggle button").forEach((b) => {
      b.addEventListener("click", () => applyLang(b.getAttribute("data-lang")));
    });

    const made = document.querySelector(".made");
    if (made) made.addEventListener("click", revealDragon);

  }

  document.addEventListener("DOMContentLoaded", init);
})();
