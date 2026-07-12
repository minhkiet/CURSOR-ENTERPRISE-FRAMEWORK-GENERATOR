"""Tests for Dashboard auto-invalidate when wired to Workflow."""
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
from cursor_framework.workflow import Workflow


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _ensure_index(sandbox: Path) -> None:
    idx = Indexer(sandbox)
    idx.scan()
    idx.write_json()


def _serve_in_thread(d: Dashboard, port: int) -> threading.Thread:
    t = threading.Thread(target=d.serve, kwargs={"port": port}, daemon=True)
    t.start()
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


def test_dashboard_uses_workflow_when_wired(sandbox_cursor: Path, memory_path: Path):
    _ensure_index(sandbox_cursor)
    port = _free_port()

    wf = Workflow(
        root=sandbox_cursor,
        memory_path=memory_path,
        auto_watch=True,
        watch_interval=0.1,
    )
    try:
        d = Dashboard(
            root=sandbox_cursor,
            memory_path=memory_path,
            workflow=wf,
        )
        _serve_in_thread(d, port)

        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/stats") as r:
            stats = json.loads(r.read())
        # workflow stats must be present in the response.
        assert "workflow" in stats
        assert stats["workflow"]["assets_indexed"] > 0
    finally:
        wf.stop_watching()


def test_dashboard_rebuilds_after_watcher_invalidation(
    sandbox_writable: Path, memory_path: Path
):
    """If Workflow watcher invalidates the index, the next /api/stats
    request must rebuild so the dashboard stays fresh."""
    # Populate sandbox with a real file so workflow.index has something.
    (sandbox_writable / "rules").mkdir(exist_ok=True)
    (sandbox_writable / "rules" / "x.mdc").write_text("# x\n", encoding="utf-8")
    _ensure_index(sandbox_writable)

    port = _free_port()
    wf = Workflow(
        root=sandbox_writable,
        memory_path=memory_path,
        auto_watch=True,
        watch_interval=0.1,
    )
    try:
        d = Dashboard(root=sandbox_writable, memory_path=memory_path, workflow=wf)
        _serve_in_thread(d, port)

        # Force index build so we have a baseline.
        wf._ensure_index()
        assert wf._index is not None
        before = wf._index.result.totals["grand_total"]

        # Manually invalidate (simulate watcher callback).
        wf._on_watch_change([])
        assert wf._index is None

        # Next request rebuilds.
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/stats") as r:
            stats = json.loads(r.read())
        # Index must have been rebuilt.
        assert wf._index is not None
        assert stats["assets_indexed"] >= before
    finally:
        wf.stop_watching()


def test_dashboard_without_workflow_still_works(
    sandbox_cursor: Path, memory_path: Path
):
    """Backward compat: Dashboard without workflow arg still serves /api/stats
    using INDEX.json on disk."""
    _ensure_index(sandbox_cursor)
    port = _free_port()
    d = Dashboard(root=sandbox_cursor, memory_path=memory_path)
    _serve_in_thread(d, port)

    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/stats") as r:
        stats = json.loads(r.read())
    assert "workflow" not in stats  # no workflow wired
    assert stats["assets_indexed"] > 0