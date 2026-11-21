"""
Vibe Sync Module — Multi-Tool Vibe Coding Synchronization Engine.

Enables seamless cross-tool compatibility across modern AI coding environments:
- Cursor IDE (.cursor/, .cursorrules)
- Windsurf / Cascade (.windsurf/, .windsurfrules)
- Claude Code (CLAUDE.md, .claude/skills/)
- Google Antigravity / Gemini CLI (.gemini/, .agents/skills/)
- Cline (.clinerules, .cline/)
- Roo Code (.roorules, .roomodes)
- GitHub Copilot (.github/copilot-instructions.md)
- Aider (.aider.conf.yml, .aider.conventions.md)
- Codex / Universal (AGENTS.md, .codex/)

Provides:
- Tool detection across environment variables and directory markers
- Native configuration and instruction generation for each tool
- Universal quality gate synchronization (U.1-U.7, §X, §Y)
- Verification and audit of workspace configuration integrity
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class VibeTool(str, Enum):
    """Supported vibe coding tools."""
    CURSOR = "cursor"
    WINDSURF = "windsurf"
    CLAUDE_CODE = "claude-code"
    ANTIGRAVITY = "antigravity"
    CLINE = "cline"
    ROO_CODE = "roo"
    COPILOT = "copilot"
    AIDER = "aider"
    CODEX = "codex"


@dataclass
class ToolSpec:
    """Specification of a vibe coding tool's configuration layout."""
    tool: VibeTool
    display_name: str
    primary_config: str
    rules_dir: Optional[str]
    skills_dir: Optional[str]
    gate_prefix: str
    env_vars: list[str] = field(default_factory=list)
    dir_markers: list[str] = field(default_factory=list)
    plugins_dir: Optional[str] = None
    global_plugins_dir: Optional[str] = None
    supports_vscode_plugins: bool = False


_VSCODE_MANIFEST_KEYS = frozenset({"activationEvents", "main", "contributes"})


