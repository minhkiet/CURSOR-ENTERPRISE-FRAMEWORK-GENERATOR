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
    
    # With TDAM Integration:
    >>> from cursor_framework import ContextBuilder, TDAMIntegration
    >>> tdam = TDAMIntegration()
    >>> cb = ContextBuilder()
    >>> cb.set_tdam(tdam)
    >>> ctx = cb.build_with_memory("design dashboard", session_id="user-1")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from .indexer import Indexer
from .skill_discovery import SkillDiscovery, get_shared_registry
from .token_optimizer import CompressionStrategy, TokenOptimizer

if TYPE_CHECKING:
    from .tdam_integration import TDAMIntegration, MemoryLayer, MemoryItem

logger = logging.getLogger(__name__)


@dataclass
class ContextResult:
    """Output of ContextBuilder.build()."""

    text: str
    tokens: int
    skill_count: int
    truncated: bool
    skills_used: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    # TDAM integration fields
    memories: list[dict] = field(default_factory=list)
    persona: Optional[str] = None
    canvas: Optional[str] = None


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
        try:
            detected = self.discovery.detect_skills(request)
        except Exception as e:
            logger.warning("Skill detection failed for request: %s", e)
            detected = []

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

    # === TDAM Integration ===

    def set_tdam(self, tdam: "TDAMIntegration") -> None:
        """
        Attach TDAM integration for memory-aware context building.

        Args:
            tdam: TDAMIntegration instance
        """
        self._tdam = tdam
        self.optimizer.set_tdam(tdam)

    def build_with_memory(
        self,
        request: str,
        session_id: str,
        max_skills: int = 5,
        include_persona: bool = True,
        include_memories: bool = True,
    ) -> ContextResult:
        """
        Build context with TDAM memory integration.

        This enhanced build method:
        1. Detects skills from request
        2. Loads relevant skills
        3. Recalls memories from TDAM layers
        4. Optionally includes persona and memories
        5. Compresses to fit budget

        Args:
            request: User request text
            session_id: Session identifier for memory lookup
            max_skills: Maximum skills to include
            include_persona: Include L3 persona
            include_memories: Include L1 atomic memories

        Returns:
            ContextResult with skills + memories + compressed text
        """
        # 1. Get skills (existing logic)
        detected = self.discovery.detect_skills(request)
        if not detected:
            detected = []

        picked = [d.skill for d in detected[:max_skills]]
        skipped = [d.skill for d in detected[max_skills:]]

        # 2. Build blocks from skills
        blocks: list[str] = []
        skills_used: list[str] = []
        for name in picked:
            content = self.discovery.load_skill_file(name)
            if not content:
                skipped.append(name)
                continue
            blocks.append(f"## Skill: {name}\n\n{content}")
            skills_used.append(name)

        # 3. Add TDAM memories if configured
        memories: list[dict] = []
        persona: Optional[str] = None
        canvas: Optional[str] = None

        if hasattr(self, "_tdam") and self._tdam is not None:
            if include_persona:
                persona = self._tdam.get_persona()
                if persona:
                    blocks.append(f"## User Persona\n\n{persona[:500]}...")

            if include_memories:
                items = self._tdam.recall(request, limit=3)
                for item in items:
                    memories.append({
                        "id": item.id,
                        "content": item.content,
                        "layer": item.layer.value,
                        "score": item.score,
                    })
                    blocks.append(f"## Memory: {item.content[:150]}...")

        # 4. Join and compress
        joined = "\n\n---\n\n".join(blocks)
        raw_tokens = self.optimizer.estimate_tokens(joined)

        available = self.optimizer.budget.available_for_context
        if available <= 0:
            budget = int(self.optimizer.max_tokens * self.optimizer.compression_threshold)
        else:
            budget = int(available * self.optimizer.compression_threshold)

        truncated = raw_tokens > budget
        if truncated:
            joined = self.optimizer.compress(
                joined,
                target_tokens=budget,
                strategy=CompressionStrategy.SEMANTIC_WITH_SUMMARY,
            )

        return ContextResult(
            text=joined,
            tokens=self.optimizer.estimate_tokens(joined),
            skill_count=len(skills_used),
            truncated=truncated,
            skills_used=skills_used,
            skipped=skipped,
            memories=memories,
            persona=persona,
            canvas=canvas,
        )

    def recall_memories(self, query: str, limit: int = 5) -> list[dict]:
        """
        Recall memories from TDAM without building full context.

        Args:
            query: Search query
            limit: Maximum memories to return

        Returns:
            List of memory dicts with id, content, layer, score
        """
        if not hasattr(self, "_tdam") or self._tdam is None:
            return []

        items = self._tdam.recall(query, limit=limit)
        return [
            {
                "id": item.id,
                "content": item.content,
                "layer": item.layer.value,
                "score": item.score,
            }
            for item in items
        ]