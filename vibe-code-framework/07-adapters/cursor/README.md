# Cursor Adapter — Rules

> **Version:** 1.0.0 | **Tool:** Cursor

---

## Cấu trúc Adapter

```
.cursor/
├── rules/
│   ├── core.mdc              ← 01-principles.md
│   ├── security.mdc          ← 02-security.md
│   ├── code-quality.mdc      ← 03-code-quality.md
│   ├── architecture.mdc      ← 04-architecture.md
│   └── git-workflow.mdc      ← 05-git-workflow.md
└── AGENTS.md                 ← (root file)
```

## Cài đặt

```powershell
# Từ thư mục vibe-code-framework
Copy-Item -Recurse 07-adapters\cursor\rules\* <your-project>\.cursor\rules\
Copy-Item 07-adapters\cursor\AGENTS.md <your-project>\.cursor\AGENTS.md
```

## Tự động sync

```powershell
.\08-scripts\sync-adapters.ps1 -Tool Cursor
```

---

## Rules Mapping

| Source | Cursor Destination |
|--------|-------------------|
| `01-core-rules/01-principles.md` | `.cursor/rules/core.mdc` |
| `01-core-rules/02-security.md` | `.cursor/rules/security.mdc` |
| `01-core-rules/03-code-quality.md` | `.cursor/rules/code-quality.mdc` |
| `01-core-rules/04-architecture.md` | `.cursor/rules/architecture.mdc` |
| `01-core-rules/05-git-workflow.md` | `.cursor/rules/git-workflow.mdc` |

## Tool-Specific Notes

- Cursor hỗ trợ `.mdc` (Markdown with Frontmatter)
- Frontmatter cho phép metadata như `description`, `trigger`
- Rules được tự động nạp khi relevant
