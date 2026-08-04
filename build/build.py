#!/usr/bin/env python3
"""Build a resume site from markdown sources.

Input:  resume/resume.<lang>.md  (YAML front-matter + structured H2/H3 body)
Output: dist/  with index.html, resume.json, resume.<lang>.json, resume.min.json,
        resume.txt, resume.md, resume-for-agents.md, agents.json,
        <Name_Surname_Role>.pdf, llms.txt, AGENTS.md, robots.txt, sitemap.xml,
        .well-known/cv.json, assets/* and (if DOMAIN set) CNAME.

Usage:
    python build/build.py            # build into dist/
    python build/build.py --check     # build then validate, non-zero exit on failure
    python build/build.py --clean    # wipe dist/ first

Env vars (optional):
    DOMAIN   e.g. krasnobai.dev  -> emits dist/CNAME and absolute URLs
    PAGES_URL fallback absolute base when DOMAIN is unset (e.g. https://user.github.io/C0FFEEC0DE)
    PDF      "0" disables PDF generation (useful in CI if WeasyPrint libs missing)
"""
from __future__ import annotations

import html
import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError as exc:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
RESUME_DIR = ROOT / "resume"
SRC_DIR = ROOT / "src"
DIST = ROOT / "dist"
LANGS = ["en", "ru"]

MD_DASH = re.compile(r"\s[—–-]\s")  # date/role separators (em, en, hyphen)


# --------------------------------------------------------------------------- #
# Parsing the markdown source format into a JSON-Resume-shaped dict
# --------------------------------------------------------------------------- #
def _split_front_matter(text: str):
    """Return (front_matter_dict, body_text). A leading HTML comment (format
    docs) is stripped first, then an optional YAML front-matter fence is read."""
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = yaml.safe_load(text[3:end]) or {}
            body = text[end + 4 :]
            return fm, body
    return {}, text


def _sections(body: str):
    """Yield (title, lines) for each `## Section`."""
    blocks = re.split(r"^## ", body, flags=re.MULTILINE)
    for blk in blocks[1:]:
        title, _, rest = blk.partition("\n")
        yield title.strip(), rest.rstrip()


def _parse_meta_line(line: str) -> dict:
    """Parse `dates: ... · location: ... · url: ...` into a dict."""
    out: dict[str, str] = {}
    for part in line.split("·"):
        part = part.strip()
        if not part:
            continue
        key, sep, val = part.partition(":")
        if sep:
            out[key.strip().lower()] = val.strip()
    return out


def _split_dates(value: str):
    """'2022-03 — present' -> ('2022-03', None). Tolerant of dash variants."""
    parts = MD_DASH.split(value)
    start = parts[0].strip() or None
    end = None
    if len(parts) > 1 and parts[1].strip().lower() not in ("present", "настоящее", "now", "сейчас", ""):
        end = parts[1].strip()
    return start, end


def _download_slug(name: str, label: str) -> str:
    """Human-friendly filename base from name + role: Aleksandr_Krasnobai_Staff_DevOps_Engineer.

    Non-alphanumeric characters are stripped, spaces become underscores. This is
    used for the downloadable PDFs only; machine-readable JSON endpoints keep
    their canonical names (ADR-0030).
    """
    def clean(s: str) -> str:
        return re.sub(r"[^\w\s-]", "", s).strip().replace(" ", "_")
    return f"{clean(name)}_{clean(label)}"


def parse_resume(path: Path) -> dict:
    fm, body = _split_front_matter(path.read_text(encoding="utf-8"))
    basics = dict(fm.get("basics") or {})
    if fm.get("profiles"):
        basics["profiles"] = fm["profiles"]
    resume: dict = {"basics": basics, "meta": fm.get("meta") or {}}
    if fm.get("availability"):  # optional hiring signals (cv.json / Open Talent Protocol)
        resume["availability"] = fm["availability"]

    for title, content in _sections(body):
        lines = [ln for ln in content.splitlines() if ln.strip()]
        key = title.lower()
        if key == "summary":
            resume["basics"]["summary"] = " ".join(ln.strip() for ln in lines)
        elif key == "experience":
            resume["work"] = _parse_titled_items(lines, ("position", "name"))
        elif key == "projects":
            resume["projects"] = _parse_project_items(lines)
        elif key == "education":
            resume["education"] = _parse_education_items(lines)
        elif key == "skills":
            resume["skills"] = _parse_skills(lines)
        elif key == "certificates":
            resume["certificates"] = _parse_certificates(lines)
        elif key == "languages":
            resume["languages"] = _parse_languages(lines)
        elif key == "contact":
            resume.setdefault("_contact", " ".join(ln.strip() for ln in lines))
    return resume


def _parse_titled_items(lines, fields):
    """H3 `### Role — Company`. fields = (position_key, name_key)."""
    items = []
    cur: dict | None = None
    for ln in lines:
        if ln.startswith("### "):
            if cur:
                items.append(cur)
            head = ln[4:].strip()
            role, _, company = head.partition(" — ")
            cur = {fields[0]: role.strip(), fields[1]: company.strip()}
        elif cur is not None and re.match(r"^[a-z]+:", ln) and "highlights" not in cur:
            meta = _parse_meta_line(ln)
            if "dates" in meta:
                s, e = _split_dates(meta["dates"])
                if s:
                    cur["startDate"] = s
                if e:
                    cur["endDate"] = e
            if "location" in meta:
                cur["location"] = meta["location"]
            if "url" in meta:
                cur["url"] = meta["url"]
        elif cur is not None and ln.startswith("- "):
            cur.setdefault("highlights", []).append(ln[2:].strip())
    if cur:
        items.append(cur)
    return items


def _parse_project_items(lines):
    items = []
    cur: dict | None = None
    for ln in lines:
        if ln.startswith("### "):
            if cur:
                items.append(cur)
            cur = {"name": ln[4:].strip()}
        elif cur is not None and re.match(r"^[a-z]+:", ln) and "highlights" not in cur:
            meta = _parse_meta_line(ln)
            if "dates" in meta:
                s, e = _split_dates(meta["dates"])
                if s:
                    cur["startDate"] = s
                if e:
                    cur["endDate"] = e
            if "url" in meta:
                cur["url"] = meta["url"]
        elif cur is not None and ln.startswith("- "):
            cur.setdefault("highlights", []).append(ln[2:].strip())
    if cur:
        items.append(cur)
    return items


def _parse_education_items(lines):
    items = []
    cur: dict | None = None
    for ln in lines:
        if ln.startswith("### "):
            if cur:
                items.append(cur)
            head = ln[4:].strip()
            degree, _, inst = head.partition(" — ")
            cur = {"studyType": degree.strip(), "institution": inst.strip()}
        elif cur is not None and re.match(r"^[a-z]+:", ln) and "courses" not in cur:
            meta = _parse_meta_line(ln)
            if "dates" in meta:
                s, e = _split_dates(meta["dates"])
                if s:
                    cur["startDate"] = s
                if e:
                    cur["endDate"] = e
            if "location" in meta:
                cur["location"] = meta["location"]
        elif cur is not None and ln.startswith("- "):
            cur.setdefault("courses", []).append(ln[2:].strip())
    if cur:
        items.append(cur)
    return items


