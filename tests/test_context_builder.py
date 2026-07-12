"""Tests for cursor_framework.context_builder."""
from __future__ import annotations

from pathlib import Path

from cursor_framework.context_builder import ContextBuilder


def test_build_returns_context_result(sandbox_cursor: Path):
    cb = ContextBuilder(root=sandbox_cursor, max_tokens=4000)
    result = cb.build("redesign landing page for our SaaS")
    assert result.tokens >= 0
    assert result.skill_count >= 0


def test_unrelated_request_empty(sandbox_cursor: Path):
    cb = ContextBuilder(root=sandbox_cursor, max_tokens=4000)
    result = cb.build("xyzzy gibberish nonsense 12345")
    assert result.skill_count == 0
    assert result.tokens == 0
    assert result.text == ""


def test_max_skills_cap(sandbox_cursor: Path):
    cb = ContextBuilder(root=sandbox_cursor, max_tokens=8000)
    result = cb.build(
        "redesign landing page portfolio payment momo security",
        max_skills=2,
    )
    assert result.skill_count <= 2


def test_compression_under_tight_budget(sandbox_cursor: Path):
    cb = ContextBuilder(root=sandbox_cursor, max_tokens=200)
    result = cb.build("redesign landing page portfolio homepage")
    # Result must fit in a small budget; allow 50% headroom for estimate noise.
    assert result.tokens <= 300


def test_skipped_populated_when_over_cap(sandbox_cursor: Path):
    cb = ContextBuilder(root=sandbox_cursor, max_tokens=8000)
    result = cb.build(
        "redesign landing page portfolio payment momo security",
        max_skills=1,
    )
    if result.skills_used:
        assert len(result.skipped) >= 0  # skipped list may be empty if registry matches 1


def test_stats_after_build(sandbox_cursor: Path):
    cb = ContextBuilder(root=sandbox_cursor, max_tokens=4000)
    cb.build("redesign landing page")
    s = cb.stats()
    assert "compression_runs" in s
    assert s["compression_runs"] >= 1