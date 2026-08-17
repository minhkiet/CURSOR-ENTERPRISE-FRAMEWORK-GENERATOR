"""Token & memory optimizer.

Runs housekeeping on the cache layer:
  - Evict expired entries
  - Evict items idle longer than a configured threshold
  - Compact caches to a target fill ratio
  - Report savings (tokens freed, items dropped, hit rate)

The optimizer is invoked by `optimize_framework` MCP tool. It is intentionally
pure — it operates on whatever caches the `Loader` exposes.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from .cache import LRUCache
from .loader import Loader


@dataclass
class OptimizationReport:
    expired_evicted: int
    idle_evicted: int
    compacted: int
    tokens_before: int
    tokens_after: int
    cache_stats_before: dict
    cache_stats_after: dict
    duration_ms: float

    def to_dict(self) -> dict:
        return {
            "expired_evicted": self.expired_evicted,
            "idle_evicted": self.idle_evicted,
            "compacted": self.compacted,
            "tokens_before": self.tokens_before,
            "tokens_after": self.tokens_after,
            "tokens_freed": self.tokens_before - self.tokens_after,
            "cache_stats_before": self.cache_stats_before,
            "cache_stats_after": self.cache_stats_after,
            "duration_ms": round(self.duration_ms, 2),
        }


class Optimizer:
    """Tune caches for memory + token budget."""

    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    # ------------------------------------------------------------------ public

    def optimize(
        self,
        idle_threshold_seconds: float = 1800.0,
        compact_to_ratio: float = 0.6,
    ) -> OptimizationReport:
        start = time.monotonic()
        before_tokens = self._total_tokens()
        stats_before = {name: cache.stats() for name, cache in self.loader.caches().items()}

        expired_total = 0
        idle_total = 0
        compacted_total = 0
        for cache in self.loader.caches().values():
            expired_total += cache.evict_expired()
            idle_total += cache.evict_idle(idle_threshold_seconds)
            compacted_total += cache.compact(compact_to_ratio)

        after_tokens = self._total_tokens()
        stats_after = {name: cache.stats() for name, cache in self.loader.caches().items()}
        duration_ms = (time.monotonic() - start) * 1000.0
        return OptimizationReport(
            expired_evicted=expired_total,
            idle_evicted=idle_total,
            compacted=compacted_total,
            tokens_before=before_tokens,
            tokens_after=after_tokens,
            cache_stats_before=stats_before,
            cache_stats_after=stats_after,
            duration_ms=duration_ms,
        )

    def total_tokens(self) -> int:
        return self._total_tokens()

    def cache_stats(self) -> dict[str, dict]:
        return {name: cache.stats() for name, cache in self.loader.caches().items()}

    def snapshot(self) -> dict[str, list[dict]]:
        return {name: cache.snapshot() for name, cache in self.loader.caches().items()}

    # ------------------------------------------------------------------ helpers

    def _total_tokens(self) -> int:
        total = 0
        for cache in self.loader.caches().values():
            total += sum(e.tokens for _, e in cache.items())
        return total
