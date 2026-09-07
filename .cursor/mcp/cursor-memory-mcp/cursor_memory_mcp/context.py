"""Context window accounting and automatic pruning."""

from __future__ import annotations

from typing import Any

from cursor_framework_mcp.loader import Loader, estimate_tokens

from .compressor import ContextCompressor
from .history import ConversationHistory
from .memory import MemoryStore


class ContextManager:
    """Combine framework cache, memories, history, and current context stats."""

    def __init__(self, loader: Loader, memory: MemoryStore, history: ConversationHistory, compressor: ContextCompressor) -> None:
        self.loader = loader
        self.memory = memory
        self.history = history
        self.compressor = compressor

    def compact(self, context: str, target_tokens: int, focus: str = "") -> dict[str, Any]:
        return self.compressor.compress(context, target_tokens, focus)

    def stats(self, current_context: str = "") -> dict[str, Any]:
        framework = {
            kind: {"items": cache.stats()["size"], "tokens": cache.stats()["total_tokens"]}
            for kind, cache in self.loader.caches().items()
        }
        memory = self.memory.stats()
        history = self.history.stats()
        current = estimate_tokens(current_context)
        framework_tokens = sum(item["tokens"] for item in framework.values())
        return {
            "current_context_tokens": current,
            "framework_cache": framework,
            "memory": memory,
            "history": history,
            "total_tokens": current + framework_tokens + memory["tokens"] + history["tokens"],
        }

    def prune(self, current_task: str, target_tokens: int) -> dict[str, Any]:
        result = self.memory.prune(current_task, target_tokens)
        cache_removed = 0
        if self.memory.total_tokens() > target_tokens:
            cache_removed = self.loader.clear()
        return {**result, "framework_cache_items_removed": cache_removed}
