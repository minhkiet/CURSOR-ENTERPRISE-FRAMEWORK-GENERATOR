#!/usr/bin/env python
"""
MCP Configuration Generator

Generates MCP configuration file for Cursor IDE.
Supports multiple workspace configurations and MCP server types.

Usage:
    python mcp_config_generator.py --output mcp.json
    python mcp_config_generator.py --workspace /path/to/project --output mcp.json
    python mcp_config_generator.py --add vercel --add browser --output mcp.json
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class McpServer:
    """MCP Server configuration."""
    command: str
    args: list[str]
    cwd: Optional[str] = None
    env: dict[str, str] = field(default_factory=dict)
    url: Optional[str] = None
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        result = {
            "command": self.command,
            "args": self.args,
        }
        if self.cwd:
            result["cwd"] = self.cwd
        if self.env:
            result["env"] = self.env
        if self.url:
            result["url"] = self.url
        if self.description:
            result["description"] = self.description
        return result


@dataclass 
class McpConfig:
    """MCP Configuration container."""
    mcpServers: dict[str, Any] = field(default_factory=dict)
    version: str = "1.0"
    syncedAt: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "mcpServers": self.mcpServers,
            "version": self.version,
            "syncedAt": self.syncedAt,
        }


class McpConfigGenerator:
    """Generator for MCP configuration files across multi-platform vibe tools."""
    
    def __init__(self, workspace_root: str, python_cmd: Optional[str] = None, target: str = "cursor"):
        self.workspace_root = Path(workspace_root).resolve()
        self.target = target
        self.python_cmd = self._resolve_python_cmd(python_cmd, target)
        self.config = McpConfig()
        self._add_cursor_framework()

    def _resolve_python_cmd(self, python_cmd: Optional[str], target: str) -> str:
        """Resolve python command, handling Windows execution alias avoidance for Cursor."""
        if python_cmd:
            return python_cmd
        if target == "cursor":
            # Prefer explicit Windows Python path if available to avoid Microsoft Store stub execution alias
            windows_candidates = [
                Path("/mnt/c/Python312/python.exe"),
                Path("C:/Python312/python.exe"),
                Path("C:\\Python312\\python.exe"),
            ]
            for c in windows_candidates:
                try:
                    if c.exists():
                        return "C:\\Python312\\python.exe"
                except OSError:
                    pass
            # Default to standard Python 3.12 location if target is Cursor on Windows
            if os.name == "nt" or Path("/mnt/c").exists():
                return "C:\\Python312\\python.exe"
        return sys.executable or "python"

    def _to_target_path(self, path_obj: Path) -> str:
        """Format path according to target platform (e.g. normalize /mnt/d to D:\\ for Cursor on Windows)."""
        p_str = str(path_obj)
        if self.target == "cursor":
            if p_str.startswith("/mnt/") and len(p_str) > 6 and p_str[6] == "/":
                drive = p_str[5].upper()
                rest = p_str[6:].replace("/", "\\")
                return f"{drive}:{rest}"
        return p_str
    
    def _find_package_dir(self, pkg_name: str) -> Optional[Path]:
        """Find package directory in tools/ or .cursor/mcp/."""
        candidates = [
            self.workspace_root / "tools" / pkg_name,
            self.workspace_root / ".cursor" / "mcp" / pkg_name,
            self.workspace_root / "mcp",
        ]
        for c in candidates:
            if c.is_dir():
                return c
        return None

    def _add_cursor_framework(self):
        """Add Cursor Framework MCP servers with multi-platform environment variables."""
        workspace = self._to_target_path(self.workspace_root)
        env_vars = {
            "CURSOR_WORKSPACE_ROOT": workspace,
            "ANTIGRAVITY_WORKSPACE_ROOT": workspace,
            "CLAUDE_PROJECT_DIR": workspace,
            "CODEX_WORKSPACE_ROOT": workspace,
            "WINDSURF_WORKSPACE_ROOT": workspace,
            "WORKSPACE_ROOT": workspace,
            "CURSOR_FRAMEWORK_CACHE_MAX_RULES": "20",
            "CURSOR_FRAMEWORK_CACHE_MAX_SKILLS": "30",
            "CURSOR_FRAMEWORK_CACHE_MAX_AGENTS": "10",
            "CURSOR_FRAMEWORK_CACHE_TTL_MINUTES": "30",
        }
        
        # cursor-framework
        framework_dir = self._find_package_dir("cursor-framework-mcp")
        if framework_dir:
            self.config.mcpServers["cursor-framework"] = McpServer(
                command=self.python_cmd,
                args=["-m", "cursor_framework_mcp.server"],
                cwd=self._to_target_path(framework_dir),
                env=env_vars,
                description="Cursor Enterprise Framework - Rules, Skills, Agents registry"
            ).to_dict()
        
        # cursor-autopilot
        autopilot_dir = self._find_package_dir("cursor-autopilot-mcp")
        if autopilot_dir:
            self.config.mcpServers["cursor-autopilot"] = McpServer(
                command=self.python_cmd,
                args=["-m", "cursor_autopilot_mcp.server"],
                cwd=self._to_target_path(autopilot_dir),
                env={
                    **env_vars,
                    "CURSOR_FRAMEWORK_ROOT": self._to_target_path(framework_dir) if framework_dir else "",
                },
                description="Auto-execution engine for workflows, gates, and suggestions"
            ).to_dict()
        
        # cursor-memory
        memory_dir = self._find_package_dir("cursor-memory-mcp")
        if memory_dir:
            cache_dir = self.workspace_root / ".cache" / "cursor-memory-mcp"
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            self.config.mcpServers["cursor-memory"] = McpServer(
                command=self.python_cmd,
                args=["-m", "cursor_memory_mcp.server"],
                cwd=self._to_target_path(memory_dir),
                env={
                    **env_vars,
                    "CURSOR_MEMORY_CACHE_DIR": self._to_target_path(cache_dir),
                    "CURSOR_CONTEXT_TOKEN_BUDGET": "100000",
                    "CURSOR_MEMORY_AUTO_PRUNE": "true",
                },
                description="Persistent workspace memory and context management"
            ).to_dict()
    
    def add_vercel(self):
        """Add Vercel MCP server."""
        self.config.mcpServers["vercel"] = {
            "url": "https://mcp.vercel.com",
            "description": "Vercel AI SDK - Deploy and manage Vercel AI projects"
        }
    
    def add_browser(self):
        """Add Browser MCP server."""
        self.config.mcpServers["browser"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-browser"],
            "description": "Browser MCP - Web automation and scraping"
        }
    
    def add_zalo(self):
        """Add Zalo MCP server."""
        zalo_dir = self.workspace_root / "tools" / "zalo-mcp"
        if zalo_dir.exists():
            self.config.mcpServers["zalo"] = McpServer(
                command="python",
                args=["-m", "zalo_mcp.server"],
                cwd=str(zalo_dir),
                env={
                    "CURSOR_WORKSPACE_ROOT": self.workspace_root,
                },
                description="Zalo API integration for messaging and OA management"
            ).to_dict()
    
    def add_telegram(self):
        """Add Telegram MCP server."""
        self.config.mcpServers["telegram"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-telegram"],
            "description": "Telegram Bot API integration"
        }
    
    def add_facebook(self):
        """Add Facebook MCP server."""
        self.config.mcpServers["facebook"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-facebook"],
            "description": "Facebook Graph API integration"
        }
    
    def add_google(self):
        """Add Google MCP server."""
        google_dir = self.workspace_root / "tools" / "google-mcp"
        if google_dir.exists():
            self.config.mcpServers["google"] = McpServer(
                command="python",
                args=["-m", "google_mcp.server"],
                cwd=str(google_dir),
                env={
                    "CURSOR_WORKSPACE_ROOT": self.workspace_root,
                },
                description="Google APIs integration (Gmail, Drive, Calendar, etc.)"
            ).to_dict()
    
    def add_shopee(self):
        """Add Shopee MCP server."""
        shopee_dir = self.workspace_root / "tools" / "shopee-mcp"
        if shopee_dir.exists():
            self.config.mcpServers["shopee"] = McpServer(
                command="python",
                args=["-m", "shopee_mcp.server"],
                cwd=str(shopee_dir),
                env={
                    "CURSOR_WORKSPACE_ROOT": self.workspace_root,
                },
                description="Shopee API integration for seller operations"
            ).to_dict()

    def add_rea(self):
        """Add REA (Reverse Engineer Anything) MCP server."""
        rea_dir = self.workspace_root / "tools" / "rea"
        rea_script = rea_dir / "scripts" / "rea.mjs"
        if rea_script.exists():
            self.config.mcpServers["rea"] = {
                "command": "node",
                "args": [self._to_target_path(rea_script), "mcp"],
                "cwd": self._to_target_path(rea_dir),
                "description": "REA - Reverse Engineer Anything: native binaries, Electron/JS, APK, WASM via MCP",
            }
        else:
            self.config.mcpServers["rea"] = {
                "command": "npx",
                "args": ["-y", "rea-agents", "mcp"],
                "description": "REA - Reverse Engineer Anything: native binaries, Electron/JS, APK, WASM via MCP",
            }
    
    def add_external(self, name: str, config: dict):
        """Add external MCP server."""
        self.config.mcpServers[name] = config
    
    def to_json(self) -> str:
        """Export configuration as JSON."""
        import datetime
        self.config.syncedAt = datetime.datetime.now().isoformat()
        return json.dumps(self.config.to_dict(), indent=2, ensure_ascii=False)
    
    def save(self, path: str):
        """Save configuration to file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())
        print(f"MCP configuration saved to: {path}")
    
    def print_summary(self):
        """Print configuration summary."""
        print("\n=== MCP Configuration Summary ===")
        print(f"Workspace: {self.workspace_root}")
        print(f"Servers: {len(self.config.mcpServers)}")
        for name in sorted(self.config.mcpServers.keys()):
            desc = self.config.mcpServers[name].get("description", "N/A")
            print(f"  - {name}: {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate MCP configuration for Cursor, Antigravity, Claude Code, Codex, Windsurf, Cline, etc."
    )
    parser.add_argument(
        "--workspace",
        "-w",
        default=".",
        help="Workspace root directory (default: current directory)"
    )
    parser.add_argument(
        "--target",
        "-t",
        default="cursor",
        choices=["cursor", "antigravity", "claude", "codex", "windsurf", "cline", "roo", "all"],
        help="Target vibe coding platform (default: cursor)"
    )
    parser.add_argument(
        "--python-cmd",
        default=None,
        help="Python executable command or path (default: auto-detected per target)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="mcp.json",
        help="Output file path (default: mcp.json)"
    )
    parser.add_argument(
        "--add",
        "-a",
        action="append",
        dest="add_servers",
        choices=["vercel", "browser", "zalo", "telegram", "facebook", "google", "shopee", "rea"],
        help="Add additional MCP servers"
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available servers without generating config"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("=== Available MCP Servers ===")
        print("Built-in:")
        print("  cursor-framework  - Cursor Enterprise Framework registry")
        print("  cursor-autopilot - Auto-execution engine")
        print("  cursor-memory    - Memory and context management")
        print("\nExternal (--add flag):")
        print("  vercel   - Vercel AI SDK")
        print("  browser  - Browser automation")
        print("  zalo     - Zalo API integration")
        print("  telegram - Telegram Bot API")
        print("  facebook - Facebook Graph API")
        print("  google   - Google APIs")
        print("  shopee   - Shopee Seller API")
        print("  rea      - REA Reverse Engineer Anything")
        return 0
    
    # Generate config
    generator = McpConfigGenerator(args.workspace, python_cmd=args.python_cmd, target=args.target)
    
    # Add requested servers
    if args.add_servers:
        for server in args.add_servers:
            if server == "vercel":
                generator.add_vercel()
            elif server == "browser":
                generator.add_browser()
            elif server == "zalo":
                generator.add_zalo()
            elif server == "telegram":
                generator.add_telegram()
            elif server == "facebook":
                generator.add_facebook()
            elif server == "google":
                generator.add_google()
            elif server == "shopee":
                generator.add_shopee()
            elif server == "rea":
                generator.add_rea()
    
    # Print summary
    generator.print_summary()
    
    # Save target configs
    ws = Path(args.workspace).resolve()
    target = args.target

    targets_map = {
        "cursor": ws / ".cursor" / "mcp.json" if (ws / ".cursor").is_dir() else ws / args.output,
        "antigravity": ws / ".gemini" / "antigravity" / "mcp.json" if (ws / ".gemini").is_dir() else ws / "mcp.json",
        "claude": ws / ".claude" / "mcp.json" if (ws / ".claude").is_dir() else ws / "claude_mcp.json",
        "codex": ws / ".codex" / "mcp.json" if (ws / ".codex").is_dir() else ws / "codex_mcp.json",
        "windsurf": ws / ".windsurf" / "mcp_config.json" if (ws / ".windsurf").is_dir() else ws / "windsurf_mcp.json",
        "cline": ws / ".cline" / "cline_mcp_settings.json" if (ws / ".cline").is_dir() else ws / "cline_mcp_settings.json",
        "roo": ws / ".roo" / "cline_mcp_settings.json" if (ws / ".roo").is_dir() else ws / "roo_mcp_settings.json",
    }

    if target == "all":
        # Save default mcp.json
        generator.save(str(ws / args.output))
        for tgt, path in targets_map.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            generator.save(str(path))
    else:
        out_path = targets_map.get(target, ws / args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        generator.save(str(out_path))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
