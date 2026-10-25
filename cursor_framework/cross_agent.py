"""
Cross-Agent Compatibility Layer

Provides unified cross-agent skill detection and compatibility for vibe coding agents:
- Cursor IDE
- Codex (cursor.com)
- Claude Code (@cursor/codex)
- Grok (x.com/grok)

This module serves as the single source of truth for:
- Universal skill definitions
- Agent-specific skill mappings
- Gate execution protocols
- Skill trigger keywords

Synchronized with TypeScript framework.ts and WPF configuration.

Usage:
    >>> from cursor_framework.cross_agent import (
    ...     get_current_agent,
    ...     get_compatible_skills,
    ...     execute_pre_gates,
    ...     execute_post_gates,
    ... )
    >>> agent = get_current_agent()
    >>> skills = get_compatible_skills("Build a landing page")
    >>> print(f"Recommended: {[s.name for s in skills]}")
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


# ─────────────────────────────────────────────────────────────────────────────
# Agent Types
# ─────────────────────────────────────────────────────────────────────────────

class AgentType(Enum):
    """Supported vibe coding agents."""
    CURSOR = "cursor"
    ANTIGRAVITY = "antigravity"
    CODEX = "codex"
    CLAUDE_CODE = "claude-code"
    WINDSURF = "windsurf"
    CLINE = "cline"
    ROO_CODE = "roo"
    GROK = "grok"
    AIDER = "aider"
    ZED = "zed"
    UNIVERSAL = "universal"
    UNKNOWN = "unknown"


class GateType(Enum):
    """Types of review gates."""
    PRE_REVIEW = "pre-review"
    POST_REVIEW = "post-review"


# ─────────────────────────────────────────────────────────────────────────────
# Universal Gate Definitions
# ─────────────────────────────────────────────────────────────────────────────

# Universal gates work on ALL agents
UNIVERSAL_GATES = {
    "pre": ["U.1", "U.2", "U.3", "U.4"],
    "post": ["U.5", "U.6", "U.7", "§X", "§Y"],
}

# Agent-specific gate extensions
AGENT_GATE_EXTENSIONS = {
    "cursor": {
        "pre": ["K.1", "K.2", "K.3", "K.4"],
        "post": ["K.5", "K.6", "K.7"],
    },
    "antigravity": {
        "pre": ["AG.1", "AG.2", "AG.3", "AG.4"],
        "post": ["AG.5", "AG.6", "AG.7"],
    },
    "codex": {
        "pre": ["CX.1", "CX.2", "CX.3", "CX.4"],
        "post": ["CX.5", "CX.6", "CX.7"],
    },
    "claude-code": {
        "pre": ["C.1", "C.2", "C.3", "C.4"],
        "post": ["C.5", "C.6", "C.7"],
    },
    "windsurf": {
        "pre": ["W.1", "W.2", "W.3", "W.4"],
        "post": ["W.5", "W.6", "W.7"],
    },
    "cline": {
        "pre": ["CL.1", "CL.2", "CL.3", "CL.4"],
        "post": ["CL.5", "CL.6", "CL.7"],
    },
    "roo": {
        "pre": ["R.1", "R.2", "R.3", "R.4"],
        "post": ["R.5", "R.6", "R.7"],
    },
    "grok": {
        "pre": ["G.1", "G.2", "G.3", "G.4"],
        "post": ["G.5", "G.6", "G.7"],
    },
    "zed": {
        "pre": ["Z.1", "Z.2", "Z.3", "Z.4"],
        "post": ["Z.5", "Z.6", "Z.7"],
    },
}

# Gate prefix mapping
GATE_PREFIXES = {
    "cursor": "K",
    "antigravity": "AG",
    "codex": "CX",
    "claude-code": "C",
    "windsurf": "W",
    "cline": "CL",
    "roo": "R",
    "grok": "G",
    "zed": "Z",
    "aider": "AI",
    "universal": "U",
    "unknown": "U",
}

# Gate descriptions for documentation
GATE_DESCRIPTIONS = {
    "U.1": "Think Before Code - What am I assuming? Is there a simpler approach?",
    "U.2": "Simplicity Check - Is this over-engineered? Can 200 lines become 50?",
    "U.3": "Surgical Scope - Only touch what was requested. Match existing style.",
    "U.4": "Goal Definition - Define verifiable success criteria.",
    "U.5": "Implementation Verification - Every line traces to request.",
    "U.6": "Simplicity Re-Check - Still minimal? Remove any added complexity.",
    "U.7": "Goal Achievement - Success criteria verified, tests pass.",
    "§X": "Verify Before Deliver - Read actual code, verify gates line-by-line.",
    "§Y": "Receive Feedback - Read feedback fully before responding.",
    "K.1": "Cursor: Think before code (Cursor-specific)",
    "K.2": "Cursor: Simplicity check (Cursor-specific)",
    "K.3": "Cursor: Surgical scope (Cursor-specific)",
    "K.4": "Cursor: Goal definition (Cursor-specific)",
    "K.5": "Cursor: Implementation verification (Cursor-specific)",
    "K.6": "Cursor: Simplicity re-check (Cursor-specific)",
    "K.7": "Cursor: Goal achievement (Cursor-specific)",
}


# ─────────────────────────────────────────────────────────────────────────────
# Universal Skills (work on ALL agents)
# ─────────────────────────────────────────────────────────────────────────────

UNIVERSAL_SKILLS = [
    # Coding Discipline
    "karpathy-coding",
    "ponytail",
    "full-output",
    
    # Frontend
    "frontend-taste",
    "frontend-review",
    "frontend-redesign",
    "hallmark",
    "dashboard-ui",
    "landing-page-pro",
    
    # Security
    "security-review",
    "reverse-engineer-anything",
    
    # Quality
    "test-analysis",
    "perf-optimization",
    "stability",
    "data-quality",
    
    # Performance
    "code-graph-analysis",
]

# Agent-specific skills (not available on all agents)
AGENT_SPECIFIC_SKILLS = {
    "cursor": [
        "vietnam-payment-review",
        "vietnam-address",
        "bazi",
        "document-ocr",
        "weknora-kb",
        "weknora-agent",
        "video-generation",
        "pixelrag",
        "visual-explainer",
        "open-design",
        "ai-copywriter",
        "simple-english",
        "book-to-skill",
        "skill-installer",
    ],
    "codex": [
        "vietnam-payment-review",
    ],
    "claude-code": [
        "vietnam-payment-review",
    ],
    "grok": [
        # Limited agent-specific skills for Grok
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# Skill Definitions
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SkillDefinition:
    """Complete skill definition with metadata."""
    name: str
    category: str
    description: str
    tags: list[str]
    triggers: list[str]
    pre_gates: list[str]
    post_gates: list[str]
    role: str = "primary"  # primary, secondary, overlay, mandatory
    dependencies: list[str] = field(default_factory=list)
    metrics: dict[str, str] = field(default_factory=dict)


# All skills in the framework - synchronized with framework.ts
ALL_SKILLS: dict[str, SkillDefinition] = {
    # ── Coding Discipline ──────────────────────────────────────────────────
    "karpathy-coding": SkillDefinition(
        name="karpathy-coding",
        category="Coding Discipline",
        description="Universal coding discipline overlay - think first, minimal code, surgical changes",
        tags=["karpathy", "coding-discipline", "think-first", "cross-agent", "overlay"],
        triggers=["coding", "implementation", "build", "think before code"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X", "§Y"],
        role="overlay",
        metrics={"lines": "-54%", "tokens": "-22%", "cost": "-20%", "time": "-27%"},
    ),
    "ponytail": SkillDefinition(
        name="ponytail",
        category="Coding Discipline",
        description="Lazy Senior Dev - YAGNI optimization, minimum code",
        tags=["yagni", "minimal", "senior"],
        triggers=["yagni", "minimal", "simplify", "lazy"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "full-output": SkillDefinition(
        name="full-output",
        category="Coding Discipline",
        description="Ensure full implementation without truncation",
        tags=["output", "completeness", "no-skeleton"],
        triggers=["full implementation", "complete", "not skeleton", "no todo"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    
    # ── Frontend ───────────────────────────────────────────────────────────
    "frontend-taste": SkillDefinition(
        name="frontend-taste",
        category="Frontend",
        description="Anti-slop frontend for landing pages, portfolios, redesigns",
        tags=["frontend", "design", "taste", "anti-slop", "landing"],
        triggers=["landing page", "portfolio", "homepage", "design"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
        metrics={"variance": "0-10", "motion": "0-10", "density": "0-10"},
    ),
    "frontend-review": SkillDefinition(
        name="frontend-review",
        category="Frontend",
        description="Quality gate for all frontend tasks - dual-gate review",
        tags=["frontend", "review", "quality", "gate", "a11y"],
        triggers=["review", "quality check", "audit ui"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    "frontend-redesign": SkillDefinition(
        name="frontend-redesign",
        category="Frontend",
        description="Upgrade UI on existing codebase without breaking it",
        tags=["frontend", "redesign", "upgrade"],
        triggers=["redesign", "upgrade", "improve existing"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "hallmark": SkillDefinition(
        name="hallmark",
        category="Frontend",
        description="Anti-slop design taste - 57 slop-test gates",
        tags=["design", "taste", "anti-slop"],
        triggers=["design", "taste", "anti-slop"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "dashboard-ui": SkillDefinition(
        name="dashboard-ui",
        category="Frontend",
        description="Dashboard/Admin components - inputs, tables, forms, pickers",
        tags=["dashboard", "admin", "ui", "components"],
        triggers=["dashboard", "admin", "table", "form"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "landing-page-pro": SkillDefinition(
        name="landing-page-pro",
        category="Frontend",
        description="Professional Landing Page - SaaS, Products, E-commerce",
        tags=["landing", "saas", "e-commerce", "hero", "pricing"],
        triggers=["landing page", "saas", "e-commerce", "pricing"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    
    # ── Security ───────────────────────────────────────────────────────────
    "security-review": SkillDefinition(
        name="security-review",
        category="Security",
        description="Comprehensive security review (OWASP Top 10 + Marketing Security)",
        tags=["security", "vulnerability", "audit", "owasp", "gdpr"],
        triggers=["security", "vulnerability", "penetration", "owasp"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    "vietnam-payment-review": SkillDefinition(
        name="vietnam-payment-review",
        category="Security",
        description="Vietnam payment provider review - MoMo, SePay, PayOS, VNPay",
        tags=["payment", "vietnam", "momo", "sepay"],
        triggers=["momo", "sepay", "payment", "vietqr"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
        dependencies=["security-review"],
    ),
    "reverse-engineer-anything": SkillDefinition(
        name="reverse-engineer-anything",
        category="Security",
        description="REA - Reverse engineer native binaries, .NET, Electron/JS, APK, WASM, EVM, Go",
        tags=["reverse-engineering", "binary-analysis", "decompiler", "disassembler", "ghidra", "hopper", "ida", "asar", "apk", "wasm"],
        triggers=["reverse-engineer", "reverse engineering", "decompile", "disasm", "binary analysis", "ghidra", "hopper", "ida", "asar", "apk analysis", "jadx", "wasm analysis"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
        dependencies=[],
    ),
    
    # ── Quality ─────────────────────────────────────────────────────────────
    "test-analysis": SkillDefinition(
        name="test-analysis",
        category="Quality",
        description="Comprehensive test analysis - functional, UI, integration, e2e",
        tags=["testing", "quality", "functional", "UI-test"],
        triggers=["test", "testing", "unit test", "e2e", "coverage"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="mandatory",
    ),
    "perf-optimization": SkillDefinition(
        name="perf-optimization",
        category="Performance",
        description="Performance optimization - memory, speed, token efficiency, caching",
        tags=["performance", "optimization", "memory", "speed"],
        triggers=["performance", "optimize", "memory", "speed", "cache"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="mandatory",
    ),
    "stability": SkillDefinition(
        name="stability",
        category="Operations",
        description="Stability and reliability - error handling, resilience, monitoring",
        tags=["stability", "reliability", "error-handling"],
        triggers=["stability", "reliability", "error", "crash"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="mandatory",
    ),
    "data-quality": SkillDefinition(
        name="data-quality",
        category="Data",
        description="Data quality and database - validation, schema, migrations",
        tags=["data", "database", "validation", "schema"],
        triggers=["data", "database", "schema", "migration"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="mandatory",
    ),
    
    # ── Performance ────────────────────────────────────────────────────────
    "code-graph-analysis": SkillDefinition(
        name="code-graph-analysis",
        category="Performance",
        description="Knowledge graph queries using Memgraph + Qdrant",
        tags=["knowledge-graph", "cypher", "memgraph"],
        triggers=["graph", "cypher", "dependencies"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    
    # ── Design ─────────────────────────────────────────────────────────────
    "open-design": SkillDefinition(
        name="open-design",
        category="Experience",
        description="Design tokens for new projects - anti-slop by default",
        tags=["design-tokens", "primitives", "tokens"],
        triggers=["design tokens", "new project", "setup"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "visual-explainer": SkillDefinition(
        name="visual-explainer",
        category="Experience",
        description="Diagrams from text - sequence, architecture, ER",
        tags=["diagram", "docs", "visualization"],
        triggers=["diagram", "visualize", "architecture"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    
    # ── Domain ───────────────────────────────────────────────────────────────
    "vietnam-address": SkillDefinition(
        name="vietnam-address",
        category="Domain",
        description="Vietnamese administrative addresses parser",
        tags=["vietnam", "address", "province"],
        triggers=["vietnam address", "province", "district"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "bazi": SkillDefinition(
        name="bazi",
        category="Domain",
        description="Four Pillars / astrology engine - Bazi (Tứ Trụ)",
        tags=["bazi", "astrology", "tu-vi"],
        triggers=["bazi", "astrology", "fortune", "tu-vi"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    "document-ocr": SkillDefinition(
        name="document-ocr",
        category="Domain",
        description="OCR document processing - invoices, IDs, contracts",
        tags=["ocr", "document", "invoice"],
        triggers=["ocr", "document", "scan", "invoice"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    
    # ── AI & RAG ───────────────────────────────────────────────────────────
    "weknora-kb": SkillDefinition(
        name="weknora-kb",
        category="AI",
        description="Knowledge base scaffold - RAG implementation, hybrid search",
        tags=["rag", "kb", "knowledge-base"],
        triggers=["rag", "knowledge-base", "retrieval"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    "weknora-agent": SkillDefinition(
        name="weknora-agent",
        category="AI",
        description="Grounded agent on WeKnora KB - tool calling, citation",
        tags=["agent", "rag", "reasoning"],
        triggers=["agent", "rag", "reasoning"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    "video-generation": SkillDefinition(
        name="video-generation",
        category="AI",
        description="AI short video generation (9:16)",
        tags=["video", "short-form", "ai"],
        triggers=["video", "short video", "ai video"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    "pixelrag": SkillDefinition(
        name="pixelrag",
        category="AI",
        description="Visual RAG - PDF, website, tables, diagrams",
        tags=["rag", "visual", "image", "document"],
        triggers=["rag", "visual", "image", "pdf"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    
    # ── Writing & Copy ────────────────────────────────────────────────────
    "ai-copywriter": SkillDefinition(
        name="ai-copywriter",
        category="Writing",
        description="Humanize AI text - 33 patterns for natural copy",
        tags=["copywriting", "humanize", "content"],
        triggers=["copywriting", "humanize", "content"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "simple-english": SkillDefinition(
        name="simple-english",
        category="Writing",
        description="Simplify to plain language",
        tags=["writing", "clarity", "plain-language"],
        triggers=["simplify", "plain language", "clarity"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
    "book-to-skill": SkillDefinition(
        name="book-to-skill",
        category="Document",
        description="Convert books/docs to agent skills",
        tags=["document", "books", "knowledge"],
        triggers=["book", "document", "convert to skill"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="primary",
    ),
    
    # ── Meta ────────────────────────────────────────────────────────────────
    "skill-installer": SkillDefinition(
        name="skill-installer",
        category="Meta",
        description="Bootstrap a skill into a repo",
        tags=["meta", "install", "skill"],
        triggers=["install skill", "add skill", "bootstrap"],
        pre_gates=["U.1", "U.2", "U.3", "U.4"],
        post_gates=["U.5", "U.6", "U.7", "§X"],
        role="secondary",
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# Agent Detection
# ─────────────────────────────────────────────────────────────────────────────

# Environment variable mappings for agent detection
AGENT_ENV_VARS = {
    "cursor": ["CURSOR_IDE", "CURSOR_PROJECT"],
    "antigravity": ["ANTIGRAVITY_APP_DATA", "ANTIGRAVITY_WORKSPACE_ROOT", "ANTIGRAVITY_CLI", "GEMINI_CLI"],
    "codex": ["CODEX_ENABLED", "ORIGIN_HOST", "CODEX_WORKSPACE_ROOT"],
    "claude-code": ["CLAUDE_IDE", "CLAUDE_API_KEY", "CLAUDE_PROJECT_DIR"],
    "windsurf": ["WINDSURF_IDE", "WINDSURF_WORKSPACE_ROOT", "CODEIUM_API_KEY"],
    "cline": ["CLINE_ACTIVE", "CLINE_VERSION"],
    "roo": ["ROO_ACTIVE", "ROO_CODE_VERSION"],
    "grok": ["GROK_API_KEY"],
    "zed": ["ZED_SERVER", "ZEDAI_API_KEY"],
    "aider": ["AIDER_ENV"],
}

# Filesystem directory markers for fallback detection
AGENT_DIR_MARKERS = {
    "antigravity": [".gemini", ".agents"],
    "cursor": [".cursor"],
    "claude-code": [".claude"],
    "codex": [".codex"],
    "windsurf": [".windsurf"],
    "cline": [".cline"],
    "roo": [".roo"],
    "zed": [".zed"],
}


def detect_agent(workspace_path: Optional[str] = None) -> AgentType:
    """
    Detect which vibe coding agent is currently running.
    Checks environment variables first, then filesystem directory markers.
    
    Returns:
        AgentType enum value
    """
    # 1. Environment variables
    for agent, env_vars in AGENT_ENV_VARS.items():
        for env_var in env_vars:
            if os.getenv(env_var):
                try:
                    return AgentType(agent)
                except ValueError:
                    continue

    # 2. Filesystem directory markers
    root = Path(workspace_path or os.getcwd()).resolve()
    for parent in [root, *root.parents[:3]]:
        for agent, markers in AGENT_DIR_MARKERS.items():
            if any((parent / m).exists() for m in markers):
                try:
                    return AgentType(agent)
                except ValueError:
                    continue

    return AgentType.UNKNOWN


def get_current_agent(workspace_path: Optional[str] = None) -> tuple[AgentType, str]:
    """
    Get current agent type and name.
    
    Returns:
        Tuple of (AgentType, display name)
    """
    agent = detect_agent(workspace_path)
    names = {
        "cursor": "Cursor IDE",
        "antigravity": "Antigravity",
        "codex": "Codex",
        "claude-code": "Claude Code",
        "windsurf": "Windsurf",
        "cline": "Cline",
        "roo": "Roo Code",
        "grok": "Grok",
        "aider": "Aider",
        "zed": "Zed AI",
        "universal": "Universal",
        "unknown": "Unknown",
    }
    return agent, names.get(agent.value, "Unknown")


def get_gate_prefix(agent: Optional[AgentType] = None) -> str:
    """Get the gate prefix for an agent."""
    if agent is None:
        agent = detect_agent()
    return GATE_PREFIXES.get(agent.value, "U")


# ─────────────────────────────────────────────────────────────────────────────
# Skill Compatibility
# ─────────────────────────────────────────────────────────────────────────────

def is_skill_compatible(skill_name: str, agent: Optional[AgentType] = None) -> bool:
    """
    Check if a skill is compatible with an agent.
    
    Args:
        skill_name: Name of the skill
        agent: Agent to check compatibility for (defaults to current agent)
    
    Returns:
        True if skill is compatible
    """
    if agent is None:
        agent = detect_agent()
    
    # Universal skills work on all agents
    if skill_name in UNIVERSAL_SKILLS:
        return True
    
    # Check agent-specific skills
    if agent.value in AGENT_SPECIFIC_SKILLS:
        return skill_name in AGENT_SPECIFIC_SKILLS[agent.value]
    
    return False


def get_compatible_skills(agent: Optional[AgentType] = None) -> list[str]:
    """
    Get all skills compatible with an agent.
    
    Args:
        agent: Agent to get skills for (defaults to current agent)
    
    Returns:
        List of compatible skill names
    """
    if agent is None:
        agent = detect_agent()
    
    skills = list(UNIVERSAL_SKILLS)
    
    if agent.value in AGENT_SPECIFIC_SKILLS:
        skills.extend(AGENT_SPECIFIC_SKILLS[agent.value])
    
    return sorted(set(skills))


def detect_skills_from_request(request: str) -> list[tuple[str, float]]:
    """
    Detect applicable skills from a request string.
    
    Args:
        request: The user request text
    
    Returns:
        List of (skill_name, confidence) tuples sorted by confidence
    """
    request_lower = request.lower()
    results = []
    
    for skill_name, skill_def in ALL_SKILLS.items():
        confidence = 0.0
        
        # Check triggers
        for trigger in skill_def.triggers:
            if trigger.lower() in request_lower:
                confidence += 0.5
        
        # Check tags
        for tag in skill_def.tags:
            if tag.lower() in request_lower:
                confidence += 0.2
        
        # Check name
        if skill_name.replace("-", " ") in request_lower:
            confidence += 0.3
        
        if confidence > 0:
            results.append((skill_name, min(0.99, confidence)))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def get_skill_definition(skill_name: str) -> Optional[SkillDefinition]:
    """Get skill definition by name."""
    return ALL_SKILLS.get(skill_name)


# ─────────────────────────────────────────────────────────────────────────────
# Gate Execution
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class GateResult:
    """Result of gate execution."""
    gate: str
    passed: bool
    description: str
    notes: str = ""


@dataclass
class GateExecutionResult:
    """Result of full gate execution."""
    skill: str
    gate_type: GateType
    gates: list[GateResult]
    all_passed: bool
    timestamp: datetime = field(default_factory=datetime.now)


def get_gates_for_skill(
    skill_name: str,
    agent: Optional[AgentType] = None,
    gate_type: GateType = GateType.PRE_REVIEW
) -> list[str]:
    """
    Get all gates to execute for a skill.
    
    Args:
        skill_name: Name of the skill
        agent: Agent to get gates for (defaults to current agent)
        gate_type: Type of gates (pre or post)
    
    Returns:
        List of gate names to execute
    """
    if agent is None:
        agent = detect_agent()
    
    skill_def = get_skill_definition(skill_name)
    if not skill_def:
        return []
    
    gates = []
    
    # Add universal gates
    universal_key = "pre" if gate_type == GateType.PRE_REVIEW else "post"
    gates.extend(UNIVERSAL_GATES[universal_key])
    
    # Add skill-specific gates
    skill_key = "pre" if gate_type == GateType.PRE_REVIEW else "post"
    gates.extend(skill_def.pre_gates if gate_type == GateType.PRE_REVIEW else skill_def.post_gates)
    
    # Add agent-specific gates
    if agent.value in AGENT_GATE_EXTENSIONS:
        agent_ext = AGENT_GATE_EXTENSIONS[agent.value]
        gates.extend(agent_ext.get(skill_key, []))
    
    return list(dict.fromkeys(gates))  # Remove duplicates, preserve order


def get_gate_description(gate: str) -> str:
    """Get description for a gate."""
    return GATE_DESCRIPTIONS.get(gate, f"Gate {gate}")


# ─────────────────────────────────────────────────────────────────────────────
# Export & Serialization
# ─────────────────────────────────────────────────────────────────────────────

def export_skill_manifest(agent: Optional[AgentType] = None) -> dict[str, Any]:
    """
    Export skill manifest for an agent.
    
    Args:
        agent: Agent to export for (defaults to current agent)
    
    Returns:
        Dictionary with skill manifest
    """
    if agent is None:
        agent = detect_agent()
    
    compatible = get_compatible_skills(agent)
    
    return {
        "version": "1.0.0",
        "agent": agent.value,
        "agent_name": get_current_agent()[1],
        "universal_skills": UNIVERSAL_SKILLS,
        "agent_specific_skills": AGENT_SPECIFIC_SKILLS.get(agent.value, []),
        "all_compatible": compatible,
        "gate_prefix": get_gate_prefix(agent),
        "universal_gates": UNIVERSAL_GATES,
        "agent_gate_extensions": AGENT_GATE_EXTENSIONS.get(agent.value, {}),
        "generated_at": datetime.now().isoformat(),
    }


def export_all_skills_json(output_path: Optional[str] = None) -> str:
    """
    Export all skills as JSON.
    
    Args:
        output_path: Optional path to write the JSON
    
    Returns:
        JSON string
    """
    skills_data = {}
    for name, skill in ALL_SKILLS.items():
        skills_data[name] = {
            "category": skill.category,
            "description": skill.description,
            "tags": skill.tags,
            "triggers": skill.triggers,
            "pre_gates": skill.pre_gates,
            "post_gates": skill.post_gates,
            "role": skill.role,
            "dependencies": skill.dependencies,
        }
    
    data = {
        "version": "1.0.0",
        "exported_at": datetime.now().isoformat(),
        "skills": skills_data,
        "universal_skills": UNIVERSAL_SKILLS,
        "agent_specific_skills": AGENT_SPECIFIC_SKILLS,
    }
    
    json_str = json.dumps(data, indent=2)
    
    if output_path:
        Path(output_path).write_text(json_str, encoding="utf-8")
    
    return json_str


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """CLI entry point for cross-agent utilities."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cross-Agent Compatibility Layer")
    parser.add_argument("--detect", action="store_true", help="Detect current agent")
    parser.add_argument("--skills", action="store_true", help="List compatible skills")
    parser.add_argument("--export", metavar="PATH", help="Export skill manifest to JSON")
    parser.add_argument("--agent", choices=["cursor", "codex", "claude-code", "grok"],
                        help="Override agent detection")
    
    args = parser.parse_args()
    
    if args.agent:
        agent = AgentType(args.agent)
    else:
        agent = detect_agent()
    
    if args.detect:
        agent_type, name = get_current_agent()
        print(f"Detected agent: {name} ({agent_type.value})")
    
    if args.skills:
        skills = get_compatible_skills(agent)
        print(f"Compatible skills for {agent.value}:")
        for skill in skills:
            print(f"  - {skill}")
    
    if args.export:
        export_all_skills_json(args.export)
        print(f"Exported to {args.export}")


if __name__ == "__main__":
    main()
