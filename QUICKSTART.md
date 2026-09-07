# Quick Start

## 1. Установка

```bash
git clone https://github.com/TopskiyPavelQwertyGang/mcp-use-cases.git
cd mcp-use-cases
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Проверка версии MCP SDK:

```bash
python -m pip show mcp | grep Version
```

Для текущих примеров используется MCP SDK v2.

## 2. CVE Analysis

Запускайте демо как Python-модуль из корня репозитория, чтобы пакет `common` корректно находился:

```bash
python -m use_cases.cve_analysis.demo
```

Ожидаемый результат:

```text
Package: freerdp3
Findings: 2
- CVE-DEMO-2026-0001 [HIGH] ...
- CVE-DEMO-2026-0002 [MEDIUM] ...
```

Источник данных для этого воспроизводимого демо — локальный файл `use_cases/cve_analysis/data/cves.json`. На этом этапе LLM не используется: проверяется MCP-контур и структурированный tool call.

## 3. API Agent

```bash
python -m use_cases.api_agent.demo
```

Разрешённый домен пройдёт policy check. Неизвестный домен будет заблокирован allowlist-политикой.

## 4. Files & Report

```bash
python -m use_cases.files_report.demo
```

После запуска появится:

```text
use_cases/files_report/output/report.md
```

Попробуйте заменить `sample.txt` на `../../README.md` — path validation должна остановить выход за разрешённую директорию.

## 5. MCP Inspector

Для Inspector нужны Node.js/npm и `npx`.

CVE server запускается через `stdio`. Рабочая команда, проверенная на Kali:

```bash
npx @modelcontextprotocol/inspector \
  .venv/bin/python \
  -m use_cases.cve_analysis.server
```

В Inspector:

1. откройте `Tools`;
2. выберите `find_cves`;
3. передайте `package = freerdp3`;
4. выполните tool call;
5. проверьте structured output и запись `TOOLS/CALL` в protocol log.

Аналогично можно открыть другие серверы:

```bash
npx @modelcontextprotocol/inspector .venv/bin/python -m use_cases.api_agent.server
npx @modelcontextprotocol/inspector .venv/bin/python -m use_cases.files_report.server
```

## Важно про архитектуру демо

MCP не является LLM. В Inspector человек вручную выступает клиентом: выполняет discovery (`tools/list`) и вызывает инструмент (`tools/call`). Следующий уровень — подключить LLM-клиент, который будет выбирать инструмент и аргументы самостоятельно.

## Главное упражнение

Не просто запустите примеры. Попробуйте изменить границы:

- добавьте новый API host в allowlist;
- уберите его обратно и проверьте BLOCKED;
- добавьте новый mock CVE;
- попробуйте path traversal в файловом кейсе;
- добавьте отдельное подтверждение для записи отчёта.

Именно изменение policy хорошо показывает разницу между возможностями модели и возможностями системы.
