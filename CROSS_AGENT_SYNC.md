# Cross-Agent Vibe Coding Sync Protocol

> **Version 1.0.0** | Multi-Agent Framework Compatibility

This document describes the cross-agent synchronization protocol for vibe coding agents using the Cursor Enterprise Framework.

---

## Overview

The framework supports four vibe coding agents with unified skill and rule management:

| Agent | Identifier | Gate Prefix | Platform |
|-------|-----------|-------------|----------|
| Cursor IDE | `cursor` | `K` | Local IDE |
| Codex | `codex` | `CX` | Cloud (origin.cursor.com) |
| Claude Code | `claude-code` | `C` | @cursor/codex |
| Grok | `grok` | `G` | x.com/grok |

---

## Agent Detection

Agents are auto-detected via environment variables:

```python
# Priority order (first match wins)
if os.getenv("CURSOR_IDE") or os.getenv("CURSOR_PROJECT"):
    return "cursor"
elif os.getenv("CODEX_ENABLED") or os.getenv("ORIGIN_HOST"):
    return "codex"
elif os.getenv("CLAUDE_IDE") or os.getenv("CLAUDE_API_KEY"):
    return "claude-code"
elif os.getenv("GROK_API_KEY"):
    return "grok"
else:
    return "unknown"  # Falls back to Cursor
```

**Implementation:** `cursor_framework/agent_integration.py` → `AgentDetector.detect()`

---

## Skill Compatibility Matrix

### Universal Skills (work on all agents)

These skills require no modification across agents:

| Skill | Cursor | Codex | Claude Code | Grok |
|-------|:------:|:-----:|:-----------:|:----:|
| karpathy-coding | ✅ | ✅ | ✅ | ✅ |
| frontend-taste | ✅ | ✅ | ✅ | ✅ |
| frontend-review | ✅ | ✅ | ✅ | ✅ |
| full-output | ✅ | ✅ | ✅ | ✅ |
| security-review | ✅ | ✅ | ✅ | ✅ |
| test-analysis | ✅ | ✅ | ✅ | ✅ |
| perf-optimization | ✅ | ✅ | ✅ | ✅ |
| stability | ✅ | ✅ | ✅ | ✅ |
| data-quality | ✅ | ✅ | ✅ | ✅ |

### Agent-Specific Skills

| Skill | Cursor Only | Codex Only | Claude Code Only | Grok Only |
|-------|:-----------:|:----------:|:----------------:|:----------:|
| ponytail | ✅ | ✅ | - | - |
| frontend-redesign | ✅ | ✅ | - | - |
| vietnam-payment-review | ✅ | ✅ | - | - |
| claude-specific | - | - | ✅ | - |
| grok-specific | - | - | - | ✅ |

---

## Gate System

### Universal Gates (U.1-U.7 + §X + §Y)

All agents support these universal gates:

```
PRE-CODE:
  U.1  Think Before Code
  U.2  Simplicity Check  
  U.3  Surgical Scope
  U.4  Goal Definition

POST-CODE:
  U.5  Implementation Verification
  U.6  Simplicity Re-Check
  U.7  Goal Achievement
  §X   Verify Before Deliver
  §Y   Receive Feedback
```

### Agent-Specific Gates

| Agent | Pre-Gates | Post-Gates |
|-------|-----------|------------|
| Cursor | K.1-K.4 | K.5-K.7 |
| Codex | CX.1-CX.4 | CX.5-CX.7 |
| Claude Code | C.1-C.4 | C.5-C.7 |
| Grok | G.1-G.4 | G.5-G.7 |

---

## Directory Structure

```
workspace/
├── .cursor/          # Cursor IDE + Codex (shared)
│   ├── skills/       # Universal + Cursor/Codex skills
│   ├── rules/        # Rule files
│   └── agents/       # Agent personas
├── .claude/          # Claude Code specific
│   ├── skills/       # Claude-specific skills
│   └── rules/
└── .grok/            # Grok specific
    ├── skills/       # Grok-specific skills
    └── rules/
```

**Key principle:** Agent-specific skills go in the agent's own directory. Universal skills can live in any directory and are searched across all.

---

## Skill Manifest Format

Each skill includes a `manifest.json` or YAML frontmatter for cross-agent compatibility:

```yaml
---
name: frontend-taste
version: 1.0.0
compatible_agents: [universal]
primary_agent: cursor
gate_prefix: U
tags: [frontend, design, landing]
---
```

### Manifest Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill identifier |
| `version` | string | Yes | Semantic version |
| `compatible_agents` | string[] | Yes | List of compatible agents (`universal` = all) |
| `primary_agent` | string | Yes | Primary agent for this skill |
| `gate_prefix` | string | No | Override gate prefix |
| `tags` | string[] | No | Search tags |
| `triggers` | string[] | No | Keyword triggers |

---

## Sync Mechanism

### Conflict Resolution

```
Priority order (highest first):
1. Agent-specific config
2. Shared config
3. Framework defaults
```

### Sync Files

| File | Location | Purpose |
|------|----------|---------|
| `agent-manifest.json` | `{agent_path}/` | Records which agent installed what |
| `skills-manifests/` | `.cursor/skills/` | Skill metadata for all agents |
| `CROSS_AGENT_SYNC.md` | workspace root | This document |

### Export Manifest

```python
from cursor_framework.skills.skill_registry import create_cross_agent_registry

registry = create_cross_agent_registry()

# Export all manifests
count = registry.export_all_manifests(".cursor/skills/manifests/")
print(f"Exported {count} manifests")

# Export single manifest
manifest = registry.create_manifest("frontend-taste")
registry.export_manifest(manifest, format="json", output_path="manifest.json")
```

---

## Installation

### Single Agent

```bash
# Cursor IDE (default)
python -m cursor_framework install --agent cursor

# Codex
python -m cursor_framework install --agent codex

# Claude Code
python -m cursor_framework install --agent claude-code

# Grok
python -m cursor_framework install --agent grok
```

### All Agents

```bash
python -m cursor_framework install --all-agents
```

### Python API

```python
from cursor_framework.skills.skill_registry import create_cross_agent_registry

registry = create_cross_agent_registry()

# Detect current agent
agent = registry.detect_agent()
print(f"Detected: {agent.value}")  # cursor, codex, claude-code, grok, unknown

# Get compatible skills
skills = registry.get_compatible_skills("claude-code")
for skill in skills:
    print(f"  - {skill.name} (confidence: {skill.confidence})")

# Search skills
results = registry.search_skills("frontend design")
for manifest, score in results:
    print(f"  {manifest.name}: {score:.2f}")
```

---

## Known Limitations

| Agent | Limitation | Workaround |
|-------|-----------|------------|
| Claude Code | Different skills path (`.claude/`) | Use `--agent claude-code` |
| Grok | Limited MCP support | Use universal gates only |
| Codex | Cloud-only context | Export context to local file |
| All agents | Skill file format differences | Use manifest format |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-09-29 | Initial cross-agent support |

---

## References

- [Cursor Enterprise Framework README](cursor_framework/README.md)
- [Agent Integration Module](cursor_framework/agent_integration.py)
- [Skill Discovery Module](cursor_framework/skill_discovery.py)
- [Cross-Agent Skill Registry](cursor_framework/skills/skill_registry.py)
- [karpathy-coding Skill](.cursor/skills/code_karpathy/SKILL.md)
