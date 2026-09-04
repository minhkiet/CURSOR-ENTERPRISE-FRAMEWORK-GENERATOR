---
name: "source-command-stats"
description: "Migrated source command `stats`"
---

# source-command-stats

Use this skill when the user asks to run the migrated source command `stats`.

## Command Template

# /stats Command
# Display framework statistics and health status

## Description
Shows comprehensive statistics about the framework including:
- Assets indexed (skills, rules, agents)
- Memory cache hits/misses
- Token usage
- Code graph metrics

## Usage
```
/stats
/stats --detailed
```

## Options
- `--detailed`: Show detailed breakdown

## Examples
```
/stats
/stats --detailed
```

## What it shows
- **Assets Indexed**: Total number of skills, rules, agents
- **Memory Hits**: Successful cache retrievals
- **Memory Misses**: Cache misses (cold reads)
- **Tokens Saved**: Estimated tokens saved by caching
- **Watcher**: Background file watcher status

## Related Commands
- `/warm` - Warm the cache
- `/scan` - Scan framework files
- `/graph` - View skill dependency graph
