# Prompt: Tử Vi Calculation - Tính Tử Vi

```markdown
# Tử Vi Calculation Workflow

## 1. INPUT
- **Ngày sinh**: [DD/MM/YYYY]
- **Giờ sinh**: [Giờ]
- **Giới tính**: [Nam / Nữ]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/tuvi/*
- knowledge/pdf/*
Load rules: tuvi.mdc, pdf-engine.mdc
```

## 3. CALCULATION STEPS

### Lá số
- [ ] Xác định điền an
- [ ] An cung mệnh
- [ ] An sao chiếu

### Vận trình
- [ ] Xác định đại vận
- [ ] Xác định tiểu vận
- [ ] Xác định lưu niên

### Diễn giải
- [ ] Tổng hợp lá số
- [ ] Diễn giải vận trình
- [ ] Đưa ra khuyến nghị

## 4. OUTPUT
- [ ] JSON data model
- [ ] PDF report generation
- [ ] Visualization

## 5. LIÊN KẾT
- [[../skills/pdf-generator]] - PDF Generator
- [[../rules/pdf-engine]] - PDF Engine Rules
```
