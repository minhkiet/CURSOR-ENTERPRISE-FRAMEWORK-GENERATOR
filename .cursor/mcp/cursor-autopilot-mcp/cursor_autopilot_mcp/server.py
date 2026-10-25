"""FastMCP server for automatic framework orchestration."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

pkg_dir = Path(__file__).resolve().parent
parent_dir = pkg_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
if str(pkg_dir) not in sys.path:
    sys.path.insert(0, str(pkg_dir))
if not __package__:
    __package__ = pkg_dir.name

try:
    from mcp.server.fastmcp import FastMCP
except Exception:
    try:
        from fastmcp import FastMCP
    except Exception:
        try:
            from .mcp_runtime import UniversalMcpServer as FastMCP
        except Exception:
            from mcp_runtime import UniversalMcpServer as FastMCP


def _bootstrap_framework_import() -> None:
    candidates = []
    for env_key in ("ANTIGRAVITY_WORKSPACE_ROOT", "CURSOR_WORKSPACE_ROOT", "CLAUDE_PROJECT_DIR", "CODEX_WORKSPACE_ROOT", "WORKSPACE_ROOT"):
        configured = os.environ.get(env_key)
        if configured:
            candidates.append(Path(configured).resolve() / "tools" / "cursor-framework-mcp")
            candidates.append(Path(configured).resolve() / ".cursor" / "mcp" / "cursor-framework-mcp")

    candidates.extend(
        [
            Path.cwd().resolve() / "tools" / "cursor-framework-mcp",
            Path.cwd().resolve() / ".cursor" / "mcp" / "cursor-framework-mcp",
            Path(__file__).resolve().parents[2] / "cursor-framework-mcp",
        ]
    )
    for candidate in candidates:
        if candidate.is_dir() and str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
            return


_bootstrap_framework_import()

from cursor_framework_mcp.loader import make_default_loader  # noqa: E402
from cursor_framework_mcp.registry import find_workspace_root  # noqa: E402

from .autopilot import Autopilot  # noqa: E402
from .gate_keeper import GateKeeper  # noqa: E402


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)


def _workspace_root() -> str:
    for env_key in ("ANTIGRAVITY_WORKSPACE_ROOT", "CURSOR_WORKSPACE_ROOT", "CLAUDE_PROJECT_DIR", "CODEX_WORKSPACE_ROOT", "WORKSPACE_ROOT"):
        configured = os.environ.get(env_key)
        if configured and Path(configured).is_dir():
            return str(Path(configured).resolve())
    return find_workspace_root(os.getcwd())


def create_server(workspace_root: str | None = None) -> FastMCP:
    root = workspace_root or _workspace_root()
    loader = make_default_loader(root)
    autopilot = Autopilot(loader)
    gate_keeper = GateKeeper(loader)
    mcp = FastMCP(
        "cursor-autopilot-mcp",
        instructions=f"Analyze tasks and prepare host-executable framework workflows. Workspace root: {root}",
    )

    @mcp.tool()
    def auto_execute(task: str, top_k: int = 8) -> str:
        """Analyze a task, auto-load matching rules/skills/agents, and return an ordered execution plan."""
        return _json(autopilot.auto_execute(task, top_k))

    @mcp.tool()
    def execute_workflow(workflow: str, task: str, payment: bool = False) -> str:
        """Resolve a predefined build/fix/review/test/security/perf workflow into host-executable steps."""
        try:
            run = autopilot.workflows.execute(workflow, task, payment=payment)
        except KeyError as exc:
            return _json({"error": "unknown_workflow", "message": str(exc)})
        return _json(run.to_dict())

    @mcp.tool()
    def run_gate_validation(skill_id: str, phase: str, evidence: str = "") -> str:
        """Validate a skill's pre/post gates against supplied evidence."""
        try:
            result = gate_keeper.validate(skill_id, phase, evidence)  # type: ignore[arg-type]
        except (KeyError, FileNotFoundError, ValueError) as exc:
            return _json({"error": "validation_failed", "message": str(exc)})
        return _json(result)

    @mcp.tool()
    def get_workflow_status(workflow_id: str) -> str:
        """Get current status for a workflow execution id."""
        run = autopilot.workflows.get_status(workflow_id)
        return _json(run.to_dict(False) if run else {"error": "not_found", "workflow_id": workflow_id})

    @mcp.tool()
    def abort_workflow(workflow_id: str) -> str:
        """Request that a running workflow stop and mark it aborted."""
        run = autopilot.workflows.abort(workflow_id)
        return _json(run.to_dict(False) if run else {"error": "not_found", "workflow_id": workflow_id})

    @mcp.tool()
    def list_workflows() -> str:
        """List available predefined workflows and their ordered steps."""
        return _json({"workflows": autopilot.workflows.list_workflows()})

    @mcp.tool()
    def estimate_cost(task: str, workflow: str | None = None) -> str:
        """Estimate context tokens and orchestration time for a task or workflow."""
        try:
            return _json(autopilot.estimate_cost(task, workflow))
        except KeyError as exc:
            return _json({"error": "unknown_workflow", "message": str(exc)})

    @mcp.tool()
    def suggest_optimization(task: str) -> str:
        """Suggest context, verification, and domain optimizations for a task."""
        return _json(autopilot.suggest_optimization(task))

    return mcp


def run() -> None:
    create_server().run()


if __name__ == "__main__":
    run()
