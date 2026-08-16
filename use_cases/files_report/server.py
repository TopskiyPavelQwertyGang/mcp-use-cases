from pathlib import Path

from mcp.server.fastmcp import FastMCP
from common.models import ReportRequest
from common.policy import safe_path

mcp = FastMCP("files-report-agent")
BASE = Path(__file__).parent
INPUT = BASE / "input"
OUTPUT = BASE / "output"


@mcp.tool()
def read_input_file(filename: str) -> str:
    """Read only from the use case input directory."""
    path = safe_path(INPUT, filename)
    return path.read_text(encoding="utf-8")


@mcp.tool()
def save_report(source_file: str, output_file: str = "report.md") -> dict:
    """Create a report only inside the output directory."""
    req = ReportRequest(source_file=source_file, output_file=output_file)
    source = safe_path(INPUT, req.source_file)
    target = safe_path(OUTPUT, req.output_file)

    text = source.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    report = "# Security Report\n\n" + "\n".join(f"- {line}" for line in lines)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(report + "\n", encoding="utf-8")
    return {"status": "OK", "path": str(target.relative_to(BASE))}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
