---
description: Fix Bug - Sửa lỗi bug với root cause analysis
trigger: fix bug, sửa lỗi, fix error, fix issue, bug fix, lỗi, error
category: Development
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /fix

## Mục tiêu
Sửa lỗi bug với phân tích root cause trước khi fix.

## Trigger Keywords
- fix bug
- sửa lỗi
- fix error
- fix issue
- bug fix
- lỗi
- error
- không hoạt động
- not working

## Workflow

### Bước 1: Memory First
- [ ] Check `memory/bugs.sqlite` cho known bugs tương tự
- [ ] Check `bug-history/` cho patterns đã biết
- [ ] Check recent fixes trong session
- [ ] Load related skill (root-cause-analysis)

### Bước 2: Bug Investigation
- [ ] Gather error information (error message, stack trace, logs)
- [ ] Reproduce the bug
- [ ] Identify affected files và components
- [ ] Analyze root cause
- [ ] Determine fix strategy

### Bước 3: Root Cause Analysis
- [ ] Apply root-cause-analysis skill
- [ ] Identify primary cause
- [ ] Identify contributing factors
- [ ] Document the root cause

### Bước 4: Fix Implementation
- [ ] Apply the fix
- [ ] Write regression tests
- [ ] Update existing tests nếu cần
- [ ] Run linters

### Bước 5: Verification
- [ ] Verify fix resolves the issue
- [ ] Run full test suite
- [ ] Check for side effects
- [ ] Verify no regression in related features

### Bước 6: Documentation
- [ ] Update `memory/bugs.sqlite` với bug details
- [ ] Document the fix trong code comments
- [ ] Update knowledge base nếu cần
- [ ] Create ADR nếu fix dẫn đến architecture change

## Liên kết
- [[../workflows/fix-bug]] - Fix Bug Workflow
- [[../prompts/bug-fix]] - Bug Fix Prompt
- [[../skills/root-cause-analysis]] - Root Cause Analysis Skill
- [[../skills/debug]] - Debug Skill
