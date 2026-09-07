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

## 2. CVE Analysis без LLM

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

Источник данных для воспроизводимого демо — локальный файл `use_cases/cve_analysis/data/cves.json`.

## 3. MCP Inspector

Для Inspector нужны Node.js/npm и `npx`.

Рабочая команда, проверенная на Kali:

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

На этом этапе LLM не используется: человек вручную выступает MCP-клиентом.

## 4. Local LLM + MCP end-to-end

Для полного агентного сценария используется локальная Ollama и `qwen3:1.7b`.

Установите Ollama для Linux, затем загрузите модель:

```bash
ollama pull qwen3:1.7b
ollama list
```

Проверьте, что Python-клиент Ollama установлен через зависимости проекта:

```bash
python -c "import ollama; print('OLLAMA PYTHON OK')"
```

Запуск end-to-end демо:

```bash
python llm_agent_demo.py
```

Ожидаемая цепочка:

```text
USER → Проверь уязвимости пакета freerdp3
MCP → available tools: find_cves
LLM → TOOL CALL: find_cves
MCP → TOOL RESULT: structured CVE data
LLM → FINAL ANSWER
```

Здесь локальная LLM получает список MCP tools, сама выбирает `find_cves`, передаёт аргументы, получает структурированный результат и формирует итоговый ответ.

Важно: данные CVE в демо локальные и учебные. Модель не должна придумывать отсутствующие факты или fixed version, если их нет в tool result.

## 5. API Agent

```bash
python -m use_cases.api_agent.demo
```

Разрешённый домен пройдёт policy check. Неизвестный домен будет заблокирован allowlist-политикой.

## 6. Files & Report

```bash
python -m use_cases.files_report.demo
```

После запуска появится:

```text
use_cases/files_report/output/report.md
```

Попробуйте заменить `sample.txt` на `../../README.md` — path validation должна остановить выход за разрешённую директорию.

## Важно про архитектуру демо

MCP не является LLM. Есть два отдельных режима:

```text
Inspector demo:
Human → MCP Client → MCP Server → Tool

Agent demo:
User → LLM → MCP Client → MCP Server → Tool → LLM → Answer
```

Чем больше автономности получает агент, тем важнее policy enforcement, validation, HITL и audit.
