"""
Spec Kit Module — Spec-Driven Development (SDD) Engine for Vibe Enterprise Framework.

Enforces specification-first, plan-first, and task-driven development workflows:
- Phase 1: Constitution (Project Principles & Quality Gates)
- Phase 2: Specify (Business & User Requirements, BDD Scenarios)
- Phase 3: Clarify (Edge-Case Discovery & Ambiguity Resolution)
- Phase 4: Plan (Architecture Blueprint, Data Models, API Contracts)
- Phase 5: Checklist (Verification & Quality Assurance Gate)
- Phase 6: Tasks (Atomic Dependency-Ordered Task Decomposition)
- Phase 7: Implement (TDD Red-Green-Refactor with Traceable Progress)

Stdlib only — zero external runtime dependencies.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

DEFAULT_CONSTITUTION_TEMPLATE = """# Project Constitution

> **Status:** Active | **Enforced By:** All AI Coding Agents & CI Gates

---

## 1. Core Principles & Philosophy
- **Think Before Coding**: Analyze intent, requirements, and edge cases before generating implementation files.
- **Specification-Driven**: Every substantial feature must originate from a documented specification (`spec.md`) and plan (`plan.md`).
- **Simplicity Guard & YAGNI**: No speculative abstractions or dead code. Implement the minimal sufficient solution.
- **Test-Driven Discipline (TDD)**: No production code without failing tests first. All tests must be deterministic.
- **Evidence-First Debugging**: Zero guesswork. Reproduce bugs with a minimal test case before modifying implementation.

---

## 2. Architectural Boundaries & Stack Invariants
- **Runtime & Language Standards**: Define explicit versions.
- **Dependency Policy**: Zero unvetted dependencies. Favor standard library and established core libraries.
- **Isolation of Concerns**: Domain logic must remain independent of external frameworks.

---

## 3. Quality & Security Gates
- **Security Invariants**: Zero unescaped inputs, strict authentication/authorization checks, zero hardcoded secrets.
- **Quality Checks**: Automated linting, type-checking, and unit test suite must pass 100% on every pull request.
- **Documentation**: Code must be self-explanatory with concise docstrings for public APIs.
"""

DEFAULT_SPEC_TEMPLATE = """# Feature Specification: {feature_name}

> **Feature Branch:** `feature/{feature_name}`  
> **Status:** Draft | Under Review | Approved | In Progress | Completed  
> **Created:** [YYYY-MM-DD]  
> **Author:** [Author/Agent]

---

## 1. Problem Statement & Motivation
- **What is the problem?** Describe the customer pain point or developer requirement.
- **Why now?** Context, urgency, or expected business/system impact.
- **Scope Boundary:** Explicitly state what is IN scope and what is OUT of scope.

---

## 2. User Scenarios & Acceptance Criteria (BDD / Gherkin)

### Scenario 1: [Primary Happy Path]
- **Given** [initial system state / user condition]
- **When** [user performs action or event triggers]
- **Then** [expected observable result and state change]

### Scenario 2: [Edge Case / Validation Failure]
- **Given** [invalid input or network timeout condition]
- **When** [action is attempted]
- **Then** [graceful error response with actionable feedback]

---

## 3. Functional Requirements
- **FR-1:** System MUST ...
- **FR-2:** System SHALL ...
- **FR-3:** System MUST NOT ...

---

## 4. Non-Functional Requirements (NFRs)
- **Performance:** Response time latency target (e.g., < 200ms p95).
- **Security & Privacy:** Authentication, authorization, sensitive data handling.
- **Reliability & Observability:** Structured error logging, metrics, fallback behavior.

---

## 5. Open Questions & Assumptions
- [ ] Question 1: [Unresolved technical or product question]
- Assumptions: [List assumptions made if questions cannot be resolved immediately]
"""

DEFAULT_PLAN_TEMPLATE = """# Technical Implementation Plan: {feature_name}

> **Spec Reference:** `spec.md`  
> **Status:** Draft | Ready for Execution | In Progress | Completed  
> **Target Release:** [Release Version]

---

## 1. Technical Context & High-Level Architecture
- **Architecture Overview:** How this feature fits into existing components and patterns.
- **Component Diagram / Data Flow:**
```
[Client / Caller] ➔ [API / Controller] ➔ [Service Layer] ➔ [Data Store]
```

---

