# Cursor Enterprise Framework MCP Server

> Version: 1.0.0 · Updated: 2026-08-09
> Companion to [Cursor Enterprise Framework](https://github.com/thaofvn-coca06/2026)

A FastMCP server that exposes the **Cursor Enterprise Framework** as MCP tools. It loads `.cursor/rules/*.mdc`, `.cursor/skills/*/SKILL.md`, `.cursor/agents/*.md`, and `.cursor/AGENTS.md` on-demand with an LRU cache, auto-detects the right skill/rule/agent for a task, and tracks token + memory budgets.

## Why

Cursor injects every rule and skill into every chat. For a framework with 43 rules and 92+ skills, that's wasteful. This MCP server:

- **Lazy-loads** rules/skills/agents only when needed
- **Caches** them with strict LRU + TTL limits
- **Detects** the relevant skill from a free-form task description
- **Pre-loads** essential skills (karpathy-coding, ponytail, full-output) at session start
- **Tracks** token & memory usage per item
- **Optimizes** the cache on demand (unload stale, compact)
- **Follows alias redirects** (e.g. `karpathy-coding` → `code_karpathy`) transparently

## Layout

```
tools/cursor-framework-mcp/
├── cursor_framework_mcp/
│   ├── __init__.py
│   ├── cache.py            # thread-safe LRU cache w/ TTL + per-kind stats
│   ├── registry.py         # one-shot index of rules/skills/agents
│   ├── loader.py           # lazy file reader (follows alias redirects)
│   ├── analyzer.py         # task → ranked skill/rule/agent suggestions
│   ├── optimizer.py        # evict expired/idle, compact, report savings
│   └── server.py           # FastMCP tool definitions
├── plugin.json             # Plugin manifest
├── requirements.txt        # mcp[cli], fastmcp, pydantic, watchfiles
└── README.md               # this file
```

## Installation

```bash
cd tools/cursor-framework-mcp
pip install -r requirements.txt
```

## Run standalone

```bash
python -m cursor_framework_mcp.server
```

## Wire into Cursor

Add to your MCP settings (`~/.cursor/mcp.json` or workspace `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "cursor-framework": {
      "command": "python",
      "args": ["-m", "cursor_framework_mcp.server"],
      "cwd": "D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR\\tools\\cursor-framework-mcp",
      "env": {
        "CURSOR_WORKSPACE_ROOT": "D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
      }
    }
  }
}
```

The server auto-detects the workspace by walking up from `cwd` looking for `.cursor/rules`. Set `CURSOR_WORKSPACE_ROOT` to override.

## Tools exposed

| Tool | Purpose |
|------|---------|
| `get_rule` | Load a `.mdc` rule by id or path |
| `get_skill` | Load a `SKILL.md` by id; with `include_dependencies=True`, also pre-load essential overlays + bundle-mates |
| `get_agent` | Load an agent persona block from `.cursor/AGENTS.md` or `agent_*.md` |
| `analyze_task` | Free-form request → ranked suggestions + a `primary` pick above 0.75 confidence |
| `load_skill_bundle` | Pre-load Bundle A–E or a custom comma-separated list |
| `get_essential_skills` | Pre-load karpathy / ponytail / full-output |
| `clear_cache` | Drop cached items by kind/id (or everything) |
| `get_framework_status` | Memory, token usage, hit rate, cached item snapshot |
| `optimize_framework` | Evict expired/idle items, compact cache, report savings |

### Example tool calls

```text
analyze_task(request="Build a Next.js landing page with hero, pricing, and testimonials")
→ primary: canvas-design (1.00), top suggestions dashboard-ui, frontend-redesign,
  frontend-review, frontend-taste, plus the essential overlay trio.

get_skill(skill_id="karpathy-coding", include_dependencies=True)
→ 488 tokens for karpathy; pulls in ponytail + full-output + bundle mates; total
  tokens reported.

load_skill_bundle(bundle="B")
→ Pre-loads the Full-Stack bundle: frontend-taste, dashboard-ui, full-output,
  karpathy-coding, ponytail, vibe-coding, stability.

get_framework_status()
→ 12 items in skill cache, 16 762 tokens, 47 % hit rate, rule/agent caches empty.

optimize_framework(idle_threshold_seconds=1800, compact_to_ratio=0.6)
→ Evicts expired entries, drops idle items, compacts to 60 % fill.

clear_cache(kind="skill")
→ Removes all 12 cached skills (or pass `key="karpathy-coding"` to drop one).
```

## Memory budget (defaults)

| Kind   | Max items | TTL     | Token estimate per item |
|--------|-----------|---------|-------------------------|
| rules  | 20        | 30 min  | ~600                    |
| skills | 30        | 30 min  | ~1 200                  |
| agents | 10        | 30 min  | ~400                    |

Tune via `CursorFrameworkConfig`:

```python
from cursor_framework_mcp.server import create_server
server = create_server(
    workspace_root="...",
    cache_cfg={"max_rules": 30, "max_skills": 50, "max_agents": 20, "ttl_seconds": 3600},
)
```

## Auto-detection (analyze_task)

`analyze_task` matches against a curated keyword matrix derived from
`.cursor/rules/rule_skill-registry.mdc` plus the built-in `DOMAIN_TRIGGERS`
table. Confidence scoring:

- 1 trigger hit → 0.33 confidence, 2 → 0.66, 3+ → 1.0 (capped)
- + domain bonus for explicit alignment (e.g. security request → security domain)
- essential overlay skills (karpathy/ponytail/full-output) get a 0.85 floor on coding tasks
- suggestions below 0.5 are dropped
- a single `primary` is returned when its confidence ≥ 0.75

## Alias handling

Several skill folders (e.g. `karpathy-coding/`, `ponytail/`, `full-output/`) are
thin redirect files pointing at their canonical home (`code_karpathy/`, etc.).
The loader detects the alias, follows it once, and serves the canonical
content. Both ids (`karpathy-coding` and `karpathy`) are registered so callers
can use either.

## License

MIT
