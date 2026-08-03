<!--
  ИСХОДНЫЙ ФОРМАТ — редактируйте этот файл, затем `python build/build.py`
  пересоберёт всё (resume.json, resume.txt, resume.pdf, index.html, llms.txt, AGENTS.md).

  Front-matter (YAML ниже) маппится в JSON Resume `basics`, `profiles`, `meta`.
  Тело использует фиксированные H2-секции; H3 — элементы внутри Experience/Projects/Education.
  Первая строка после H3 может быть строкой метаданных:
      dates: 2022-03 — present · location: Berlin · url: https://example.com
  Остальные строки-списки (`- ...`) становятся `highlights`.

  СТАТУС ДАННЫХ — канонический материал резюме (ADR-0029).
  Материал ниже является единственным источником правды для всех
  человекочитаемых, машиночитаемых и ATS-выходов.
-->
---
basics:
  name: "Aleksandr Krasnobai"
  label: "Ведущий DevOps-инженер"
  email: "hi@krasnobai.dev"
  url: "https://krasnobai.dev"
  summary: "Staff DevOps Engineer — 18 лет поддержки высоконагруженных платформ: от 500M+ запросов в день до флотов в 10 000 серверов."
  location:
    city: "Белград"
    region: "Сербия"
    countryCode: "RS"
    note: "право на работу"
profiles:
  - {network: "GitHub",   username: "C0FFEEC0DE", url: "https://github.com/C0FFEEC0DE"}
  - {network: "LinkedIn", username: "aleksandrkrasnobai", url: "https://www.linkedin.com/in/aleksandrkrasnobai"}
  - {network: "Telegram", username: "krasnobaicoach", url: "https://t.me/krasnobaicoach"}
availability:
  status: "open"
  roles: ["Staff DevOps Engineer", "SRE", "Platform Engineer"]
  work_model: "remote"
  locations: ["Remote (EU)", "Belgrade, Serbia"]
meta:
  canonical: "https://krasnobai.dev/resume.json"
  version: "0.3.0"
  lastModified: "2026-07-31"
  intro: "Александр — Staff DevOps Engineer с почти 18-летним опытом в IT в областях DevOps и Site Reliability Engineering, эксплуатирующий высоконагруженные платформы, обрабатывающие 500M+ запросов в день. Специализируется на инфраструктуре как коде, CI/CD-автоматизации, observability и Kubernetes, спроектировал brand safety pipeline, сокративший инфраструктурные затраты на 80%. Руководит инженерными командами из 60+ человек и применяет AI-оркестрацию и агентные системы для автоматизации сложных операционных процессов."
languages_hint:
  available: ["en", "ru"]
---

## Summary

Staff DevOps Engineer — 18 лет поддержки высоконагруженных платформ: от 500M+ запросов в день до флотов в 10 000 серверов.

## Experience

