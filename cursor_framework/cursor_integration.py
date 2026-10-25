"""
Cursor Integration Module

Provides integration layer for Cursor IDE to consume the framework's
context and memory systems.

Features:
    - CLI command to dump current context state
    - Generates `.cursor/context.json` for Cursor to read
    - REST API endpoints for real-time queries
    - Integrates with Workflow system
    - Context enrichment for Cursor sessions

Usage:
    >>> from cursor_framework.cursor_integration import CursorIntegration
    >>> ci = CursorIntegration(root=".")
    >>> ci.dump_context()
    >>> ci.serve()  # Start REST API

    # CLI:
    >>> python -m cursor_framework dump-context
    >>> python -m cursor_framework serve-api --port 8767
"""

from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional

from .code_graph import CodeGraph, CodeGraphResult
from .session_memory import SessionMemory, SessionStats
from .workflow import Workflow

logger = logging.getLogger(__name__)


# Default API settings
DEFAULT_API_HOST = "127.0.0.1"
DEFAULT_API_PORT = 8767


@dataclass
class CursorContext:
    """Context state for Cursor to consume."""
    project: str
    root: str
    generated_at: str
    session_id: str
    files_read: list[str] = field(default_factory=list)
    recent_files: list[str] = field(default_factory=list)
    token_summary: dict[str, Any] = field(default_factory=dict)
    code_graph_summary: dict[str, Any] = field(default_factory=dict)
    skills_in_context: list[str] = field(default_factory=list)
    cache_hit_rate: float = 0.0


@dataclass
class APIResponse:
    """Standard API response wrapper."""
    success: bool
    data: Any = None
    error: str = ""
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp,
        }


