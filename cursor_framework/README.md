# Cursor Enterprise Framework - Python Library

A comprehensive Python library supporting the Cursor Enterprise Framework rules and skills. This library provides utilities for context routing, memory management, token optimization, and automatic skill discovery.

## Features

- **Context Router**: Intelligent intent classification and skill routing
- **Memory Manager**: Memory-first context management with tiered architecture
- **Token Optimizer**: Token usage optimization for LLM interactions
- **Skill Discovery**: Automatic skill detection and pre/post-review gates
- **Code Review**: Frontend code review utilities
- **Rules/Skills Parser**: Parse and validate .mdc rule and skill files
- **Utilities**: Text, file, code, HTTP, and security utilities

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from cursor_framework import ContextRouter, MemoryManager, SkillDiscovery

# Route a request to appropriate skill
router = ContextRouter()
route = router.route("Create a landing page for SaaS product")
print(f"Skill: {route.skill.value}, Confidence: {route.confidence}")

# Manage context with memory
memory = MemoryManager()
memory.store("project_info", {"name": "myapp"}, tier=MemoryTier.SESSION)
context = memory.retrieve("project_info")

# Discover applicable skills
discovery = SkillDiscovery()
skills = discovery.detect_skills("Build a landing page with full implementation")
print(f"Detected skills: {[s.skill for s in skills]}")
```

## Module Overview

### Core Modules

| Module | Description |
|--------|-------------|
| `context_router` | Intent classification and skill routing |
| `memory_manager` | Memory-first context management |
| `token_optimizer` | Token usage optimization |
| `skill_discovery` | Automatic skill detection and loading |

### Utility Modules

| Module | Description |
|--------|-------------|
| `utils/text_utils` | Text processing utilities |
| `utils/file_utils` | File operations |
| `utils/code_utils` | Code analysis utilities |
| `utils/http_utils` | HTTP request helpers |
| `utils/security_utils` | Security helpers |

### Integration Modules

| Module | Description |
|--------|-------------|
| `review/frontend_reviewer` | Frontend code review |
| `rules_parser` | Parse .mdc rule files |
| `skills_parser` | Parse skill files |

## Framework Integration

This library is designed to work with the Cursor Enterprise Framework rules and skills:

- **133 rule files** covering enterprise architecture patterns
- **Skills** for frontend, security, testing, and more
- **Pre-review and post-review gates** for quality assurance

## Cross-Agent Compatibility

The framework supports multiple vibe coding agents with unified skill and rule management.

### Supported Agents

| Agent | Identifier | Gate Prefix | Skills Path | Rules Path |
|-------|-----------|-------------|-------------|------------|
| Cursor IDE | `cursor` | `K` | `.cursor/skills` | `.cursor/rules` |
| Codex | `codex` | `CX` | `.cursor/skills` | `.cursor/rules` |
| Claude Code | `claude-code` | `C` | `.claude/skills` | `.claude/rules` |
| Grok | `grok` | `G` | `.grok/skills` | `.grok/rules` |
| Universal | `universal` | `U` | (all paths) | (all paths) |

### Installation per Agent

#### Cursor IDE / Codex
```bash
# Primary installation target
python -m cursor_framework install --agent cursor
```

#### Claude Code (@cursor/codex)
```bash
# Install to Claude Code skills directory
python -m cursor_framework install --agent claude-code
```

#### Grok (x.com/grok)
```bash
# Install to Grok skills directory
python -m cursor_framework install --agent grok
```

### Universal Gates (U.1-U.7)

All agents support universal gates that work identically:

**Pre-Code Gates:**
- `U.1` Think: State assumptions, ask if unclear
- `U.2` Simple: Check for over-engineering
- `U.3` Scope: Define surgical boundaries
- `U.4` Goals: Define verifiable success criteria

**Post-Code Gates:**
- `U.5` Verify: Check each line traces to request
- `U.6` Simple: Can 200 lines be 50?
- `U.7` Done: Goals met?

### Agent-Specific Gates

| Agent | Pre-Gates | Post-Gates |
|-------|-----------|------------|
| Cursor | K.1-K.4 | K.5-K.7 |
| Codex | CX.1-CX.4 | CX.5-CX.7 |
| Claude Code | C.1-C.4 | C.5-C.7 |
| Grok | G.1-G.4 | G.5-G.7 |

### Skill Compatibility

Universal skills work on all agents without modification:
- `karpathy-coding` - Universal coding discipline
- `frontend-taste` - Anti-slop frontend
- `frontend-review` - Quality gate
- `full-output` - Complete implementation
- `security-review` - OWASP security
- `test-analysis` - Testing strategy
- `perf-optimization` - Performance
- `stability` - Error handling
- `data-quality` - Database/schema

### Agent Detection

The framework auto-detects which agent is running:

```python
from cursor_framework.skills.skill_registry import create_cross_agent_registry

registry = create_cross_agent_registry()
agent = registry.detect_agent()
print(f"Detected: {agent.value}")  # cursor, codex, claude-code, grok, unknown
```

### Cross-Agent Sync

Sync skills across all agents:
```python
from cursor_framework.skills.skill_registry import create_cross_agent_registry

registry = create_cross_agent_registry()
manifest = registry.export_all_manifests(".cursor/skills/manifests/")
```

### Known Limitations

| Agent | Limitation | Workaround |
|-------|-----------|------------|
| Claude Code | Different skill path | Use `.claude/skills` |
| Grok | Limited MCP support | Use universal gates |
| Codex | Cloud-only context | Export context to file |

## License

MIT
