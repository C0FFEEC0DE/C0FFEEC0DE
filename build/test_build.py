"""Tests for build/build.py.

Run from repo root:  python -m pytest build/test_build.py -q
"""
import json
import os
import re
import sys

import pytest

# make `import build` resolve to build/build.py (no package __init__ needed)
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import build  # noqa: E402


# Expected downloadable résumé filename from name + role (ADR-0030/0031)
PDF_NAME = "Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf"


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
              "resume.txt", "resume.md", "resume-for-agents.md", "agents.json",
              PDF_NAME, "llms.txt", "AGENTS.md", "robots.txt", "sitemap.xml"):
        assert (dist / f).is_file(), f"missing {f}"
    assert (dist / ".well-known" / "cv.json").is_file(), "missing .well-known/cv.json"
    assert (dist / "assets" / "site.css").is_file()
    assert (dist / "assets" / "print.css").is_file()
    assert (dist / "assets" / "dragon.js").is_file()
    assert (dist / "assets" / "dragon-og.png").is_file(), "missing Open Graph image"


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


def test_russian_resume_json(dist):
    build.build(clean=True)
    r = json.loads((dist / "resume.ru.json").read_text("utf-8"))
    assert "инженер" in r["basics"]["label"].lower()
    assert r["work"][0]["name"] == "Grid Dynamics"
    assert r["languages"], "languages should parse"


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
    assert cv["agent_readable"].endswith("resume-for-agents.md")
    assert cv["agent_spec"].endswith("agents.json")
    assert cv["human_pdf"] == cv["ats_pdf"]
    assert PDF_NAME in cv["human_pdf"]


def test_single_pdf(dist):
    try:
        import weasyprint  # noqa: F401
    except Exception:
        pytest.skip("weasyprint not installed")
    build.build(clean=True)
    pdf = dist / PDF_NAME
    assert pdf.read_bytes()[:4] == b"%PDF" and pdf.stat().st_size > 1000
    assert not (dist / PDF_NAME.replace(".pdf", "_branded.pdf")).exists()


def test_availability_in_resume_json(dist):
    build.build(clean=True)
    r = json.loads((dist / "resume.json").read_text("utf-8"))
    work_model = r["availability"]["work_model"]
    assert "remote" in work_model, f"availability work_model missing remote: {work_model}"


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
    pdf = dist / PDF_NAME
    assert pdf.is_file()
    assert pdf.stat().st_size > 100, "PDF should not be empty"
    assert pdf.read_bytes()[:4] == b"%PDF"


