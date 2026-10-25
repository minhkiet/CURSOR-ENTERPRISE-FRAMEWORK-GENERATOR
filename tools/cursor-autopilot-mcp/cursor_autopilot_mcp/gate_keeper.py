"""Pre- and post-execution gate validation."""

from __future__ import annotations

import re
from typing import Any, Literal

from cursor_framework_mcp.loader import Loader

GatePhase = Literal["pre", "post"]
_CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s+(.+)$", re.MULTILINE)
_HEADING_RE = re.compile(r"^#{2,6}\s+(.+)$", re.MULTILINE)


class GateKeeper:
    """Extract and validate a skill's documented quality gates."""

    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    def validate(self, skill_id: str, phase: GatePhase, evidence: str = "") -> dict[str, Any]:
        if phase not in {"pre", "post"}:
            raise ValueError("phase must be 'pre' or 'post'")
        loaded = self.loader.load_skill(skill_id)
        checks = self._extract_checks(loaded.body, phase)
        evidence_norm = evidence.strip().lower()
        results = [
            {
                "check": check,
                "passed": self._has_evidence(check, evidence_norm),
            }
            for check in checks
        ]
        passed = bool(results) and all(item["passed"] for item in results)
        return {
            "skill": loaded.item.id,
            "phase": phase,
            "passed": passed,
            "status": "passed" if passed else "needs_evidence",
            "checks": results,
            "tokens": loaded.tokens,
            "message": None if checks else f"No explicit {phase}-gate checklist was found in the skill",
        }

    @staticmethod
    def _extract_checks(body: str, phase: GatePhase) -> list[str]:
        sections = re.split(r"(?m)^(#{2,6}\s+.+)$", body)
        selected: list[str] = []
        keywords = ("pre", "before") if phase == "pre" else ("post", "after", "verify")
        for index in range(1, len(sections), 2):
            heading = sections[index]
            content = sections[index + 1] if index + 1 < len(sections) else ""
            if any(keyword in heading.lower() for keyword in keywords):
                selected.extend(check.strip() for check in _CHECKBOX_RE.findall(content))
        if selected:
            return list(dict.fromkeys(selected))

        headings = [heading.strip() for heading in _HEADING_RE.findall(body)]
        fallback = [heading for heading in headings if any(keyword in heading.lower() for keyword in keywords)]
        return list(dict.fromkeys(fallback))

    @staticmethod
    def _has_evidence(check: str, evidence: str) -> bool:
        if not evidence:
            return False
        words = [word for word in re.findall(r"[a-z0-9-]{4,}", check.lower()) if word not in {"should", "before", "after", "verify", "check"}]
        return not words or any(word in evidence for word in words)
