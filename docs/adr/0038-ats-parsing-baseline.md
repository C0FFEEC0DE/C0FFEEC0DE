# ADR-0038 — ATS parsing baseline

Date: 2026-08-04 · Status: Accepted

## Context

Applicant tracking systems do not share one public ranking algorithm, but their
official support guidance converges on a conservative parsing contract.
Greenhouse identifies columns, tables, headers, footers, text boxes, graphics,
and image-only files as common causes of failed parsing. Lever supports PDF but
recommends verifying that its text is selectable. Workday HiredScore compares
parsed résumé content with job requirements, so explicit, truthful terminology
matters more than decorative presentation or hidden keywords.

References:

- [Greenhouse: Unsuccessful resume parse](https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse)
- [Lever: Understanding resume parsing](https://help.lever.co/hc/en-us/articles/20087345054749-Understanding-resume-parsing)
- [Workday HiredScore: Candidate profiles](https://doc.workday.com/hiredscore/en-us/workday-hiredscore/recruiter-productivity-/concept--candidate-profiles.html)

## Decision

1. Keep one canonical English PDF with a real, selectable text layer, one
   column, standard fonts, conventional section headings, and chronological
   roles with explicit titles, employers, dates, and locations.
2. Put name, contact details, summary, experience, skills, education,
   certifications, and languages in the document body. Do not depend on page
   headers, footers, tables, sidebars, text boxes, icons, images, or charts to
   convey résumé facts.
3. Use vocabulary that the owner has confirmed and that a recruiter may search
   for. Keep it in readable experience evidence and skills; do not hide text,
   repeat keywords mechanically, or rename historical job titles.
4. Treat job-description tailoring as a separate, evidence-preserving step.
   Create a role-specific variant only from an actual job description, never a
   generic duplicate with a different heading.
5. Verify each release by extracting the generated PDF and checking identity,
   contacts, standard sections, core role vocabulary, reading boundaries, and
   absence of template or rendering artifacts.
6. Keep JSON Resume, plain text, Markdown, and agent-readable mirrors available
   as secondary machine surfaces, all generated from the same source.

## Consequences

- The PDF favours predictable parsing while retaining restrained visual
  hierarchy for humans.
- Searchability comes from explicit evidence-backed language rather than
  keyword stuffing.
- No layout change may weaken the extracted-text contract without an ADR and
  regression-test update.
- ADR-0014, ADR-0031, ADR-0033, and ADR-0036 remain in force and are tightened
  by this baseline.
