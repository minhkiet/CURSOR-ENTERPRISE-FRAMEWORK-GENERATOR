"""
Code Graph RAG Integration

Optional integration with vitali87/code-graph-rag for advanced code analysis.

This module provides a lazy import wrapper - code-graph-rag is only imported
when explicitly requested, avoiding unnecessary dependencies.

Usage:
    from cursor_framework.integrations.code_graph_rag import CodeGraphRAG

    rag = CodeGraphRAG(project_root=".")
    rag.index()
    results = await rag.query("How is authentication handled?")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

_lazy_import_error: str | None = None

try:
    from codebase_rag.cli import app as _cli_app
    from codebase_rag.mcp.server import serve_stdio as _serve_stdio
    from codebase_rag.main import CodebaseRAG as _CodebaseRAG
    from codebase_rag.config import settings as _settings

    _code_graph_rag_available = True
except ImportError as e:
    _lazy_import_error = str(e)
    _code_graph_rag_available = False
    _cli_app = None
    _serve_stdio = None
    _CodebaseRAG = None
    _settings = None

__all__ = [
    "CodeGraphRAG",
    "is_available",
    "get_installation_help",
]


def is_available() -> bool:
    """Check if code-graph-rag is installed."""
    return _code_graph_rag_available


def get_installation_help() -> str:
    """Return installation instructions if code-graph-rag is not installed."""
    return """
code-graph-rag is not installed. Install with:

    uv tool install "code-graph-rag[treesitter-full,semantic]"

Or with pipx:

    pipx install "code-graph-rag[treesitter-full,semantic]"

After installation, start the services:

    cgr daemon up
"""


class CodeGraphRAG:
    """
    Wrapper for code-graph-rag providing a consistent interface.

    This class provides a high-level API for interacting with code-graph-rag
    while gracefully handling the case where it's not installed.

    Args:
        project_root: Path to the project to analyze
        update_graph: Whether to update the graph on init

    Example:
        >>> from cursor_framework.integrations.code_graph_rag import CodeGraphRAG
        >>> rag = CodeGraphRAG("/path/to/project")
        >>> await rag.index()
        >>> results = await rag.query("How is auth implemented?")
    """

    def __init__(
        self,
        project_root: str | None = None,
        update_graph: bool = False,
    ) -> None:
        if not _code_graph_rag_available:
            raise ImportError(
                f"code-graph-rag is not installed. {get_installation_help()}"
            )

        from pathlib import Path

        self._root = Path(project_root) if project_root else Path.cwd()
        self._update_graph = update_graph
        self._instance: _CodebaseRAG | None = None

    @property
    def project_root(self) -> str:
        """Get the project root path."""
        return str(self._root)

    async def index(self) -> dict:
        """
        Index the repository into the knowledge graph.

        Returns:
            Dictionary with indexing results
        """
        if not _code_graph_rag_available:
            raise ImportError(get_installation_help())

        # Lazy import to avoid loading heavy dependencies
        from codebase_rag.graph_updater import GraphUpdater

        updater = GraphUpdater(
            project_root=str(self._root),
            update_graph=self._update_graph,
        )
        return await updater.update_graph()

    async def query(self, question: str) -> str:
        """
        Query the code graph with a natural language question.

        Args:
            question: Natural language question about the codebase

        Returns:
            Answer with code references
        """
        if not _code_graph_rag_available:
            raise ImportError(get_installation_help())

        if self._instance is None:
            self._instance = _CodebaseRAG(
                project_root=str(self._root),
            )

        return await self._instance.query(question)

    def get_graph_stats(self) -> dict:
        """
        Get statistics about the indexed graph.

        Returns:
            Dictionary with node counts, relationships, etc.
        """
        if not _code_graph_rag_available:
            raise ImportError(get_installation_help())

        from codebase_rag.graph_loader import GraphLoader
        from codebase_rag.utils.path_utils import derive_project_name

        project_name = derive_project_name(self._root)
        loader = GraphLoader()

        stats = loader.get_project_stats(project_name)
        return stats if stats else {}


class CodeGraphRAGCommand:
    """
    CLI command wrapper for code-graph-rag.

    This class provides a programmatic interface to code-graph-rag CLI commands.

    Example:
        >>> from cursor_framework.integrations.code_graph_rag import CodeGraphRAGCommand
        >>> cmd = CodeGraphRAGCommand()
        >>> cmd.daemon_up()
        >>> cmd.start("/path/to/repo", update_graph=True)
    """

    @staticmethod
    def daemon_up() -> None:
        """Start the Memgraph + Qdrant daemon."""
        if not _code_graph_rag_available:
            raise ImportError(get_installation_help())

        import subprocess
        subprocess.run(["cgr", "daemon", "up"], check=True)

    @staticmethod
    def daemon_down() -> None:
        """Stop the Memgraph + Qdrant daemon."""
        if not _code_graph_rag_available:
            raise ImportError(get_installation_help())

        import subprocess
        subprocess.run(["cgr", "daemon", "down"], check=True)

    @staticmethod
    def start(repo_path: str, update_graph: bool = False) -> None:
        """
        Start code-graph-rag for a repository.

        Args:
            repo_path: Path to the repository
            update_graph: Whether to update the graph
        """
        if not _code_graph_rag_available:
            raise ImportError(get_installation_help())

        import subprocess

        args = ["cgr", "start", "--repo-path", repo_path]
        if update_graph:
            args.append("--update-graph")

        subprocess.run(args, check=True)


if TYPE_CHECKING:
    pass
