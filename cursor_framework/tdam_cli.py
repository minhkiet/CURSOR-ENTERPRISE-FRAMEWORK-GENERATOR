"""
TDAM CLI - TencentDB Agent Memory Command-Line Interface

A beautiful, user-friendly CLI for managing agent memory operations.
Supports layered memory (L0-L3), symbolic memory (Mermaid), and context compression.

Usage:
    python -m cursor_framework.tdam_cli status
    python -m cursor_framework.tdam_cli capture --session s1 --message "Hello"
    python -m cursor_framework.tdam_cli recall --query "preferences"
    python -m cursor_framework.tdam_cli compact --session s1 --ratio 0.7
    python -m cursor_framework.tdam_cli persona --read
    python -m cursor_framework.tdam_cli persona --write "# Updated Profile"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Windows encoding fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from cursor_framework import (
    TDAMIntegration,
    TDAMConfig,
    MemoryLayer,
    ConversationTurn,
)


# ============================================================
# Console Output Helpers
# ============================================================

class RichConsole:
    """Beautiful console output wrapper with Windows encoding support."""

    def __init__(self):
        self.console = Console() if HAS_RICH else None
        self._has_rich = HAS_RICH
        self._setup_windows_encoding()

    def _setup_windows_encoding(self):
        """Setup Windows console for UTF-8."""
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding="utf-8")
                sys.stderr.reconfigure(encoding="utf-8")
            except (AttributeError, OSError):
                pass

    def print(self, text: str = "", style: str = "", **kwargs):
        if self._has_rich and self.console:
            self.console.print(text, style=style, **kwargs)
        else:
            print(text)

    def print_panel(self, title: str, content: str, border_style: str = "blue"):
        if self._has_rich and self.console:
            panel = Panel(content, title=title, border_style=border_style)
            self.console.print(panel)
        else:
            print(f"=== {title} ===\n{content}")

    def print_table(self, title: str, headers: list, rows: list, success: bool = True):
        if self._has_rich and self.console:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            for h in headers:
                table.add_column(h)
            for row in rows:
                table.add_row(*[str(c) for c in row])
            self.console.print(table)
        else:
            print(f"\n=== {title} ===")
            print(" | ".join(headers))
            print("-" * 60)
            for row in rows:
                print(" | ".join(str(c) for c in row))

    def print_tree(self, title: str, items: list[tuple]):
        if self._has_rich and self.console:
            tree = Tree(f"[bold blue]{title}[/bold blue]")
            for label, value in items:
                tree.add(f"[yellow]{label}:[/yellow] {value}")
            self.console.print(tree)
        else:
            print(f"\n=== {title} ===")
            for label, value in items:
                print(f"  {label}: {value}")

    def print_code(self, title: str, code: str, language: str = "markdown"):
        if self._has_rich and self.console:
            syntax = Syntax(code, language, theme="monokai", line_numbers=True)
            panel = Panel(syntax, title=title, border_style="green")
            self.console.print(panel)
        else:
            print(f"\n=== {title} ===\n{code}")

    def print_markdown(self, content: str):
        if self._has_rich and self.console:
            md = Markdown(content)
            self.console.print(md)
        else:
            print(content)

    def print_success(self, message: str):
        if self._has_rich and self.console:
            self.console.print(f"[bold green]✓[/bold green] {message}")
        else:
            print(f"✓ {message}")

    def print_error(self, message: str):
        if self._has_rich and self.console:
            self.console.print(f"[bold red]✗[/bold red] {message}")
        else:
            print(f"✗ {message}")

    def print_warning(self, message: str):
        if self._has_rich and self.console:
            self.console.print(f"[bold yellow]![/bold yellow] {message}")
        else:
            print(f"! {message}")

    def print_info(self, message: str):
        if self._has_rich and self.console:
            self.console.print(f"[bold cyan]ℹ[/bold cyan] {message}")
        else:
            print(f"ℹ {message}")

    def print_header(self, text: str):
        if self._has_rich and self.console:
            self.console.print(f"\n[bold cyan]═══[/bold cyan] [bold white]{text}[/bold white] [bold cyan]═══[/bold cyan]\n")
        else:
            print(f"\n{'='*20} {text} {'='*20}\n")


# ============================================================
# TDAM CLI Commands
# ============================================================

class TDAMCLI:
    """TDAM Command-Line Interface."""

    def __init__(self, config: Optional[TDAMConfig] = None):
        self.console = RichConsole()
        self.config = config or TDAMConfig()
        self._load_config_from_env()
        self.tdam = TDAMIntegration(self.config)

    def _load_config_from_env(self):
        """Load configuration from environment variables."""
        self.config.endpoint = os.getenv("TDAM_ENDPOINT", self.config.endpoint)
        self.config.api_key = os.getenv("TDAM_API_KEY", self.config.api_key)
        self.config.service_id = os.getenv("TDAM_SERVICE_ID", self.config.service_id)

    def status(self):
        """Show TDAM connection status and configuration."""
        self.console.print_header("TDAM Status")

        # Connection status
        is_connected = self.tdam.is_available()
        status_color = "green" if is_connected else "red"
        status_text = "Connected" if is_connected else "Not Connected"

        self.console.print_tree(
            "Connection Status",
            [
                ("Status", f"[{status_color}]{status_text}[/{status_color}]"),
                ("Endpoint", self.config.endpoint),
                ("Service ID", self.config.service_id or "Not set"),
                ("API Key", "***" + self.config.api_key[-4:] if self.config.api_key else "Not set"),
            ]
        )

        # Configuration
        self.console.print_tree(
            "Configuration",
            [
                ("Recall Strategy", self.config.recall_strategy),
                ("Max Results", str(self.config.max_results)),
                ("Offload Enabled", str(self.config.offload_enabled)),
                ("Mild Offload Ratio", str(self.config.mild_offload_ratio)),
                ("Aggressive Ratio", str(self.config.aggressive_compress_ratio)),
            ]
        )

        # Memory layers info
        self.console.print_markdown("""
