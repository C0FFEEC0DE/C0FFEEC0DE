"""Tests for build/build.py.

Run from repo root:  python -m pytest build/test_build.py -q
"""
import json
import os
import sys

import pytest

# make `import build` resolve to build/build.py (no package __init__ needed)
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import build  # noqa: E402


@pytest.fixture
def dist(tmp_path, monkeypatch):
    """Point build.DIST at a temp dir so tests never pollute the real dist/.
    Use a subdir of tmp_path so build(clean=True) doesn't wipe co-located
    fixtures (e.g. the attacked resume sources)."""
    monkeypatch.setattr(build, "DIST", tmp_path / "dist")
    # a base URL is set so llms.txt/sitemap get absolute URLs (as in CI)
    monkeypatch.delenv("DOMAIN", raising=False)
    monkeypatch.setenv("PAGES_URL", "https://user.github.io/C0FFEEC0DE")
    monkeypatch.setenv("PDF", "1")
    yield tmp_path / "dist"


@pytest.fixture
def resume_md_attacked(tmp_path):
    """Write resume markdown whose content is hostile to confirm it is escaped."""
    rdir = tmp_path / "resume"
    rdir.mkdir()
    payload = (
        "---\n"
        "basics:\n"
        '  name: "</script><script>alert(1)</script>"\n'
        "  label: x\n"
        "  email: a@b.co\n"
        "  location: Berlin\n"  # a string, not a dict — must not crash
        "---\n\n"
        "## Summary\n"
        "fine\n\n"
        "## Experience\n"
        "### Role — Co\n"
        "dates: 2020 — present\n"
        "- {{JSONLD}} should not be substituted\n"
        "- <b>bold</b> and <script>alert(2)</script>\n"
    )
    (rdir / "resume.en.md").write_text(payload, encoding="utf-8")
    (rdir / "resume.ru.md").write_text(payload, encoding="utf-8")
    return rdir


# --- structure -------------------------------------------------------------- #
def test_build_produces_core_files(dist):
    build.build(clean=True)
    for f in ("index.html", "resume.json", "resume.ru.json", "resume.min.json",
              "resume.txt", "resume.md", "resume.pdf", "resume-branded.pdf",
              "llms.txt", "AGENTS.md", "robots.txt", "sitemap.xml"):
        assert (dist / f).is_file(), f"missing {f}"
    assert (dist / ".well-known" / "cv.json").is_file(), "missing .well-known/cv.json"
    assert (dist / "assets" / "site.css").is_file()
    assert (dist / "assets" / "print.css").is_file()
    assert (dist / "assets" / "dragon.js").is_file()


def test_resume_json_valid(dist):
    build.build(clean=True)
    r = json.loads((dist / "resume.json").read_text("utf-8"))
    assert r["basics"]["name"] == "Aleksandr Krasnobai"
    assert r["basics"]["email"]
    assert r["basics"]["profiles"], "profiles should parse from front-matter"
    assert r["work"], "work experience should parse"
    assert r["work"][0]["position"]
    assert r["work"][0]["name"] == "Grid Dynamics"
    assert r["work"][0]["highlights"], "highlights should parse"
    assert r["skills"], "skills should parse"
    assert r["projects"], "projects should parse"
    assert r["certificates"], "certificates should parse"
    assert r["languages"], "languages should parse"
    assert r["languages"][0]["fluency"] == "Professional working"


def test_russian_resume_json(dist):
    build.build(clean=True)
    r = json.loads((dist / "resume.ru.json").read_text("utf-8"))
    assert "инженер" in r["basics"]["label"].lower()
    assert r["work"][0]["name"] == "Grid Dynamics"


def test_resume_txt_has_both_langs(dist):
    build.build(clean=True)
    txt = (dist / "resume.txt").read_text("utf-8")
    assert "ENGLISH" in txt
    assert "РУССКИЙ" in txt


