---
name: "source-command-warm"
description: "Migrated source command `warm`"
---

# source-command-warm

Use this skill when the user asks to run the migrated source command `warm`.

## Command Template

# /warm Command
# Warm up framework cache and prepare for next request

## Description
Warms the framework cache by scanning .cursor/ and building indexes.
Run this after adding new skills or rules to ensure they're available.

## Usage
```
/warm
/warm --force
```

## Options
- `--force`: Force full re-scan even if cache is fresh

## Examples
```
/warm
/warm --force
```

## What it does
1. Scans .cursor/ directory for skills, rules, agents
2. Builds skill dependency index
3. Persists memory cache
4. Returns statistics

## Related Commands
- `/stats` - View framework statistics
- `/scan` - Scan without warming
- `/clear` - Clear cache
