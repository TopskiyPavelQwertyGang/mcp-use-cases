from dataclasses import dataclass
from urllib.parse import urlparse
from pathlib import Path


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str


ALLOWED_API_HOSTS = {"api.github.com", "httpbin.org"}
ALLOWED_HTTP_METHODS = {"GET"}


def check_api_request(method: str, url: str) -> PolicyDecision:
    method = method.upper()
    host = urlparse(url).hostname or ""

    if method not in ALLOWED_HTTP_METHODS:
        return PolicyDecision(False, f"HTTP method {method} is not allowed")
    if host not in ALLOWED_API_HOSTS:
        return PolicyDecision(False, f"Host {host} is not in allowlist")
    return PolicyDecision(True, "request allowed")


def safe_path(base_dir: Path, candidate: str) -> Path:
    base = base_dir.resolve()
    target = (base / candidate).resolve()
    if base != target and base not in target.parents:
        raise ValueError("Path escapes allowed directory")
    return target
