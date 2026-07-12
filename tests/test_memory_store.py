"""Tests for cursor_framework.memory_store."""
from __future__ import annotations

from pathlib import Path

import pytest

from cursor_framework.memory_manager import MemoryManager, MemoryTier
from cursor_framework.memory_store import MemoryStore


def test_round_trip_preserves_values(tmp_path: Path):
    store_path = tmp_path / "m.json"
    m1 = MemoryManager()
    m1.store("user:1", {"name": "Ada"}, tier=MemoryTier.WARM)
    m1.store("user:2", {"name": "Bo"}, tier=MemoryTier.COLD)
    m1.store("hot", [1, 2, 3], tier=MemoryTier.HOT)
    MemoryStore(store_path).save(m1)

    m2 = MemoryManager()
    n = MemoryStore(store_path).load_into(m2)
    assert n == 3
    assert m2.retrieve("user:1") == {"name": "Ada"}
    assert m2.retrieve("hot") == [1, 2, 3]


def test_missing_file_returns_zero(tmp_path: Path):
    m = MemoryManager()
    n = MemoryStore(tmp_path / "missing.json").load_into(m)
    assert n == 0


def test_corrupt_file_returns_zero(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text("not json{", encoding="utf-8")
    m = MemoryManager()
    assert MemoryStore(p).load_into(m) == 0


def test_atomic_write_no_tmp_leftovers(tmp_path: Path):
    p = tmp_path / "x.json"
    m = MemoryManager()
    m.store("k", "v", tier=MemoryTier.HOT)
    MemoryStore(p).save(m)
    leftovers = list(tmp_path.glob("x.json.*"))
    assert not leftovers


def test_stats_restored(tmp_path: Path):
    p = tmp_path / "m.json"
    m1 = MemoryManager()
    m1.store("k", "v", tier=MemoryTier.WARM)
    m1._hits = 42
    m1._misses = 7
    MemoryStore(p).save(m1)

    m2 = MemoryManager()
    MemoryStore(p).load_into(m2)
    assert m2._hits == 42
    assert m2._misses == 7


def test_large_value_round_trip(tmp_path: Path):
    p = tmp_path / "m.json"
    big = {"data": "x" * 5000}
    m1 = MemoryManager()
    m1.store("big", big, tier=MemoryTier.WARM)
    MemoryStore(p).save(m1)

    m2 = MemoryManager()
    MemoryStore(p).load_into(m2)
    assert m2.retrieve("big") == big


def test_unknown_schema_refused(tmp_path: Path):
    """Future-proofing: refuse unknown schema versions."""
    import json
    p = tmp_path / "future.json"
    p.write_text(json.dumps({"schema_version": 999, "entries": []}), encoding="utf-8")
    m = MemoryManager()
    assert MemoryStore(p).load_into(m) == 0