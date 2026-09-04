---
name: "source-command-clear"
description: "Migrated source command `clear`"
---

# source-command-clear

Use this skill when the user asks to run the migrated source command `clear`.

## Command Template

# /clear Command
# Clear framework cache

## Description
Clears the framework cache including memory and index files.
Use with caution - will slow down next request as cache rebuilds.

## Usage
```
/clear
/clear --force
/clear --dry-run
```

## Options
- `--force`: Actually delete files (default is dry-run)
- `--dry-run`: Show what would be deleted without deleting

## Examples
```
/clear --dry-run
/clear --force
```

## What it does
1. Shows/delets memory cache file
2. Shows/deletes INDEX.json
3. Shows/deletes INDEX.md

## Safety
- Default is dry-run (shows what would happen)
- Must use `--force` to actually delete

## Related Commands
- `/warm` - Rebuild cache after clearing
- `/stats` - View cache statistics
