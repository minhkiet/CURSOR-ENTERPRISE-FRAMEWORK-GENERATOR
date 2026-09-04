---
name: "source-command-scan"
description: "Migrated source command `scan`"
---

# source-command-scan

Use this skill when the user asks to run the migrated source command `scan`.

## Command Template

# /scan Command
# Scan .cursor directory without warming cache

## Description
Scans the .cursor/ directory and returns asset counts.
Does not persist cache or warm anything.

## Usage
```
/scan
```

## Examples
```
/scan
```

## What it does
1. Scans .cursor/ directory
2. Counts skills, rules, agents, knowledge bases
3. Returns totals in JSON format

## Output Format
```json
{
  "totals": {
    "skills": 50,
    "rules": 20,
    "agents": 10,
    "knowledge": 100,
    "grand_total": 180
  }
}
```

## Related Commands
- `/warm` - Warm cache after scan
- `/stats` - View persisted statistics
- `/index` - Full scan + persist