def _parse_skills(lines):
    out = []
    for ln in lines:
        if not ln.startswith("- "):
            continue
        body = ln[2:]
        name, sep, kws = body.partition(":")
        name = name.strip().strip("*")
        if sep:
            kws = [k.strip() for k in kws.split(",") if k.strip()]
        else:
            kws = []
        out.append({"name": name, "keywords": kws})
    return out


def _parse_certificates(lines):
    out = []
    for ln in lines:
        if not ln.startswith("- "):
            continue
        body = ln[2:]
        # **Name** — issuer (date)
        m = re.match(r"\*\*(.+?)\*\*\s*[—–-]\s*(.+?)\s*\(([^)]+)\)\s*$", body)
        if m:
            out.append({"name": m[1].strip(), "issuer": m[2].strip(), "date": m[3].strip()})
        else:
            out.append({"name": body.strip()})
    return out


def _parse_languages(lines):
    out = []
    for ln in lines:
        if not ln.startswith("- "):
            continue
        body = ln[2:]
        m = re.match(r"\*\*(.+?)\*\*\s*\((.+?)\)", body)
        if m:
            out.append({"language": m[1].strip(), "fluency": m[2].strip()})
        else:
            out.append({"language": body.strip()})
    return out


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def _tag_pill(text: str) -> str:
    return f'<span class="tag">{esc(text)}</span>'


def render_header_fragment(r: dict, lang: str) -> str:
    """Header only — injected into the landing hero, one per language. Shows
    identity (tags + name + one-line summary/lead)."""
    b = r["basics"]
    tags: list[str] = []
    if b.get("label"):
        tags.append(_tag_pill(b["label"]))
    loc = b.get("location")
    if isinstance(loc, dict) and loc.get("city"):
        region = loc.get("region") or loc.get("countryCode")
        city = loc["city"]
        tag_text = city
        if region:
            tag_text += f", {region}"
        if loc.get("note"):
            tag_text += f" — {loc['note']}"
        tags.append(_tag_pill(tag_text))
    elif isinstance(loc, str) and loc:
        tags.append(_tag_pill(loc))

    parts: list[str] = []
    if tags:
        parts.append(f'<p class="tags">{"".join(tags)}</p>')
    parts.append(f'<h1>{esc(b.get("name"))}</h1>')
    if b.get("summary"):
        parts.append(f'<p class="lead">{esc(b["summary"])}</p>')
    return "\n".join(parts)


def _contact_section(b: dict, lang: str, *, show_url: bool = True) -> str:
    """The Contact block, shared by the landing page and the PDF so the
    contact surface stays in lockstep (ADR-0013/0031).

    The landing page uses show_url=False because the visitor is already on the
    site; every other surface (PDF, resume.json, resume.txt, llms.txt) keeps
    the canonical URL."""
    contacts = []
    if b.get("email"):
        contacts.append(f'<a href="mailto:{esc(b["email"])}">{esc(b["email"])}</a>')
    if b.get("phone"):
        contacts.append(esc(b["phone"]))
    if show_url and b.get("url"):
        contacts.append(f'<a href="{esc(b["url"])}">{esc(b["url"])}</a>')
    for p in b.get("profiles", []) or []:
        contacts.append(f'<a href="{esc(p.get("url"))}">{esc(p.get("network"))}</a>')
    if not contacts:
        return ""
    return (f'<section class="block"><h2>{esc(_t(lang, "Contact"))}</h2>'
            f'<p class="contact">{" · ".join(contacts)}</p></section>')


def _business_card_contacts(b: dict, lang: str) -> str:
    """Compact contact row for the landing-page business card: LinkedIn +
    Telegram + email. GitHub is intentionally omitted here and lives in the
    footer machine links."""
    items: list[str] = []
    for p in b.get("profiles", []) or []:
        network = p.get("network", "")
        if network in ("LinkedIn", "Telegram"):
            items.append(f'<a href="{esc(p.get("url"))}">{esc(network)}</a>')
    if b.get("email"):
        items.append(f'<a href="mailto:{esc(b["email"])}">{esc(b["email"])}</a>')
    if not items:
        return ""
    sep = '<span class="sep" aria-hidden="true">·</span>'
    return f'<div class="contact-row">{sep.join(items)}</div>'


def render_contact_fragment(r: dict, lang: str) -> str:
    """Business-card contact row — injected into the landing #resume block
    (ADR-0025). The full résumé body lives in the branded PDF and the
    machine-readable outputs; the landing page shows identity (hero) + three
    top contacts only and funnels to the PDF for the detail."""
    return _business_card_contacts(r["basics"], lang)


def render_body_fragment(r: dict, lang: str) -> str:
    """Résumé sections WITHOUT the header — used by the branded PDF (via
    render_html_fragment). The landing page uses render_contact_fragment instead
    (ADR-0025), so the full body renders only in the PDF, not on the page."""
    b = r["basics"]
    parts: list[str] = []

    def section(title, inner):
        return f'<section class="block"><h2>{esc(title)}</h2>{inner}</section>'

    # Contact line (full set, including GitHub, for the branded PDF)
    contact = _contact_section(b, lang)
    if contact:
        parts.append(contact)

    intro = (r.get("meta") or {}).get("intro", "")
    if intro:
        parts.append(section(_t(lang, "Summary"), f"<p>{esc(intro)}</p>"))

    work = r.get("work", [])
    if work:
        items = []
        for w in work:
            dates = _fmt_range(w.get("startDate"), w.get("endDate"), lang)
            items.append(
                '<div class="job">'
                f'<h3><span class="role">{esc(w.get("position"))}</span>'
                f'<span class="at"> — </span><span class="org">{esc(w.get("name"))}</span></h3>'
                f'<div class="meta">{esc(dates)}{(" · " + esc(w["location"])) if w.get("location") else ""}</div>'
                + (_hl(w.get("highlights")) if w.get("highlights") else "")
                + "</div>"
            )
        parts.append(section(_t(lang, "Experience"), "".join(items)))

    skills = r.get("skills", [])
    if skills:
        chips = []
        for s in skills:
            if s.get("keywords"):
                chips.append(f'<div class="skill-group"><span class="skill-name">{esc(s["name"])}</span>: '
                             + ", ".join(esc(k) for k in s["keywords"]) + "</div>")
        parts.append(section(_t(lang, "Skills"), '<div class="skills">' + "".join(chips) + "</div>"))

    proj = r.get("projects", [])
    if proj:
        items = []
        for p in proj:
            head = f'<h3>{esc(p.get("name"))}</h3>'
            meta = []
            if p.get("startDate"):
                meta.append(esc(_fmt_range(p.get("startDate"), p.get("endDate"), lang)))
            if p.get("url"):
                meta.append(f'<a href="{esc(p["url"])}">{esc(p["url"])}</a>')
            items.append('<div class="project">' + head
                         + (f'<div class="meta">{" · ".join(meta)}</div>' if meta else "")
                         + (_hl(p.get("highlights")) if p.get("highlights") else "") + "</div>")
        parts.append(section(_t(lang, "Projects"), "".join(items)))

    edu = r.get("education", [])
    if edu:
        items = []
        for e in edu:
            items.append('<div class="edu"><h3>'
                         + esc(e.get("studyType")) + (f' — {esc(e["institution"])}' if e.get("institution") else "")
                         + '</h3>' + (f'<div class="meta">{esc(_fmt_range(e.get("startDate"), e.get("endDate"), lang))}'
                                       + (f' · {esc(e["location"])}' if e.get("location") else "")
                                       + '</div>' if e.get("startDate") else "")
                         + (_hl(e.get("courses")) if e.get("courses") else "") + "</div>")
        parts.append(section(_t(lang, "Education"), "".join(items)))

    certs = r.get("certificates", [])
    if certs:
        items = "".join(f"<li><strong>{esc(c['name'])}</strong>"
                        + (f' — {esc(c["issuer"])}' if c.get("issuer") else "")
                        + (f' ({esc(c["date"])})' if c.get("date") else "") + "</li>"
                        for c in certs)
        parts.append(section(_t(lang, "Certificates"), f"<ul>{items}</ul>"))

    langs = r.get("languages", [])
    if langs:
        items = "".join(f"<li><strong>{esc(l['language'])}</strong>"
                        + (f' ({esc(l["fluency"])})' if l.get("fluency") else "") + "</li>" for l in langs)
        parts.append(section(_t(lang, "Languages"), f"<ul>{items}</ul>"))

    return "\n".join(parts)