def _detect_plugin_format(manifest_path: Path) -> str:
    """Classify a plugin bundle from its manifest, without loading its code."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "generic"
    if isinstance(manifest, dict) and _VSCODE_MANIFEST_KEYS.intersection(manifest):
        return "vscode"
    return "generic"


TOOL_SPECS: dict[VibeTool, ToolSpec] = {
    VibeTool.CURSOR: ToolSpec(
        tool=VibeTool.CURSOR,
        display_name="Cursor IDE",
        primary_config=".cursorrules",
        rules_dir=".cursor/rules",
        skills_dir=".cursor/skills",
        gate_prefix="K",
        env_vars=["CURSOR_IDE", "CURSOR_PROJECT"],
        dir_markers=[".cursor"],
        plugins_dir=".cursor/plugins",
        global_plugins_dir=".cursor/extensions",
        supports_vscode_plugins=True,
    ),
    VibeTool.WINDSURF: ToolSpec(
        tool=VibeTool.WINDSURF,
        display_name="Windsurf / Cascade",
        primary_config=".windsurfrules",
        rules_dir=".windsurf/rules",
        skills_dir=".windsurf/skills",
        gate_prefix="W",
        env_vars=["WINDSURF_IDE", "WINDSURF_WORKSPACE_ROOT", "CODEIUM_API_KEY"],
        dir_markers=[".windsurf"],
        plugins_dir=".windsurf/plugins",
        global_plugins_dir=".windsurf/extensions",
        supports_vscode_plugins=True,
    ),
    VibeTool.CLAUDE_CODE: ToolSpec(
        tool=VibeTool.CLAUDE_CODE,
        display_name="Claude Code",
        primary_config="CLAUDE.md",
        rules_dir=".claude/rules",
        skills_dir=".claude/skills",
        gate_prefix="C",
        env_vars=["CLAUDE_IDE", "CLAUDE_API_KEY", "CLAUDE_PROJECT_DIR"],
        dir_markers=[".claude"],
        plugins_dir=".claude/plugins",
        global_plugins_dir=".claude/plugins",
    ),
    VibeTool.ANTIGRAVITY: ToolSpec(
        tool=VibeTool.ANTIGRAVITY,
        display_name="Google Antigravity / Gemini CLI",
        primary_config=".gemini/config.json",
        rules_dir=".gemini/rules",
        skills_dir=".agents/skills",
        gate_prefix="AG",
        env_vars=["ANTIGRAVITY_APP_DATA", "ANTIGRAVITY_WORKSPACE_ROOT", "ANTIGRAVITY_CLI", "GEMINI_CLI"],
        dir_markers=[".gemini", ".agents"],
        plugins_dir=".agents/plugins",
        global_plugins_dir=".gemini/antigravity/plugins",
    ),
    VibeTool.CLINE: ToolSpec(
        tool=VibeTool.CLINE,
        display_name="Cline",
        primary_config=".clinerules",
        rules_dir=".cline/rules",
        skills_dir=".cline/skills",
        gate_prefix="CL",
        env_vars=["CLINE_ACTIVE", "CLINE_VERSION"],
        dir_markers=[".cline"],
        plugins_dir=".cline/plugins",
        global_plugins_dir=".cline/plugins",
        supports_vscode_plugins=True,
    ),
    VibeTool.ROO_CODE: ToolSpec(
        tool=VibeTool.ROO_CODE,
        display_name="Roo Code",
        primary_config=".roorules",
        rules_dir=".roo/rules",
        skills_dir=".roo/skills",
        gate_prefix="R",
        env_vars=["ROO_ACTIVE", "ROO_CODE_VERSION"],
        dir_markers=[".roo"],
        plugins_dir=".roo/plugins",
        global_plugins_dir=".roo/plugins",
        supports_vscode_plugins=True,
    ),
    VibeTool.COPILOT: ToolSpec(
        tool=VibeTool.COPILOT,
        display_name="GitHub Copilot",
        primary_config=".github/copilot-instructions.md",
        rules_dir=".github/rules",
        skills_dir=None,
        gate_prefix="CP",
        env_vars=["COPILOT_AGENT", "GITHUB_COPILOT"],
        dir_markers=[".github"],
        plugins_dir=".github/plugins",
        global_plugins_dir=".github/plugins",
    ),
    VibeTool.AIDER: ToolSpec(
        tool=VibeTool.AIDER,
        display_name="Aider",
        primary_config=".aider.conventions.md",
        rules_dir=None,
        skills_dir=None,
        gate_prefix="AI",
        env_vars=["AIDER_ENV"],
        dir_markers=[".aider.conf.yml"],
        plugins_dir=None,
        global_plugins_dir=None,
    ),
    VibeTool.CODEX: ToolSpec(
        tool=VibeTool.CODEX,
        display_name="Codex",
        primary_config="AGENTS.md",
        rules_dir=".codex/rules",
        skills_dir=".codex/skills",
        gate_prefix="CX",
        env_vars=["CODEX_ENABLED", "ORIGIN_HOST", "CODEX_WORKSPACE_ROOT"],
        dir_markers=[".codex"],
        plugins_dir=".codex/plugins",
        global_plugins_dir=".codex/plugins",
    ),
}

DEFAULT_SYNC_TOOLS = (
    VibeTool.CODEX,
    VibeTool.CLAUDE_CODE,
    VibeTool.CURSOR,
    VibeTool.WINDSURF,
    VibeTool.ANTIGRAVITY,
)

DEFAULT_PLUGIN_TOOLS = (
    VibeTool.CURSOR,
    VibeTool.WINDSURF,
    VibeTool.CLAUDE_CODE,
    VibeTool.ANTIGRAVITY,
    VibeTool.CLINE,
    VibeTool.ROO_CODE,
    VibeTool.CODEX,
)


@dataclass
class ToolDetectionResult:
    """Detection status for a vibe coding tool."""
    tool: VibeTool
    display_name: str
    detected: bool
    reasons: list[str] = field(default_factory=list)
    config_exists: bool = False
    rules_dir_exists: bool = False
    skills_dir_exists: bool = False


@dataclass
class SyncFileRecord:
    """Record of a created or updated tool configuration file."""
    tool: VibeTool
    file_path: Path
    action: str  # "created", "updated", "skipped", "would_create", "would_update"
    description: str


@dataclass
class VibeSyncReport:
    """Summary report of vibe synchronization."""
    workspace_root: Path
    tools_detected: list[VibeTool]
    synced_tools: list[VibeTool]
    files_modified: list[SyncFileRecord]
    dry_run: bool
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace_root": str(self.workspace_root),
            "tools_detected": [t.value for t in self.tools_detected],
            "synced_tools": [t.value for t in self.synced_tools],
            "files_modified": [
                {
                    "tool": r.tool.value,
                    "file_path": str(r.file_path),
                    "action": r.action,
                    "description": r.description,
                }
                for r in self.files_modified
            ],
            "dry_run": self.dry_run,
            "errors": self.errors,
        }


class VibeDetector:
    """Detects active and installed vibe coding tools in a workspace."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()

    def detect_all(self) -> list[ToolDetectionResult]:
        """Detect status for all supported vibe tools."""
        results = []
        for tool, spec in TOOL_SPECS.items():
            results.append(self.detect_tool(tool))
        return results

    def detect_active_tools(self) -> list[VibeTool]:
        """Return list of tools currently active or present in the workspace."""
        active = []
        for result in self.detect_all():
            if result.detected:
                active.append(result.tool)
        return active

    def detect_runtime_tools(self) -> list[VibeTool]:
        """Return tools with a runtime signal, not merely an adapter folder.

        Adapter folders such as ``.cursor/`` or ``.claude/`` also exist in
        framework repositories that merely ship sync payloads. Only explicit
        environment markers and native primary configs identify a live tool.
        """
        runtime: list[VibeTool] = []
        for tool, spec in TOOL_SPECS.items():
            env_active = any(os.getenv(var) for var in spec.env_vars)
            config_active = (self.workspace_root / spec.primary_config).exists()
            if env_active or config_active:
                runtime.append(tool)
        return runtime

    def detect_tool(self, tool: VibeTool) -> ToolDetectionResult:
        """Inspect workspace and environment for a specific tool."""
        spec = TOOL_SPECS[tool]
        reasons = []

        # 1. Check environment variables
        for var in spec.env_vars:
            if os.getenv(var):
                reasons.append(f"Environment variable '{var}' is set")

        # 2. Check directory markers
        for marker in spec.dir_markers:
            target = self.workspace_root / marker
            if target.exists():
                reasons.append(f"Directory/file marker '{marker}' exists")

        # 3. Check primary config
        primary_cfg = self.workspace_root / spec.primary_config
        config_exists = primary_cfg.exists()
        if config_exists:
            reasons.append(f"Primary configuration '{spec.primary_config}' exists")

        # 4. Check rules/skills dirs
        rules_dir_exists = False
        if spec.rules_dir:
            rules_dir_exists = (self.workspace_root / spec.rules_dir).exists()
            if rules_dir_exists:
                reasons.append(f"Rules directory '{spec.rules_dir}' exists")

        skills_dir_exists = False
        if spec.skills_dir:
            skills_dir_exists = (self.workspace_root / spec.skills_dir).exists()
            if skills_dir_exists:
                reasons.append(f"Skills directory '{spec.skills_dir}' exists")

        detected = len(reasons) > 0
        return ToolDetectionResult(
            tool=tool,
            display_name=spec.display_name,
            detected=detected,
            reasons=reasons,
            config_exists=config_exists,
            rules_dir_exists=rules_dir_exists,
            skills_dir_exists=skills_dir_exists,
        )


