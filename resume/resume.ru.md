<!--
  ИСХОДНЫЙ ФОРМАТ — редактируйте этот файл, затем `python build/build.py`
  пересоберёт всё (resume.json, resume.txt, resume.pdf, index.html, llms.txt, AGENTS.md).

  Front-matter (YAML ниже) маппится в JSON Resume `basics`, `profiles`, `meta`.
  Тело использует фиксированные H2-секции; H3 — элементы внутри Experience/Projects/Education.
  Первая строка после H3 может быть строкой метаданных:
      dates: 2022-03 — present · location: Berlin · url: https://example.com
  Остальные строки-списки (`- ...`) становятся `highlights`.

  СТАТУС ДАННЫХ — реальные данные из LinkedIn владельца
  (linkedin.com/in/aleksandrkrasnobai) и локальных репозиториев проектов. Поля
  `TODO` — пробелы: LinkedIn скрывает их из публичного профиля, их нужно
  заполнить перед публикацией — email, телефон, Telegram-ник, дата начала и
  точная должность в Grid Dynamics, предыдущие роли, степень/годы образования. Черновые (выведенные) значения — заголовок, обзор, группа
  навыков и описания проектов — это предложения, которые владелец может править.
-->
---
basics:
  name: "Aleksandr Krasnobai"
  label: "Старший DevOps / SRE-инженер"   # TODO: подтвердить точный заголовок
  email: "hi@krasnobai.dev"
  # phone: "+TODO"                         # TODO: реальный телефон (удалите строку, если нет)
  url: "https://krasnobai.dev"
  summary: "Старший DevOps / SRE-инженер из Белграда, Сербия — ПМЖ, часовой пояс CET, без визовой поддержки. Строю и сопровождаю высоконагруженные распределённые системы и платформу, которая позволяет команде быстро выпускать продукт."
  location:
    city: "Белград"
    region: "RS"
    countryCode: "RS"
profiles:
  - {network: "GitHub",   username: "C0FFEEC0DE", url: "https://github.com/C0FFEEC0DE"}
  - {network: "LinkedIn", username: "aleksandrkrasnobai", url: "https://www.linkedin.com/in/aleksandrkrasnobai"}
  - {network: "Telegram", username: "TODO", url: "https://t.me/TODO"}
availability:
  status: "open"   # TODO: подтвердите, что открыты к предложениям
  roles: ["Senior DevOps Engineer", "SRE", "Cloud Infrastructure Engineer"]
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

Старший DevOps / SRE-инженер из Белграда, Сербия — ПМЖ, часовой пояс CET, без визовой поддержки. Строю и сопровождаю высоконагруженные распределённые системы и платформу, которая позволяет команде быстро выпускать продукт.

## Experience

### Старший DevOps-инженер — Grid Dynamics
dates: TODO — настоящее · location: Белград, Сербия · url: https://www.gridynamics.com
<!-- TODO: подтвердить точную должность и дату начала -->
- Возглавлял команду из трёх инженеров, построившую мультиязычный сервис переводов для brand safety (FastAPI + CTranslate2) — от прототипа до 40+ кластеров за шесть месяцев, ~500 млн запросов в день на 60+ языках.
- ~10× пропускная способность на том же железе и ~80% снижение стоимости за счёт оптимизации инференса и настройки флота.
- Самовосстанавливающаяся инфраструктура с двойными health-checks; стенд нагрузочного тестирования на Locust валидировал ёмкость перед каждым расширением.
<!-- TODO: добавить предыдущие роли (до Grid Dynamics, Санкт-Петербург / Россия) — LinkedIn скрывает должности, компании и даты из публичного профиля. -->

## Skills

- **Облако**: AWS (Solutions Architect Associate, Cloud Practitioner), Azure (сети)
- **Инфраструктура / DevOps**: Kubernetes, Terraform, Linux / Red Hat (RHCSA), CI/CD, оркестрация контейнеров
- **Бэкенд**: Python, FastAPI, Node.js (ESM)
- **ML / Данные**: CTranslate2, высоконагруженный инференс, нагрузочное тестирование (Locust)
- **Безопасность**: Google Cybersecurity, brand-safety системы, корпоративная архитектура
- **Подходы**: SRE, zero-trust sandboxing, code review, лидство команды

## Projects

### agnthive
url: https://agnthive.run
- Open-source MIT-плагин для Claude Code на Node.js (ESM), обеспечивающий hook-gated SDLC (discover → design → implement → verify → review → docs) с 8 специализированными агентами и набором бенчмарков, который ловит регрессии агентов до релиза. Кроссплатформенный (Linux/macOS/Windows). github.com/C0FFEEC0DE/agnthive

### opendevops.run
url: https://opendevops.run
- Fusion DevOps-платформа с автономным SRE-агентом на чистом Python; 860+ тестов. github.com/C0FFEEC0DE/opendevops.run

## Education

### TODO — Ульяновский государственный педагогический университет
location: Ульяновск, Россия
<!-- TODO: степень, направление и годы (LinkedIn скрывает их) -->

## Certificates

- **AWS Certified Solutions Architect – Associate** — Amazon Web Services (2020)
- **AWS Certified Cloud Practitioner** — Amazon Web Services (2019)
- **Red Hat Certified System Administrator (RHCSA)** — Red Hat (Credential ID 140-219-007)
- **Google Cybersecurity Certificate** — Coursera (2024)
- **Configure secure access to your workloads using Azure networking** — Microsoft (2024)
- **Enterprise Architecture in Practice** — LinkedIn (2022)
- **ICF Associate Certified Coach (ACC)** — ICF (TODO)

## Languages

- **Английский** (Professional working)
- **Русский** (родной)

## Contact

Быстрее всего по почте: hi@krasnobai.dev — обычно отвечаю в течение дня. Открыт к старшим DevOps / SRE и cloud-infrastructure ролям в удалённо-дружественных командах (Белград, Сербия — ПМЖ, часовой пояс CET, без визовой поддержки).