"""
Token Optimizer Module

Implements token optimization strategies for LLM interactions.
Reduces token consumption while maintaining context quality.

Features:
    - Token budget management
    - Semantic compression
    - Context window optimization
    - Smart summarization
    - Priority-based context retention
    - TDAM Symbolic Memory integration (Mermaid Canvas)

Usage:
    >>> from cursor_framework import TokenOptimizer, TokenBudget
    >>> optimizer = TokenOptimizer(max_tokens=100000)
    >>> compressed = optimizer.compress(context, target_tokens=8000)
    
    # With TDAM Symbolic Memory:
    >>> from cursor_framework import TokenOptimizer, TDAMIntegration
    >>> optimizer = TokenOptimizer()
    >>> optimizer.set_tdam(tdam)
    >>> result = optimizer.compact_with_mermaid(messages, ratio=0.7)
"""

import json
import logging
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .tdam_integration import TDAMIntegration, OffloadResult, ConversationTurn

from .tdam_integration import OffloadStrategy

logger = logging.getLogger(__name__)


class TokenBudget:
    """Manages token budgets for different operations."""

    def __init__(
        self,
        max_tokens: int = 100000,
        system_reserve: int = 5000,
        response_reserve: int = 3000,
    ):
        """
        Initialize token budget.

        Args:
            max_tokens: Maximum context window size
            system_reserve: Tokens reserved for system prompts
            response_reserve: Tokens reserved for responses
        """
        self.max_tokens = max_tokens
        self.system_reserve = system_reserve
        self.response_reserve = response_reserve
        self._used_tokens = 0
        self._history: list[dict] = []

    @property
    def available_for_context(self) -> int:
        """Calculate available tokens for user context."""
        return self.max_tokens - self.system_reserve - self.response_reserve

    @property
    def current_usage(self) -> int:
        """Get current token usage."""
        return self._used_tokens

    @property
    def usage_ratio(self) -> float:
        """Get ratio of used to max tokens."""
        return self._used_tokens / self.max_tokens if self.max_tokens > 0 else 0

    def allocate(
        self, purpose: str, tokens: int, priority: int = 5
    ) -> bool:
        """
        Attempt to allocate tokens for a purpose.

        Args:
            purpose: Description of the allocation
            tokens: Number of tokens to allocate
            priority: Priority level (1-10)

        Returns:
            True if allocation successful, False otherwise
        """
        if self._used_tokens + tokens > self.available_for_context:
            return False

        self._used_tokens += tokens
        self._history.append({
            "purpose": purpose,
            "tokens": tokens,
            "priority": priority,
            "timestamp": datetime.now(),
        })
        return True

    def release(self, tokens: int):
        """Release allocated tokens."""
        self._used_tokens = max(0, self._used_tokens - tokens)

    def get_usage_breakdown(self) -> dict:
        """Get detailed usage breakdown."""
        breakdown: dict = {}
        for entry in self._history:
            purpose = entry["purpose"]
            if purpose not in breakdown:
                breakdown[purpose] = {"count": 0, "total_tokens": 0}
            breakdown[purpose]["count"] += 1
            breakdown[purpose]["total_tokens"] += entry["tokens"]
        return breakdown


class CompressionStrategy(Enum):
    """Strategies for context compression."""

    SEMANTIC = "semantic"  # Keep meaning, remove redundancy
    STRUCTURAL = "structural"  # Compress structure, keep data
    TEMPORAL = "temporal"  # Summarize based on recency
    SEMANTIC_WITH_SUMMARY = "semantic_with_summary"  # Semantic + generate summary


@dataclass
class CompressionResult:
    """Result of context compression."""

    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    strategy_used: CompressionStrategy
    summary: Optional[str] = None
    removed_items: list[str] = field(default_factory=list)
    preserved_items: list[str] = field(default_factory=list)


@dataclass
class TokenSegment:
    """A segment of tokenized content."""

    content: str
    tokens: int
    priority: int
    category: str
    metadata: dict = field(default_factory=dict)


