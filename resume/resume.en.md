<!--
  SOURCE FORMAT — edit this file, then `python build/build.py` regenerates everything
  (resume.json, resume.txt, resume.pdf, index.html, llms.txt, AGENTS.md).

  Front-matter (YAML below) maps to JSON Resume `basics`, `profiles`, `meta`.
  Body uses fixed H2 sections; H3s are items inside Experience/Projects/Education.
  The first line after an H3 may be a metadata line:
      dates: 2022-03 — present · location: Berlin · url: https://example.com
  Remaining bullet lines (`- ...`) become `highlights`.

  DATA STATUS — real data sourced from the owner's LinkedIn
  (linkedin.com/in/aleksandrkrasnobai) plus local project repos. Items marked
  `TODO` are gaps: LinkedIn hides them from public view and they must be filled
  before going live — phone, the Grid Dynamics start
  date and exact title, prior roles, education degree/dates. Drafted (inferred) values — the headline, summary, skills grouping,
  and project descriptions — are proposals the owner can edit.
-->
---
basics:
  name: "Aleksandr Krasnobai"
  label: "Senior DevOps / SRE / Platform Engineer"   # TODO: confirm exact headline
  email: "hi@krasnobai.dev"
  # phone: "+TODO"                         # TODO: real phone (delete line if unused)
  url: "https://krasnobai.dev"
  summary: "DON'T PANIC — I keep distributed systems running."
  location:
    city: "Belgrade"
    region: "Serbia"
    countryCode: "RS"
    note: "permanent residence"
profiles:
  - {network: "GitHub",   username: "C0FFEEC0DE", url: "https://github.com/C0FFEEC0DE"}
  - {network: "LinkedIn", username: "aleksandrkrasnobai", url: "https://www.linkedin.com/in/aleksandrkrasnobai"}
  - {network: "Telegram", username: "krasnobaicoach", url: "https://t.me/krasnobaicoach"}
availability:
  status: "open"   # TODO: confirm you are actively open to roles
  roles: ["Senior DevOps Engineer", "SRE", "Platform Engineer", "Cloud Infrastructure Engineer"]
  work_model: "remote"
  locations: ["Remote (EU)", "Belgrade, Serbia"]
meta:
  canonical: "https://krasnobai.dev/resume.json"
  version: "0.2.0"
  lastModified: "2026-07-30"
languages_hint:
  available: ["en", "ru"]
---

## Summary

DON'T PANIC — I keep distributed systems running.

## Experience

### Senior DevOps Engineer — Grid Dynamics
dates: TODO — present · location: Belgrade, Serbia · url: https://www.gridynamics.com
<!-- TODO: confirm exact title and start date -->
- Led a 3-engineer team building a multi-language brand-safety translation service (FastAPI + CTranslate2) — from prototype to 40+ clusters in six months, handling ~500M requests/day across 60+ languages.
- ~10× throughput on the same hardware and ~80% cost reduction through inference optimization and fleet tuning.
- Self-healing infrastructure with dual health checks; a Locust-based load-testing rig validated capacity before every scale-out.
<!-- TODO: add prior roles (pre-Grid Dynamics, St Petersburg / Russia) — LinkedIn hides titles, companies and dates from public view. -->

## Skills

- **Cloud**: AWS (Solutions Architect Associate, Cloud Practitioner), Azure (networking)
- **Infrastructure / DevOps**: Kubernetes, Terraform, Linux / Red Hat (RHCSA), CI/CD, container orchestration
- **Backend**: Python, FastAPI, Node.js (ESM)
- **ML / Data**: CTranslate2, high-throughput inference, Locust load testing
- **Security**: Google Cybersecurity, brand-safety systems, enterprise architecture
- **Practices**: SRE, zero-trust sandboxing, code review, team leadership

## Projects

### agnthive
url: https://agnthive.run
- Open-source, MIT-licensed Node.js ESM plugin for Claude Code that enforces a hook-gated SDLC (discover → design → implement → verify → review → docs) with 8 specialist agents and a benchmark suite that catches agent regressions before they ship. Cross-platform (Linux/macOS/Windows). github.com/C0FFEEC0DE/agnthive

### opendevops.run
url: https://opendevops.run
- Fusion DevOps platform with an autonomous SRE agent core, in pure Python; 860+ tests. github.com/C0FFEEC0DE/opendevops.run

## Education

### TODO — Ulyanovsk State Pedagogical University
location: Ulyanovsk, Russia
<!-- TODO: degree, field of study, and dates (LinkedIn hides them) -->

## Certificates

- **AWS Certified Solutions Architect – Associate** — Amazon Web Services (2020)
- **AWS Certified Cloud Practitioner** — Amazon Web Services (2019)
- **Red Hat Certified System Administrator (RHCSA)** — Red Hat (Credential ID 140-219-007)
- **Google Cybersecurity Certificate** — Coursera (2024)
- **Configure secure access to your workloads using Azure networking** — Microsoft (2024)
- **Enterprise Architecture in Practice** — LinkedIn (2022)
- **ICF Associate Certified Coach (ACC)** — ICF (TODO)

## Languages

- **English** (Professional working)
- **Russian** (native)

## Contact

Best reached by email: hi@krasnobai.dev — usually reply within a day. Open to senior DevOps / SRE and cloud-infrastructure roles in remote-friendly teams (based in Belgrade, Serbia — permanent residence, CET, no visa sponsorship).