# MCP Use Cases

Практические сценарии, где **MCP + AI-агенты** экономят время в реальной работе.

> Репозиторий отвечает на вопрос: **«Я понял MCP и безопасность. Что я могу автоматизировать уже завтра?»**

## 3 сценария

### 1. CVE Analysis Agent

```text
Пакет → CVE → версии → приоритет → краткий отчёт
```

Агент получает имя пакета, собирает данные из локального mock-источника, фильтрует уязвимости по версии и формирует итог.

Папка: [`use_cases/cve_analysis`](use_cases/cve_analysis)

---

### 2. API Agent

```text
Задача → разрешённый API → нормализация → ответ
```

Пример безопасной работы с внешним API через allowlist доменов и методов.

Папка: [`use_cases/api_agent`](use_cases/api_agent)

---

### 3. Files & Report Agent

```text
Файлы → извлечение данных → сводка → отчёт
```

Агент читает только разрешённую директорию и сохраняет результат только в `output/`.

Папка: [`use_cases/files_report`](use_cases/files_report)

## Почему именно эти кейсы

Они показывают три самых частых паттерна:

- **данные безопасности** — CVE, пакеты, версии;
- **внешние сервисы** — API;
- **локальные данные** — файлы и отчёты.

При этом каждый пример специально сделан небольшим: его можно прочитать, запустить и изменить под себя за 10–20 минут.

## Быстрый старт

### Требования

- Python 3.10+
- `uv` или `pip`

### Установка

```bash
git clone https://github.com/TopskiyPavelQwertyGang/mcp-use-cases.git
cd mcp-use-cases
uv sync
```

Или:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" httpx pydantic
```

## Запуск

### CVE Analysis

```bash
uv run python use_cases/cve_analysis/demo.py
```

### API Agent

```bash
uv run python use_cases/api_agent/demo.py
```

### Files & Report

```bash
uv run python use_cases/files_report/demo.py
```

## Что важно заметить

Все три примера используют один и тот же подход:

```text
USER
  ↓
AGENT
  ↓
POLICY / VALIDATION
  ↓
TOOL
  ↓
RESULT
```

То есть **use case меняется, security-принцип остаётся тем же**.

## Структура

```text
.
├── README.md
├── pyproject.toml
├── QUICKSTART.md
├── common/
│   ├── policy.py
│   └── models.py
└── use_cases/
    ├── cve_analysis/
    │   ├── demo.py
    │   ├── server.py
    │   └── data/cves.json
    ├── api_agent/
    │   ├── demo.py
    │   └── server.py
    └── files_report/
        ├── demo.py
        ├── server.py
        ├── input/
        │   └── sample.txt
        └── output/
            └── .gitkeep
```

## Learning path

1. **mcp-protocol-guide** — понять MCP.
2. **mcp-secure-agents** — понять границы и policy enforcement.
3. **mcp-use-cases** — применить подход к рабочим сценариям.

## Идеи для адаптации

- анализ CVE для вашего дистрибутива;
- проверка пакетов перед релизом;
- внутренний API-helper;
- генерация отчётов из логов;
- triage входящих security findings;
- read-only доступ к CMDB / asset inventory;
- подготовка черновиков Jira / Confluence / Markdown-отчётов.

## Важно

Примеры учебные и специально используют mock/local data там, где это помогает избежать ключей, токенов и опасных прав.

Перед production-использованием добавьте IAM, rate limits, аудит, секрет-хранилище, полноценную модель угроз и отдельную policy enforcement layer.

---

**Learn → Secure → Build**

Этот репозиторий — третий уровень learning path.