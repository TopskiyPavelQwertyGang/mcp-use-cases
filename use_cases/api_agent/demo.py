import httpx

from common.policy import check_api_request


def safe_get(url: str) -> dict:
    decision = check_api_request("GET", url)
    if not decision.allowed:
        return {"status": "BLOCKED", "reason": decision.reason}

    response = httpx.get(url, timeout=5.0)
    return {"status": "OK", "code": response.status_code, "url": str(response.url)}


if __name__ == "__main__":
    for url in [
        "https://httpbin.org/get",
        "https://example.com/",
    ]:
        print(url, "→", safe_get(url))
