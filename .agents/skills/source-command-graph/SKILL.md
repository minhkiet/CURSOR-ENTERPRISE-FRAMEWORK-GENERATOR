---
name: "source-command-graph"
description: "Migrated source command `graph`"
---

# source-command-graph

Use this skill when the user asks to run the migrated source command `graph`.

## Command Template

# /graph Command
# Visualize skill dependency graph

## Description
Opens the skill dependency graph visualization in browser.
Shows relationships between skills, agents, and their dependencies.

## Usage
```
/graph
/graph --port 8766
```

## Options
- `--port`: Port for the graph server (default: 8766)

## Examples
```
/graph
/graph --port 9000
```

## What it shows
- **Nodes**: Skills (blue) and Agents (orange)
- **Edges**: Dependencies between components
- **Interaction**: Drag nodes, zoom, pan

## Legend
- 🔵 Blue circles: Skills
- 🟠 Orange circles: Agents
- ─ Blue lines: Explicit dependencies
- ── Orange dashed: Co-occurrence patterns

## Related Commands
- `/stats` - View framework statistics
- `/warm` - Warm the cache
- `/scan` - Scan framework files
