<!--
  SOURCE FORMAT — edit this file, then `python build/build.py` regenerates everything
  (resume.json, resume.txt, the single PDF, resume-for-agents.md, agents.json, index.html, llms.txt, AGENTS.md).

  Front-matter (YAML below) maps to JSON Resume `basics`, `profiles`, `meta`.
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
  summary: "Staff DevOps Engineer — 18 years keeping high-throughput platforms running, from 500M+ req/day pipelines to 10,000-server fleets."
  location:
    city: "Belgrade"
    region: "Serbia"
    countryCode: "RS"
    note: "work authorized"
profiles:
  - {network: "GitHub",   username: "C0FFEEC0DE", url: "https://github.com/C0FFEEC0DE"}
  - {network: "LinkedIn", username: "aleksandrkrasnobai", url: "https://www.linkedin.com/in/aleksandrkrasnobai"}
  - {network: "Telegram", username: "krasnobaicoach", url: "https://t.me/krasnobaicoach"}
availability:
  status: "open"
  roles: ["Staff DevOps Engineer", "SRE", "Platform Engineer"]
  work_model: "full-remote EU, open to hybrid in Belgrade"
  locations: ["Remote (EU)", "Belgrade, Serbia"]
  timezone: "CET (UTC+1)"
meta:
  canonical: "https://krasnobai.dev/resume.json"
  version: "0.3.0"
  lastModified: "2026-07-31"
  intro: "Aleksandr is a Staff DevOps Engineer with close to 18 years of IT experience across DevOps and Site Reliability Engineering, operating high-throughput platforms that process 500M+ requests per day. He specializes in infrastructure as code, CI/CD automation, observability, and Kubernetes, and he architected a brand safety pipeline that cut infrastructure costs by 80%. He leads engineering teams of 60+ engineers and applies AI orchestration and agentic systems to automate complex operational workflows."
languages_hint:
  available: ["en", "ru"]
---

## Summary

Staff DevOps Engineer — 18 years keeping high-throughput platforms running, from 500M+ req/day pipelines to 10,000-server fleets.

## Experience

### Staff DevOps Engineer — Grid Dynamics
dates: Jan 2019 — present · location: Serbia · url: https://www.gridynamics.com
- Operating and scaling high-throughput data-processing infrastructure supporting 500M+ daily requests for a global ad-verification platform. The platform validates performance across the digital advertising supply chain for major media clients, including a brand safety pipeline processing ~500M requests per day.
- Owned the Brand Safety Pipeline end-to-end (FastAPI + CTranslate2) — architecture, deployment, scaling, and operations for a platform processing ~500M requests/day.
- Cut infrastructure costs by 80% through inference model swap, code and runtime optimization for ECS, and autoscaling fine-tuning.
- Built a custom load-testing framework that emulated real client traffic, using it to tune scaling metrics and right-size hardware based on measured behavior instead of guesses.
- Reduced alert noise from ~10,000 alerts/day to 1-10/day by redesigning the alerting stack and eliminating cascading alerts across an AWS fleet peaking at 10,000 servers.
- Built a custom AI agent for alert triage and assisted on-call duty, extending it with custom plugins and specialized skills for the SRE/DevOps/Ops teams; integrated LLM-assisted triage into the incident response workflow.
- Optimized infrastructure for AI workloads, including converting operational documentation and infrastructure definitions into AI-ready formats for LLM consumption.
- Led incident response and postmortems; developed runbooks, alert review processes, and incident procedures so on-call engineers resolve issues without tribal knowledge.
- Prepared infrastructure for ISO 27001 certification — implemented required security controls, applied audit recommendations, and aligned infrastructure practices with the standard's control points.
- Operated 500M+ req/day data-processing infrastructure across a fleet of up to 10,000 AWS servers at peak; built the monitoring stack (Prometheus, Grafana, ELK).
- Built and maintained a shared Jenkins pipeline library, developing and adapting it for developer teams; delivered stack components including alerting libraries and data pipelines in Airflow and Databricks.
- Deployed and operated multi-tenant managed Kubernetes clusters (EKS) in AWS.
- Automated infrastructure with Puppet and Ansible, adding tests and CI pipelines for infrastructure code so changes ship without breaking production; used AWS CDK and CloudFormation for parts of the infrastructure.
- Own the DevOps direction for Grid Dynamics Serbia — professional development, community building, and team morale; developed internal training courses, an assessment system, and technical development roadmaps for engineers.
- Leading professional-development track for 60 DevOps engineers through 10 specialization leads.

