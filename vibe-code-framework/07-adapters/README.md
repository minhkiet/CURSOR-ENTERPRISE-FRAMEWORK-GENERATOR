# Adapter Index

> **Version:** 1.0.0 | **Updated:** 2026-10-09

---

## Tổng quan

`07-adapters/` chứa các script để convert nội dung từ thư mục nguồn (01-core-rules, 03-skills, 04-agents) sang định dạng phù hợp cho từng tool.

## Tool Conventions

### Cursor

| Source | Destination | Format |
|--------|-------------|--------|
| 01-core-rules/* | .cursor/rules/*.mdc | Markdown (thay .md → .mdc) |
| 03-skills/*/SKILL.md | .cursor/skills/*/SKILL.md | Markdown |
| 04-agents/*.md | .cursor/agents/*.md | Markdown |

### Claude Code

| Source | Destination | Format |
|--------|-------------|--------|
| 01-core-rules/* | .claude/rules/*.md | Markdown |
| 03-skills/*/SKILL.md | .claude/skills/*/SKILL.md | Markdown |
| 04-agents/*.md | .claude/agents/*.md | Markdown |

### OpenAI Codex

| Source | Destination | Format |
|--------|-------------|--------|
| 01-core-rules/* | Sections in AGENTS.md | Markdown |
| 03-skills/*/SKILL.md | .agents/skills/*/SKILL.md | Markdown |
| 04-agents/*.md | Sections in AGENTS.md | Markdown |

### GitHub Copilot

| Source | Destination | Format |
|--------|-------------|--------|
| 01-core-rules/* | Sections in .github/copilot-instructions.md | Markdown |

---

## Adapter Structure

```
07-adapters/
├── cursor/
│   ├── rules/                    # .cursor/rules/*.mdc
│   ├── skills/                  # .cursor/skills/
│   └── agents/                  # .cursor/agents/
├── claude-code/
│   ├── rules/                   # .claude/rules/
│   ├── skills/                 # .claude/skills/
│   └── agents/                 # .claude/agents/
├── codex/
│   └── skills/                  # .agents/skills/
├── copilot/
│   └── instructions/           # .github/copilot-instructions.md
├── windsurf/
│   └── rules/                  # .windsurf/rules/
└── antigravity/
    └── rules/                  # Tool-specific
```

## Sync Strategy

### 1. Convert Format
- Thay đổi extension (.md → .mdc)
- Thêm tool-specific frontmatter nếu cần

### 2. Update Paths
- Cập nhật đường dẫn tương đối
- Thêm tool-specific imports

### 3. Validate
- Kiểm tra file được tạo
- Chạy lint nếu có

---

## Quick Start

```powershell
# Sync all adapters
.\08-scripts\sync-adapters.ps1

# Sync specific tool
.\08-scripts\sync-adapters.ps1 -Tool Cursor

# Sync specific category
.\08-scripts\sync-adapters.ps1 -Category rules
```

```bash
# Unix
./08-scripts/sync-adapters.sh --tool cursor
```
