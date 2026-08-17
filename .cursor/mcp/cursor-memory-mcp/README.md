# Cursor Memory MCP

FastMCP companion for `cursor-framework-mcp` that manages hierarchical memory and token-aware context.

## Features

- Short-term session memory, medium-term project memory, and persistent long-term memory.
- Relevance ranking using lexical overlap, recency, memory tier, and access frequency.
- Deterministic extractive context compression.
- Automatic token-budget pruning.
- Long-term compression before atomic disk persistence.
- Framework cache token accounting through the shared loader.

## Installation

```bash
cd tools/cursor-memory-mcp
pip install -r requirements.txt
python -m cursor_memory_mcp.server
```

Set `CURSOR_WORKSPACE_ROOT` to the framework repository root. Persistent data is stored at `.cache/cursor-memory-mcp.json`.

## Cursor configuration

```json
{
  "mcpServers": {
    "cursor-memory": {
      "command": "python",
      "args": ["-m", "cursor_memory_mcp.server"],
      "cwd": "D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR\\tools\\cursor-memory-mcp",
      "env": {
        "CURSOR_WORKSPACE_ROOT": "D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
      }
    }
  }
}
```

## Tools

- `store_memory`: store facts or conclusions with tier, project, session, kind, and tags.
- `recall_memory`: rank relevant memories for a task.
- `compact_context`: compress text to a target token budget.
- `summarize_history`: summarize old JSON conversation messages and preserve recent ones.
- `get_context_stats`: report current, framework cache, history, and memory token usage.
- `prune_context`: remove low-relevance memories to meet a budget.
- `export_memory`: return JSON or write a workspace-contained export.
- `import_memory`: restore or merge a JSON export.
- `sync_to_disk`: compact long-term memory and persist atomically.

The autopilot MCP can use recalled memories as task context, while this server accounts for resource context loaded by the shared framework MCP.
