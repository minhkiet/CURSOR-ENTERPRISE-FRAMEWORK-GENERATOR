"""Workflow definitions and thread-safe execution state."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from .executor import ResourceExecutor

WORKFLOWS: dict[str, list[str]] = {
    "build": ["karpathy-coding", "ponytail", "full-output", "code-reviewer"],
    "fix": ["debugger", "karpathy-coding", "code-reviewer"],
    "review": ["analyze_task", "load_appropriate_reviewer", "run_review"],
    "test": ["test-engineer", "analyze_coverage", "run_tests"],
    "security": ["security-review", "security-auditor"],
    "perf": ["web-performance-auditor", "perf_optimization"],
}


@dataclass
class WorkflowRun:
    """Mutable status for one workflow execution."""

    id: str
    workflow: str
    task: str
    status: str = "running"
    current_step: int = 0
    steps: list[dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    abort_requested: bool = False

    def to_dict(self, include_instructions: bool = True) -> dict[str, Any]:
        steps = self.steps
        if not include_instructions:
            steps = [{key: value for key, value in step.items() if key != "instructions"} for step in steps]
        return {
            "id": self.id,
            "workflow": self.workflow,
            "task": self.task,
            "status": self.status,
            "current_step": self.current_step,
            "step_count": len(self.steps),
            "steps": steps,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class WorkflowOrchestrator:
    """Resolve predefined workflows and retain their status in memory."""

    def __init__(self, executor: ResourceExecutor) -> None:
        self.executor = executor
        self._runs: dict[str, WorkflowRun] = {}
        self._lock = threading.RLock()

    def list_workflows(self) -> dict[str, list[str]]:
        return {name: list(steps) for name, steps in WORKFLOWS.items()}

    def execute(self, workflow: str, task: str, payment: bool = False) -> WorkflowRun:
        if workflow not in WORKFLOWS:
            raise KeyError(f"Unknown workflow '{workflow}'")
        step_ids = list(WORKFLOWS[workflow])
        if workflow == "security" and payment:
            step_ids.append("vietnam-payment-review")

        run = WorkflowRun(id=uuid.uuid4().hex, workflow=workflow, task=task)
        with self._lock:
            self._runs[run.id] = run

        for index, step_id in enumerate(step_ids, start=1):
            with self._lock:
                if run.abort_requested:
                    run.status = "aborted"
                    run.updated_at = time.time()
                    break
            step = self.executor.execute(step_id)
            with self._lock:
                run.steps.append(step.to_dict())
                run.current_step = index
                run.updated_at = time.time()
                if step.status == "failed":
                    run.status = "failed"
                    break
        else:
            with self._lock:
                run.status = "ready"
                run.updated_at = time.time()
        return run

    def get_status(self, workflow_id: str) -> WorkflowRun | None:
        with self._lock:
            return self._runs.get(workflow_id)

    def abort(self, workflow_id: str) -> WorkflowRun | None:
        with self._lock:
            run = self._runs.get(workflow_id)
            if run is None:
                return None
            run.abort_requested = True
            if run.status in {"running", "ready"}:
                run.status = "aborted"
            run.updated_at = time.time()
            return run
