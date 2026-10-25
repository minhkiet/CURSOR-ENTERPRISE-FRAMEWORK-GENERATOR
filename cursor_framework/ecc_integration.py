"""
ECC (Enhanced Code Copilot) Integration Module

This module provides integration with the ECC framework (https://github.com/affaan-m/ECC),
enabling:
- 68 agents
- 292 skills
- 94 commands
- Hooks and memory system
- AgentShield security scanning
- Multi-harness support (Claude Code, Codex, Cursor, and more)

Supported harnesses:
- Claude Code: Native ecc@ecc plugin
- Codex: Native plugin + legacy sync
- Cursor: Project-local .cursor/ adapter
- Antigravity: Project-local .antigravity/ adapter
- Gemini CLI: Project-local .gemini/ config
- Zed: Project-local .zed/ adapter
- OpenCode: npm build + install
- Qwen CLI: Project-local .qwen/ adapter
- Hermes: Project-local .hermes/ adapter
- OpenClaw: Managed home-directory install
- Kimi Code: Project-local .kimi-code/ install
- CodeBuddy: Project-local .codebuddy/ install
- JoyCode: Project-local .joycode/ install
- GitHub Copilot: .github/copilot-instructions.md

ECC Version: 2.2.2

Usage:
    >>> from cursor_framework.ecc_integration import ECCIntegration
    >>> ecc = ECCIntegration()
    >>> status = ecc.get_status()
    >>> print(f"ECC installed: {status['installed']}")
"""

from __future__ import annotations

import json
import os
import subprocess
import shutil
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
import urllib.request
import zipfile
import tempfile

__version__ = "1.0.0"
__ecc_version__ = "2.2.2"

# ─────────────────────────────────────────────────────────────────────────────
# Types & Enums
# ─────────────────────────────────────────────────────────────────────────────


class HarnessType(Enum):
    """Supported agent harness types."""
    CLAUDE_CODE = "claude"
    CODEX = "codex"
    CURSOR = "cursor"
    ANTIGRAVITY = "antigravity"
    GEMINI = "gemini"
    ZED = "zed"
    OPENCODE = "opencode"
    QWEN = "qwen"
    HERMES = "hermes"
    OPENCLAW = "openclaw"
    KIMI = "kimi"
    CODEBUDDY = "codebuddy"
    JOYCODE = "joycode"
    GITHUB_COPILOT = "copilot"


class InstallProfile(Enum):
    """ECC installation profiles."""
    MINIMAL = "minimal"  # Rules, agents, core skills - no hooks
    CORE = "core"  # Full skills + commands
    FULL = "full"  # Everything including hooks


class InstallStatus(Enum):
    """Installation status for a harness."""
    NOT_INSTALLED = "not_installed"
    PARTIAL = "partial"
    INSTALLED = "installed"
    OUTDATED = "outdated"


# ─────────────────────────────────────────────────────────────────────────────
# Data Classes
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class HarnessInfo:
    """Information about a target harness."""
    type: HarnessType
    name: str
    install_path: str
    config_file: str
    supported_profiles: list[InstallProfile]
    requires_node: bool
    requires_git: bool
    has_hooks: bool
    has_native_plugin: bool
    description: str


@dataclass
class ECCComponent:
    """A component in ECC (skill, agent, rule, etc.)."""
    name: str
    type: str  # skill, agent, rule, command, hook
    path: str
    description: str
    tags: list[str]
    dependencies: list[str] = field(default_factory=list)
    size_bytes: int = 0


@dataclass
class HarnessInstallStatus:
    """Installation status for a specific harness."""
    harness: HarnessType
    status: InstallStatus
    version: Optional[str]
    last_updated: Optional[datetime]
    installed_components: list[str]
    missing_components: list[str]
    profile: Optional[InstallProfile]


