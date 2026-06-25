"""
HTTP Utilities

HTTP request/response helpers.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class HTTPResponse:
    """HTTP response wrapper."""

    status_code: int
    headers: dict
    body: str
    error: Optional[str] = None


def make_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    timeout: int = 30,
) -> HTTPResponse:
    """
    Make HTTP request.

    Args:
        url: Request URL
        method: HTTP method
        headers: Request headers
        data: Request body data
        timeout: Request timeout

    Returns:
        HTTPResponse object
    """
    headers = headers or {}
    headers["User-Agent"] = "CursorFramework/1.0"

    req = urllib.request.Request(url, method=method, headers=headers)

    if data:
        if isinstance(data, dict):
            data = urllib.parse.urlencode(data).encode()
        req.data = data

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return HTTPResponse(
                status_code=response.status,
                headers=dict(response.headers),
                body=body,
            )
    except urllib.error.HTTPError as e:
        return HTTPResponse(
            status_code=e.code,
            headers=dict(e.headers),
            body=e.read().decode("utf-8") if e.fp else "",
            error=str(e),
        )
    except urllib.error.URLError as e:
        return HTTPResponse(
            status_code=0,
            headers={},
            body="",
            error=str(e.reason),
        )


def get_json(url: str, headers: Optional[dict] = None) -> Optional[Any]:
    """
    Get JSON from URL.

    Args:
        url: Request URL
        headers: Optional headers

    Returns:
        Parsed JSON or None
    """
    response = make_request(url, headers=headers)
    if response.status_code == 200:
        try:
            return json.loads(response.body)
        except json.JSONDecodeError:
            return None
    return None


def post_json(
    url: str,
    data: dict,
    headers: Optional[dict] = None,
) -> Optional[Any]:
    """
    POST JSON to URL.

    Args:
        url: Request URL
        data: JSON data to post
        headers: Optional headers

    Returns:
        Parsed JSON response or None
    """
    headers = headers or {}
    headers["Content-Type"] = "application/json"

    response = make_request(
        url,
        method="POST",
        headers=headers,
        data=json.dumps(data).encode(),
    )

    if response.status_code in (200, 201):
        try:
            return json.loads(response.body)
        except json.JSONDecodeError:
            return None
    return None


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid
    """
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def encode_params(params: dict) -> str:
    """
    URL encode parameters.

    Args:
        params: Parameters to encode

    Returns:
        Encoded string
    """
    return urllib.parse.urlencode(params)
