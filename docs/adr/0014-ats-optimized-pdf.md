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
- Standard section headings: "Work Experience", "Skills", "Projects",
  "Education", "Certifications", "Languages". The "Summary" front-matter field
  is intentionally omitted from the ATS PDF so the document opens directly with
  the experience section, while the one-line identity statement remains on the
  landing page and in machine-readable metadata.
- Contact block at the top (name, label, email, phone, location, profiles).
- Dates on the **same line** as role/company, format "Mon YYYY – Present".
- Plain `•` bullets; no tables, no columns, no graphics, no color dependency.
- Real, selectable text (WeasyPrint text layer), filename `resume.pdf`.
The branded version is kept as a separate `resume-branded.pdf` for humans.

## Consequences
- The default PDF can be forwarded into any ATS safely.
- A copy-paste / cursor self-test passes (logical order, selectable words).
- The branded PDF remains for direct human sharing; both are generated in CI.

## Version history
- **v1 (2026-07-30):** the ATS PDF is emitted as `resume.pdf` and the branded
  PDF as `resume-branded.pdf`.
- **v2 (2026-07-31):** filenames changed to the `Name_Surname_Role` pattern
  per ADR-0030. The ATS PDF is now
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` and the branded PDF is
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer_branded.pdf`; everything else in
  this decision stays the same.