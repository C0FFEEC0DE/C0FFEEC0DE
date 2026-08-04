# ADR-0041 — PDF text-layer integrity

Date: 2026-08-04 · Status: Accepted

## Context

The PDF was selectable, but extraction joined adjacent header elements into
strings such as `ENGINEERBELGRADE` and `KrasnobaiStaff`. Certificate list bullets
were also emitted at the end of the extracted document instead of beside their
labels. A visually correct PDF can therefore still give an ATS malformed text.

## Decision

1. Insert explicit whitespace between semantic header and document blocks in
   the HTML used to generate the PDF.
2. Render certifications as simple block elements rather than generated list
   markers, while preserving the same visible single-column hierarchy.
3. Test the extracted PDF text for identity and role boundaries, required SRE
   vocabulary, certification attainment labels, and absence of detached bullet
   artifacts.
4. Enforce the same boundary checks in the release validator, not only in unit
   tests.
5. Continue to cap the PDF at four pages and retain real text, standard fonts,
   standard headings, and clickable links.

## Consequences

- ATS extraction more closely matches the visible reading order.
- CSS or renderer changes that silently corrupt token boundaries fail before
  release.
- ADR-0036 and ADR-0038 are amended by a stronger semantic text-layer gate.
