# Copilot Adapter — GitHub Copilot

> **Tool:** GitHub Copilot | **Version:** 1.0.0

---

## Cấu trúc

```
.github/
├── copilot-instructions.md     # Main instructions file
└── instructions/              # Additional instruction files
    ├── rules.md               # Core rules
    ├── security.md           # Security guidelines
    └── workflow.md           # Workflow guidelines
```

## copilot-instructions.md

Copilot sử dụng `.github/copilot-instructions.md` làm main instructions file. Đây là tổng hợp của:

- Core principles (YAGNI, KISS, DRY)
- Security rules
- Architecture guidelines
- Git workflow
- Coding standards

## Cài đặt

```bash
# Copy main instructions
cp .github/copilot-instructions.md /path/to/project/.github/

# Hoặc tạo mới
cat > /path/to/project/.github/copilot-instructions.md << 'EOF'
# Copilot Instructions

[Các rules từ 01-core-rules/*]
EOF
```

## Tool-Specific Notes

- Copilot chỉ đọc một file instructions chính
- Không hỗ trợ multi-file skill như Cursor
- Nên tổng hợp tất cả rules vào một file

## Content Structure

```markdown
# Copilot Instructions

## Core Principles
- YAGNI
- KISS
- DRY

## Security Rules
- No hardcoded secrets
- Input validation
- SQL injection prevention

## Architecture
- Clean Architecture
- Dependency Injection

## Git Workflow
- Branch naming
- Commit format
- PR guidelines

## Code Quality
- Naming conventions
- Error handling
- Testing strategy
```
