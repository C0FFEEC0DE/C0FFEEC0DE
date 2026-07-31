# ADR-0024 — Contact profiles: GitHub, LinkedIn, Telegram

Date: 2026-07-30 · Status: Accepted (v3: 2026-07-31)

## Context

ADR-0016 fixed the contact set as `[GitHub, LinkedIn, Telegram]`. In the first
version of ADR-0024 the owner requested dropping Telegram as a contact channel.
After using the two-channel layout for a short period, the owner decided the
original three-channel set better serves the hiring audience: some recruiters and
collaborators prefer Telegram, and the handle is stable (`@krasnobaicoach`).

## Decision

The contact profiles are a fixed, ordered set of three:

1. **GitHub** — code, contributions, proof of work.
2. **LinkedIn** — professional history, the channel most recruiters use.
3. **Telegram** — `@krasnobaicoach` at `https://t.me/krasnobaicoach`.

These three are emitted in `basics.profiles` of both `resume/resume.en.md` and
`resume/resume.ru.md` (same handles, same order). The personal site URL stays in
`basics.url` (it is the canonical location, not a social profile), so it is not
duplicated as a `Website` profile.

The landing page's visible Contact row is intentionally narrower than the
source `basics.profiles`: it shows email + LinkedIn + Telegram. GitHub is still
reachable, but as a machine-readable format link in the footer (alongside
`resume.json`, `llms.txt`, etc.) rather than in the Contact row. Every
machine-readable and printable output continues to carry all three profiles.

## Consequences

- The three profiles render consistently across every machine-readable and
  printable audience surface: `resume.json` / `resume.ru.json` (`profiles`),
  `resume.txt`, `resume.md` (Contact section), the ATS PDF (`resume.pdf`) and
  branded PDF (`resume-branded.pdf`) contact lines, `llms.txt` (Contact
  section, for LLM agents), and JSON-LD `sameAs`. The landing-page Contact
  section (HTML) shows LinkedIn + Telegram + email; GitHub appears in the footer
  machine-links list, not in the Contact row.
- `cv.json` and `AGENTS.md` are discovery/index pointers to `resume.json`
  rather than duplicate contact surfaces; an agent follows them to the
  canonical `profiles`.
- A test asserts the three networks are present in both language files in the
  declared order.
- Removing Telegram again (or changing the handle/order) requires a new ADR
  (or superseding this one).

## Revision history
- **v1 (2026-07-30):** contact set reduced to `[GitHub, LinkedIn]`; Telegram
  removed from all surfaces.
- **v2 (2026-07-31):** Telegram re-added as the third channel with the stable
  handle `@krasnobaicoach`; order restored to `[GitHub, LinkedIn, Telegram]`.
- **v3 (2026-07-31):** clarified that the landing-page Contact row shows
  LinkedIn + Telegram + email, while GitHub is exposed through the footer
  machine-links list. The source `basics.profiles` and all machine-readable/
  printable outputs still carry all three profiles.