# --- agent-facing ------------------------------------------------------------ #
def test_metadata_tier(dist):
    build.build(clean=True)
    m = json.loads((dist / "resume.min.json").read_text("utf-8"))
    assert m["name"] == "Aleksandr Krasnobai"
    assert m["label"]
    assert isinstance(m["top_skills"], list) and m["top_skills"]
    # years_experience is derived from work start dates; until the owner fills
    # the Grid Dynamics start date it is None, which is valid.
    assert m.get("years_experience") is None or m["years_experience"] >= 1
    assert m["full"].endswith("resume.json")
    assert m["availability"]["status"] == "open"  # hiring signals surfaced


def test_cv_json_discovery(dist):
    build.build(clean=True)
    cv = json.loads((dist / ".well-known" / "cv.json").read_text("utf-8"))
    assert cv["schema"] == "cv.json"
    assert cv["primary"].endswith("resume.json")
    assert cv["languages"]["ru"].endswith("resume.ru.json")
    assert cv["metadata_tier"].endswith("resume.min.json")


def test_two_pdfs(dist):
    try:
        import weasyprint  # noqa: F401
    except Exception:
        pytest.skip("weasyprint not installed")
    build.build(clean=True)
    ats = dist / "resume.pdf"
    branded = dist / "resume-branded.pdf"
    assert ats.read_bytes()[:4] == b"%PDF" and ats.stat().st_size > 1000
    assert branded.read_bytes()[:4] == b"%PDF" and branded.stat().st_size > 1000


def test_availability_in_resume_json(dist):
    build.build(clean=True)
    r = json.loads((dist / "resume.json").read_text("utf-8"))
    assert r["availability"]["work_model"] == "remote"


def test_llms_txt_shape(dist):
    build.build(clean=True)
    llms = (dist / "llms.txt").read_text("utf-8")
    assert llms.startswith("# "), "llms.txt must start with H1"
    assert "\n> " in llms, "llms.txt must have a blockquote summary"
    assert "resume.json" in llms
    assert "resume.txt" in llms
    assert "AGENTS.md" in llms


def test_agents_md_links(dist):
    build.build(clean=True)
    md = (dist / "AGENTS.md").read_text("utf-8")
    assert "resume.json" in md
    assert "JSON Resume" in md


def test_index_html_injected(dist):
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    assert "{{" not in html, "template placeholders must be replaced"
    assert "{{RESUME_EN_HTML}}" not in html
    assert "Krasnobai" in html
    assert 'application/ld+json' in html
    assert '"@type": "Person"' in html or '"@type":"Person"' in html


# --- domain / CNAME --------------------------------------------------------- #
def test_no_cname_without_domain(dist):
    build.build(clean=True)
    assert not (dist / "CNAME").exists()


def test_cname_with_domain(dist, monkeypatch):
    monkeypatch.setenv("DOMAIN", "krasnobai.dev")
    build.build(clean=True)
    assert (dist / "CNAME").read_text("utf-8").strip() == "krasnobai.dev"
    # llms.txt should then use absolute URLs
    assert "https://krasnobai.dev/resume.json" in (dist / "llms.txt").read_text("utf-8")


# --- PDF -------------------------------------------------------------------- #
def test_pdf_generated(dist):
    try:
        import weasyprint  # noqa: F401
    except Exception:
        pytest.skip("weasyprint not installed")
    build.build(clean=True)
    pdf = dist / "resume.pdf"
    assert pdf.is_file()
    assert pdf.stat().st_size > 100, "PDF should not be empty"
    assert pdf.read_bytes()[:4] == b"%PDF"


# --- check() ---------------------------------------------------------------- #
def test_check_passes(dist):
    build.build(clean=True)
    errs = build.check({"en": {"basics": {"name": "x", "email": "y"}, "work": [{}]},
                        "ru": {"basics": {"name": "x", "email": "y"}, "work": [{}]}})
    # those minimal dicts satisfy required fields; llms.txt etc. were built
    assert errs == []


def test_check_flags_missing_basics(dist):
    build.build(clean=True)
    errs = build.check({"en": {"basics": {}, "work": []}, "ru": {"basics": {}, "work": []}})
    assert any("basics missing" in e for e in errs)
    assert any("no work experience" in e for e in errs)