### Offensive Security Researcher — Independent
dates: Feb 2026 — present · location: Serbia
- Independent offensive-security research alongside a full-time Staff DevOps Engineer role — a self-directed practice exploring AI-agent and infrastructure attack surfaces before they reach production.
- Breaks agentic systems for exploitable paths: prompt injection, guardrails bypass, agent privilege escalation, and unauthorized tool use.
- Red-teams CI/CD pipelines and cloud environments, then feeds findings back into platform-hardening and secure-by-default infrastructure design.
- Connects DevOps security with AI safety: agents with production access are treated with the same scrutiny as any other privileged infrastructure component.

### DevOps Engineer — Grid Dynamics
dates: Feb 2018 — Jan 2019 · location: St. Petersburg, Russia
- Self-service continuous-delivery tooling for a large US retail company. Built an internal self-service platform where QA and development teams spin up test environments with selected versions of microservice components in a few clicks, without depending on a central operations team.
- Built and maintained an internal self-service platform with a web UI that provisioned environments from templates across AWS, GCP, and Azure, letting dev teams spin up test environments with pinned versions of microservice components in a few clicks.
- Building self-service CI/CD tooling and automating release pipelines.
- Improving deployment workflows across cloud environments.
- Onboarding QA and development teams.
- Achieved a 30% reduction in manual deployment steps through end-to-end pipeline automation.

### DevOps Engineer — Grid Dynamics
dates: Mar 2017 — Feb 2018 · location: St. Petersburg, Russia
- Internal continuous-delivery platform built for Grid Dynamics' own R&D teams. This project treated CI/CD as a product for other engineers to improve delivery predictability.
- Built a shared Jenkins pipeline library used by 27 R&D teams, letting developers deploy a new service from scratch in about 5 minutes — first to the dev environment, then to production.
- Abstracted away Jenkins internals, build logic, permissions, and cloud deployment targets so developers never had to dig into pipeline details.
- Automating and improving CI/CD pipeline workflows.
- Testing and validating platform reliability.
- Gathering feedback and requirements from R&D teams.
- Onboarding R&D teams onto the platform.
- Improved delivery predictability by 100% for the initial internal pilot teams.

### DevOps Engineer — Grid Dynamics
dates: Aug 2016 — Mar 2017 · location: St. Petersburg, Russia
- DevOps for a payments technology company (fintech). Worked as one of the DevOps engineers supporting internal development processes, with a focus on AWS IoT infrastructure for physical security scanning devices.
- Supported internal development processes as one of the DevOps engineers — CI/CD pipelines, environments, and deployments for the payments platform.
- Built and operated AWS IoT infrastructure for a fleet of security scanners deployed around ATMs; scanners monitored surrounding Wi-Fi networks and Bluetooth traffic, collecting data to detect suspicious devices.
- Prepared infrastructure for ISO 27001 certification — implemented security controls, applied audit recommendations, and aligned infrastructure with the standard's control points.
- Automated environment provisioning using IaC in AWS.
- Set up monitoring and alerting.
- Collaborated with developers on infrastructure changes.

### DevOps / SRE Engineer — MZ
dates: Mar 2015 — Jul 2016 · location: St. Petersburg, Russia
- Server-side platform for an online gaming product focused on production reliability. The team focus was on monitoring live game services and supporting safe releases.
- Rewrote ~80% of the Puppet codebase managing deployments for production and development environments.
- Migrated part of the services from on-premises infrastructure (3,000 servers) to AWS cloud.
- Built Puppet testing processes (unit, functional, and integration tests for modules) so bugs were caught in dev/staging and never reached production — Puppet did not break production for a year, even when people made mistakes.
- Replaced the monitoring system with Sensu, enabling automatic instance registration and making it trivial to add new checks and services.
- Reduced alert noise to 1-2 relevant alerts per week.
- Set up incident response so that within 5 minutes of an alert the team was assembled in a war room with initial communication out both internally and externally.
- Introduced a source of truth for infrastructure as a simple MySQL database, used it to drive automation.
- Worked with Cloudflare for content delivery and physical F5 appliances for load balancing (legacy from on-prem).
- Supporting live production systems and resolving incidents.

### System Administrator — Zodiac Interactive
dates: Aug 2014 — May 2015 · location: St. Petersburg, Russia
- Corporate IT infrastructure and internal services administration. One of two administrators responsible for the corporate network, VPNs, and internal services. The role spanned server administration, network services, and the move toward Infrastructure as Code.
- One of two administrators running the corporate network with its own autonomous system (AS), a mesh of VPNs connecting offices, networks, and clients.
- Administered corporate resources — email, Jenkins, VPN, and other internal services.
- Implemented monitoring for internal and customer services.
- Introduced Infrastructure as Code with Ansible, moving infrastructure management from manual changes to code.
- Automated internal processes — user onboarding and offboarding via OpenLDAP with centralized authentication for internal services.

