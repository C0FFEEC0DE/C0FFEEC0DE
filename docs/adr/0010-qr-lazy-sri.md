# ADR-0010 — QR via lazy-loaded, SRI-locked CDN dependency

Date: 2026-07-30 · Status: Accepted

## Context
A scannable QR gives the "tap-to-collect" feel of an NFC token. The dragon must
stay offline-light, so the QR library should only load when requested.

## Decision
Use `qrcode-generator@1.4.4` from jsDelivr, loaded lazily only when the visitor
clicks "Show QR". The `<script>` tag is pinned and SRI-locked
(`sha384-lQXOAy…`). If SRI/load fails, the QR degrades to a "copy the link"
message (fail-safe; no security impact).

## Consequences
- Most visitors (who don't scan) download no extra JS.
- A CDN outage or hash mismatch never breaks the rest of the page.
- The dependency surface is one small, stable, self-contained browser build.