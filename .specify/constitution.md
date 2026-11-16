# Project Constitution

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
- **Runtime & Language Standards**: Define explicit versions (e.g., Python 3.10+, Node.js 20 LTS).
- **Dependency Policy**: Zero unvetted dependencies. Favor standard library and established core libraries.
- **Isolation of Concerns**: Domain logic must remain independent of external frameworks and delivery mechanisms.

---

## 3. Quality & Security Gates
- **Security Invariants**: Zero unescaped inputs (XSS/SQLi prevention), strict authentication/authorization checks, zero hardcoded secrets.
- **Quality Checks**: Automated linting, type-checking, and unit test suite must pass 100% on every pull request.
- **Documentation**: Code must be self-explanatory with concise docstrings for public APIs.
