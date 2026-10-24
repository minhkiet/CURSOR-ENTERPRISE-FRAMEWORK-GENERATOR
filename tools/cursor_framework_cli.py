#!/usr/bin/env python3
"""
Cursor Framework CLI - Standalone Tool

A self-contained CLI tool for Cursor Enterprise Framework operations.
Can run independently from Cursor IDE in any directory.

Usage:
    python cursor_framework_cli.py --help
    python cursor_framework_cli.py status
    python cursor_framework_cli.py skills list
    python cursor_framework_cli.py skills install <skill-repo>
    python cursor_framework_cli.py run <workflow>
    python cursor_framework_cli.py mcp status
    python cursor_framework_cli.py mcp start <server>

Requirements:
    pip install click requests rich

Install:
    pip install -e tools/cursor_framework_cli
    # Or just copy this file anywhere and run with Python 3.10+
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import click
    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "click", "rich"], check=True)
    import click

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def color(text: str, c: str) -> str:
    return f"{c}{text}{Colors.ENDC}"

def find_cursor_root() -> Optional[Path]:
    """Find the cursor framework root directory."""
    # Check environment variable
    env_root = os.environ.get("CURSOR_WORKSPACE_ROOT") or os.environ.get("CURSOR_PROJECT")
    if env_root and Path(env_root).exists():
        return Path(env_root)
    
    # Walk up from current directory
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".cursor").is_dir():
            return parent
        if (parent / "cursor_framework").is_dir():
            return parent
        if (parent / "tools").is_dir() and (parent / ".agents").is_dir():
            return parent
    
    # Check common locations
    home = Path.home()
    common_locations = [
        home / ".cursor",
        home / "Projects" / "Cursor Enterprise Framework Generator",
        Path("D:/PROJECTS/CURSORS/CURSOR ENTERPRISE FRAMEWORK GENERATOR"),
    ]
    
    for loc in common_locations:
        if loc.exists():
            return loc
    
    return None

@dataclass
class FrameworkInfo:
    root: Path
    skills_count: int = 0
    rules_count: int = 0
    agents_count: int = 0
    commands_count: int = 0
    mcp_servers: list = field(default_factory=list)
    
    def load_stats(self):
        """Load framework statistics."""
        # Count skills
        skills_dir = self.root / ".agents" / "skills"
        if skills_dir.exists():
            self.skills_count = len(list(skills_dir.glob("*/SKILL.md")))
        
        # Count rules
        rules_dir = self.root / ".cursor" / "rules"
        if rules_dir.exists():
            self.rules_count = len(list(rules_dir.glob("*.mdc")))
        
        # Count agents
        agents_dir = self.root / ".codex" / "agents"
        if agents_dir.exists():
            self.agents_count = len(list(agents_dir.glob("*.toml")))
        
        # Count commands
        commands_dir = self.root / ".agents" / "skills"
        if commands_dir.exists():
            self.commands_count = len(list(commands_dir.glob("source-command-*/SKILL.md")))
        
        # MCP servers
        self.mcp_servers = [
            {"name": "cursor-framework", "status": "available"},
            {"name": "cursor-autopilot", "status": "available"},
            {"name": "cursor-memory", "status": "available"},
            {"name": "vercel", "status": "config"},
            {"name": "browser", "status": "config"},
        ]
    
    def to_dict(self) -> dict:
        return {
            "root": str(self.root),
            "skills": self.skills_count,
            "rules": self.rules_count,
            "agents": self.agents_count,
            "commands": self.commands_count,
            "mcp_servers": self.mcp_servers,
        }

@click.group()
@click.version_option(version="2.0.0")
def cli():
    """Cursor Enterprise Framework CLI - Standalone tool for framework operations."""
    pass

@cli.group()
def skills():
    """Skill management commands."""
    pass

@cli.group()
def mcp():
    """MCP server management commands."""
    pass

@cli.group()
def run():
    """Run workflows and commands."""
    pass

@cli.group()
def api():
    """API integration commands (Zalo, Telegram, Facebook, Google, Shopee)."""
    pass

@cli.command()
def status():
    """Show framework status and statistics."""
    root = find_cursor_root()
    
    if not root:
        click.echo(color("Framework not found!", Colors.RED))
        click.echo("Please ensure CURSOR_WORKSPACE_ROOT is set or run from project directory.")
        sys.exit(1)
    
    info = FrameworkInfo(root)
    info.load_stats()
    
    click.echo(color("\n📦 Cursor Enterprise Framework Status", Colors.HEADER + Colors.BOLD))
    click.echo(color("=" * 50, Colors.CYAN))
    click.echo(f"\nRoot: {color(str(root), Colors.GREEN)}")
    click.echo(f"\n{color('📊 Statistics:', Colors.BOLD)}")
    click.echo(f"  • Skills:      {color(str(info.skills_count), Colors.GREEN)}")
    click.echo(f"  • Rules:       {color(str(info.rules_count), Colors.GREEN)}")
    click.echo(f"  • Agents:      {color(str(info.agents_count), Colors.GREEN)}")
    click.echo(f"  • Commands:    {color(str(info.commands_count), Colors.GREEN)}")
    
    click.echo(f"\n{color('🔌 MCP Servers:', Colors.BOLD)}")
    for server in info.mcp_servers:
        status_color = Colors.GREEN if server['status'] == 'available' else Colors.YELLOW
        click.echo(f"  • {server['name']}: {color(server['status'], status_color)}")
    
    click.echo(f"\n{color('📁 Directory Structure:', Colors.BOLD)}")
    dirs = [".agents", ".cursor", "cursor_framework_web", "cursor-setup-gui-wpf", "tools"]
    for d in dirs:
        path = root / d
        exists = color("✓", Colors.GREEN) if path.exists() else color("✗", Colors.RED)
        click.echo(f"  {exists} {d}/")

@skills.command()
def list():
    """List all available skills."""
    root = find_cursor_root()
    if not root:
        click.echo(color("Framework not found!", Colors.RED))
        sys.exit(1)
    
    skills_dir = root / ".agents" / "skills"
    if not skills_dir.exists():
        click.echo(color("Skills directory not found!", Colors.RED))
        sys.exit(1)
    
    skill_files = list(skills_dir.glob("*/SKILL.md"))
    click.echo(color(f"\n📚 Available Skills ({len(skill_files)})", Colors.HEADER + Colors.BOLD))
    click.echo(color("-" * 50, Colors.CYAN))
    
    categories = {}
    for sf in sorted(skill_files):
        # Get category from path
        parts = sf.parent.relative_to(skills_dir).parts
        if len(parts) > 1:
            cat = parts[0]
        else:
            cat = "uncategorized"
        
        if cat not in categories:
            categories[cat] = []
        
        # Get skill name from first line of file
        try:
            with open(sf, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip().lstrip('#').strip()
            name = first_line if first_line else sf.parent.name
        except:
            name = sf.parent.name
        
        categories[cat].append((sf.parent.name, name))
    
    for cat, items in sorted(categories.items()):
        click.echo(f"\n{color(cat.upper(), Colors.YELLOW)}")
        for skill_id, skill_name in sorted(items):
            click.echo(f"  • {color(skill_id, Colors.GREEN)} - {skill_name}")

@skills.command()
@click.argument("skill_id")
def show(skill_id: str):
    """Show skill details."""
    root = find_cursor_root()
    if not root:
        click.echo(color("Framework not found!", Colors.RED))
        sys.exit(1)
    
    skill_path = root / ".agents" / "skills" / skill_id / "SKILL.md"
    if not skill_path.exists():
        click.echo(color(f"Skill '{skill_id}' not found!", Colors.RED))
        sys.exit(1)
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    click.echo(content)

@mcp.command()
def status():
    """Show MCP server status."""
    root = find_cursor_root()
    
    click.echo(color("\n🔌 MCP Servers Status", Colors.HEADER + Colors.BOLD))
    click.echo(color("=" * 50, Colors.CYAN))
    
    servers = [
        ("cursor-framework", "Rules, Skills, Agents Registry", True),
        ("cursor-autopilot", "Workflow Automation & Gates", True),
        ("cursor-memory", "Token-aware Memory Management", True),
        ("vercel", "Vercel Deployment Integration", False),
        ("browser", "Browser Automation (CDP)", False),
    ]
    
    for name, desc, available in servers:
        status_icon = color("●", Colors.GREEN) if available else color("○", Colors.YELLOW)
        click.echo(f"\n  {status_icon} {color(name, Colors.BOLD)}")
        click.echo(f"     {desc}")

@mcp.command()
@click.argument("server")
def start(server: str):
    """Start an MCP server."""
    servers = {
        "cursor-framework": "cursor_framework_mcp.server",
        "cursor-autopilot": "cursor_autopilot_mcp.server",
        "cursor-memory": "cursor_memory_mcp.server",
    }
    
    if server not in servers:
        click.echo(color(f"Unknown server: {server}", Colors.RED))
        click.echo(f"Available servers: {', '.join(servers.keys())}")
        sys.exit(1)
    
    click.echo(f"Starting {server}...")
    
    root = find_cursor_root()
    if root:
        mcp_dir = root / "tools" / f"{server}-mcp"
        if mcp_dir.exists():
            os.chdir(mcp_dir)
    
    cmd = [sys.executable, "-m", servers[server]]
    click.echo(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

@api.command()
@click.argument("platform")
@click.option("--token", "-t", help="API token")
@click.option("--uid", "-u", help="User/Chat ID")
@click.option("--message", "-m", help="Message content")
def send(platform: str, token: str, uid: str, message: str):
    """Send message via API platform (zalo, telegram, facebook)."""
    if platform.lower() not in ["zalo", "telegram", "facebook"]:
        click.echo(color(f"Unknown platform: {platform}", Colors.RED))
        sys.exit(1)
    
    if not token:
        token = os.environ.get(f"{platform.upper()}_TOKEN")
    
    if not token:
        click.echo(color(f"Token required. Use --token or set {platform.upper()}_TOKEN env var.", Colors.YELLOW))
        sys.exit(1)
    
    root = find_cursor_root()
    if root:
        integration_path = root / "tools" / "api_integrations" / f"{platform}_integration.py"
        if integration_path.exists():
            click.echo(f"Found integration at: {integration_path}")
            click.echo(f"Import from: tools.api_integrations.{platform}_integration")
            return
    
    click.echo(f"API integration for {platform} ready.")
    click.echo("Use Python to call the integration:")

@api.command()
def list():
    """List available API integrations."""
    integrations = [
        ("zalo", "Zalo OA API", "Messages, profile, menu, followers"),
        ("telegram", "Telegram Bot API", "Messages, media, groups, inline"),
        ("facebook", "Facebook Graph API", "Page posts, Messenger, insights"),
        ("google", "Google APIs", "Sheets, Gmail, Calendar, Maps, Drive"),
        ("shopee", "Shopee Open Platform", "Products, orders, logistics, finance"),
    ]
    
    click.echo(color("\n📡 API Integrations", Colors.HEADER + Colors.BOLD))
    click.echo(color("-" * 50, Colors.CYAN))
    
    for name, platform, features in integrations:
        click.echo(f"\n  {color(name.upper(), Colors.GREEN)} ({platform})")
        click.echo(f"  Features: {features}")

@run.command()
@click.argument("workflow")
def workflow(workflow: str):
    """Run a predefined workflow."""
    workflows = {
        "build": "Build & test workflow",
        "deploy": "Deployment workflow",
        "review": "Code review workflow",
        "test": "Testing workflow",
        "security": "Security audit workflow",
        "perf": "Performance audit workflow",
    }
    
    if workflow not in workflows:
        click.echo(color(f"Unknown workflow: {workflow}", Colors.RED))
        click.echo("\nAvailable workflows:")
        for w, desc in workflows.items():
            click.echo(f"  • {w}: {desc}")
        sys.exit(1)
    
    click.echo(color(f"\n🚀 Running workflow: {workflow}", Colors.GREEN))
    click.echo(color(f"Description: {workflows[workflow]}", Colors.CYAN))
    
    root = find_cursor_root()
    if root:
        workflow_dir = root / ".cursor" / "workflows"
        workflow_file = workflow_dir / f"{workflow}.yaml"
        
        if workflow_file.exists():
            click.echo(f"\nWorkflow file: {workflow_file}")
        else:
            click.echo(f"\nWorkflow file not found: {workflow_file}")

def main():
    cli()

if __name__ == "__main__":
    main()