### Staff DevOps Engineer — Grid Dynamics
dates: янв 2019 — настоящее · location: Сербия · url: https://www.gridynamics.com
- Эксплуатация и масштабирование высоконагруженной инфраструктуры обработки данных с 500M+ запросов в день для глобальной платформы ad-verification. Платформа валидирует производительность в цепочке цифровой рекламы для крупных медиа-клиентов, включая brand safety pipeline с ~500M запросов в день.
- End-to-end владение Brand Safety Pipeline (FastAPI + CTranslate2) — архитектура, деплой, масштабирование и эксплуатация платформы с ~500M запросов в день.
- Сократил инфраструктурные затраты на 80% за счёт смены inference-модели, оптимизации кода и runtime для ECS, а также точной настройки autoscaling.
- Построил собственный фреймворк нагрузочного тестирования, эмулирующий реальный клиентский трафик; использовал его для настройки метрик масштабирования и подбора железа по измеренному поведению, а не догадкам.
- Снизил шум алертов с ~10 000 в день до 1-10 в день, перепроектировав стек алертинга и устранив каскадные алерты в AWS-флоте до 10 000 серверов в пике.
- Построил кастомного AI-агента для triage алертов и помощи дежурству, расширив его кастомными плагинами и специализированными навыками для SRE/DevOps/Ops-команд; интегрировал LLM-assisted triage в процесс реагирования на инциденты.
- Оптимизировал инфраструктуру под AI-нагрузки, включая преобразование операционной документации и инфраструктурных определений в форматы, удобные для потребления LLM.
- Руководил реагированием на инциденты и постмортемами; разработал runbook’и, процессы review алертов и процедуры инцидентов, чтобы дежурные инженеры решали проблемы без трайбал-знаний.
- Готовил инфраструктуру к сертификации ISO 27001 — внедрил требуемые security-контроли, применил рекомендации аудита и выровнял инфраструктурные практики с контрольными точками стандарта.
- Эксплуатировал инфраструктуру обработки данных с 500M+ запросов в день на флоте до 10 000 AWS-серверов в пике; построил стек мониторинга (Prometheus, Grafana, ELK).
- Построил и поддерживал shared Jenkins pipeline library, развивая и адаптируя её под команды разработчиков; поставлял компоненты стека, включая alerting libraries и data pipelines в Airflow и Databricks.
- Разворачивал и эксплуатировал мульти-тенантные managed Kubernetes-кластеры (EKS) в AWS.
- Автоматизировал инфраструктуру с Puppet и Ansible, добавляя тесты и CI-пайплайны для инфраструктурного кода, чтобы изменения не ломали прод; использовал AWS CDK и CloudFormation для части инфраструктуры.
- Веду DevOps-направление Grid Dynamics Serbia — профессиональное развитие, community и морально-психологический климат; разработал внутренние курсы, систему оценки и технические роадмапы развития для инженеров.
- Веду трек профессионального развития 60 DevOps-инженеров через 10 лидов специализаций.

### Offensive Security Researcher — Самозанятый
dates: фев 2026 — настоящее · location: Сербия
- Offensive security research с фокусом на AI-системы и инфраструктуру — ломаю AI-агентов до того, как это сделают злоумышленники. Связываю DevOps-безопасность с AI safety: агенты с прод-доступом получают такой же скрютин, как и любая другая инфраструктура.
- Тестирую агентные системы на эксплуатируемые векторы (prompt injection, обход guardrails, privilege escalation агента).
- Red teaming CI/CD и cloud-окружений.
- Анализ поверхности атаки инфраструктуры.

### DevOps Engineer — Grid Dynamics
dates: фев 2018 — янв 2019 · location: Санкт-Петербург, Россия
- Self-service continuous-delivery tooling для крупного американского ритейлера. Построил внутреннюю self-service платформу, где QA и команды разработки за несколько кликов поднимают тестовые окружения с выбранными версиями микросервисных компонентов, не завися от центральной operations-команды.
- Построил и поддерживал внутреннюю self-service платформу с веб-интерфейсом, которая из шаблонов провижинила окружения в AWS, GCP и Azure, позволяя dev-командам за несколько кликов получать тестовые окружения с фиксированными версиями микросервисных компонентов.
- Строил self-service CI/CD tooling и автоматизировал release pipelines.
- Улучшал deployment-воркфлоу в разных cloud-окружениях.
- Онбордил QA и dev-команды.
- Добился 30% сокращения ручных шагов деплоя через end-to-end автоматизацию пайплайна.

### DevOps Engineer — Grid Dynamics
dates: мар 2017 — фев 2018 · location: Санкт-Петербург, Россия
- Внутренняя continuous-delivery платформа для собственных R&D-команд Grid Dynamics. Проект рассматривал CI/CD как продукт для других инженеров, чтобы повысить предсказуемость доставки.
- Построил shared Jenkins pipeline library, которой пользовались 27 R&D-командами; разработчики могли за ~5 минут задеплоить новый сервис с нуля — сначала в dev, затем в production.
- Абстрагировал внутренности Jenkins, build-логику, пермиссии и целевые cloud-деплои, чтобы разработчики не лезли в детали пайплайнов.
- Автоматизировал и улучшал CI/CD-воркфлоу.
- Тестировал и валидировал надёжность платформы.
- Собирал фидбек и требования от R&D-команд.
- Онбордил R&D-команды на платформу.
- Повысил предсказуемость доставки на 100% для первых пилотных команд.

