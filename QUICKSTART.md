# Quick Start

## 1. Установка

```bash
git clone https://github.com/TopskiyPavelQwertyGang/mcp-use-cases.git
cd mcp-use-cases
uv sync
```

Если `uv` не установлен:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" httpx pydantic
```

## 2. CVE Analysis

```bash
uv run python use_cases/cve_analysis/demo.py
```

Ожидаемая идея результата:

```text
Package: freerdp3
Findings: 2
- CVE-DEMO-2026-0001 [HIGH] ...
- CVE-DEMO-2026-0002 [MEDIUM] ...
```

## 3. API Agent

```bash
uv run python use_cases/api_agent/demo.py
```

Разрешённый домен пройдёт policy check. Неизвестный домен будет заблокирован allowlist-политикой.

## 4. Files & Report

```bash
uv run python use_cases/files_report/demo.py
```

После запуска появится:

```text
use_cases/files_report/output/report.md
```

Попробуйте заменить `sample.txt` на `../../README.md` — path validation должна остановить выход за разрешённую директорию.

## 5. MCP Inspector

Любой сервер можно открыть через Inspector, например:

```bash
uv run mcp dev use_cases/cve_analysis/server.py
```

После этого посмотрите доступные tools и вызовите их вручную.

## Главное упражнение

Не просто запустите примеры. Попробуйте изменить границы:

- добавьте новый API host в allowlist;
- уберите его обратно и проверьте BLOCKED;
- добавьте новый mock CVE;
- попробуйте path traversal в файловом кейсе;
- добавьте отдельное подтверждение для записи отчёта.

Именно изменение policy хорошо показывает разницу между возможностями модели и возможностями системы.