class TokenOptimizer:
    """
    Optimizes token usage while maintaining context quality.

    Implements various compression strategies and smart
    context management for efficient LLM interactions.
    """

    # Token estimation: GPT models average ~0.75 tokens/word for English.
    # For multilingual support, we use a word-based estimation with
    # language-aware adjustment. This is more accurate than char-based.
    TOKENS_PER_WORD = 0.75

    # Fallback char-based ratio for short texts or mixed content
    TOKENS_PER_CHAR_FALLBACK = 0.25

    # ponytail: frozenset for O(1) char membership in estimate_tokens.
    _SPECIAL_CHARS = frozenset(".,;:!?()[]{}\n")

    # Priority keywords for different content types
    PRIORITY_INDICATORS = {
        "high": frozenset(("critical", "essential", "required", "must", "important", "key")),
        "medium": frozenset(("should", "recommended", "useful", "relevant")),
        "low": frozenset(("optional", "maybe", "possible", "example")),
    }

    def __init__(
        self,
        max_tokens: int = 100000,
        compression_threshold: float = 0.7,
    ):
        """
        Initialize the token optimizer.

        Args:
            max_tokens: Maximum tokens available
            compression_threshold: Ratio at which to trigger compression
        """
        self.max_tokens = max_tokens
        self.compression_threshold = compression_threshold
        self.budget = TokenBudget(max_tokens)
        # ponytail: bounded history prevents unbounded growth on long-running
        # processes. 1000 entries is far above any realistic per-process
        # compression count and keeps memory footprint negligible.
        self._compression_history: deque[CompressionResult] = deque(maxlen=1000)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Uses word-based estimation for accuracy:
        - GPT models average ~0.75 tokens/word for English
        - Multilingual/short text falls back to char-based estimation

        For code content, tokens are estimated higher due to special characters
        and shorter variable names.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        if not text:
            return 0

        # ponytail: single char-scan that counts both whitespace (for
        # word count) and special chars in one pass. Replaces the older
        # text.split() + sum(...) loop pair.
        word_count = 0
        special_count = 0
        in_word = False
        special = self._SPECIAL_CHARS
        for ch in text:
            if ch.isspace():
                if in_word:
                    word_count += 1
                    in_word = False
            else:
                in_word = True
                if ch in special:
                    special_count += 1
        if in_word:
            word_count += 1

        if word_count == 0:
            # Fallback for very short or no-whitespace text
            return max(1, int(len(text) * self.TOKENS_PER_CHAR_FALLBACK))

        # Detect content type for more accurate estimation
        head = text[:500]
        is_code = (
            text.startswith("```")
            or "def " in head
            or "function " in head
            or "const " in head
            or "class " in head
            or "import " in head
        )

        if is_code:
            # Code tends to have shorter "words" but more tokens
            # Estimate ~1.5 tokens per code "word"
            return max(word_count, int(word_count * 1.5))

        # Standard text: ~0.75 tokens per word
        # Add overhead for punctuation and formatting
        base_tokens = word_count * self.TOKENS_PER_WORD
        special_tokens = special_count * 0.1
        return max(word_count, int(base_tokens + special_tokens))

    def compress(
        self,
        context: str | list | dict,
        target_tokens: Optional[int] = None,
        strategy: CompressionStrategy = CompressionStrategy.SEMANTIC,
    ) -> str:
        """
        Compress context to fit within token budget.

        Args:
            context: Context to compress
            target_tokens: Target token count (defaults to available)
            strategy: Compression strategy to use

        Returns:
            Compressed context string
        """
        if isinstance(context, dict):
            context = self._dict_to_text(context)
        elif isinstance(context, list):
            context = self._list_to_text(context)

        original_tokens = self.estimate_tokens(context)

        if target_tokens is None:
            target_tokens = int(self.available_for_context * self.compression_threshold)

        if original_tokens <= target_tokens:
            return context

        compressed = self._apply_compression(context, target_tokens, strategy)
        compressed_tokens = self.estimate_tokens(compressed)

        result = CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / original_tokens,
            strategy_used=strategy,
        )
        self._compression_history.append(result)

        return compressed

    def _apply_compression(
        self, text: str, target_tokens: int, strategy: CompressionStrategy
    ) -> str:
        """Apply the selected compression strategy."""
        if strategy == CompressionStrategy.SEMANTIC:
            return self._semantic_compress(text, target_tokens)
        elif strategy == CompressionStrategy.STRUCTURAL:
            return self._structural_compress(text, target_tokens)
        elif strategy == CompressionStrategy.TEMPORAL:
            return self._temporal_compress(text, target_tokens)
        elif strategy == CompressionStrategy.SEMANTIC_WITH_SUMMARY:
            return self._semantic_with_summary(text, target_tokens)
        return text

    def _semantic_compress(self, text: str, target_tokens: int) -> str:
        """Semantic compression - keep meaning, remove redundancy."""
        lines = text.split("\n")
        segments = self._create_segments(lines)

        segments.sort(key=lambda s: s.priority, reverse=True)

        selected: list[str] = []
        current_tokens = 0

        for segment in segments:
            if current_tokens + segment.tokens <= target_tokens:
                selected.append(segment.content)
                current_tokens += segment.tokens

        return "\n".join(selected)

    def _structural_compress(self, text: str, target_tokens: int) -> str:
        """Structural compression - compress structure while keeping data."""
        lines = text.split("\n")
        compressed_lines: list[str] = []
        current_tokens = 0

        for line in lines:
            line_tokens = self.estimate_tokens(line)
            if current_tokens + line_tokens <= target_tokens:
                compressed_lines.append(self._abbreviate_line(line))
                current_tokens += line_tokens

        return "\n".join(compressed_lines)

    def _temporal_compress(self, text: str, target_tokens: int) -> str:
        """Temporal compression - prioritize recent content."""
        lines = text.split("\n")
        segments = self._create_segments(lines)

        segments.sort(key=lambda s: (-s.priority, -len(s.content)))

        selected: list[str] = []
        current_tokens = 0

        for segment in segments:
            if current_tokens + segment.tokens <= target_tokens:
                selected.append(segment.content)
                current_tokens += segment.tokens

        return "\n".join(selected)

    def _semantic_with_summary(self, text: str, target_tokens: int) -> str:
        """Semantic compression with auto-generated summary."""
        lines = text.split("\n")
        segments = self._create_segments(lines)

        segments.sort(key=lambda s: s.priority, reverse=True)

        summary_tokens = int(target_tokens * 0.15)
        summary_segment = self._generate_summary(segments, summary_tokens)

        remaining_tokens = target_tokens - self.estimate_tokens(summary_segment)
        content_lines: list[str] = []
        current_tokens = 0

        for segment in segments:
            if current_tokens + segment.tokens <= remaining_tokens:
                content_lines.append(segment.content)
                current_tokens += segment.tokens

        return f"{summary_segment}\n\n{''.join(content_lines)}"

    def _create_segments(self, lines: list[str]) -> list[TokenSegment]:
        """Create prioritized segments from text lines."""
        segments = []
        for line in lines:
            if not line.strip():
                continue
            tokens = self.estimate_tokens(line)
            priority = self._calculate_priority(line)
            category = self._categorize_line(line)
            segments.append(TokenSegment(
                content=line,
                tokens=tokens,
                priority=priority,
                category=category,
            ))
        return segments

    def _calculate_priority(self, line: str) -> int:
        """Calculate priority score for a line."""
        line_lower = line.casefold()
        priority = 5

        for level, keywords in self.PRIORITY_INDICATORS.items():
            # ponytail: substring membership check (casefold already applied).
            # frozenset iter is fine here — keywords are short and small.
            if any(kw in line_lower for kw in keywords):
                if level == "high":
                    priority = 9
                elif level == "medium":
                    priority = 6
                else:
                    priority = 3

        if line.startswith("#"):
            priority = 10
        elif line.startswith("```"):
            priority = 7

        return priority

    def _categorize_line(self, line: str) -> str:
        """Categorize a line of text."""
        if line.startswith("#"):
            return "heading"
        elif line.startswith("```"):
            return "code"
        elif line.startswith("-"):
            return "list_item"
        elif re.match(r"^\d+\.", line):
            return "numbered_item"
        elif "@" in line:
            return "reference"
        else:
            return "body"

    def _abbreviate_line(self, line: str) -> str:
        """Abbreviate a line while preserving key information."""
        if len(line) <= 80:
            return line

        if line.startswith("#"):
            return line

        if "=" in line or ":" in line:
            parts = re.split(r"[:=]", line, maxsplit=1)
            if len(parts[1]) <= 60:
                return line
            return f"{parts[0]}: {parts[1][:57]}..."

        if len(line) <= 100:
            return line

        return line[:77] + "..."

    def _generate_summary(self, segments: list[TokenSegment], max_tokens: int) -> str:
        """Generate a summary from segments."""
        summary_parts = ["## Summary"]

        categories = set(s.category for s in segments)

        for category in ["heading", "code", "list_item"]:
            if category in categories:
                cat_segments = [s for s in segments if s.category == category][:3]
                for s in cat_segments:
                    text = s.content[:50] + "..." if len(s.content) > 50 else s.content
                    summary_parts.append(f"- {text}")

        summary = "\n".join(summary_parts)
        if self.estimate_tokens(summary) > max_tokens:
            summary = summary[:max_tokens * 4] + "..."

        return summary

    def _dict_to_text(self, data: dict, indent: int = 0) -> str:
        """Convert dictionary to readable text."""
        lines = []
        prefix = "  " * indent

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._dict_to_text(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}: [{len(value)} items]")
            else:
                lines.append(f"{prefix}{key}: {value}")

        return "\n".join(lines)

    def _list_to_text(self, items: list) -> str:
        """Convert list to readable text."""
        return "\n".join(f"- {item}" for item in items)

    def optimize_context_window(
        self,
        system: str,
        history: list[dict],
        current_prompt: str,
        max_context_tokens: Optional[int] = None,
    ) -> dict:
        """
        Optimize entire context window for LLM interaction.

        Args:
            system: System prompt
            history: Conversation history
            current_prompt: Current user prompt
            max_context_tokens: Maximum tokens for entire context

        Returns:
            Dictionary with optimized components
        """
        if max_context_tokens is None:
            max_context_tokens = self.max_tokens

        system_tokens = self.estimate_tokens(system)
        current_tokens = self.estimate_tokens(current_prompt)
        available = max_context_tokens - system_tokens - current_tokens

        if available <= 0:
            return {
                "system": self.compress(system, max_context_tokens // 3),
                "history": [],
                "current_prompt": current_prompt,
            }

        history_text = self._format_history(history)
        optimized_history = self.compress(
            history_text,
            target_tokens=int(available * 0.9),
            strategy=CompressionStrategy.SEMANTIC_WITH_SUMMARY,
        )

        return {
            "system": system,
            "history": self._parse_history(optimized_history),
            "current_prompt": current_prompt,
        }

    def _format_history(self, history: list[dict]) -> str:
        """Format conversation history as text."""
        lines = []
        for entry in history:
            role = entry.get("role", "user")
            content = entry.get("content", "")
            lines.append(f"## {role.upper()}")
            lines.append(content)
            lines.append("")
        return "\n".join(lines)

    def _parse_history(self, text: str) -> list[dict]:
        """Parse history text back to list of dicts."""
        history = []
        current_role = "user"
        current_content: list[str] = []

        for line in text.split("\n"):
            if line.startswith("## "):
                if current_content:
                    history.append({
                        "role": current_role,
                        "content": "\n".join(current_content),
                    })
                    current_content = []
                current_role = line[3:].strip().lower()
            else:
                current_content.append(line)

        if current_content:
            history.append({
                "role": current_role,
                "content": "\n".join(current_content),
            })

        return history

    def get_compression_stats(self) -> dict:
        """Get compression statistics."""
        if not self._compression_history:
            return {"total_compressions": 0}

        total_original = sum(r.original_tokens for r in self._compression_history)
        total_compressed = sum(r.compressed_tokens for r in self._compression_history)

        return {
            "total_compressions": len(self._compression_history),
            "total_original_tokens": total_original,
            "total_compressed_tokens": total_compressed,
            "avg_compression_ratio": sum(r.compression_ratio for r in self._compression_history) / len(self._compression_history),
            "tokens_saved": total_original - total_compressed,
        }

    @property
    def available_for_context(self) -> int:
        """Get available tokens for context."""
        return self.budget.available_for_context

    # === TDAM Symbolic Memory Integration ===

    def set_tdam(self, tdam: "TDAMIntegration") -> None:
        """
        Attach TDAM integration for symbolic memory compression.

        Args:
            tdam: TDAMIntegration instance
        """
        self._tdam = tdam

    def compact_with_mermaid(
        self,
        session_id: str,
        messages: list[dict],
        ratio: float = 0.7,
        context_window: int = 128000,
    ) -> Optional["OffloadResult"]:
        """
        Compact conversation using TDAM Mermaid Canvas.

        This uses TDAM's offload API to:
        1. Offload verbose tool logs to external storage
        2. Convert state to lightweight Mermaid symbols
        3. Return compressed messages + canvas for traceability

        Args:
            session_id: Session identifier
            messages: Conversation messages (list of dicts with role/content)
            ratio: Target compression ratio (0.0-1.0)
            context_window: Context window size

        Returns:
            OffloadResult with compressed content and canvas
        """
        if not hasattr(self, "_tdam") or self._tdam is None:
            logger.warning("TDAM not configured, using local compression")
            return None

        # Convert dict messages to ConversationTurn
        from .tdam_integration import ConversationTurn

        turns = [
            ConversationTurn(
                role=m.get("role", "user"),
                content=m.get("content", ""),
                tool_name=m.get("tool_name"),
                tool_result=m.get("tool_result"),
            )
            for m in messages
        ]

        result = self._tdam.compact_context(
            session_id, turns, ratio=ratio, context_window=context_window
        )

        if result:
            # Update compression stats
            self._compression_history.append(
                CompressionResult(
                    original_tokens=result.tokens_before,
                    compressed_tokens=result.tokens_after,
                    compression_ratio=result.compression_ratio,
                    strategy_used=CompressionStrategy.SEMANTIC,
                    summary=f"Mermaid compact: {len(messages)} → {len(result.messages)} messages",
                )
            )

        return result

    def build_mermaid_context(
        self,
        session_id: str,
        current_task: str,
        max_tokens: int = 4000,
    ) -> dict[str, Any]:
        """
        Build context with Mermaid canvas for task execution.

        Combines TDAM layered memory recall with Mermaid canvas
        for efficient context window usage.

        Args:
            session_id: Session identifier
            current_task: Current task description
            max_tokens: Maximum tokens for context

        Returns:
            Dict with {persona, memories, canvas, text, tokens}
        """
        if not hasattr(self, "_tdam") or self._tdam is None:
            return {"error": "TDAM not configured"}

        # Get full context from TDAM
        tdam_context = self._tdam.build_context(session_id, current_task, max_tokens)

        # Format as text
        parts: list[str] = []

        # Add persona if available
        if tdam_context.get("persona"):
            parts.append(f"## User Persona\n{tdam_context['persona']}")

        # Add memories
        memories = tdam_context.get("memories", [])
        if memories:
            parts.append(f"## Relevant Memories ({len(memories)})")
            for m in memories[:5]:  # Top 5
                parts.append(f"- {m['content'][:200]}")

        # Add canvas
        canvas = tdam_context.get("canvas", "")
        if canvas:
            parts.append(f"## Task State (Mermaid)\n```mermaid\n{canvas}\n```")

        text = "\n\n".join(parts)
        tokens = self.estimate_tokens(text)

        return {
            "text": text,
            "tokens": tokens,
            "persona": tdam_context.get("persona"),
            "memories": memories,
            "canvas": canvas,
        }

    def should_trigger_offload(self, current_tokens: int) -> bool:
        """
        Check if offload should be triggered based on context usage.

        Args:
            current_tokens: Current token count

        Returns:
            True if offload recommended
        """
        threshold = int(self.max_tokens * self.compression_threshold)
        return current_tokens >= threshold

    def get_symbolic_stats(self) -> dict:
        """
        Get statistics about symbolic memory compression.

        Returns:
            Stats dict with mermaid and tdam metrics
        """
        stats = self.get_compression_stats()

        tdam_stats = {}
        if hasattr(self, "_tdam") and self._tdam is not None:
            tdam_stats = {
                "tdam_available": self._tdam.is_available(),
                "persona_cached": self._tdam._persona_cache is not None,
            }

        return {
            "compression": stats,
            "tdam": tdam_stats,
            "context_window": {
                "max_tokens": self.max_tokens,
                "compression_threshold": self.compression_threshold,
                "available": self.available_for_context,
            },
        }


def create_optimizer(max_tokens: int = 100000) -> TokenOptimizer:
    """Factory function to create a configured TokenOptimizer."""
    return TokenOptimizer(max_tokens=max_tokens)
