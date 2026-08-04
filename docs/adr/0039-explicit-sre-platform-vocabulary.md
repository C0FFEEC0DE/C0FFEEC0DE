# ADR-0039 — Explicit SRE and platform-engineering vocabulary

Date: 2026-08-04 · Status: Accepted

## Context

The résumé described reliability and platform outcomes but omitted common
names for the practices behind them. The owner confirmed that production work
across the career included SLO/SLI ownership, error budgets, toil reduction,
MTTR, on-call, RTO/RPO, platform engineering, developer experience, and golden
paths. Omitting those terms weakens both human comprehension and legitimate ATS
matching.

## Decision

1. Add the confirmed terminology to the English and Russian canonical sources.
2. Place SLOs, SLIs, error budgets, on-call, incident response, MTTR, and
   RTO/RPO with production reliability work; place toil reduction with
   automation; and place platform engineering, developer experience, and golden
   paths with shared delivery and self-service platforms.
3. Add dedicated `Platform Engineering` and `Reliability Engineering` skills
   groups so exact market vocabulary remains discoverable without forcing every
   term into every role.
4. Expand target-role metadata to Staff DevOps Engineer, Staff Site Reliability
   Engineer, and Staff Platform Engineer. Preserve every historical job title
   exactly as held.
5. Keep quantified claims unchanged unless the owner supplies new evidence.
   Confirmed practice names may be added, but invented percentages, service
   levels, recovery targets, team sizes, and incident statistics may not.

## Consequences

- ATS and recruiters can identify the full SRE/platform scope directly.
- The content stays evidence-first and readable instead of becoming a keyword
  inventory.
- EN/RU skills remain structurally aligned, with English industry terms retained
  in the Russian version where they are commonly used in searches.
