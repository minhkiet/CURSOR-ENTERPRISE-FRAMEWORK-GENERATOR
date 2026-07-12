"""Tests for cursor_framework.indexer."""
from __future__ import annotations

from pathlib import Path

import pytest

from cursor_framework.indexer import AssetEntry, Indexer


def test_scan_returns_categories(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    result = idx.scan()
    # Every tracked category must be present (even if empty).
    expected_cats = {
        "agents", "commands", "hooks", "knowledge", "memory",
        "prompts", "references", "rules", "scripts", "skills",
        "templates", "workflows",
    }
    assert expected_cats.issubset(set(result.categories.keys()))


def test_totals_match_ground_truth(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    result = idx.scan()
    # rules/ has .md and .mdc files; we know at least 1 of each exists in
    # a real framework checkout.
    real_rules = list((sandbox_cursor / "rules").rglob("*.mdc"))
    real_rules += list((sandbox_cursor / "rules").rglob("*.md"))
    assert result.totals["rules"] == len(real_rules)


def test_skills_are_directories(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    result = idx.scan()
    for entry in result.categories["skills"]:
        assert entry.kind == "directory"
        assert entry.category == "skills"


def test_skill_entries_have_metadata(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    result = idx.scan()
    skills = result.categories["skills"]
    assert skills, "no skills found"
    # At least one skill should have parsed frontmatter (description non-empty)
    with_desc = [s for s in skills if s.description]
    assert with_desc, "no skill descriptions parsed"


def test_write_json_creates_file(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    idx.scan()
    out = idx.write_json()
    assert out.exists()
    import json
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["totals"]["grand_total"] == idx.result.totals["grand_total"]


def test_write_markdown_contains_totals(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    idx.scan()
    out = idx.write_markdown()
    text = out.read_text(encoding="utf-8")
    assert "Auto-generated" in text
    assert "grand_total" in text
    assert str(idx.result.totals["grand_total"]) in text


def test_nonexistent_root_raises(tmp_path: Path):
    idx = Indexer(tmp_path / "does_not_exist")
    with pytest.raises(FileNotFoundError):
        idx.scan()


def test_stats_property(sandbox_cursor: Path):
    idx = Indexer(sandbox_cursor)
    idx.scan()
    assert "grand_total" in idx.stats
    assert idx.stats["grand_total"] == idx.result.totals["grand_total"]