# Google Antigravity Adapter

> **Tool:** Google Antigravity (Gemini) | **Version:** 1.0.0

---

## Cấu trúc

```
# Workspace-level rules (trong project)
# Global rules (trong ~/.antigravity/)

antigravity-rules/
├── workspace.md             # Workspace-specific rules
├── global.md              # Global rules
├── principles.md          # Core principles
├── security.md           # Security guidelines
└── architecture.md      # Architecture guidelines
```

## Cài đặt

```bash
# Workspace rules
mkdir -p /path/to/project/.antigravity
cp antigravity-rules/* /path/to/project/.antigravity/

# Global rules
mkdir -p ~/.antigravity
cp antigravity-rules/* ~/.antigravity/
```

## Tool-Specific Notes

- Antigravity hỗ trợ workspace-level và global rules
- Có thể cấu hình qua `antigravity.json`
- Định dạng: Markdown

## Rules Mapping

| Source | Destination |
|--------|------------|
| `01-core-rules/01-principles.md` | `.antigravity/principles.md` |
| `01-core-rules/02-security.md` | `.antigravity/security.md` |
| `01-core-rules/03-code-quality.md` | `.antigravity/code-quality.md` |
| `01-core-rules/04-architecture.md` | `.antigravity/architecture.md` |
| `01-core-rules/05-git-workflow.md` | `.antigravity/git-workflow.md` |

## Configuration Example

```json
{
  "rules": {
    "workspace": ".antigravity/workspace.md",
    "global": ".antigravity/global.md"
  },
  "skills": {
    "enabled": true,
    "path": ".antigravity/skills"
  }
}
```
