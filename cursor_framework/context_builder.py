"""
Context Builder Module

Orchestrates Indexer + SkillDiscovery + TokenOptimizer so callers get a
single function: "given a request, give me a token-budgeted context of the
right skills."

Pipeline:
    request → SkillDiscovery.detect_skills() → load skill files (cached)
            → TokenOptimizer.compress() → within budget

Usage:
    >>> from cursor_framework import ContextBuilder
    >>> cb = ContextBuilder(root=".cursor", max_tokens=4000)
    >>> ctx = cb.build("redesign landing page for SaaS")
    >>> print(ctx.tokens, ctx.skill_count, ctx.truncated)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .indexer import Indexer
from .skill_discovery import SkillDiscovery, get_shared_registry
from .token_optimizer import CompressionStrategy, TokenOptimizer


@dataclass
class ContextResult:
    """Output of ContextBuilder.build()."""

    text: str
    tokens: int
    skill_count: int
    truncated: bool
    skills_used: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


class ContextBuilder:
    """Build a token-budgeted context from a user request."""

    def __init__(
        self,
        root: str | Path = ".cursor",
        max_tokens: int = 4000,
        compression_threshold: float = 0.7,
    ) -> None:
        self.root = Path(root).resolve()
        self.optimizer = TokenOptimizer(
            max_tokens=max_tokens,
            compression_threshold=compression_threshold,
        )
        # SkillDiscovery reads via base_path + registry paths like
        # ".cursor/skills/<name>/SKILL.md".
        self.discovery = SkillDiscovery(base_path=str(self.root.parent))
        self._index: Indexer | None = None

    def _ensure_index(self) -> Indexer:
        """Lazy scan — only build the asset index once per ContextBuilder."""
        if self._index is None:
            idx = Indexer(self.root)
            idx.scan()
            self._index = idx
        return self._index

    def build(self, request: str, max_skills: int = 5) -> ContextResult:
        """
        Detect skills, load them, compress to fit budget.

        Args:
            request: User request text
            max_skills: Cap on number of skills to include (default 5)

        Returns:
            ContextResult with compressed text + metadata
        """
        detected = self.discovery.detect_skills(request)
        if not detected:
            return ContextResult(
                text="", tokens=0, skill_count=0,
                truncated=False, skills_used=[], skipped=[],
            )

        picked = [d.skill for d in detected[:max_skills]]
        skipped = [d.skill for d in detected[max_skills:]]

        blocks: list[str] = []
        skills_used: list[str] = []
        for name in picked:
            content = self.discovery.load_skill_file(name)
            if not content:
                skipped.append(name)
                continue
            blocks.append(f"## Skill: {name}\n\n{content}")
            skills_used.append(name)

        joined = "\n\n---\n\n".join(blocks)
        raw_tokens = self.optimizer.estimate_tokens(joined)

        available = self.optimizer.budget.available_for_context
        # ponytail: TokenOptimizer defaults assume 100k budget. For smaller
        # budgets (e.g. 4k) the system+response reserves (8k) overshoot the
        # ceiling. Clamp to max_tokens floor so compression has a positive
        # target and never returns a stub.
        if available <= 0:
            budget = int(self.optimizer.max_tokens * self.optimizer.compression_threshold)
        else:
            budget = int(available * self.optimizer.compression_threshold)
        if raw_tokens <= budget:
            return ContextResult(
                text=joined,
                tokens=raw_tokens,
                skill_count=len(skills_used),
                truncated=False,
                skills_used=skills_used,
                skipped=skipped,
            )

        compressed = self.optimizer.compress(
            joined,
            target_tokens=budget,
            strategy=CompressionStrategy.SEMANTIC_WITH_SUMMARY,
        )
        return ContextResult(
            text=compressed,
            tokens=self.optimizer.estimate_tokens(compressed),
            skill_count=len(skills_used),
            truncated=True,
            skills_used=skills_used,
            skipped=skipped,
        )

    def stats(self) -> dict[str, int]:
        """Quick access to underlying optimizer + compression stats."""
        return {
            "compression_runs": len(self.optimizer._compression_history),
            "available_tokens": self.optimizer.available_for_context,
            "budget_ratio": self.optimizer.budget.usage_ratio,
        }