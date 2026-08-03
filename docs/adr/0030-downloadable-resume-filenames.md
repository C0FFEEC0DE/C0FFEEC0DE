# ADR-0030 — Downloadable résumé PDFs use `Name_Surname_Role` filenames

**Status:** Accepted  
**Date:** 2026-07-31

## Context

The landing page offers two human-facing résumé downloads:

- the primary CTA button downloads the ATS-optimized PDF;
- the footer machine-links list also offers a designed/branded PDF.

Previously both files used generic names (`resume.pdf` and `resume-branded.pdf`).
When a visitor downloaded the PDF, the saved file gave no indication of the
owner or role, which is inconvenient for recruiters and unprofessional for
sharing.

## Decision

Downloadable résumé PDFs are named from the canonical résumé front-matter:

```
<name>_<label>.pdf
<name>_<label>_branded.pdf
```

For the current content this produces:

- `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf`
- `Aleksandr_Krasnobai_Staff_DevOps_Engineer_branded.pdf`

The slug is computed in `build/build.py` by `_download_slug(name, label)`:

- strip non-alphanumeric characters (except hyphens);
- collapse spaces to underscores;
- concatenate `name` and `label` with an underscore.

Machine-readable endpoints keep their canonical names:

- `resume.json`, `resume.ru.json`, `resume.min.json` — JSON Resume convention;
- `.well-known/cv.json` — cv.json discovery convention;
- `resume.txt`, `resume.md` — stable curl-friendly plain-text and markdown mirrors;
- `llms.txt`, `AGENTS.md` — agent-discovery files.

## Consequences

- Recruiters who save the PDF get an immediately meaningful filename.
- `src/index.html` uses `{{PDF_ATS}}` and `{{PDF_BRANDED}}` placeholders so the
  links stay in sync with the résumé content without hand-editing.
- `build/build.py` passes the same filenames to `llms.txt`, `AGENTS.md`, and
  `.well-known/cv.json` so every surface points at the correct file.
- If `basics.name` or `basics.label` change, the PDF filenames change
  automatically; tests pin the expected names just like they pin other
  résumé data.
- The old generic names (`resume.pdf`, `resume-branded.pdf`) are no longer
  emitted or served.