## 2. Data Models & API Contracts

### Data Model Changes
```typescript
interface {feature_pascal}Model {{
  id: string;
  createdAt: string;
}}
```

### API Endpoints / Function Signatures
- **Method/Route:** `POST /api/v1/{feature_name}`
- **Request Payload:** `{{ ... }}`
- **Response Format:** `{{ status: "ok", data: {{ ... }} }}`

---

## 3. Technology Stack & Dependencies
- **Languages & Frameworks:** Standard library first, zero unvetted dependencies.
- **File Impact Map:**
  - `path/to/models.py` (New / Modified)
  - `path/to/service.py` (New)
  - `path/to/tests/test_service.py` (New test suite)

---

## 4. Verification & Testing Strategy
- **Unit Tests:** Core logic, edge cases, validator rules.
- **Integration Tests:** End-to-end data pipeline or API contract test.
- **Manual Verification Steps:** Step-by-step verification commands and expected outputs.

---

## 5. Risk Assessment & Rollback Plan
- **Primary Risks:** Backward compatibility, breaking changes.
- **Mitigation:** Safe feature flags or dual-write strategy.
- **Rollback Procedure:** Steps to cleanly revert.
"""

DEFAULT_TASKS_TEMPLATE = """# Implementation Tasks: {feature_name}

> **Spec Reference:** `spec.md` | **Plan Reference:** `plan.md`  
> **Progress:** 0 / 4 Tasks Completed (0%)

---

## Task Execution Instructions
1. Execute tasks in strict sequential order (Phase by Phase).
2. For every task, follow the TDD Red-Green-Refactor cycle.
3. Verify using the specified verification command before checking off `[x]`.
4. Keep atomic commits: one logical commit per task.

---

## Phase 1: Environment & Test Harness (RED)
- [ ] **Task 1.1: Setup test scaffolding & fixtures**
  - **Files:** `tests/test_{feature_snake}.py`
  - **Action:** Write failing test cases covering core acceptance scenarios from `spec.md`.
  - **Verification:** Test runner command (Must FAIL with expected reason).

---

## Phase 2: Core Domain & Data Layer (GREEN)
- [ ] **Task 2.1: Implement core models & data structures**
  - **Files:** `src/models/{feature_snake}.py`
  - **Action:** Define models and serialization logic.
  - **Verification:** Run type check and unit tests.
- [ ] **Task 2.2: Implement business logic service**
  - **Files:** `src/services/{feature_snake}_service.py`
  - **Action:** Write minimal implementation to satisfy failing unit tests.
  - **Verification:** Unit tests pass cleanly.

---

## Phase 3: Integration & API Exposure
- [ ] **Task 3.1: Expose API routes / CLI commands**
  - **Files:** `src/api/{feature_snake}_router.py`
  - **Action:** Connect service layer to router/CLI handler.
  - **Verification:** Test endpoint responses and error handling.

---

## Phase 4: Refactor & Polish
- [ ] **Task 4.1: Code review against CEF Quality Gates (CX.1-CX.7)**
  - **Action:** Eliminate temporary code, verify zero skeleton code, check docstrings.
  - **Verification:** Full test suite run + lint check.
"""

DEFAULT_CHECKLIST_TEMPLATE = """# Quality & Verification Checklist: {feature_name}

> **Spec:** `spec.md` | **Plan:** `plan.md` | **Tasks:** `tasks.md`

---

## 1. Specification & Requirements Verification
- [ ] Problem statement is clear, unambiguous, and justified.
- [ ] Scope boundary clearly states what is IN and OUT of scope.
- [ ] Acceptance criteria written in deterministic Given/When/Then format.
- [ ] Edge cases (empty data, network timeouts, invalid inputs) addressed.

---

## 2. Technical Architecture & Plan Verification
- [ ] Architecture respects existing codebase patterns and constitution.
- [ ] Simplicity check: adheres to YAGNI (no speculative generic helpers).
- [ ] Security reviewed: inputs validated, authorization verified, zero leaked secrets.
- [ ] Data models and API contracts defined and backwards-compatible.

---

