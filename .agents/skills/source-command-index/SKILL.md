---
name: "source-command-index"
description: "Migrated source command `index`"
---

# source-command-index

Use this skill when the user asks to run the migrated source command `index`.

## Command Template

# /index Command
# Full scan and persist framework index

## Description
Performs a full scan of the .cursor/ directory and persists
both INDEX.json and INDEX.md files.

## Usage
```
/index
/index --rebuild
```

## Options
- `--rebuild`: Force complete rebuild

## Examples
```
/index
/index --rebuild
```

## What it does
1. Scans .cursor/ directory
2. Builds comprehensive index
3. Writes INDEX.json
4. Writes INDEX.md (markdown version)

## Output Files
- `.cursor/INDEX.json` - Machine-readable index
- `.cursor/INDEX.md` - Human-readable markdown

## Related Commands
- `/scan` - Quick scan without persist
- `/warm` - Warm cache without full index
- `/stats` - View current stats
