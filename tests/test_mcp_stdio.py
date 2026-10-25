"""
Tests for Universal Stdio MCP Servers across Multi-Platform Environments.

Verifies:
1. JSON-RPC 2.0 initialize negotiation
2. tools/list discovery
3. tools/call execution
4. Proper stdio clean output without corrupted stderr noise
For all 5 MCP servers in the framework:
- cursor_framework_mcp
- cursor_autopilot_mcp
- cursor_memory_mcp
- framework_server (mcp/framework_server.py)
- file_server (mcp/file_server.py)
"""

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_mcp_session(server_script: Path, tool_to_call: str, tool_args: dict, env_extra: dict = None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["WORKSPACE_ROOT"] = str(REPO_ROOT)
    env["CURSOR_WORKSPACE_ROOT"] = str(REPO_ROOT)
    if env_extra:
        env.update(env_extra)

    proc = subprocess.Popen(
        [sys.executable, str(server_script)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=env,
        cwd=str(REPO_ROOT)
    )

    try:
        # Step 1: initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-stdio-client", "version": "1.0.0"}
            }
        }
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()

        resp_line = proc.stdout.readline()
        assert resp_line, f"Server {server_script.name} died without output. Stderr: {proc.stderr.read()}"
        init_resp = json.loads(resp_line)
        assert init_resp.get("id") == 1, f"Expected id 1, got {init_resp}"
        assert "result" in init_resp, f"No result in init_resp: {init_resp}"
        server_info = init_resp["result"].get("serverInfo", {})
        server_name = server_info.get("name", "unknown")

        # Step 2: initialized notification
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        proc.stdin.flush()

        # Step 3: tools/list
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        proc.stdin.write(json.dumps(list_req) + "\n")
        proc.stdin.flush()

        list_line = proc.stdout.readline()
        assert list_line, "No response for tools/list"
        list_resp = json.loads(list_line)
        assert list_resp.get("id") == 2
        tools = list_resp.get("result", {}).get("tools", [])
        tool_names = [t["name"] for t in tools]
        assert len(tools) > 0, f"No tools returned by {server_name}"
        assert tool_to_call in tool_names, f"Expected tool '{tool_to_call}' not found in {tool_names}"

        # Step 4: tools/call
        call_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_to_call,
                "arguments": tool_args
            }
        }
        proc.stdin.write(json.dumps(call_req) + "\n")
        proc.stdin.flush()

        call_line = proc.stdout.readline()
        assert call_line, "No response for tools/call"
        call_resp = json.loads(call_line)
        assert call_resp.get("id") == 3
        assert "result" in call_resp, f"tools/call failed: {call_resp}"

        content = call_resp["result"].get("content", [])
        assert len(content) > 0, f"Expected content in tools/call result: {call_resp}"
        text = content[0].get("text", "")

        return {
            "server": server_name,
            "tool_count": len(tools),
            "tool_called": tool_to_call,
            "call_result_snippet": text[:150]
        }
    finally:
        try:
            if proc.stdin and not proc.stdin.closed:
                proc.stdin.close()
            if proc.stdout and not proc.stdout.closed:
                proc.stdout.close()
            if proc.stderr and not proc.stderr.closed:
                proc.stderr.close()
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            pass


import unittest


class McpStdioTestCase(unittest.TestCase):
    def test_cursor_framework_mcp(self):
        path = REPO_ROOT / "tools" / "cursor-framework-mcp" / "cursor_framework_mcp" / "server.py"
        res = run_mcp_session(path, "get_framework_status", {})
        self.assertGreaterEqual(res["tool_count"], 5)
        self.assertTrue(
            "framework" in res["call_result_snippet"].lower()
            or "version" in res["call_result_snippet"].lower()
            or "rules" in res["call_result_snippet"].lower()
        )

    def test_cursor_autopilot_mcp(self):
        path = REPO_ROOT / "tools" / "cursor-autopilot-mcp" / "cursor_autopilot_mcp" / "server.py"
        res = run_mcp_session(path, "list_workflows", {})
        self.assertGreaterEqual(res["tool_count"], 4)
        self.assertTrue("workflow" in res["call_result_snippet"].lower() or "[" in res["call_result_snippet"])

    def test_cursor_memory_mcp(self):
        path = REPO_ROOT / "tools" / "cursor-memory-mcp" / "cursor_memory_mcp" / "server.py"
        res = run_mcp_session(path, "get_context_stats", {})
        self.assertGreaterEqual(res["tool_count"], 5)
        self.assertTrue("context" in res["call_result_snippet"].lower() or "{" in res["call_result_snippet"])

    def test_mcp_framework_server(self):
        path = REPO_ROOT / "mcp" / "framework_server.py"
        res = run_mcp_session(path, "get_stats", {})
        self.assertGreaterEqual(res["tool_count"], 3)
        self.assertTrue("status" in res["call_result_snippet"].lower() or "{" in res["call_result_snippet"])

    def test_mcp_file_server(self):
        path = REPO_ROOT / "mcp" / "file_server.py"
        res = run_mcp_session(path, "list_dir", {"path": "."})
        self.assertGreaterEqual(res["tool_count"], 2)
        self.assertTrue("files" in res["call_result_snippet"].lower() or "[" in res["call_result_snippet"])


if __name__ == "__main__":
    servers = [
        (REPO_ROOT / "tools" / "cursor-framework-mcp" / "cursor_framework_mcp" / "server.py", "get_framework_status", {}),
        (REPO_ROOT / "tools" / "cursor-autopilot-mcp" / "cursor_autopilot_mcp" / "server.py", "list_workflows", {}),
        (REPO_ROOT / "tools" / "cursor-memory-mcp" / "cursor_memory_mcp" / "server.py", "get_context_stats", {}),
        (REPO_ROOT / "mcp" / "framework_server.py", "get_stats", {}),
        (REPO_ROOT / "mcp" / "file_server.py", "list_dir", {"path": "."}),
    ]

    print("=" * 60)
    print("RUNNING MULTI-PLATFORM STDIO MCP SERVER TESTS")
    print("=" * 60)

    all_passed = True
    for script, tool, args in servers:
        try:
            r = run_mcp_session(script, tool, args)
            print(f"[PASS] {script.name} ({r['server']}): {r['tool_count']} tools available | Called '{r['tool_called']}' -> OK")
        except Exception as e:
            print(f"[FAIL] {script.name}: {e}")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("ALL 5 MCP SERVERS PASSED STDIO JSON-RPC 2.0 PROTOCOL VERIFICATION!")
    else:
        print("SOME MCP TESTS FAILED")
        sys.exit(1)
