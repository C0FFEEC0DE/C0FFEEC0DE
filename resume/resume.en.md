<!--
  SOURCE FORMAT — edit this file, then `python build/build.py` regenerates everything
  (JSON Resume EN/RU, plain text/markdown, the single PDF, agent manifests,
  discovery files, index.html, sitemap, and crawler metadata).

  Front-matter (YAML below) maps to JSON Resume `basics`, `profiles`,
  `availability`, and `meta`.
  Body uses fixed H2 sections; H3s are items inside Experience/Projects/Education.
  The first line after an H3 may be a metadata line:
      dates: 2022-03 — present · location: Berlin · url: https://example.com
  Remaining bullet lines (`- ...`) become `highlights`.

  DATA STATUS — canonical résumé content (ADR-0029). The material below is the
  single source of truth for all human, machine, and ATS outputs.
-->
---
basics:
  name: "Aleksandr Krasnobai"
  label: "Staff DevOps Engineer"
  email: "hi@krasnobai.dev"
  url: "https://krasnobai.dev"
  summary: "Staff DevOps/SRE Engineer with 18 years operating high-throughput cloud platforms: 500M+ requests/day and fleets of up to 10,000 instances."
  location:
    city: "Belgrade"
    region: "Serbia"
    countryCode: "RS"
    note: "authorized to work in Serbia"
    tag: "Belgrade · Serbia work authorization"
profiles:
  - {network: "GitHub",   username: "C0FFEEC0DE", url: "https://github.com/C0FFEEC0DE"}
  - {network: "LinkedIn", username: "aleksandrkrasnobai", url: "https://www.linkedin.com/in/aleksandrkrasnobai"}
  - {network: "Telegram", username: "krasnobaicoach", url: "https://t.me/krasnobaicoach"}
availability:
  status: "open"
  roles: ["Staff DevOps Engineer", "SRE", "Platform Engineer"]
  work_model: "remote across European time zones; open to hybrid roles in Belgrade"
  locations: ["European time zones (remote)", "Belgrade, Serbia"]
  timezone: "Europe/Belgrade — CET/CEST (UTC+1/+2)"
meta:
  canonical: "https://krasnobai.dev/resume.json"
  version: "0.4.1"
  lastModified: "2026-08-04"
  intro: "Staff DevOps/SRE Engineer with 18 years of experience operating high-throughput cloud platforms. Reduced infrastructure costs by 80%, redesigned alerting for a fleet of up to 10,000 instances, and built delivery and reliability platforms used by dozens of engineering teams. Leads a professional-development program for 60 DevOps engineers through 10 specialization leads and applies LLM orchestration to operational workflows."
  impact:
    - {value: "80%", label: "infrastructure cost reduction"}
    - {value: "500M+", label: "requests processed per day"}
    - {value: "10,000", label: "instances at peak fleet scale"}
languages_hint:
  available: ["en", "ru"]
---

## Summary

Staff DevOps/SRE Engineer with 18 years operating high-throughput cloud platforms: 500M+ requests/day and fleets of up to 10,000 instances.

## Experience

### Staff DevOps Engineer — Grid Dynamics
dates: 2019-01 — present · location: Serbia · url: https://www.gridynamics.com
- Operate and scale data-processing infrastructure handling 500M+ daily requests across an AWS fleet that has peaked at 10,000 compute instances.
- Own the Brand Safety inference pipeline end-to-end (FastAPI and CTranslate2), including architecture, deployment, scaling, and production operations.
- Cut infrastructure costs by 80% through inference model swap, code and runtime optimization for ECS, and autoscaling fine-tuning.
- Built a production-representative load-testing framework to select instance types and tune autoscaling thresholds from measured behavior.
- Reduced alert volume from approximately 10,000 events/day to 1–10/day by redesigning alert routing and eliminating cascades.
- Built an LLM-assisted alert-triage agent with team-specific plugins and integrated it into incident-response workflows.
- Operate multi-tenant EKS clusters and infrastructure automation using AWS CDK, CloudFormation, Puppet, and Ansible; maintain observability with Prometheus, Grafana, and ELK.
- Lead a professional-development program for 60 DevOps engineers through 10 specialization leads, including internal courses, assessment, and technical growth roadmaps.

### DevOps Engineer — Grid Dynamics
dates: 2016-08 — 2019-01 · location: St. Petersburg, Russia
- Built a shared Jenkins pipeline library used by 27 R&D teams, enabling a new service to reach development and production environments in approximately five minutes.
- Built a self-service web platform that provisioned version-pinned test environments across AWS, GCP, and Azure and reduced manual deployment steps by 30%.
- Built and operated AWS IoT infrastructure for physical security scanners deployed around ATMs.
- Implemented infrastructure controls and audit recommendations supporting ISO 27001 certification readiness.

