# Vibe Code Framework — Installation & Sync Scripts

> **Version:** 1.1.0

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `install.ps1` | Install framework cho Windows và PowerShell Core |
| `sync-adapters.ps1` | Sync adapters cho tất cả tools |
| `sync-adapters.sh` | Sync adapters cho Unix |
| `validate.ps1` | Validate framework structure |
| `inventory.ps1` | Inventory và phân loại `.cursor` không destructive |
| `preflight.ps1` | Kiểm tra điều kiện nghiệm thu và lý do `BLOCKED` |
| `rollback-target.ps1` | Snapshot/restore/verify một target adapter được chỉ định |

---

## Usage

### Windows (PowerShell)

```powershell
# Install framework for Cursor
.\08-scripts\install.ps1 -Tool Cursor -SourcePath (Resolve-Path .).Path -TargetPath "C:\Projects\MyApp"

# Install for Claude Code
.\08-scripts\install.ps1 -Tool ClaudeCode -SourcePath (Resolve-Path .).Path -TargetPath "C:\Projects\MyApp"

# Install for all tools
.\08-scripts\install.ps1 -Tool All -SourcePath (Resolve-Path .).Path -TargetPath "C:\Projects\MyApp"

# Sync adapters
.\08-scripts\sync-adapters.ps1 -Tool Cursor -SourcePath (Resolve-Path .).Path -TargetPath "C:\Projects\MyApp"

# Validate framework
.\08-scripts\validate.ps1
```

### Unix (Bash/PowerShell Core)

```bash
# Make executable
chmod +x 08-scripts/*.sh

# Install
pwsh ./08-scripts/install.ps1 -Tool Cursor -SourcePath "$PWD" -TargetPath "/projects/my-app"

# Sync
pwsh ./08-scripts/sync-adapters.sh -Tool cursor -SourcePath "$PWD" -TargetPath "/projects/my-app"
```

## Execution input contract

Always provide the Resource Hub root as `-SourcePath` and the consumer project
as `-TargetPath` for install/sync. The canonical manifest is resolved from
`00-governance/resource-manifest.json` unless `-ManifestPath` is explicitly
provided. `inventory.ps1` is read-only and classifies the host `.cursor`
boundary; it does not migrate or delete resources.

```powershell
.\08-scripts\install.ps1 -Tool Cursor -SourcePath (Resolve-Path .).Path -TargetPath "C:\Projects\MyApp"
.\08-scripts\sync-adapters.ps1 -Tool Cursor -SourcePath (Resolve-Path .).Path -TargetPath "C:\Projects\MyApp"
.\08-scripts\inventory.ps1 -ProjectPath "C:\Projects\MyApp"
.\08-scripts\inventory.ps1 -ProjectPath "C:\Projects\MyApp" `
  -OutputPath ".\00-governance\records\cursor-inventory.json"
.\08-scripts\preflight.ps1 -FrameworkPath (Resolve-Path .).Path -ProjectPath "C:\Projects\MyApp"
# If `python` is a Windows Store shim, provide the approved interpreter:
.\08-scripts\preflight.ps1 -PythonPath "C:\path\to\venv\Scripts\python.exe"
# Safe additive Resource Hub operations can be checked independently from
# blocked whole-ecosystem .cursor migration:
.\08-scripts\preflight.ps1 -OperationalOnly

# Target-only rollback. Use a narrow affected directory, never the whole
# repository or `.cursor`; BackupPath must be outside the Resource Hub.
.\08-scripts\rollback-target.ps1 -Mode Snapshot `
  -TargetPath "C:\Projects\MyApp\.cursor\skills\example" `
  -BackupPath "C:\ReleaseBackups\CHG-0001-before"
.\08-scripts\rollback-target.ps1 -Mode Restore `
  -TargetPath "C:\Projects\MyApp\.cursor\skills\example" `
  -BackupPath "C:\ReleaseBackups\CHG-0001-before" -ConfirmRestore
.\08-scripts\rollback-target.ps1 -Mode Verify `
  -TargetPath "C:\Projects\MyApp\.cursor\skills\example" `
  -BackupPath "C:\ReleaseBackups\CHG-0001-before"
```

Khi project có `.venv\Scripts\python.exe`, `preflight.ps1` sẽ tự ưu tiên
environment này trước Windows Store shim và runtime nền. Environment `.venv/`
được loại khỏi Git; cài dev dependencies bằng:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Inventory output is a review queue, not a migration plan. Unknown resources
keep `reviewStatus=BLOCKED`, empty owner/source/dependency fields, and
`approvalRequired=true` until a real owner supplies evidence.

`-OperationalOnly` is a limited runtime/readiness gate for canonical Resource
Hub validation, tested adapters, builds, tests, and target-only rollback. A
`PASS` in this mode never approves migration and always returns
`migrationAllowed=false`; the normal whole-ecosystem verdict remains the
authoritative migration gate.

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