def _pdf_text(pdf_path):
    """Extract all text from a PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except Exception:
        pytest.skip("pypdf not installed")
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def test_pdf_is_machine_readable(dist):
    """The single human-readable/ATS-safe PDF must contain selectable text for
    the key facts: name, role, company, skills, experience, and contact links."""
    try:
        import weasyprint  # noqa: F401
    except Exception:
        pytest.skip("weasyprint not installed")
    build.build(clean=True)
    text = _pdf_text(dist / PDF_NAME)
    assert "Aleksandr Krasnobai" in text, "PDF missing name"
    assert "Staff DevOps Engineer" in text, "PDF missing role"
    assert "Grid Dynamics" in text, "PDF missing company"
    assert "hi@krasnobai.dev" in text, "PDF missing email"
    assert "linkedin.com/in/" in text and "aleksandrkrasnobai" in text, "PDF missing LinkedIn"
    assert "t.me/krasnobaicoach" in text, "PDF missing Telegram"
    # skills rendered as real text
    assert any(k in text for k in ("Kubernetes", "Terraform", "AWS", "Python")), "PDF missing skills"
    assert "Experience" in text, "PDF missing Experience section"


def test_pdf_contacts_are_readable(dist):
    """The single PDF exposes contact details as real text: email + LinkedIn +
    Telegram labels and full URLs."""
    try:
        import weasyprint  # noqa: F401
    except Exception:
        pytest.skip("weasyprint not installed")
    build.build(clean=True)

    text = _pdf_text(dist / PDF_NAME)
    assert "hi@krasnobai.dev" in text, "PDF missing email"
    assert "linkedin.com/in/" in text and "aleksandrkrasnobai" in text, "PDF missing LinkedIn URL"
    assert "t.me/krasnobaicoach" in text, "PDF missing Telegram URL"
    assert "LinkedIn" in text, "PDF missing LinkedIn label"
    assert "Telegram" in text, "PDF missing Telegram label"
    assert "GitHub" in text, "PDF missing GitHub label"


def test_pdf_formatting_is_intact(dist):
    """The generated PDF must not have obvious layout corruption: every page is
    within standard US-letter dimensions and has real text."""
    try:
        from pypdf import PdfReader
    except Exception:
        pytest.skip("pypdf not installed")
    try:
        import weasyprint  # noqa: F401
    except Exception:
        pytest.skip("weasyprint not installed")
    build.build(clean=True)
    reader = PdfReader(str(dist / PDF_NAME))
    assert len(reader.pages) >= 1, f"{PDF_NAME} has no pages"
    for i, page in enumerate(reader.pages):
        box = page.mediabox
        w, h = float(box.width), float(box.height)
        # standard page sizes with tolerance (letter / A4 in points)
        assert 400 <= w <= 650, f"{PDF_NAME} page {i} width {w} looks corrupt"
        assert 500 <= h <= 850, f"{PDF_NAME} page {i} height {h} looks corrupt"
        text = page.extract_text() or ""
        assert len(text.strip()) > 20, f"{PDF_NAME} page {i} has almost no text"


# --- check() ---------------------------------------------------------------- #
def test_check_passes(dist):
    build.build(clean=True)
    # Validate the actual dist output, which is built from the real résumé
    # sources. The downloadable PDF filenames depend on name + role, so check()
    # must see the real resumes to know which files to expect.
    real = {
        "en": build.parse_resume(build.RESUME_DIR / "resume.en.md"),
        "ru": build.parse_resume(build.RESUME_DIR / "resume.ru.md"),
    }
    errs = build.check(real)
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
    """The Contact block (#resume) must NOT contain an <h1> — the name lives
    once in the hero (regression for the duplicated blocks bug)."""
    import re
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    # Slice only the first <section id="resume"> block (class may precede id).
    m = re.search(r'<section[^>]*\sid="resume"[^>]*>(.*?)\n\s*</section>', html, re.S)
    assert m, "#resume section not found"
    resume = m.group(1)
    assert '<header class="hero">' not in resume
    assert "<h1>" not in resume


def test_hero_has_one_h1_per_language(dist):
    """The hero holds exactly one <h1> per language block (EN visible, RU
    hidden) — so a single visible name, not a duplicate."""
    import re
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    # Extract the hero section by class; it now follows the Contact section.
    m = re.search(r'<section class="hero"[^>]*>(.*?)\n\s*</section>', html, re.S)
    assert m, "hero section not found"
    hero = m.group(1)
    h1s = re.findall(r"<h1>.*?</h1>", hero, re.S)
    assert len(h1s) == 2, f"expected one h1 per language in hero, got {len(h1s)}"
    assert all("Krasnobai" in h for h in h1s)
    # the EN block is visible, the RU block is hidden by default
    assert 'data-lang="en"' in hero
    assert 'data-lang="ru" hidden' in hero


def test_hero_header_is_bilingual(dist):
    """Both language headers are injected; the RU label is Russian, not the
    hardcoded English one. The hero shows role tag + location tag + name +
    one-line summary/lead."""
    import re
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    m = re.search(r'<section class="hero"[^>]*>(.*?)\n\s*</section>', html, re.S)
    assert m, "hero section not found"
    hero = m.group(1)
    assert "Staff DevOps Engineer" in hero
    assert "Ведущий DevOps-инженер" in hero
    assert "Aleksandr Krasnobai" in hero
    # location tags in both languages
    assert "Belgrade, Serbia — work authorized" in hero
    assert "Белград, Сербия — право на работу" in hero
    # one-line summary/lead (apostrophe is HTML-escaped in the rendered HTML)
    assert "high-throughput platforms" in hero or "высоконагруженных платформ" in hero
    # no leftover template placeholders
    assert "{{HEADER_EN}}" not in html and "{{HEADER_RU}}" not in html


def test_landing_page_has_no_duplicate_info(dist):
    """ADR business card: each fact should appear at most once per visible
    language block, not duplicated inside the same block."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    # Check each language block independently; the RU block is hidden by default.
    for lang in ("en", "ru"):
        m = re.search(rf'<div class="lang-block" data-lang="{lang}"[^\>]*>(.*?)\s*</div\s*>', html, re.S)
        assert m, f"{lang} lang-block not found"
        block = m.group(1)
        # "Staff DevOps Engineer" is intentionally repeated: once in the role
        # tag and once at the start of the one-line summary/lead.
        for f in ("Belgrade", "high-throughput"):
            assert block.count(f) <= 1, f"fact '{f}' duplicated in {lang} block"


def test_open_graph_tags_present_and_escaped(dist):
    """Open Graph tags must use the résumé name/role/summary and be escaped."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    assert 'property="og:title"' in html
    assert "Aleksandr Krasnobai" in html
    assert "Staff DevOps Engineer" in html
    assert 'property="og:description"' in html
    assert "high-throughput platforms" in html or "500M+" in html
    assert 'property="og:image"' in html
    assert "dragon-og.png" in html
    assert 'property="og:type"' in html
    assert 'property="profile:first_name"' in html
    assert 'property="profile:last_name"' in html


def test_favicon_resolves(dist):
    """ADR-0032: the red Space Invader favicon is linked and copied to assets."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    assert 'rel="icon"' in html
    assert "assets/favicon.svg" in html
    favicon = dist / "assets" / "favicon.svg"
    assert favicon.is_file(), "favicon.svg must be copied to dist/assets/"
    svg = favicon.read_text("utf-8")
    assert "#c62828" in svg, "favicon must use the red Space Invader color"
    assert "<rect" in svg, "favicon must be pixel-art rectangles"


def test_landing_page_shows_contact_only(dist):
    """ADR-0025: the landing #resume block shows the compact business-card
    contacts only — email + LinkedIn + Telegram. The full résumé body
    (Experience, Skills, Projects, Education, Certificates, Languages) lives
    in the PDF and markdown outputs, not on the page."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    resume = html[html.find('id="resume"'):html.find("<footer")]
    # both languages are present, each with the three top contacts
    assert 'class="contact-row"' in resume
    assert "LinkedIn" in resume and "Telegram" in resume
    assert "mailto:" in resume
    # GitHub is intentionally moved to the footer machine links, not the top contacts
    github_in_resume = re.search(r'id="resume".*GitHub', resume, re.S)
    assert not github_in_resume, "GitHub must not appear in the #resume contact row"
    # none of the other résumé sections leak onto the landing page
    for absent in ("Work Experience", "Skills", "Projects", "Education",
                   "Certificates", "Languages", "Опыт работы", "Навыки",
                   "Проекты", "Образование", "Сертификаты", "Языки"):
        assert absent not in resume, f"landing page leaked section: {absent}"
    # the dedicated LLM/AI-agent and markdown outputs carry the full résumé
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    md = build.render_markdown(en)
    assert "## Experience" in md
    assert "## Skills" in md
    assert "GitHub" in md


# --- single PDF format: single column, standard font, real text, no graphics - #
def test_resume_html_is_single_column_standard_font(dist):
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    html = build.render_resume_html(en, "en")
    assert "sans-serif" in html                 # standard system font
    assert "column-count" not in html         # no multi-column
    assert "float:" not in html               # no floats
    assert "<canvas" not in html and "<img" not in html  # no graphics


def test_resume_pdf_dates_formatted_on_role(dist):
    """PDF date ranges render as 'Mon YYYY – Present', not raw YYYY-MM. The
    formatter is unit-checked directly; the integration check only verifies raw
    ISO never leaks into the single PDF render."""
    assert build._fmt_ats("2022-03", None, "en") == "Mar 2022 – Present"
    assert build._fmt_ats("2022-03", "2024-05", "en") == "Mar 2022 – May 2024"
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    html = build.render_resume_html(en, "en")
    assert "2022-03" not in html                # raw ISO date must not leak


def test_resume_pdf_has_real_selectable_text(dist):
    """Single PDF body uses real text in headings/bullets, not images/tables."""
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    html = build.render_resume_html(en, "en")
    assert "<table" not in html
    assert "<h3>" in html and "Staff DevOps Engineer" in html
    assert "<ul>" in html and "<li>" in html


# --- metadata tier + JSON-LD + sitemap -------------------------------------- #
def test_min_json_shape(dist):
    build.build(clean=True)
    m = json.loads((dist / "resume.min.json").read_text("utf-8"))
    for k in ("name", "label", "top_skills", "years_experience", "full", "availability"):
        assert k in m, f"metadata tier missing {k}"
    assert m["availability"]["status"] == "open"
    work_model = m["availability"]["work_model"]
    assert "remote" in work_model, f"metadata tier work_model missing remote: {work_model}"
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
    assert "English (B2" in txt or "Английский (B2" in txt
    assert "Russian (Native)" in txt or "Русский (Native)" in txt


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


# --- hero CTA: single primary PDF download button ----------------------------
def test_hero_cta_is_pdf_download(dist):
    """The minimal business card has one primary CTA: download the single
    human-readable/ATS-safe PDF. AI/LLM résumé links live in the footer machine
    links, not in the hero."""
    import re
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    cta = re.search(r'<section class="cta-section"[^>]*>(.*?)</section>', html, re.S).group(1)
    links = re.findall(r'href="([^"]+)"', cta)
    assert links == [PDF_NAME], f"hero CTA should have exactly one PDF link, got {links}"
    assert 'data-i18n="download"' in cta, "CTA uses the bilingual download label"


# --- ADR-0017: fixed light Forest theme + system sans-serif ------------------ #
def test_single_forest_theme_no_picker(dist):
    """ADR-0017 v4: fixed light Forest theme. The palette picker is gone, there
    is no data-palette attribute, no dark block, no theme toggle, and the page
    uses system sans-serif (ADR-0018 v2)."""
    build.build(clean=True)
    html = (dist / "index.html").read_text("utf-8")
    # the palette picker and theme toggle must be gone
    assert 'id="palette-select"' not in html, "palette picker should be removed"
    assert "palette-pick" not in html, "palette-pick label should be removed"
    assert 'class="theme-toggle"' not in html, "theme toggle should be removed"
    css = (dist / "assets" / "site.css").read_text("utf-8")
    # no data-palette or data-theme dark axis remains
    assert "data-palette" not in css, "no data-palette should remain in CSS"
    assert ':root[data-theme="dark"]' not in css, "no dark theme block should remain in CSS"
    assert "@media (prefers-color-scheme: dark)" not in css, "no no-JS dark query should remain"
    # ADR-0018 v2: system sans-serif, no JetBrains Mono
    assert "--c-head-font:" not in css, "--c-head-font should be removed"
    assert "JetBrains Mono" not in css, "JetBrains Mono should be removed from CSS"
    assert "@font-face" not in css, "no @font-face should remain in site CSS"
    for w in ("jetbrains-mono-400.woff2", "jetbrains-mono-700.woff2"):
        assert not (dist / "assets" / w).exists(), f"{w} should not be copied to assets"
    assert not (dist / "assets" / "jetbrains-mono-LICENSE.txt").exists(), (
        "JetBrains Mono OFL license should not ship now that the font is gone")


def test_forest_has_single_light_block(dist):
    """The fixed Forest theme defines exactly one :root block with the light
    palette; there is no dark override."""
    import re
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    light = re.search(r"(?<![\w-]):root\s*\{([^}]*)\}", css)
    assert light, "bare :root (light) block missing"
    light_vars = set(re.findall(r"--(c-[a-z-]+)\s*:", light.group(1)))
    assert light_vars, "light block declares no --c-* vars"
    # the canonical Forest light values are present
    assert "--c-accent: #2f7d3a" in light.group(1), "forest light accent wrong"
    assert "--c-bg: #f4f6f2" in light.group(1), "forest light background wrong"


def test_pdf_html_uses_forest_palette(dist):
    """The single human-readable/ATS-safe PDF (render_resume_html inline CSS)
    must use the Forest palette, not the old calm blue/brown, and use a system
    sans-serif."""
    build.build(clean=True)
    en = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    html = build.render_resume_html(en, "en")
    assert "#2f7d3a" in html, "PDF HTML must use the Forest green accent"
    assert "#3a5ae0" not in html, "old calm blue accent must not leak into PDF HTML"
    assert "#2a2620" not in html, "old calm brown text must not leak into PDF HTML"
    assert "sans-serif" in html, "PDF HTML must use a system sans-serif"


# --- ADR-0019: automated WCAG contrast guard for the fixed light theme -------- #
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
    """Parse site.css into {"light": {var: hex}} from the top-level :root
    block. Comments are stripped first so they do not pollute selector detection.
    The @media print :root block is nested inside @media, so the brace-depth
    walker sees it as the body of the @media rule and skips it."""
    import re
    # strip CSS comments — they can contain braces and appear before :root,
    # which would otherwise make the selector include the comment text.
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
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
    """ADR-0019: compute WCAG contrast for the fixed light Forest theme and
    assert AA (>=4.5:1) for body text, muted text, link/accent text on both the
    page background and the block surface, plus filled-button text on the
    accent. Machine-enforced so a future color edit can't silently regress."""
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    theme = _theme_vars(css)
    assert set(theme) == {"light"}, f"parsed modes {sorted(theme)}"

    # filled button text color is white on the green accent
    BTN_FG = "#ffffff"
    failures = []
    v = theme["light"]
    for key in ("c-bg", "c-surface", "c-text", "c-muted", "c-accent"):
        assert v.get(key), f"light: missing --{key}"
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
        "button-fg/accent": (BTN_FG, accent),
    }
    for name, (fg, b) in checks.items():
        r = _contrast(fg, b)
        if r < 4.5:
            failures.append(f"light {name} {fg} on {b} = {r:.2f}:1")
    assert not failures, (
        "WCAG AA (<4.5:1) contrast failures:\n  " + "\n  ".join(failures))


