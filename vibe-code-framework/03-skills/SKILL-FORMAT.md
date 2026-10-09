# SKILL.md — Standard Format

> **Version:** 1.0.0 | **Skill:** [skill-name]

---

## Metadata

```yaml
name: create-feature
description: Tạo feature mới từ spec đến implementation
category: development
triggers:
  - "tạo feature"
  - "build feature"
  - "implement feature"
  - "add new feature"
version: 1.0.0
gates:
  - pre
  - post
requires:
  - principles
  - code-quality
```

---

## SKILL.md Format

Mỗi SKILL.md phải có các phần sau:

### 1. Header với Metadata

```markdown
# Create Feature Skill

**Version:** 1.0.0  
**Category:** Development  
**Triggers:** tạo feature, implement, build  
**Gates:** Pre-check, Post-check
```

### 2. Mục tiêu (Goal)

Mô tả ngắn gọn skill này làm gì.

### 3. Trigger Conditions

Khi nào skill này được kích hoạt.

### 4. Pre-Check Gates

Các bước kiểm tra **TRƯỚC KHI** bắt đầu implementation.

### 5. Process Steps

Các bước thực hiện, có thể bao gồm sub-skills.

### 6. Post-Check Gates

Các bước kiểm tra **SAU KHI** implementation để đảm bảo chất lượng.

### 7. Output

Kết quả mong đợi của skill.

### 8. Error Handling

Cách xử lý khi có lỗi.

---

## Gate Definition

### Pre-Check Gates

Kiểm tra trước khi bắt đầu:

```
┌─────────────────────────────────────────────────────────────┐
│ Pre-Check Gates                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Requirements Clear?                                     │
│     □ Đã hiểu rõ requirement chưa?                         │
│     □ Có spec/PRDs đầy đủ?                                │
│     □ Đã xác định acceptance criteria?                     │
│                                                             │
│  2. Design Approved?                                        │
│     □ Kiến trúc đã được approve?                          │
│     □ API contract đã finalize?                           │
│     □ Database schema đã approve?                          │
│                                                             │
│  3. Dependencies Known?                                     │
│     □ Cần tạo migration?                                   │
│     □ Cần tạo API mới?                                    │
│     □ Cần tạo UI components?                               │
│                                                             │
│  4. Environment Ready?                                       │
│     □ Code đã sync?                                        │
│     □ Tests chạy được?                                     │
│     □ Build được?                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Post-Check Gates

Kiểm tra sau khi implement:

```
┌─────────────────────────────────────────────────────────────┐
│ Post-Check Gates                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Code Quality                                            │
│     □ Lint passed?                                          │
│     □ Type check passed?                                    │
│     □ Format correct?                                        │
│                                                             │
│  2. Tests                                                   │
│     □ Unit tests passed?                                    │
│     □ Integration tests passed?                             │
│     □ Coverage acceptable?                                   │
│                                                             │
│  3. Functionality                                            │
│     □ Feature hoạt động đúng?                             │
│     □ Edge cases handled?                                   │
│     □ Error handling correct?                               │
│                                                             │
│  4. Security                                                │
│     □ No secrets exposed?                                  │
│     □ Input validated?                                      │
│     □ SQL injection protected?                               │
│                                                             │
│  5. Documentation                                           │
│     □ Code commented if needed?                             │
│     □ README updated?                                       │
│     □ API docs updated?                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Example SKILL.md

```markdown
# Create Feature

**Version:** 1.0.0  
**Triggers:** tạo feature, implement feature, add new feature

---

## Goal

Tạo feature mới từ specification đến implementation hoàn chỉnh, đảm bảo:
- Chất lượng code theo standards
- Test coverage đầy đủ
- Documentation cần thiết

## Trigger Conditions

Skill này được kích hoạt khi:
- User yêu cầu tạo feature mới
- User muốn implement một tính năng cụ thể
- User muốn thêm functionality vào hệ thống

## Pre-Check Gates

### P.1: Requirements Understanding
- [ ] Đã đọc và hiểu requirements
- [ ] Đã xác định acceptance criteria
- [ ] Đã clarify nếu có ambiguous points

### P.2: Design Review
- [ ] Đã review kiến trúc liên quan
- [ ] Đã xác định các components cần tạo
- [ ] Đã review API contracts nếu cần

### P.3: Environment Check
- [ ] Branch đúng và update
- [ ] Không có uncommitted changes trong feature branch
- [ ] Tests pass ở current state

## Process Steps

### Step 1: Create Spec

```markdown
# Feature: [Tên Feature]

## Overview
[Mô tả ngắn về feature]

## Requirements
1. [Requirement 1]
2. [Requirement 2]

## Acceptance Criteria
- [ ] AC1: [Criteria 1]
- [ ] AC2: [Criteria 2]

## Technical Design
### Components
- [Component 1]
- [Component 2]

### API Endpoints
- `POST /api/resource` - Create
- `GET /api/resource/:id` - Read

### Database
- Table: [table_name]
  - id: UUID
  - ...

## Out of Scope
- [Item 1]
- [Item 2]
```

### Step 2: Implement Domain Layer

1. Create entity
2. Create repository interface
3. Create domain service if needed

### Step 3: Implement Application Layer

1. Create DTOs
2. Create use case
3. Implement repository

### Step 4: Implement Infrastructure Layer

1. Create database migration
2. Implement repository
3. Create external service adapters

### Step 5: Implement Presentation Layer

1. Create API controller
2. Add validation
3. Add error handling

### Step 6: Write Tests

1. Unit tests for domain
2. Unit tests for use case
3. Integration tests for API

## Post-Check Gates

### C.1: Code Quality
- [ ] `npm run lint` passed
- [ ] `npm run type-check` passed
- [ ] No console.log/debugger left

### C.2: Tests
- [ ] Unit tests: all passed
- [ ] Integration tests: all passed
- [ ] Coverage: > 80%

### C.3: Functionality
- [ ] Feature works as specified
- [ ] Edge cases handled
- [ ] Error handling correct

### C.4: Security
- [ ] No hardcoded secrets
- [ ] Input validated
- [ ] SQL injection protected

### C.5: Documentation
- [ ] Code self-documenting
- [ ] README updated if needed
- [ ] API docs updated

## Output

- Feature hoàn chỉnh
- Tests passing
- PR ready for review

## Error Handling

| Error | Response |
|-------|----------|
| Requirements unclear | Ask user for clarification |
| Design issue | Propose alternatives |
| Test failure | Debug and fix |
| Build failure | Check dependencies |
```