### DevOps / SRE Engineer — MZ
dates: 2015-03 — 2016-07 · location: St. Petersburg, Russia
- Rewrote ~80% of the Puppet codebase managing deployments for production and development environments.
- Migrated services from a 3,000-server on-premises estate to AWS.
- Introduced unit, functional, and integration testing for Puppet modules, achieving 12 months without Puppet-caused production incidents.
- Replaced the monitoring platform with Sensu, enabling automatic instance registration and simpler service onboarding.
- Reduced alert noise to 1-2 relevant alerts per week.

### System Administrator — Zodiac Interactive
dates: 2014 — 2015 · location: St. Petersburg, Russia
- Co-managed a corporate network with its own autonomous system and a VPN mesh connecting offices, clients, and internal networks.
- Administered corporate resources — email, Jenkins, VPN, and other internal services.
- Introduced Infrastructure as Code with Ansible, moving infrastructure management from manual changes to code.
- Automated internal processes — user onboarding and offboarding via OpenLDAP with centralized authentication for internal services.

### Cloud Engineer — Echo
dates: 2013-02 — 2014-03 · location: Russia
- Operated the AWS platform for real-time comment streaming, including ELB, EC2, S3, backups, deployments, and incident response.
- Automated configuration and infrastructure operations with Puppet.
- Built monitoring and preventive maintenance workflows for production services.

### Earlier Infrastructure Experience — ITECH.group / Ultramarine ISP
dates: 2008 — 2013 · location: Russia
- Administered customer-facing hosting servers and core network services for corporate clients.
- Implemented monitoring for internal and customer services.
- Installed network equipment and supported enterprise connectivity.

## Skills

- **Cloud:** AWS, GCP, Microsoft Azure
- **Platform:** Kubernetes, EKS, Docker, Helm, Linux
- **Infrastructure as Code:** Terraform, AWS CDK, CloudFormation, Ansible, Puppet
- **Delivery:** Jenkins, GitHub Actions, GitLab CI, Argo CD
- **Observability:** Prometheus, Grafana, Elasticsearch, Logstash, Kibana, PagerDuty
- **Programming:** Python, Bash, Groovy, SQL
- **Data:** Kafka, PostgreSQL, Airflow, Databricks
- **AI and Security:** LLM orchestration, agent security testing, prompt-injection assessment, incident triage automation

## Projects

### krasnobai.dev
url: https://krasnobai.dev
- Bilingual résumé site generated from one Markdown source into a tested ATS PDF, JSON Resume, agent-readable formats, and an accessible static UI.
- Deployed through GitHub Actions with no backend, tracking, remote fonts, or runtime CDN dependency.

### AI Agent and Infrastructure Security Research
dates: 2026-02 — present
- Evaluate agentic systems for prompt injection, guardrail bypass, privilege escalation, and unauthorized tool execution.
- Red-team CI/CD and cloud attack surfaces and feed findings into secure-by-default platform design.
- Treat production-capable agents as privileged infrastructure components and test their permissions and tool boundaries accordingly.

### agnthive
url: https://agnthive.run
- Open-source Node.js plugin for Claude Code that enforces a hook-gated SDLC with eight specialist agents and a cross-platform regression benchmark suite. github.com/C0FFEEC0DE/agnthive

### opendevops.run
url: https://opendevops.run
- Python DevOps platform with an autonomous SRE agent core and 860+ automated tests. github.com/C0FFEEC0DE/opendevops.run

## Education

### Specialist Degree in Physics and Informatics — Ulyanovsk State Pedagogical University
dates: 2003 — 2011 · location: Ulyanovsk, Russia
- Department of Physics & Informatics

## Certificates

- **ICF Associate Certified Coach (ACC)** — ICF
- **Red Hat Certified System Administrator (RHCSA)** — Red Hat (2016)
- **AWS Certified Cloud Practitioner** — Amazon Web Services (2019)
- **AWS Certified Solutions Architect – Associate** — Amazon Web Services (2020)
- **Google Cybersecurity Certificate** — Coursera (2024)
- **Configuring Secure Access to Workloads Using Azure Networking** — Microsoft (2024)
- **Microsoft Certified: Azure Network Engineer Associate** — Microsoft

## Languages

- **Russian** (Native)
- **English** (B2 — Upper-intermediate)
