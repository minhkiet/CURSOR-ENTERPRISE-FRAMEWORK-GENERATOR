# Workflow: Fix Bug - Sửa lỗi Bug

## Mục tiêu
Workflow chuẩn để fix bug hiệu quả.

## Trigger
Khi user báo cáo bug hoặc yêu cầu sửa lỗi.

## Workflow Steps

### Bước 1: Reproduce
- [ ] Understand bug description
- [ ] Reproduce bug
- [ ] Check bug-history.sqlite
- [ ] Document reproduction steps

### Bước 2: Analyze
- [ ] Read stack trace
- [ ] Identify root cause
- [ ] Check similar bugs
- [ ] Document root cause

### Bước 3: Fix
- [ ] Create fix
- [ ] Write unit test
- [ ] Verify fix works

### Bước 4: Update Memory
- [ ] Update bug-history.sqlite
- [ ] Add to bug patterns if applicable

## Liên kết
- [[../prompts/bug-fix]] - Bug Fix Prompt
- [[../skills/debug]] - Debug Skill
- [[../skills/root-cause-analysis]] - Root Cause Analysis
