/* share.js — visitor's dragon "token": seed management, render, share link, QR.
   No backend. Seed lives in the URL (?d=) + localStorage so the same link always
   shows the same dragon. QR is lazy-loaded only when requested. */
(function () {
  "use strict";

  const STORE_KEY = "dragon.seed";
  const canvas = document.getElementById("dragon");
  const idEl = document.getElementById("dragon-id");
  const shareBtn = document.querySelector(".share-btn");
  const shareLink = document.getElementById("share-link");
  const liShare = document.getElementById("share-li");
  const qrBox = document.getElementById("qr");
  const qrToggle = document.querySelector(".qr-toggle");

  // QR lib (pinned, SRI-locked). Self-contained browser build exposing global
  // `qrcode(typeNum, ecl)` with createDataURL(). If it fails to load we degrade quietly.
  const QR_SRC = "https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js";
  const QR_INTEGRITY = "sha384-lQXOAyZwHXE55JFyrOMB7nY2Wv+m5ZWNtJcHrd1rceRQXAYNLak8ukN5TjBTcIwz";

  function makeSeed() {
    if (window.crypto && crypto.getRandomValues) {
      const b = new Uint8Array(5);
      crypto.getRandomValues(b);
      return Array.from(b, (x) => x.toString(36).padStart(2, "0")).join("").slice(0, 8);
    }
    return Math.random().toString(36).slice(2, 10); // eslint-disable-line no-restricted-globals
  }

  function currentSeed() {
    const url = new URL(location.href);
    let s = url.searchParams.get("d");
    if (!s) s = localStorage.getItem(STORE_KEY);
    if (!s) { s = makeSeed(); }
    // sanitise: alnum only, max 12 chars
    s = s.replace(/[^a-z0-9]/gi, "").slice(0, 12) || makeSeed();
    localStorage.setItem(STORE_KEY, s);
    url.searchParams.set("d", s);
    if (location.search !== url.search) history.replaceState(null, "", url);
    return s;
  }

  function shareUrl(seed) {
    const u = new URL(location.href);
    u.searchParams.set("d", seed);
    u.hash = "";
    return u.toString();
  }

  async function copy(text, btn) {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (_) { /* noop */ }
      ta.remove();
    }
    if (btn) { const orig = btn.textContent; btn.textContent = "✓"; setTimeout(() => { btn.textContent = orig; }, 1200); }
  }

  function loadQr() {
    return new Promise((resolve, reject) => {
      if (window.qrcode) return resolve();
      const s = document.createElement("script");
      s.src = QR_SRC;
      if (QR_INTEGRITY) { s.integrity = QR_INTEGRITY; s.crossOrigin = "anonymous"; }
      s.onload = () => resolve();
      s.onerror = () => reject(new Error("QR lib failed"));
      document.head.appendChild(s);
    });
  }

  async function showQr(seed) {
    qrToggle.hidden = true;
    qrBox.hidden = false;
    qrBox.textContent = "…";
    try {
      await loadQr();
      const url = shareUrl(seed);
      const qr = window.qrcode(0, "M"); // type 0 = auto size, medium error correction
      qr.addData(url);
      qr.make();
      const dataUrl = qr.createDataURL(4, 2); // cellSize 4, margin 2
      qrBox.innerHTML = "";
      const img = document.createElement("img");
      img.src = dataUrl; img.alt = "QR code linking to your dragon";
      qrBox.appendChild(img);
    } catch (e) {
      qrBox.textContent = "QR unavailable — just copy the link below.";
    }
  }

  function init() {
    if (!canvas) return;
    const seed = currentSeed();
    window.DRAGON.draw(canvas, seed);
    if (idEl) idEl.textContent = "#" + seed;
    // ADR-0022: pre-fill a LinkedIn share dialog with the dragon URL so the
    // visitor only has to press Publish (no SDK, no tracking, opens in a new tab).
    if (liShare) liShare.href = "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(shareUrl(seed));

    if (shareBtn) shareBtn.addEventListener("click", () => {
      const url = shareUrl(seed);
      copy(url, shareBtn);
      // ADR-0021: reveal the share URL inline so it is visible + selectable
      // even if the clipboard write failed silently.
      if (shareLink) {
        shareLink.value = url;
        shareLink.hidden = false;
        try { shareLink.select(); } catch (_) { /* readonly select may throw; ignore */ }
      }
      if (qrToggle) qrToggle.hidden = false;
      if (liShare) liShare.hidden = false;
    });
    if (qrToggle) qrToggle.addEventListener("click", () => showQr(seed));
  }

  document.addEventListener("DOMContentLoaded", init);
})();