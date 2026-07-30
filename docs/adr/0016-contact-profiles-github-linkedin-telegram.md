# ADR-0016 — Contact profiles: GitHub, LinkedIn, Telegram

Date: 2026-07-30 · Status: Accepted

## Context
The résumé's contact section (rendered from `basics.profiles` in JSON Resume)
is how a recruiter or collaborator reaches the person. A scattered or
inconsistent set of profiles adds friction and cognitive load (which
ADR-0008 forbids). The audience for this site spans hiring (GitHub/LinkedIn)
and the broader tech community (Telegram is a primary channel for many
European and open-source communities).

## Decision
The contact profiles are a fixed, ordered set of three:

1. **GitHub** — code, contributions, proof of work.
2. **LinkedIn** — professional history, the channel most recruiters use.
3. **Telegram** — a fast, low-friction direct message channel (`https://t.me/<handle>`).

These three are emitted in `basics.profiles` of both `resume/resume.en.md` and
`resume/resume.ru.md` (same handles, same order). The personal site URL stays in
`basics.url` (it is the canonical location, not a social profile), so it is not
duplicated as a `Website` profile.

## Consequences
- The three profiles render consistently across every audience surface: the
  landing-page Contact section (HTML), `resume.json` / `resume.ru.json`
  (`profiles`), `resume.txt`, `resume.md` (Contact section), the ATS PDF
  (`resume.pdf`) and branded PDF (`resume-branded.pdf`) contact lines,
  `llms.txt` (Contact section, for LLM agents), and JSON-LD `sameAs`.
- `cv.json` and `AGENTS.md` are discovery/index pointers to `resume.json`
  rather than duplicate contact surfaces; an agent follows them to the
  canonical `profiles`.
- Telegram is first-class in the JSON Resume `profiles` array, so AI agents
  and parsers that read `resume.json` see it alongside GitHub/LinkedIn.
- A test asserts the three networks are present in both language files AND in
  the ATS render, the branded-PDF body, `llms.txt`, and `resume.md`, so a
  future edit or renderer regression that drops one is caught in CI.
- Adding a fourth channel requires a new ADR (or superseding this one).