#!/usr/bin/env python3
"""Retrying public smoke test for a deployed résumé site (ADR-0036 v2)."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resume" / "resume.en.md"
USER_AGENT = "krasnobai.dev deployment verifier/1.0"


def _source_value(text: str, key: str, indent: int = 2) -> str:
    match = re.search(rf"^{' ' * indent}{re.escape(key)}:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing {key!r} in {SOURCE}")
    return match.group(1).strip()


def expected_release() -> dict[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    return {
        "name": _source_value(source, "name"),
        "label": _source_value(source, "label"),
        "version": _source_value(source, "version"),
        "lastModified": _source_value(source, "lastModified"),
    }


def fetch(base: str, path: str) -> tuple[bytes, str]:
    url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    separator = "&" if "?" in url else "?"
    request = Request(
        f"{url}{separator}_verify={time.time_ns()}",
        headers={"Cache-Control": "no-cache", "User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"{path}: HTTP {response.status}")
        return response.read(), response.headers.get_content_type()


def verify_once(base: str, expected: dict[str, str]) -> None:
    index_bytes, index_type = fetch(base, "")
    index = index_bytes.decode("utf-8")
    if index_type != "text/html":
        raise ValueError(f"index: unexpected content type {index_type}")
    for value in (expected["name"], expected["label"]):
        if value not in index:
            raise ValueError(f"index: missing current {value!r}")
    for marker in ('Content-Security-Policy', 'assets/og-card.png', 'assets/favicon.svg'):
        if marker not in index:
            raise ValueError(f"index: missing {marker}")
    stylesheet_hosts = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="https?://([^/]+)', index, re.I)
    if stylesheet_hosts:
        raise ValueError(f"index: third-party stylesheets found: {stylesheet_hosts}")

    resume_bytes, _ = fetch(base, "resume.json")
    resume = json.loads(resume_bytes)
    actual = {
        "name": resume["basics"]["name"],
        "label": resume["basics"]["label"],
        "version": resume["meta"]["version"],
        "lastModified": resume["meta"]["lastModified"],
    }
    if actual != expected:
        raise ValueError(f"resume.json is stale: expected {expected}, got {actual}")
    if not resume.get("$schema", "").endswith("/v1.0.0/schema.json"):
        raise ValueError("resume.json: missing JSON Resume v1.0.0 schema marker")

    json_paths = ("resume.ru.json", "resume.min.json", ".well-known/cv.json", "agents.json")
    for path in json_paths:
        payload, _ = fetch(base, path)
        json.loads(payload)

    text_paths = ("resume.txt", "resume.md", "resume-for-agents.md", "llms.txt", "AGENTS.md", "robots.txt")
    for path in text_paths:
        payload, _ = fetch(base, path)
        if expected["name"].encode() not in payload and path != "robots.txt":
            raise ValueError(f"{path}: missing current owner name")

    agents_payload, _ = fetch(base, "agents.json")
    if "facts_policy" not in json.loads(agents_payload):
        raise ValueError("agents.json: missing evidence policy")

    png, png_type = fetch(base, "assets/og-card.png")
    if png_type != "image/png" or not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("og-card.png: invalid PNG response")
    width, height = struct.unpack(">II", png[16:24])
    if (width, height) != (1200, 630):
        raise ValueError(f"og-card.png: expected 1200x630, got {width}x{height}")

    favicon, _ = fetch(base, "assets/favicon.svg")
    if b"<svg" not in favicon:
        raise ValueError("favicon.svg: invalid SVG response")

    pdf_match = re.search(r'href="([^\"]+\.pdf)"', index)
    if not pdf_match:
        raise ValueError("index: PDF link not found")
    pdf, pdf_type = fetch(base, pdf_match.group(1))
    if not pdf.startswith(b"%PDF-") or pdf_type != "application/pdf":
        raise ValueError(f"PDF: invalid response ({pdf_type})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="deployed site URL, including any project path")
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=float, default=10.0)
    args = parser.parse_args(argv)
    expected = expected_release()

    last_error: Exception | None = None
    for attempt in range(1, args.attempts + 1):
        try:
            verify_once(args.base_url, expected)
        except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
            last_error = exc
            print(f"attempt {attempt}/{args.attempts}: {exc}", file=sys.stderr)
            if attempt < args.attempts:
                time.sleep(args.delay)
        else:
            print(
                f"DEPLOY OK — {args.base_url.rstrip('/')} "
                f"(résumé {expected['version']}, modified {expected['lastModified']})"
            )
            return 0

    print(f"DEPLOY CHECK FAILED — {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
