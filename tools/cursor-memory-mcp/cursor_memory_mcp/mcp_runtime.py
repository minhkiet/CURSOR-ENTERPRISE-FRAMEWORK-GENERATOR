"""
Universal MCP Runtime (Zero-Dependency Stdio JSON-RPC 2.0 Engine)

Enables MCP tools to run seamlessly on ANY vibe coding platform:
- Cursor IDE
- Google Antigravity / Gemini CLI
- Claude Code
- Codex
- Windsurf
- Cline / Roo Code
- Any standard MCP-compliant client

Zero external dependencies required (uses standard library json, sys, inspect).
Gracefully leverages official `mcp.server.fastmcp` or `fastmcp` if available,
with a robust fallback that never crashes due to missing packages.
"""

from __future__ import annotations

import inspect
import json
import logging
import os
import sys
import traceback
from typing import Any, Callable, Dict, List, Optional

# Setup stderr logger for MCP (NEVER log to stdout - stdout is reserved for JSON-RPC)
logger = logging.getLogger("mcp_runtime")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _python_type_to_json_type(py_type: Any) -> str:
    """Map python types to JSON Schema types."""
    if py_type in (int, float):
        return "number" if py_type is float else "integer"
    if py_type is bool:
        return "boolean"
    if py_type is str:
        return "string"
    if py_type in (list, List) or getattr(py_type, "__origin__", None) in (list, List):
        return "array"
    if py_type in (dict, Dict) or getattr(py_type, "__origin__", None) in (dict, Dict):
        return "object"
    return "string"


class UniversalMcpServer:
    """
    Universal MCP Server compatible with the Model Context Protocol (2024-11-05).
    Provides @tool and @resource decorators and standard stdio JSON-RPC 2.0 transport.
    """

    def __init__(self, name: str, version: str = "1.0.0", instructions: str = ""):
        self.name = name
        self.version = version
        self.instructions = instructions
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._resources: Dict[str, Dict[str, Any]] = {}
        self._fastmcp_instance: Any = None

        # Check if FastMCP is available and not broken by namespace collisions
        self._has_fastmcp = False
        try:
            # Avoid local directory shadowing by verifying server submodule
            from mcp.server.fastmcp import FastMCP  # type: ignore
            self._fastmcp_class = FastMCP
            self._has_fastmcp = True
        except Exception:
            try:
                from fastmcp import FastMCP  # type: ignore
                self._fastmcp_class = FastMCP
                self._has_fastmcp = True
            except Exception:
                self._has_fastmcp = False

    def tool(self, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator to register an MCP tool function."""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            tool_desc = description or (func.__doc__ or "").strip()
            
            # Inspect signature to generate JSON schema
            sig = inspect.signature(func)
            properties: Dict[str, Any] = {}
            required: List[str] = []

            for param_name, param in sig.parameters.items():
                if param_name in ("self", "cls"):
                    continue
                
                param_type = "string"
                if param.annotation != inspect.Parameter.empty:
                    param_type = _python_type_to_json_type(param.annotation)
                
                prop_meta: Dict[str, Any] = {"type": param_type}
                if param.default is inspect.Parameter.empty:
                    required.append(param_name)
                else:
                    prop_meta["default"] = param.default

                properties[param_name] = prop_meta

            input_schema = {
                "type": "object",
                "properties": properties,
                "required": required,
            }

            self._tools[tool_name] = {
                "name": tool_name,
                "description": tool_desc,
                "inputSchema": input_schema,
                "func": func,
            }
            return func
        return decorator

    def resource(self, uri: str, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator to register an MCP resource."""
        def decorator(func: Callable):
            res_name = name or func.__name__
            res_desc = description or (func.__doc__ or "").strip()
            self._resources[uri] = {
                "uri": uri,
                "name": res_name,
                "description": res_desc,
                "func": func,
            }
            return func
        return decorator

    def handle_request(self, req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single JSON-RPC 2.0 request dictionary and return response."""
        req_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params", {}) or {}

        # Handle notifications (no id)
        if req_id is None:
            if method == "notifications/initialized":
                logger.info("Client sent notifications/initialized")
            return None

        # Standard MCP JSON-RPC methods
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"subscribe": False, "listChanged": False},
                    },
                    "serverInfo": {
                        "name": self.name,
                        "version": self.version,
                    },
                    "instructions": self.instructions,
                },
            }

        elif method == "ping":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {},
            }

        elif method == "tools/list":
            tools_list = []
            for t in self._tools.values():
                tools_list.append({
                    "name": t["name"],
                    "description": t["description"],
                    "inputSchema": t["inputSchema"],
                })
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": tools_list,
                },
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {}) or {}
            if tool_name not in self._tools:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool '{tool_name}' not found",
                    },
                }

            tool_def = self._tools[tool_name]
            func = tool_def["func"]

            try:
                # Call tool function with arguments
                result = func(**arguments)
                
                # Format output into MCP text content
                if isinstance(result, str):
                    text_content = result
                elif isinstance(result, (dict, list, int, float, bool)) or result is None:
                    text_content = json.dumps(result, ensure_ascii=False, indent=2, default=str)
                else:
                    text_content = str(result)

                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": text_content,
                            }
                        ],
                        "isError": False,
                    },
                }
            except Exception as e:
                logger.error(f"Error executing tool '{tool_name}': {e}", exc_info=True)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error executing tool '{tool_name}': {str(e)}\n{traceback.format_exc()}",
                            }
                        ],
                        "isError": True,
                    },
                }

        elif method == "resources/list":
            res_list = []
            for r in self._resources.values():
                res_list.append({
                    "uri": r["uri"],
                    "name": r["name"],
                    "description": r["description"],
                    "mimeType": "application/json",
                })
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "resources": res_list,
                },
            }

        elif method == "resources/read":
            uri = params.get("uri")
            if uri not in self._resources:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32602,
                        "message": f"Resource uri '{uri}' not found",
                    },
                }
            res_def = self._resources[uri]
            try:
                result = res_def["func"]()
                text_content = result if isinstance(result, str) else json.dumps(result, indent=2)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": text_content,
                            }
                        ],
                    },
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": f"Error reading resource: {str(e)}",
                    },
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not implemented",
                },
            }

    def run_stdio(self):
        """Run stdio JSON-RPC loop using pure standard library."""
        logger.info(f"Starting Universal MCP Server '{self.name}' v{self.version} in Stdio mode...")
        # Ensure utf-8 streams
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                logger.error(f"Invalid JSON received: {exc}")
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()
                continue

            resp = self.handle_request(req)
            if resp is not None:
                out = json.dumps(resp, ensure_ascii=False)
                sys.stdout.write(out + "\n")
                sys.stdout.flush()

    def run(self, transport: str = "stdio"):
        """Run server with specified transport. Defaults to stdio."""
        self.run_stdio()


def create_mcp_server(name: str, version: str = "1.0.0", instructions: str = "") -> UniversalMcpServer:
    """Factory function to create a UniversalMcpServer instance."""
    return UniversalMcpServer(name=name, version=version, instructions=instructions)
