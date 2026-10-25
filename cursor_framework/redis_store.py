"""
Redis Observability & Distributed Memory Store Module.

Implements Redis observability guidance:
- Metric tracking: memory, clients, throughput (ops/sec), hit ratio, rejected connections
- Incident triage: SLOWLOG GET, MEMORY DOCTOR, CLIENT LIST, INFO
- Distributed caching: Redis-backed store for MemoryManager with automatic TTL
- Zero-crash resilience: graceful degradation when Redis is offline or redis-py is not installed
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .memory_manager import MemoryManager, MemoryEntry, MemoryTier

logger = logging.getLogger(__name__)

# Check if redis-py is installed
try:
    import redis
    from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
    redis = None  # type: ignore[assignment]
    RedisConnectionError = Exception  # type: ignore[misc,assignment]
    RedisTimeoutError = Exception  # type: ignore[misc,assignment]


@dataclass
class RedisMetricSnapshot:
    """Snapshot of Redis observability metrics."""
    timestamp: str
    is_connected: bool
    used_memory_bytes: int = 0
    used_memory_human: str = "0B"
    maxmemory_bytes: int = 0
    maxmemory_human: str = "0B"
    memory_usage_ratio: float = 0.0
    connected_clients: int = 0
    blocked_clients: int = 0
    instantaneous_ops_per_sec: int = 0
    keyspace_hits: int = 0
    keyspace_misses: int = 0
    hit_ratio: float = 0.0
    rejected_connections: int = 0
    rdb_last_save_time: int = 0
    alerts: list[str] = field(default_factory=list)
    raw_info: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "is_connected": self.is_connected,
            "used_memory_human": self.used_memory_human,
            "maxmemory_human": self.maxmemory_human,
            "memory_usage_ratio": round(self.memory_usage_ratio, 4),
            "connected_clients": self.connected_clients,
            "blocked_clients": self.blocked_clients,
            "instantaneous_ops_per_sec": self.instantaneous_ops_per_sec,
            "keyspace_hits": self.keyspace_hits,
            "keyspace_misses": self.keyspace_misses,
            "hit_ratio_percent": round(self.hit_ratio * 100, 2),
            "rejected_connections": self.rejected_connections,
            "alerts": self.alerts,
        }


@dataclass
class SlowlogEntry:
    """Parsed Redis SLOWLOG entry."""
    entry_id: int
    start_time: int
    duration_micros: int
    command: str
    client_ip: Optional[str] = None
    client_name: Optional[str] = None


class RedisObservability:
    """
    Monitors Redis health, metrics, slow commands, and evaluates alert thresholds.
    Adheres strictly to the Redis Observability operational guidelines.
    """

    def __init__(self, redis_url: Optional[str] = None, client: Any = None) -> None:
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self._client = client
        self._connected = False

    @property
    def is_library_available(self) -> bool:
        return HAS_REDIS

    def get_client(self) -> Any:
        """Get or initialize Redis client with defensive timeout."""
        if self._client is not None:
            return self._client

        if not HAS_REDIS:
            return None

        try:
            self._client = redis.Redis.from_url(
                self.redis_url,
                socket_timeout=2.0,
                socket_connect_timeout=2.0,
                decode_responses=True,
            )
            return self._client
        except Exception as exc:
            logger.warning("Failed to initialize Redis client from URL %s: %s", self.redis_url, exc)
            return None

    def ping(self) -> bool:
        """Check if Redis server is reachable."""
        client = self.get_client()
        if client is None:
            return False
        try:
            return bool(client.ping())
        except (RedisConnectionError, RedisTimeoutError, Exception):
            return False

    def collect_metrics(self) -> RedisMetricSnapshot:
        """
        Collect key metrics from INFO command and evaluate incident alert rules:
        - used_memory vs maxmemory (>80% trigger)
        - connected_clients
        - blocked_clients (>0 trigger)
        - instantaneous_ops_per_sec
        - hit_ratio (<80% trigger)
        - rejected_connections (>0 trigger)
        """
        now_str = datetime.now().isoformat()
        client = self.get_client()

        if client is None:
            return RedisMetricSnapshot(
                timestamp=now_str,
                is_connected=False,
                alerts=["Redis client library 'redis' is not installed or client creation failed"],
            )

        try:
            info = client.info()
        except Exception as exc:
            return RedisMetricSnapshot(
                timestamp=now_str,
                is_connected=False,
                alerts=[f"Unable to connect to Redis server ({self.redis_url}): {exc}"],
            )

        used_mem = int(info.get("used_memory", 0))
        used_mem_human = str(info.get("used_memory_human", f"{used_mem}B"))
        max_mem = int(info.get("maxmemory", 0))
        max_mem_human = str(info.get("maxmemory_human", f"{max_mem}B"))

        mem_ratio = (used_mem / max_mem) if max_mem > 0 else 0.0

        clients = int(info.get("connected_clients", 0))
        blocked = int(info.get("blocked_clients", 0))
        ops_sec = int(info.get("instantaneous_ops_per_sec", 0))
        hits = int(info.get("keyspace_hits", 0))
        misses = int(info.get("keyspace_misses", 0))
        hit_ratio = hits / max(1, hits + misses)
        rejected = int(info.get("rejected_connections", 0))
        rdb_save = int(info.get("rdb_last_save_time", 0))

        # Evaluate Alerts
        alerts = []
        if max_mem > 0 and mem_ratio > 0.8:
            alerts.append(f"CRITICAL: Memory pressure at {mem_ratio:.1%} (>80% maxmemory)")
        if (hits + misses) > 50 and hit_ratio < 0.8:
            alerts.append(f"WARNING: Low cache hit ratio {hit_ratio:.1%} (<80%)")
        if rejected > 0:
            alerts.append(f"CRITICAL: Rejected connections detected: {rejected}")
        if blocked > 0:
            alerts.append(f"WARNING: Clients blocked waiting on operations: {blocked}")

        return RedisMetricSnapshot(
            timestamp=now_str,
            is_connected=True,
            used_memory_bytes=used_mem,
            used_memory_human=used_mem_human,
            maxmemory_bytes=max_mem,
            maxmemory_human=max_mem_human,
            memory_usage_ratio=mem_ratio,
            connected_clients=clients,
            blocked_clients=blocked,
            instantaneous_ops_per_sec=ops_sec,
            keyspace_hits=hits,
            keyspace_misses=misses,
            hit_ratio=hit_ratio,
            rejected_connections=rejected,
            rdb_last_save_time=rdb_save,
            alerts=alerts,
            raw_info=info,
        )

    def slowlog_get(self, limit: int = 10) -> list[SlowlogEntry]:
        """Fetch slow queries exceeding execution threshold."""
        client = self.get_client()
        if client is None:
            return []
        try:
            raw_entries = client.slowlog_get(limit)
            parsed: list[SlowlogEntry] = []
            for item in raw_entries:
                cmd = item.get("command", "")
                if isinstance(cmd, (list, tuple)):
                    cmd = " ".join(str(c) for c in cmd)
                parsed.append(
                    SlowlogEntry(
                        entry_id=item.get("id", 0),
                        start_time=item.get("start_time", 0),
                        duration_micros=item.get("duration", 0),
                        command=str(cmd),
                        client_ip=item.get("client_address"),
                        client_name=item.get("client_name"),
                    )
                )
            return parsed
        except Exception as exc:
            logger.warning("Failed to query slowlog: %s", exc)
            return []

    def memory_doctor(self) -> str:
        """Run MEMORY DOCTOR for an automated diagnostics summary."""
        client = self.get_client()
        if client is None:
            return "Redis client not available."
        try:
            return str(client.execute_command("MEMORY", "DOCTOR"))
        except Exception as exc:
            return f"MEMORY DOCTOR unavailable: {exc}"

    def get_client_list(self) -> list[dict[str, Any]]:
        """Fetch active client connections."""
        client = self.get_client()
        if client is None:
            return []
        try:
            return list(client.client_list())
        except Exception as exc:
            logger.warning("Failed to fetch client list: %s", exc)
            return []


class RedisMemoryStore:
    """
    Redis-backed persistence store for `MemoryManager`.
    Stores entries as JSON with TTL per tier, and provides seamless fallback
    to local memory when Redis is absent.
    """

    KEY_PREFIX = "cf:mem"

    # Default TTL in seconds
    TIER_TTL = {
        "hot": 3600,         # 1 hour
        "warm": 86400,       # 24 hours
        "cold": 604800,      # 7 days
        "session": 7200,     # 2 hours
    }

    def __init__(
        self,
        redis_url: Optional[str] = None,
        fallback_json_path: Optional[str] = None,
        observability: Optional[RedisObservability] = None,
    ) -> None:
        self.observability = observability or RedisObservability(redis_url=redis_url)
        self.fallback_json_path = fallback_json_path or ".cache/memory.json"
        self._is_online = False

    def is_connected(self) -> bool:
        """Check if Redis connection is active and responsive."""
        if not self.observability.is_library_available:
            return False
        return self.observability.ping()

    def _make_key(self, tier: str, key: str) -> str:
        return f"{self.KEY_PREFIX}:{tier}:{key}"

    def save(self, manager: "MemoryManager") -> int:
        """Save MemoryManager entries to Redis. Falls back to local JSON if offline."""
        client = self.observability.get_client()
        if client is None or not self.is_connected():
            # Fallback to standard MemoryStore
            from .memory_store import MemoryStore
            logger.info("Redis offline. Saving entries to JSON fallback: %s", self.fallback_json_path)
            return MemoryStore(self.fallback_json_path).save(manager)

        from .memory_store import _serialize_entry

        count = 0
        pipe = client.pipeline()
        for tier, tier_dict in manager._storage.items():
            tier_val = tier.value if hasattr(tier, "value") else str(tier)
            ttl = self.TIER_TTL.get(tier_val, 86400)

            for key, entry in tier_dict.items():
                redis_key = self._make_key(tier_val, key)
                serialized = json.dumps(_serialize_entry(entry), default=str)
                pipe.set(redis_key, serialized, ex=ttl)
                count += 1

        try:
            pipe.execute()
            manager._dirty = False
            return count
        except Exception as exc:
            logger.error("Error saving to Redis, falling back to JSON: %s", exc)
            from .memory_store import MemoryStore
            return MemoryStore(self.fallback_json_path).save(manager)

    def load_into(self, manager: "MemoryManager") -> int:
        """Load entries from Redis into MemoryManager. Falls back to JSON if Redis is offline."""
        client = self.observability.get_client()
        if client is None or not self.is_connected():
            from .memory_store import MemoryStore
            return MemoryStore(self.fallback_json_path).load_into(manager)

        from .memory_store import _deserialize_entry

        try:
            pattern = f"{self.KEY_PREFIX}:*"
            keys = client.keys(pattern)
            if not keys:
                # If Redis is empty, attempt to seed from local JSON
                from .memory_store import MemoryStore
                seeded = MemoryStore(self.fallback_json_path).load_into(manager)
                if seeded > 0:
                    self.save(manager)
                return seeded

            count = 0
            pipe = client.pipeline()
            for k in keys:
                pipe.get(k)
            values = pipe.execute()

            for raw in values:
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                    entry = _deserialize_entry(data)
                    manager._storage[entry.tier][entry.key] = entry
                    count += 1
                except Exception:
                    continue

            return count
        except Exception as exc:
            logger.warning("Error loading from Redis, trying JSON fallback: %s", exc)
            from .memory_store import MemoryStore
            return MemoryStore(self.fallback_json_path).load_into(manager)
