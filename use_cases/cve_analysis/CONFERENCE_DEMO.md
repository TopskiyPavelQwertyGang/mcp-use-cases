# Conference demo: CVE analysis pipeline

Цель демо — показать не чат с LLM, а управляемый workflow, где модель выбирает ограниченные MCP-инструменты, получает структурированные данные и оставляет ответственное решение инженеру.

## Flow

```text
USER
  ↓
AI HOST / AGENT
  ↓
MCP CLIENT
  ↓
CVE ANALYSIS MCP SERVER
  ├─ get_package_context
  ├─ find_cves
  ├─ get_cve_details
  └─ get_fix_guidance
  ↓
STRUCTURED CONTEXT
  ↓
LLM ANALYSIS
  ↓
ENGINEER REVIEW
```

## Suggested prompt

```text
Проанализируй freerdp3 версии 3.8.0. Используй доступные MCP tools, покажи найденные CVE, отдели факты из источника от своего вывода и предложи дальнейшие действия. Ничего не изменяй без подтверждения инженера.
```

## What to show on stage

1. MCP Inspector or AI host discovers the four tools.
2. The model requests package context.
3. The model calls `find_cves`.
4. For a HIGH finding it calls `get_cve_details` and `get_fix_guidance`.
5. The final answer explicitly leaves applicability/remediation approval to the engineer.
6. Switch to `mcp-secure-agents` and demonstrate that a write/shell action is denied while export requires HITL.

## Security message

The LLM is not the authorization layer. Inputs are validated, capabilities are bounded, side effects are policy-controlled, and sensitive actions can cross a human approval boundary.

## Demo limitation

The dataset is intentionally local and synthetic. This demonstrates orchestration and security boundaries, not production vulnerability intelligence. A production implementation would replace the data adapter and add IAM, secrets management, observability, rate limits, durable audit and scenario-specific policy enforcement.
