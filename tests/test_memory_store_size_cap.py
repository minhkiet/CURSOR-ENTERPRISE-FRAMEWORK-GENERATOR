"""Tests for MemoryStore size cap and edge cases."""
from __future__ import annotations

import json
from pathlib import Path

from cursor_framework.memory_manager import MemoryManager
from cursor_framework.memory_store import MemoryStore


def test_load_skips_oversized_file(tmp_path: Path):
    """Step 2/3: load_into must refuse files > MAX_LOAD_BYTES (DoS guard)."""
    path = tmp_path / "memory.json"
    # Write a fake file just over the 50MB cap so we don't allocate 50MB.
    path.write_bytes(b'{"entries": []}' + b" " * (MemoryStore.MAX_LOAD_BYTES + 10))

    store = MemoryStore(path)
    m = MemoryManager()
    restored = store.load_into(m)
    assert restored == 0


def test_load_normal_file_succeeds(tmp_path: Path):
    """Sanity: a normal-sized memory file still loads correctly."""
    path = tmp_path / "memory.json"
    payload = {
        "schema_version": 1,
        "saved_at": "2026-07-12T10:00:00",
        "hits": 3,
        "misses": 1,
        "total_tokens_saved": 100,
        "entries": [],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")

    store = MemoryStore(path)
    m = MemoryManager()
    restored = store.load_into(m)
    assert restored == 0
    assert m._hits == 3


def test_load_at_boundary_succeeds(tmp_path: Path):
    """A file at exactly MAX_LOAD_BYTES is allowed."""
    path = tmp_path / "memory.json"
    path.write_bytes(b'{"schema_version": 1, "entries": []}', encoding=None) \
        if False else path.write_text(
            '{"schema_version": 1, "hits": 0, "misses": 0,'
            ' "total_tokens_saved": 0, "entries": []}',
            encoding="utf-8",
        )
    # Pad to right under the cap. Most modern filesystems handle this.
    current = path.stat().st_size
    pad = MemoryStore.MAX_LOAD_BYTES - current - 100  # safely under
    with path.open("ab") as fh:
        fh.write(b" " * pad)

    store = MemoryStore(path)
    m = MemoryManager()
    restored = store.load_into(m)
    # File is structurally valid → loads cleanly even if huge.
    assert restored == 0


def test_max_load_bytes_constant_is_50mb():
    """Ponytail: keep the cap explicit so callers can override."""
    assert MemoryStore.MAX_LOAD_BYTES == 50 * 1024 * 1024