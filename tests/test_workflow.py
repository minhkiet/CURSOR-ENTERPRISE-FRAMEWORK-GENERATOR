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


def test_cache_hit_persists_memory_to_disk(sandbox_cursor: Path, memory_path: Path):
    """Step 1/3: cache hit branch must save memory to disk so a process
    crash between hits doesn't lose stats or HOT-tier entries."""
    wf1 = Workflow(root=sandbox_cursor, memory_path=memory_path, strict_persist=True)
    r1 = wf1.ask("redesign landing page for SaaS")
    assert r1.from_cache is False  # first call: miss

    # Second call hits cache — this branch is what we fixed.
    r2 = wf1.ask("redesign landing page for SaaS")
    assert r2.from_cache is True

    # Memory file must exist and be non-empty after a cache hit.
    assert memory_path.exists()
    size = memory_path.stat().st_size
    assert size > 0, "cache hit did not persist memory to disk"

    # Restart simulation: new Workflow reads same file. Stats must survive.
    wf2 = Workflow(root=sandbox_cursor, memory_path=memory_path)
    assert wf2.memory._hits >= 1, "hits counter lost after restart"


def test_latency_ms_recorded_on_hit_and_miss(sandbox_cursor: Path, memory_path: Path):
    """Step 3/3: WorkflowResult.latency_ms reflects the full ask() time
    on both cache hit and cache miss paths."""
    wf = Workflow(root=sandbox_cursor, memory_path=memory_path)

    # First call: cache miss → must build context.
    r1 = wf.ask("redesign landing page for SaaS")
    assert r1.latency_ms >= 0.0
    assert r1.latency_ms < 5000  # sanity: under 5s on dev machine

    # Second call: cache hit → latency should be much smaller.
    r2 = wf.ask("redesign landing page for SaaS")
    assert r2.from_cache is True
    assert r2.latency_ms >= 0.0
    assert r2.latency_ms <= r1.latency_ms + 5  # hit at worst as slow as miss


def test_latency_ms_default_zero_on_construction():
    """Default value is 0.0 so callers iterating WorkflowResult without
    timing data still get a sane number."""
    from cursor_framework.workflow import WorkflowResult
    r = WorkflowResult(context=None, from_cache=False,
                       memory_hits=0, memory_misses=0, asset_count=0)
    assert r.latency_ms == 0.0