def _hl(items):
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def _fmt_range(start, end, lang):
    present = _t(lang, "present")
    if start and end:
        return f"{start} — {end}"
    if start:
        return f"{start} — {present}"
    return end or ""


_T = {
    "en": {"Contact": "Contact", "Experience": "Work Experience", "Skills": "Skills",
           "Projects": "Projects", "Education": "Education", "Certificates": "Certifications",
           "Languages": "Languages", "Summary": "Summary", "present": "Present",
           "download": "Download résumé (PDF)", "copy": "Copy curl one-liner",
           "share": "Share my dragon", "dragon_line": "This is your little dragon — it's yours. Share the link so each colleague gets their own.",
           "greeting": "Hi there — glad you stopped by. Here's my résumé, and a tiny friend for the road.",
           "curl_label": "Or grab it from your terminal:"},
    "ru": {"Contact": "Контакты", "Experience": "Опыт работы", "Skills": "Навыки",
           "Projects": "Проекты", "Education": "Образование", "Certificates": "Сертификаты",
           "Languages": "Языки", "Summary": "Обзор", "present": "наст.",
           "download": "Скачать резюме (PDF)", "copy": "Скопировать curl-команду",
           "share": "Поделиться дракончиком", "dragon_line": "Это твой дракончик — он твой. Поделись ссылкой, и у каждого коллеги появится свой.",
           "greeting": "Привет — рад, что заглянули. Вот моё резюме и маленький друг на удачу.",
           "curl_label": "Или заберите из терминала:"},
}


def _t(lang, key):
    return _T[lang][key]


def render_text(r: dict) -> str:
    b = r["basics"]
    intro = (r.get("meta") or {}).get("intro", "")
    out = [b.get("name", ""), b.get("label", ""), ""]
    if intro:
        out += [intro, ""]
    elif b.get("summary"):
        out += [b["summary"], ""]
    contact = []
    if b.get("email"):
        contact.append(f"email: {b['email']}")
    if b.get("phone"):
        contact.append(f"phone: {b['phone']}")
    if b.get("url"):
        contact.append(f"web: {b['url']}")
    for p in b.get("profiles", []) or []:
        contact.append(f"{p.get('network')}: {p.get('url')}")
    if contact:
        out += [" | ".join(contact), ""]

    def block(title, lines):
        return [title, "-" * len(title)] + lines + [""]

    if r.get("work"):
        lines = []
        for w in r["work"]:
            lines.append(f"{w.get('position')} — {w.get('name')}")
            d = _fmt_range(w.get("startDate"), w.get("endDate"), "en")
            if d:
                lines.append(f"  {d}" + (f" · {w['location']}" if w.get("location") else ""))
            for h in w.get("highlights", []):
                lines.append(f"  - {h}")
            lines.append("")
        out += block("EXPERIENCE", lines)
    if r.get("skills"):
        lines = [f"- {s['name']}: " + ", ".join(s.get("keywords", [])) for s in r["skills"]]
        out += block("SKILLS", lines)
    if r.get("projects"):
        lines = []
        for p in r["projects"]:
            lines.append(p.get("name", ""))
            if p.get("url"):
                lines.append(f"  {p['url']}")
            for h in p.get("highlights", []):
                lines.append(f"  - {h}")
            lines.append("")
        out += block("PROJECTS", lines)
    if r.get("education"):
        lines = []
        for e in r["education"]:
            lines.append(f"{e.get('studyType')} — {e.get('institution')}")
            d = _fmt_range(e.get("startDate"), e.get("endDate"), "en")
            if d:
                lines.append(f"  {d}")
            lines.append("")
        out += block("EDUCATION", lines)
    if r.get("certificates"):
        out += block("CERTIFICATES", [f"- {c.get('name')} — {c.get('issuer')} ({c.get('date')})" for c in r["certificates"]])
    if r.get("languages"):
        out += block("LANGUAGES", [f"- {l.get('language')} ({l.get('fluency')})" for l in r["languages"]])
    return "\n".join(out).rstrip() + "\n"


