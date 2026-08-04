# scripts/validate_consistency.py — cross-check dist/ against canonical resume.en.md
"""Validate that every generated output matches the single source of truth.

Reads resume/resume.en.md and asserts that name, role, email, url and the three
required profiles (GitHub, LinkedIn, Telegram) appear consistently across:
- resume.json, resume.ru.json, resume.min.json, .well-known/cv.json, agents.json
- resume.txt, resume.md, resume-for-agents.md, llms.txt, AGENTS.md
- index.html
- the downloadable PDF filename and size

Fails with a non-zero exit code and a list of mismatches.
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

REQUIRED_PROFILES = ["GitHub", "LinkedIn", "Telegram"]
STALE_TERMS = ["backend engineer", "devops/sre engineer"]


def main() -> int:
    errors: list[str] = []

    resume_src = (ROOT / "resume" / "resume.en.md").read_text(encoding="utf-8")
    if not yaml:
        print("pyyaml is required", file=sys.stderr)
        return 1
    data = yaml.safe_load(resume_src.split("---", 2)[1])
    basics = data["basics"]

    name = basics["name"]
    label = basics["label"]
    summary = basics["summary"]
    email = basics["email"]
    url = basics["url"]
    profiles = {p["network"]: p for p in data.get("profiles", [])}

    for net in REQUIRED_PROFILES:
        if net not in profiles:
            errors.append(f"canonical source missing profile: {net}")

    github = profiles.get("GitHub", {}).get("url", "")
    linkedin = profiles.get("LinkedIn", {}).get("url", "")
    telegram = profiles.get("Telegram", {}).get("url", "")

    pdf_name = f"{name.replace(' ', '_')}_{label.replace(' ', '_')}.pdf"

    # JSON Resume canonical files
    for fname in ["resume.json", "resume.ru.json"]:
        obj = json.loads((DIST / fname).read_text(encoding="utf-8"))
        b = obj.get("basics", {})
        if b.get("name") != name:
            errors.append(f"{fname} name mismatch: {b.get('name')}")
        if b.get("email") != email:
            errors.append(f"{fname} email mismatch: {b.get('email')}")
        if b.get("url") != url:
            errors.append(f"{fname} url mismatch: {b.get('url')}")
        prof = {p["network"]: p for p in b.get("profiles", [])}
        for net, expected in [("GitHub", github), ("LinkedIn", linkedin), ("Telegram", telegram)]:
            if prof.get(net, {}).get("url") != expected:
                errors.append(f"{fname} {net} URL mismatch: {prof.get(net, {}).get('url')}")

    # resume.min.json metadata tier
    mini = json.loads((DIST / "resume.min.json").read_text(encoding="utf-8"))
    if mini.get("name") != name:
        errors.append(f"resume.min.json name mismatch: {mini.get('name')}")
    if mini.get("label") != label:
        errors.append(f"resume.min.json label mismatch: {mini.get('label')}")

    # .well-known/cv.json
    cv = json.loads((DIST / ".well-known" / "cv.json").read_text(encoding="utf-8"))
    # cv.json values may be absolute URLs when DOMAIN/PAGES_URL is set; compare
    # the path/filename component in addition to bare filenames.
    def _filename_or_bare(value: str) -> str:
        return value.rsplit("/", 1)[-1] if isinstance(value, str) else value
    if _filename_or_bare(cv.get("primary", "")) != "resume.json":
        errors.append(f"cv.json primary mismatch: {cv.get('primary')}")
    if _filename_or_bare(cv.get("human_pdf", "")) != pdf_name:
        errors.append(f"cv.json human_pdf mismatch: {cv.get('human_pdf')}")
    if _filename_or_bare(cv.get("ats_pdf", "")) != pdf_name:
        errors.append(f"cv.json ats_pdf mismatch: {cv.get('ats_pdf')}")

    # agents.json
    agents = json.loads((DIST / "agents.json").read_text(encoding="utf-8"))
    desc = agents.get("description", "")
    if name not in desc:
        errors.append("agents.json description missing name")
    if label not in desc:
        errors.append("agents.json description missing label")

    # Text/markdown outputs
    for fname in ["resume.txt", "resume.md", "resume-for-agents.md", "llms.txt"]:
        text = (DIST / fname).read_text(encoding="utf-8")
        for value, label_name in [
            (name, "name"),
            (label, "role"),
            (email, "email"),
            (github, "GitHub"),
            (linkedin, "LinkedIn"),
            (telegram, "Telegram"),
        ]:
            if value not in text:
                errors.append(f"{fname} missing {label_name}")

    # AGENTS.md
    agents_md = (DIST / "AGENTS.md").read_text(encoding="utf-8")
    for value, label_name in [(name, "name"), (label, "role"), (email, "email")]:
        if value not in agents_md:
            errors.append(f"AGENTS.md missing {label_name}")

    # index.html
    idx = (DIST / "index.html").read_text(encoding="utf-8")
    for value, label_name in [
        (name, "name"),
        (label, "role"),
        (email, "email"),
        (github, "GitHub"),
        (linkedin, "LinkedIn"),
        (telegram, "Telegram"),
        (summary, "summary"),
    ]:
        if value not in idx:
            errors.append(f"index.html missing {label_name}")

    # Stale / misleading text
    for fname in [
        "dist/index.html",
        "dist/resume.txt",
        "dist/resume.md",
        "dist/resume-for-agents.md",
        "dist/AGENTS.md",
        "dist/llms.txt",
    ]:
        text = (ROOT / fname).read_text(encoding="utf-8").lower()
        for term in STALE_TERMS:
            if term in text:
                errors.append(f"{fname} contains stale role text: {term}")

    # PDF
    pdf_path = DIST / pdf_name
    if not pdf_path.exists():
        errors.append(f"PDF missing: {pdf_name}")
    elif pdf_path.stat().st_size <= 100:
        errors.append(f"PDF is empty/placeholder: {pdf_name}")

    if errors:
        print("CONSISTENCY ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("OK — all generated outputs are consistent with resume/resume.en.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