### DevOps Engineer — Grid Dynamics
dates: авг 2016 — мар 2017 · location: Санкт-Петербург, Россия
- DevOps для платёжной технологичной компании (fintech). Работал одним из DevOps-инженеров, поддерживающих внутренние процессы разработки, с фокусом на AWS IoT-инфраструктуру для физических security-сканеров.
- Поддерживал внутренние процессы разработки как один из DevOps-инженеров — CI/CD пайплайны, окружения и деплои для платёжной платформы.
- Построил и эксплуатировал AWS IoT-инфраструктуру для флота security-сканеров возле банкоматов; сканеры мониторили окружающие Wi-Fi-сети и Bluetooth-трафик, собирая данные для выявления подозрительных устройств.
- Готовил инфраструктуру к сертификации ISO 27001 — внедрил security-контроли, применил рекомендации аудита и выровнял инфраструктуру с контрольными точками стандарта.
- Автоматизировал провижининг окружений через IaC в AWS.
- Настроил мониторинг и алертинг.
- Сотрудничал с разработчиками по инфраструктурным изменениям.

### DevOps / SRE Engineer — MZ
dates: мар 2015 — июл 2016 · location: Санкт-Петербург, Россия
- Серверная платформа для онлайн-игрового продукта с фокусом на production-надёжность. Команда занималась мониторингом live game-сервисов и поддержкой безопасных релизов.
- Переписал ~80% Puppet-кодовой базы, управляющей деплоем production и development окружений.
- Мигрировал часть сервисов из on-premises инфраструктуры (3 000 серверов) в AWS.
- Построил процессы тестирования Puppet (unit, functional и integration tests для модулей), чтобы баги отлавливались в dev/staging и не доходили до production — Puppet не ломал production в течение года, даже когда люди ошибались.
- Заменил систему мониторинга на Sensu, включив автоматическую регистрацию инстансов и упростив добавление новых чеков и сервисов.
- Снизил шум алертов до 1-2 релевантных алертов в неделю.
- Настроил incident response: в течение 5 минут после алерта команда собиралась в war room с первичной коммуникацией внутрь и наружу.
- Внедрил source of truth для инфраструктуры в виде простой MySQL-базы и использовал её для драйва автоматизации.
- Работал с Cloudflare для доставки контента и физическими F5-балансировщиками (legacy из on-prem).
- Поддерживал live production-системы и разбирал инциденты.

### System Administrator — Zodiac Interactive
dates: авг 2014 — май 2015 · location: Санкт-Петербург, Россия
- Администрирование корпоративной IT-инфраструктуры и внутренних сервисов. Один из двух администраторов, отвечавших за корпоративную сеть, VPN и внутренние сервисы. Роль охватывала администрирование серверов, сетевых сервисов и переход к Infrastructure as Code.
- Один из двух администраторов корпоративной сети с собственной автономной системой (AS), mesh VPN, соединяющий офисы, сети и клиентов.
- Администрировал корпоративные ресурсы — почта, Jenkins, VPN и другие внутренние сервисы.
- Внедрил мониторинг внутренних и клиентских сервисов.
- Внедрил Infrastructure as Code на Ansible, переведя управление инфраструктурой из ручных изменений в код.
- Автоматизировал внутренние процессы — onboarding/offboarding пользователей через OpenLDAP с централизованной аутентификацией для внутренних сервисов.

### Cloud Engineer — Echo
dates: фев 2013 — мар 2014 · location: Россия
- Cloud-платформа для real-time comment streaming. Работал полноценным cloud-инженером в ролях DevOps и SRE на AWS с Puppet-driven configuration management. Фокус — на стабильности платформы и улучшении того, как она деплоится и эксплуатируется ежедневно.
- Полноценная cloud-инженерная роль на AWS — DevOps и SRE ответственности: управление инфраструктурой, деплоями и production-операциями.
- Управлял AWS-инфраструктурой (ELB, EC2, S3, бэкапы).
- Автоматизировал инфраструктуру через Puppet.
- Мониторил серверы и занимался fault prevention.
- Поддерживал live production-системы и разбирал инциденты.

