# Prompt: Bát Tự Calculation - Tính Bát Tự

```markdown
# Bát Tự Calculation Workflow

## 1. INPUT
- **Ngày sinh**: [DD/MM/YYYY]
- **Giờ sinh**: [Giờ]
- **Giới tính**: [Nam / Nữ]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/bazi/*
- knowledge/pdf/*
Load rules: bazi.mdc, pdf-engine.mdc
```

## 3. CALCULATION STEPS

### Tứ trụ
- [ ] Xác định Can Chi năm sinh
- [ ] Xác định Can Chi tháng sinh
- [ ] Xác định Can Chi ngày sinh
- [ ] Xác định Can Chi giờ sinh

### Ngũ hành
- [ ] Xác định Ngũ hành của mệnh
- [ ] Xác định tương sinh/tương khắc

### Cung mệnh
- [ ] An cung mệnh
- [ ] An sao chiếu

### Vận trình
- [ ] Xác định đại vận
- [ ] Xác định lưu niên vận

## 4. OUTPUT
- [ ] JSON data model
- [ ] PDF report generation
- [ ] Visualization

## 5. LIÊN KẾT
- [[../skills/pdf-generator]] - PDF Generator
- [[../rules/pdf-engine]] - PDF Engine Rules
```
