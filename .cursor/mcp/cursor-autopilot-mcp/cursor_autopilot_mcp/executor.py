"""Load framework resources and describe their execution.

MCP servers cannot directly invoke Cursor subagents. This executor therefore loads
rules/skills/agents through ``cursor-framework-mcp`` and returns an explicit,
ordered execution plan that the host agent can follow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from cursor_framework_mcp.loader import Loader


@dataclass(frozen=True)
class ExecutionStep:
    """A resolved workflow step."""

    id: str
    kind: str
    action: str
    status: str
    path: str | None = None
    tokens: int = 0
    instructions: str | None = None
    error: str | None = None

    def to_dict(self, include_body: bool = True) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "kind": self.kind,
            "action": self.action,
            "status": self.status,
            "path": self.path,
            "tokens": self.tokens,
        }
        if include_body and self.instructions is not None:
            data["instructions"] = self.instructions
        if self.error:
            data["error"] = self.error
        return data


class ResourceExecutor:
    """Resolve framework resources using the shared registry and loader."""

    ACTIONS = {"analyze_task", "load_appropriate_reviewer", "run_review", "analyze_coverage", "run_tests", "perf_optimization"}

    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    def execute(self, step_id: str) -> ExecutionStep:
        if step_id in self.ACTIONS:
            return ExecutionStep(
                id=step_id,
                kind="action",
                action=step_id,
                status="ready",
                instructions=self._action_instructions(step_id),
            )

        item = self.loader.registry.lookup(step_id)
        if item is None:
            return ExecutionStep(step_id, "unknown", "load", "failed", error=f"Resource '{step_id}' was not found")

        try:
            if item.kind == "rule":
                loaded = self.loader.load_rule(step_id)
            elif item.kind == "skill":
                loaded = self.loader.load_skill(step_id)
            else:
                loaded = self.loader.load_agent(step_id)
        except (KeyError, FileNotFoundError, OSError) as exc:
            return ExecutionStep(step_id, item.kind, "load", "failed", path=item.path, error=str(exc))

        return ExecutionStep(
            id=loaded.item.id,
            kind=loaded.item.kind,
            action="apply" if loaded.item.kind != "agent" else "delegate",
            status="ready",
            path=loaded.item.path,
            tokens=loaded.tokens,
            instructions=loaded.body,
        )

    def execute_many(self, step_ids: Iterable[str]) -> list[ExecutionStep]:
        return [self.execute(step_id) for step_id in step_ids]

    @staticmethod
    def _action_instructions(action: str) -> str:
        instructions = {
            "analyze_task": "Analyze the request and select framework resources relevant to its domains.",
            "load_appropriate_reviewer": "Select the highest-confidence reviewer agent for the detected domain.",
            "run_review": "Review correctness, design, readability, security, and performance; report actionable findings.",
            "analyze_coverage": "Inspect test coverage and identify untested critical and error paths.",
            "run_tests": "Run the narrowest relevant test suite and report command, exit status, and failures.",
            "perf_optimization": "Measure bottlenecks first, apply targeted optimizations, and verify the improvement.",
        }
        return instructions[action]
