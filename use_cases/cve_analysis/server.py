import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from common.models import PackageQuery

mcp = FastMCP("cve-analysis")
DATA = Path(__file__).parent / "data" / "cves.json"


@mcp.tool()
def find_cves(package: str, version: str | None = None) -> list[dict]:
    """Return demo CVE records for an allowed package name."""
    query = PackageQuery(name=package, version=version)
    records = json.loads(DATA.read_text(encoding="utf-8"))
    return [item for item in records if item["package"].lower() == query.name.lower()]


@mcp.prompt()
def analyze_package(package: str) -> str:
    return (
        f"Проанализируй найденные уязвимости пакета {package}. "
        "Сначала перечисли HIGH, затем MEDIUM и LOW. Не выдумывай отсутствующие CVE."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