## 3. Implementation & Testing Gates (CEF CX.1 - CX.7)
- [ ] **[CX.TDD] Strict RED-GREEN-REFACTOR**: Failing test written before production code.
- [ ] **[CX.5] Traceability**: Every added line maps directly to a task in `tasks.md`.
- [ ] **[CX.6] Zero Skeleton Code**: Complete runnable implementation without TODO placeholders.
- [ ] **[CX.7] Automated Verification**: 100% test pass with zero regression in existing test suite.
- [ ] **[§X] Line-by-Line Audit**: Diff reviewed, debug code and temporary logs removed.
"""


def _to_pascal_case(s: str) -> str:
    parts = re.split(r"[-_]+", s)
    return "".join(p.capitalize() for p in parts if p)


def _to_snake_case(s: str) -> str:
    parts = re.split(r"[-_]+", s)
    return "_".join(p.lower() for p in parts if p)


class SpecKitManager:
    """Manages the Spec-Driven Development (SDD) workspace, templates, and validation."""

    def __init__(self, workspace_root: Optional[Path | str] = None) -> None:
        if workspace_root is None:
            self.workspace = Path.cwd()
        else:
            self.workspace = Path(workspace_root).resolve()

        self.specify_root = self.workspace / ".specify"
        self.specs_dir = self.specify_root / "specs"
        self.constitution_path = self.specify_root / "constitution.md"
        self.templates_dir = self.workspace / "vibe-code-framework" / "06-templates"

    def _read_template_or_default(self, filename: str, default_content: str) -> str:
        tpl_file = self.templates_dir / filename
        if tpl_file.exists():
            try:
                return tpl_file.read_text(encoding="utf-8")
            except OSError:
                pass
        return default_content

    def init_constitution(self, force: bool = False) -> Path:
        """Create or initialize the project constitution file."""
        self.specify_root.mkdir(parents=True, exist_ok=True)
        if self.constitution_path.exists() and not force:
            return self.constitution_path

        content = self._read_template_or_default("constitution-template.md", DEFAULT_CONSTITUTION_TEMPLATE)
        self.constitution_path.write_text(content, encoding="utf-8")
        return self.constitution_path

    def get_feature_dir(self, feature_name: str) -> Path:
        """Get the directory path for a specific feature."""
        slug = re.sub(r"[^a-zA-Z0-9_\-]+", "-", feature_name).strip("-").lower()
        return self.specs_dir / slug

    def init_feature(self, feature_name: str, force: bool = False) -> dict[str, Path]:
        """Scaffold a new feature spec bundle (spec.md, plan.md, tasks.md, checklist.md)."""
        feature_dir = self.get_feature_dir(feature_name)
        if feature_dir.exists() and not force:
            raise FileExistsError(f"Feature spec bundle already exists: {feature_dir}")

        feature_dir.mkdir(parents=True, exist_ok=True)
        self.init_constitution()

        pascal = _to_pascal_case(feature_name)
        snake = _to_snake_case(feature_name)

        # 1. Spec
        spec_tpl = self._read_template_or_default("spec-template.md", DEFAULT_SPEC_TEMPLATE)
        spec_content = spec_tpl.replace("{feature_name}", feature_name)
        if "[Feature Name]" in spec_content:
            spec_content = spec_content.replace("[Feature Name]", feature_name)
        if "[feature-name]" in spec_content:
            spec_content = spec_content.replace("[feature-name]", feature_name)
        spec_path = feature_dir / "spec.md"
        spec_path.write_text(spec_content, encoding="utf-8")

        # 2. Plan
        plan_tpl = self._read_template_or_default("plan-template.md", DEFAULT_PLAN_TEMPLATE)
        plan_content = plan_tpl.replace("{feature_name}", feature_name)
        plan_content = plan_content.replace("{feature_pascal}", pascal)
        if "[Feature Name]" in plan_content:
            plan_content = plan_content.replace("[Feature Name]", feature_name)
        plan_path = feature_dir / "plan.md"
        plan_path.write_text(plan_content, encoding="utf-8")

        # 3. Tasks
        tasks_tpl = self._read_template_or_default("tasks-template.md", DEFAULT_TASKS_TEMPLATE)
        tasks_content = tasks_tpl.replace("{feature_name}", feature_name)
        tasks_content = tasks_content.replace("{feature_snake}", snake)
        if "[Feature Name]" in tasks_content:
            tasks_content = tasks_content.replace("[Feature Name]", feature_name)
        if "[feature]" in tasks_content:
            tasks_content = tasks_content.replace("[feature]", snake)
        tasks_path = feature_dir / "tasks.md"
        tasks_path.write_text(tasks_content, encoding="utf-8")

        # 4. Checklist
        chk_tpl = self._read_template_or_default("checklist-template.md", DEFAULT_CHECKLIST_TEMPLATE)
        chk_content = chk_tpl.replace("{feature_name}", feature_name)
        if "[Feature Name]" in chk_content:
            chk_content = chk_content.replace("[Feature Name]", feature_name)
        chk_path = feature_dir / "checklist.md"
        chk_path.write_text(chk_content, encoding="utf-8")

        return {
            "spec": spec_path,
            "plan": plan_path,
            "tasks": tasks_path,
            "checklist": chk_path,
        }

    def list_features(self) -> list[str]:
        """List all registered features in .specify/specs/."""
        if not self.specs_dir.exists():
            return []
        return sorted([d.name for d in self.specs_dir.iterdir() if d.is_dir()])

    def get_feature_status(self, feature_name: str) -> dict[str, Any]:
        """Parse tasks.md and checklist to compute feature completion rate."""
        feature_dir = self.get_feature_dir(feature_name)
        spec_path = feature_dir / "spec.md"
        plan_path = feature_dir / "plan.md"
        tasks_path = feature_dir / "tasks.md"
        chk_path = feature_dir / "checklist.md"

        has_spec = spec_path.exists()
        has_plan = plan_path.exists()
        has_tasks = tasks_path.exists()
        has_checklist = chk_path.exists()

        completed_tasks = 0
        pending_tasks = 0

        if has_tasks:
            try:
                tasks_text = tasks_path.read_text(encoding="utf-8")
                for line in tasks_text.splitlines():
                    trimmed = line.strip()
                    if trimmed.startswith("- [x]") or trimmed.startswith("* [x]"):
                        completed_tasks += 1
                    elif trimmed.startswith("- [ ]") or trimmed.startswith("* [ ]"):
                        pending_tasks += 1
            except OSError as e:
                logger.warning(f"Failed to read tasks file for {feature_name}: {e}")

        total_tasks = completed_tasks + pending_tasks
        progress_percent = (
            round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0.0
        )
        is_complete = total_tasks > 0 and pending_tasks == 0

        return {
            "feature": feature_name,
            "directory": str(feature_dir),
            "has_spec": has_spec,
            "has_plan": has_plan,
            "has_tasks": has_tasks,
            "has_checklist": has_checklist,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "progress_percent": progress_percent,
            "is_complete": is_complete,
        }

    def validate_feature(self, feature_name: str) -> dict[str, Any]:
        """Validate a feature against CEF Quality Gates & SDD standards."""
        feature_dir = self.get_feature_dir(feature_name)
        errors: list[str] = []
        warnings: list[str] = []

        if not feature_dir.exists():
            return {
                "valid": False,
                "feature": feature_name,
                "errors": [f"Feature directory not found: {feature_dir}"],
                "warnings": warnings,
            }

        # Check required files
        for filename in ("spec.md", "plan.md", "tasks.md", "checklist.md"):
            p = feature_dir / filename
            if not p.exists():
                errors.append(f"{filename} missing from feature bundle.")

        # Content validations
        spec_path = feature_dir / "spec.md"
        if spec_path.exists():
            content = spec_path.read_text(encoding="utf-8")
            if "Problem Statement" not in content and "problem" not in content.lower():
                warnings.append("spec.md lacks a clear Problem Statement section.")
            if "Scenario" not in content and "Given" not in content:
                warnings.append("spec.md has no BDD acceptance criteria scenarios (Given/When/Then).")

        plan_path = feature_dir / "plan.md"
        if plan_path.exists():
            content = plan_path.read_text(encoding="utf-8")
            if "Architecture" not in content and "architecture" not in content.lower():
                warnings.append("plan.md lacks an Architecture Overview section.")
            if "Verification" not in content and "Testing" not in content:
                warnings.append("plan.md lacks a Testing and Verification Strategy.")

        tasks_path = feature_dir / "tasks.md"
        if tasks_path.exists():
            status = self.get_feature_status(feature_name)
            if status["total_tasks"] == 0:
                errors.append("tasks.md contains 0 actionable tasks.")

        return {
            "valid": len(errors) == 0,
            "feature": feature_name,
            "errors": errors,
            "warnings": warnings,
        }
