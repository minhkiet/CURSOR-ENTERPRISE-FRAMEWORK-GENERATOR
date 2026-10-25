---
name: "source-command-dashboard"
description: "Migrated source command `dashboard`"
---

# source-command-dashboard

Use this skill when the user asks to run the migrated source command `dashboard`.

## Command Template

# /dashboard Command
# Open framework dashboard

## Description
Opens the framework dashboard in the default browser.
Shows:
- Framework statistics
- Recent activity
- Memory usage
- Quick actions

## Usage
```
/dashboard
/dashboard --port 8765
```

## Options
- `--port`: Port for dashboard server (default: 8765)

## Examples
```
/dashboard
/dashboard --port 9000
```

## What it shows
- Asset counts (skills, rules, agents)
- Memory cache stats
- Quick action buttons
- Framework health status

## Related Commands
- `/stats` - View stats in terminal
- `/warm` - Warm cache before using dashboard
