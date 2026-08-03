"""
Memory Manager Module

Implements the Memory First principle for context management.
Prioritizes context from memory before external queries.

Features:
    - Tiered memory architecture (hot, warm, cold)
    - Session context preservation
    - Semantic compression
    - Context invalidation and freshness tracking
    - Cross-reference linking

Usage:
    >>> from cursor_framework import MemoryManager, MemoryTier
    >>> manager = MemoryManager()
    >>> manager.store("project_info", {"name": "myapp"}, tier=MemoryTier.SESSION)
    >>> context = manager.retrieve("project_info")
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import hashlib
import json


class MemoryTier(Enum):
    """Memory tier levels with different retention characteristics."""

    HOT = "hot"  # Session-level, fast access, limited retention
    WARM = "warm"  # Project-level, moderate access speed
    COLD = "cold"  # Long-term storage, slower access


class MemoryEntry:
    """Represents a single memory entry with metadata."""

    def __init__(
        self,
        key: str,
        value: Any,
        tier: MemoryTier,
        ttl_seconds: Optional[int] = None,
        priority: int = 5,
    ):
        self.key = key
        self.value = value
        self.tier = tier
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.access_count = 0
        self.ttl_seconds = ttl_seconds
        self.priority = priority
        self.stale = False
        self.references: list[str] = []
        self.version = 1
        self._hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute hash for deduplication."""
        content = json.dumps(self.value, sort_keys=True, default=str)
        return hashlib.md5(content.encode()).hexdigest()

    @property
    def is_expired(self) -> bool:
        """Check if entry has expired based on TTL."""
        if self.ttl_seconds is None:
            return False
        age = datetime.now() - self.created_at
        return age.total_seconds() > self.ttl_seconds

    @property
    def is_fresh(self) -> bool:
        """Check if entry is still fresh (not stale and not expired)."""
        return not self.stale and not self.is_expired

    def access(self) -> Any:
        """Record access and return value."""
        self.last_accessed = datetime.now()
        self.access_count += 1
        return self.value

    def mark_stale(self):
        """Mark entry as stale."""
        self.stale = True

    def add_reference(self, key: str):
        """Add a cross-reference to another entry."""
        if key not in self.references:
            self.references.append(key)

    def update(self, value: Any):
        """Update entry value and increment version."""
        self.value = value
        self.version += 1
        self._hash = self._compute_hash()
        self.stale = False


@dataclass
class MemoryStats:
    """Statistics about memory usage."""

    total_entries: int = 0
    entries_by_tier: dict[MemoryTier, int] = field(default_factory=dict)
    hit_rate: float = 0.0
    miss_rate: float = 0.0
    stale_entries: int = 0
    avg_access_count: float = 0.0
    token_savings: int = 0


