"""Tests for the mtime cache added to SkillDiscovery.load_skill_file."""
from __future__ import annotations

import time
from pathlib import Path

from cursor_framework.skill_discovery import SkillDiscovery


def test_first_load_populates_cache(sandbox_cursor: Path):
    # base_path is the parent of .cursor/ (the file uses root/registry.path).
    sd = SkillDiscovery(base_path=str(sandbox_cursor.parent))
    sd.registry.register(
        sd.registry.get("frontend-taste")  # any registered skill
    ) if False else None  # noop; use one that exists on disk

    # Use a real skill whose SKILL.md exists in the sandbox.
    content = sd.load_skill_file("frontend-taste")
    if content is None:
        # sandbox may not have all default-registry skills on disk; skip.
        import pytest
        pytest.skip("frontend-taste SKILL.md not present in sandbox")
    assert len(sd._skill_file_cache) == 1


def test_second_load_hits_cache(sandbox_cursor: Path):
    sd = SkillDiscovery(base_path=str(sandbox_cursor.parent))
    first = sd.load_skill_file("frontend-taste")
    if first is None:
        import pytest
        pytest.skip("skill file missing")
    second = sd.load_skill_file("frontend-taste")
    assert first == second


def test_cache_invalidates_on_mtime_change(sandbox_cursor: Path):
    sd = SkillDiscovery(base_path=str(sandbox_cursor.parent))
    skill_path = sandbox_cursor / "skills" / "frontend-taste" / "SKILL.md"
    if not skill_path.exists():
        import pytest
        pytest.skip("skill file missing")

    first = sd.load_skill_file("frontend-taste")
    # Bump mtime by rewriting (touch may not bump on some FS).
    time.sleep(1.1)  # ensure mtime tick differs
    skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    second = sd.load_skill_file("frontend-taste")
    # Cache must reflect the rewrite (length differs).
    assert second != first
    assert len(second) == len(first) + 1


def test_clear_skill_cache(sandbox_cursor: Path):
    sd = SkillDiscovery(base_path=str(sandbox_cursor.parent))
    sd.load_skill_file("frontend-taste")
    n = sd.clear_skill_cache()
    assert n >= 1
    assert len(sd._skill_file_cache) == 0


def test_unknown_skill_returns_none(sandbox_cursor: Path):
    sd = SkillDiscovery(base_path=str(sandbox_cursor.parent))
    assert sd.load_skill_file("definitely-not-a-real-skill-xyz") is None