def test_cli_check_exits_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(build, "DIST", tmp_path)
    monkeypatch.delenv("DOMAIN", raising=False)
    code = build.main(["--check"])
    assert code == 0


# --- security: escaping / injection (review findings #1, #2, #3) ------------- #
def test_attacked_resume_does_not_crash(dist, resume_md_attacked, monkeypatch):
    """A string `location` and odd front-matter must not raise (finding #3)."""
    monkeypatch.setattr(build, "RESUME_DIR", resume_md_attacked)
    build.build(clean=True)  # must not raise
    r = json.loads((dist / "resume.json").read_text("utf-8"))
    assert r["basics"]["name"]


def test_jsonld_script_breakout_escaped(dist, resume_md_attacked, monkeypatch):
    """A `</script>` in a front-matter field must not break out of the JSON-LD
    block (finding #1)."""
    monkeypatch.setattr(build, "RESUME_DIR", resume_md_attacked)
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    assert "<script>alert(1)</script>" not in html
    # JSON-LD block present and intact (escaped form, not raw markup)
    assert "application/ld+json" in html


def test_no_placeholder_injection_into_body(dist, resume_md_attacked, monkeypatch):
    """A `{{JSONLD}}` token in resume content must stay literal, not be
    substituted when the content is injected as a template value (finding #2).
    The body no longer renders into index.html (ADR-0025), so test the
    protection directly: body HTML used as a replacement value is not re-scanned
    by inject_template's single-pass re.sub."""
    monkeypatch.setattr(build, "RESUME_DIR", resume_md_attacked)
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    # the JSON-LD @context appears exactly once (in its own <script>), not leaked
    assert html.count('"@context"') == 1
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    body = build.render_body_fragment(en, "en")
    # body content carrying {{JSONLD}} is injected as a VALUE, not re-scanned,
    # so the token survives literal and the JSON-LD block is not substituted in
    out = build.inject_template("{{RESUME_EN_HTML}}",
                                {"RESUME_EN_HTML": body, "JSONLD": "LEAKED-JSONLD"})
    assert "{{JSONLD}}" in out
    assert "LEAKED-JSONLD" not in out


def test_resume_html_escapes_script(dist, resume_md_attacked, monkeypatch):
    """`<script>` inside highlights must be HTML-escaped in the rendered body.
    Highlights render into the branded-PDF body now, not index.html (ADR-0025),
    so check render_body_fragment directly."""
    monkeypatch.setattr(build, "RESUME_DIR", resume_md_attacked)
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    body = build.render_body_fragment(en, "en")
    assert "<script>alert(2)</script>" not in body
    assert "&lt;script&gt;" in body


def test_sitemap_only_with_base(dist, monkeypatch):
    """Sitemap requires absolute URLs; with no base it is omitted (finding #5)."""
    monkeypatch.delenv("PAGES_URL", raising=False)
    monkeypatch.delenv("DOMAIN", raising=False)
    build.build(clean=True)
    assert not (dist / "sitemap.xml").exists()
    assert "Sitemap:" not in (dist / "robots.txt").read_text("utf-8")


# --- no-duplication: header lives once in the hero, body has no header ------- #
def test_resume_body_has_no_header(dist):
    """The résumé block must NOT contain its own <header class="hero"> — the
    name/label/summary live once in the hero (regression for the duplicated
    blocks bug)."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    resume = html[html.find('id="resume"'):]
    assert '<header class="hero">' not in resume
    assert "<h1>" not in resume


def test_hero_has_one_h1_per_language(dist):
    """The hero holds exactly one <h1> per language block (EN visible, RU
    hidden) — so a single visible name, not a duplicate."""
    import re
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    hero_end = html.find('id="resume"')
    hero = html[:hero_end]
    h1s = re.findall(r"<h1>.*?</h1>", hero, re.S)
    assert len(h1s) == 2, f"expected one h1 per language in hero, got {len(h1s)}"
    assert all("Krasnobai" in h for h in h1s)
    # the EN block is visible, the RU block is hidden by default
    assert 'data-lang="en"' in hero
    assert 'data-lang="ru" hidden' in hero


def test_hero_header_is_bilingual(dist):
    """Both language headers are injected; the RU label is Russian, not the
    hardcoded English one (regression for the EN-only hero-label bug)."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    hero = html[: html.find('id="resume"')]
    assert "Senior DevOps / SRE Engineer" in hero
    assert "Старший DevOps / SRE-инженер" in hero
    # no leftover template placeholders
    assert "{{HEADER_EN}}" not in html and "{{HEADER_RU}}" not in html


