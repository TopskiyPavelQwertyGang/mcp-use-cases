import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from common.models import PackageQuery

mcp = FastMCP("cve-analysis")
DATA = Path(__file__).parent / "data" / "cves.json"


def _records() -> list[dict]:
    return json.loads(DATA.read_text(encoding="utf-8"))


@mcp.tool()
def get_package_context(package: str, version: str | None = None) -> dict:
    """Validate package input and return the bounded context used by the analysis."""
    query = PackageQuery(name=package, version=version)
    return {
        "package": query.name,
        "version": query.version,
        "data_source": "local-demo-dataset",
        "write_access": False,
    }


@mcp.tool()
def find_cves(package: str, version: str | None = None) -> list[dict]:
    """Return demo CVE records for a validated package name."""
    query = PackageQuery(name=package, version=version)
    return [item for item in _records() if item["package"].lower() == query.name.lower()]


@mcp.tool()
def get_cve_details(cve_id: str) -> dict:
    """Return one CVE record from the local demo dataset."""
    normalized = cve_id.strip().upper()
    if not normalized.startswith("CVE-") or len(normalized) > 40:
        raise ValueError("invalid CVE identifier")
    for item in _records():
        if item["cve"].upper() == normalized:
            return item
    return {"cve": normalized, "found": False}


@mcp.tool()
def get_fix_guidance(cve_id: str) -> dict:
    """Derive bounded remediation guidance from demo metadata without changing state."""
    details = get_cve_details(cve_id)
    if details.get("found") is False:
        return {"cve": cve_id, "guidance": "No local record; escalate to engineer."}
    affected = details.get("affected", "unknown")
    return {
        "cve": details["cve"],
        "affected": affected,
        "guidance": "Review the affected range and upgrade to a vendor-fixed version when available.",
        "requires_engineer_review": True,
    }


@mcp.prompt()
def analyze_package(package: str, version: str | None = None) -> str:
    version_text = version or "unknown"
    return (
        f"Проанализируй пакет {package} версии {version_text}. "
        "Сначала получи package context, затем найди CVE. Для значимых записей запроси детали "
        "и remediation guidance. Не выдумывай отсутствующие данные и отделяй факты от вывода модели. "
        "Финальное решение о применимости и исправлении оставь инженеру."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
