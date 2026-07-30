# ADR-0015 — AI-agent discoverability: cv.json well-known + metadata tier

Date: 2026-07-30 · Status: Accepted

## Context
2026 AI-agent resume standards (cv.json, Open Talent Protocol) emphasize
**discovery** and **token economy**: an agent shouldn't have to fetch a full
multi-KB JSON just to decide whether to read further, and it should find the
machine data without guessing URLs.

## Decision
Add two lightweight AI-facing artifacts, both derived from `resume.json`:
- **`/.well-known/cv.json`** — a discovery manifest (cv.json convention) that
  points agents at `resume.json` (and the RU mirror). Served at the well-known
  path so agents can find it by convention.
- **`resume.min.json`** — a token-cheap "metadata tier" (~100 tokens, inspired by
  OTP's `metadata` tier): name, label, location, top skills, years of experience,
  availability/hiring signals, and a link to the full `resume.json`. Agents can
  screen on this before fetching the full file.

Both are listed in `llms.txt` and `AGENTS.md` alongside the existing JSON Resume
outputs. Hiring signals (`availability`, `work_model`, `visa_status`) are optional
front-matter fields surfaced into `resume.json` and `resume.min.json` when present.

## Consequences
- Agents get a conventional discovery entry point and a cheap screening object.
- Adding more signals later is additive (extra keys in JSON Resume, which allows
  `additionalProperties`).
- The well-known path is a single file; no routing/server needed on Pages.