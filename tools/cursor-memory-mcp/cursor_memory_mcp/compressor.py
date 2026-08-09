"""Deterministic token-aware text compression."""

from __future__ import annotations

import re
from typing import Any

from cursor_framework_mcp.loader import estimate_tokens

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")
_WORD_RE = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)
_STOP_WORDS = {"the", "and", "for", "that", "with", "this", "from", "are", "was", "were", "have", "has", "into", "your", "you"}


class ContextCompressor:
    """Extract high-information sentences until a token budget is met."""

    def compress(self, text: str, target_tokens: int, focus: str = "") -> dict[str, Any]:
        if target_tokens < 1:
            raise ValueError("target_tokens must be positive")
        source_tokens = estimate_tokens(text)
        if source_tokens <= target_tokens:
            return {"text": text.strip(), "original_tokens": source_tokens, "compressed_tokens": source_tokens, "saved_tokens": 0}

        focus_words = set(_WORD_RE.findall(focus.lower()))
        sentences = [sentence.strip() for sentence in _SENTENCE_RE.split(text) if sentence.strip()]
        frequencies: dict[str, int] = {}
        for sentence in sentences:
            for word in _WORD_RE.findall(sentence.lower()):
                if word not in _STOP_WORDS and len(word) > 2:
                    frequencies[word] = frequencies.get(word, 0) + 1

        ranked: list[tuple[float, int, str]] = []
        for index, sentence in enumerate(sentences):
            words = set(_WORD_RE.findall(sentence.lower()))
            density = sum(frequencies.get(word, 0) for word in words) / max(1, len(words))
            focus_bonus = len(words & focus_words) * 3
            marker_bonus = 2 if any(marker in sentence.lower() for marker in ("decision", "error", "result", "must", "fixed", "conclusion")) else 0
            ranked.append((density + focus_bonus + marker_bonus, index, sentence))

        chosen: list[tuple[int, str]] = []
        used = 0
        for _, index, sentence in sorted(ranked, key=lambda item: (-item[0], item[1])):
            cost = estimate_tokens(sentence)
            if chosen and used + cost > target_tokens:
                continue
            chosen.append((index, sentence))
            used += cost
            if used >= target_tokens:
                break
        compressed = " ".join(sentence for _, sentence in sorted(chosen))
        compressed_tokens = estimate_tokens(compressed)
        return {
            "text": compressed,
            "original_tokens": source_tokens,
            "compressed_tokens": compressed_tokens,
            "saved_tokens": max(0, source_tokens - compressed_tokens),
        }
