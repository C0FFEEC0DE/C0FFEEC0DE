# ADR-0040 — Credential dates mean attainment, not active status

Date: 2026-08-04 · Status: Accepted

## Context

The source contains attainment years for some credentials but does not contain
verification URLs, credential IDs, expiry dates, or owner-confirmed current
status. A bare year beside a certification can be misread as evidence that it
is still active. This is especially unsafe because providers use different
renewal policies: AWS certifications are generally valid for three years, while
Microsoft role-based certifications commonly renew annually.

References:

- [AWS Certification recertification policy](https://aws.amazon.com/certification/policies/recertification/)
- [Microsoft certification renewal FAQ](https://learn.microsoft.com/en-us/credentials/certifications/renew-your-microsoft-certification-faq)

## Decision

1. Keep the parsed JSON Resume `date` value as the supplied attainment year.
2. Render a supplied date as `earned YYYY` in English and `получен в YYYY` in
   Russian human-readable, plain-text, Markdown, PDF, and agent-facing outputs.
3. Do not emit `active`, `current`, `valid`, an expiry date, a credential ID, or
   a verification URL unless the owner supplies that fact.
4. Leave credentials without a supplied date undated and make no status claim.
5. Keep the conventional `Certifications` PDF heading for ATS recognition.

## Consequences

- The résumé proves historical attainment without implying unverified validity.
- JSON consumers retain a simple source date, while narrative outputs explain
  its meaning.
- Future verified status can be added without rewriting historical data.