### Memory Layers

| Layer | Description | Storage |
|-------|-------------|---------|
| **L0** | Raw conversation | `conversations/` |
| **L1** | Atomic memories | Vector DB / SQLite |
| **L2** | Scenario blocks | `scene_blocks/*.md` |
| **L3** | User persona | `persona.md` |
""")

    def capture(self, session_id: str, messages: list[str], role: str = "user"):
        """Capture conversation messages."""
        self.console.print_header(f"Capture Messages - Session: {session_id}")

        turns = [
            ConversationTurn(
                role=role,
                content=msg,
                timestamp=datetime.now(),
            )
            for msg in messages
        ]

        self.console.print_info(f"Capturing {len(turns)} message(s)...")

        result = self.tdam.capture_conversation(session_id, turns)

        if "error" in result:
            self.console.print_error(f"Failed: {result['error']}")
            return False

        self.console.print_success(f"Captured {len(result.get('accepted_ids', []))} message(s)")
        return True

    def recall(self, query: str, layers: Optional[list[str]] = None, limit: int = 5):
        """Recall memories by query."""
        self.console.print_header(f"Recall Memories - Query: {query}")

        # Parse layers
        layer_map = {
            "l0": MemoryLayer.L0_CONVERSATION,
            "l1": MemoryLayer.L1_ATOM,
            "l2": MemoryLayer.L2_SCENARIO,
            "l3": MemoryLayer.L3_PERSONA,
        }
        search_layers = None
        if layers:
            search_layers = [layer_map.get(l.lower()) for l in layers if l.lower() in layer_map]
            search_layers = [l for l in search_layers if l]

        self.console.print_info(f"Searching in layers: {layers or 'all'} (limit: {limit})...")

        items = self.tdam.recall(query, layers=search_layers, limit=limit)

        if not items:
            self.console.print_warning("No memories found")
            return []

        # Display results
        table_data = []
        for item in items:
            content_preview = item.content[:60] + "..." if len(item.content) > 60 else item.content
            table_data.append([
                item.layer.value.upper(),
                f"{item.score:.2f}",
                content_preview,
            ])

        self.console.print_table(
            f"Found {len(items)} Memories",
            ["Layer", "Score", "Content"],
            table_data
        )

        return items

    def compact(self, session_id: str, messages: list[str], ratio: float = 0.7, context_window: int = 128000):
        """Compact context into Mermaid canvas."""
        self.console.print_header(f"Compact Context - Session: {session_id}")

        self.console.print_info(f"Ratio: {ratio}, Context Window: {context_window:,} tokens")

        turns = [
            ConversationTurn(role="user" if i % 2 == 0 else "assistant", content=msg)
            for i, msg in enumerate(messages)
        ]

        result = self.tdam.compact_context(session_id, turns, ratio=ratio, context_window=context_window)

        if not result:
            self.console.print_error("Compaction failed")
            return None

        # Show stats
        self.console.print_tree(
            "Compression Results",
            [
                ("Tokens Before", f"{result.tokens_before:,}"),
                ("Tokens After", f"{result.tokens_after:,}"),
                ("Savings", f"{result.tokens_before - result.tokens_after:,} ({(1-ratio)*100:.0f}%)"),
                ("Compression Ratio", f"{result.compression_ratio:.1%}"),
                ("Messages Before", str(len(messages))),
                ("Messages After", str(len(result.messages))),
            ]
        )

        # Show Mermaid canvas
        if result.mermaid_canvas:
            self.console.print_code("Mermaid Canvas", result.mermaid_canvas, "mermaid")

        return result

    def persona_read(self):
        """Read user persona."""
        self.console.print_header("User Persona (L3)")

        persona = self.tdam.get_persona()

        if not persona:
            self.console.print_warning("No persona found")
            return None

        self.console.print_code("Persona", persona, "markdown")
        return persona

    def persona_write(self, content: str):
        """Write user persona."""
        self.console.print_header("Update Persona")

        self.console.print_info("Current persona preview:")
        self.console.print_code("Old Persona", self.tdam.get_persona() or "(empty)", "markdown")

        self.console.print_info("New persona:")
        self.console.print_code("New Persona", content, "markdown")

        if Confirm.ask("[yellow]Update persona?[/yellow]"):
            success = self.tdam.update_persona(content)
            if success:
                self.console.print_success("Persona updated")
            else:
                self.console.print_error("Failed to update persona")
            return success

        return False

    def persona_interactive(self):
        """Interactive persona editor."""
        self.console.print_header("Interactive Persona Editor")

        current = self.tdam.get_persona() or ""

        self.console.print_info("Current persona (or empty):")
        if current:
            self.console.print(current[:500] + ("..." if len(current) > 500 else ""))
        else:
            self.console.print("(empty)")

        print()
        print("Select an action:")
        print("  1. View full persona")
        print("  2. Edit persona (replace all)")
        print("  3. Append to persona")
        print("  4. Clear persona")
        print("  5. Exit")

        choice = Prompt.ask(
            "[cyan]Choice[/cyan]",
            choices=["1", "2", "3", "4", "5"],
            default="5"
        )

        if choice == "1":
            self.persona_read()
        elif choice == "2":
            new_content = Prompt.ask("[cyan]Enter new persona (Markdown)[/cyan]")
            self.persona_write(new_content)
        elif choice == "3":
            append = Prompt.ask("[cyan]Content to append[/cyan]")
            new_content = (current + "\n\n" + append).strip()
            self.persona_write(new_content)
        elif choice == "4":
            if Confirm.ask("[red]Clear persona?[/red]"):
                self.persona_write("")
        # choice == "5" - exit

    def scenarios_list(self, prefix: str = ""):
        """List scenario files."""
        self.console.print_header(f"Scenarios - Prefix: '{prefix or '(root)'}'")

        scenarios = self.tdam.list_scenarios(prefix)

        if not scenarios:
            self.console.print_warning("No scenarios found")
            return []

        table_data = [[s] for s in scenarios]
        self.console.print_table("Scenarios", ["Path"], table_data)

        return scenarios

    def scenarios_read(self, path: str):
        """Read a scenario file."""
        self.console.print_header(f"Read Scenario: {path}")

        content = self.tdam.get_scenario(path)

        if not content:
            self.console.print_error(f"Scenario not found: {path}")
            return None

        self.console.print_code(f"Scenario: {path}", content, "markdown")
        return content

    def tool_call(self, session_id: str, tool_name: str, params: str, result: str):
        """Capture a tool call (fire-and-forget)."""
        self.console.print_header(f"Tool Call - Session: {session_id}")

        try:
            params_dict = json.loads(params) if params else {}
        except json.JSONDecodeError:
            params_dict = {"raw": params}

        success = self.tdam.capture_tool_call(
            session_id=session_id,
            tool_name=tool_name,
            params=params_dict,
            result=result,
        )

        if success:
            self.console.print_success(f"Captured {tool_name} call")
        else:
            self.console.print_error("Failed to capture tool call")

        return success

    def build_context(self, session_id: str, task: str, max_tokens: int = 4000):
        """Build complete context from all memory layers."""
        self.console.print_header(f"Build Context - Session: {session_id}")

        context = self.tdam.build_context(session_id, task, max_tokens)

        # Show summary
        self.console.print_tree(
            "Context Summary",
            [
                ("Task", task),
                ("Max Tokens", str(max_tokens)),
                ("Persona", "Yes" if context.get("persona") else "No"),
                ("Memories", str(len(context.get("memories", [])))),
                ("Total Tokens", str(context.get("total_tokens", 0))),
            ]
        )

        # Show persona if exists
        if context.get("persona"):
            self.console.print_code("Persona (L3)", context["persona"][:500] + "...", "markdown")

        # Show memories
        memories = context.get("memories", [])
        if memories:
            table_data = [
                [m["content"][:50] + "...", f"{m['score']:.2f}"]
                for m in memories
            ]
            self.console.print_table("Relevant Memories (L1)", ["Content", "Score"], table_data)

        return context


# ============================================================
# CLI Entry Point
# ============================================================

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="TDAM CLI - TencentDB Agent Memory CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s capture --session s1 --message "Hello" --message "How are you?"
  %(prog)s recall --query "preferences"
  %(prog)s recall --query "project" --layers l1 l2 --limit 10
  %(prog)s compact --session s1 --ratio 0.7 --message "Long conversation..."
  %(prog)s persona --read
  %(prog)s persona --write "# My Profile"
  %(prog)s persona --interactive
  %(prog)s scenarios --list
  %(prog)s scenarios --read "project-workflow.md"
  %(prog)s tool-call --session s1 --tool search --params '{"q":"python"}' --result "Python results"
  %(prog)s build-context --session s1 --task "build dashboard"
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Status command
    subparsers.add_parser("status", help="Show TDAM connection status")

    # Capture command
    capture = subparsers.add_parser("capture", help="Capture conversation messages")
    capture.add_argument("--session", "-s", required=True, help="Session ID")
    capture.add_argument("--message", "-m", action="append", required=True, help="Message content")
    capture.add_argument("--role", "-r", default="user", choices=["user", "assistant", "system"], help="Message role")

    # Recall command
    recall = subparsers.add_parser("recall", help="Recall memories")
    recall.add_argument("--query", "-q", required=True, help="Search query")
    recall.add_argument("--layers", "-l", nargs="+", help="Memory layers (l0, l1, l2, l3)")
    recall.add_argument("--limit", "-n", type=int, default=5, help="Max results")

    # Compact command
    compact = subparsers.add_parser("compact", help="Compact context to Mermaid")
    compact.add_argument("--session", "-s", required=True, help="Session ID")
    compact.add_argument("--message", "-m", action="append", required=True, help="Message content")
    compact.add_argument("--ratio", "-r", type=float, default=0.7, help="Compression ratio")
    compact.add_argument("--context-window", "-w", type=int, default=128000, help="Context window size")

    # Persona command
    persona = subparsers.add_parser("persona", help="Manage user persona")
    persona.add_argument("--read", action="store_true", help="Read persona")
    persona.add_argument("--write", "-w", help="Write persona content")
    persona.add_argument("--interactive", "-i", action="store_true", help="Interactive editor")

    # Scenarios command
    scenarios = subparsers.add_parser("scenarios", help="Manage scenarios")
    scenarios.add_argument("--list", "-l", action="store_true", help="List scenarios")
    scenarios.add_argument("--read", "-r", help="Read scenario by path")

    # Tool call command
    toolcall = subparsers.add_parser("tool-call", help="Capture tool call")
    toolcall.add_argument("--session", "-s", required=True, help="Session ID")
    toolcall.add_argument("--tool", "-t", required=True, help="Tool name")
    toolcall.add_argument("--params", "-p", default="{}", help="Tool parameters (JSON)")
    toolcall.add_argument("--result", "-r", required=True, help="Tool result")

    # Build context command
    buildctx = subparsers.add_parser("build-context", help="Build full context")
    buildctx.add_argument("--session", "-s", required=True, help="Session ID")
    buildctx.add_argument("--task", "-t", required=True, help="Current task")
    buildctx.add_argument("--max-tokens", "-m", type=int, default=4000, help="Max tokens")

    return parser


def main():
    """Main entry point."""
    if not HAS_RICH:
        print("Warning: 'rich' library not installed. Install with: pip install rich")
        print("Output will be less colorful but functional.\n")

    # When invoked via `python -m cursor_framework tdam <cmd> ...`,
    # the leading `tdam` is just a routing key — strip it before parsing.
    argv = sys.argv[1:]
    if argv and argv[0] == "tdam":
        sys.argv = [sys.argv[0]] + argv[1:]

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    console = RichConsole()

    try:
        cli = TDAMCLI()

        if args.command == "status":
            cli.status()

        elif args.command == "capture":
            cli.capture(args.session, args.message, args.role)

        elif args.command == "recall":
            cli.recall(args.query, args.layers, args.limit)

        elif args.command == "compact":
            cli.compact(args.session, args.message, args.ratio, args.context_window)

        elif args.command == "persona":
            if args.interactive:
                cli.persona_interactive()
            elif args.write:
                cli.persona_write(args.write)
            elif args.read:
                cli.persona_read()
            else:
                parser.parse_args(["persona", "-h"])

        elif args.command == "scenarios":
            if args.list:
                cli.scenarios_list()
            elif args.read:
                cli.scenarios_read(args.read)
            else:
                parser.parse_args(["scenarios", "-h"])

        elif args.command == "tool-call":
            cli.tool_call(args.session, args.tool, args.params, args.result)

        elif args.command == "build-context":
            cli.build_context(args.session, args.task, args.max_tokens)

    except KeyboardInterrupt:
        console.print_warning("Interrupted")
    except Exception as e:
        console.print_error(f"Error: {e}")
        if os.getenv("DEBUG"):
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
