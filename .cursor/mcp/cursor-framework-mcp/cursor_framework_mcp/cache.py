"""LRU cache for loaded rules/skills/agents with TTL and per-kind limits.

Keeps the last *N* items per kind, evicts the least-recently-used, and expires
items after a configurable TTL. Token estimates are tracked per entry so the
optimizer can compute memory pressure.

This is intentionally tiny and dependency-free so the MCP server stays cheap
to import.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class CacheEntry(Generic[V]):
    """One cache slot."""

    key: str
    value: V
    tokens: int = 0
    loaded_at: float = 0.0
    last_access: float = 0.0
    hits: int = 0
    metadata: dict = field(default_factory=dict)

    def is_expired(self, ttl_seconds: float, now: float | None = None) -> bool:
        if ttl_seconds <= 0:
            return False
        ts = now if now is not None else time.monotonic()
        return (ts - self.last_access) > ttl_seconds


class LRUCache(Generic[K, V]):
    """Thread-safe LRU cache with TTL and capacity limits.

    Eviction policy:
      - If size > max_items, evict the least-recently-used entry.
      - On every `get` / `has`, expired entries are dropped lazily.

    Stats:
      - hits, misses, evictions, expirations are tracked for `get_framework_status`.
    """

    def __init__(self, max_items: int = 30, ttl_seconds: float = 1800.0, name: str = "cache") -> None:
        self.max_items = max(1, int(max_items))
        self.ttl_seconds = float(ttl_seconds)
        self.name = name
        self._items: "OrderedDict[str, CacheEntry[V]]" = OrderedDict()
        self._lock = threading.RLock()
        # Stats
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    # ------------------------------------------------------------------ basic ops

    def get(self, key: str) -> V | None:
        """Return value for key or None. Updates LRU position + stats."""
        with self._lock:
            entry = self._items.get(key)
            if entry is None:
                self.misses += 1
                return None
            now = time.monotonic()
            if entry.is_expired(self.ttl_seconds, now):
                # Drop expired
                del self._items[key]
                self.expirations += 1
                self.misses += 1
                return None
            entry.last_access = now
            entry.hits += 1
            self._items.move_to_end(key)
            self.hits += 1
            return entry.value

    def has(self, key: str) -> bool:
        with self._lock:
            entry = self._items.get(key)
            if entry is None:
                return False
            if entry.is_expired(self.ttl_seconds):
                del self._items[key]
                self.expirations += 1
                return False
            return True

    def put(self, key: str, value: V, tokens: int = 0, metadata: dict | None = None) -> V:
        """Insert/refresh. Evicts oldest until within capacity."""
        metadata = metadata or {}
        with self._lock:
            now = time.monotonic()
            entry = self._items.get(key)
            if entry is not None:
                entry.value = value
                entry.tokens = tokens
                entry.metadata = metadata
                entry.last_access = now
                entry.loaded_at = now
                entry.hits = 0
                self._items.move_to_end(key)
            else:
                entry = CacheEntry(
                    key=key,
                    value=value,
                    tokens=tokens,
                    loaded_at=now,
                    last_access=now,
                    metadata=metadata,
                )
                self._items[key] = entry
                while len(self._items) > self.max_items:
                    evicted_key, _ = self._items.popitem(last=False)
                    self.evictions += 1
            return value

    def remove(self, key: str) -> bool:
        with self._lock:
            return self._items.pop(key, None) is not None

    def clear(self) -> int:
        with self._lock:
            n = len(self._items)
            self._items.clear()
            return n

    # ------------------------------------------------------------------ iteration

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._items.keys())

    def items(self) -> list[tuple[str, CacheEntry[V]]]:
        with self._lock:
            return [(k, e) for k, e in self._items.items()]

    def snapshot(self) -> list[dict]:
        """Public-friendly view of the cache for status endpoints."""
        with self._lock:
            out: list[dict] = []
            now = time.monotonic()
            for key, entry in self._items.items():
                age = now - entry.loaded_at
                idle = now - entry.last_access
                out.append(
                    {
                        "key": key,
                        "tokens": entry.tokens,
                        "hits": entry.hits,
                        "age_seconds": round(age, 1),
                        "idle_seconds": round(idle, 1),
                        "metadata": entry.metadata,
                    }
                )
            return out

    # ------------------------------------------------------------------ housekeeping

    def evict_expired(self, now: float | None = None) -> int:
        """Drop expired entries; return count removed."""
        with self._lock:
            ts = now if now is not None else time.monotonic()
            victims = [k for k, e in self._items.items() if e.is_expired(self.ttl_seconds, ts)]
            for k in victims:
                del self._items[k]
                self.expirations += 1
            return len(victims)

    def evict_idle(self, max_idle_seconds: float) -> int:
        """Drop entries idle longer than threshold."""
        with self._lock:
            ts = time.monotonic()
            victims = [
                k
                for k, e in self._items.items()
                if (ts - e.last_access) > max_idle_seconds
            ]
            for k in victims:
                del self._items[k]
                self.evictions += 1
            return len(victims)

    def compact(self, target: float = 0.6) -> int:
        """Shrink to `target` of max_items (only if above target)."""
        with self._lock:
            keep = max(1, int(self.max_items * target))
            if len(self._items) <= keep:
                return 0
            # Drop oldest until at target
            to_drop = len(self._items) - keep
            for _ in range(to_drop):
                self._items.popitem(last=False)
                self.evictions += 1
            return to_drop

    # ------------------------------------------------------------------ stats

    def stats(self) -> dict:
        with self._lock:
            total_tokens = sum(e.tokens for e in self._items.values())
            return {
                "name": self.name,
                "size": len(self._items),
                "max_items": self.max_items,
                "ttl_seconds": self.ttl_seconds,
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "expirations": self.expirations,
                "tokens_tracked": total_tokens,
                "hit_rate": (self.hits / (self.hits + self.misses)) if (self.hits + self.misses) else 0.0,
            }
