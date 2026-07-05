# Cursor Enterprise Framework v5.0.0

> First official GUI release of the Cursor Enterprise Framework installer.
> Build date: **2026-07-04** — Branch-state build, no prior git tag.

## Overview

A clean re-build of the **Windows GUI installer** (`cursor-setup.exe`) together with the
**framework content bundle** (`cursor-setup.zip`). The installer extracts the full
`.cursor` framework to a user-selected folder with progress reporting and a built-in
sanity check.

## Assets

| File | Size | SHA-256 |
|------|-----:|---------|
| `cursor-setup.exe` | 412 KB | `1A6DA6CDA4B56BF10E94D7DDA62AAFC79231756AB4717830B7B7163D57AAFCA5` |
| `cursor-setup.zip` | 21.09 MB | `8BEC021A5799113D808EBE8AF81C34D9D42F9DD39B6D0F6A45D53B9D1E4B7322` |

The `Setup.exe` is a self-contained .NET 8 (Windows Forms) single-file executable that
runs on Windows 10/11 x64 — no .NET runtime required.

The `Setup.zip` contains the full framework payload: **605 files** under `.cursor/`.
The installer extracts `cursor-setup.zip` to the user-selected destination `.cursor/`
folder, copies an `.ico`, and verifies file counts.

## What's Inside (v5.0.0)

| Component | Files | Notes |
|-----------|------:|-------|
| `agents/` | 8 | `code-reviewer`, `frontend-architect`, `backend-reviewer`, `database-reviewer`, `api-designer`, `security-auditor`, `test-engineer`, `web-performance-auditor` |
| `rules/` | 42 | Architecture, security, frontend, backend, databases, deployment, testing, performance, … |
| `skills/` | 42 | karpathy-coding, ponytail, frontend-review, frontend-redesign, full-output, bazi, vietnam-payment-review, etc. |
| `commands/` | 28 | Agent slash-commands (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`) |
| `prompts/` | 31 | Reusable prompt templates |
| `workflows/` | 11 | n8n / Trigger.dev / Temporal pattern docs |
| `hooks/` | 15 | Lifecycle hooks and webhook handlers |
| `knowledge/` | 329 | Domain knowledge pack (multi-tenant, RLS, billing, CRM, AI, …) |
| `templates/` | 6 | Bazi, blog, CRM, numerology, portfolio, sale — Vue/Vite scaffolds |
| `scripts/` | 34 | Python automation scripts |
| `memory/` | 14 | Project memories & notes |
| `references/` | 4 | Checklists |
| `cache/` | 36 | Pre-computed dependency / syntax caches |

**Total: 605 files, 13 categories.**

## Highlights vs previous

- **GUI refresh** (WinForms, `setup.ico`-branded, progress bar, real-time extraction log)
- **Self-contained build** — `PublishSingleFile` + `SelfContained=true`, no .NET dependency on the target machine
- **ZIP sidecar architecture** — same `.zip` payload can be reused by CI / PowerShell `quick-install.ps1`
- **Pre-flight checks** — prompt elevation only when `Program Files` is targeted; friendly error if `.cursor` already exists
- **Count verification** — installer asserts file count against the manifest

## Install

1. Download `cursor-setup.exe` and `cursor-setup.zip` (keep them in the same folder).
2. Run `cursor-setup.exe`.
3. Pick a destination folder (the installer recreates `.cursor/` inside it).
4. Wait for the progress bar; click **Finish** when done.

## Verify

After installation:

```bash
ls .cursor/rules | head
ls .cursor/skills
ls .cursor/agents
```

You should see **42 rules**, **42 skills**, **8 agents** respectively.

## Compatibility

- **OS**: Windows 10 (1809+) / Windows 11 x64
- **Architecture**: x64 (no ARM64 build yet — added to v5.1 roadmap)
- **No .NET runtime required** (self-contained)

## Contributing

Issues / PRs: <https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR>

---

**Full Changelog**: <https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/commits/main>