def test_button_text_color_is_white_on_accent(dist):
    """The filled-button text color is white on the Forest accent (#2f7d3a),
    so the contrast guard's BTN_FG assumption holds."""
    import re
    build.build(clean=True)
    css = (dist / "assets" / "site.css").read_text("utf-8")
    assert re.search(r"\.btn-primary\s*\{[^}]*--bs-btn-color:\s*#fff", css), (
        "light .btn-primary must use white text")


# --- ADR-0024 v2: contact profiles are GitHub, LinkedIn, Telegram ---------- #
def test_contact_profiles_required_set(dist):
    """Both language files must carry the ADR-0024 v2 contact set, in order, and
    no stray Website profile (the site URL lives in basics.url, not profiles)."""
    build.build(clean=True)
    expected = ["GitHub", "LinkedIn", "Telegram"]
    for fn in ("resume.json", "resume.ru.json"):
        r = json.loads((dist / fn).read_text("utf-8"))
        networks = [p.get("network") for p in r["basics"].get("profiles", [])]
        assert networks == expected, f"{fn} profiles = {networks}"
        assert "Website" not in networks
    # ADR-0024 v2: Telegram is back and must reach EVERY audience surface,
    # not just JSON. The same handle is used everywhere.
    en_resume = build.parse_resume(build.RESUME_DIR / "resume.en.md")
    assert "t.me/krasnobaicoach" in build.render_resume_html(en_resume, "en")  # single PDF
    html = (dist / "index.html").read_text("utf-8")
    assert "t.me/krasnobaicoach" in html
    assert "Telegram" in (dist / "resume.txt").read_text("utf-8")
    assert "t.me/krasnobaicoach" in (dist / "resume.txt").read_text("utf-8")
    assert "Telegram" in (dist / "llms.txt").read_text("utf-8")                  # LLM index
    assert "t.me/krasnobaicoach" in (dist / "llms.txt").read_text("utf-8")
    assert "Telegram" in (dist / "resume.md").read_text("utf-8")                # markdown mirror
    assert "t.me/krasnobaicoach" in (dist / "resume.md").read_text("utf-8")
    assert "Telegram" in (dist / "resume-for-agents.md").read_text("utf-8")     # LLM/AI-agent build
    assert "t.me/krasnobaicoach" in (dist / "resume-for-agents.md").read_text("utf-8")