@dataclass
class ECCStatus:
    """Overall ECC installation status."""
    installed: bool
    version: Optional[str]
    repository_path: Optional[str]
    available_harnesses: list[HarnessType]
    installed_harnesses: list[HarnessInstallStatus]
    local_components: dict[str, int]  # type -> count
    npm_available: bool
    git_available: bool


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

ECC_REPO_URL = "https://github.com/affaan-m/ECC.git"
ECC_NPM_PACKAGE = "ecc-universal"
ECC_VERSION = "2.2.2"

DEFAULT_INSTALL_PROFILES = {
    InstallProfile.MINIMAL: {
        "agents": True,
        "rules": True,
        "skills": False,
        "commands": False,
        "hooks": False,
        "memory": False,
    },
    InstallProfile.CORE: {
        "agents": True,
        "rules": True,
        "skills": True,
        "commands": True,
        "hooks": False,
        "memory": True,
    },
    InstallProfile.FULL: {
        "agents": True,
        "rules": True,
        "skills": True,
        "commands": True,
        "hooks": True,
        "memory": True,
    },
}

HARNESS_INFO: dict[HarnessType, HarnessInfo] = {
    HarnessType.CLAUDE_CODE: HarnessInfo(
        type=HarnessType.CLAUDE_CODE,
        name="Claude Code",
        install_path="~/.claude",
        config_file="~/.claude/settings.json",
        supported_profiles=[InstallProfile.MINIMAL, InstallProfile.CORE, InstallProfile.FULL],
        requires_node=True,
        requires_git=True,
        has_hooks=True,
        has_native_plugin=True,
        description="Native Claude Code plugin ecc@ecc with full hooks support",
    ),
    HarnessType.CODEX: HarnessInfo(
        type=HarnessType.CODEX,
        name="Codex",
        install_path="~/.codex",
        config_file="~/.codex/config.toml",
        supported_profiles=[InstallProfile.MINIMAL, InstallProfile.CORE],
        requires_node=True,
        requires_git=True,
        has_hooks=True,
        has_native_plugin=True,
        description="Codex native plugin or legacy sync to ~/.codex",
    ),
    HarnessType.CURSOR: HarnessInfo(
        type=HarnessType.CURSOR,
        name="Cursor",
        install_path=".cursor",
        config_file=".cursor/settings.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Cursor adapter",
    ),
    HarnessType.ANTIGRAVITY: HarnessInfo(
        type=HarnessType.ANTIGRAVITY,
        name="Antigravity",
        install_path=".antigravity",
        config_file=".antigravity/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Antigravity adapter",
    ),
    HarnessType.GEMINI: HarnessInfo(
        type=HarnessType.GEMINI,
        name="Gemini CLI",
        install_path=".gemini",
        config_file=".gemini/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Gemini CLI config",
    ),
    HarnessType.ZED: HarnessInfo(
        type=HarnessType.ZED,
        name="Zed",
        install_path=".zed",
        config_file=".zed/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Zed adapter",
    ),
    HarnessType.OPENCODE: HarnessInfo(
        type=HarnessType.OPENCODE,
        name="OpenCode",
        install_path=".opencode",
        config_file=".opencode/config.json",
        supported_profiles=[InstallProfile.MINIMAL, InstallProfile.CORE, InstallProfile.FULL],
        requires_node=True,
        requires_git=True,
        has_hooks=True,
        has_native_plugin=False,
        description="npm build required before install",
    ),
    HarnessType.QWEN: HarnessInfo(
        type=HarnessType.QWEN,
        name="Qwen CLI",
        install_path=".qwen",
        config_file=".qwen/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Qwen CLI adapter",
    ),
    HarnessType.HERMES: HarnessInfo(
        type=HarnessType.HERMES,
        name="Hermes",
        install_path=".hermes",
        config_file=".hermes/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Hermes adapter",
    ),
    HarnessType.OPENCLAW: HarnessInfo(
        type=HarnessType.OPENCLAW,
        name="OpenClaw",
        install_path="~/.openclaw",
        config_file="~/.openclaw/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Managed home-directory install",
    ),
    HarnessType.KIMI: HarnessInfo(
        type=HarnessType.KIMI,
        name="Kimi Code",
        install_path=".kimi-code",
        config_file=".kimi-code/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=True,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local Kimi Code install",
    ),
    HarnessType.CODEBUDDY: HarnessInfo(
        type=HarnessType.CODEBUDDY,
        name="CodeBuddy",
        install_path=".codebuddy",
        config_file=".codebuddy/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local CodeBuddy adapter",
    ),
    HarnessType.JOYCODE: HarnessInfo(
        type=HarnessType.JOYCODE,
        name="JoyCode",
        install_path=".joycode",
        config_file=".joycode/config.json",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=True,
        has_hooks=False,
        has_native_plugin=False,
        description="Project-local JoyCode adapter",
    ),
    HarnessType.GITHUB_COPILOT: HarnessInfo(
        type=HarnessType.GITHUB_COPILOT,
        name="GitHub Copilot",
        install_path=".github",
        config_file=".github/copilot-instructions.md",
        supported_profiles=[InstallProfile.MINIMAL],
        requires_node=False,
        requires_git=False,
        has_hooks=False,
        has_native_plugin=False,
        description="Copilot instruction file in .github/",
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# ECC Integration Class
# ─────────────────────────────────────────────────────────────────────────────


class ECCIntegration:
    """
    Main integration class for ECC (Enhanced Code Copilot).
    
    Provides:
    - Repository management (clone, update, checkout)
    - Component discovery (skills, agents, rules, commands, hooks)
    - Multi-harness installation
    - Installation status checking
    - Profile management
    
    Usage:
        >>> ecc = ECCIntegration()
        >>> status = ecc.get_status()
        >>> print(f"ECC version: {status['version']}")
        >>> 
        >>> # Install for Claude Code
        >>> result = ecc.install_harness(HarnessType.CLAUDE_CODE, InstallProfile.CORE)
        >>> print(f"Installed: {result['success']}")
    """

    def __init__(
        self,
        workspace_path: Optional[str] = None,
        cache_path: Optional[str] = None,
    ):
        """
        Initialize ECC integration.
        
        Args:
            workspace_path: Path to workspace (default: current directory)
            cache_path: Path for cached data (default: ~/.cache/cursor-ecc)
        """
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.cache_path = Path(cache_path) if cache_path else Path.home() / ".cache" / "cursor-ecc"
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # State
        self._repo_path: Optional[Path] = None
        self._components: Optional[dict[str, list[ECCComponent]]] = None
        
    # ─────────────────────────────────────────────────────────────────────────
    # Utility Methods
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def check_node() -> bool:
        """Check if Node.js is available."""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @staticmethod
    def check_git() -> bool:
        """Check if Git is available."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @staticmethod
    def get_node_version() -> Optional[str]:
        """Get Node.js version."""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return None

    def _resolve_path(self, path: str) -> Path:
        """Resolve ~ and relative paths."""
        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = self.workspace_path / path
        return Path(path)

    def _ensure_git_repo(self) -> Optional[Path]:
        """Ensure ECC repository is cloned."""
        if self._repo_path and self._repo_path.exists():
            return self._repo_path
            
        # Check for existing clone
        default_clone = self.cache_path / "ecc"
        if default_clone.exists():
            self._repo_path = default_clone
            return default_clone
            
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # Repository Management
    # ─────────────────────────────────────────────────────────────────────────
    
    def clone_repository(
        self,
        target_path: Optional[str] = None,
        branch: str = "main",
        shallow: bool = False,
    ) -> dict[str, Any]:
        """
        Clone the ECC repository.
        
        Args:
            target_path: Where to clone (default: ~/.cache/cursor-ecc/ecc)
            branch: Branch to checkout (default: main)
            shallow: Use shallow clone (default: False)
            
        Returns:
            dict with success status and details
        """
        if not self.check_git():
            return {
                "success": False,
                "error": "Git is not available",
                "requires": ["git"],
            }
            
        target = Path(target_path) if target_path else self.cache_path / "ecc"
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if already cloned
        if target.exists():
            return {
                "success": True,
                "already_exists": True,
                "path": str(target),
                "version": self._get_repo_version(target),
            }
        
        try:
            cmd = ["git", "clone"]
            if shallow:
                cmd.extend(["--depth", "1"])
            cmd.extend(["--branch", branch, ECC_REPO_URL, str(target)])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 min timeout
            )
            
            if result.returncode == 0:
                self._repo_path = target
                return {
                    "success": True,
                    "path": str(target),
                    "version": self._get_repo_version(target),
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Clone timed out after 5 minutes",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def update_repository(self, target_path: Optional[str] = None) -> dict[str, Any]:
        """
        Update the ECC repository to latest.
        
        Args:
            target_path: Path to ECC repo (default: cached repo)
            
        Returns:
            dict with success status and details
        """
        repo_path = Path(target_path) if target_path else self._ensure_git_repo()
        if not repo_path or not repo_path.exists():
            return {
                "success": False,
                "error": "Repository not found. Call clone_repository first.",
            }
            
        try:
            # Fetch and checkout main
            subprocess.run(
                ["git", "fetch", "origin"],
                cwd=repo_path,
                capture_output=True,
                timeout=60,
            )
            subprocess.run(
                ["git", "checkout", "main"],
                cwd=repo_path,
                capture_output=True,
                timeout=30,
            )
            subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=repo_path,
                capture_output=True,
                timeout=60,
            )
            
            return {
                "success": True,
                "path": str(repo_path),
                "version": self._get_repo_version(repo_path),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def _get_repo_version(self, repo_path: Path) -> Optional[str]:
        """Get version from package.json or git describe."""
        pkg_file = repo_path / "package.json"
        if pkg_file.exists():
            try:
                pkg = json.loads(pkg_file.read_text())
                return pkg.get("version", ECC_VERSION)
            except Exception:
                pass
        
        # Fall back to git
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
            
        return ECC_VERSION

    # ─────────────────────────────────────────────────────────────────────────
    # Component Discovery
    # ─────────────────────────────────────────────────────────────────────────
    
    def discover_components(self, repo_path: Optional[str] = None) -> dict[str, list[ECCComponent]]:
        """
        Discover all ECC components from the repository.
        
        Args:
            repo_path: Path to ECC repo
            
        Returns:
            dict mapping component type to list of components
        """
        ecc_path = Path(repo_path) if repo_path else self._ensure_git_repo()
        if not ecc_path or not ecc_path.exists():
            return {}
            
        if self._components:
            return self._components
            
        components: dict[str, list[ECCComponent]] = {
            "agents": [],
            "skills": [],
            "rules": [],
            "commands": [],
            "hooks": [],
            "scripts": [],
        }
        
        # Discover agents
        agents_dir = ecc_path / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                components["agents"].append(self._read_component(agent_file, "agent"))
                
        # Discover skills
        skills_dir = ecc_path / ".agents" / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        components["skills"].append(self._read_component(skill_md, "skill"))
                        
        # Discover rules
        rules_dir = ecc_path / "rules"
        if rules_dir.exists():
            for rule_file in rules_dir.rglob("*.md"):
                if rule_file.is_file():
                    components["rules"].append(self._read_component(rule_file, "rule"))
                    
        # Discover commands
        commands_dir = ecc_path / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                components["commands"].append(self._read_component(cmd_file, "command"))
                
        # Discover hooks
        hooks_dir = ecc_path / "hooks"
        if hooks_dir.exists():
            for hook_file in hooks_dir.rglob("*.js"):
                if hook_file.is_file():
                    components["hooks"].append(self._read_component(hook_file, "hook"))
                    
        # Discover scripts
        scripts_dir = ecc_path / "scripts"
        if scripts_dir.exists():
            for script_file in scripts_dir.glob("*.js"):
                components["scripts"].append(self._read_component(script_file, "script"))
                
        self._components = components
        return components

    def _read_component(self, file_path: Path, component_type: str) -> ECCComponent:
        """Read a component file and extract metadata."""
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        
        name = file_path.stem
        description = ""
        tags = []
        dependencies = []
        
        # Try to extract frontmatter or first description
        lines = content.split("\n")
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line.startswith("# ") and not description:
                description = line[2:].strip()
            elif any(line.startswith(f"{tag}:") for tag in ["tags", "keywords"]):
                tags_str = line.split(":", 1)[1].strip()
                tags = [t.strip() for t in tags_str.replace("[", "").replace("]", "").split(",")]
                
        return ECCComponent(
            name=name,
            type=component_type,
            path=str(file_path.relative_to(file_path.parent.parent)),
            description=description,
            tags=tags,
            dependencies=dependencies,
            size_bytes=len(content.encode("utf-8")),
        )

    def get_component_summary(self) -> dict[str, int]:
        """Get count of each component type."""
        if not self._components:
            self.discover_components()
            
        if not self._components:
            return {}
            
        return {k: len(v) for k, v in self._components.items()}

    # ─────────────────────────────────────────────────────────────────────────
    # Harness Installation
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_install_status(
        self,
        harness: HarnessType,
        base_path: Optional[str] = None,
    ) -> HarnessInstallStatus:
        """
        Get installation status for a harness.
        
        Args:
            harness: The harness to check
            base_path: Base path for project-local installs
            
        Returns:
            HarnessInstallStatus with current state
        """
        info = HARNESS_INFO.get(harness)
        if not info:
            return HarnessInstallStatus(
                harness=harness,
                status=InstallStatus.NOT_INSTALLED,
                version=None,
                last_updated=None,
                installed_components=[],
                missing_components=[],
                profile=None,
            )
            
        install_path = self._resolve_path(info.install_path)
        if not base_path and not info.install_path.startswith("."):
            base_path = str(Path.home())
            
        if base_path:
            install_path = Path(base_path) / info.install_path.replace("~/.", "")
            install_path = self._resolve_path(str(install_path))
            
        # Check what's installed
        installed = []
        missing = []
        
        # Check agents
        agents_dir = install_path / "agents"
        if agents_dir.exists():
            installed.extend([f.stem for f in agents_dir.glob("*.md")])
            
        # Check skills
        skills_dir = install_path / "skills"
        if skills_dir.exists():
            installed.extend([d.name for d in skills_dir.iterdir() if d.is_dir()])
            
        # Check rules
        rules_dir = install_path / "rules"
        if rules_dir.exists():
            installed.extend(["rules"])
            
        # Check for ECC marker
        marker_file = install_path / ".ecc-installed"
        if marker_file.exists():
            try:
                marker_data = json.loads(marker_file.read_text())
                return HarnessInstallStatus(
                    harness=harness,
                    status=InstallStatus.INSTALLED,
                    version=marker_data.get("version"),
                    last_updated=datetime.fromisoformat(marker_data.get("updated", "")),
                    installed_components=installed,
                    missing_components=missing,
                    profile=InstallProfile(marker_data.get("profile", "minimal")),
                )
            except Exception:
                pass
                
        if installed:
            return HarnessInstallStatus(
                harness=harness,
                status=InstallStatus.PARTIAL,
                version=None,
                last_updated=None,
                installed_components=installed,
                missing_components=missing,
                profile=None,
            )
            
        return HarnessInstallStatus(
            harness=harness,
            status=InstallStatus.NOT_INSTALLED,
            version=None,
            last_updated=None,
            installed_components=[],
            missing_components=[],
            profile=None,
        )

    def install_harness(
        self,
        harness: HarnessType,
        profile: InstallProfile = InstallProfile.CORE,
        base_path: Optional[str] = None,
        repo_path: Optional[str] = None,
        enable_hooks: bool = False,
    ) -> dict[str, Any]:
        """
        Install ECC components for a specific harness.
        
        Args:
            harness: Target harness type
            profile: Installation profile (minimal, core, full)
            base_path: Base path for project-local installs
            repo_path: Path to ECC repository
            enable_hooks: Enable hooks runtime (if supported)
            
        Returns:
            dict with success status and details
        """
        info = HARNESS_INFO.get(harness)
        if not info:
            return {
                "success": False,
                "error": f"Unknown harness: {harness}",
            }
            
        if profile not in info.supported_profiles:
            return {
                "success": False,
                "error": f"Profile {profile.value} not supported for {harness.value}. "
                        f"Supported: {[p.value for p in info.supported_profiles]}",
            }
            
        # Ensure repo exists
        ecc_path = Path(repo_path) if repo_path else self._ensure_git_repo()
        if not ecc_path or not ecc_path.exists():
            clone_result = self.clone_repository()
            if not clone_result["success"]:
                return clone_result
            ecc_path = Path(clone_result["path"])
            
        # Resolve install path
        if info.install_path.startswith("~"):
            install_path = self._resolve_path(info.install_path)
        elif base_path:
            rel_path = info.install_path.lstrip("./")
            install_path = Path(base_path) / rel_path
        else:
            install_path = self.workspace_path / info.install_path
            
        install_path.mkdir(parents=True, exist_ok=True)
        
        # Get profile config
        profile_config = DEFAULT_INSTALL_PROFILES.get(profile, {})
        
        try:
            installed = []
            
            # Install agents
            if profile_config.get("agents", True):
                src_agents = ecc_path / "agents"
                dst_agents = install_path / "agents"
                if src_agents.exists():
                    dst_agents.mkdir(parents=True, exist_ok=True)
                    for agent_file in src_agents.glob("*.md"):
                        shutil.copy2(agent_file, dst_agents / agent_file.name)
                        installed.append(f"agent:{agent_file.stem}")
                        
            # Install rules
            if profile_config.get("rules", True):
                src_rules = ecc_path / "rules"
                dst_rules = install_path / "rules"
                if src_rules.exists():
                    dst_rules.mkdir(parents=True, exist_ok=True)
                    # Copy common rules + optionally language-specific
                    for rule_dir in src_rules.iterdir():
                        if rule_dir.is_dir() or rule_dir.suffix in [".md", ".mdc"]:
                            dest = dst_rules / rule_dir.name
                            if rule_dir.is_dir():
                                shutil.copytree(rule_dir, dest, dirs_exist_ok=True)
                            else:
                                shutil.copy2(rule_dir, dest)
                            installed.append(f"rule:{rule_dir.stem}")
                            
            # Install skills
            if profile_config.get("skills", True):
                src_skills = ecc_path / ".agents" / "skills"
                dst_skills = install_path / "skills"
                if src_skills.exists():
                    dst_skills.mkdir(parents=True, exist_ok=True)
                    for skill_dir in src_skills.iterdir():
                        if skill_dir.is_dir():
                            dest = dst_skills / skill_dir.name
                            shutil.copytree(skill_dir, dest, dirs_exist_ok=True)
                            installed.append(f"skill:{skill_dir.name}")
                            
            # Install commands
            if profile_config.get("commands", True):
                src_cmds = ecc_path / "commands"
                dst_cmds = install_path / "commands"
                if src_cmds.exists():
                    dst_cmds.mkdir(parents=True, exist_ok=True)
                    for cmd_file in src_cmds.glob("*.md"):
                        shutil.copy2(cmd_file, dst_cmds / cmd_file.name)
                        installed.append(f"command:{cmd_file.stem}")
                        
            # Install hooks (if supported and enabled)
            if profile_config.get("hooks", True) and enable_hooks and info.has_hooks:
                src_hooks = ecc_path / "hooks"
                dst_hooks = install_path / "hooks"
                if src_hooks.exists():
                    dst_hooks.mkdir(parents=True, exist_ok=True)
                    for hook_file in src_hooks.rglob("*"):
                        if hook_file.is_file():
                            rel_path = hook_file.relative_to(src_hooks)
                            dest = dst_hooks / rel_path
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(hook_file, dest)
                    installed.append("hooks")
                    
            # Write marker
            marker_data = {
                "version": ECC_VERSION,
                "profile": profile.value,
                "harness": harness.value,
                "updated": datetime.now().isoformat(),
                "installed": installed,
            }
            (install_path / ".ecc-installed").write_text(json.dumps(marker_data, indent=2))
            
            return {
                "success": True,
                "harness": harness.value,
                "profile": profile.value,
                "path": str(install_path),
                "installed_count": len(installed),
                "installed": installed,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "harness": harness.value,
            }

    def uninstall_harness(
        self,
        harness: HarnessType,
        base_path: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Uninstall ECC from a harness.
        
        Args:
            harness: Target harness
            base_path: Base path for project-local installs
            
        Returns:
            dict with success status
        """
        info = HARNESS_INFO.get(harness)
        if not info:
            return {"success": False, "error": f"Unknown harness: {harness}"}
            
        if info.install_path.startswith("~"):
            install_path = self._resolve_path(info.install_path)
        elif base_path:
            rel_path = info.install_path.lstrip("./")
            install_path = Path(base_path) / rel_path
        else:
            install_path = self.workspace_path / info.install_path
            
        if not install_path.exists():
            return {"success": True, "message": "Already uninstalled"}
            
        try:
            # Remove marker
            marker = install_path / ".ecc-installed"
            if marker.exists():
                marker.unlink()
                
            # Remove components (optional - could preserve user modifications)
            # For now, just remove the marker
                
            return {
                "success": True,
                "path": str(install_path),
                "message": "ECC marker removed. Components may remain.",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ─────────────────────────────────────────────────────────────────────────
    # Status & Info
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_status(self) -> ECCStatus:
        """
        Get overall ECC status.
        
        Returns:
            ECCStatus with all relevant information
        """
        repo = self._ensure_git_repo()
        repo_path = str(repo) if repo else None
        
        # Get component summary
        if repo:
            self.discover_components(repo_path)
        components = self.get_component_summary()
        
        # Check each harness
        installed_harnesses = []
        for harness_type in HarnessType:
            status = self.get_install_status(harness_type)
            if status.status != InstallStatus.NOT_INSTALLED:
                installed_harnesses.append(status)
                
        return ECCStatus(
            installed=repo is not None,
            version=self._get_repo_version(repo) if repo else None,
            repository_path=repo_path,
            available_harnesses=list(HarnessType),
            installed_harnesses=installed_harnesses,
            local_components=components,
            npm_available=self.check_node(),
            git_available=self.check_git(),
        )

    def get_supported_harnesses(self) -> list[HarnessInfo]:
        """Get list of supported harnesses."""
        return list(HARNESS_INFO.values())

    def get_harness_info(self, harness: HarnessType) -> Optional[HarnessInfo]:
        """Get info for a specific harness."""
        return HARNESS_INFO.get(harness)

    # ─────────────────────────────────────────────────────────────────────────
    # NPM-based Installation (for Claude Code, Codex)
    # ─────────────────────────────────────────────────────────────────────────
    
    def install_via_npm(
        self,
        harness: HarnessType,
        profile: InstallProfile = InstallProfile.CORE,
        scope: str = "user",  # user, project, local
        enable_hooks: bool = True,
    ) -> dict[str, Any]:
        """
        Install ECC using npm for Claude Code or Codex.
        
        Args:
            harness: Target harness (must be Claude Code or Codex)
            profile: Installation profile
            scope: Install scope (user/project/local)
            enable_hooks: Enable hooks runtime
            
        Returns:
            dict with success status
        """
        if harness not in [HarnessType.CLAUDE_CODE, HarnessType.CODEX]:
            return {
                "success": False,
                "error": f"NPM install only supported for Claude Code and Codex, not {harness.value}",
            }
            
        if not self.check_node():
            return {
                "success": False,
                "error": "Node.js is required for npm-based installation",
                "requires": ["node"],
            }
            
        # Build install command
        cmd = [
            "npx", f"ecc-universal@{ECC_VERSION}",
            "install",
            "--profile", profile.value,
            "--target", harness.value,
        ]
        
        if scope != "user":
            cmd.extend(["--scope", scope])
            
        if enable_hooks:
            cmd.append("--enable-hooks")
            
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 min timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "harness": harness.value,
                    "profile": profile.value,
                    "scope": scope,
                    "output": result.stdout,
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "stdout": result.stdout,
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Installation timed out after 5 minutes",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    # ─────────────────────────────────────────────────────────────────────────
    # Export & Import
    # ─────────────────────────────────────────────────────────────────────────
    
    def export_manifest(self, repo_path: Optional[str] = None) -> dict[str, Any]:
        """
        Export ECC manifest for debugging/sharing.
        
        Args:
            repo_path: Path to ECC repository
            
        Returns:
            dict with full manifest
        """
        if repo_path:
            self.discover_components(repo_path)
        else:
            self.discover_components()
            
        status = self.get_status()
        
        return {
            "version": ECC_VERSION,
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "path": status.repository_path,
                "installed": status.installed,
                "version": status.version,
            },
            "harnesses": {
                "available": [h.value for h in status.available_harnesses],
                "installed": [
                    {
                        "type": s.harness.value,
                        "status": s.status.value,
                        "version": s.version,
                        "profile": s.profile.value if s.profile else None,
                    }
                    for s in status.installed_harnesses
                ],
            },
            "components": {
                "agents": len(self._components.get("agents", [])) if self._components else 0,
                "skills": len(self._components.get("skills", [])) if self._components else 0,
                "rules": len(self._components.get("rules", [])) if self._components else 0,
                "commands": len(self._components.get("commands", [])) if self._components else 0,
                "hooks": len(self._components.get("hooks", [])) if self._components else 0,
            },
            "requirements": {
                "node_available": status.npm_available,
                "git_available": status.git_available,
                "node_version": self.get_node_version(),
            },
        }


# ─────────────────────────────────────────────────────────────────────────────
# Factory Functions
# ─────────────────────────────────────────────────────────────────────────────


def create_ecc_integration(
    workspace_path: Optional[str] = None,
    cache_path: Optional[str] = None,
) -> ECCIntegration:
    """
    Create an ECCIntegration instance.
    
    Args:
        workspace_path: Path to workspace
        cache_path: Path for cached data
        
    Returns:
        Configured ECCIntegration instance
    """
    return ECCIntegration(
        workspace_path=workspace_path,
        cache_path=cache_path,
    )


# ─────────────────────────────────────────────────────────────────────────────
# CLI Helpers
# ─────────────────────────────────────────────────────────────────────────────


def run_ecc_setup(
    harness: str = "claude",
    profile: str = "core",
    guided: bool = True,
) -> dict[str, Any]:
    """
    Run ECC setup via npx.
    
    Args:
        harness: Target harness
        profile: Installation profile
        guided: Use guided setup
        
    Returns:
        dict with results
    """
    ecc = ECCIntegration()
    
    harness_type = HarnessType(harness.lower())
    
    if harness_type in [HarnessType.CLAUDE_CODE, HarnessType.CODEX]:
        return ecc.install_via_npm(
            harness=harness_type,
            profile=InstallProfile(profile.lower()),
        )
    else:
        return ecc.install_harness(
            harness=harness_type,
            profile=InstallProfile(profile.lower()),
        )
