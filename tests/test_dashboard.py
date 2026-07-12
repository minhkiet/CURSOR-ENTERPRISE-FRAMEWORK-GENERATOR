"""Tests for cursor_framework.dashboard."""
from __future__ import annotations

import json
import socket
import threading
import time
import urllib.error
import urllib.request
from http.client import HTTPConnection
from pathlib import Path

import pytest

from cursor_framework.dashboard import Dashboard
from cursor_framework.indexer import Indexer


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _ensure_index(sandbox: Path) -> None:
    """Helper: write INDEX.json so dashboard has data to serve."""
    idx = Indexer(sandbox)
    idx.scan()
    idx.write_json()


def _serve_in_thread(d: Dashboard, port: int) -> threading.Thread:
    t = threading.Thread(target=d.serve, kwargs={"port": port}, daemon=True)
    t.start()
    # Wait for server to come up. Accept any response — auth-enabled
    # dashboards will respond 401 until caller sends the token.
    for _ in range(40):
        try:
            conn = HTTPConnection("127.0.0.1", port, timeout=0.2)
            try:
                conn.request("GET", "/api/stats")
                resp = conn.getresponse()
                resp.read()
                if resp.status in (200, 401):
                    return t
            finally:
                conn.close()
        except (OSError, urllib.error.URLError):
            time.sleep(0.05)
    raise RuntimeError("server did not start")


def test_serves_html(sandbox_cursor: Path, memory_path: Path):
    _ensure_index(sandbox_cursor)
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as r:
        html = r.read().decode("utf-8")
    assert "Cursor Framework Dashboard" in html


def test_api_stats(sandbox_cursor: Path, memory_path: Path):
    _ensure_index(sandbox_cursor)
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/stats") as r:
        stats = json.loads(r.read())
    assert "assets_indexed" in stats
    assert stats["assets_indexed"] > 0
    assert stats["index_fresh"] is True


def test_api_index(sandbox_cursor: Path, memory_path: Path):
    _ensure_index(sandbox_cursor)
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/index") as r:
        data = json.loads(r.read())
    assert "categories" in data
    assert "totals" in data


def test_api_memory_no_file(sandbox_cursor: Path, memory_path: Path):
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/memory") as r:
        mem = json.loads(r.read())
    assert mem["entries"] == 0


def test_404_for_unknown(sandbox_cursor: Path, memory_path: Path):
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/nope", timeout=1)
        raise AssertionError("expected 404")
    except urllib.error.HTTPError as e:
        assert e.code == 404


def test_path_traversal_blocked(sandbox_cursor: Path, memory_path: Path):
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    try:
        urllib.request.urlopen(
            f"http://127.0.0.1:{port}/../../etc/passwd", timeout=1
        )
        raise AssertionError("traversal should have been blocked")
    except urllib.error.HTTPError as e:
        assert e.code == 404


def test_auth_required_when_token_set(sandbox_cursor: Path, memory_path: Path):
    _ensure_index(sandbox_cursor)
    port = _free_port()
    d = Dashboard(
        root=sandbox_cursor, memory_path=memory_path, auth_token="secret123"
    )
    _serve_in_thread(d, port)

    # No token → 401
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/api/stats", timeout=1)
        raise AssertionError("expected 401")
    except urllib.error.HTTPError as e:
        assert e.code == 401

    # With query token → 200
    with urllib.request.urlopen(
        f"http://127.0.0.1:{port}/api/stats?token=secret123", timeout=1
    ) as r:
        stats = json.loads(r.read())
    assert stats["assets_indexed"] > 0

    # With header token → 200
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/stats",
        headers={"X-Auth-Token": "secret123"},
    )
    with urllib.request.urlopen(req, timeout=1) as r:
        stats = json.loads(r.read())
    assert stats["assets_indexed"] > 0


def test_auth_wrong_token_rejected(sandbox_cursor: Path, memory_path: Path):
    port = _free_port()
    d = Dashboard(
        root=sandbox_cursor, memory_path=memory_path, auth_token="secret123"
    )
    _serve_in_thread(d, port)
    try:
        urllib.request.urlopen(
            f"http://127.0.0.1:{port}/api/stats?token=wrong", timeout=1
        )
        raise AssertionError("expected 401")
    except urllib.error.HTTPError as e:
        assert e.code == 401