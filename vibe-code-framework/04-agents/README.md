# Agents Index

> **Version:** 1.0.0 | **Updated:** 2026-10-09

---

## Tổng quan

`04-agents/` chứa các agent personas dùng chung cho mọi Vibe Coding tool.

## Agent Personas

| Agent | Mô tả | Triggers |
|-------|--------|----------|
| [architect.md](./architect.md) | Solution Architect - thiết kế kiến trúc | thiết kế, architecture, system design |
| [frontend.md](./frontend.md) | Frontend Engineer - Vue/React specialist | frontend, ui, component |
| [backend.md](./backend.md) | Backend Engineer - API/Database | backend, api, server |
| [database.md](./database.md) | Database Engineer - Schema/Migration | database, migration, query |
| [reviewer.md](./reviewer.md) | Code Reviewer - Quality assurance | review, check, audit |

## Ánh xạ sang tool

| Tool | Agent File | Format |
|------|------------|--------|
| Cursor | `.cursor/agents/` | Markdown |
| Claude Code | `.claude/agents/` | Markdown |
| Codex | `AGENTS.md` | Section trong AGENTS.md |
| Copilot | `.github/copilot-instructions.md` | Section |
