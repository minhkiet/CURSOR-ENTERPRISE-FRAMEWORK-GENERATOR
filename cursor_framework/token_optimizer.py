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

Usage:
    >>> from cursor_framework import TokenOptimizer, TokenBudget
    >>> optimizer = TokenOptimizer(max_tokens=100000)
    >>> compressed = optimizer.compress(context, target_tokens=8000)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
import json
import re


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

    # Average tokens per character ratio (conservative estimate)
    TOKENS_PER_CHAR = 0.25

    # Priority keywords for different content types
    PRIORITY_INDICATORS = {
        "high": ["critical", "essential", "required", "must", "important", "key"],
        "medium": ["should", "recommended", "useful", "relevant"],
        "low": ["optional", "maybe", "possible", "example"],
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
        self._compression_history: list[CompressionResult] = []

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        return int(len(text) * self.TOKENS_PER_CHAR)

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
        line_lower = line.lower()
        priority = 5

        for level, keywords in self.PRIORITY_INDICATORS.items():
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


def create_optimizer(max_tokens: int = 100000) -> TokenOptimizer:
    """Factory function to create a configured TokenOptimizer."""
    return TokenOptimizer(max_tokens=max_tokens)
