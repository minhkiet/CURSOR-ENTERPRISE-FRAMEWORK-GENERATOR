"""Task analyzer — auto-detect relevant rules/skills/agents from a free-form request.

Scoring:
  - For each skill, count how many of its (curated) triggers match the request.
  - For each rule, the same against the registry's `triggers` list.
  - Confidence = matches / max(matches, 3) clamped to [0, 1], with bonus for
    mandatory-overlay skills (karpathy/ponytail/full-output) on coding tasks.

Outputs ranked suggestions and a `primary` pick when confidence >= 0.75.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .loader import Loader
from .registry import DOMAIN_TRIGGERS, ESSENTIAL_SKILLS, SKILL_DOMAINS, AGENT_DOMAINS

_TOKEN_RE = re.compile(r"[a-z][a-z0-9-]{2,}", re.IGNORECASE)
_DOMAIN_BONUS: dict[str, float] = {
    "frontend": 0.10,
    "backend": 0.10,
    "database": 0.10,
    "security": 0.15,
    "payment": 0.15,
    "performance": 0.10,
    "design": 0.05,
    "ai": 0.05,
    "infra": 0.05,
    "writing": 0.05,
    "documentation": 0.05,
    "video": 0.10,
    "scraping": 0.10,
    "cloning": 0.10,
}

_CODING_HINTS = {"code", "function", "class", "implement", "build", "fix", "refactor", "debug", "add", "create", "update"}


@dataclass
class Suggestion:
    id: str
    kind: str  # "rule" | "skill" | "agent"
    confidence: float
    domains: list[str]
    reason: str
    path: str


@dataclass
class AnalysisResult:
    request: str
    detected_language: str
    detected_domains: list[str]
    is_coding_task: bool
    suggestions: list[Suggestion]
    primary: Suggestion | None
    essential_skills: list[Suggestion]


class TaskAnalyzer:
    """Score a request against the registry."""

    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    # ------------------------------------------------------------------ public

    def analyze(self, request: str, top_k: int = 8) -> AnalysisResult:
        request_norm = request.strip()
        lower = request_norm.lower()
        tokens = set(_TOKEN_RE.findall(lower))

        detected_domains = self._detect_domains(tokens, lower)
        is_coding = any(h in tokens for h in _CODING_HINTS) or "implement" in lower or "build a" in lower

        suggestions: list[Suggestion] = []

        # Skills
        for item_id, item in self.loader.registry.skills.items():
            conf, reason = self._score_skill(item.id, tokens, lower, detected_domains, is_coding)
            if conf > 0:
                suggestions.append(
                    Suggestion(
                        id=item.id,
                        kind="skill",
                        confidence=round(conf, 3),
                        domains=item.domains,
                        reason=reason,
                        path=item.path,
                    )
                )

        # Rules
        for item_id, item in self.loader.registry.rules.items():
            conf, reason = self._score_rule(item, tokens, lower, detected_domains, is_coding)
            if conf > 0:
                suggestions.append(
                    Suggestion(
                        id=item.id,
                        kind="rule",
                        confidence=round(conf, 3),
                        domains=item.domains,
                        reason=reason,
                        path=item.path,
                    )
                )

        # Agents
        for item_id, item in self.loader.registry.agents.items():
            conf, reason = self._score_agent(item, tokens, lower, detected_domains)
            if conf > 0:
                suggestions.append(
                    Suggestion(
                        id=item.id,
                        kind="agent",
                        confidence=round(conf, 3),
                        domains=item.domains,
                        reason=reason,
                        path=item.path,
                    )
                )

        suggestions.sort(key=lambda s: (-s.confidence, s.id))
        top = suggestions[:top_k]

        primary = top[0] if top and top[0].confidence >= 0.75 else None

        essential = self._essential_suggestions()

        return AnalysisResult(
            request=request_norm,
            detected_language=self._detect_language(lower),
            detected_domains=detected_domains,
            is_coding_task=is_coding,
            suggestions=top,
            primary=primary,
            essential_skills=essential,
        )

    # ------------------------------------------------------------------ scoring

    def _score_skill(
        self,
        skill_id: str,
        tokens: set[str],
        lower: str,
        domains: list[str],
        is_coding: bool,
    ) -> tuple[float, str]:
        skill_domains = SKILL_DOMAINS.get(skill_id, [])
        # Triggers = curated domain keywords that fit this skill
        trigger_set: set[str] = set()
        for d in skill_domains:
            trigger_set.update(DOMAIN_TRIGGERS.get(d, []))
        # Match request tokens against triggers
        matches = sum(1 for t in trigger_set if t in lower or t.replace(" ", "-") in lower)
        # Also count id hits
        if skill_id in lower:
            matches += 3
        # Domain alignment
        domain_overlap = set(domains) & set(skill_domains)
        base = min(1.0, matches / 3.0) if matches else 0.0
        bonus = sum(_DOMAIN_BONUS.get(d, 0) for d in domain_overlap)
        # Mandatory overlay skills always get a floor on coding tasks
        if skill_id in ESSENTIAL_SKILLS and is_coding:
            base = max(base, 0.85)
        conf = min(1.0, base + bonus)
        reason_bits: list[str] = []
        if matches:
            reason_bits.append(f"{matches} trigger hits")
        if domain_overlap:
            reason_bits.append(f"domains: {', '.join(sorted(domain_overlap))}")
        if skill_id in ESSENTIAL_SKILLS and is_coding:
            reason_bits.append("essential overlay")
        return (conf, "; ".join(reason_bits) or "no signal")

    def _score_rule(
        self,
        item,
        tokens: set[str],
        lower: str,
        domains: list[str],
        is_coding: bool,
    ) -> tuple[float, str]:
        triggers = {t.lower() for t in item.triggers}
        matches = sum(1 for t in triggers if t in lower)
        base = min(1.0, matches / 4.0) if matches else 0.0
        if item.id in lower:
            base = max(base, 0.9)
        # Domain alignment
        domain_overlap = set(domains) & set(item.domains)
        bonus = sum(_DOMAIN_BONUS.get(d, 0) for d in domain_overlap) * 0.5
        conf = min(1.0, base + bonus)
        reason_bits = []
        if matches:
            reason_bits.append(f"{matches} tag hits")
        if domain_overlap:
            reason_bits.append(f"domains: {', '.join(sorted(domain_overlap))}")
        return (conf, "; ".join(reason_bits) or "low signal")

    def _score_agent(
        self,
        item,
        tokens: set[str],
        lower: str,
        domains: list[str],
    ) -> tuple[float, str]:
        # Agents fire on review-style verbs
        review_hints = {"review", "audit", "refactor", "debug", "design", "architect", "test", "document", "deploy", "scrape", "clone"}
        if not any(h in lower for h in review_hints):
            return (0.0, "no review verb")
        agent_domains = AGENT_DOMAINS.get(item.id, item.domains)
        overlap = set(domains) & set(agent_domains)
        base = 0.5 if any(h in item.id for h in lower.split()) else 0.4
        if item.id in lower or item.id.replace("-", " ") in lower:
            base = max(base, 0.85)
        bonus = sum(_DOMAIN_BONUS.get(d, 0) for d in overlap) * 0.5
        conf = min(1.0, base + bonus)
        return (conf, f"review verb + domain overlap {sorted(overlap)}")

    # ------------------------------------------------------------------ helpers

    def _detect_domains(self, tokens: set[str], lower: str) -> list[str]:
        detected: list[str] = []
        for domain, kws in DOMAIN_TRIGGERS.items():
            for kw in kws:
                if kw in lower:
                    detected.append(domain)
                    break
        # Deduplicate preserve order
        return list(dict.fromkeys(detected))

    def _detect_language(self, lower: str) -> str:
        # Heuristic only; real translation lives in proto_multi-language-vibe-code.
        for word, lang in (("the", "en"), ("và", "vi"), ("的", "zh"), ("です", "ja"), ("은", "ko")):
            if word in lower:
                return lang
        return "en"

    def _essential_suggestions(self) -> list[Suggestion]:
        out: list[Suggestion] = []
        for sid in ESSENTIAL_SKILLS:
            item = self.loader.registry.skills.get(sid)
            if item is None:
                continue
            out.append(
                Suggestion(
                    id=sid,
                    kind="skill",
                    confidence=1.0,
                    domains=item.domains,
                    reason="essential overlay",
                    path=item.path,
                )
            )
        return out
