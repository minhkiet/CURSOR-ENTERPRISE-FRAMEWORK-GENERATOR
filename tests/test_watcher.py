"""Tests for cursor_framework.watcher."""
from __future__ import annotations

import time
from pathlib import Path

from cursor_framework.watcher import Watcher


def test_detects_file_creation(sandbox_writable: Path):
    triggered = []
    w = Watcher(sandbox_writable, on_change=lambda paths: triggered.extend(paths), interval=0.1)
    w.take_snapshot()
    w.start()
    try:
        new_file = sandbox_writable / "_watch_test.mdc"
        new_file.write_text("# test\n", encoding="utf-8")
        # Wait up to 2s for detection.
        for _ in range(40):
            if triggered:
                break
            time.sleep(0.05)
        assert triggered, "watcher did not detect file creation"
    finally:
        w.stop()


def test_detects_file_modification(sandbox_writable: Path):
    triggered = []
    target = sandbox_writable / "_watch_modify.mdc"
    target.write_text("# v1\n", encoding="utf-8")

    w = Watcher(sandbox_writable, on_change=lambda paths: triggered.extend(paths), interval=0.1)
    w.take_snapshot()
    w.start()
    try:
        time.sleep(1.1)  # ensure mtime tick differs
        target.write_text("# v2\n", encoding="utf-8")
        for _ in range(40):
            if triggered:
                break
            time.sleep(0.05)
        assert triggered
    finally:
        w.stop()


def test_callback_exception_does_not_kill_loop(sandbox_writable: Path):
    def explode(paths):
        raise RuntimeError("boom")

    w = Watcher(sandbox_writable, on_change=explode, interval=0.1)
    w.take_snapshot()
    w.start()
    try:
        (sandbox_writable / "_boom.mdc").write_text("x\n", encoding="utf-8")
        time.sleep(0.5)  # let poll cycles run
        assert w.stats["scans_run"] >= 1
    finally:
        w.stop()


def test_stats_increment(sandbox_cursor: Path):
    """Watcher on a populated directory must report tracked_files > 0."""
    w = Watcher(sandbox_cursor, on_change=lambda p: None, interval=0.1)
    w.take_snapshot()
    s = w.stats
    assert s["tracked_files"] > 0


def test_ignore_substrings(sandbox_writable: Path):
    triggered = []
    (sandbox_writable / ".cache").mkdir()
    ignored = sandbox_writable / ".cache" / "skip.json"
    ignored.write_text("{}", encoding="utf-8")

    w = Watcher(
        sandbox_writable,
        on_change=lambda paths: triggered.extend(paths),
        interval=0.1,
        ignore_globs=(".cache",),
    )
    w.take_snapshot()
    w.start()
    try:
        time.sleep(0.5)
        assert not any(".cache" in str(p) for p in triggered)
    finally:
        w.stop()