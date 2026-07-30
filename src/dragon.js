/* dragon.js — render a deterministic pixel-art dragon onto a <canvas>.
   Seed -> hash -> mulberry32 PRNG -> pick parts -> draw shapes on a 16x16 grid.
   Fully offline; no external dependencies. Same seed always gives the same dragon. */
(function (global) {
  "use strict";

  const GRID = 16;

  // ---- hashing / PRNG -------------------------------------------------------- #
  function fnv1a(str) {
    let h = 0x811c9dc5;
    for (let i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 0x01000193);
    }
    return h >>> 0;
  }
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ---- tiny 16x16 pixel buffer ---------------------------------------------- #
  function newGrid() { return new Array(GRID * GRID).fill(null); }
  const px = (g, x, y, c) => {
    x = Math.round(x); y = Math.round(y);
    if (x >= 0 && x < GRID && y >= 0 && y < GRID) g[y * GRID + x] = c;
  };
  function fillEllipse(g, cx, cy, rx, ry, c) {
    for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) {
      for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) {
        const dx = (x - cx) / rx, dy = (y - cy) / ry;
        if (dx * dx + dy * dy <= 1.0) px(g, x, y, c);
      }
    }
  }
  function line(g, x0, y0, x1, y1, c) {
    x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
    const sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    let err = dx - dy;
    for (;;) {
      px(g, x0, y0, c);
      if (x0 === x1 && y0 === y1) break;
      const e2 = 2 * err;
      if (e2 > -dy) { err -= dy; x0 += sx; }
      if (e2 < dx) { err += dx; y0 += sy; }
    }
  }
  function tri(g, x0, y0, x1, y1, x2, y2, c) {
    // fill a small triangle by scanning the bounding box
    const minX = Math.min(x0, x1, x2), maxX = Math.max(x0, x1, x2);
    const minY = Math.min(y0, y1, y2), maxY = Math.max(y0, y1, y2);
    for (let y = minY; y <= maxY; y++) {
      for (let x = minX; x <= maxX; x++) {
        const a = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0);
        const b = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1);
        const c2 = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2);
        const s = [a, b, c2];
        const neg = s.filter((v) => v < 0).length, pos = s.filter((v) => v > 0).length;
        if (neg === 0 || pos === 0) px(g, x, y, c);
      }
    }
  }
  const rect = (g, x, y, w, h, c) => {
    for (let i = 0; i < w; i++) for (let j = 0; j < h; j++) px(g, x + i, y + j, c);
  };

  // ---- compose a dragon from a PRNG ----------------------------------------- #
  function compose(rng) {
    const P = global.DRAGON_PARTS.PALETTES[Math.floor(rng() * global.DRAGON_PARTS.PALETTES.length)];
    const pick = (k) => Math.floor(rng() * global.DRAGON_PARTS.OPTIONS[k]);
    const cfg = {
      palette: P,
      bodyScale: pick("bodyScale"),
      eyeStyle: pick("eyeStyle"),
      wingStyle: pick("wingStyle"),
      hornStyle: pick("hornStyle"),
      accessory: pick("accessory"),
      mouth: pick("mouth"),
    };
    const g = newGrid();
    const C = cfg.palette;
    const cx = 8, cy = 10;
    const rx = [6, 5, 4][cfg.bodyScale];
    const ry = [6, 5, 5][cfg.bodyScale];

    // wings behind body
    if (cfg.wingStyle !== 3) {
      const wy = cy - 2;
      if (cfg.wingStyle === 0) { // bat
        tri(g, cx - rx, wy, 0, wy - 4, cx - rx + 1, wy + 1, C.body);
        tri(g, cx + rx, wy, 15, wy - 4, cx + rx - 1, wy + 1, C.body);
      } else if (cfg.wingStyle === 1) { // round
        fillEllipse(g, 1.5, wy, 2.5, 3, C.body);
        fillEllipse(g, 14.5, wy, 2.5, 3, C.body);
      } else { // small
        tri(g, cx - rx, wy, cx - rx - 2, wy - 2, cx - rx, wy + 1, C.body);
        tri(g, cx + rx, wy, cx + rx + 2, wy - 2, cx + rx, wy + 1, C.body);
      }
    }

    // body + belly
    fillEllipse(g, cx, cy, rx, ry, C.body);
    fillEllipse(g, cx, cy + 1, Math.max(2, rx - 2), Math.max(2, ry - 2), C.belly);

    // head spike outline along the top (a few darker pixels)
    for (let x = cx - rx + 1; x <= cx + rx - 1; x += 2) px(g, x, cy - ry, C.spike);

    // eyes
    const ey = cy - 2, exL = cx - 2, exR = cx + 2;
    if (cfg.eyeStyle === 0) { px(g, exL, ey, C.eye); px(g, exR, ey, C.eye); }
    else if (cfg.eyeStyle === 1) { line(g, exL - 1, ey, exL + 1, ey, C.eye); line(g, exR - 1, ey, exR + 1, ey, C.eye); }
    else if (cfg.eyeStyle === 2) { rect(g, exL - 1, ey, 2, 2, C.eye); rect(g, exR, ey, 2, 2, C.eye); }
    else { px(g, exL, ey, C.eye); px(g, exL - 1, ey - 1, C.eye); px(g, exR, ey, C.eye); px(g, exR + 1, ey - 1, C.eye); }

    // mouth
    if (cfg.mouth === 1) line(g, cx - 1, ey + 3, cx + 1, ey + 3, C.spike);
    else if (cfg.mouth === 2) px(g, cx, ey + 3, C.spike);

    // horns
    const hy = cy - ry;
    if (cfg.hornStyle === 1) { line(g, cx - 2, hy, cx - 3, hy - 3, C.accent); line(g, cx + 2, hy, cx + 3, hy - 3, C.accent); }
    else if (cfg.hornStyle === 2) { line(g, cx - 2, hy, cx - 1, hy - 3, C.accent); line(g, cx + 2, hy, cx + 1, hy - 3, C.accent); }
    else if (cfg.hornStyle === 3) { px(g, cx - 2, hy - 1, C.accent); px(g, cx - 2, hy - 2, C.accent); px(g, cx + 2, hy - 1, C.accent); px(g, cx + 2, hy - 2, C.accent); }

    // feet
    rect(g, cx - 3, cy + ry, 2, 1, C.spike);
    rect(g, cx + 1, cy + ry, 2, 1, C.spike);

    // accessory
    if (cfg.accessory === 1) { // scarf around neck
      rect(g, cx - rx, cy - 1, rx * 2, 2, C.accent);
    } else if (cfg.accessory === 2) { // crown above head
      px(g, cx - 1, cy - ry - 1, C.accent); px(g, cx, cy - ry - 2, C.accent); px(g, cx + 1, cy - ry - 1, C.accent);
    } else if (cfg.accessory === 3) { // star on head
      px(g, cx, cy - ry - 1, C.accent); px(g, cx - 1, cy - ry, C.accent); px(g, cx + 1, cy - ry, C.accent);
      px(g, cx, cy - ry, "#ffffff");
    }

    return { grid: g, palette: C, cfg };
  }

  // ---- draw to canvas ------------------------------------------------------- #
  function draw(canvas, seed) {
    const rng = mulberry32(fnv1a(seed));
    const { grid } = compose(rng);
    canvas.width = GRID; canvas.height = GRID;
    const ctx = canvas.getContext("2d");
    const img = ctx.createImageData(GRID, GRID);
    for (let i = 0; i < grid.length; i++) {
      const c = grid[i];
      const o = i * 4;
      if (c) {
        const [r, gC, b] = hexToRgb(c);
        img.data[o] = r; img.data[o + 1] = gC; img.data[o + 2] = b; img.data[o + 3] = 255;
      } else {
        img.data[o + 3] = 0; // transparent
      }
    }
    ctx.putImageData(img, 0, 0);
  }

  function hexToRgb(h) {
    const s = h.replace("#", "");
    return [parseInt(s.slice(0, 2), 16), parseInt(s.slice(2, 4), 16), parseInt(s.slice(4, 6), 16)];
  }

  global.DRAGON = { draw, compose, fnv1a, mulberry32 };
})(window);