class VibeSyncEngine:
    """
    Synchronizes skills, rules, and quality gates across vibe coding tools.
    Generates tool-native instruction files so AI agents work consistently.
    """

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()
        self.detector = VibeDetector(self.workspace_root)

    def generate_unified_instructions(self, tool: VibeTool) -> str:
        """Generate high-signal, anti-slop rules tailored for the specific tool."""
        spec = TOOL_SPECS[tool]
        prefix = spec.gate_prefix

        lines = [
            f"# Vibe Enterprise Framework — {spec.display_name} Instructions",
            "",
            "> Production-grade coding discipline, quality gates, and surgical implementation rules.",
            "",
            "## 1. Core Engineering Principles",
            "- **Think Before Coding**: State assumptions and identify the simplest path before touching code.",
            "- **Surgical Changes**: Modify only what was requested. Preserve formatting, comments, and docstrings.",
            "- **Zero Skeleton Code**: Write complete, runnable implementations. Never leave placeholder TODOs.",
            "- **Verify Everything**: Validate syntax, run automated unit tests, and verify edge cases before delivery.",
            "",
            f"## 2. Universal Quality Gates ({prefix}.1 - {prefix}.7)",
            f"- **[{prefix}.1] Pre-Flight Thinking**: Analyze requirements, dependencies, and potential side effects.",
            f"- **[{prefix}.2] Simplicity Guard**: Avoid unnecessary abstractions. YAGNI (You Aren't Gonna Need It).",
            f"- **[{prefix}.3] Scope Discipline**: Touch only targeted files; do not refactor unrelated modules.",
            f"- **[{prefix}.4] Success Criteria**: Define clear, testable outputs before starting implementation.",
            f"- **[{prefix}.5] Traceability**: Every added line must directly trace to the user prompt.",
            f"- **[{prefix}.6] Simplicity Re-check**: Review diff to remove debug code, temporary logs, or bloat.",
            f"- **[{prefix}.7] Verification**: Run automated test suites and verify all tests pass without errors.",
            f"- **[§X] Line-by-Line Audit**: Read actual code changes before declaring the task complete.",
            f"- **[§Y] Constructive Response**: Summarize key decisions concisely and link modified files.",
            "",
            "## 3. Tool-Specific Runtime Guidelines",
        ]

        if tool == VibeTool.CURSOR:
            lines.extend([
                "- Work natively with `.cursor/rules/*.mdc` for domain-specific architecture guidelines.",
                "- Use `python -m vibe_framework ask` or `vibe-warm` to keep context index fresh.",
                "- Use `python -m vibe_framework spec` for Spec-Driven Development workflows.",
                "- Keep `.cursorrules` concise to prevent context window saturation.",
            ])
        elif tool == VibeTool.WINDSURF:
            lines.extend([
                "- Cascade handles multi-file edits surgically.",
                "- Always read workspace files before editing to maintain symbol consistency.",
                "- Verify all changes using terminal command executions.",
            ])
        elif tool == VibeTool.CLAUDE_CODE:
            lines.extend([
                "- Claude Code respects concise, actionable commands in `CLAUDE.md`.",
                "- Common workflow commands:",
                "  * Run tests: `python -m unittest discover -v`",
                "  * Fast install: `uv pip install -e \".[all]\"`",
                "  * Framework CLI: `uv run vibe-framework --help`",
                "  * Spec-Driven Development: `python -m vibe_framework spec init <feature>`",
            ])
        elif tool == VibeTool.ANTIGRAVITY:
            lines.extend([
                "- Antigravity coordinates multi-agent subagent workflows.",
                "- Skills are loaded from `.agents/skills/` and `.gemini/skills/`.",
                "- Store persistent task context and structured plans in markdown artifacts.",
            ])
        elif tool in (VibeTool.CLINE, VibeTool.ROO_CODE):
            lines.extend([
                "- Follow autonomous step-by-step tool execution.",
                "- Request user confirmation before running destructive filesystem or network commands.",
                "- Use `.roomodes` for switching between Architect, Code, and Ask personas.",
            ])
        elif tool == VibeTool.COPILOT:
            lines.extend([
                "- Apply inline completions following existing repository style and typing.",
                "- Refer to `.github/copilot-instructions.md` for project architecture.",
            ])
        elif tool == VibeTool.AIDER:
            lines.extend([
                "- Keep git commit messages concise and descriptive.",
                "- Apply minimal diffs to avoid merge conflicts.",
            ])
        elif tool == VibeTool.CODEX:
            lines.extend([
                "- Treat `AGENTS.md` as the repository-wide source of truth for agent instructions.",
                "- Keep `.codex/` configuration minimal and prefer native workspace permissions.",
                "- Use `python -m vibe_framework warm` when the context index needs a refresh.",
            ])
        else:
            lines.extend([
                "- Refer to `AGENTS.md` for framework rules and versioning conventions.",
            ])

        lines.extend([
            "",
            "## 4. Verification Commands",
            "```bash",
            "# Run Python test suite",
            "python -m unittest discover -s vibe_framework/tests -v",
            "",
            "# Fast package execution via uv",
            "uv run vibe-framework stats",
            "```",
            "",
        ])

        return "\n".join(lines)

    def sync(
        self,
        tools: Optional[list[VibeTool]] = None,
        dry_run: bool = False,
        force: bool = False,
    ) -> VibeSyncReport:
        """
        Synchronize configuration and instructions for the specified tools.
        If tools is None, synchronizes all detected tools (or a neutral default set).
        """
        detected_results = self.detector.detect_all()
        detected_tools = [r.tool for r in detected_results if r.detected]

        if not tools:
            tools = detected_tools if detected_tools else list(DEFAULT_SYNC_TOOLS)

        modified: list[SyncFileRecord] = []
        errors: list[str] = []

        for tool in tools:
            spec = TOOL_SPECS[tool]
            config_path = self.workspace_root / spec.primary_config

            content = self.generate_unified_instructions(tool)

            try:
                action = self._write_or_simulate(
                    file_path=config_path,
                    content=content,
                    dry_run=dry_run,
                    force=force,
                )
                modified.append(
                    SyncFileRecord(
                        tool=tool,
                        file_path=config_path,
                        action=action,
                        description=f"Primary instructions for {spec.display_name}",
                    )
                )

                # Ensure rules directory exists if defined
                if spec.rules_dir:
                    r_dir = self.workspace_root / spec.rules_dir
                    if not dry_run:
                        r_dir.mkdir(parents=True, exist_ok=True)
                    else:
                        if not r_dir.exists():
                            modified.append(
                                SyncFileRecord(
                                    tool=tool,
                                    file_path=r_dir,
                                    action="would_create_dir",
                                    description=f"Rules directory for {spec.display_name}",
                                )
                            )

            except Exception as exc:
                logger.error("Failed to sync tool %s: %s", tool.value, exc)
                errors.append(f"{tool.value}: {exc}")

        return VibeSyncReport(
            workspace_root=self.workspace_root,
            tools_detected=detected_tools,
            synced_tools=tools,
            files_modified=modified,
            dry_run=dry_run,
            errors=errors,
        )

    def _write_or_simulate(
        self,
        file_path: Path,
        content: str,
        dry_run: bool,
        force: bool,
    ) -> str:
        """Write content to file or simulate action."""
        existed = file_path.exists()
        if file_path.exists():
            existing = file_path.read_text(encoding="utf-8", errors="replace")
            if existing.strip() == content.strip():
                return "skipped"
            if dry_run:
                return "would_update"
            if not force:
                # Never destroy workspace-specific instructions. The caller
                # reports this as "skipped"; --force is the explicit opt-in.
                return "skipped"

        if dry_run:
            return "would_create"

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return "updated" if existed else "created"

    def install_plugins(
        self,
        tools: Optional[list[VibeTool]] = None,
        source_dir: Optional[Path | str] = None,
        global_install: bool = False,
        force: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """
        Deploy framework plugins into the specified vibe coding tools.
        Copies plugins from source_dir (default: workspace/plugins) to tool plugin directories.
        """
        import shutil

        src = Path(source_dir or (self.workspace_root / "plugins")).resolve()
        if not src.exists():
            return {
                "success": False,
                "error": f"Source plugins directory not found: {src}",
                "dry_run": dry_run,
                "results": {},
            }

        plugin_dirs = [d for d in src.iterdir() if d.is_dir() and (d / "manifest.json").exists()]
        if not plugin_dirs:
            return {
                "success": False,
                "error": f"No valid plugins with manifest.json found in {src}",
                "dry_run": dry_run,
                "results": {},
            }

        if tools is None:
            detected = self.detector.detect_runtime_tools()
            tools = detected if detected else list(DEFAULT_PLUGIN_TOOLS)

        user_home = Path.home()
        results: dict[str, Any] = {}

        for tool in tools:
            spec = TOOL_SPECS[tool]
            target_sub = spec.global_plugins_dir if global_install else spec.plugins_dir
            if not target_sub:
                results[tool.value] = {"status": "skipped", "reason": "No plugin directory defined for this tool"}
                continue

            compatible_plugins: list[Path] = []
            incompatible_plugins: list[dict[str, str]] = []
            for plugin_dir in plugin_dirs:
                if _detect_plugin_format(plugin_dir / "manifest.json") == "vscode" and not spec.supports_vscode_plugins:
                    incompatible_plugins.append({
                        "plugin": plugin_dir.name,
                        "status": "skipped",
                        "reason": "VS Code-style extension bundle is not loaded by this runtime",
                    })
                else:
                    compatible_plugins.append(plugin_dir)

            if not compatible_plugins and incompatible_plugins:
                results[tool.value] = {
                    "status": "skipped",
                    "reason": f"{spec.display_name} does not load VS Code-style extension bundles",
                    "display_name": spec.display_name,
                    "dry_run": dry_run,
                    "plugins": incompatible_plugins,
                }
                continue

            target_base = (user_home / target_sub) if global_install else (self.workspace_root / target_sub)
            if not dry_run:
                target_base.mkdir(parents=True, exist_ok=True)

            installed_for_tool = []
            for p in compatible_plugins:
                dest = target_base / p.name
                already_exists = dest.exists()
                if already_exists and not force:
                    installed_for_tool.append({"plugin": p.name, "status": "exists", "path": str(dest)})
                    continue
                if dry_run:
                    status = "would_overwrite" if already_exists else "would_install"
                    installed_for_tool.append({"plugin": p.name, "status": status, "path": str(dest)})
                    continue
                shutil.copytree(p, dest, dirs_exist_ok=True)
                installed_for_tool.append({"plugin": p.name, "status": "installed", "path": str(dest)})
            installed_for_tool.extend(incompatible_plugins)

            results[tool.value] = {
                "display_name": spec.display_name,
                "target_directory": str(target_base),
                "is_global": global_install,
                "dry_run": dry_run,
                "plugins": installed_for_tool,
            }

        return {"success": True, "source": str(src), "dry_run": dry_run, "results": results}


def get_vibe_summary(workspace_root: str | Path | None = None) -> dict[str, Any]:
    """Helper returning a clean dictionary summary of all vibe tools in workspace."""
    detector = VibeDetector(workspace_root)
    results = detector.detect_all()
    return {
        "workspace_root": str(detector.workspace_root),
        "tools": [
            {
                "tool": r.tool.value,
                "display_name": r.display_name,
                "detected": r.detected,
                "reasons": r.reasons,
                "config_exists": r.config_exists,
                "rules_dir_exists": r.rules_dir_exists,
                "skills_dir_exists": r.skills_dir_exists,
            }
            for r in results
        ],
        "active_count": sum(1 for r in results if r.detected),
    }