def render_markdown(r: dict) -> str:
    """Clean markdown mirror (no front-matter/comments)."""
    b = r["basics"]
    intro = (r.get("meta") or {}).get("intro", "")
    out = [f"# {b.get('name','')}", ""]
    if b.get("label"):
        out += [f"*{b['label']}*", ""]
    if intro:
        out += [intro, ""]
    elif b.get("summary"):
        out += [b["summary"], ""]
    # Contact (ADR-0024: GitHub, LinkedIn + email/phone/url)
    contact = []
    if b.get("email"):
        contact.append(f"<{b['email']}>")
    if b.get("phone"):
        contact.append(b.get("phone"))
    if b.get("url"):
        contact.append(f"<{b['url']}>")
    for p in b.get("profiles", []) or []:
        contact.append(f"[{p.get('network')}]({p.get('url')})")
    if contact:
        out += ["## Contact", ""]
        for c in contact:
            out.append(f"- {c}")
        out.append("")
    if r.get("work"):
        out += ["## Experience", ""]
        for w in r["work"]:
            out.append(f"### {w.get('position')} — {w.get('name')}")
            d = _fmt_range(w.get("startDate"), w.get("endDate"), "en")
            if d:
                out.append(f"*{d}" + (f" · {w['location']}" if w.get("location") else "") + "*")
            for h in w.get("highlights", []):
                out.append(f"- {h}")
            out.append("")
    if r.get("skills"):
        out += ["## Skills", ""]
        for s in r["skills"]:
            out.append(f"- **{s['name']}**: " + ", ".join(s.get("keywords", [])))
        out.append("")
    if r.get("projects"):
        out += ["## Projects", ""]
        for p in r["projects"]:
            out.append(f"### {p.get('name')}")
            if p.get("url"):
                out.append(f"<{p['url']}>")
            for h in p.get("highlights", []):
                out.append(f"- {h}")
            out.append("")
    if r.get("education"):
        out += ["## Education", ""]
        for e in r["education"]:
            out.append(f"### {e.get('studyType')} — {e.get('institution')}")
            d = _fmt_range(e.get("startDate"), e.get("endDate"), "en")
            if d:
                out.append(f"*{d}*")
            out.append("")
    if r.get("certificates"):
        out += ["## Certificates", ""]
        for c in r["certificates"]:
            out.append(f"- **{c.get('name')}** — {c.get('issuer')} ({c.get('date')})")
        out.append("")
    if r.get("languages"):
        out += ["## Languages", ""]
        for l in r["languages"]:
            out.append(f"- **{l.get('language')}** ({l.get('fluency')})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_pdf_html(r: dict, lang: str) -> str:
    """Wrapper for the single human/ATS PDF (ADR-0031)."""
    body = render_resume_html(r, lang)
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<title>{esc(r['basics'].get('name'))} — résumé</title>
</head><body>{body}</body></html>"""


_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _fmt_ats(start, end, lang):
    """ATS-safe date range, e.g. 'Mar 2022 – Present'. Tolerates YYYY and YYYY-MM."""
    def fmt(v):
        v = (v or "").strip()
        if not v:
            return ""
        if re.fullmatch(r"\d{4}", v):
            return v
        m = re.fullmatch(r"(\d{4})-(\d{1,2})", v)
        if m:
            y, mo = m.groups()
            return f"{_MONTHS[int(mo) - 1]} {y}"
        return v
    s, e = fmt(start), fmt(end)
    if s and e:
        return f"{s} – {e}"
    if s:
        return f"{s} – {_t(lang, 'present')}"
    return e


# Human-readable AND ATS-safe single PDF (ADR-0031).
# Combines Forest palette/visual hierarchy with ATS-safe structure:
# single column, real text, standard fonts, dates on role line, no tables/floats.
_RESUME_CSS = """
@page { margin: 0.75in 0.85in; }
* { box-sizing: border-box; }
body {
  font: 10.8pt/1.45 -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #1f2a1f; background: #fff; margin: 0;
}
h1 { font-size: 21pt; margin: 0 0 3px; letter-spacing: -0.01em; }
h2 { font-size: 12pt; margin: 16px 0 5px; border-bottom: 1.5px solid #2f7d3a; padding-bottom: 2px; color: #1f2a1f; }
h3 { font-size: 10.8pt; margin: 8px 0 2px; }
a { color: #2f7d3a; text-decoration: none; }
.hero { margin-bottom: 6px; }
.hero .tags { margin: 0 0 4px; }
.hero .tag {
  display: inline-block; font-size: 8.5pt; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.03em; color: #2f7d3a; background: #f4f6f2;
  border: 1px solid #e0e6dd; border-radius: 999px; padding: 1px 6px; margin-right: 4px;
}
.hero .lead { color: #5b6b5b; max-width: 62ch; margin: 4px 0 0; }
.block { margin: 10px 0; page-break-inside: avoid; }
.block + .block { border-top: 1px solid #e0e6dd; padding-top: 8px; }
.contact { color: #5b6b5b; font-size: 10pt; margin: 0 0 6px; }
.contact a { color: #1f2a1f; }
.meta { color: #5b6b5b; font-size: 9.8pt; margin-bottom: 3px; }
.job, .project, .edu { margin-bottom: 8px; }
.job:last-child, .project:last-child, .edu:last-child { margin-bottom: 0; }
.role { font-weight: 700; }
.at { color: #5b6b5b; }
.org { color: #2f7d3a; font-weight: 700; }
.skills { display: flex; flex-direction: column; gap: 3px; }
.skill-name { color: #2f7d3a; font-weight: 600; }
ul { margin: 3px 0 0; padding-left: 16px; }
li { margin: 2px 0; }
"""


def render_resume_html(r: dict, lang: str) -> str:
    """Single PDF render: visually designed + ATS-safe (ADR-0031)."""
    b = r["basics"]
    parts = [f'<style>{_RESUME_CSS}</style>']

    # Header
    header_parts = ['<div class="hero">']
    tags = []
    if b.get("label"):
        tags.append(f'<span class="tag">{esc(b["label"])}</span>')
    loc = b.get("location")
    if isinstance(loc, dict) and loc.get("city"):
        tag_text = loc["city"]
        if loc.get("region"):
            tag_text += f', {loc["region"]}'
        if loc.get("note"):
            tag_text += f' — {loc["note"]}'
        tags.append(f'<span class="tag">{esc(tag_text)}</span>')
    if tags:
        header_parts.append(f'<p class="tags">{"".join(tags)}</p>')
    header_parts.append(f'<h1>{esc(b.get("name"))}</h1>')
    if b.get("summary"):
        header_parts.append(f'<p class="lead">{esc(b["summary"])}</p>')
    header_parts.append('</div>')
    parts.append("".join(header_parts))

    # Contact — label + URL for both human readability and ATS extraction
    contacts = []
    if b.get("email"):
        contacts.append(f'<a href="mailto:{esc(b["email"])}">{esc(b["email"])}</a>')
    if b.get("phone"):
        contacts.append(esc(b["phone"]))
    for p in b.get("profiles", []) or []:
        network = esc(p.get("network"))
        url = esc(p.get("url"))
        display = f"{network}: {url.replace('https://', '')}"
        contacts.append(f'<a href="{url}">{display}</a>')
    if contacts:
        parts.append(f'<p class="contact">{" · ".join(contacts)}</p>')

    def sec(title, inner):
        return f'<section class="block"><h2>{esc(title)}</h2>{inner}</section>'

    # Summary (full intro)
    intro = (r.get("meta") or {}).get("intro", "")
    if intro:
        parts.append(sec(_t(lang, "Summary"), f'<p>{esc(intro)}</p>'))

    # Experience
    if r.get("work"):
        items = []
        for w in r["work"]:
            d = _fmt_ats(w.get("startDate"), w.get("endDate"), lang)
            meta = d
            if w.get("location"):
                meta += f" | {esc(w['location'])}"
            items.append(
                '<div class="job">'
                f'<h3><span class="role">{esc(w.get("position"))}</span>'
                f'<span class="at"> — </span><span class="org">{esc(w.get("name"))}</span></h3>'
                f'<div class="meta">{meta}</div>'
                + (_hl(w.get("highlights")) if w.get("highlights") else "")
                + "</div>"
            )
        parts.append(sec(_t(lang, "Experience"), "".join(items)))

    # Skills
    if r.get("skills"):
        chips = []
        for s in r["skills"]:
            if s.get("keywords"):
                chips.append(f'<div class="skill-group"><span class="skill-name">{esc(s["name"])}</span>: '
                             + ", ".join(esc(k) for k in s["keywords"]) + "</div>")
        parts.append(sec(_t(lang, "Skills"), '<div class="skills">' + "".join(chips) + "</div>"))

    # Projects
    if r.get("projects"):
        items = []
        for p in r["projects"]:
            meta_parts = []
            d = _fmt_ats(p.get("startDate"), p.get("endDate"), lang)
            if d:
                meta_parts.append(d)
            if p.get("url"):
                meta_parts.append(f'<a href="{esc(p["url"])}">{esc(p["url"])}</a>')
            meta = f'<div class="meta">{" | ".join(meta_parts)}</div>' if meta_parts else ""
            items.append('<div class="project">'
                         + f'<h3>{esc(p.get("name"))}</h3>'
                         + meta
                         + (_hl(p.get("highlights")) if p.get("highlights") else "")
                         + "</div>")
        parts.append(sec(_t(lang, "Projects"), "".join(items)))

    # Education
    if r.get("education"):
        items = []
        for e in r["education"]:
            d = _fmt_ats(e.get("startDate"), e.get("endDate"), lang)
            meta = (f'<div class="meta">{esc(d)}'
                    + (f' · {esc(e["location"])}' if e.get("location") else '')
                    + '</div>') if d else ""
            items.append('<div class="edu"><h3>'
                         + esc(e.get("studyType")) + (f' — {esc(e["institution"])}' if e.get("institution") else "")
                         + '</h3>' + meta
                         + (_hl(e.get("courses")) if e.get("courses") else "") + "</div>")
        parts.append(sec(_t(lang, "Education"), "".join(items)))

    # Certificates
    if r.get("certificates"):
        body = "<ul>" + "".join(f"<li><strong>{esc(c['name'])}</strong>"
                                + (f' — {esc(c["issuer"])}' if c.get("issuer") else "")
                                + (f' ({esc(c["date"])})' if c.get("date") else "") + "</li>"
                                for c in r["certificates"]) + "</ul>"
        parts.append(sec(_t(lang, "Certificates"), body))

    # Languages
    if r.get("languages"):
        body = "<p>" + ", ".join(f"<strong>{esc(l['language'])}</strong> ({esc(l['fluency'])})"
                                 for l in r["languages"]) + "</p>"
        parts.append(sec(_t(lang, "Languages"), body))

    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<title>{esc(b.get('name'))} — résumé</title></head><body>{''.join(parts)}</body></html>"""


# --------------------------------------------------------------------------- #
# AI-agent facing files
# --------------------------------------------------------------------------- #
def _years_experience(r: dict) -> int | None:
    """Rough years of experience from the earliest work startDate to today."""
    starts = []
    for w in r.get("work", []):
        s = (w.get("startDate") or "")[:4]
        if s.isdigit():
            starts.append(int(s))
    if not starts:
        return None
    return max(0, date.today().year - min(starts))


def build_min_json(r: dict, base: str) -> dict:
    """Token-cheap metadata tier (~100 tokens) for agent screening (ADR-0015).
    Enough to decide whether to fetch the full resume.json."""
    b = r["basics"]
    top_skills = []
    for s in r.get("skills", [])[:3]:
        top_skills.extend(s.get("keywords", [])[:4])
    out = {
        "name": b.get("name"),
        "label": b.get("label"),
        "location": b.get("location", {}).get("city") if isinstance(b.get("location"), dict) else b.get("location"),
        "years_experience": _years_experience(r),
        "top_skills": top_skills[:10],
        "full": _abs(base, "resume.json"),
    }
    avail = r.get("availability")
    if avail:
        out["availability"] = avail
    return out


def build_cv_json(r: dict, base: str, pdf_name: str) -> dict:
    """cv.json-style discovery manifest at /.well-known/cv.json (ADR-0015/0031)."""
    return {
        "schema": "cv.json",
        "version": "1.2.1",
        "primary": _abs(base, "resume.json"),
        "languages": {
            "en": _abs(base, "resume.json"),
            "ru": _abs(base, "resume.ru.json"),
        },
        "plain_text": _abs(base, "resume.txt"),
        "metadata_tier": _abs(base, "resume.min.json"),
        "agent_readable": _abs(base, "resume-for-agents.md"),
        "agent_spec": _abs(base, "agents.json"),
        "human_pdf": _abs(base, pdf_name),
        "ats_pdf": _abs(base, pdf_name),
    }


def build_llms_txt(r: dict, base: str, pdf_name: str) -> str:
    """llmstxt.org-compliant index for LLM and AI-agent crawlers (ADR-0031).

    Ordered by cost-to-ingest: metadata tier first, then structured JSON, then
    the agent-optimized markdown, then human artifacts last.
    """
    b = r["basics"]
    name = b.get("name", "Résumé")
    summary = (r.get("meta") or {}).get("intro", b.get("summary", ""))
    links = [
        ("resume.min.json", "Metadata tier (~100 tokens) — read this first"),
        ("resume.json", "JSON Resume v1.0.0 — canonical structured source"),
        ("resume.ru.json", "JSON Resume v1.0.0 — Russian mirror"),
        (".well-known/cv.json", "cv.json discovery manifest"),
        ("resume-for-agents.md", "LLM/AI-agent optimized résumé markdown"),
        ("agents.json", "OpenAI-style structured-output function spec"),
        ("resume.txt", "Plain-text résumé (both languages)"),
        ("resume.md", "Clean markdown résumé"),
        (pdf_name, "Human-readable, ATS-safe PDF"),
        ("AGENTS.md", "Instructions for AI agents"),
    ]
    link_lines = "\n".join(f"- [{p}]({_abs(base, p)}): {d}" for p, d in links)
    # Contact surface (ADR-0024): GitHub, LinkedIn, Telegram for LLM agents.
    contact_lines = [f"- **Email:** {b.get('email', '')}"]
    for p in (b.get("profiles", []) or []):
        contact_lines.append(f"- {p.get('network')}: {p.get('url')}")
    contact_block = f"\n## Contact\n" + "\n".join(contact_lines) + "\n"
    avail = r.get("availability")
    avail_block = ""
    if avail:
        tz = avail.get("timezone")
        tz_line = f"\n- Time zone: {tz}" if tz else ""
        avail_block = (
            "\n## Availability\n"
            f"- Status: {avail.get('status')}\n"
            f"- Roles: {', '.join(avail.get('roles', []))}\n"
            f"- Work model: {avail.get('work_model')}\n"
            f"- Locations: {', '.join(avail.get('locations', []))}{tz_line}\n"
        )
    return f"""# {name}

> {summary}
{contact_block}{avail_block}
## Files
{link_lines}

## Instructions for AI agents

1. Read `resume.min.json` first to decide relevance (~100 tokens).
2. Fetch `resume.json` for the canonical structured résumé.
3. For a narrative, keyword-rich version optimized for summarisation, read
   `resume-for-agents.md`.
4. Use `agents.json` for OpenAI-style structured-output function calls.
5. Do not infer facts not present in these files. Contact and availability are
   explicitly listed above.
"""


def build_agents_md(r: dict, base: str, pdf_name: str) -> str:
    """Instructions for AI agents / recruiter crawlers (ADR-0003/0031)."""
    b = r["basics"]
    name = b.get("name", "")
    return f"""# AGENTS.md — instructions for AI agents

This is the personal résumé site of {name} ({b.get('label', '')}).

## Source-of-truth hierarchy

1. `{_abs(base, 'resume.min.json')}` — token-cheap metadata tier (~100 tokens).
   Read this first to decide whether the profile is relevant.
2. `{_abs(base, 'resume.json')}` — canonical English JSON Resume v1.0.0
   (fields: basics, work, education, skills, projects, certificates, languages,
   meta, and optional `availability` hiring signals).
3. `{_abs(base, 'resume.ru.json')}` — Russian mirror.
4. `{_abs(base, '.well-known/cv.json')}` — cv.json discovery manifest.
5. `{_abs(base, 'resume-for-agents.md')}` — narrative, keyword-rich résumé
   optimized for LLM summarisation and extraction.
6. `{_abs(base, 'agents.json')}` — OpenAI-style structured-output function spec.

## Human artifact

- `{_abs(base, pdf_name)}` — single human-readable, ATS-safe PDF.

## Rules

- Prefer `resume.json` for factual claims.
- Use `resume-for-agents.md` for natural-language summaries.
- Do not infer facts not present in the files above.
- Contact: `basics.email` = {b.get('email', '')} and `basics.profiles`.
"""


def build_resume_for_agents(r: dict, base: str) -> str:
    """Narrative, keyword-rich résumé optimized for LLM/AI-agent ingestion
    (ADR-0031). Front-loads the summary, keeps section headings explicit, and
    surfaces availability signals.
    """
    b = r["basics"]
    name = b.get("name", "")
    label = b.get("label", "")
    summary = (r.get("meta") or {}).get("intro", b.get("summary", ""))

    lines = [
        f"# {name}",
        "",
        f"**{label}**",
        "",
    ]

    # Availability front-loaded so agents see hiring signals immediately
    avail = r.get("availability")
    if avail:
        tz = avail.get("timezone")
        tz_line = f"\n- **Time zone:** {tz}" if tz else ""
        lines += [
            "## Availability",
            "",
            f"- **Status:** {avail.get('status')}",
            f"- **Open roles:** {', '.join(avail.get('roles', []))}",
            f"- **Work model:** {avail.get('work_model')}",
            f"- **Locations:** {', '.join(avail.get('locations', []))}{tz_line}",
            "",
        ]

    # Contact
    lines += [
        "## Contact",
        "",
        f"- **Email:** {b.get('email', '')}",
    ]
    if b.get("phone"):
        lines.append(f"- **Phone:** {b.get('phone')}")
    for p in b.get("profiles", []) or []:
        lines.append(f"- **{p.get('network')}:** {p.get('url')}")
    lines.append("")

    # Executive summary
    if summary:
        lines += [
            "## Executive summary",
            "",
            summary,
            "",
        ]

    # Experience with metrics preserved
    if r.get("work"):
        lines += ["## Experience", ""]
        for w in r["work"]:
            d = _fmt_range(w.get("startDate"), w.get("endDate"), "en")
            loc = f" · {w['location']}" if w.get("location") else ""
            lines.append(f"### {w.get('position')} — {w.get('name')}")
            lines.append(f"*{d}{loc}*")
            lines.append("")
            for h in w.get("highlights", []):
                lines.append(f"- {h}")
            lines.append("")

    # Skills matrix
    if r.get("skills"):
        lines += ["## Skills", ""]
        for s in r["skills"]:
            lines.append(f"- **{s['name']}:** {', '.join(s.get('keywords', []))}")
        lines.append("")

    # Projects
    if r.get("projects"):
        lines += ["## Projects", ""]
        for p in r["projects"]:
            lines.append(f"### {p.get('name')}")
            d = _fmt_range(p.get("startDate"), p.get("endDate"), "en")
            if d:
                lines.append(f"*{d}*")
            if p.get("url"):
                lines.append(f"- URL: {p['url']}")
            for h in p.get("highlights", []):
                lines.append(f"- {h}")
            lines.append("")

    # Education
    if r.get("education"):
        lines += ["## Education", ""]
        for e in r["education"]:
            lines.append(f"- **{e.get('studyType')}** — {e.get('institution')}")
            d = _fmt_range(e.get("startDate"), e.get("endDate"), "en")
            if d:
                lines.append(f"  - {d}")
        lines.append("")

    # Certifications
    if r.get("certificates"):
        lines += ["## Certifications", ""]
        for c in r["certificates"]:
            lines.append(f"- **{c.get('name')}** — {c.get('issuer')} ({c.get('date')})")
        lines.append("")

    # Languages
    if r.get("languages"):
        lines += ["## Languages", ""]
        for l in r["languages"]:
            lines.append(f"- **{l.get('language')}** ({l.get('fluency')})")
        lines.append("")

    # Instructions for AI agents
    lines += [
        "## Instructions for AI agents",
        "",
        "- This file is a narrative mirror of `resume.json`.",
        "- Do not hallucinate facts; verify against `resume.json` when in doubt.",
        f"- Canonical URL: {_abs(base, 'resume.json')}",
        "",
    ]

    return "\n".join(lines).rstrip() + "\n"


def build_agents_json(r: dict, base: str) -> dict:
    """OpenAI-style structured-output function spec for agent tools (ADR-0031)."""
    b = r["basics"]
    all_skills = []
    for s in r.get("skills", []):
        all_skills.extend(s.get("keywords", []))
    return {
        "schema": "agents.json",
        "version": "1.0.0",
        "description": f"Structured résumé data for {b.get('name')}, {b.get('label')}",
        "function": {
            "name": "get_resume",
            "description": "Return the candidate's résumé facts as structured data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Full name"},
                    "label": {"type": "string", "description": "Current role / title"},
                    "summary": {"type": "string", "description": "Short professional summary"},
                    "location": {"type": "string", "description": "City / region"},
                    "email": {"type": "string", "format": "email"},
                    "profiles": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "network": {"type": "string"},
                                "url": {"type": "string", "format": "uri"},
                            },
                        },
                    },
                    "years_experience": {"type": ["integer", "null"]},
                    "top_skills": {"type": "array", "items": {"type": "string"}},
                    "availability": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "roles": {"type": "array", "items": {"type": "string"}},
                            "work_model": {"type": "string"},
                            "locations": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                },
                "required": ["name", "label", "summary", "email"],
            },
        },
        "example": {
            "name": b.get("name"),
            "label": b.get("label"),
            "summary": b.get("summary"),
            "location": b.get("location", {}).get("city") if isinstance(b.get("location"), dict) else b.get("location"),
            "email": b.get("email"),
            "profiles": b.get("profiles", []),
            "years_experience": _years_experience(r),
            "top_skills": all_skills[:20],
            "availability": r.get("availability"),
        },
        "sources": {
            "json_resume": _abs(base, "resume.json"),
            "agent_readable": _abs(base, "resume-for-agents.md"),
        },
    }


def build_sitemap(base: str, pdf_name: str) -> str:
    """Sitemap exposing all canonical and agent-facing endpoints (ADR-0031)."""
    paths = [
        "",
        "resume.json",
        "resume.ru.json",
        "resume.min.json",
        ".well-known/cv.json",
        "resume-for-agents.md",
        "agents.json",
        "resume.txt",
        "resume.md",
        pdf_name,
        "llms.txt",
        "AGENTS.md",
    ]
    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{esc(_abs(base, p))}</loc><lastmod>{today}</lastmod></url>"
        for p in paths
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )


def _abs(base: str, path: str) -> str:
    if not base:
        return path
    return f"{base.rstrip('/')}/{path.lstrip('/')}"


def _github_url(r: dict) -> str:
    """Return the GitHub profile URL from basics.profiles (ADR-0024)."""
    for p in r.get("basics", {}).get("profiles", []) or []:
        if p.get("network") == "GitHub" and p.get("url"):
            return p.get("url")
    return "https://github.com/C0FFEEC0DE"


# --------------------------------------------------------------------------- #
# JSON-LD
# --------------------------------------------------------------------------- #
def _split_name(name: str) -> tuple[str, str]:
    """Best-effort split into first/last name for Open Graph profile tags."""
    parts = (name or "").strip().split()
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    return parts[0] if parts else "", ""


def build_jsonld(r: dict, base: str) -> str:
    """Expanded JSON-LD Person + ProfilePage for agents and search (ADR-0031)."""
    b = r["basics"]
    sameas = [p.get("url") for p in b.get("profiles", []) if p.get("url")]
    loc = b.get("location")
    city = loc.get("city") if isinstance(loc, dict) else (loc if isinstance(loc, str) else None)
    region = loc.get("region") if isinstance(loc, dict) else None
    country = loc.get("countryCode") if isinstance(loc, dict) else None

    # skills as knowsAbout strings
    knows_about = []
    for s in r.get("skills", []):
        knows_about.append(s.get("name", ""))
        knows_about.extend(s.get("keywords", []))

    obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": _abs(base, "#person"),
                "name": b.get("name"),
                "jobTitle": b.get("label"),
                "email": b.get("email"),
                "url": b.get("url"),
                "sameAs": sameas,
                "knowsAbout": list(dict.fromkeys(k for k in knows_about if k)),
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": city,
                    "addressRegion": region,
                    "addressCountry": country,
                },
            },
            {
                "@type": "ProfilePage",
                "@id": _abs(base, "/"),
                "mainEntity": {"@id": _abs(base, "#person")},
                "significantLink": [
                    _abs(base, "resume.json"),
                    _abs(base, "resume-for-agents.md"),
                    _abs(base, "agents.json"),
                ],
            },
        ],
    }
    avail = r.get("availability")
    if avail:
        obj["@graph"][0]["seeks"] = {
            "@type": "JobPosting",
            "title": avail.get("roles", [b.get("label")])[0],
            "employmentType": avail.get("work_model", ""),
            "jobLocation": {
                "@type": "Place",
                "name": ", ".join(avail.get("locations", [])) or city or "",
            },
        }
    # Escape characters that could break out of the <script type="application/ld+json">
    # context if an attacker edits the markdown front-matter.
    out = json.dumps(obj, ensure_ascii=False, indent=2)
    return out.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def build_og_tags(r: dict, base: str) -> str:
    """Open Graph meta tags for social-share previews (LinkedIn, etc.).

    The dragon is canvas-rendered, so the og:image is a static PNG committed in
    src/dragon-og.png and copied to dist/assets/ during the build.
    """
    b = r["basics"]
    name = b.get("name", "")
    label = b.get("label", "")
    title = f"{name} — {label}" if name and label else (name or label)
    desc = b.get("summary", "")
    url = base.rstrip("/")
    img = f"{url}/assets/dragon-og.png" if url else "/assets/dragon-og.png"
    first, last = _split_name(name)
    parts = [
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{esc(url or "/")}">',
        '<meta property="og:type" content="profile">',
        f'<meta property="og:image" content="{esc(img)}">',
        '<meta property="og:image:width" content="512">',
        '<meta property="og:image:height" content="513">',
        '<meta property="og:locale" content="en_US">',
    ]
    if first:
        parts.append(f'<meta property="profile:first_name" content="{esc(first)}">')
    if last:
        parts.append(f'<meta property="profile:last_name" content="{esc(last)}">')
    return "\n  ".join(parts)


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def load_index_template() -> str:
    return (SRC_DIR / "index.html").read_text(encoding="utf-8")