def test_render_body_fragment_has_no_header(dist):
    """render_body_fragment (used for the résumé block) must not emit a header
    or h1; render_html_fragment (used for the branded PDF) must."""
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    body = build.render_body_fragment(en, "en")
    full = build.render_html_fragment(en, "en")
    assert "<header class=\"hero\">" not in body
    assert "<h1>" not in body
    assert "<header class=\"hero\">" in full
    assert "<h1>" in full


def test_landing_page_shows_contact_only(dist):
    """ADR-0025: the landing #resume block shows Contact only — the full résumé
    body (Experience, Skills, Projects, Education, Certificates, Languages)
    lives in the branded PDF, not on the page. Guards against re-injecting
    render_body_fragment into the landing page."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    resume = html[html.find('id="resume"'):html.find("<footer")]
    # Contact is the one block kept (both languages)
    assert "Contact" in resume and "Контакты" in resume
    # none of the other résumé sections leak onto the landing page
    for absent in ("Work Experience", "Skills", "Projects", "Education",
                   "Certificates", "Languages", "Опыт работы", "Навыки",
                   "Проекты", "Образование", "Сертификаты", "Языки"):
        assert absent not in resume, f"landing page leaked section: {absent}"
    # the branded PDF body still carries the full résumé
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    body = build.render_body_fragment(en, "en")
    assert "Work Experience" in body
    assert "Skills" in body


# --- ATS format: single column, standard font, real text, no graphics ------- #
def test_ats_is_single_column_standard_font(dist):
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    ats = build.render_ats_html(en, "en")
    assert "Arial, Helvetica" in ats            # standard ATS font
    assert "column-count" not in ats            # no multi-column
    assert "float:" not in ats                  # no floats
    assert "<canvas" not in ats and "<img" not in ats  # no graphics


def test_ats_dates_formatted_on_role(dist):
    """ATS date ranges render as 'Mon YYYY – Present', not raw YYYY-MM. The
    formatter is unit-checked directly (the real résumé's first role date is a
    TODO placeholder until the owner fills it, so the format check is decoupled
    from the live data); the integration check only verifies raw ISO never
    leaks into the ATS render."""
    assert build._fmt_ats("2022-03", None, "en") == "Mar 2022 – Present"
    assert build._fmt_ats("2022-03", "2024-05", "en") == "Mar 2022 – May 2024"
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    ats = build.render_ats_html(en, "en")
    assert "2022-03" not in ats                  # raw ISO date must not leak


def test_ats_has_real_selectable_text(dist):
    """ATS body uses real text in headings/bullets, not images or tables."""
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    ats = build.render_ats_html(en, "en")
    assert "<table" not in ats
    assert "<h3>" in ats and "Senior DevOps Engineer" in ats
    assert "<ul>" in ats and "<li>" in ats


# --- metadata tier + JSON-LD + sitemap -------------------------------------- #
def test_min_json_shape(dist):
    build.build(clean=True)
    m = json.loads((dist / "resume.min.json").read_text("utf-8"))
    for k in ("name", "label", "top_skills", "years_experience", "full", "availability"):
        assert k in m, f"metadata tier missing {k}"
    assert m["availability"]["status"] == "open"
    assert m["availability"]["work_model"] == "remote"
    assert isinstance(m["availability"].get("roles"), list) and m["availability"]["roles"]


def test_jsonld_is_person_with_name(dist):
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    assert '"@type": "Person"' in html or '"@type":"Person"' in html
    assert "Aleksandr Krasnobai" in html
    assert "@context" in html and "schema.org" in html


def test_sitemap_has_urls(dist):
    """With a base URL set, sitemap.xml is a valid urlset with loc entries."""
    build.build(clean=True)
    sx = (dist / "sitemap.xml").read_text("utf-8")
    assert sx.lstrip().startswith("<?xml")
    assert "<urlset" in sx
    assert "<loc>https://user.github.io/C0FFEEC0DE/" in sx


def test_resume_txt_languages_and_fluency(dist):
    build.build(clean=True)
    txt = (dist / "resume.txt").read_text("utf-8")
    assert "English (Professional working)" in txt
    assert "Russian (native)" in txt


def test_resume_md_is_clean_markdown(dist):
    build.build(clean=True)
    md = (dist / "resume.md").read_text("utf-8")
    assert md.lstrip().startswith("# Aleksandr Krasnobai")
    assert "## Experience" in md
    assert "## Skills" in md
    # no front-matter / HTML comments / script tags leaked into the mirror
    assert not md.lstrip().startswith("---")
    assert "<!--" not in md
    assert "<script" not in md


# --- hero CTA: two explicit links — human PDF + machine/AI résumé ----------- #
def test_hero_cta_has_two_audience_links(dist):
    """The hero has exactly two primary links with distinct audiences: the
    human PDF (resume.pdf) and the machine/AI résumé (resume.json). The
    branded PDF is NOT in the hero (it lives in the footer)."""
    import re
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    cta = re.search(r'<div class="cta">(.*?)</div>', html, re.S).group(1)
    links = re.findall(r'href="([^"]+)"', cta)
    assert "resume.pdf" in links, "hero must link the human PDF"
    assert "resume.json" in links, "hero must link the machine/AI résumé"
    assert "resume-branded.pdf" not in links, "branded PDF stays in the footer"
    assert len(links) == 2, f"hero CTA should have two links, got {links}"


def test_ai_link_label_is_bilingual(dist):
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    assert 'data-i18n="ai_resume"' in html


# --- ADR-0017: single Forest theme + ADR-0018 human feel -------------------- #
def test_single_forest_theme_no_picker(dist):
    """ADR-0017 was reduced to a single Forest theme per owner preference: the
    palette picker is gone, there is no data-palette attribute anywhere, and
    Forest is the bare :root default. The human feel (ADR-0018) — self-hosted
    JetBrains Mono headings + OFL license — is still present."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    # the palette picker must be gone
    assert 'id="palette-select"' not in html, "palette picker should be removed"
    assert "palette-pick" not in html, "palette-pick label should be removed"
    css = (dist / "assets" / "site.css").read_text("utf-8")
    # no data-palette attribute anywhere — Forest is the bare :root default
    assert "data-palette" not in css, "no data-palette should remain in CSS"
    # ADR-0018: JetBrains Mono headings + self-hosted woff2
    assert "--c-head-font:" in css and "JetBrains Mono" in css
    assert "@font-face" in css and "jetbrains-mono-400.woff2" in css
    for w in ("jetbrains-mono-400.woff2", "jetbrains-mono-700.woff2"):
        assert (dist / "assets" / w).is_file(), f"missing {w} in assets"
    # OFL-1.1 requires the license accompany redistribution
    assert (dist / "assets" / "jetbrains-mono-LICENSE.txt").is_file(), (
        "JetBrains Mono OFL license must ship with the font")


