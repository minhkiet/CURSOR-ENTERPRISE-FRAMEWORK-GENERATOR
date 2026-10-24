"""
Cross-Agent Skill Registry

Provides unified skill registration and compatibility management across vibe coding agents:
- Cursor IDE
- Codex (cursor.com)
- Claude Code (@cursor/codex)
- Grok (x.com/grok)

Features:
    - Cross-agent skill compatibility mapping
    - Skill conversion utilities
    - Agent-specific skill overrides
    - Unified skill manifest format

Usage:
    >>> from cursor_framework.skills.skill_registry import CrossAgentSkillRegistry
    >>> registry = CrossAgentSkillRegistry()
    >>> compatible = registry.get_compatible_skills("frontend-taste", agent="claude-code")
    >>> print(f"Compatible: {[s.name for s in compatible]}")
    ['frontend-taste', 'frontend-review', 'full-output']

    >>> # Convert a skill manifest
    >>> manifest = registry.create_manifest("frontend-taste")
    >>> registry.export_manifest(manifest, format="json")
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class AgentType(Enum):
    """Supported vibe coding agents."""
    CURSOR = "cursor"
    CODEX = "codex"
    CLAUDE_CODE = "claude-code"
    GROK = "grok"
    UNIVERSAL = "universal"  # Works on all agents
    UNKNOWN = "unknown"


class GatePrefix(Enum):
    """Gate prefix mapping per agent."""
    CURSOR = "K"
    CODEX = "CX"
    CLAUDE_CODE = "C"
    GROK = "G"
    UNIVERSAL = "U"
    UNKNOWN = "U"


@dataclass
class SkillManifest:
    """Standardized skill manifest for cross-agent compatibility."""
    name: str
    version: str
    compatible_agents: list[str]
    primary_agent: str
    tags: list[str]
    triggers: list[str]
    pre_gates: list[str]
    post_gates: list[str]
    agent_gates: dict[str, list[str]] = field(default_factory=dict)
    path: Optional[str] = None
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "version": self.version,
            "compatible_agents": self.compatible_agents,
            "primary_agent": self.primary_agent,
            "tags": self.tags,
            "triggers": self.triggers,
            "pre_gates": self.pre_gates,
            "post_gates": self.post_gates,
            "agent_gates": self.agent_gates,
            "path": self.path,
            "description": self.description,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SkillManifest":
        """Create from dictionary."""
        return cls(
            name=data.get("name", ""),
            version=data.get("version", "1.0.0"),
            compatible_agents=data.get("compatible_agents", ["universal"]),
            primary_agent=data.get("primary_agent", "cursor"),
            tags=data.get("tags", []),
            triggers=data.get("triggers", []),
            pre_gates=data.get("pre_gates", []),
            post_gates=data.get("post_gates", []),
            agent_gates=data.get("agent_gates", {}),
            path=data.get("path"),
            description=data.get("description", ""),
            dependencies=data.get("dependencies", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )

    def is_compatible(self, agent: str) -> bool:
        """Check if skill is compatible with an agent."""
        if "universal" in self.compatible_agents:
            return True
        return agent in self.compatible_agents

    def get_gate_prefix(self, agent: str) -> str:
        """Get the gate prefix for a specific agent."""
        prefix_map = {
            "cursor": GatePrefix.CURSOR.value,
            "codex": GatePrefix.CODEX.value,
            "claude-code": GatePrefix.CLAUDE_CODE.value,
            "grok": GatePrefix.GROK.value,
            "universal": GatePrefix.UNIVERSAL.value,
        }
        return prefix_map.get(agent, GatePrefix.UNKNOWN.value)


@dataclass
class CrossAgentSkill:
    """A skill with cross-agent compatibility info."""
    manifest: SkillManifest
    confidence: float = 1.0
    compatible_with: list[str] = field(default_factory=list)
    agent_specific: bool = False


class CrossAgentSkillRegistry:
    """
    Unified skill registry for cross-agent compatibility.

    Maintains a registry of skills with agent compatibility metadata,
    and provides utilities for skill conversion and export.

    This registry is synchronized with the TypeScript framework.ts
    to ensure consistent skill definitions across all vibe coding agents.
    """

    # Universal skills that work on all agents
    UNIVERSAL_SKILLS = [
        "karpathy-coding",
        "frontend-taste",
        "frontend-review",
        "full-output",
        "security-review",
        "test-analysis",
        "perf-optimization",
        "stability",
        "data-quality",
        "code-graph-analysis",
        "karpathy",
    ]

    # Agent-specific skill mappings - synchronized with TypeScript framework.ts
    AGENT_SKILL_MAPPINGS: dict[str, list[str]] = {
        "cursor": [
            # Core coding
            "ponytail",
            "karpathy-coding",
            # Frontend
            "frontend-taste",
            "frontend-review",
            "frontend-redesign",
            "hallmark",
            "dashboard-ui",
            "landing-page-pro",
            # Design
            "open-design",
            "visual-explainer",
            "ui-ux-pro-max",
            # Security
            "security-review",
            "vietnam-payment-review",
            # Domain
            "vietnam-address",
            "bazi",
            "document-ocr",
            # AI & RAG
            "weknora-kb",
            "weknora-agent",
            "video-generation",
            "pixelrag",
            "ai-copywriter",
            "simple-english",
            "book-to-skill",
            # Performance
            "code-graph-analysis",
            # Quality
            "test-analysis",
            "perf-optimization",
            "stability",
            "data-quality",
            # Meta
            "skill-installer",
            "full-output",
        ],
        "codex": [
            # Core coding
            "ponytail",
            "karpathy-coding",
            # Frontend
            "frontend-taste",
            "frontend-review",
            "frontend-redesign",
            # Security
            "security-review",
            "vietnam-payment-review",
            # Quality
            "test-analysis",
            "perf-optimization",
            "stability",
            "data-quality",
            # Meta
            "full-output",
        ],
        "claude-code": [
            # Core coding
            "ponytail",
            "karpathy-coding",
            # Frontend
            "frontend-taste",
            "frontend-review",
            "frontend-redesign",
            # Security
            "security-review",
            "vietnam-payment-review",
            # Quality
            "test-analysis",
            "perf-optimization",
            "stability",
            "data-quality",
            # Meta
            "full-output",
        ],
        "grok": [
            # Core coding
            "ponytail",
            "karpathy-coding",
            # Frontend
            "frontend-taste",
            "frontend-review",
            # Security
            "security-review",
            # Quality
            "test-analysis",
            "perf-optimization",
            # Meta
            "full-output",
        ],
    }

    # Gate definitions per agent
    GATE_DEFINITIONS: dict[str, dict[str, list[str]]] = {
        "universal": {
            "pre": ["U.1", "U.2", "U.3", "U.4"],
            "post": ["U.5", "U.6", "U.7", "§X", "§Y"],
        },
        "cursor": {
            "pre": ["K.1", "K.2", "K.3", "K.4"],
            "post": ["K.5", "K.6", "K.7"],
        },
        "codex": {
            "pre": ["CX.1", "CX.2", "CX.3", "CX.4"],
            "post": ["CX.5", "CX.6", "CX.7"],
        },
        "claude-code": {
            "pre": ["C.1", "C.2", "C.3", "C.4"],
            "post": ["C.5", "C.6", "C.7"],
        },
        "grok": {
            "pre": ["G.1", "G.2", "G.3", "G.4"],
            "post": ["G.5", "G.6", "G.7"],
        },
    }

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the cross-agent skill registry.

        Args:
            base_path: Base path for skill files
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self._manifests: dict[str, SkillManifest] = {}
        self._agent_skills: dict[str, list[str]] = {}
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the registry with default skills."""
        self._register_universal_skills()
        self._register_agent_skills()
        self._scan_skill_directories()

    def _register_universal_skills(self) -> None:
        """Register universal skills that work on all agents - synchronized with TypeScript framework.ts."""
        universal_data = {
            # ── Coding Discipline ──────────────────────────────────────────
            "karpathy-coding": {
                "version": "3.0.0",
                "description": "Universal coding discipline overlay - think first, minimal code, surgical changes",
                "tags": ["karpathy", "coding-discipline", "think-first", "cross-agent", "universal"],
                "triggers": ["coding", "implementation", "build", "think before code"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X", "§Y"],
                "agent_gates": {
                    "cursor": ["K.1", "K.2", "K.3", "K.4", "K.5", "K.6", "K.7"],
                    "codex": ["CX.1", "CX.2", "CX.3", "CX.4", "CX.5", "CX.6", "CX.7"],
                    "claude-code": ["C.1", "C.2", "C.3", "C.4", "C.5", "C.6", "C.7"],
                    "grok": ["G.1", "G.2", "G.3", "G.4", "G.5", "G.6", "G.7"],
                },
            },
            "ponytail": {
                "version": "1.0.0",
                "description": "Lazy Senior Dev - YAGNI optimization, minimum code",
                "tags": ["yagni", "minimal", "senior", "coding-discipline"],
                "triggers": ["yagni", "minimal", "simplify"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "full-output": {
                "version": "1.0.0",
                "description": "Ensure full implementation without truncation - no skeletons, no TODOs",
                "tags": ["output", "completeness", "implementation", "no-skeleton"],
                "triggers": ["full implementation", "complete", "not skeleton", "no todo"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Frontend ───────────────────────────────────────────────────
            "frontend-taste": {
                "version": "1.0.0",
                "description": "Anti-slop frontend for landing pages, portfolios, redesigns",
                "tags": ["frontend", "design", "landing", "taste", "anti-slop"],
                "triggers": ["landing page", "portfolio", "homepage", "design"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "frontend-review": {
                "version": "1.0.0",
                "description": "Quality gate for all frontend tasks - dual-gate review",
                "tags": ["frontend", "review", "quality", "gate", "a11y"],
                "triggers": ["review", "quality check", "audit ui"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "frontend-redesign": {
                "version": "1.0.0",
                "description": "Upgrade UI on existing codebase without breaking it",
                "tags": ["frontend", "redesign", "upgrade", "improve"],
                "triggers": ["redesign", "upgrade", "improve existing", "modernize"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "hallmark": {
                "version": "1.0.0",
                "description": "Anti-slop design taste - 57 slop-test gates",
                "tags": ["design", "taste", "anti-slop", "hallmark"],
                "triggers": ["design", "taste", "anti-slop"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "dashboard-ui": {
                "version": "1.0.0",
                "description": "Dashboard/Admin components - inputs, tables, forms, pickers",
                "tags": ["dashboard", "admin", "ui", "components"],
                "triggers": ["dashboard", "admin", "table", "form"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "landing-page-pro": {
                "version": "1.0.0",
                "description": "Professional Landing Page - SaaS, Products, E-commerce",
                "tags": ["landing", "saas", "e-commerce", "hero", "pricing"],
                "triggers": ["landing page", "saas", "e-commerce", "pricing"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Security ───────────────────────────────────────────────────
            "security-review": {
                "version": "1.1.0",
                "description": "Comprehensive security review (OWASP Top 10 + Marketing Security)",
                "tags": ["security", "vulnerability", "audit", "owasp", "gdpr", "consent"],
                "triggers": ["security", "vulnerability", "penetration", "owasp"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "vietnam-payment-review": {
                "version": "1.0.0",
                "description": "Vietnam payment provider review - MoMo, SePay, PayOS, VNPay",
                "tags": ["payment", "vietnam", "momo", "sepay", "webhook"],
                "triggers": ["momo", "sepay", "payment", "vietqr", "vietnam payment"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Writing & Copy ─────────────────────────────────────────────
            "ai-copywriter": {
                "version": "1.0.0",
                "description": "Humanize AI text - 33 patterns for natural copy",
                "tags": ["copywriting", "humanize", "content"],
                "triggers": ["copywriting", "humanize", "content"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "simple-english": {
                "version": "1.0.0",
                "description": "Simplify to plain language",
                "tags": ["writing", "clarity", "plain-language"],
                "triggers": ["simplify", "plain language", "clarity"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Document & Knowledge ────────────────────────────────────────
            "book-to-skill": {
                "version": "1.0.0",
                "description": "Convert books/docs to agent skills",
                "tags": ["document", "books", "knowledge", "skill"],
                "triggers": ["book", "document", "convert to skill", "knowledge"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "document-ocr": {
                "version": "1.0.0",
                "description": "OCR document processing - invoices, IDs, contracts",
                "tags": ["ocr", "document", "invoice", "extraction"],
                "triggers": ["ocr", "document", "scan", "invoice"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "pixelrag": {
                "version": "1.0.0",
                "description": "Visual RAG - PDF, website, tables, diagrams",
                "tags": ["rag", "visual", "image", "document"],
                "triggers": ["rag", "visual", "image", "pdf"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── AI & RAG ───────────────────────────────────────────────────
            "weknora-kb": {
                "version": "1.0.0",
                "description": "Knowledge base scaffold - RAG implementation, hybrid search",
                "tags": ["rag", "kb", "knowledge-base", "weknora"],
                "triggers": ["rag", "knowledge-base", "retrieval"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "weknora-agent": {
                "version": "1.0.0",
                "description": "Grounded agent on WeKnora KB - tool calling, citation",
                "tags": ["agent", "rag", "reasoning", "weknora"],
                "triggers": ["agent", "rag", "reasoning"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "video-generation": {
                "version": "1.0.0",
                "description": "AI short video generation (9:16)",
                "tags": ["video", "short-form", "ai"],
                "triggers": ["video", "short video", "ai video"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Performance ─────────────────────────────────────────────────
            "code-graph-analysis": {
                "version": "1.0.0",
                "description": "Knowledge graph queries using Memgraph + Qdrant",
                "tags": ["knowledge-graph", "cypher", "memgraph", "code-analysis"],
                "triggers": ["graph", "cypher", "dependencies", "code analysis"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "perf-optimization": {
                "version": "1.0.0",
                "description": "Performance optimization - memory, speed, token efficiency, caching",
                "tags": ["performance", "optimization", "memory", "speed", "token"],
                "triggers": ["performance", "optimize", "memory", "speed", "cache"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Quality ───────────────────────────────────────────────────
            "test-analysis": {
                "version": "1.0.0",
                "description": "Comprehensive test analysis - functional, UI, integration, e2e",
                "tags": ["testing", "quality", "functional", "UI-test", "integration", "e2e"],
                "triggers": ["test", "testing", "unit test", "e2e", "coverage"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "stability": {
                "version": "1.0.0",
                "description": "Stability and reliability - error handling, resilience, monitoring",
                "tags": ["stability", "reliability", "error-handling", "resilience"],
                "triggers": ["stability", "reliability", "error", "crash", "monitoring"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "data-quality": {
                "version": "1.0.0",
                "description": "Data quality and database - validation, schema, migrations",
                "tags": ["data", "database", "validation", "schema", "migration"],
                "triggers": ["data", "database", "schema", "migration", "validation"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Design ─────────────────────────────────────────────────────
            "open-design": {
                "version": "1.0.0",
                "description": "Design tokens for new projects - anti-slop by default",
                "tags": ["design-tokens", "primitives", "tokens"],
                "triggers": ["design tokens", "new project", "setup"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "visual-explainer": {
                "version": "1.0.0",
                "description": "Diagrams from text - sequence, architecture, ER",
                "tags": ["diagram", "docs", "visualization"],
                "triggers": ["diagram", "visualize", "architecture"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Domain ─────────────────────────────────────────────────────
            "vietnam-address": {
                "version": "1.0.0",
                "description": "Vietnamese administrative addresses parser",
                "tags": ["vietnam", "address", "province", "district"],
                "triggers": ["vietnam address", "province", "district", "ward"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            "bazi": {
                "version": "1.0.0",
                "description": "Four Pillars / astrology engine - Bazi (Tứ Trụ)",
                "tags": ["bazi", "astrology", "tu-vi", "four-pillars"],
                "triggers": ["bazi", "astrology", "fortune", "tu-vi"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
            # ── Meta ───────────────────────────────────────────────────────
            "skill-installer": {
                "version": "1.0.0",
                "description": "Bootstrap a skill into a repo",
                "tags": ["meta", "install", "skill"],
                "triggers": ["install skill", "add skill", "bootstrap"],
                "pre_gates": ["U.1", "U.2", "U.3", "U.4"],
                "post_gates": ["U.5", "U.6", "U.7", "§X"],
            },
        }

        for name, data in universal_data.items():
            manifest = SkillManifest(
                name=name,
                version=data["version"],
                compatible_agents=["universal"],
                primary_agent="cursor",
                tags=data["tags"],
                triggers=data["triggers"],
                pre_gates=data["pre_gates"],
                post_gates=data["post_gates"],
                agent_gates=data.get("agent_gates", {}),
                description=data["description"],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
            )
            self._manifests[name] = manifest

    def _register_agent_skills(self) -> None:
        """Register agent-specific skills."""
        for agent, skills in self.AGENT_SKILL_MAPPINGS.items():
            self._agent_skills[agent] = skills
            for skill_name in skills:
                if skill_name not in self._manifests:
                    manifest = SkillManifest(
                        name=skill_name,
                        version="1.0.0",
                        compatible_agents=[agent],
                        primary_agent=agent,
                        tags=[agent, "agent-specific"],
                        triggers=[],
                        pre_gates=[f"{agent[:1].upper()}.1", f"{agent[:1].upper()}.2"],
                        post_gates=[f"{agent[:1].upper()}.3", f"{agent[:1].upper()}.4"],
                        description=f"{agent} specific skill: {skill_name}",
                        created_at=datetime.now().isoformat(),
                        updated_at=datetime.now().isoformat(),
                    )
                    self._manifests[skill_name] = manifest

    def _scan_skill_directories(self) -> None:
        """Scan agent-specific skill directories."""
        skill_dirs = {
            "cursor": self.base_path / ".cursor" / "skills",
            "codex": self.base_path / ".cursor" / "skills",
            "claude-code": self.base_path / ".claude" / "skills",
            "grok": self.base_path / ".grok" / "skills",
        }

        for agent, skill_dir in skill_dirs.items():
            if skill_dir.exists():
                for skill_md in skill_dir.rglob("SKILL.md"):
                    self._register_skill_file(skill_md, agent)

    def _register_skill_file(self, path: Path, agent: str) -> None:
        """Register a skill from a SKILL.md file."""
        try:
            content = path.read_text(encoding="utf-8")
            name = path.parent.name

            # Parse frontmatter for compatibility info
            compatible = ["universal"] if "universal" in content.lower() else [agent]
            if agent in content:
                compatible.append(agent)

            # Check for other agents mentioned
            for other_agent in ["codex", "claude-code", "grok", "cursor"]:
                if other_agent in content and other_agent not in compatible:
                    compatible.append(other_agent)

            # Get description from first paragraph
            description = ""
            lines = content.split("\n")
            for line in lines:
                if line.strip() and not line.startswith("#") and not line.startswith("-"):
                    description = line.strip()[:200]
                    break

            if name in self._manifests:
                # Update existing manifest
                manifest = self._manifests[name]
                for a in compatible:
                    if a not in manifest.compatible_agents:
                        manifest.compatible_agents.append(a)
                manifest.updated_at = datetime.now().isoformat()
            else:
                # Create new manifest
                manifest = SkillManifest(
                    name=name,
                    version="1.0.0",
                    compatible_agents=compatible,
                    primary_agent=agent,
                    tags=[agent, "skill"],
                    triggers=[],
                    pre_gates=["U.1", "U.2", "U.3", "U.4"],
                    post_gates=["U.5", "U.6", "U.7", "§X"],
                    path=str(path),
                    description=description,
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                )
                self._manifests[name] = manifest

        except (OSError, UnicodeDecodeError):
            pass

    def get_skill(self, name: str) -> Optional[SkillManifest]:
        """Get a skill manifest by name."""
        return self._manifests.get(name)

    def get_compatible_skills(self, agent: str) -> list[SkillManifest]:
        """Get all skills compatible with an agent."""
        compatible = []
        for manifest in self._manifests.values():
            if manifest.is_compatible(agent):
                compatible.append(manifest)
        return compatible

    def get_skills_by_tag(self, tag: str) -> list[SkillManifest]:
        """Get all skills with a specific tag."""
        return [
            m for m in self._manifests.values()
            if tag in m.tags
        ]

    def search_skills(self, query: str) -> list[tuple[SkillManifest, float]]:
        """Search skills by name, tag, or trigger."""
        query_lower = query.lower()
        results = []

        for manifest in self._manifests.values():
            score = 0.0

            # Name match (highest weight)
            if query_lower in manifest.name.lower():
                score += 0.5

            # Tag match
            for tag in manifest.tags:
                if query_lower in tag.lower():
                    score += 0.3

            # Trigger match
            for trigger in manifest.triggers:
                if query_lower in trigger.lower():
                    score += 0.2

            if score > 0:
                results.append((manifest, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def create_manifest(self, skill_name: str) -> Optional[SkillManifest]:
        """Create a standardized manifest for a skill."""
        manifest = self._manifests.get(skill_name)
        if manifest is None:
            return None

        # Return a copy with all agent-specific gates resolved
        resolved = SkillManifest(
            name=manifest.name,
            version=manifest.version,
            compatible_agents=manifest.compatible_agents.copy(),
            primary_agent=manifest.primary_agent,
            tags=manifest.tags.copy(),
            triggers=manifest.triggers.copy(),
            pre_gates=manifest.pre_gates.copy(),
            post_gates=manifest.post_gates.copy(),
            agent_gates=manifest.agent_gates.copy(),
            path=manifest.path,
            description=manifest.description,
            dependencies=manifest.dependencies.copy(),
            created_at=manifest.created_at,
            updated_at=datetime.now().isoformat(),
        )
        return resolved

    def export_manifest(
        self,
        manifest: SkillManifest,
        format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Export a manifest to specified format.

        Args:
            manifest: The manifest to export
            format: Export format ("json" or "yaml")
            output_path: Optional path to write the export

        Returns:
            The exported content as a string
        """
        if format == "json":
            content = json.dumps(manifest.to_dict(), indent=2)
        elif format == "yaml":
            content = self._to_yaml(manifest.to_dict())
        else:
            raise ValueError(f"Unsupported format: {format}")

        if output_path:
            Path(output_path).write_text(content, encoding="utf-8")

        return content

    def _to_yaml(self, data: dict[str, Any], indent: int = 0) -> str:
        """Convert dict to YAML-like string."""
        lines = []
        prefix = "  " * indent

        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{prefix}  - {item}")
            elif isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._to_yaml(value, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {value}")

        return "\n".join(lines)

    def get_agent_gates(self, agent: str) -> dict[str, list[str]]:
        """Get gate definitions for an agent."""
        gates = {
            "pre": self.GATE_DEFINITIONS["universal"]["pre"].copy(),
            "post": self.GATE_DEFINITIONS["universal"]["post"].copy(),
        }

        if agent in self.GATE_DEFINITIONS:
            agent_def = self.GATE_DEFINITIONS[agent]
            gates["pre"].extend(agent_def.get("pre", []))
            gates["post"].extend(agent_def.get("post", []))

        return gates

    def detect_agent(self) -> AgentType:
        """Detect which agent is running based on environment."""
        if os.getenv("CURSOR_IDE") or os.getenv("CURSOR_PROJECT"):
            return AgentType.CURSOR
        elif os.getenv("CODEX_ENABLED") or os.getenv("ORIGIN_HOST"):
            return AgentType.CODEX
        elif os.getenv("CLAUDE_IDE") or os.getenv("CLAUDE_API_KEY"):
            return AgentType.CLAUDE_CODE
        elif os.getenv("GROK_API_KEY"):
            return AgentType.GROK
        else:
            return AgentType.UNKNOWN

    def get_recommended_skills(self, agent: str, task: str) -> list[CrossAgentSkill]:
        """Get recommended skills for a task on a specific agent."""
        compatible = self.get_compatible_skills(agent)
        task_lower = task.lower()
        recommended = []

        for manifest in compatible:
            score = 0.0

            # Check triggers
            for trigger in manifest.triggers:
                if trigger.lower() in task_lower:
                    score += 0.5

            # Check tags
            for tag in manifest.tags:
                if tag.lower() in task_lower:
                    score += 0.3

            if score > 0:
                cross_skill = CrossAgentSkill(
                    manifest=manifest,
                    confidence=min(score, 0.99),
                    compatible_with=manifest.compatible_agents.copy(),
                    agent_specific=agent not in manifest.compatible_agents,
                )
                recommended.append(cross_skill)

        recommended.sort(key=lambda x: x.confidence, reverse=True)
        return recommended

    def export_all_manifests(self, output_dir: str) -> int:
        """
        Export all skill manifests to a directory.

        Args:
            output_dir: Directory to write manifests

        Returns:
            Number of manifests exported
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        count = 0
        for manifest in self._manifests.values():
            manifest_path = output_path / f"{manifest.name}.json"
            self.export_manifest(manifest, format="json", output_path=str(manifest_path))
            count += 1

        return count

    def get_registry_stats(self) -> dict[str, Any]:
        """Get statistics about the registry."""
        agent_counts = {}
        for manifest in self._manifests.values():
            for agent in manifest.compatible_agents:
                agent_counts[agent] = agent_counts.get(agent, 0) + 1

        return {
            "total_skills": len(self._manifests),
            "universal_skills": sum(
                1 for m in self._manifests.values()
                if "universal" in m.compatible_agents
            ),
            "agent_specific_skills": {
                agent: len(skills)
                for agent, skills in self._agent_skills.items()
            },
            "skills_by_agent": agent_counts,
            "gates": {
                agent: gates
                for agent, gates in self.GATE_DEFINITIONS.items()
            },
        }


def create_cross_agent_registry(base_path: Optional[str] = None) -> CrossAgentSkillRegistry:
    """
    Factory function to create a CrossAgentSkillRegistry.

    Args:
        base_path: Base path for skill files

    Returns:
        Configured CrossAgentSkillRegistry instance
    """
    return CrossAgentSkillRegistry(base_path=base_path)