class CursorIntegration:
    """
    Integration layer between Cursor and the framework.

    Provides:
        - Context dumping for Cursor consumption
        - REST API for real-time queries
        - Workflow integration
        - Code graph access
        - Session memory tracking
    """

    def __init__(
        self,
        root: str | Path = ".",
        cache_path: str | Path = ".cache/session_memory.json",
        context_path: str | Path = ".cursor/context.json",
        session_id: Optional[str] = None,
    ) -> None:
        """
        Initialize Cursor integration.

        Args:
            root: Project root directory
            cache_path: Session memory cache path
            context_path: Output path for context.json
            session_id: Unique session identifier
        """
        self.root = Path(root).resolve()
        self.cache_path = Path(cache_path)
        self.context_path = Path(context_path)
        self.session_id = session_id or self._generate_session_id()

        # Initialize components
        self.session_memory = SessionMemory(cache_path=self.cache_path)
        self.code_graph: Optional[CodeGraph] = None
        self._workflow: Optional[Workflow] = None

        # API server state
        self._api_server: Optional[ThreadingHTTPServer] = None
        self._api_thread: Optional[threading.Thread] = None
        self._api_running = False

    @staticmethod
    def _generate_session_id() -> str:
        """Generate a unique session ID."""
        timestamp = str(time.time()).encode()
        return hashlib.md5(timestamp).hexdigest()[:12]

    def _get_workflow(self) -> Workflow:
        """Lazy initialization of Workflow."""
        if self._workflow is None:
            self._workflow = Workflow(
                root=str(self.root / ".cursor"),
                memory_path=str(self.root / self.cache_path),
            )
        return self._workflow

    def get_code_graph(self, force_rescan: bool = False) -> CodeGraphResult:
        """
        Get or build the code graph.

        Args:
            force_rescan: Force a fresh scan

        Returns:
            CodeGraphResult
        """
        if self.code_graph is None or force_rescan:
            self.code_graph = CodeGraph(root=self.root)
            self.code_graph.scan()
        return self.code_graph.result

    def dump_context(
        self,
        output_path: Optional[str | Path] = None,
        include_graph: bool = True,
    ) -> Path:
        """
        Dump current context state to `.cursor/context.json`.

        Args:
            output_path: Override output path
            include_graph: Include code graph summary

        Returns:
            Path to the dumped file
        """
        output = output_path or self.context_path
        path = Path(output)

        # Build context
        token_summary = self.session_memory.get_token_summary()
        recent = self.session_memory.get_recent_files(limit=20)

        context = {
            "project": self.root.name,
            "root": str(self.root),
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "session_id": self.session_id,
            "files_read": list(self.session_memory._reads.keys()),
            "recent_files": recent,
            "token_summary": token_summary,
            "cache_hit_rate": token_summary.get("cache_hit_rate", 0),
        }

        # Add code graph summary if available
        if include_graph:
            try:
                graph = self.get_code_graph()
                context["code_graph_summary"] = {
                    "module_count": graph.module_count,
                    "dependency_count": graph.dependency_count,
                    "languages": graph.languages,
                    "scanned_at": graph.scanned_at,
                }
            except Exception as e:
                logger.warning("Failed to include code graph: %s", e)

        # Add skills from workflow
        try:
            workflow = self._get_workflow()
            stats = workflow.stats()
            context["skills_in_context"] = list(
                workflow.builder.discovery._skill_file_cache.keys()
            )[:20]  # Top 20
            context["workflow_stats"] = {
                "memory_hits": stats.get("memory_hits", 0),
                "memory_misses": stats.get("memory_misses", 0),
                "assets_indexed": stats.get("assets_indexed", 0),
            }
        except Exception as e:
            logger.warning("Failed to include workflow stats: %s", e)

        # Write to file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(context, indent=2, ensure_ascii=False), encoding="utf-8")

        logger.info("Context dumped to %s", path)
        return path

    def mark_file_read(
        self,
        file_path: str,
        tokens: int,
        context_lines: int = 0,
    ) -> bool:
        """
        Mark a file as read for the session.

        Args:
            file_path: Path to the file
            tokens: Token count
            context_lines: Number of lines read

        Returns:
            True if new read, False if cached
        """
        # Compute content hash if file exists
        content_hash = ""
        try:
            content = Path(file_path).read_text(encoding="utf-8", errors="replace")
            content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
        except OSError:
            pass

        return self.session_memory.mark_file_read(
            file_path=file_path,
            tokens=tokens,
            context_lines=context_lines,
            content_hash=content_hash,
        )

    def check_file_freshness(self, file_path: str) -> bool:
        """
        Check if a cached file is still fresh.

        Args:
            file_path: Path to check

        Returns:
            True if file is unchanged, False if modified
        """
        try:
            content = Path(file_path).read_text(encoding="utf-8", errors="replace")
            current_hash = hashlib.md5(content.encode()).hexdigest()[:12]
            return not self.session_memory.check_file_changed(file_path, current_hash)
        except OSError:
            return False

    def get_context_for_file(self, file_path: str) -> dict[str, Any]:
        """
        Get cached context for a specific file.

        Args:
            file_path: Path to the file

        Returns:
            Context dict or empty dict
        """
        return self.session_memory.get_context(file_path) or {}

    def build_context_prompt(
        self,
        current_file: str,
        max_tokens: int = 4000,
    ) -> str:
        """
        Build a context prompt for Cursor based on session state.

        Args:
            current_file: Current file being edited
            max_tokens: Maximum tokens for context

        Returns:
            Context string
        """
        parts = ["## Session Context"]

        # Add recent files
        recent = self.session_memory.get_recent_files(limit=5)
        if recent:
            parts.append(f"\n### Recently Read Files\n- " + "\n- ".join(recent))

        # Add token summary
        summary = self.session_memory.get_token_summary()
        parts.append(f"\n### Token Usage\n- Files: {summary['files_read']}")
        parts.append(f"- Tokens: {summary['total_tokens']}")
        parts.append(f"- Cache hit rate: {summary['cache_hit_rate']}%")

        # Add code graph summary
        try:
            graph = self.get_code_graph()
            parts.append(f"\n### Project Structure")
            parts.append(f"- Modules: {graph.module_count}")
            parts.append(f"- Dependencies: {graph.dependency_count}")
            parts.append(f"- Languages: {', '.join(graph.languages.keys())}")
        except Exception:
            pass

        # Add related files from code graph
        if current_file:
            try:
                graph = self.get_code_graph()
                module = graph.find_module(Path(current_file).stem)
                if module:
                    deps = graph.find_dependents(module.path)
                    if deps:
                        dep_names = [d.name for d in deps[:5]]
                        parts.append(f"\n### Related Files\n- " + "\n- ".join(dep_names))
            except Exception:
                pass

        return "\n".join(parts)

    def serve(
        self,
        host: str = DEFAULT_API_HOST,
        port: int = DEFAULT_API_PORT,
        background: bool = False,
    ) -> None:
        """
        Start the REST API server.

        Args:
            host: Bind host
            port: Bind port
            background: Run in background thread
        """
        if self._api_running:
            logger.warning("API server already running")
            return

        self._api_running = True

        # Create API handler with self reference
        integration = self

        class APIHandler(BaseHTTPRequestHandler):
            def log_message(self, *args, **kwargs):
                pass  # Silence logs

            def _send_json(self, status: int, data: dict) -> None:
                """Send JSON response."""
                body = json.dumps(data, ensure_ascii=False).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)

            def _ok(self, data: Any = None) -> None:
                self._send_json(200, APIResponse(
                    success=True,
                    data=data,
                    timestamp=datetime.now().isoformat(timespec="seconds"),
                ).to_dict())

            def _error(self, message: str, status: int = 400) -> None:
                self._send_json(status, APIResponse(
                    success=False,
                    error=message,
                    timestamp=datetime.now().isoformat(timespec="seconds"),
                ).to_dict())

            def do_GET(self) -> None:  # noqa: N802
                path = self.path.split("?")[0]

                # Health check
                if path == "/health":
                    self._ok({"status": "ok", "session_id": integration.session_id})
                    return

                # Get context summary
                if path == "/api/context":
                    self._ok(integration.session_memory.export_context())
                    return

                # Get token stats
                if path == "/api/stats":
                    self._ok(integration.session_memory.get_token_summary())
                    return

                # Get code graph
                if path == "/api/graph":
                    graph = integration.get_code_graph()
                    self._ok(graph.to_dict() if graph else {})
                    return

                # Get recent files
                if path == "/api/recent":
                    limit = 10
                    if "limit=" in self.path:
                        try:
                            limit = int(self.path.split("limit=")[1].split("&")[0])
                        except (ValueError, IndexError):
                            pass
                    self._ok({"files": integration.session_memory.get_recent_files(limit)})
                    return

                # Get file context
                if path.startswith("/api/file/"):
                    file_path = path[9:]  # Strip "/api/file/"
                    file_path = file_path.replace("%20", " ")
                    context = integration.get_context_for_file(file_path)
                    self._ok(context if context else {"found": False})
                    return

                self._error("Not found", 404)

            def do_POST(self) -> None:  # noqa: N802
                path = self.path.split("?")[0]

                # Read body
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length) if content_length > 0 else b"{}"

                try:
                    data = json.loads(body.decode("utf-8"))
                except json.JSONDecodeError:
                    self._error("Invalid JSON")
                    return

                # Mark file read
                if path == "/api/read":
                    file_path = data.get("file_path")
                    tokens = data.get("tokens", 0)
                    context_lines = data.get("context_lines", 0)
                    if not file_path:
                        self._error("file_path required")
                        return
                    is_new = integration.mark_file_read(file_path, tokens, context_lines)
                    self._ok({"new_read": is_new})
                    return

                # Check freshness
                if path == "/api/fresh":
                    file_path = data.get("file_path")
                    if not file_path:
                        self._error("file_path required")
                        return
                    is_fresh = integration.check_file_freshness(file_path)
                    self._ok({"fresh": is_fresh})
                    return

                # Dump context
                if path == "/api/dump":
                    path = integration.dump_context()
                    self._ok({"dumped": str(path)})
                    return

                # Clear session
                if path == "/api/clear":
                    result = integration.session_memory.clear_session()
                    self._ok(result)
                    return

                self._error("Not found", 404)

            def do_OPTIONS(self) -> None:  # noqa: N802
                """Handle CORS preflight."""
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

        def run_server() -> None:
            server = ThreadingHTTPServer((host, port), APIHandler)
            integration._api_server = server
            logger.info("API server starting on %s:%s", host, port)
            try:
                while integration._api_running:
                    server.handle_request()
            except Exception as e:
                if integration._api_running:
                    logger.error("API server error: %s", e)
            finally:
                server.server_close()

        if background:
            self._api_thread = threading.Thread(target=run_server, daemon=True)
            self._api_thread.start()
            logger.info("API server running in background on %s:%s", host, port)
        else:
            run_server()

    def stop_api(self) -> None:
        """Stop the REST API server."""
        self._api_running = False
        if self._api_server:
            self._api_server.shutdown()
            self._api_server = None
        if self._api_thread:
            self._api_thread.join(timeout=2)
            self._api_thread = None

    def get_endpoints(self) -> dict[str, str]:
        """
        Get list of available API endpoints.

        Returns:
            Dict of endpoint -> description
        """
        return {
            "GET /health": "Health check",
            "GET /api/context": "Get full session context",
            "GET /api/stats": "Get token statistics",
            "GET /api/graph": "Get code graph",
            "GET /api/recent?limit=N": "Get recently read files",
            "GET /api/file/<path>": "Get context for a file",
            "POST /api/read": "Mark file as read",
            "POST /api/fresh": "Check file freshness",
            "POST /api/dump": "Dump context to file",
            "POST /api/clear": "Clear session memory",
        }


def create_integration(
    root: str | Path = ".",
) -> CursorIntegration:
    """
    Factory function to create CursorIntegration.

    Args:
        root: Project root directory

    Returns:
        Configured CursorIntegration instance
    """
    return CursorIntegration(root=root)


def main() -> int:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Cursor Integration CLI")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--cache-path", default=".cache/session_memory.json",
                        help="Session memory path")
    sub = parser.add_parser("dump-context", help="Dump context to .cursor/context.json")
    sub.add_argument("--output", help="Output path")

    serve = argparse.ArgumentParser()
    serve.add_argument("--host", default=DEFAULT_API_HOST)
    serve.add_argument("--port", type=int, default=DEFAULT_API_PORT)

    args = parser.parse_args()

    integration = CursorIntegration(root=args.root, cache_path=args.cache_path)

    if args.subcommand == "dump-context":
        path = integration.dump_context()
        print(f"Context dumped to: {path}")
    elif args.subcommand == "serve":
        print(f"Starting API server on {args.host}:{args.port}")
        print("Endpoints:")
        for endpoint, desc in integration.get_endpoints().items():
            print(f"  {endpoint}: {desc}")
        integration.serve(host=args.host, port=args.port)
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
