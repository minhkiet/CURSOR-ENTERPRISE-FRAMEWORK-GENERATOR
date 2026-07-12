"""
Memory Store Module

JSON-backed persistence for `MemoryManager`. Round-trips `MemoryEntry`
objects across Python sessions so cache survives restarts — no more
rebuilding context from scratch on every new process.

Format: nested dict, one file per store. Atomic write via tmp + rename.

Usage:
    >>> from cursor_framework import MemoryManager, MemoryTier, MemoryStore
    >>> m = MemoryManager()
    >>> m.store("user:42", {"name": "Ada"}, tier=MemoryTier.WARM)
    >>> MemoryStore(".cache/memory.json").save(m)
    >>> # later, in a new process:
    >>> m2 = MemoryManager()
    >>> MemoryStore(".cache/memory.json").load_into(m2)
    >>> m2.retrieve("user:42")
    {'name': 'Ada'}

Design note: we serialize entries as plain dicts rather than pickle so the
file is portable across Python versions and inspectable by humans / tools.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .memory_manager import MemoryManager, MemoryEntry, MemoryTier


def _serialize_entry(entry: "MemoryEntry") -> dict[str, Any]:
    """MemoryEntry → plain dict. Datetimes become ISO strings."""
    return {
        "key": entry.key,
        "value": entry.value,
        "tier": entry.tier.value,
        "created_at": entry.created_at.isoformat(),
        "last_accessed": entry.last_accessed.isoformat(),
        "access_count": entry.access_count,
        "ttl_seconds": entry.ttl_seconds,
        "priority": entry.priority,
        "stale": entry.stale,
        "references": list(entry.references),
        "version": entry.version,
    }


def _deserialize_entry(data: dict[str, Any]) -> "MemoryEntry":
    """Plain dict → MemoryEntry. Re-binds datetimes from ISO strings."""
    from .memory_manager import MemoryEntry, MemoryTier

    entry = MemoryEntry(
        key=data["key"],
        value=data["value"],
        tier=MemoryTier(data["tier"]),
        ttl_seconds=data.get("ttl_seconds"),
        priority=data.get("priority", 5),
    )
    entry.created_at = datetime.fromisoformat(data["created_at"])
    entry.last_accessed = datetime.fromisoformat(data["last_accessed"])
    entry.access_count = data.get("access_count", 0)
    entry.stale = data.get("stale", False)
    entry.references = list(data.get("references", []))
    entry.version = data.get("version", 1)
    return entry


class MemoryStore:
    """Persist a `MemoryManager` to a JSON file."""

    SCHEMA_VERSION = 1

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)

    def save(self, manager: "MemoryManager") -> int:
        """
        Write all entries from `manager` to disk. Atomic via tmp + rename.

        Returns the number of entries written.
        """
        payload = {
            "schema_version": self.SCHEMA_VERSION,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "hits": manager._hits,
            "misses": manager._misses,
            "total_tokens_saved": manager._total_tokens_saved,
            "entries": [
                _serialize_entry(entry)
                for tier_dict in manager._storage.values()
                for entry in tier_dict.values()
            ],
        }

        self.path.parent.mkdir(parents=True, exist_ok=True)
        # ponytail: atomic write avoids half-written files on crash.
        fd, tmp_name = tempfile.mkstemp(
            prefix=self.path.name + ".", dir=self.path.parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                # ponytail: default=str mirrors MemoryEntry._compute_hash —
                # matches the same lossy-but-practical convention used by
                # the rest of the framework. set/tuple → repr-style string.
                json.dump(
                    payload, fh,
                    ensure_ascii=False, indent=2,
                    default=str,
                )
            os.replace(tmp_name, self.path)
        except Exception:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise

        return len(payload["entries"])

    def load_into(self, manager: "MemoryManager") -> int:
        """
        Read entries from disk into `manager`.

        Returns the number of entries restored. Missing or corrupt files
        leave `manager` unchanged (no exception thrown).
        """
        if not self.path.exists():
            return 0

        try:
            with self.path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return 0

        if payload.get("schema_version") != self.SCHEMA_VERSION:
            # Future-proofing: refuse unknown schemas rather than silently corrupt.
            return 0

        manager._hits = payload.get("hits", 0)
        manager._misses = payload.get("misses", 0)
        manager._total_tokens_saved = payload.get("total_tokens_saved", 0)

        count = 0
        for raw in payload.get("entries", []):
            try:
                entry = _deserialize_entry(raw)
            except (KeyError, ValueError):
                continue  # skip malformed, keep going
            manager._storage[entry.tier][entry.key] = entry
            count += 1
        return count

    def exists(self) -> bool:
        return self.path.exists()