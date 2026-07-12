"""
Workflow Module — single entry point for the 4-phase pipeline.

Combines Indexer → SkillDiscovery (cache) → ContextBuilder → MemoryStore
so callers get one function: `workflow.ask(request)` returns a
token-budgeted context plus auto-persisted memory.

Usage:
    >>> from cursor_framework import Workflow
    >>> wf = Workflow(root=".cursor", memory_path=".cache/memory.json")
    >>> result = wf.ask("redesign landing page for our SaaS")
    >>> print(result.context.tokens, result.from_cache)

Design:
    - Workflow is a thin orchestrator. All real logic lives in the 4 modules.
    - State survives across Python sessions via MemoryStore.
    - First call after restart: scans .cursor/, builds full context.
    - Subsequent calls (same request key): may hit memory cache.

This is the only class an agent should need to import for normal work.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from pathlib import Path

from .context_builder import ContextBuilder, ContextResult
from .indexer import Indexer
from .memory_manager import MemoryManager, MemoryTier
from .memory_store import MemoryStore


@dataclass
class WorkflowResult:
    """One Workflow.ask() response — everything the caller might want."""

    context: ContextResult
    from_cache: bool
    memory_hits: int
    memory_misses: int
    asset_count: int
    latency_ms: float = 0.0


class Workflow:
    """
    High-level pipeline: scan → detect → build → cache.

    One Workflow instance per project. Reuse across many ask() calls —
    the cache (skill files + memory) accumulates.
    """

    def __init__(
        self,
        root: str | Path = ".cursor",
        memory_path: str | Path = ".cache/memory.json",
        max_tokens: int = 4000,
        max_skills: int = 5,
        auto_watch: bool = False,
        watch_interval: float = 5.0,
    ) -> None:
        self.root = Path(root).resolve()
        self.memory_path = Path(memory_path)
        self.max_skills = max_skills
        self.builder = ContextBuilder(root=self.root, max_tokens=max_tokens)
        self.memory = MemoryManager()
        self.store = MemoryStore(self.memory_path)

        # Load persisted memory from previous sessions, if any.
        restored = self.store.load_into(self.memory)
        self._restored_entries = restored

        # Lazy asset index — built once, reused.
        self._index: Indexer | None = None

        # Optional auto-watcher: re-index on file change so INDEX.json stays
        # fresh without manual scan. Lazy import avoids a hard dep at
        # module-load time and keeps Workflow usable without watcher.
        self._watcher = None
        if auto_watch:
            from .watcher import Watcher
            self._watcher = Watcher(
                self.root,
                on_change=self._on_watch_change,
                interval=watch_interval,
            )
            self._watcher.take_snapshot()  # baseline before start
            self._watcher.start()

    def _ensure_index(self) -> Indexer:
        if self._index is None:
            idx = Indexer(self.root)
            idx.scan()
            self._index = idx
        return self._index

    @staticmethod
    def _request_key(request: str) -> str:
        """Stable hash for cache lookup — same request → same key."""
        return "request:" + hashlib.md5(request.encode("utf-8")).hexdigest()

    def ask(self, request: str) -> WorkflowResult:
        """
        Process a user request and return budgeted context.

        Flow:
            1. Compute request hash key
            2. Check memory cache → if fresh HIT with valid ContextResult,
               return cached value
            3. Otherwise: ensure index, build context via ContextBuilder
            4. Store context in memory (HOT tier, 1h TTL)
            5. Persist memory to disk

        Note on `from_cache`:
            True only when the cached value round-trips as a real
            ContextResult (in-process case). After process restart the
            JSON-serialized dataclass comes back as a plain dict, so
            Workflow gracefully rebuilds — `from_cache=False` but
            `memory_hits` still increments (the key lookup hit).
        """
        # ponytail: time the full ask() call so callers can surface
        # cache-hit vs cache-miss latency in dashboards / benchmarks.
        started = time.perf_counter()

        idx = self._ensure_index()
        key = self._request_key(request)

        cached = self.memory.retrieve(key)
        if cached is not None and isinstance(cached, ContextResult):
            # ponytail: persist memory on cache hit too — process crash
            # between hits should not lose stats or HOT-tier entries.
            # Cheap (~few KB JSON) so we don't gate it behind a flag.
            self.store.save(self.memory)
            return WorkflowResult(
                context=cached,
                from_cache=True,
                memory_hits=self.memory._hits,
                memory_misses=self.memory._misses,
                asset_count=idx.result.totals.get("grand_total", 0),
                latency_ms=(time.perf_counter() - started) * 1000,
            )
        # ponytail: cached value may be a plain dict after JSON round-trip
        # (dataclass loses its type through json). Fall back to rebuild.
        if cached is not None:
            self.memory.delete(key)

        # Cache miss — build fresh
        context = self.builder.build(request, max_skills=self.max_skills)

        # Store in HOT tier so rapid follow-ups hit cache
        self.memory.store(key, context, tier=MemoryTier.HOT, priority=8)

        # Persist after every successful build so we never lose state
        self.store.save(self.memory)

        return WorkflowResult(
            context=context,
            from_cache=False,
            memory_hits=self.memory._hits,
            memory_misses=self.memory._misses,
            asset_count=idx.result.totals.get("grand_total", 0),
            latency_ms=(time.perf_counter() - started) * 1000,
        )

    def stats(self) -> dict[str, int]:
        """Aggregate stats from all subsystems — useful for dashboard."""
        return {
            "restored_entries": self._restored_entries,
            "memory_entries": sum(len(t) for t in self.memory._storage.values()),
            "memory_hits": self.memory._hits,
            "memory_misses": self.memory._misses,
            "tokens_saved": self.memory._total_tokens_saved,
            "assets_indexed": (
                self._index.result.totals.get("grand_total", 0)
                if self._index else 0
            ),
            "cache_files": len(self.builder.discovery._skill_file_cache),
            "watcher_scans": (
                self._watcher.stats["scans_run"] if self._watcher else 0
            ),
            "watcher_changes": (
                self._watcher.stats["changes_detected"] if self._watcher else 0
            ),
        }

    def _on_watch_change(self, paths: list) -> None:
        """Watcher callback: invalidate index so next ask() rebuilds it."""
        # ponytail: don't scan inside the watcher thread — let the next
        # ask() do it on the main thread (avoid concurrency bugs in
        # Indexer.scan() which mutates self.result).
        self._index = None

    def stop_watching(self) -> None:
        """Stop the background auto-watcher if running."""
        if self._watcher is not None:
            self._watcher.stop()
            self._watcher = None

    def warm(self) -> dict[str, int]:
        """
        Force a full warm-up: ensure index, save state, return stats.
        Useful at startup to surface asset count without making a request.
        """
        idx = self._ensure_index()
        self.store.save(self.memory)
        return self.stats()