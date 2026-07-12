"""Tests for cursor_framework.workflow."""
from __future__ import annotations

from pathlib import Path

from cursor_framework.workflow import Workflow


def test_first_ask_misses_cache(sandbox_cursor: Path, memory_path: Path):
    wf = Workflow(root=sandbox_cursor, memory_path=memory_path)
    r = wf.ask("redesign landing page")
    assert r.from_cache is False


def test_repeat_ask_hits_cache(sandbox_cursor: Path, memory_path: Path):
    wf = Workflow(root=sandbox_cursor, memory_path=memory_path)
    wf.ask("redesign landing page")
    r2 = wf.ask("redesign landing page")
    assert r2.from_cache is True


def test_simulation_restart_restores_memory(sandbox_cursor: Path, memory_path: Path):
    wf1 = Workflow(root=sandbox_cursor, memory_path=memory_path)
    wf1.ask("redesign landing page")

    wf2 = Workflow(root=sandbox_cursor, memory_path=memory_path)
    s = wf2.stats()
    assert s["restored_entries"] >= 1


def test_stats_includes_assets(sandbox_cursor: Path, memory_path: Path):
    wf = Workflow(root=sandbox_cursor, memory_path=memory_path)
    wf.ask("redesign landing page")
    s = wf.stats()
    assert s["assets_indexed"] > 0
    assert "memory_hits" in s


def test_warm_returns_stats(sandbox_cursor: Path, memory_path: Path):
    wf = Workflow(root=sandbox_cursor, memory_path=memory_path)
    out = wf.warm()
    assert "assets_indexed" in out
    assert out["assets_indexed"] > 0


def test_graceful_fallback_after_restart(sandbox_cursor: Path, memory_path: Path):
    """After restart, cached ContextResult becomes dict on load.
    Workflow must rebuild without crashing."""
    wf1 = Workflow(root=sandbox_cursor, memory_path=memory_path)
    wf1.ask("redesign landing page")

    wf2 = Workflow(root=sandbox_cursor, memory_path=memory_path)
    r = wf2.ask("redesign landing page")
    assert r.context.skill_count >= 0
    assert r.context.tokens >= 0