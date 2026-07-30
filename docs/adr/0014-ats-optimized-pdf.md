# ADR-0014 — `resume.pdf` is the ATS-optimized render

Date: 2026-07-30 · Status: Accepted

## Context
The original `resume.pdf` was rendered from the styled landing-page CSS (cards,
accent colors, non-standard layout). Single column, so not catastrophic, but it
violates ATS best practice: non-standard visual structure, dates on a separate
meta line, chip-style skills, and decorative styling. ATS platforms (Taleo,
Workday, iCIMS) corrupt ~1 in 3 resumes via tables/columns/text-boxes; the safe
default is plain, standard, top-to-bottom text.

## Decision
`resume.pdf` (the default download) is a dedicated **ATS-optimized** render:
- Single column, full width, 0.6–0.75in margins.
- Standard font (Helvetica/Arial), 10.5–11pt body, 13–14pt name, bold headings.
- Standard section headings: "Summary", "Work Experience", "Skills", "Projects",
  "Education", "Certifications", "Languages".
- Contact block at the top (name, label, email, phone, location, profiles).
- Dates on the **same line** as role/company, format "Mon YYYY – Present".
- Plain `•` bullets; no tables, no columns, no graphics, no color dependency.
- Real, selectable text (WeasyPrint text layer), filename `resume.pdf`.
The branded version is kept as a separate `resume-branded.pdf` for humans.

## Consequences
- The default PDF can be forwarded into any ATS safely.
- A copy-paste / cursor self-test passes (logical order, selectable words).
- `resume-branded.pdf` remains for direct human sharing; both are generated in CI.