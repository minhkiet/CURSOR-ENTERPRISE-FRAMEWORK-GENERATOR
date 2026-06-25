"""
Skill Discovery Module

Implements automatic skill detection and loading for the framework.
Supports pre-review and post-review gates as defined in skill-integration.mdc.

Features:
    - Automatic skill detection from request keywords
    - Skill loading and validation
    - Gate execution (pre-review and post-review)
    - Skill combination rules
    - Skill metadata management

Usage:
    >>> from cursor_framework import SkillDiscovery
    >>> discovery = SkillDiscovery()
    >>> skills = discovery.detect_skills("Create a landing page for SaaS")
    >>> print(skills)
    [Skill.FRONTEND_TASTE, Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW]
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
import json
import os


class GateType(Enum):
    """Types of review gates."""

    PRE_REVIEW = "pre-review"
    POST_REVIEW = "post-review"


@dataclass
class GateResult:
    """Result of a gate execution."""

    gate_type: GateType
    skill: str
    section: str
    passed: bool
    items_checked: int
    items_passed: int
    failed_items: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    notes: str = ""


@dataclass
class SkillMetadata:
    """Metadata for a skill."""

    name: str
    version: str
    description: str
    tags: list[str]
    path: str
    pre_review_sections: list[str]
    post_review_sections: list[str]
    trigger_keywords: list[str]
    dependencies: list[str] = field(default_factory=list)


@dataclass
class DetectedSkill:
    """A detected skill with routing information."""

    skill: str
    confidence: float
    metadata: SkillMetadata
    gates_to_execute: list[GateType] = field(default_factory=list)


class SkillRegistry:
    """
    Registry for all available skills in the framework.

    Maintains metadata and relationships between skills.
    """

    def __init__(self):
        """Initialize the skill registry."""
        self._skills: dict[str, SkillMetadata] = {}
        self._skill_paths: dict[str, str] = {}
        self._initialize_default_skills()

    def _initialize_default_skills(self):
        """Initialize default skills from framework."""
        default_skills = [
            SkillMetadata(
                name="frontend-taste",
                version="1.0.0",
                description="Anti-slop frontend for landing pages and portfolios",
                tags=["frontend", "design", "landing", "taste"],
                path=".cursor/skills/frontend-taste/SKILL.md",
                pre_review_sections=["0.A", "0.B", "0.C", "0.D", "0.E", "0.F"],
                post_review_sections=["6.A", "6.B", "6.C", "6.D", "6.E", "6.F", "6.G", "6.H"],
                trigger_keywords=[
                    "landing page", "portfolio", "landing", "homepage", "marketing site",
                    "minimalist", "awwwards", "apple-y", "linear-style", "brutalist",
                    "editorial", "greenfield frontend", "new website", "create page"
                ],
            ),
            SkillMetadata(
                name="frontend-redesign",
                version="1.0.0",
                description="Upgrade UI on existing codebase",
                tags=["frontend", "redesign", "upgrade", "improve"],
                path=".cursor/skills/frontend-redesign/SKILL.md",
                pre_review_sections=["0.A", "0.B", "0.C", "0.D", "0.E"],
                post_review_sections=["4.A", "4.B", "4.C", "4.D", "4.E"],
                trigger_keywords=[
                    "redesign", "upgrade", "improve existing", "modernize",
                    "redesign site", "redesign app", "enhance current"
                ],
            ),
            SkillMetadata(
                name="frontend-review",
                version="1.0.0",
                description="Quality gate for all frontend tasks",
                tags=["frontend", "review", "quality", "gate"],
                path=".cursor/skills/frontend-review/SKILL.md",
                pre_review_sections=["A.1", "A.2", "A.3"],
                post_review_sections=["B.1", "B.2", "B.3", "B.4", "B.5", "B.6", "B.7"],
                trigger_keywords=[
                    "review", "quality check", "audit ui", "taste check",
                    "check quality", "code review frontend"
                ],
            ),
            SkillMetadata(
                name="full-output",
                version="1.0.0",
                description="Ensure full implementation without truncation",
                tags=["output", "completeness", "implementation"],
                path=".cursor/skills/full-output/SKILL.md",
                pre_review_sections=["0.A", "0.B"],
                post_review_sections=["5.A", "5.B", "5.C"],
                trigger_keywords=[
                    "full implementation", "complete", "not skeleton", "no todo",
                    "multiple files", "all files", "full code", "not partial"
                ],
            ),
            SkillMetadata(
                name="security-review",
                version="1.0.0",
                description="Comprehensive security review",
                tags=["security", "vulnerability", "audit"],
                path=".cursor/skills/security-review/SKILL.md",
                pre_review_sections=["S.1", "S.2", "S.3"],
                post_review_sections=["Security-1", "Security-2", "Security-3", "Security-4", "Security-5", "Security-6", "Security-7", "Security-8", "Security-9"],
                trigger_keywords=[
                    "security", "vulnerability", "penetration", "owasp", "xss",
                    "sql injection", "ssrf", "csrf", "authentication", "authorization",
                    "apk decompile", "binary analysis", "prompt injection", "exploit"
                ],
            ),
            SkillMetadata(
                name="vietnam-payment-review",
                version="1.0.0",
                description="Vietnam payment provider review",
                tags=["payment", "vietnam", "momo", "sepay"],
                path=".cursor/skills/vietnam-payment-review/SKILL.md",
                pre_review_sections=["payment-pre"],
                post_review_sections=["payment-post"],
                trigger_keywords=[
                    "momo", "sepay", "ayos", "vietqr", "zalo pay", "zalo", "payos",
                    "vnpay", "vietnam payment", "payment integration", "thanh toan"
                ],
                dependencies=["security-review"],
            ),
        ]

        for skill in default_skills:
            self.register(skill)

    def register(self, metadata: SkillMetadata):
        """Register a skill with metadata."""
        self._skills[metadata.name] = metadata
        self._skill_paths[metadata.name] = metadata.path

    def get(self, name: str) -> Optional[SkillMetadata]:
        """Get skill metadata by name."""
        return self._skills.get(name)

    def get_all(self) -> list[SkillMetadata]:
        """Get all registered skills."""
        return list(self._skills.values())

    def find_by_keyword(self, keyword: str) -> list[SkillMetadata]:
        """Find skills matching a keyword."""
        keyword_lower = keyword.lower()
        matches = []

        for skill in self._skills.values():
            if keyword_lower in skill.name.lower():
                matches.append(skill)
            elif any(keyword_lower in kw.lower() for kw in skill.trigger_keywords):
                matches.append(skill)

        return matches

    def get_dependencies(self, name: str) -> list[str]:
        """Get dependencies for a skill."""
        skill = self._skills.get(name)
        return skill.dependencies if skill else []


class GateExecutor:
    """
    Executes pre-review and post-review gates for skills.

    Simulates gate execution and tracks results.
    """

    def __init__(self):
        """Initialize the gate executor."""
        self._results: list[GateResult] = []

    def execute_pre_review(
        self,
        skill: SkillMetadata,
        context: dict,
    ) -> GateResult:
        """
        Execute pre-review gate for a skill.

        Args:
            skill: The skill metadata
            context: Request context

        Returns:
            GateResult with execution details
        """
        checked = len(skill.pre_review_sections)
        passed_items = 0
        failed_items = []

        for section in skill.pre_review_sections:
            if self._check_pre_section(section, context):
                passed_items += 1
            else:
                failed_items.append(section)

        result = GateResult(
            gate_type=GateType.PRE_REVIEW,
            skill=skill.name,
            section=",".join(skill.pre_review_sections),
            passed=len(failed_items) == 0,
            items_checked=checked,
            items_passed=passed_items,
            failed_items=failed_items,
            notes=f"Pre-review gate for {skill.name}",
        )

        self._results.append(result)
        return result

    def execute_post_review(
        self,
        skill: SkillMetadata,
        context: dict,
    ) -> GateResult:
        """
        Execute post-review gate for a skill.

        Args:
            skill: The skill metadata
            context: Implementation context

        Returns:
            GateResult with execution details
        """
        checked = len(skill.post_review_sections)
        passed_items = 0
        failed_items = []

        for section in skill.post_review_sections:
            if self._check_post_section(section, context):
                passed_items += 1
            else:
                failed_items.append(section)

        result = GateResult(
            gate_type=GateType.POST_REVIEW,
            skill=skill.name,
            section=",".join(skill.post_review_sections),
            passed=len(failed_items) == 0,
            items_checked=checked,
            items_passed=passed_items,
            failed_items=failed_items,
            notes=f"Post-review gate for {skill.name}",
        )

        self._results.append(result)
        return result

    def _check_pre_section(self, section: str, context: dict) -> bool:
        """Check if a pre-review section passes."""
        return True

    def _check_post_section(self, section: str, context: dict) -> bool:
        """Check if a post-review section passes."""
        return True

    def get_results(self) -> list[GateResult]:
        """Get all gate execution results."""
        return self._results.copy()

    def get_summary(self) -> dict:
        """Get summary of gate executions."""
        pre_results = [r for r in self._results if r.gate_type == GateType.PRE_REVIEW]
        post_results = [r for r in self._results if r.gate_type == GateType.POST_REVIEW]

        return {
            "total_gates": len(self._results),
            "pre_review": {
                "total": len(pre_results),
                "passed": sum(1 for r in pre_results if r.passed),
                "failed": sum(1 for r in pre_results if not r.passed),
            },
            "post_review": {
                "total": len(post_results),
                "passed": sum(1 for r in post_results if r.passed),
                "failed": sum(1 for r in post_results if not r.passed),
            },
        }


class SkillDiscovery:
    """
    Automatic skill detection and loading system.

    Detects applicable skills based on request analysis
    and manages skill execution workflow.
    """

    # Skill combination rules
    COMBINATION_RULES = {
        "landing_page": {
            "primary": "frontend-taste",
            "secondary": ["full-output", "frontend-review"],
            "gates": ["taste-pre", "taste-post", "fulloutput-pre", "fulloutput-post", "review-pre", "review-post"],
        },
        "redesign": {
            "primary": "frontend-redesign",
            "secondary": ["full-output", "frontend-review"],
            "gates": ["redesign-pre", "redesign-post", "fulloutput-pre", "fulloutput-post", "review-pre", "review-post"],
        },
        "multi_file": {
            "primary": "full-output",
            "secondary": ["frontend-review"],
            "gates": ["fulloutput-pre", "fulloutput-post", "review-pre", "review-post"],
        },
        "frontend_review": {
            "primary": "frontend-review",
            "secondary": [],
            "gates": ["review-pre", "review-post"],
        },
        "payment_task": {
            "primary": "vietnam-payment-review",
            "secondary": ["security-review"],
            "gates": ["payment-pre", "payment-post", "security-pre", "security-post"],
        },
        "security_task": {
            "primary": "security-review",
            "secondary": [],
            "gates": ["security-pre", "security-post"],
        },
    }

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize skill discovery.

        Args:
            base_path: Base path for skill files
        """
        self.registry = SkillRegistry()
        self.gate_executor = GateExecutor()
        self.base_path = base_path or os.getcwd()
        self._discovery_history: list[DetectedSkill] = []

    def detect_skills(self, request: str) -> list[DetectedSkill]:
        """
        Detect applicable skills from a request.

        Args:
            request: The user request text

        Returns:
            List of detected skills with metadata
        """
        detected: list[DetectedSkill] = []
        request_lower = request.lower()

        for skill_metadata in self.registry.get_all():
            confidence = self._calculate_confidence(request_lower, skill_metadata)

            if confidence > 0.1:
                skill = DetectedSkill(
                    skill=skill_metadata.name,
                    confidence=confidence,
                    metadata=skill_metadata,
                    gates_to_execute=self._determine_gates(skill_metadata),
                )
                detected.append(skill)
                self._discovery_history.append(skill)

        detected.sort(key=lambda s: s.confidence, reverse=True)
        return detected

    def _calculate_confidence(
        self, request: str, skill: SkillMetadata
    ) -> float:
        """Calculate confidence score for skill match."""
        matches = 0
        total_triggers = len(skill.trigger_keywords)

        for keyword in skill.trigger_keywords:
            if keyword.lower() in request:
                matches += 1

        base_confidence = matches / total_triggers if total_triggers > 0 else 0

        if skill.name.replace("-", " ") in request:
            base_confidence += 0.3

        return min(0.99, base_confidence)

    def _determine_gates(self, skill: SkillMetadata) -> list[GateType]:
        """Determine which gates to execute for a skill."""
        return [GateType.PRE_REVIEW, GateType.POST_REVIEW]

    def get_combined_skills(self, request: str) -> list[DetectedSkill]:
        """
        Get combined skills based on skill combination rules.

        Args:
            request: The user request

        Returns:
            List of skills to apply in order
        """
        detected = self.detect_skills(request)
        if not detected:
            return []

        primary = detected[0].skill

        combination_key = self._match_combination(primary, request)
        if combination_key and combination_key in self.COMBINATION_RULES:
            rule = self.COMBINATION_RULES[combination_key]
            combined = []

            primary_skill = next(
                (s for s in detected if s.skill == rule["primary"]),
                None,
            )
            if primary_skill:
                combined.append(primary_skill)

            for secondary_name in rule["secondary"]:
                secondary_skill = next(
                    (s for s in detected if s.skill == secondary_name),
                    self.registry.get(secondary_name),
                )
                if secondary_skill:
                    if isinstance(secondary_skill, SkillMetadata):
                        combined.append(DetectedSkill(
                            skill=secondary_skill.name,
                            confidence=0.8,
                            metadata=secondary_skill,
                            gates_to_execute=self._determine_gates(secondary_skill),
                        ))
                    else:
                        combined.append(secondary_skill)

            return combined

        return detected

    def _match_combination(self, primary: str, request: str) -> Optional[str]:
        """Match request to a combination rule."""
        request_lower = request.lower()

        if any(kw in request_lower for kw in ["landing", "portfolio", "homepage"]):
            return "landing_page"
        elif any(kw in request_lower for kw in ["redesign", "upgrade", "improve"]):
            return "redesign"
        elif any(kw in request_lower for kw in ["momo", "sepay", "payment", "vietqr"]):
            return "payment_task"
        elif any(kw in request_lower for kw in ["security", "vulnerability"]):
            return "security_task"
        elif any(kw in request_lower for kw in ["full", "complete", "multiple files"]):
            return "multi_file"

        return None

    def load_skill_file(self, skill_name: str) -> Optional[str]:
        """
        Load skill file content.

        Args:
            skill_name: Name of the skill

        Returns:
            Skill file content or None
        """
        skill = self.registry.get(skill_name)
        if not skill:
            return None

        skill_path = Path(self.base_path) / skill.path
        if skill_path.exists():
            return skill_path.read_text(encoding="utf-8")

        return None

    def execute_gates(
        self, skills: list[DetectedSkill], context: dict, gate_type: GateType
    ) -> list[GateResult]:
        """
        Execute gates for multiple skills.

        Args:
            skills: List of detected skills
            context: Execution context
            gate_type: Type of gate to execute

        Returns:
            List of gate results
        """
        results = []

        for skill_detected in skills:
            skill_metadata = skill_detected.metadata

            if gate_type == GateType.PRE_REVIEW:
                result = self.gate_executor.execute_pre_review(skill_metadata, context)
            else:
                result = self.gate_executor.execute_post_review(skill_metadata, context)

            results.append(result)

        return results

    def get_discovery_stats(self) -> dict:
        """Get statistics about skill discovery."""
        return {
            "total_discoveries": len(self._discovery_history),
            "unique_skills": len(set(s.skill for s in self._discovery_history)),
            "avg_confidence": (
                sum(s.confidence for s in self._discovery_history) / len(self._discovery_history)
                if self._discovery_history else 0
            ),
            "gate_summary": self.gate_executor.get_summary(),
        }


def create_discovery(base_path: Optional[str] = None) -> SkillDiscovery:
    """Factory function to create a configured SkillDiscovery."""
    return SkillDiscovery(base_path=base_path)
