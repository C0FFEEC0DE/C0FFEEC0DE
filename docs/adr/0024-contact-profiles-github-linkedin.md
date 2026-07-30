# ADR-0024 — Contact profiles: GitHub, LinkedIn

Date: 2026-07-30 · Status: Accepted · Supersedes ADR-0016

## Context
ADR-0016 fixed the contact set as `[GitHub, LinkedIn, Telegram]`. The owner
requested dropping Telegram as a contact channel. Keeping a profile the owner
no longer wants to be reached on adds friction and presents a stale surface to
recruiters and collaborators — the opposite of the low-cognitive-load goal in
ADR-0008. The remaining two channels (GitHub, LinkedIn) cover the hiring
audience fully; the personal site URL remains in `basics.url`.

## Decision
The contact profiles are a fixed, ordered set of two:

1. **GitHub** — code, contributions, proof of work.
2. **LinkedIn** — professional history, the channel most recruiters use.

These two are emitted in `basics.profiles` of both `resume/resume.en.md` and
`resume/resume.ru.md` (same handles, same order). The personal site URL stays in
`basics.url` (it is the canonical location, not a social profile), so it is not
duplicated as a `Website` profile. Telegram is removed entirely; no `t.me/` link
appears on any audience surface.

## Consequences
- The two profiles render consistently across every audience surface: the
  landing-page Contact section (HTML), `resume.json` / `resume.ru.json`
  (`profiles`), `resume.txt`, `resume.md` (Contact section), the ATS PDF
  (`resume.pdf`) and branded PDF (`resume-branded.pdf`) contact lines,
  `llms.txt` (Contact section, for LLM agents), and JSON-LD `sameAs`.
- `cv.json` and `AGENTS.md` are discovery/index pointers to `resume.json`
  rather than duplicate contact surfaces; an agent follows them to the
  canonical `profiles`.
- A test asserts the two networks are present in both language files AND that
  Telegram/`t.me/` does not leak into the ATS render, the branded-PDF body,
  `index.html`, `resume.txt`, `llms.txt`, or `resume.md`, so a future edit or
  renderer regression that re-introduces Telegram is caught in CI.
- Adding a third channel (or re-adding Telegram) requires a new ADR (or
  superseding this one).