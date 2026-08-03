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
    phase_ms: dict[str, float] = field(default_factory=dict)


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
        strict_persist: bool = False,
    ) -> None:
        """
        Args:
            root: Path to the `.cursor` directory.
            memory_path: Path to the persisted JSON memory file.
            max_tokens: Token budget for ContextBuilder.
            max_skills: Cap on skills per request.
            auto_watch: Spawn a background Watcher to invalidate cache
                when files change.
            watch_interval: Watcher poll interval (seconds).
            strict_persist: When True, persist memory after every ask
                (including cache hits). Defaults to False so the hit path
                stays allocation-free. Set to True for tests / CI that
                assert on disk state after a hit.
        """
        self.root = Path(root).resolve()
        self.memory_path = Path(memory_path)
        self.max_skills = max_skills
        self.strict_persist = strict_persist
        self.builder = ContextBuilder(root=self.root, max_tokens=max_tokens)
        self.memory = MemoryManager()
        self.store = MemoryStore(self.memory_path)

        # Load persisted memory from previous sessions, if any.
        restored = self.store.load_into(self.memory)
        self._restored_entries = restored

        # Lazy asset index — built only on cache miss.
        self._index: Indexer | None = None
        # Memoize ETag across calls; invalidated by watcher events.
        self._etag_cache: tuple[str, str] | None = None

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
        """Stable hash for cache lookup."""
        return "request:" + hashlib.md5(request.encode("utf-8")).hexdigest()

    def _compute_etag(self) -> str:
        """
        Compute ETag from skill file mtimes.

        Returns a hash of all skill file modification times.
        Invalidates cache when any skill file changes.

        Ponytail: memoized per (root, mtime_signature). The signature
        collapses all file mtimes into a single string we hash once.
        Watcher events invalidate the cache via `_etag_cache = None`.
        A full scan on every ask() is the prior behaviour — this cuts
        the hot path from O(framework files) to O(1) on cache hit.
        """
        if self._etag_cache is not None:
            return self._etag_cache[0]

        etag_parts: list[str] = []

        # Walk skill directories and collect mtimes
        skill_dirs = [
            self.root / "skills",
            self.root / "rules",
            self.root / "agents",
        ]

        for skill_dir in skill_dirs:
            if not skill_dir.exists():
                continue
            for path in sorted(skill_dir.rglob("*")):
                if path.is_file():
                    try:
                        mtime = path.stat().st_mtime
                        etag_parts.append(f"{path.relative_to(self.root)}:{mtime}")
                    except OSError:
                        pass

        # Also include INDEX.json mtime if exists
        index_path = self.root / "INDEX.json"
        if index_path.exists():
            try:
                mtime = index_path.stat().st_mtime
                etag_parts.append(f"INDEX.json:{mtime}")
            except OSError:
                pass

        # Hash all parts together
        combined = "|".join(sorted(etag_parts))
        etag = hashlib.md5(combined.encode("utf-8")).hexdigest()
        self._etag_cache = (etag, combined)
        return etag

    def invalidate_cache(self, key_pattern: str | None = None) -> int:
        """
        Invalidate cached entries.
        
        Args:
            key_pattern: If provided, only invalidate keys matching this pattern.
                        If None, invalidates all HOT tier entries.
        
        Returns:
            Number of entries invalidated
        """
        if key_pattern:
            # Delete specific keys matching pattern
            deleted = 0
            for tier in MemoryTier:
                keys_to_delete = [
                    k for k in self.memory._storage[tier]
                    if key_pattern in k
                ]
                for k in keys_to_delete:
                    self.memory.delete(k, tier)
                    deleted += 1
            return deleted
        else:
            # Clear all HOT tier (session cache)
            count = len(self.memory._storage[MemoryTier.HOT])
            self.memory._storage[MemoryTier.HOT].clear()
            return count

    def ask(self, request: str) -> WorkflowResult:
        """
        Process a user request and return budgeted context.

        Flow:
            1. Compute request hash key
            2. Check memory cache → if fresh HIT with valid ContextResult and matching ETag,
               return cached value
            3. Otherwise: ensure index, build context via ContextBuilder
            4. Store context in memory (HOT tier, 1h TTL)
            5. Persist memory to disk (only if dirty — hit path may skip)

        Note on `from_cache`:
            True only when the cached value round-trips as a real
            ContextResult (in-process case). After process restart the
            JSON-serialized dataclass comes back as a plain dict, so
            Workflow gracefully rebuilds — `from_cache=False` but
            `memory_hits` still increments (the key lookup hit).

        Note on ETag:
            Cache is invalidated when skill files change (based on mtime).
            The ETag is stored alongside the cached ContextResult.
        """
        # ponytail: time the full ask() call so callers can surface
        # cache-hit vs cache-miss latency in dashboards / benchmarks.
        started = time.perf_counter()
        phase_ms: dict[str, float] = {}

        # Cache hit path: skip Indexer.scan entirely. ETag is memoized
        # so we only walk the framework tree on first call or after
        # watcher invalidation.
        etag_start = time.perf_counter()
        current_etag = self._compute_etag()
        phase_ms["etag_ms"] = (time.perf_counter() - etag_start) * 1000

        # Create cache key with ETag for proper invalidation
        base_key = self._request_key(request)
        cache_key = f"{base_key}:{current_etag}"

        cached = self.memory.retrieve(cache_key)
        if cached is not None and isinstance(cached, ContextResult):
            # ponytail: persist-on-hit is now optional via save_if_dirty.
            # Cache hits don't mutate memory, so the dirty flag stays
            # False and the JSON write is skipped — unless the caller
            # opted into strict_persist.
            if self.strict_persist:
                self.store.save(self.memory)
            else:
                self.store.save_if_dirty(self.memory)
            asset_count = (
                self._index.result.totals.get("grand_total", 0)
                if self._index is not None
                else 0
            )
            phase_ms["total_ms"] = (time.perf_counter() - started) * 1000
            return WorkflowResult(
                context=cached,
                from_cache=True,
                memory_hits=self.memory._hits,
                memory_misses=self.memory._misses,
                asset_count=asset_count,
                latency_ms=(time.perf_counter() - started) * 1000,
                phase_ms=phase_ms,
            )
        # ponytail: cached value may be a plain dict after JSON round-trip
        # (dataclass loses its type through json). Fall back to rebuild.
        # Also check for stale cache (different ETag).
        if cached is not None:
            self.memory.delete(cache_key)

        # Cache miss — build fresh. Indexer.scan only runs here.
        idx_start = time.perf_counter()
        idx = self._ensure_index()
        phase_ms["index_ms"] = (time.perf_counter() - idx_start) * 1000

        build_start = time.perf_counter()
        context = self.builder.build(request, max_skills=self.max_skills)
        phase_ms["build_ms"] = (time.perf_counter() - build_start) * 1000

        # Store in HOT tier so rapid follow-ups hit cache
        # Include ETag in key for proper invalidation
        self.memory.store(cache_key, context, tier=MemoryTier.HOT, priority=8)

        # Persist after every successful build so we never lose state.
        # store() marks the manager dirty, so save_if_dirty does the work.
        self.store.save_if_dirty(self.memory)

        phase_ms["total_ms"] = (time.perf_counter() - started) * 1000
        return WorkflowResult(
            context=context,
            from_cache=False,
            memory_hits=self.memory._hits,
            memory_misses=self.memory._misses,
            asset_count=idx.result.totals.get("grand_total", 0),
            latency_ms=(time.perf_counter() - started) * 1000,
            phase_ms=phase_ms,
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
        """
        Watcher callback: invalidate index so next ask() rebuilds it.

        Also invalidates HOT tier cache so stale skill files don't return
        old cached results.
        """
        # ponytail: don't scan inside the watcher thread — let the next
        # ask() do it on the main thread (avoid concurrency bugs in
        # Indexer.scan() which mutates self.result).
        self._index = None
        # ponytail: also invalidate the memoized ETag so the next ask()
        # walks the framework tree and re-derives a fresh hash.
        self._etag_cache = None

        # Invalidate HOT tier cache so changed files trigger fresh builds
        self.invalidate_cache()  # Clears all HOT tier entries

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