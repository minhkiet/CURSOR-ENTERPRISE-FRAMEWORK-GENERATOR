"""Task analysis and automatic framework resource selection."""

from __future__ import annotations

from typing import Any

from cursor_framework_mcp.analyzer import AnalysisResult, TaskAnalyzer
from cursor_framework_mcp.loader import Loader, estimate_tokens

from .executor import ResourceExecutor
from .workflow import WorkflowOrchestrator


class Autopilot:
    """Analyze tasks, load matching resources, and create executable plans."""

    def __init__(self, loader: Loader) -> None:
        self.loader = loader
        self.analyzer = TaskAnalyzer(loader)
        self.executor = ResourceExecutor(loader)
        self.workflows = WorkflowOrchestrator(self.executor)

    def auto_execute(self, task: str, top_k: int = 8) -> dict[str, Any]:
        analysis = self.analyzer.analyze(task, top_k=top_k)
        selected = self._select_resources(analysis)
        steps = self.executor.execute_many(selected)
        return {
            "task": task,
            "analysis": self._analysis_to_dict(analysis),
            "status": "ready" if all(step.status == "ready" for step in steps) else "partial",
            "execution_mode": "host_orchestrated",
            "steps": [step.to_dict() for step in steps],
            "estimated_tokens": estimate_tokens(task) + sum(step.tokens for step in steps),
        }

    def estimate_cost(self, task: str, workflow: str | None = None) -> dict[str, Any]:
        if workflow:
            if workflow not in self.workflows.list_workflows():
                raise KeyError(f"Unknown workflow '{workflow}'")
            ids = self.workflows.list_workflows()[workflow]
        else:
            analysis = self.analyzer.analyze(task, top_k=8)
            ids = self._select_resources(analysis)
        steps = self.executor.execute_many(ids)
        input_tokens = estimate_tokens(task)
        resource_tokens = sum(step.tokens for step in steps)
        total_tokens = input_tokens + resource_tokens
        return {
            "task": task,
            "workflow": workflow,
            "input_tokens": input_tokens,
            "resource_tokens": resource_tokens,
            "estimated_total_tokens": total_tokens,
            "estimated_minutes": round(max(0.5, 0.5 + len(steps) * 1.5 + total_tokens / 6000), 1),
            "resources": [{"id": step.id, "kind": step.kind, "tokens": step.tokens} for step in steps],
            "note": "Estimate covers framework context and orchestration, not model-specific pricing.",
        }

    def suggest_optimization(self, task: str) -> dict[str, Any]:
        analysis = self.analyzer.analyze(task, top_k=8)
        domains = set(analysis.detected_domains)
        suggestions = [
            "Load only the top-ranked resources and essential overlays.",
            "Use narrow verification commands before broad test suites.",
            "Compact completed workflow output into conclusions and evidence.",
        ]
        if "frontend" in domains:
            suggestions.append("Defer heavy components and parallelize independent data fetching.")
        if "database" in domains:
            suggestions.append("Inspect query plans and indexes before changing data access code.")
        if "security" in domains:
            suggestions.append("Validate authentication, authorization, and untrusted inputs at boundaries.")
        if "performance" in domains:
            suggestions.append("Measure a baseline before optimizing and compare after changes.")
        return {"task": task, "domains": sorted(domains), "suggestions": suggestions}

    @staticmethod
    def _select_resources(analysis: AnalysisResult) -> list[str]:
        ids: list[str] = []
        if analysis.is_coding_task:
            ids.extend(item.id for item in analysis.essential_skills)
        ids.extend(item.id for item in analysis.suggestions if item.confidence >= 0.5)
        return list(dict.fromkeys(ids))

    @staticmethod
    def _analysis_to_dict(result: AnalysisResult) -> dict[str, Any]:
        def suggestion(item: Any) -> dict[str, Any]:
            return {
                "id": item.id,
                "kind": item.kind,
                "confidence": item.confidence,
                "domains": item.domains,
                "reason": item.reason,
                "path": item.path,
            }

        return {
            "request": result.request,
            "detected_language": result.detected_language,
            "detected_domains": result.detected_domains,
            "is_coding_task": result.is_coding_task,
            "primary": suggestion(result.primary) if result.primary else None,
            "suggestions": [suggestion(item) for item in result.suggestions],
            "essential_skills": [suggestion(item) for item in result.essential_skills],
        }
