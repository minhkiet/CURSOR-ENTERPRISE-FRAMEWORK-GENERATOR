# Cursor Framework Automation & Hooks Plugin

Automates background indexing, file watching, Git quality hooks, and TDD execution for Cursor Enterprise Framework.

## Features
- **Background Auto-Warming**: Automatically runs debounced index rebuilds when skills, rules, or framework files change.
- **Git Hooks Installer**: One-click installation of `pre-commit`, `post-commit`, and `pre-push` quality hooks directly into `.git/hooks`.
- **Quality Gates Verification**: Runs comprehensive pre-flight verification across tests, rule consistency, and secret prevention.
- **TDD Test Runner**: Instant execution of the unit test suite with live output channel logging.
- **Multi-Agent Sync**: Keeps `.cursor`, `.agents`, `.gemini`, and `.codex` in continuous harmony.

## Settings
- `cursorFramework.automation.autoWarmOnSave`: Enable automatic cache warm on file changes (default: `true`).
- `cursorFramework.automation.debounceMs`: Debounce delay in ms before triggering auto-warm (default: `1500`).
- `cursorFramework.automation.enforceTdd`: Enforce passing unit tests before commit (default: `true`).
