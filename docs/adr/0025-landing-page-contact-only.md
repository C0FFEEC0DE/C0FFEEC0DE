# ADR-0025 — Landing page shows Contact only; full résumé lives in the PDF

Date: 2026-07-30 · Status: Accepted · Supersedes part of ADR-0013

## Context
ADR-0013 established three audiences (human, LLM-agent, ATS) and rendered the
full résumé body — Contact → Experience → Skills → Projects → Education →
Certificates → Languages — into the landing page's `#resume` block via
`render_body_fragment`, shared in lockstep with the branded PDF.

The owner wants the landing page to be a light front door: identity (hero) plus
a way to make contact, funneling to the branded PDF for the full detail. The
landing page is not where a recruiter reads the résumé; the PDF is. Duplicating
the entire body onto the page adds scroll/length (against the low-cognitive-load
goal of ADR-0008) for no audience benefit — the human who wants the detail
downloads the PDF, and the machine/ATS audiences read `resume.json` /
`resume.txt` / `resume.pdf`, never the landing HTML.

## Decision
The landing page's `#resume` block renders **Contact only**, via a new
`render_contact_fragment`. The full résumé body (`render_body_fragment`) is
removed from the landing page and lives exclusively in the branded PDF (via
`render_html_fragment`) and the machine-readable outputs (`resume.json`,
`resume.ru.json`, `resume.txt`, `resume.md`, `resume.pdf`).

The Contact markup is shared between the landing page and the branded PDF
through a single `_contact_section` helper, so the contact surface stays in
lockstep across the two even though the rest of the body now diverges. The hero
is unchanged except that the dragon has moved to a hidden footer easter egg
(ADR-0026) and the single primary CTA sits in its own section below Contact
(ADR-0020 v3).

This supersedes the ADR-0013 statement that `render_body_fragment` is used by
both the landing `#resume` block and the branded-PDF body. ADR-0013's
three-audience decision stands; only the landing-page human render is narrowed.

## Consequences
- The landing page is short: hero + Contact + CTA + footer.
  Experience/Skills/Projects/Education/Certificates/Languages no longer appear
  in `index.html`.
- `render_body_fragment` is now used only by `render_html_fragment` (the branded
  PDF); `render_contact_fragment` is used only by the landing page. The two
  renderers diverge intentionally except for Contact, which stays shared.
- A build test (`test_landing_page_shows_contact_only`) asserts the landing
  `#resume` block contains Contact and none of the other sections, and that the
  branded-PDF body still carries the full résumé — so a future edit that
  re-injects `render_body_fragment` into the landing page is caught in CI.
- The UI test that asserted the `#resume` block contained an Experience entry
  ("Grid Dynamics") now asserts Contact content ("LinkedIn") instead.
- The skip-link targets `#main` (the start of the single `<main>` landmark),
  not `#resume`, as decided in ADR-0020 v2. Reversing this decision (re-showing
  the body on the page) requires a new ADR (or superseding this one).
