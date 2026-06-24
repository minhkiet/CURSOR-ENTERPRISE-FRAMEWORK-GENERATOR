---
description: On-Error Hook - Analyze error và suggest fix khi có error
trigger: khi có error, on error, lỗi xảy ra
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: on-error

## Mục tiêu
Analyze error, identify root cause, và suggest fix khi có error trong quá trình làm việc.

## Trigger
Tự động trigger khi phát hiện error trong quá trình làm việc.

## Workflow

### Bước 1: Error Collection
- [ ] Collect error message
- [ ] Collect stack trace
- [ ] Collect context (files, code)
- [ ] Collect recent actions

### Bước 2: Error Analysis
- [ ] Parse error type
- [ ] Identify error category
- [ ] Check known error patterns
- [ ] Identify potential causes

### Bước 3: Root Cause Analysis
- [ ] Apply root-cause-analysis skill
- [ ] Analyze error chain
- [ ] Identify primary cause
- [ ] Identify contributing factors

### Bước 4: Fix Suggestions
- [ ] Look up fix in knowledge base
- [ ] Check for similar errors in bugs.sqlite
- [ ] Generate fix suggestions
- [ ] Provide code examples

### Bước 5: Knowledge Update
- [ ] Add error to bugs.sqlite if new
- [ ] Update anti-patterns if needed
- [ ] Update documentation if needed

### Bước 6: Report
- [ ] Print error summary
- [ ] Print root cause
- [ ] Print fix suggestions
- [ ] Print related resources

## Error Categories
| Category | Examples | Fix Approach |
|----------|---------|-------------|
| Syntax | Missing semicolon, typo | Fix syntax |
| Type | Type mismatch, null | Add type guard |
| Import | Missing module | Install/import |
| Config | Wrong env, missing secret | Set config |
| Runtime | Null pointer, out of memory | Handle edge case |
| Build | Build failed | Fix build config |
| Test | Test failed | Fix code or test |
| Security | Vulnerability | Apply security fix |

## Liên kết
- [[../skills/root-cause-analysis]] - Root Cause Analysis Skill
- [[../skills/debug]] - Debug Skill
- [[../rules/memory-first]] - Memory First Rules
