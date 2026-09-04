---
name: "source-command-skills"
description: "Migrated source command `skills`"
---

# source-command-skills

Use this skill when the user asks to run the migrated source command `skills`.

## Command Template

# /skills Command
# Discover and display relevant skills

## Description
Finds and displays skills that match the current context or query.
Use to see what skills are available or recommended.

## Usage
```
/skills
/skills [query]
```

## Arguments
- `query` (optional): Filter skills by keyword

## Examples
```
/skills
/skills frontend
/skills "security audit"
```

## What it shows
- Matching skills with scores
- Skill paths and descriptions
- Related skills (combo)

## Related Commands
- `/find` - Find specific skill
- `/graph` - View skill dependencies
