from pathlib import Path

from common.models import ReportRequest
from common.policy import safe_path

BASE = Path(__file__).parent
INPUT = BASE / "input"
OUTPUT = BASE / "output"


def build_report(source_file: str, output_file: str = "report.md") -> Path:
    req = ReportRequest(source_file=source_file, output_file=output_file)
    source = safe_path(INPUT, req.source_file)
    target = safe_path(OUTPUT, req.output_file)

    text = source.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    report = "# Security Report\n\n" + "\n".join(f"- {line}" for line in lines)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(report + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    path = build_report("sample.txt")
    print(f"Report created: {path}")