class MemoryManager:
    """
    Manages hierarchical memory with tiered architecture.

    Implements Memory First principle by prioritizing cached
    context over external queries.
    """

    # Default TTL values per tier (in seconds)
    DEFAULT_TTL = {
        MemoryTier.HOT: 3600,  # 1 hour
        MemoryTier.WARM: 86400,  # 24 hours
        MemoryTier.COLD: 604800,  # 7 days
    }

    # Priority thresholds
    PRIORITY_THRESHOLD_HIGH = 7
    PRIORITY_THRESHOLD_LOW = 3

    def __init__(self, max_entries_per_tier: Optional[dict[MemoryTier, int]] = None):
        """
        Initialize the memory manager.

        Args:
            max_entries_per_tier: Optional limits per tier
        """
        self._storage: dict[MemoryTier, dict[str, MemoryEntry]] = {
            tier: {} for tier in MemoryTier
        }
        self._max_entries = max_entries_per_tier or {
            MemoryTier.HOT: 100,
            MemoryTier.WARM: 500,
            MemoryTier.COLD: 1000,
        }
        self._hits = 0
        self._misses = 0
        self._total_tokens_saved = 0
        # ponytail: persistence dirty flag. `MemoryStore.save_if_dirty` skips
        # the O(entries) JSON write when nothing has been mutated since the
        # last save. Cuts cache-hit disk I/O from ~few-ms to 0.
        self._dirty = False

    def store(
        self,
        key: str,
        value: Any,
        tier: MemoryTier = MemoryTier.WARM,
        ttl_seconds: Optional[int] = None,
        priority: int = 5,
    ) -> MemoryEntry:
        """
        Store a value in memory.

        Args:
            key: Unique identifier for the entry
            value: The value to store
            tier: Memory tier to store in
            ttl_seconds: Optional time-to-live in seconds
            priority: Priority level (1-10)

        Returns:
            The created MemoryEntry
        """
        if ttl_seconds is None:
            ttl_seconds = self.DEFAULT_TTL.get(tier)

        entry = MemoryEntry(
            key=key,
            value=value,
            tier=tier,
            ttl_seconds=ttl_seconds,
            priority=priority,
        )

        self._storage[tier][key] = entry
        self._dirty = True

        if self._should_evict(tier):
            self._evict_low_priority(tier)

        return entry

    def retrieve(self, key: str, tier: Optional[MemoryTier] = None) -> Optional[Any]:
        """
        Retrieve a value from memory.

        Args:
            key: The key to look up
            tier: Optional specific tier to search

        Returns:
            The stored value or None if not found
        """
        if tier is not None:
            return self._retrieve_from_tier(key, tier)

        for search_tier in [MemoryTier.HOT, MemoryTier.WARM, MemoryTier.COLD]:
            value = self._retrieve_from_tier(key, search_tier)
            if value is not None:
                self._hits += 1
                return value

        self._misses += 1
        return None

    def _retrieve_from_tier(self, key: str, tier: MemoryTier) -> Optional[Any]:
        """Retrieve from a specific tier."""
        entry = self._storage[tier].get(key)
        if entry is None:
            return None

        if entry.is_expired:
            self.delete(key, tier)
            self._misses += 1
            return None

        return entry.access()

    def delete(self, key: str, tier: Optional[MemoryTier] = None):
        """
        Delete an entry from memory.

        Args:
            key: The key to delete
            tier: Optional specific tier, or all tiers if None
        """
        deleted = False
        if tier is not None:
            if self._storage[tier].pop(key, None) is not None:
                deleted = True
        else:
            for t in MemoryTier:
                if self._storage[t].pop(key, None) is not None:
                    deleted = True
        if deleted:
            self._dirty = True

    def invalidate(self, key: str, tier: Optional[MemoryTier] = None):
        """
        Mark an entry as stale without deleting.

        Args:
            key: The key to invalidate
            tier: Optional specific tier
        """
        changed = False
        if tier is not None:
            entry = self._storage[tier].get(key)
            if entry and not entry.stale:
                entry.mark_stale()
                changed = True
        else:
            for t in MemoryTier:
                entry = self._storage[t].get(key)
                if entry and not entry.stale:
                    entry.mark_stale()
                    changed = True
        if changed:
            self._dirty = True

    def link_entries(self, key1: str, key2: str):
        """
        Create cross-reference links between two entries.

        Args:
            key1: First entry key
            key2: Second entry key
        """
        for tier in MemoryTier:
            entry1 = self._storage[tier].get(key1)
            entry2 = self._storage[tier].get(key2)
            if entry1:
                entry1.add_reference(key2)
            if entry2:
                entry2.add_reference(key1)

    def query_by_pattern(self, pattern: str, tier: Optional[MemoryTier] = None) -> dict[str, Any]:
        """
        Query entries by key pattern.

        Args:
            pattern: Pattern to match (supports * wildcard)
            tier: Optional specific tier to search

        Returns:
            Dictionary of matching key-value pairs
        """
        results = {}
        search_tiers = [tier] if tier else list(MemoryTier)

        for t in search_tiers:
            for key, entry in self._storage[t].items():
                if self._matches_pattern(key, pattern):
                    if entry.is_fresh:
                        results[key] = entry.value

        return results

    def _matches_pattern(self, key: str, pattern: str) -> bool:
        """Check if key matches pattern."""
        if "*" in pattern:
            import fnmatch
            return fnmatch.fnmatch(key, pattern)
        return pattern in key

    def get_related(self, key: str) -> list[Any]:
        """
        Get all entries related to a given key.

        Args:
            key: The key to find relations for

        Returns:
            List of related values
        """
        for tier in MemoryTier:
            entry = self._storage[tier].get(key)
            if entry:
                return [self.retrieve(ref) for ref in entry.references if self.retrieve(ref)]
        return []

    def get_stats(self) -> MemoryStats:
        """Get memory statistics."""
        stats = MemoryStats()
        stats.total_entries = sum(len(tier) for tier in self._storage.values())
        stats.entries_by_tier = {tier: len(self._storage[tier]) for tier in MemoryTier}

        total_requests = self._hits + self._misses
        if total_requests > 0:
            stats.hit_rate = self._hits / total_requests
            stats.miss_rate = self._misses / total_requests

        all_entries = [e for tier in self._storage.values() for e in tier.values()]
        stats.stale_entries = sum(1 for e in all_entries if e.stale)

        if all_entries:
            stats.avg_access_count = sum(e.access_count for e in all_entries) / len(all_entries)

        stats.token_savings = self._total_tokens_saved
        return stats

    def cleanup_expired(self):
        """Remove all expired entries."""
        for tier in MemoryTier:
            expired_keys = [
                key for key, entry in self._storage[tier].items()
                if entry.is_expired
            ]
            for key in expired_keys:
                del self._storage[tier][key]

    def optimize(self):
        """Optimize memory by cleaning up and compressing."""
        self.cleanup_expired()
        for tier in MemoryTier:
            self._evict_low_priority(tier, keep_ratio=0.8)

    def _should_evict(self, tier: MemoryTier) -> bool:
        """Check if eviction is needed for a tier."""
        return len(self._storage[tier]) >= self._max_entries[tier]

    def _evict_low_priority(self, tier: MemoryTier, keep_ratio: float = 1.0):
        """Evict low priority entries when needed."""
        entries = list(self._storage[tier].values())
        entries.sort(key=lambda e: (e.priority, e.access_count, e.last_accessed))

        keep_count = int(len(entries) * keep_ratio)
        to_evict = entries[:-keep_count] if keep_count > 0 else entries

        for entry in to_evict:
            self._total_tokens_saved += self._estimate_tokens(entry.value)
            del self._storage[tier][entry.key]

    def _estimate_tokens(self, value: Any) -> int:
        """Estimate token count for value compression tracking."""
        try:
            text = json.dumps(value, default=str)
            # Use word-based estimation for accuracy
            words = text.split()
            if len(words) <= 5:
                # Short values: use char-based
                return max(1, len(text) // 4)
            # Longer values: ~0.75 tokens per word
            return max(len(words), int(len(words) * 0.75))
        except:
            return 100

    def store_session_context(
        self, session_id: str, context: dict[str, Any]
    ):
        """
        Store context for a specific session.

        Args:
            session_id: The session identifier
            context: Dictionary of context values
        """
        for key, value in context.items():
            full_key = f"session:{session_id}:{key}"
            self.store(full_key, value, tier=MemoryTier.HOT)

    def retrieve_session_context(
        self, session_id: str, key: str
    ) -> Optional[Any]:
        """
        Retrieve session-specific context.

        Args:
            session_id: The session identifier
            key: The context key

        Returns:
            The stored context value or None
        """
        full_key = f"session:{session_id}:{key}"
        return self.retrieve(full_key, tier=MemoryTier.HOT)

    def clear_session(self, session_id: str):
        """Clear all context for a session."""
        pattern = f"session:{session_id}:*"
        self.delete_by_pattern(pattern)

    def delete_by_pattern(self, pattern: str):
        """Delete all entries matching a pattern."""
        for tier in MemoryTier:
            keys_to_delete = [
                key for key in self._storage[tier]
                if self._matches_pattern(key, pattern)
            ]
            for key in keys_to_delete:
                del self._storage[tier][key]


def create_memory_manager() -> MemoryManager:
    """Factory function to create a configured MemoryManager."""
    return MemoryManager()
