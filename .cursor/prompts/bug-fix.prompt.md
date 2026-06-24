---
description: Prompt chuan de sua bug - phan tich root cause truoc khi fix
trigger: bug fix, fix bug, loi, error
category: Development
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Bug Fix - Sửa lỗi Bug

## Mô tả
Prompt template chuẩn để sửa bug trong Cursor Enterprise Framework.

## Trigger Keywords
- "fix bug"
- "sửa lỗi"
- "bug fix"
- "lỗi"
- "error"
- "crash"

## Prompt Template

```markdown
# Bug Fix Workflow

## 1. BUG INFORMATION
- **Bug ID**: [BUG-ID]
- **Mô tả lỗi**: [Mô tả ngắn gọn]
- **Severity**: [Critical / High / Medium / Low]
- **Domain**: [Frontend / Backend / Database / AI / Infra]

## 2. REPRODUCTION STEPS
1. [Bước 1]
2. [Bước 2]
3. [Bước 3]

**Expected behavior**: [Mô tả kết quả mong đợi]
**Actual behavior**: [Mô tả kết quả thực tế]

## 3. CONTEXT LOADING
```
Yêu cầu: Chỉ load knowledge liên quan đến bug domain
- Bug domain: [Xác định domain]
- Skip: Tất cả domain không liên quan
- Memory: Kiểm tra bug-history trước
```

## 4. INVESTIGATION WORKFLOW

### Bước 1: Reproduce
- [ ] Reproduce được lỗi
- [ ] Xác định reproduction rate
- [ ] Ghi lại environment details

### Bước 2: Analyze
- [ ] Đọc stack trace
- [ ] Xác định root cause
- [ ] Check similar bugs trong bug-history.sqlite

### Bước 3: Identify
- [ ] Xác định file gây lỗi
- [ ] Xác định line number
- [ ] Xác định root cause category:
  - [ ] coding-error
  - [ ] design-flaw
  - [ ] configuration
  - [ ] dependency
  - [ ] environment
  - [ ] data
  - [ ] third-party

### Bước 4: Fix
- [ ] Tạo fix
- [ ] Viết unit test
- [ ] Test fix

## 5. OUTPUT FORMAT

### Root Cause Analysis
```
Category: [root cause category]
Root Cause: [mô tả root cause]
Confidence: [Low / Medium / High]
```

### Fix Description
```
Files Changed: [danh sách file]
Lines Added: [số dòng]
Lines Removed: [số dòng]
Approach: [mô tả approach]
```

### Verification
```
[ ] Fix được verify
[ ] Regression test passed
[ ] Cập nhật bug-history.sqlite
```

## 6. ANTI PATTERNS
- [ ] KHÔNG sửa triệt để, chỉ workaround
- [ ] KHÔNG ignore similar bugs đã có
- [ ] KHÔNG fix mà không viết test
- [ ] KHÔNG fix nhiều bugs trong một lần

## 7. BEST PRACTICES
- [ ] Sử dụng bug-history.sqlite để tránh repeat
- [ ] Tạo minimal reproduction case
- [ ] Viết test trước khi fix (TDD approach)
- [ ] Cập nhật documentation nếu cần
- [ ] Review code sau khi fix

## 8. LIÊN KẾT
- [[../skills/debug]] - Debug Skill
- [[../skills/root-cause-analysis]] - Root Cause Analysis
- [[../rules/memory-first]] - Memory First
- [[../rules/coding-standards]] - Coding Standards
- [[../memory/bug-history]] - Bug History (folder: bug-history/)