### System Administrator — ITECH.group
dates: 2012 — 2013
- IT-аутсорсинг и хостинг-провайдер для корпоративных клиентов. Отвечал за доступность клиентских серверов и core сетевых сервисов, а также за их мониторинг.
- Администрировал сетевые серверы и core-сервисы.
- Поддерживал клиентские серверы.
- Внедрял мониторинг внутренних и клиентских сервисов.

### Technical Engineer — ООО «Ультрамарин» ISP
dates: 2008 — 2012
- Техническая поддержка и установка сетевого оборудования для корпоративных клиентов. Роль включала обработку тикетов и сетевое оборудование для заказчиков.
- Обрабатывал support-тикеты.
- Устанавливал сетевое оборудование.
- Повышал качество технической поддержки.

## Skills

- **Облачные платформы:** Amazon Web Services (AWS), Google Cloud Platform (GCP), Microsoft Azure, AWS Control Tower, AWS Lambda, AWS IoT, Google Compute Engine, AWS Step Functions, Cosmos DB, AWS CDK, Amazon S3 Glacier, BigQuery, EKS, GKE, AKS
- **Контейнеры и оркестрация:** Docker, Kubernetes, Helm, EKS, GKE, AKS, KVM
- **Configuration Management и IaC:** Terraform, Ansible, Puppet, Salt, Chef
- **CI/CD и автоматизация:** Jenkins, Jenkins Job DSL, Jenkins Pipeline, GitHub Actions, GitLab CI, ArgoCD, Maven, Gradle, GNU Make, GitHub, Google Cloud Build, AWS CodePipeline, Rake
- **Мониторинг и observability:** Prometheus, Grafana, Elasticsearch, Logstash, Kibana, Nagios, Zabbix, Icinga, Graphite, Sensu, Cacti, SmokePing, PagerDuty
- **Программирование и скрипты:** Bash, Python, Groovy, SQL, YAML, JSON, Markdown, HTML
- **Базы данных и messaging:** PostgreSQL, MySQL, RabbitMQ, Kafka, Kafka Streams, Amazon DynamoDB, Amazon SQS, HDFS, Cloudera CDH
- **Сети и безопасность:** LDAP, TLS/X.509, IAM, Secrets Management, Monitoring and Auditing, Akamai, tcpdump / Wireshark
- **AI и агентная инженерия:** Claude Code, LLM Orchestration, Multi-Agent Systems, Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), LLM Applications Development, AI Agent Security, Prompt Injection Testing
- **ОС и виртуализация:** Linux (CentOS, Ubuntu, Debian, Red Hat Enterprise Linux), MacOS, Docker, KVM
- **Архитектура и методологии:** Site Reliability Engineering (SRE), Incident Management, GitOps, Platform Engineering, Agile, Scrum, Kanban, JIRA, REST, Microservices architecture, Pipeline architecture (ETL)
- **Тестирование:** JMeter, Jagger

## Projects

### agnthive
url: https://agnthive.run
- Open-source MIT-плагин для Claude Code на Node.js (ESM), обеспечивающий hook-gated SDLC (discover → design → implement → verify → review → docs) с 8 специализированными агентами и набором бенчмарков, который ловит регрессии агентов до релиза. Кроссплатформенный (Linux/macOS/Windows). github.com/C0FFEEC0DE/agnthive

### opendevops.run
url: https://opendevops.run
- Fusion DevOps-платформа с автономным SRE-агентом на чистом Python; 860+ тестов. github.com/C0FFEEC0DE/opendevops.run

## Education

### Специалитет по физике и информатике — Ульяновский государственный педагогический университет
dates: 2003 — 2011 · location: Ульяновск, Россия
- Кафедра физики и информатики

## Certificates

- **ICF Associate Certified Coach (ACC)** — ICF
- **Red Hat Certified System Administrator (RHCSA)** — Red Hat (2016)
- **AWS Certified Cloud Practitioner** — Amazon Web Services (2019)
- **AWS Certified Solutions Architect – Associate** — Amazon Web Services (2020)
- **Google Cybersecurity Certificate** — Coursera (2024)
- **Configuring Secure Access to Workloads Using Azure Networking** — Microsoft (2024)
- **Microsoft Certified: Azure Network Engineer Associate** — Microsoft

## Languages

- **Русский** (Native)
- **Английский** (B2 — Upper-intermediate)