def test_forest_has_light_and_dark_blocks(dist):
    """The single Forest theme defines a bare :root (light) block and a
    :root[data-theme="dark"] block, and the dark block declares the same full
    --c-* var set as the light block so dark mode fully overrides light (no
    light value can leak through in dark mode)."""
    import re
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    light = re.search(r"(?<![\w-]):root\s*\{([^}]*)\}", css)
    assert light, "bare :root (light) block missing"
    dark = re.search(r':root\[data-theme="dark"\]\s*\{([^}]*)\}', css)
    assert dark, ":root[data-theme=dark] block missing"
    light_vars = set(re.findall(r"--(c-[a-z-]+)\s*:", light.group(1)))
    dark_vars = set(re.findall(r"--(c-[a-z-]+)\s*:", dark.group(1)))
    assert light_vars, "light block declares no --c-* vars"
    # --c-head-font is mode-independent (the font stack doesn't flip with mode),
    # so the dark block intentionally omits it; every other --c-* color token
    # that light declares must be re-declared in dark so no light color leaks.
    mode_sensitive = light_vars - {"c-head-font"}
    assert dark_vars == mode_sensitive, (
        f"dark var set {dark_vars} != light color set {mode_sensitive}; a missing "
        "var would let the light value leak through in dark mode")
    # the canonical Forest values are present
    assert "--c-accent: #2f7d3a" in light.group(1), "forest light accent wrong"
    assert "--c-accent: #7cc68a" in dark.group(1), "forest dark accent wrong"


