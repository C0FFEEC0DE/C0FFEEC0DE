# ADR-0033 — Evidence-first, concise résumé content

Date: 2026-08-04 · Status: Accepted

## Context

The canonical résumé had strong outcomes but diluted them across a seven-page
PDF, repeated the same scale figures, mixed duties with achievements, and used
several claims whose wording was broader than the supporting detail. The Russian
mirror also mixed translated prose with unnecessary English jargon. Independent
security research was listed as concurrent employment, which could be read as a
second job rather than professional research.

## Decision

1. Keep only claims that are present in owner-provided source material; never
   invent dates, credential IDs, legal status, measurement definitions, or
   adoption statistics.
2. Make claims audit-friendly: identify the system, action, scale, and outcome.
   Avoid undefined percentages and language that implies direct line management
   when the source describes a professional-development program.
3. Limit the current role to the highest-signal outcomes, merge the 2016–2019
   Grid Dynamics project history into one progression entry, and compress early
   infrastructure roles.
4. Move independent AI-agent and infrastructure security work from employment to
   Selected Projects / Independent Research.
5. Reduce the skills matrix to technologies supported by the experience and
   projects. Do not list file formats or generic delivery methodologies as core
   Staff-level skills.
6. Use consistent implied-first-person action verbs and consistent tense.
7. Render certifications with issuer and optional date. Missing facts are omitted
   cleanly rather than represented as `None`, `unknown`, or guessed values.
8. Keep the English résumé canonical and maintain a professionally translated
   Russian mirror with technical product names left in English only where they
   are established identifiers.

## Consequences

- The résumé becomes shorter and easier to scan while preserving career depth.
- Exceptional figures remain visible but no longer repeat within one role.
- Interviewers can trace every public claim to a concrete source bullet.
- Some credential dates and metric definitions remain intentionally absent until
  the owner provides verifiable facts.
- ADR-0029 remains the historical record of the full-content import; this ADR
  governs its editorial and evidence standard.
