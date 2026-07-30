/* dragon-parts.js — palettes + option lists for the procedural pixel dragon.
   Rendered entirely client-side by dragon.js (offline, no dependencies).
   Color roles: body, belly, spike (darker outline/feet), eye, accent (accessory). */
(function (global) {
  "use strict";

  const PALETTES = [
    { name: "mossy",   body: "#5fb878", belly: "#d9e6a8", spike: "#2f7a4f", eye: "#1c1c1c", accent: "#e0a331" },
    { name: "ember",   body: "#d4633a", belly: "#f3c98a", spike: "#8a2f1f", eye: "#1c1c1c", accent: "#ffd24a" },
    { name: "frost",   body: "#6fa8d6", belly: "#d7eefb", spike: "#3a6f9a", eye: "#14202b", accent: "#bfe3ff" },
    { name: "lavender", body: "#9b7fd4", belly: "#e6dcf5", spike: "#5f4691", eye: "#241b38", accent: "#f4a8c8" },
    { name: "slate",   body: "#5c6675", belly: "#c5ccd6", spike: "#2f353f", eye: "#1c1c1c", accent: "#7fd1c0" },
  ];

  // Knobs the PRNG picks from. Counts chosen so the combined space is wide
  // but every combination still reads as a cute dragon.
  const OPTIONS = {
    bodyScale: 3,  // 0 chubby, 1 normal, 2 slim
    eyeStyle: 3,   // 0 round, 1 slit, 2 two-pixel, 3 sleepy
    wingStyle: 3,  // 0 bat, 1 round, 2 small, 3 none
    hornStyle: 4,  // 0 none, 1 straight, 2 curved, 3 two small
    accessory: 4,  // 0 none, 1 scarf, 2 crown, 3 star
    mouth: 2,      // 0 none, 1 smile, 2 tiny
  };

  global.DRAGON_PARTS = { PALETTES, OPTIONS };
})(window);