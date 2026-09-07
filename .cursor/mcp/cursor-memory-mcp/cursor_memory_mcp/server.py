"""FastMCP server for context and hierarchical memory management."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit("FastMCP is not installed. Install requirements.txt") from exc


def _bootstrap_framework_import() -> None:
    configured = os.environ.get("CURSOR_WORKSPACE_ROOT")
    candidates = []
    if configured:
        candidates.append(Path(configured).resolve() / "tools" / "cursor-framework-mcp")
    candidates.extend(
        [
            Path.cwd().resolve() / "tools" / "cursor-framework-mcp",
            Path(__file__).resolve().parents[2] / "cursor-framework-mcp",
        ]
    )
    for candidate in candidates:
        if candidate.is_dir() and str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
            return


_bootstrap_framework_import()

from cursor_framework_mcp.loader import make_default_loader  # noqa: E402
from cursor_framework_mcp.registry import find_workspace_root  # noqa: E402

from .compressor import ContextCompressor  # noqa: E402
from .context import ContextManager  # noqa: E402
from .history import ConversationHistory  # noqa: E402
from .memory import MemoryStore  # noqa: E402


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)


def _root() -> str:
    configured = os.environ.get("CURSOR_WORKSPACE_ROOT")
    if configured and Path(configured).is_dir():
        return str(Path(configured).resolve())
    return find_workspace_root(os.getcwd())


def create_server(workspace_root: str | None = None, token_budget: int = 24_000) -> FastMCP:
    root = workspace_root or _root()
    loader = make_default_loader(root)
    compressor = ContextCompressor()
    memory = MemoryStore(root, loader, token_budget=token_budget)
    history = ConversationHistory(compressor)
    context = ContextManager(loader, memory, history, compressor)
    memory.load_from_disk()

    mcp = FastMCP("cursor-memory-mcp", instructions=f"Token-aware hierarchical memory for Cursor Enterprise Framework. Workspace root: {root}")

    @mcp.tool()
    def store_memory(content: str, tier: str = "short", kind: str = "fact", project: str = "default", session: str = "default", tags: list[str] | None = None) -> str:
        """Store a fact or conclusion in short-, medium-, or long-term memory."""
        try:
            item = memory.store(content, tier, kind, project, session, tags)  # type: ignore[arg-type]
        except ValueError as exc:
            return _json({"error": "invalid_memory", "message": str(exc)})
        return _json(item.__dict__)

    @mcp.tool()
    def recall_memory(task: str, limit: int = 10, project: str | None = None, session: str | None = None) -> str:
        """Recall memories ranked by task relevance, recency, tier, and access frequency."""
        return _json({"task": task, "memories": memory.recall(task, limit, project, session)})

    @mcp.tool()
    def compact_context(context_text: str, target_tokens: int, focus: str = "") -> str:
        """Compress context deterministically to a target token budget."""
        try:
            return _json(context.compact(context_text, target_tokens, focus))
        except ValueError as exc:
            return _json({"error": "invalid_budget", "message": str(exc)})

    @mcp.tool()
    def summarize_history(history_json: str, keep_recent: int = 8, target_tokens: int = 800) -> str:
        """Summarize old conversation messages while retaining recent messages verbatim."""
        try:
            messages = json.loads(history_json)
            if not isinstance(messages, list):
                raise ValueError("history_json must encode a list")
            local = ConversationHistory(compressor)
            for message in messages:
                local.add(str(message.get("role", "user")), str(message.get("content", "")))
            return _json(local.summarize(keep_recent, target_tokens))
        except (json.JSONDecodeError, ValueError, AttributeError) as exc:
            return _json({"error": "invalid_history", "message": str(exc)})

    @mcp.tool()
    def get_context_stats(current_context: str = "") -> str:
        """Get token usage for current text, framework cache, memory tiers, and history."""
        return _json(context.stats(current_context))

    @mcp.tool()
    def prune_context(current_task: str = "", target_tokens: int = 12_000) -> str:
        """Remove least-relevant memories until the requested memory budget is met."""
        try:
            return _json(context.prune(current_task, target_tokens))
        except ValueError as exc:
            return _json({"error": "invalid_budget", "message": str(exc)})

    @mcp.tool()
    def export_memory(output_path: str | None = None) -> str:
        """Export all memory as JSON, optionally writing it below the workspace root."""
        payload = memory.export_data()
        if output_path:
            target = (Path(root) / output_path).resolve()
            try:
                target.relative_to(Path(root).resolve())
            except ValueError:
                return _json({"error": "path_outside_workspace"})
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            return _json({"path": str(target), "items": len(payload["memories"])})
        return _json(payload)

    @mcp.tool()
    def import_memory(memory_json: str, merge: bool = True) -> str:
        """Import hierarchical memories from a JSON export."""
        try:
            return _json(memory.import_data(json.loads(memory_json), merge))
        except (json.JSONDecodeError, ValueError) as exc:
            return _json({"error": "invalid_import", "message": str(exc)})

    @mcp.tool()
    def sync_to_disk(compact_long_term: bool = True) -> str:
        """Optionally compress long-term memories and atomically persist them to disk."""
        compaction = memory.compact_long_term() if compact_long_term else None
        return _json({"sync": memory.sync_to_disk(), "compaction": compaction})

    return mcp


def run() -> None:
    create_server().run()


if __name__ == "__main__":
    run()