def test_branded_pdf_palette_matches_forest(dist):
    """The branded PDF (src/print.css, rendered via WeasyPrint) must use the
    Forest palette, not the old calm blue/brown — so the downloadable PDF
    matches the on-screen Forest theme (the @cr review caught it drifting to
    the pre-reduction calm colors)."""
    build.build(clean=True)
    css = (build.SRC_DIR / "print.css").read_text("utf-8")
    assert "#2f7d3a" in css, "branded PDF must use the Forest green accent"
    assert "#3a5ae0" not in css, "old calm blue accent must not survive in print.css"
    assert "#2a2620" not in css, "old calm brown text must not survive in print.css"


def test_no_js_dark_query_is_scoped_to_no_js(dist):
    """Every prefers-color-scheme:dark selector must be scoped to no-JS
    (data-theme absent) so it only applies before JS sets data-theme —
    otherwise it would pollute JS-on dark mode (static guard for the @cr no-JS
    verification gap, since Playwright always runs with JS on)."""
    import re
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    # the no-JS scoped selector must exist (forest-dark + button-text dark rules)
    assert ":not([data-theme=\"light\"]):not([data-theme=\"dark\"])" in css, (
        "no-JS scoped dark selector missing")
    # no UN-scoped ":root:not([data-theme=\"light\"])" may remain — i.e. every
    # occurrence must be immediately followed by ":not([data-theme=\"dark\"])".
    broad = re.findall(
        r":root:not\(\[data-theme=\"light\"]\)(?!\s*:not\(\[data-theme=\"dark\"]\))",
        css,
    )
    assert not broad, f"un-scoped prefers-dark selector still present: {broad}"


