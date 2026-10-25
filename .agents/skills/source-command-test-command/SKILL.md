---
name: "source-command-test-command"
description: "Test - Chiến lược và implementation testing"
---

# source-command-test-command

Use this skill when the user asks to run the migrated source command `test-command`.

## Command Template

# Command: /test

## Mục tiêu
Thiết kế và implement chiến lược testing toàn diện.

## Trigger Keywords
- test
- testing
- viết test
- unit test
- integration test
- e2e test
- end to end test
- test strategy
- chiến lược test
- viết bài test
- write tests

## Workflow

### Bước 1: Testing Strategy
- [ ] Load testing rules
- [ ] Identify test pyramid (unit/integration/e2e)
- [ ] Select testing framework
- [ ] Define coverage targets
- [ ] Define test data strategy

### Bước 2: Unit Tests
- [ ] Test utilities và helpers
- [ ] Test business logic
- [ ] Test edge cases
- [ ] Test error paths
- [ ] Mock external dependencies

### Bước 3: Integration Tests
- [ ] Test database operations
- [ ] Test API endpoints
- [ ] Test message queues
- [ ] Test external services (mocked)

### Bước 4: E2E Tests
- [ ] Test critical user flows
- [ ] Test happy paths
- [ ] Test error recovery

### Bước 5: CI/CD Integration
- [ ] Add tests to CI pipeline
- [ ] Set up test reports
- [ ] Set up coverage reports

## Liên kết
- [[../prompts/testing-strategy]] - Testing Strategy Prompt
- [[../skills/testing-strategy]] - Testing Strategy Skill
- [[../rules/testing]] - Testing Rules
- [[../rules/tdd]] - TDD Rules
