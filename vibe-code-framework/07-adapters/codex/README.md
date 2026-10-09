# Codex Adapter — OpenAI Codex

> **Tool:** OpenAI Codex | **Version:** 1.0.0

---

## Cấu trúc

```
.agents/
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
└── agents/                # Agent personas
    ├── architect.md
    └── reviewer.md
```

## AGENTS.md

Codex sử dụng `AGENTS.md` làm single source of truth. File này chứa:

- Core principles
- Architecture rules
- Agent definitions
- Security guidelines

Xem: [`AGENTS.md`](../../AGENTS.md)

## Cài đặt

```bash
# Copy AGENTS.md
cp AGENTS.md /path/to/project/AGENTS.md

# Copy skills
cp -r 03-skills/*/SKILL.md /path/to/project/.agents/skills/

# Copy agents
cp -r 04-agents/*.md /path/to/project/.agents/agents/
```

## Tool-Specific Notes

- Codex đọc `AGENTS.md` trong project root
- Skills cần được đặt trong `.agents/skills/`
- Agent personas có thể được định nghĩa trong `AGENTS.md`

## Skills Mapping

| Source | Destination |
|--------|------------|
| `03-skills/create-feature/SKILL.md` | `.agents/skills/create-feature/SKILL.md` |
| `03-skills/create-api/SKILL.md` | `.agents/skills/create-api/SKILL.md` |
| `03-skills/create-ui/SKILL.md` | `.agents/skills/create-ui/SKILL.md` |
| `03-skills/database-migration/SKILL.md` | `.agents/skills/database-migration/SKILL.md` |
| `03-skills/code-review/SKILL.md` | `.agents/skills/code-review/SKILL.md` |
| `03-skills/debug-error/SKILL.md` | `.agents/skills/debug-error/SKILL.md` |
