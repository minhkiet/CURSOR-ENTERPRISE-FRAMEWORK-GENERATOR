# Cursor Framework MCP, Plugins, Hooks & Commands

> Utilities for faster, more stable development with Cursor Framework

## Overview

This directory contains integrations to enhance Cursor IDE and streamline framework operations:

- **MCP Servers**: Model Context Protocol servers for AI tool access
- **Plugins**: Cursor IDE extensions for quick actions
- **Hooks**: Git hooks for automated validation
- **Commands**: Slash commands for common workflows

## Quick Start

```powershell
# Install hooks
.\hooks\install-hooks.ps1

# Warm cache
.\scripts\framework-utils.ps1 warm

# View stats
.\scripts\framework-utils.ps1 stats
```

## Directory Structure

```
├── mcp/                    # MCP Server implementations
│   ├── framework_server.py  # Framework utilities MCP
│   ├── file_server.py      # File operations MCP
│   └── mcp_config.json     # Cursor MCP configuration
├── plugins/                 # Cursor IDE plugins
│   ├── quick-actions/       # Quick action commands
│   └── manifest.json
├── hooks/                   # Git hooks
│   ├── pre-commit          # Bash pre-commit
│   ├── post-commit         # Bash post-commit
│   ├── pre-push           # Bash pre-push validation
│   ├── pre-commit.ps1      # PowerShell pre-commit
│   └── install-hooks.ps1   # Hook installer
├── commands/                # Slash commands
│   ├── warm.md
│   ├── stats.md
│   ├── scan.md
│   ├── index.md
│   ├── clear.md
│   ├── graph.md
│   ├── skills.md
│   └── dashboard.md
└── scripts/                # Utility scripts
    └── framework-utils.ps1  # PowerShell utilities
```

## MCP Servers

### Installation

1. Copy `mcp/mcp_config.json` to your Cursor settings
2. Restart Cursor IDE

### Available MCP Servers

#### `cursor-framework`
Framework utilities - context management, skill discovery, memory operations

**Tools:**
- `ask_framework` - Process request through workflow
- `warm_cache` - Warm framework cache
- `get_stats` - Get framework statistics
- `scan_framework` - Scan .cursor directory
- `discover_skills` - Find relevant skills
- `get_skill_graph` - Get dependency graph
- `scan_code_graph` - Scan project code
- `mark_file_read` - Track session files
- `build_context` - Generate context prompt
- `dump_context` - Dump session context

#### `file-ops`
File operations - search, copy, move, delete, tree view

**Tools:**
- `ensure_directory` - Create directory
- `find_files` - Glob search
- `copy_file` / `batch_copy` - File copy
- `move_file` - File move
- `delete_file` / `batch_delete` - File delete
- `read_file` / `write_file` - Read/write
- `list_dir` - Directory listing
- `search_in_files` - Text search
- `find_duplicates` - Duplicate finder
- `count_lines` - LOC counter
- `tree` - Directory tree

## Plugins

### Quick Actions Plugin

Provides quick access commands in Cursor IDE:

- `Ctrl+Shift+F1` - Show stats
- `Ctrl+Shift+F2` - Warm cache
- Command Palette - All framework commands

**Installation:**
Copy `plugins/quick-actions/` to Cursor plugins directory

## Git Hooks

### Available Hooks

| Hook | Purpose |
|------|---------|
| `pre-commit` | Warm cache, validate skills |
| `post-commit` | Update memory, log commit |
| `pre-push` | Validate code, check for secrets |

### Installation

**PowerShell (Windows):**
```powershell
.\hooks\install-hooks.ps1
```

**Bash (Linux/macOS):**
```bash
chmod +x hooks/pre-commit hooks/post-commit hooks/pre-push
cp hooks/pre-commit .git/hooks/
cp hooks/post-commit .git/hooks/
cp hooks/pre-push .git/hooks/
```

## Slash Commands

Access via `/` in Cursor chat:

| Command | Description |
|---------|-------------|
| `/warm` | Warm framework cache |
| `/stats` | Show statistics |
| `/scan` | Scan .cursor directory |
| `/index` | Rebuild index |
| `/clear` | Clear cache |
| `/graph` | Open skill graph |
| `/skills` | Discover skills |
| `/dashboard` | Open dashboard |

## PowerShell Utilities

```powershell
# Warm cache
.\scripts\framework-utils.ps1 warm

# View stats
.\scripts\framework-utils.ps1 stats

# Scan skills
.\scripts\framework-utils.ps1 scan

# Clear cache
.\scripts\framework-utils.ps1 clear -WhatIf
.\scripts\framework-utils.ps1 clear -Force

# Open dashboard
.\scripts\framework-utils.ps1 dashboard

# View graph
.\scripts\framework-utils.ps1 graph

# JSON output
.\scripts\framework-utils.ps1 stats -Json
```

## Requirements

- Python 3.8+
- cursor_framework package (`pip install -e cursor_framework`)
- For MCP: `pip install fastmcp`

## License

MIT - See main project license
