---
name: speckit-plan
description: "Generate technical blueprints and architecture plans (plan.md) mapping functional requirements into models, API contracts, dependencies, and testing strategies."
---

# SpecKit Plan Skill

> **Version:** 1.0.0 | **Phase:** Technical Planning & Architecture | **Output:** `plan.md`

---

## 1. Objective
Transform an approved `spec.md` into an actionable, robust technical design (`plan.md`). Ensure the architecture respects the project constitution, codebase patterns, and YAGNI simplicity.

---

## 2. Planning Structure

Every `plan.md` must contain:
1. **System Context & Flow**:
   - Architectural diagram showing component interaction.
   - Boundaries between domain logic, persistence, and external APIs.
2. **Data Models & Contracts**:
   - Concrete schemas, types, and interfaces.
   - Endpoint routes, payloads, status codes, and error formats.
3. **File Impact Map**:
   - Specific paths of files to be created or modified.
   - Blast radius assessment (ensuring modifications are strictly localized).
4. **Verification & Testing Strategy**:
   - Unit test scope (testing edge cases and validation rules).
   - Integration / E2E verification commands.
5. **Risk & Rollback Strategy**:
   - Potential failure modes and explicit rollback procedure.
