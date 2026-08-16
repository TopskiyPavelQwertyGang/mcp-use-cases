import json
from pathlib import Path

from common.models import PackageQuery


DATA = Path(__file__).parent / "data" / "cves.json"


def analyze_package(name: str, version: str | None = None) -> list[dict]:
    query = PackageQuery(name=name, version=version)
    records = json.loads(DATA.read_text(encoding="utf-8"))
    return [item for item in records if item["package"].lower() == query.name.lower()]


if __name__ == "__main__":
    package = "freerdp3"
    findings = analyze_package(package)

    print(f"Package: {package}")
    print(f"Findings: {len(findings)}")
    for item in findings:
        print(f"- {item['cve']} [{item['severity']}] {item['summary']}")
