---
description: Comprehensive test analysis skill covering functional, UI, integration, and e2e testing. Ensures code correctness through systematic test design and verification.
version: 1.0.0
created: 2026-08-03
tags: [testing, quality, functional, UI-test, integration, e2e, verification, QA]
role: mandatory
domains: [testing, quality, frontend, backend]
confidence:
  base: 0.80
  threshold: 0.80
  auto_select: true
triggers:
  - "test"
  - "testing"
  - "unit test"
  - "integration test"
  - "e2e test"
  - "end to end"
  - "ui test"
  - "component test"
  - "functional test"
  - "verify"
  - "assertion"
  - "test case"
  - "test coverage"
  - "regression"
  - "mock"
  - "fixture"
  - "spy"
  - "stub"
  - "tdd"
  - "bdd"
  - "vitest"
  - "jest"
  - "playwright"
  - "cypress"
  - "selenium"
  - "kiểm thử"
  - "đảm bảo chất lượng"
---

# Test Analysis Skill - Comprehensive Testing Guide

## Overview

This skill ensures code correctness through systematic test design, execution, and verification. Covers functional testing, UI testing, integration testing, and end-to-end testing.

## Test Categories

### 1. Functional Testing
- Unit tests for individual functions/modules
- Input/output verification
- Edge case handling
- Error condition testing

### 2. UI Testing
- Component rendering
- User interaction simulation
- Visual regression
- Accessibility (a11y)

### 3. Integration Testing
- API endpoint testing
- Database operations
- Service communication
- Data flow verification

### 4. E2E Testing
- Full user journey
- Cross-browser testing
- Performance benchmarks
- Security validation

## Test Design Principles

### AAA Pattern
```
Arrange -> Act -> Assert
```

### Given-When-Then
```
Given [precondition]
When [action]
Then [expected result]
```

### Test Naming Convention
```
[UnitOfWork]_[Scenario]_[ExpectedBehavior]
```

## Quality Gates

### Pre-Testing (§T.1)
- [ ] Test coverage baseline established
- [ ] Test environment configured
- [ ] Test data prepared
- [ ] Mock/stub strategy defined

### Post-Testing (§T.2)
- [ ] All tests pass
- [ ] Coverage meets threshold (>80%)
- [ ] No flaky tests
- [ ] Performance acceptable

## Tools & Frameworks

| Type | Tools |
|------|-------|
| Unit | Jest, Vitest, pytest, JUnit |
| UI | Playwright, Cypress, Testing Library |
| API | Postman, REST-assured, SuperTest |
| E2E | Playwright, Cypress, Selenium |
| Coverage | Istanbul, Coverage.py, JaCoCo |

## Anti-Patterns to Reject

- Tests without assertions
- Hardcoded values without fixtures
- Mocking everything (no real behavior)
- Brittle tests that break on refactor
- Tests that only test happy path
- Race conditions in async tests
