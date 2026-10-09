# Windsurf Adapter

> **Tool:** Windsurf | **Version:** 1.0.0

---

## Cấu trúc

```
.windsurf/
├── rules/                   # Rules
│   ├── principles.md
│   ├── security.md
│   ├── code-quality.md
│   ├── architecture.md
│   └── git-workflow.md
├── skills/                 # Skills (if supported)
│   └── ...
└── config.json            # Windsurf configuration
```

## Cài đặt

```bash
# Tạo thư mục
mkdir -p ~/.windsurf/rules

# Copy rules
cp 01-core-rules/*.md ~/.windsurf/rules/

# Copy skills
cp -r 03-skills/*/SKILL.md ~/.windsurf/skills/
```

## Tool-Specific Notes

- Windsurf hỗ trợ `.windsurf/rules/` directory
- Rules được nạp tự động khi relevant
- Định dạng: Markdown thuần túy

## Rules Mapping

| Source | Destination |
|--------|------------|
| `01-core-rules/01-principles.md` | `.windsurf/rules/principles.md` |
| `01-core-rules/02-security.md` | `.windsurf/rules/security.md` |
| `01-core-rules/03-code-quality.md` | `.windsurf/rules/code-quality.md` |
| `01-core-rules/04-architecture.md` | `.windsurf/rules/architecture.md` |
| `01-core-rules/05-git-workflow.md` | `.windsurf/rules/git-workflow.md` |
