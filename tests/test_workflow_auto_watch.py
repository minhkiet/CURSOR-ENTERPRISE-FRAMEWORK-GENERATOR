"""Tests for Workflow auto-watcher integration."""
from __future__ import annotations

import time
from pathlib import Path

from cursor_framework.workflow import Workflow


def test_auto_watch_off_by_default(sandbox_cursor: Path, memory_path: Path):
    wf = Workflow(root=sandbox_cursor, memory_path=memory_path)
    assert wf._watcher is None


def test_auto_watch_invalidates_index_on_change(sandbox_writable: Path, memory_path: Path):
    """When watcher detects a change, _index must be invalidated so
    the next ask() rebuilds with fresh data."""
    # Pre-populate scratch with a fake SKILL.md so SkillDiscovery finds it
    (sandbox_writable / "rules").mkdir(exist_ok=True)

    wf = Workflow(
        root=sandbox_writable,
        memory_path=memory_path,
        auto_watch=True,
        watch_interval=0.1,
    )
    try:
        # First ask: builds the index
        wf.ask("test query")
        assert wf._index is not None
        old_index = wf._index

        # Trigger a change in the scratch dir
        (sandbox_writable / "rules" / "_new.mdc").write_text("# x\n", encoding="utf-8")

        # Wait for watcher to detect + invalidate
        for _ in range(40):
            if wf._index is None:
                break
            time.sleep(0.05)

        assert wf._index is None, "watcher did not invalidate index"
    finally:
        wf.stop_watching()


def test_stop_watching(sandbox_writable: Path, memory_path: Path):
    wf = Workflow(
        root=sandbox_writable,
        memory_path=memory_path,
        auto_watch=True,
        watch_interval=0.1,
    )
    assert wf._watcher is not None
    wf.stop_watching()
    assert wf._watcher is None
    # Idempotent
    wf.stop_watching()
    assert wf._watcher is None


def test_stats_include_watcher(sandbox_cursor: Path, memory_path: Path):
    wf = Workflow(
        root=sandbox_cursor,
        memory_path=memory_path,
        auto_watch=True,
        watch_interval=0.1,
    )
    try:
        time.sleep(0.3)  # let watcher poll
        s = wf.stats()
        assert "watcher_scans" in s
        assert s["watcher_scans"] >= 1
    finally:
        wf.stop_watching()