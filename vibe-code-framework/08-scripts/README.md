# Vibe Code Framework — Installation & Sync Scripts

> **Version:** 1.1.0

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `install.ps1` | Install framework cho Windows |
| `install.sh` | Install framework cho Unix |
| `sync-adapters.ps1` | Sync adapters cho tất cả tools |
| `sync-adapters.sh` | Sync adapters cho Unix |
| `validate.ps1` | Validate framework structure |

---

## Usage

### Windows (PowerShell)

```powershell
# Install framework for Cursor
.\08-scripts\install.ps1 -Tool Cursor

# Install for Claude Code
.\08-scripts\install.ps1 -Tool ClaudeCode

# Install for all tools
.\08-scripts\install.ps1 -Tool All

# Sync adapters
.\08-scripts\sync-adapters.ps1 -Tool Cursor

# Validate framework
.\08-scripts\validate.ps1
```

### Unix (Bash/PowerShell Core)

```bash
# Make executable
chmod +x 08-scripts/*.sh

# Install
./08-scripts/install.sh --tool cursor

# Sync
./08-scripts/sync-adapters.sh --tool cursor
```

---

## Supported Tools

| Tool | Rules | Skills | Agents |
|------|-------|--------|--------|
| Cursor | `.cursor/rules/*.mdc` | `.cursor/skills/*/SKILL.md` | `.cursor/agents/*.md` |
| Claude Code | `.claude/rules/*.md` | `.claude/skills/*/SKILL.md` | `.claude/agents/*.md` |
| Codex | `AGENTS.md` | `.agents/skills/*/SKILL.md` | `AGENTS.md` |
| Copilot | `.github/copilot-instructions.md` | — | — |
| Windsurf | `.windsurf/rules/*.md` | — | — |
| Antigravity | `.antigravity/*.md` | — | — |

---

## Requirements

- PowerShell 5.0+ (Windows)
- Bash 4.0+ hoặc PowerShell Core (Unix)
- Git
