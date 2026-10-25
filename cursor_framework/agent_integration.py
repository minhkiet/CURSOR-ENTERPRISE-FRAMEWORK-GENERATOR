"""
Agent Integration Module

Provides cross-agent compatibility detection and integration for vibe coding agents:
- Cursor IDE
- Codex (cursor.com)
- Claude Code (@cursor/codex)
- Grok (x.com/grok)

Features:
    - Agent detection via environment variables
    - Agent-specific gate prefixes
    - Cross-agent skill compatibility
    - Unified agent interface

Usage:
    >>> from cursor_framework.agent_integration import AgentDetector, AgentType, CrossAgentIntegration
    >>> detector = AgentDetector()
    >>> agent = detector.detect()
    >>> print(f"Running on: {agent.value}")
    Running on: cursor
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


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
    UNKNOWN = "unknown"


@dataclass
class AgentInfo:
    """Information about the detected agent."""
    agent_type: AgentType
    name: str
    version: Optional[str] = None
    skills_path: Optional[str] = None
    rules_path: Optional[str] = None
    agents_path: Optional[str] = None
    gate_prefix: str = "U"
    supports_mcp: bool = False
    supports_rules: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentCapability:
    """Agent capability descriptor."""
    name: str
    supported: bool
    description: str
    notes: Optional[str] = None


class AgentDetector:
    """
    Detects which vibe coding agent is currently running.
    
    Uses environment variables and filesystem markers to identify the agent:
    - Cursor IDE: CURSOR_IDE, CURSOR_PROJECT, .cursor/
    - Antigravity: ANTIGRAVITY_APP_DATA, ANTIGRAVITY_WORKSPACE_ROOT, GEMINI_CLI, .gemini/, .agents/
    - Codex: CODEX_ENABLED, ORIGIN_HOST, .codex/
    - Claude Code: CLAUDE_IDE, CLAUDE_API_KEY, .claude/
    - Windsurf: WINDSURF_IDE, .windsurf/
    - Cline: CLINE_ACTIVE, .cline/
    - Roo Code: ROO_ACTIVE, .roo/
    - Grok: GROK_API_KEY
    - Zed: ZED_SERVER, .zed/
    - Aider: AIDER_ENV
    """

    # Environment variable mappings
    ENV_MAPPINGS: dict[AgentType, list[str]] = {
        AgentType.CURSOR: ["CURSOR_IDE", "CURSOR_PROJECT"],
        AgentType.ANTIGRAVITY: ["ANTIGRAVITY_APP_DATA", "ANTIGRAVITY_WORKSPACE_ROOT", "ANTIGRAVITY_CLI", "GEMINI_CLI"],
        AgentType.CODEX: ["CODEX_ENABLED", "ORIGIN_HOST", "CODEX_WORKSPACE_ROOT"],
        AgentType.CLAUDE_CODE: ["CLAUDE_IDE", "CLAUDE_API_KEY", "CLAUDE_PROJECT_DIR"],
        AgentType.WINDSURF: ["WINDSURF_IDE", "WINDSURF_WORKSPACE_ROOT", "CODEIUM_API_KEY"],
        AgentType.CLINE: ["CLINE_ACTIVE", "CLINE_VERSION"],
        AgentType.ROO_CODE: ["ROO_ACTIVE", "ROO_CODE_VERSION"],
        AgentType.GROK: ["GROK_API_KEY"],
        AgentType.ZED: ["ZED_SERVER", "ZEDAI_API_KEY"],
        AgentType.AIDER: ["AIDER_ENV"],
    }

    # Directory marker mappings
    DIR_MARKERS: dict[AgentType, list[str]] = {
        AgentType.ANTIGRAVITY: [".gemini", ".agents"],
        AgentType.CURSOR: [".cursor"],
        AgentType.CLAUDE_CODE: [".claude"],
        AgentType.CODEX: [".codex"],
        AgentType.WINDSURF: [".windsurf"],
        AgentType.CLINE: [".cline"],
        AgentType.ROO_CODE: [".roo"],
        AgentType.ZED: [".zed"],
    }

    # Agent metadata
    AGENT_METADATA: dict[AgentType, dict[str, Any]] = {
        AgentType.CURSOR: {
            "name": "Cursor IDE",
            "gate_prefix": "K",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".cursor/skills",
            "rules_path": ".cursor/rules",
            "agents_path": ".cursor/agents",
        },
        AgentType.ANTIGRAVITY: {
            "name": "Antigravity",
            "gate_prefix": "AG",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".gemini/skills",
            "rules_path": ".gemini/rules",
            "agents_path": ".gemini/agents",
        },
        AgentType.CODEX: {
            "name": "Codex (cursor.com)",
            "gate_prefix": "CX",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".cursor/skills",
            "rules_path": ".cursor/rules",
            "agents_path": ".cursor/agents",
        },
        AgentType.CLAUDE_CODE: {
            "name": "Claude Code (@cursor/codex)",
            "gate_prefix": "C",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".claude/skills",
            "rules_path": ".claude/rules",
            "agents_path": ".claude/agents",
        },
        AgentType.WINDSURF: {
            "name": "Windsurf",
            "gate_prefix": "W",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".windsurf/rules",
            "rules_path": ".windsurf/rules",
            "agents_path": ".windsurf/workflows",
        },
        AgentType.CLINE: {
            "name": "Cline",
            "gate_prefix": "CL",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".cline/skills",
            "rules_path": ".cline/rules",
            "agents_path": ".cline/agents",
        },
        AgentType.ROO_CODE: {
            "name": "Roo Code",
            "gate_prefix": "R",
            "supports_mcp": True,
            "supports_rules": True,
            "skills_path": ".roo/rules",
            "rules_path": ".roo/rules",
            "agents_path": ".roo/modes",
        },
        AgentType.GROK: {
            "name": "Grok (x.com/grok)",
            "gate_prefix": "G",
            "supports_mcp": False,
            "supports_rules": True,
            "skills_path": ".grok/skills",
            "rules_path": ".grok/rules",
            "agents_path": ".grok/agents",
        },
        AgentType.ZED: {
            "name": "Zed AI",
            "gate_prefix": "Z",
            "supports_mcp": False,
            "supports_rules": True,
            "skills_path": ".zed",
            "rules_path": ".zed",
            "agents_path": ".zed/agents",
        },
        AgentType.AIDER: {
            "name": "Aider",
            "gate_prefix": "AI",
            "supports_mcp": False,
            "supports_rules": True,
            "skills_path": ".aider",
            "rules_path": ".aider",
            "agents_path": ".aider",
        },
    }

    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize agent detector.
        
        Args:
            workspace_root: Root directory of the workspace
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self._detected: Optional[AgentType] = None

    def detect(self) -> AgentType:
        """
        Detect which agent is running.
        
        Returns:
            AgentType enum value
        """
        if self._detected is not None:
            return self._detected

        # 1. Check environment variables
        for agent_type, env_vars in self.ENV_MAPPINGS.items():
            for env_var in env_vars:
                if os.getenv(env_var):
                    self._detected = agent_type
                    return self._detected

        # 2. Check filesystem directory markers
        for parent in [self.workspace_root, *self.workspace_root.parents[:3]]:
            for agent_type, markers in self.DIR_MARKERS.items():
                if any((parent / m).exists() for m in markers):
                    self._detected = agent_type
                    return self._detected

        self._detected = AgentType.UNKNOWN
        return self._detected

    def get_agent_info(self) -> AgentInfo:
        """
        Get detailed information about the detected agent.
        
        Returns:
            AgentInfo with agent metadata
        """
        agent_type = self.detect()
        metadata = self.AGENT_METADATA.get(agent_type, {})

        return AgentInfo(
            agent_type=agent_type,
            name=metadata.get("name", "Unknown Agent"),
            gate_prefix=metadata.get("gate_prefix", "U"),
            supports_mcp=metadata.get("supports_mcp", False),
            supports_rules=metadata.get("supports_rules", False),
            skills_path=self._resolve_path(metadata.get("skills_path")),
            rules_path=self._resolve_path(metadata.get("rules_path")),
            agents_path=self._resolve_path(metadata.get("agents_path")),
            version=os.getenv(f"{agent_type.value.upper()}_VERSION"),
            metadata=metadata,
        )

    def _resolve_path(self, relative: Optional[str]) -> Optional[str]:
        """Resolve a relative path against workspace root."""
        if relative is None:
            return None
        path = self.workspace_root / relative
        return str(path) if path.exists() else None

    def get_capabilities(self) -> list[AgentCapability]:
        """
        Get list of capabilities for the detected agent.
        
        Returns:
            List of AgentCapability descriptors
        """
        info = self.get_agent_info()
        capabilities = []

        # Core capabilities (universal)
        capabilities.extend([
            AgentCapability(
                name="Universal Gates (U.1-U.7)",
                supported=True,
                description="Core vibe coding discipline gates",
            ),
            AgentCapability(
                name="§X Verification",
                supported=True,
                description="Pre-deliver verification step",
            ),
            AgentCapability(
                name="§Y Feedback Handling",
                supported=True,
                description="Feedback reception protocol",
            ),
        ])

        # Agent-specific capabilities
        capabilities.extend([
            AgentCapability(
                name="Agent-Specific Gates",
                supported=True,
                description=f"{info.gate_prefix}.X gates for {info.name}",
                notes=f"Prefix: {info.gate_prefix}",
            ),
            AgentCapability(
                name="MCP Tools",
                supported=info.supports_mcp,
                description="Model Context Protocol tool support",
                notes="Not available on all agents" if not info.supports_mcp else None,
            ),
            AgentCapability(
                name="Rule Files",
                supported=info.supports_rules,
                description=".rules/*.mdc file support",
                notes="Not available on all agents" if not info.supports_rules else None,
            ),
            AgentCapability(
                name="Skill System",
                supported=info.supports_rules,
                description="Auto-discovery skill loading",
                notes="Requires skills_path configuration" if not info.supports_rules else None,
            ),
        ])

        return capabilities

    def get_gate_prefix(self) -> str:
        """
        Get the gate prefix for the detected agent.
        
        Returns:
            Gate prefix string (e.g., "K", "CX", "C", "G", "U")
        """
        return self.get_agent_info().gate_prefix

    def get_skills_paths(self) -> list[str]:
        """
        Get all possible skills paths for cross-agent compatibility.
        
        Returns:
            List of skills paths from most to least preferred
        """
        paths = []
        
        # Add detected agent's skills path first
        info = self.get_agent_info()
        if info.skills_path:
            paths.append(info.skills_path)
        
        # Add Cursor path as fallback (primary target)
        cursor_path = str(self.workspace_root / ".cursor/skills")
        if cursor_path not in paths:
            paths.append(cursor_path)
        
        # Add Claude Code path
        claude_path = str(self.workspace_root / ".claude/skills")
        if claude_path not in paths:
            paths.append(claude_path)
        
        # Add Grok path
        grok_path = str(self.workspace_root / ".grok/skills")
        if grok_path not in paths:
            paths.append(grok_path)
        
        # Add Codex path (often shared with Cursor)
        codex_path = str(self.workspace_root / ".cursor/skills")
        if codex_path not in paths:
            paths.append(codex_path)

        return paths

    def get_rules_paths(self) -> list[str]:
        """
        Get all possible rules paths for cross-agent compatibility.
        
        Returns:
            List of rules paths from most to least preferred
        """
        paths = []
        
        info = self.get_agent_info()
        if info.rules_path:
            paths.append(info.rules_path)
        
        # Add standard paths
        for agent_dir in [".cursor", ".claude", ".grok"]:
            rules_path = str(self.workspace_root / agent_dir / "rules")
            if rules_path not in paths:
                paths.append(rules_path)

        return paths


class CrossAgentIntegration:
    """
    Unified interface for cross-agent skill and rule compatibility.
    
    Provides a consistent API regardless of which agent is running.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize cross-agent integration.
        
        Args:
            workspace_root: Root directory of the workspace
        """
        self.detector = AgentDetector(workspace_root)
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()

    def get_current_agent(self) -> AgentInfo:
        """Get information about the current agent."""
        return self.detector.get_agent_info()

    def get_compatible_skills(self) -> list[Path]:
        """
        Get all skills compatible with the current agent.
        
        Returns:
            List of Path objects for skill files
        """
        skills_paths = self.detector.get_skills_paths()
        skills = []

        for base_path in skills_paths:
            skills_dir = Path(base_path)
            if skills_dir.exists():
                for skill_file in skills_dir.rglob("SKILL.md"):
                    # Check if skill is compatible with current agent
                    if self._is_skill_compatible(skill_file):
                        skills.append(skill_file)

        return skills

    def _is_skill_compatible(self, skill_path: Path) -> bool:
        """
        Check if a skill is compatible with the current agent.
        
        Args:
            skill_path: Path to the SKILL.md file
            
        Returns:
            True if skill is compatible
        """
        try:
            content = skill_path.read_text(encoding="utf-8")
            
            # Check front matter for compatible_agents
            if "compatible_agents:" in content or "compatible_agents :" in content:
                agent_info = self.detector.get_agent_info()
                # Extract compatible_agents list from front matter
                # This is a simplified check
                if "universal" in content.lower():
                    return True
                if agent_info.agent_type.value in content:
                    return True
            
            # If no compatibility info, assume universal compatibility
            return True
            
        except (OSError, UnicodeDecodeError):
            return False

    def get_skill_gate_prefix(self, skill_path: Path) -> str:
        """
        Get the appropriate gate prefix for a skill.
        
        Args:
            skill_path: Path to the SKILL.md file
            
        Returns:
            Gate prefix (e.g., "K", "CX", "U")
        """
        try:
            content = skill_path.read_text(encoding="utf-8")
            
            # Check for agent-specific gates in skill
            agent_info = self.detector.get_agent_info()
            
            if agent_info.agent_type == AgentType.CURSOR:
                if "K.1" in content or "K.2" in content:
                    return "K"
            elif agent_info.agent_type == AgentType.CODEX:
                if "CX.1" in content or "CX.2" in content:
                    return "CX"
            elif agent_info.agent_type == AgentType.CLAUDE_CODE:
                if "C.1" in content or "C.2" in content:
                    return "C"
            elif agent_info.agent_type == AgentType.GROK:
                if "G.1" in content or "G.2" in content:
                    return "G"
            
            # Default to universal prefix
            return "U"
            
        except (OSError, UnicodeDecodeError):
            return "U"

    def get_cross_agent_config(self) -> dict[str, Any]:
        """
        Get configuration for cross-agent synchronization.
        
        Returns:
            Configuration dictionary
        """
        agent_info = self.get_current_agent()
        
        return {
            "agent": agent_info.agent_type.value,
            "agent_name": agent_info.name,
            "gate_prefix": agent_info.gate_prefix,
            "supports_mcp": agent_info.supports_mcp,
            "supports_rules": agent_info.supports_rules,
            "skills_paths": self.detector.get_skills_paths(),
            "rules_paths": self.detector.get_rules_paths(),
            "workspace_root": str(self.workspace_root),
        }

    def export_sync_manifest(self, output_path: Optional[str] = None) -> dict[str, Any]:
        """
        Export a sync manifest for cross-agent compatibility.
        
        Args:
            output_path: Optional path to save the manifest
            
        Returns:
            Manifest dictionary
        """
        manifest = {
            "version": "1.0.0",
            "generated_at": str(Path(__file__).stat().st_mtime),
            "current_agent": self.get_current_agent().agent_type.value,
            "compatible_agents": [a.value for a in AgentType],
            "skills_paths": self.detector.get_skills_paths(),
            "rules_paths": self.detector.get_rules_paths(),
            "gate_prefixes": {
                "cursor": "K",
                "codex": "CX",
                "claude-code": "C",
                "grok": "G",
                "unknown": "U",
            },
            "universal_gates": ["U.1", "U.2", "U.3", "U.4", "U.5", "U.6", "U.7", "§X", "§Y"],
        }
        
        if output_path:
            import json
            Path(output_path).write_text(
                json.dumps(manifest, indent=2),
                encoding="utf-8"
            )
        
        return manifest


def create_agent_integration(workspace_root: Optional[str] = None) -> CrossAgentIntegration:
    """
    Factory function to create CrossAgentIntegration.
    
    Args:
        workspace_root: Root directory of the workspace
        
    Returns:
        Configured CrossAgentIntegration instance
    """
    return CrossAgentIntegration(workspace_root=workspace_root)
