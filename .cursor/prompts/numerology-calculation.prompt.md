---
description: Prompt chuan de tinh Than So Hoc - so chu dao, so linh hon
trigger: numerology, than so hoc
category: Domain
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Numerology Calculation - Tính Thần Số Học

```markdown
# Numerology Calculation Workflow

## 1. INPUT
- **Họ tên**: [Full name]
- **Ngày sinh**: [DD/MM/YYYY]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/numerology/*
- knowledge/pdf/*
Load rules: numerology.mdc, pdf-engine.mdc
```

## 3. CALCULATION STEPS

### Số chủ đạo
- [ ] Tính tổng ngày sinh
- [ ] Rút gọn về 1-9 hoặc 11, 22, 33
- [ ] Diễn giải ý nghĩa

### Số linh hồn
- [ ] Trích xuất nguyên âm
- [ ] Tính tổng
- [ ] Diễn giải

### Số nhân cách
- [ ] Trích xuất phụ âm
- [ ] Tính tổng
- [ ] Diễn giải

### Số vận mệnh
- [ ] Tính từ họ tên đầy đủ
- [ ] Diễn giải

## 4. OUTPUT
- [ ] JSON data model
- [ ] PDF report generation

## 5. LIÊN KẾT
- [[../skills/pdf-generator]] - PDF Generator
- [[../rules/pdf-engine]] - PDF Engine Rules
```
