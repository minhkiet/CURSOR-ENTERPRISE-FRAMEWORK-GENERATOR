"""Hierarchical memory store with relevance scoring and persistence."""

from __future__ import annotations

import json
import math
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from cursor_framework_mcp.loader import Loader, estimate_tokens

from .compressor import ContextCompressor

MemoryTier = Literal["short", "medium", "long"]


@dataclass
class MemoryItem:
    id: str
    content: str
    tier: MemoryTier
    kind: str = "fact"
    project: str = "default"
    session: str = "default"
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    access_count: int = 0
    tokens: int = 0


class MemoryStore:
    """Thread-safe short-, medium-, and long-term memory store."""

    TIERS = {"short", "medium", "long"}

    def __init__(self, root: str, loader: Loader, token_budget: int = 24_000) -> None:
        self.root = Path(root).resolve()
        self.loader = loader
        self.token_budget = token_budget
        self.compressor = ContextCompressor()
        self._items: dict[str, MemoryItem] = {}
        self._lock = threading.RLock()
        self.disk_path = self.root / ".cache" / "cursor-memory-mcp.json"

    def store(self, content: str, tier: MemoryTier = "short", kind: str = "fact", project: str = "default", session: str = "default", tags: list[str] | None = None) -> MemoryItem:
        if tier not in self.TIERS:
            raise ValueError(f"tier must be one of {sorted(self.TIERS)}")
        if not content.strip():
            raise ValueError("content cannot be empty")
        item = MemoryItem(
            id=uuid.uuid4().hex,
            content=content.strip(),
            tier=tier,
            kind=kind,
            project=project,
            session=session,
            tags=list(dict.fromkeys(tags or [])),
            tokens=estimate_tokens(content),
        )
        with self._lock:
            self._items[item.id] = item
        return item

    def recall(self, task: str, limit: int = 10, project: str | None = None, session: str | None = None) -> list[dict[str, Any]]:
        now = time.time()
        with self._lock:
            candidates = [item for item in self._items.values() if (project is None or item.project == project) and (session is None or item.session == session)]
            scored = [(self._score(item, task, now), item) for item in candidates]
            scored.sort(key=lambda pair: (-pair[0], -pair[1].updated_at))
            result: list[dict[str, Any]] = []
            for score, item in scored[: max(0, limit)]:
                item.access_count += 1
                result.append({**asdict(item), "relevance": round(score, 4)})
            return result

    def prune(self, task: str = "", target_tokens: int | None = None) -> dict[str, Any]:
        budget = target_tokens if target_tokens is not None else self.token_budget
        if budget < 0:
            raise ValueError("target_tokens cannot be negative")
        now = time.time()
        with self._lock:
            before = self.total_tokens()
            if before <= budget:
                return {"removed": [], "tokens_before": before, "tokens_after": before, "saved_tokens": 0}
            ranked = sorted(self._items.values(), key=lambda item: (self._score(item, task, now), item.updated_at))
            removed: list[str] = []
            current = before
            for item in ranked:
                if current <= budget:
                    break
                removed.append(item.id)
                current -= item.tokens
                del self._items[item.id]
            return {"removed": removed, "tokens_before": before, "tokens_after": current, "saved_tokens": before - current}

    def compact_long_term(self, target_tokens_per_item: int = 200) -> dict[str, int]:
        before = self.total_tokens()
        with self._lock:
            for item in self._items.values():
                if item.tier != "long" or item.tokens <= target_tokens_per_item:
                    continue
                result = self.compressor.compress(item.content, target_tokens_per_item)
                item.content = result["text"]
                item.tokens = result["compressed_tokens"]
                item.updated_at = time.time()
        after = self.total_tokens()
        return {"tokens_before": before, "tokens_after": after, "saved_tokens": before - after}

    def export_data(self) -> dict[str, Any]:
        with self._lock:
            return {"version": 1, "token_budget": self.token_budget, "memories": [asdict(item) for item in self._items.values()]}

    def import_data(self, payload: dict[str, Any], merge: bool = True) -> dict[str, int]:
        memories = payload.get("memories")
        if not isinstance(memories, list):
            raise ValueError("payload.memories must be a list")
        imported = 0
        with self._lock:
            if not merge:
                self._items.clear()
            for raw in memories:
                if not isinstance(raw, dict) or not raw.get("content"):
                    continue
                tier = raw.get("tier", "long")
                if tier not in self.TIERS:
                    continue
                item = MemoryItem(
                    id=str(raw.get("id") or uuid.uuid4().hex),
                    content=str(raw["content"]),
                    tier=tier,
                    kind=str(raw.get("kind", "fact")),
                    project=str(raw.get("project", "default")),
                    session=str(raw.get("session", "default")),
                    tags=[str(tag) for tag in raw.get("tags", [])],
                    created_at=float(raw.get("created_at", time.time())),
                    updated_at=float(raw.get("updated_at", time.time())),
                    access_count=int(raw.get("access_count", 0)),
                    tokens=int(raw.get("tokens") or estimate_tokens(str(raw["content"]))),
                )
                self._items[item.id] = item
                imported += 1
        return {"imported": imported, "total": len(self._items)}

    def sync_to_disk(self) -> dict[str, Any]:
        self.disk_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.disk_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.export_data(), ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.disk_path)
        return {"path": str(self.disk_path), "items": len(self._items), "tokens": self.total_tokens()}

    def load_from_disk(self) -> dict[str, int]:
        if not self.disk_path.is_file():
            return {"imported": 0, "total": len(self._items)}
        payload = json.loads(self.disk_path.read_text(encoding="utf-8"))
        return self.import_data(payload, merge=True)

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_tier = {tier: {"items": 0, "tokens": 0} for tier in sorted(self.TIERS)}
            for item in self._items.values():
                by_tier[item.tier]["items"] += 1
                by_tier[item.tier]["tokens"] += item.tokens
            return {"items": len(self._items), "tokens": self.total_tokens(), "token_budget": self.token_budget, "by_tier": by_tier}

    def total_tokens(self) -> int:
        return sum(item.tokens for item in self._items.values())

    @staticmethod
    def _score(item: MemoryItem, task: str, now: float) -> float:
        task_words = set(task.lower().split())
        memory_words = set(item.content.lower().split()) | {tag.lower() for tag in item.tags}
        overlap = len(task_words & memory_words) / max(1, len(task_words))
        age_days = max(0.0, now - item.updated_at) / 86_400
        recency = math.exp(-age_days / {"short": 2, "medium": 30, "long": 180}[item.tier])
        tier_weight = {"short": 1.0, "medium": 0.9, "long": 0.8}[item.tier]
        access_bonus = min(0.1, item.access_count * 0.01)
        return overlap * 0.7 + recency * 0.2 * tier_weight + access_bonus
