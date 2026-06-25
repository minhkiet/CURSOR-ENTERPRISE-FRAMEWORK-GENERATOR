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

## License

MIT