# --- ADR-0019: automated WCAG contrast guard for the single theme/mode ------- #
def _hex_lum(color):
    """Relative luminance of a #rgb / #rrggbb color (sRGB, WCAG 2.x)."""
    h = color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    R, G, B = lin(r), lin(g), lin(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def _contrast(fg, bg):
    a, b = _hex_lum(fg), _hex_lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def _theme_vars(css):
    """Parse site.css into {"light": {var: hex}, "dark": {...}} from the
    top-level :root (light) and :root[data-theme="dark"] (dark) blocks.
    Top-level only: the @media print :root and the no-JS media :root:not(...)
    are nested inside @media, so the brace-depth walker sees them as the body
    of the @media rule, not as top-level selectors — they are skipped."""
    import re
    out = {}
    i, n = 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            break
        selector = css[i:brace].strip()
        depth, j = 1, brace + 1
        while j < n and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        body = css[brace + 1:j - 1]
        i = j
        if selector == ":root":
            mode = "light"
        elif selector == ':root[data-theme="dark"]':
            mode = "dark"
        else:
            continue  # @media blocks, component rules, etc. — not theme blocks
        vals = dict(re.findall(r"--(c-[a-z-]+)\s*:\s*(#[0-9a-fA-F]{3,8})", body))
        out[mode] = vals
    return out


def test_forest_theme_meets_aa_contrast(dist):
    """ADR-0019: compute WCAG contrast for the Forest theme, light AND dark, and
    assert AA (>=4.5:1) for body text, muted text, link/accent text on both the
    page background and the block surface, plus filled-button text on the
    accent. Machine-enforced so a future color edit can't silently regress."""
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    theme = _theme_vars(css)
    assert set(theme) == {"light", "dark"}, f"parsed modes {sorted(theme)}"

    # filled button / active-toggle text color: white in light, near-black in dark
    BTN_FG = {"light": "#ffffff", "dark": "#15171c"}
    failures = []
    for mode in ("light", "dark"):
        v = theme[mode]
        for key in ("c-bg", "c-surface", "c-text", "c-muted", "c-accent"):
            assert v.get(key), f"{mode}: missing --{key}"
        bg, surface = v["c-bg"], v["c-surface"]
        text, muted, accent = v["c-text"], v["c-muted"], v["c-accent"]
        # Block interiors (.block { background: var(--c-surface) }) hold most of
        # the page's text — summary, meta, role, contact links — so contrast must
        # be enforced against c-surface too, not only c-bg.
        checks = {
            "text/bg": (text, bg),
            "muted/bg": (muted, bg),
            "accent/bg (link text)": (accent, bg),
            "text/surface (block body)": (text, surface),
            "muted/surface (block meta)": (muted, surface),
            "accent/surface (block link)": (accent, surface),
            "button-fg/accent": (BTN_FG[mode], accent),
        }
        for name, (fg, b) in checks.items():
            r = _contrast(fg, b)
            if r < 4.5:
                failures.append(f"{mode} {name} {fg} on {b} = {r:.2f}:1")
    assert not failures, (
        "WCAG AA (<4.5:1) contrast failures:\n  " + "\n  ".join(failures))


def test_button_text_color_matches_mode(dist):
    """The filled-button text color must be white in light and #15171c in dark
    (the global rule), so the contrast guard's BTN_FG assumption holds — a
    future edit that flips this would otherwise make the contrast guard test
    the wrong pair."""
    import re
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    # light: .btn-primary --bs-btn-color: #fff
    assert re.search(r"\.btn-primary\s*\{[^}]*--bs-btn-color:\s*#fff", css), (
        "light .btn-primary must use white text")
    # dark: :root[data-theme="dark"] .btn-primary --bs-btn-color: #15171c
    assert ':root[data-theme="dark"] .btn-primary' in css
    assert re.search(
        r':root\[data-theme="dark"\]\s*\.btn-primary\s*\{[^}]*--bs-btn-color:\s*#15171c',
        css), "dark .btn-primary must use #15171c text"


# --- ADR-0024: contact profiles are GitHub, LinkedIn (supersedes ADR-0016) --- #
def test_contact_profiles_required_set(dist):
    """Both language files must carry the ADR-0024 contact set, in order, and
    no stray Website profile (the site URL lives in basics.url, not profiles)."""
    build.build(clean=True)
    expected = ["GitHub", "LinkedIn"]
    for fn in ("resume.json", "resume.ru.json"):
        r = json.loads((dist / fn).read_text("utf-8"))
        networks = [p.get("network") for p in r["basics"].get("profiles", [])]
        assert networks == expected, f"{fn} profiles = {networks}"
        assert "Website" not in networks
    # ADR-0024: Telegram is no longer a contact channel — it must not leak into
    # any audience surface. The contact set reaches EVERY audience, not just JSON.
    en_resume = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    assert "t.me/" not in build.render_ats_html(en_resume, "en")      # ATS PDF
    assert "t.me/" not in build.render_body_fragment(en_resume, "en")  # branded PDF body
    html = (dist / "index.html").read_text("utf-8")
    assert "t.me/" not in html
    assert "Telegram" not in (dist / "resume.txt").read_text("utf-8")
    assert "Telegram" not in (dist / "llms.txt").read_text("utf-8")             # LLM index
    assert "t.me/" not in (dist / "llms.txt").read_text("utf-8")
    assert "Telegram" not in (dist / "resume.md").read_text("utf-8")             # markdown mirror
    assert "t.me/" not in (dist / "resume.md").read_text("utf-8")