### Cloud Engineer — Echo
dates: Feb 2013 — Mar 2014 · location: Russia
- Cloud platform for real-time comment streaming. Worked as a full-fledged cloud engineer in DevOps and SRE capacities on AWS, with Puppet-driven configuration management. The focus was on keeping the platform stable and improving how it was deployed and operated day to day.
- Full cloud engineering role on AWS — DevOps and SRE responsibilities: managing infrastructure, deployments, and production operations.
- Managed AWS infrastructure (ELB, EC2, S3, backups).
- Automated infrastructure via Puppet.
- Monitored servers and performed fault prevention.
- Supporting live production systems and resolving incidents.

### System Administrator — ITECH.group
dates: 2012 — 2013
- IT outsourcing and hosting provider serving corporate clients. Responsible for keeping customer-facing servers and core network services available and properly monitored.
- Administering network servers and core services.
- Maintaining customer-facing servers.
- Implementing monitoring for internal and customer services.

### Technical Engineer — LLC "Ultramarine" ISP
dates: 2008 — 2012
- Technical support and network equipment installation for enterprise customers. This involved managing support tickets and network equipment for customers.
- Managing support tickets.
- Installing network equipment.
- Improving technical support quality.

## Skills

- **Cloud Platforms:** Amazon Web Services (AWS), Google Cloud Platform (GCP), Microsoft Azure, AWS Control Tower, AWS Lambda, AWS IoT, Google Compute Engine, AWS Step Functions, Cosmos DB, AWS CDK, Amazon S3 Glacier, BigQuery, EKS, GKE, AKS
- **Containers & Orchestration:** Docker, Kubernetes, Helm, EKS, GKE, AKS, KVM
- **Configuration Management & IaC:** Terraform, Ansible, Puppet, Salt, Chef
- **CI/CD & Automation:** Jenkins, Jenkins Job DSL, Jenkins Pipeline, GitHub Actions, GitLab CI, ArgoCD, Maven, Gradle, GNU Make, GitHub, Google Cloud Build, AWS CodePipeline, Rake
- **Monitoring & Observability:** Prometheus, Grafana, Elasticsearch, Logstash, Kibana, Nagios, Zabbix, Icinga, Graphite, Sensu, Cacti, SmokePing, PagerDuty
- **Programming & Scripting:** Bash, Python, Groovy, SQL, YAML, JSON, Markdown, HTML
- **Databases & Messaging:** PostgreSQL, MySQL, RabbitMQ, Kafka, Kafka Streams, Amazon DynamoDB, Amazon SQS, HDFS, Cloudera CDH
- **Networking & Security:** LDAP, TLS/X.509, IAM, Secrets Management, Monitoring and Auditing, Akamai, tcpdump / Wireshark
- **AI & Agentic Engineering:** Claude Code, LLM Orchestration, Multi-Agent Systems, Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), LLM Applications Development, AI Agent Security, Prompt Injection Testing
- **OS & Virtualization:** Linux (CentOS, Ubuntu, Debian, Red Hat Enterprise Linux), MacOS, Docker, KVM
- **Architecture & Methodology:** Site Reliability Engineering (SRE), Incident Management, GitOps, Platform Engineering, Agile, Scrum, Kanban, JIRA, REST, Microservices architecture, Pipeline architecture (ETL)
- **Testing:** JMeter, Jagger

## Projects

### krasnobai.dev
url: https://krasnobai.dev
- Personal bilingual résumé site built from a single markdown source with a pure-Python build pipeline. One `resume.en.md` generates 10+ outputs: JSON Resume, llms.txt, AGENTS.md, .well-known/cv.json, agents.json, an ATS-safe PDF, Open Graph previews, and Playwright-tested UI.
- Deployed to GitHub Pages via GitHub Actions; uses SRI-pinned Bootstrap, self-hosted SVG/PNG assets, and no backend or tracking.
- Demonstrates infrastructure-as-code, CI/CD, accessibility, automated testing, and LLM/AI-agent discoverability best practices in a tiny, hand-crafted package.

### agnthive
url: https://agnthive.run
- Open-source, MIT-licensed Node.js ESM plugin for Claude Code that enforces a hook-gated SDLC (discover → design → implement → verify → review → docs) with 8 specialist agents and a benchmark suite that catches agent regressions before they ship. Cross-platform (Linux/macOS/Windows). github.com/C0FFEEC0DE/agnthive

### opendevops.run
url: https://opendevops.run
- Fusion DevOps platform with an autonomous SRE agent core, in pure Python; 860+ tests. github.com/C0FFEEC0DE/opendevops.run

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
