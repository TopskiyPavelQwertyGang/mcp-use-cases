import httpx

from mcp.server.fastmcp import FastMCP
from common.policy import check_api_request

mcp = FastMCP("safe-api-agent")


@mcp.tool()
def safe_get(url: str) -> dict:
    """GET only from explicitly allowlisted hosts."""
    decision = check_api_request("GET", url)
    if not decision.allowed:
        return {"status": "BLOCKED", "reason": decision.reason}

    response = httpx.get(url, timeout=5.0)
    return {
        "status": "OK",
        "code": response.status_code,
        "url": str(response.url),
        "body_preview": response.text[:300],
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
