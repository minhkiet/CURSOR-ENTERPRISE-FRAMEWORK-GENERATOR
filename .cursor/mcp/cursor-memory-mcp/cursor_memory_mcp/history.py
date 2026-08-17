"""Conversation history storage and summarization."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Any

from cursor_framework_mcp.loader import estimate_tokens

from .compressor import ContextCompressor


@dataclass
class HistoryMessage:
    role: str
    content: str
    timestamp: float
    tokens: int


class ConversationHistory:
    """In-memory ordered conversation history."""

    def __init__(self, compressor: ContextCompressor) -> None:
        self.compressor = compressor
        self.messages: list[HistoryMessage] = []

    def add(self, role: str, content: str) -> HistoryMessage:
        if role not in {"system", "user", "assistant", "tool"}:
            raise ValueError("invalid conversation role")
        message = HistoryMessage(role, content, time.time(), estimate_tokens(content))
        self.messages.append(message)
        return message

    def summarize(self, keep_recent: int = 8, target_tokens: int = 800) -> dict[str, Any]:
        split_at = max(0, len(self.messages) - max(0, keep_recent))
        old = self.messages[:split_at]
        recent = self.messages[split_at:]
        source = "\n".join(f"{message.role}: {message.content}" for message in old)
        summary = self.compressor.compress(source, target_tokens, focus="decisions conclusions errors results") if source else {"text": "", "original_tokens": 0, "compressed_tokens": 0, "saved_tokens": 0}
        return {"summary": summary, "summarized_messages": len(old), "recent_messages": [asdict(message) for message in recent]}

    def stats(self) -> dict[str, int]:
        return {"messages": len(self.messages), "tokens": sum(message.tokens for message in self.messages)}
