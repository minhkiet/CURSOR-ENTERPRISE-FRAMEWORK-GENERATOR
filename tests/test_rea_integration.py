import json
import subprocess
import sys
from pathlib import Path
import pytest

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cursor_framework.cross_agent import ALL_SKILLS, UNIVERSAL_SKILLS, SkillDefinition
from cursor_framework.skill_discovery import CrossAgentSkillDiscovery, SkillDiscovery
from tools.mcp_config_generator import McpConfigGenerator


def test_rea_tool_files_exist():
    """Verify REA vendor files, entrypoint script and SYNC.md exist."""
    repo_root = Path(__file__).resolve().parent.parent
    rea_dir = repo_root / "tools" / "rea"
    assert rea_dir.is_dir(), "tools/rea directory must exist"
    assert (rea_dir / "scripts" / "rea.mjs").is_file(), "scripts/rea.mjs must exist"
    assert (rea_dir / "package.json").is_file(), "package.json must exist"
    assert (rea_dir / "SYNC.md").is_file(), "SYNC.md must exist"


def test_rea_compiled_runtime_present():
    """Verify the compiled REA runtime exists when it has been built.

    ponytail: `dist/` is a gitignored build output (tools/rea AGENTS.md:
    never commit dist/ or node_modules/). The root repository CI does not
    build the Node runtime, so assert its presence only when a build exists
    and skip otherwise instead of failing a run that never built it.
    """
    repo_root = Path(__file__).resolve().parent.parent
    rea_dir = repo_root / "tools" / "rea"
    if not (rea_dir / "dist").is_dir():
        pytest.skip("REA compiled runtime not built; run `npm ci && npm run build:cached` in tools/rea")
    assert (rea_dir / "dist" / "main.js").is_file(), "compiled dist/main.js must exist"


def test_rea_cli_execution():
    """Verify REA CLI runs with node and reports version 6.4.0."""
    repo_root = Path(__file__).resolve().parent.parent
    rea_dir = repo_root / "tools" / "rea"
    if not (rea_dir / "dist").is_dir():
        pytest.skip("REA compiled runtime not built; run `npm ci && npm run build:cached` in tools/rea")
    rea_script = rea_dir / "scripts" / "rea.mjs"
    res = subprocess.run(
        ["node", str(rea_script), "--version"],
        capture_output=True,
        text=True,
        cwd=str(repo_root),
    )
    assert res.returncode == 0, f"rea CLI failed with error: {res.stderr}"
    assert "6.4.0" in res.stdout.strip()


def test_rea_skills_exist():
    """Verify reverse-engineer-anything skills are present in .cursor and .agents."""
    repo_root = Path(__file__).resolve().parent.parent

    cursor_skill = repo_root / ".cursor" / "skills" / "sec_reverse-engineer-anything"
    agents_skill = repo_root / ".agents" / "skills" / "reverse-engineer-anything"

    assert (cursor_skill / "SKILL.md").is_file(), ".cursor SKILL.md must exist"
    assert (agents_skill / "SKILL.md").is_file(), ".agents SKILL.md must exist"

    # Check references
    assert (cursor_skill / "references" / "evidence-workflows.md").is_file()
    assert (cursor_skill / "references" / "javascript-applications.md").is_file()
    assert (cursor_skill / "references" / "native-and-artifacts.md").is_file()


def test_cross_agent_registration():
    """Verify skill registration in cross_agent.py."""
    assert "reverse-engineer-anything" in UNIVERSAL_SKILLS
    assert "reverse-engineer-anything" in ALL_SKILLS

    skill_def = ALL_SKILLS["reverse-engineer-anything"]
    assert isinstance(skill_def, SkillDefinition)
    assert skill_def.category == "Security"
    assert any("reverse" in t for t in skill_def.triggers)
    assert "ghidra" in skill_def.triggers or "decompile" in skill_def.triggers


def test_skill_discovery_includes_rea():
    """Verify skill discovery identifies reverse-engineer-anything."""
    discovery = CrossAgentSkillDiscovery()
    assert "reverse-engineer-anything" in discovery.UNIVERSAL_SKILLS
    assert "reverse-engineer-anything" in discovery.AGENT_SKILL_MAPPINGS["cursor"]
    assert "reverse-engineer-anything" in discovery.AGENT_SKILL_MAPPINGS["codex"]


def test_mcp_config_generator_rea():
    """Verify McpConfigGenerator can configure rea MCP server."""
    repo_root = Path(__file__).resolve().parent.parent
    generator = McpConfigGenerator(str(repo_root), target="cursor")
    generator.add_rea()

    config = generator.config.to_dict()
    assert "rea" in config["mcpServers"]
    rea_server = config["mcpServers"]["rea"]
    assert rea_server["command"] == "node"
    assert any("rea.mjs" in arg for arg in rea_server["args"])


def test_commands_exist():
    """Verify /rea and /reverse commands exist."""
    repo_root = Path(__file__).resolve().parent.parent
    rea_cmd = repo_root / ".cursor" / "commands" / "rea.md"
    reverse_cmd = repo_root / ".cursor" / "commands" / "reverse.md"

    assert rea_cmd.is_file(), "rea.md must exist"
    assert reverse_cmd.is_file(), "reverse.md must exist"
    assert "Reverse Engineer Anything" in rea_cmd.read_text(encoding="utf-8")
