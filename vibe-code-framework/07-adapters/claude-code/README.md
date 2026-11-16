# Claude Code Adapter

> **Tool:** Claude Code | **Version:** 1.0.0

---

## Cấu trúc

```
.claude/
├── rules/                   # Rules (source format)
│   ├── 01-principles.md
│   ├── 02-security.md
│   ├── 03-code-quality.md
│   ├── 04-architecture.md
│   └── 05-git-workflow.md
├── skills/                 # Skills
│   ├── create-feature/
│   │   └── SKILL.md
│   ├── create-api/
│   │   └── SKILL.md
│   ├── create-ui/
│   │   └── SKILL.md
│   ├── database-migration/
│   │   └── SKILL.md
│   ├── code-review/
│   │   └── SKILL.md
│   └── debug-error/
│       └── SKILL.md
└── agents/                 # Agent personas
    ├── architect.md
    └── reviewer.md
```

## Cài đặt

```bash
# Từ vibe-code-framework
cp -r 01-core-rules/* ~/.claude/rules/
cp -r 03-skills/*/SKILL.md ~/.claude/skills/
cp -r 04-agents/*.md ~/.claude/agents/

# Hoặc dùng sync script
./08-scripts/sync-adapters.sh --tool claude
```

## Rules Mapping

| Source | Destination |
|--------|------------|
| `01-core-rules/01-principles.md` | `.claude/rules/01-principles.md` |
| `01-core-rules/02-security.md` | `.claude/rules/02-security.md` |
| `01-core-rules/03-code-quality.md` | `.claude/rules/03-code-quality.md` |
| `01-core-rules/04-architecture.md` | `.claude/rules/04-architecture.md` |
| `01-core-rules/05-git-workflow.md` | `.claude/rules/05-git-workflow.md` |

## Skills Mapping

| Source | Destination |
|--------|------------|
| `03-skills/create-feature/SKILL.md` | `.claude/skills/create-feature/SKILL.md` |
| `03-skills/create-api/SKILL.md` | `.claude/skills/create-api/SKILL.md` |
| `03-skills/create-ui/SKILL.md` | `.claude/skills/create-ui/SKILL.md` |
| `03-skills/database-migration/SKILL.md` | `.claude/skills/database-migration/SKILL.md` |
| `03-skills/code-review/SKILL.md` | `.claude/skills/code-review/SKILL.md` |
| `03-skills/debug-error/SKILL.md` | `.claude/skills/debug-error/SKILL.md` |

## Tool-Specific Notes

- Claude Code sử dụng `.md` thuần túy (không có frontmatter đặc biệt)
- Rules được nạp từ `.claude/rules/`
- Skills được nạp từ `.claude/skills/`

---

## Persistent Memory (claude-mem Integration)

Adapter này tích hợp trực tiếp với engine [claude-mem](https://github.com/thedotmack/claude-mem) để duy trì trí nhớ và nén lịch sử phiên làm việc:

### 1. Cài đặt plugin
```bash
claude plugin marketplace add thedotmack/claude-mem
claude plugin install claude-mem
```
Hoặc chạy script tự động:
```powershell
.\install-claude-mem.ps1
```

### 2. Nguyên lý hoạt động
- **Hooks tự động**: Tự động bắt sự kiện `SessionStart`, `PostToolUse`, và `SessionEnd`.
- **Background Worker**: Nén dữ liệu raw tool outputs thành ~500 token semantic observations, lưu vào SQLite (`~/.claude-mem/claude-mem.db`).
- **Dashboard xem lại**: Truy cập Web UI tại `http://localhost:37777` để duyệt memory stream.
- **MCP Server**: Có thể chia sẻ bộ nhớ cho Cursor / Antigravity qua file `mcp/mcp_config.json`.
