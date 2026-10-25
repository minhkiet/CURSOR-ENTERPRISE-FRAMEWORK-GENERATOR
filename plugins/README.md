# Cursor Framework Plugins

This directory contains plugin integrations for Cursor IDE to enhance productivity.

## Available Plugins

### Quick Actions Plugin
- `quick-actions/` - Quick access to common framework operations

### Status Line Plugin
- `status-line/` - Display framework stats in status bar

### Automation Plugin
- `automation/` - Automated workflows and pre-commit hooks

## Structure

```
plugins/
├── manifest.json          # Plugin manifest
├── quick-actions/         # Quick action commands
│   ├── manifest.json
│   └── commands/
├── status-line/           # Status bar integration
│   └── manifest.json
└── automation/            # Automated workflows
    └── manifest.json
```

## Installation

Copy the plugin folder to your Cursor plugins directory:
- Windows: `%USERPROFILE%\.cursor\plugins\`
- macOS: `~/.cursor/plugins/`
- Linux: `~/.cursor/plugins/`

Or use the built-in plugin manager in Cursor IDE.
