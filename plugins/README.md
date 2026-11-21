# Vibe Framework Plugins

This directory contains plugin integrations for Cursor IDE, Claude Code, and Agent ecosystems to enhance productivity, code quality, and telemetry.

## Available Plugins

### 1. Quick Actions Plugin (`quick-actions/`)
- Fast Command Palette and keyboard shortcuts for framework CLI operations (`warm`, `stats`, `scan`, `index`, `clear-cache`, `dump-graph`, `dashboard`).

### 2. Status Line Plugin (`status-line/`)
- Real-time telemetry in the IDE status bar: cache warmth indicator, active skills count, active rules count, and memory token consumption. Includes interactive Quick Menu.

### 3. Automation & Quality Hooks Plugin (`automation/`)
- Automated background indexing on file save (debounced file watcher), one-click Git hooks installation (`pre-commit`, `post-commit`, `pre-push`), and TDD quality gate verification.

### 4. Context Monitor Plugin (`context-monitor/`)
- Session memory inspector, prompt preview, token budget analyzer, and Redis observability dashboard.

### 5. Spec Kit SDD Plugin (`spec-kit/`)
- Spec-Driven Development GUI helper: scaffold feature specs (`init`), list specifications, track status checklists, and validate against project Constitution rules.

### 6. Security & Pentest Suite (`hackingtool/`)
- 183+ pentesting and OSINT tools (nmap, nuclei, amass, subfinder, httpx, sherlock, sqlmap) wired into Cursor IDE and Claude Code marketplace.

---

## Directory Structure

```
plugins/
├── manifest.json              # Master plugin catalog & registry
├── README.md                  # Documentation
├── quick-actions/             # Quick action commands
│   ├── manifest.json
│   └── index.js
├── status-line/               # Real-time status bar integration
│   ├── manifest.json
│   ├── index.js
│   └── README.md
├── automation/                # Automated workflows & hooks
│   ├── manifest.json
│   ├── index.js
│   └── README.md
├── context-monitor/           # Context & token monitoring
│   ├── manifest.json
│   ├── index.js
│   └── README.md
├── spec-kit/                  # Spec-Driven Development (SDD)
│   ├── manifest.json
│   ├── index.js
│   └── README.md
└── hackingtool/               # Security & OSINT suite
    ├── manifest.json
    ├── index.js
    └── README.md
```

## Installation

### For Cursor IDE / VS Code:
Copy any desired plugin directory (or all) to your Cursor extensions/plugins directory:
- **Windows**: `%USERPROFILE%\.cursor\plugins\` or `%APPDATA%\.cursor\extensions\`
- **macOS**: `~/.cursor/plugins/`
- **Linux**: `~/.cursor/plugins/`

### Python CLI (dry-run first)

```bash
# Preview only — creates no directories and copies no files
python -m vibe_framework vibe install-plugins --dry-run

# Machine-readable report for CI (errors still exit with code 1)
python -m vibe_framework vibe install-plugins --json

# Explicit overwrite when a plugin directory already exists
python -m vibe_framework vibe install-plugins --force
```

`install-plugins` uses runtime detection when `--tool` is omitted. If no
runtime signal is present, it falls back to Cursor and Windsurf.

Compatibility: these plugins are VS Code-style extension bundles (`main`,
`activationEvents`, `contributes`). Only Cursor and Windsurf receive them.
Claude Code, Codex, Cline, Roo Code, Copilot, and Antigravity are skipped with
a reported reason because they do not load this extension format.