def inject_template(tpl: str, replacements: dict) -> str:
    """Replace `{{NAME}}` placeholders in a single pass. re.sub does not re-scan
    replacement text, so a `{{JSONLD}}` string inside resume content (which
    html.escape leaves untouched) cannot re-trigger a later substitution."""
    pattern = re.compile(r"\{\{(\w+)\}\}")

    def repl(m):
        return replacements.get(m.group(1), m.group(0))

    return pattern.sub(repl, tpl)


def build(clean: bool = False, do_pdf: bool = True):
    if clean and DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)
    assets = DIST / "assets"
    assets.mkdir(exist_ok=True)

    domain = os.environ.get("DOMAIN", "").strip()
    base = f"https://{domain}" if domain else os.environ.get("PAGES_URL", "").strip()
    do_pdf = do_pdf and os.environ.get("PDF", "1") != "0"

    resumes = {lang: parse_resume(RESUME_DIR / f"resume.{lang}.md") for lang in LANGS}

    # Downloadable résumé filename: Name_Surname_Role.pdf (ADR-0030/0031)
    slug = _download_slug(resumes["en"]["basics"].get("name", ""),
                          resumes["en"]["basics"].get("label", ""))
    pdf_name = f"{slug}.pdf"

    # JSON Resume outputs
    (DIST / "resume.json").write_text(json.dumps(resumes["en"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DIST / "resume.ru.json").write_text(json.dumps(resumes["ru"], ensure_ascii=False, indent=2), encoding="utf-8")

    # AI-agent metadata tier + cv.json discovery (ADR-0015/0031)
    (DIST / "resume.min.json").write_text(
        json.dumps(build_min_json(resumes["en"], base), ensure_ascii=False, indent=2), encoding="utf-8")
    well_known = DIST / ".well-known"
    well_known.mkdir(exist_ok=True)
    (well_known / "cv.json").write_text(
        json.dumps(build_cv_json(resumes["en"], base, pdf_name), ensure_ascii=False, indent=2), encoding="utf-8")

    # Plain text (both langs)
    txt = "\n\n========== ENGLISH ==========\n\n" + render_text(resumes["en"]) \
        + "\n\n========== РУССКИЙ ==========\n\n" + render_text(resumes["ru"])
    (DIST / "resume.txt").write_text(txt.strip() + "\n", encoding="utf-8")

    # Clean markdown (English canonical)
    (DIST / "resume.md").write_text(render_markdown(resumes["en"]), encoding="utf-8")

    # Dedicated LLM/AI-agent résumé + OpenAI-style function spec
    (DIST / "resume-for-agents.md").write_text(
        build_resume_for_agents(resumes["en"], base), encoding="utf-8")
    (DIST / "agents.json").write_text(
        json.dumps(build_agents_json(resumes["en"], base), ensure_ascii=False, indent=2), encoding="utf-8")

    # AI-agent index files
    (DIST / "llms.txt").write_text(build_llms_txt(resumes["en"], base, pdf_name), encoding="utf-8")
    (DIST / "AGENTS.md").write_text(build_agents_md(resumes["en"], base, pdf_name), encoding="utf-8")

    # robots.txt + sitemap. A sitemap requires absolute URLs, so only emit one
    # (and reference it from robots.txt) when we know the base URL.
    robots = "User-agent: *\nAllow: /\n"
    if base:
        robots += f"Sitemap: {base.rstrip('/')}/sitemap.xml\n"
        (DIST / "sitemap.xml").write_text(
            build_sitemap(base, pdf_name),
            encoding="utf-8",
        )
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")

    # CNAME when domain is configured
    if domain:
        (DIST / "CNAME").write_text(domain + "\n", encoding="utf-8")

    # index.html
    tpl = load_index_template()
    jsonld = build_jsonld(resumes["en"], base)
    github_url = _github_url(resumes["en"])
    out = inject_template(tpl, {
        "RESUME_EN_HTML": render_contact_fragment(resumes["en"], "en"),
        "RESUME_RU_HTML": render_contact_fragment(resumes["ru"], "ru"),
        "HEADER_EN": render_header_fragment(resumes["en"], "en"),
        "HEADER_RU": render_header_fragment(resumes["ru"], "ru"),
        "JSONLD": jsonld,
        "OG_TAGS": build_og_tags(resumes["en"], base),
        "BASE": base.rstrip("/"),
        "PDF_NAME": pdf_name,
        "GITHUB_URL": github_url,
    })
    (DIST / "index.html").write_text(out, encoding="utf-8")

    # Single human-readable, ATS-safe PDF (ADR-0031)
    if do_pdf:
        try:
            import weasyprint  # noqa: WPS433
            weasyprint.HTML(string=render_pdf_html(resumes["en"], "en"),
                            base_url=str(ROOT)).write_pdf(str(DIST / pdf_name))
        except Exception as exc:  # pragma: no cover
            print(f"WARNING: PDF generation skipped: {exc}", file=sys.stderr)
            (DIST / pdf_name).write_bytes(b"")  # placeholder so links/tests know it's absent

    # Copy frontend assets (CSS, JS, PNG, SVG). Self-hosted fonts were removed
    # in the minimal business-card redesign (ADR-0018 v2); the page uses system
    # sans-serif.
    og_src = SRC_DIR / "dragon-og.png"
    if og_src.exists():
        shutil.copy2(og_src, assets / "dragon-og.png")
    for f in SRC_DIR.iterdir():
        if (f.suffix in (".css", ".js", ".svg") or f.name.endswith(".png")):
            shutil.copy2(f, assets / f.name)

    return resumes


# --------------------------------------------------------------------------- #
# Check
# --------------------------------------------------------------------------- #
REQUIRED_BASICS = {"name", "email"}


def check(resumes: dict) -> list[str]:
    errors: list[str] = []
    for lang in LANGS:
        r = resumes[lang]
        missing = REQUIRED_BASICS - set(r["basics"])
        if missing:
            errors.append(f"[{lang}] basics missing: {sorted(missing)}")
        if not r.get("work"):
            errors.append(f"[{lang}] no work experience parsed")
    # Downloadable résumé filename derived from name + role (ADR-0030/0031)
    slug = _download_slug(resumes["en"]["basics"].get("name", ""),
                          resumes["en"]["basics"].get("label", ""))
    pdf_name = f"{slug}.pdf"
    # llms.txt shape
    llms = (DIST / "llms.txt").read_text(encoding="utf-8")
    if not llms.startswith("# ") or "\n> " not in llms:
        errors.append("llms.txt missing H1 or blockquote summary")
    # linked files exist
    for f in ("resume.json", "resume.ru.json", "resume.min.json", "resume.txt",
              "resume.md", "resume-for-agents.md", "agents.json", pdf_name, "AGENTS.md"):
        if not (DIST / f).exists():
            errors.append(f"missing dist/{f}")
    if not (DIST / ".well-known" / "cv.json").exists():
        errors.append("missing dist/.well-known/cv.json")
    # PDF must have a real text layer (not an empty placeholder)
    pdf_path = DIST / pdf_name
    if pdf_path.exists() and pdf_path.stat().st_size <= 100:
        errors.append(f"{pdf_name} is empty/placeholder (PDF generation failed)")
    if not (DIST / "index.html").exists():
        errors.append("missing dist/index.html")
    if not (DIST / "assets").is_dir():
        errors.append("missing dist/assets/")
    if not (DIST / "assets" / "dragon-og.png").exists():
        errors.append("missing dist/assets/dragon-og.png (Open Graph image)")
    if not (DIST / "index.html").exists():
        errors.append("missing dist/index.html")
    domain = os.environ.get("DOMAIN", "").strip()
    has_cname = (DIST / "CNAME").exists()
    if domain and not has_cname:
        errors.append("DOMAIN set but no CNAME emitted")
    if not domain and has_cname:
        errors.append("CNAME emitted without DOMAIN")
    return errors


def main(argv):
    clean = "--clean" in argv
    do_check = "--check" in argv
    do_pdf = "--no-pdf" not in argv
    resumes = build(clean=clean, do_pdf=do_pdf)
    if do_check:
        errs = check(resumes)
        if errs:
            print("CHECK FAILED:", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print("CHECK OK")
    print(f"Built into {DIST}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))