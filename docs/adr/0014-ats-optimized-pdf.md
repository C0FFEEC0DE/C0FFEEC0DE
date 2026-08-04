# ADR-0014 — `resume.pdf` is the ATS-optimized render

Date: 2026-07-30 · Status: Accepted (amended by ADR-0031 — the ATS-safe render is now also the human-facing PDF)

## Context
The original `resume.pdf` was rendered from the styled landing-page CSS (cards,
accent colors, non-standard layout). Single column, so not catastrophic, but it
violates ATS best practice: non-standard visual structure, dates on a separate
meta line, chip-style skills, and decorative styling. ATS platforms (Taleo,
Workday, iCIMS) corrupt ~1 in 3 resumes via tables/columns/text-boxes; the safe
default is plain, standard, top-to-bottom text.

ADR-0031 keeps these ATS-safety rules but applies them to the *same* file that
humans download, so the single PDF must also look attractive (Forest palette,
clean hierarchy, generous spacing) while remaining structurally ATS-safe.

## Decision
`Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` (the default download) is the
single human-readable, ATS-optimized render:
- Single column, full width, 0.75–0.85in margins.
- System sans-serif font stack (Segoe UI, Roboto, Helvetica Neue, Arial), 10.5–11pt
  body, ~21pt name, bold headings.
- Standard section headings: "Summary", "Work Experience", "Skills", "Projects",
  "Education", "Certifications", "Languages". A brief Summary from `meta.intro`
  is included so the PDF is self-contained for humans; Work Experience follows
  immediately after.
- Contact block at the top (name, label, email, phone, profiles as label + full URL).
- Dates on the **same line** as role/company, format "Mon YYYY – Present".
- Plain `•` bullets; no tables, no columns, no graphics.
- Forest palette and clean visual hierarchy for human readability; color is not
  the only signal (text hierarchy, spacing) so it remains safe if printed in greyscale.
- Real, selectable text (WeasyPrint text layer).
There is no separate branded PDF.

## Consequences
- The default PDF can be forwarded into any ATS safely and still looks good in email.
- A copy-paste / cursor self-test passes (logical order, selectable words).
- Only one PDF is generated in CI, removing the two-file confusion.

## Version history
- **v1 (2026-07-30):** the ATS PDF is emitted as `resume.pdf` and the branded
  PDF as `resume-branded.pdf`.
- **v2 (2026-07-31):** filenames changed to the `Name_Surname_Role` pattern
  per ADR-0030. The ATS PDF is now
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` and the branded PDF is
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer_branded.pdf`; everything else in
  this decision stays the same.
- **v3 (2026-08-03):** ADR-0031 merges the two PDFs. The single
  `Aleksandr_Krasnobai_Staff_DevOps_Engineer.pdf` is both the ATS-safe and
  human-readable download.