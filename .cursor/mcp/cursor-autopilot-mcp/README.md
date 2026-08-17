# Cursor Autopilot MCP

FastMCP companion for `cursor-framework-mcp`. It analyzes tasks, loads matching framework rules/skills/agents, validates quality gates, and prepares ordered workflows for the Cursor host agent.

## Safety and execution model

MCP servers cannot directly invoke Cursor subagents or IDE commands. `auto_execute` and `execute_workflow` therefore return fully resolved, host-executable plans, including resource instructions and status. They never run arbitrary shell commands.

## Installation

```bash
cd tools/cursor-autopilot-mcp
pip install -r requirements.txt
python -m cursor_autopilot_mcp.server
```

Set `CURSOR_WORKSPACE_ROOT` to the framework repository root. The server imports the shared registry, loader, analyzer, and token estimator from `tools/cursor-framework-mcp`.

## Cursor configuration

```json
{
  "mcpServers": {
    "cursor-autopilot": {
      "command": "python",
      "args": ["-m", "cursor_autopilot_mcp.server"],
      "cwd": "D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR\\tools\\cursor-autopilot-mcp",
      "env": {
        "CURSOR_WORKSPACE_ROOT": "D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
      }
    }
  }
}
```

## Tools

- `auto_execute`: analyze task and return loaded, ordered execution steps.
- `execute_workflow`: prepare `build`, `fix`, `review`, `test`, `security`, or `perf`.
- `run_gate_validation`: evaluate a skill's pre/post checklist against evidence.
- `get_workflow_status`: retrieve an execution state by id.
- `abort_workflow`: mark a workflow aborted.
- `list_workflows`: list predefined step sequences.
- `estimate_cost`: estimate context tokens and orchestration minutes.
- `suggest_optimization`: return task- and domain-specific optimizations.

The security workflow conditionally adds `vietnam-payment-review` when `payment=true`.
