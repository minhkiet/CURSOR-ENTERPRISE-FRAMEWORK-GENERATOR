"""
Cursor Framework MCP Server

High-level MCP server wrapping cursor_framework utilities for Cursor IDE.
Provides tools for context management, skill discovery, memory operations, and workflow.

Usage:
    python mcp/framework_server.py
    
Or configure in Cursor MCP settings:
    - Add config from mcp/mcp_config.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

# Use fastmcp if available, fallback to minimal implementation
try:
    from fastmcp import FastMCP
    HAS_FASTMCP = True
except ImportError:
    HAS_FASTMCP = False
    print("fastmcp not installed. Run: pip install fastmcp", file=sys.stderr)

# Initialize FastMCP server
if HAS_FASTMCP:
    mcp = FastMCP("cursor-framework")

# ============================================================================
# Framework Core Imports (lazy-loaded)
# ============================================================================

def _get_workflow(root: str, memory_path: str):
    """Lazy load workflow to avoid import overhead."""
    from cursor_framework.workflow import Workflow
    return Workflow(root=root, memory_path=memory_path)

def _get_indexer(root: str):
    """Lazy load indexer."""
    from cursor_framework.indexer import Indexer
    return Indexer(root)

def _get_skill_discovery(root: str):
    """Lazy load skill discovery."""
    from cursor_framework.skill_discovery import SkillDiscovery
    return SkillDiscovery(root=root)

def _get_code_graph(root: str):
    """Lazy load code graph."""
    from cursor_framework.code_graph import CodeGraph
    return CodeGraph(root=root)

def _get_cursor_integration(root: str, memory_path: str):
    """Lazy load cursor integration."""
    from cursor_framework.cursor_integration import CursorIntegration
    return CursorIntegration(root=root, cache_path=memory_path)

# ============================================================================
# MCP Tools - Context & Memory
# ============================================================================

if HAS_FASTMCP:

    @mcp.tool()
    def ask_framework(request: str, root: str = ".cursor", memory_path: str = ".cache/memory.json") -> dict:
        """
        Process a request through the framework workflow.
        
        Args:
            request: Natural language request to route through the framework
            root: Path to .cursor directory
            memory_path: Path to memory cache file
        
        Returns:
            Dict with context, cache status, memory stats, and latency
        """
        wf = _get_workflow(root, memory_path)
        result = wf.ask(request)
        return {
            "context": result.context.text,
            "context_tokens": result.context.tokens,
            "skills_used": result.context.skills_used,
            "from_cache": result.from_cache,
            "memory_hits": result.memory_hits,
            "memory_misses": result.memory_misses,
            "latency_ms": round(result.latency_ms, 2),
            "phase_ms": {k: round(v, 2) for k, v in result.phase_ms.items()} if result.phase_ms else {}
        }

    @mcp.tool()
    def warm_cache(root: str = ".cursor", memory_path: str = ".cache/memory.json") -> dict:
        """
        Warm up the framework cache (scan + persist).
        
        Args:
            root: Path to .cursor directory
            memory_path: Path to memory cache file
        
        Returns:
            Stats about indexed assets and memory entries
        """
        wf = _get_workflow(root, memory_path)
        stats = wf.warm()
        return stats

    @mcp.tool()
    def get_stats(root: str = ".cursor", memory_path: str = ".cache/memory.json") -> dict:
        """
        Get framework statistics.
        
        Args:
            root: Path to .cursor directory
            memory_path: Path to memory cache file
        
        Returns:
            Memory hits, misses, tokens saved, assets indexed
        """
        wf = _get_workflow(root, memory_path)
        return wf.stats()

    @mcp.tool()
    def clear_cache(force: bool = False, root: str = ".cursor", memory_path: str = ".cache/memory.json") -> dict:
        """
        Clear the framework cache.
        
        Args:
            force: Actually delete (False = dry run)
            root: Path to .cursor directory
            memory_path: Path to memory cache file
        
        Returns:
            List of files that would/were deleted
        """
        from cursor_framework.memory_store import MemoryStore
        from pathlib import Path
        
        root_path = Path(root).resolve()
        memory_file = Path(memory_path)
        if not memory_file.is_absolute():
            memory_file = (Path.cwd() / memory_file).resolve()
        
        candidates = [memory_file]
        for name in ("INDEX.json", "INDEX.md"):
            p = root_path / name
            if p not in candidates:
                candidates.append(p)
        
        existing = [p for p in candidates if p.exists()]
        
        if not force:
            return {
                "dry_run": True,
                "would_delete": [str(p) for p in existing],
                "missing": [str(p) for p in candidates if p not in existing]
            }
        
        deleted = []
        for p in existing:
            try:
                p.unlink()
                deleted.append(str(p))
            except OSError as e:
                return {"error": str(e), "deleted": deleted}
        
        return {"dry_run": False, "deleted": deleted}

    # ============================================================================
    # MCP Tools - Skills & Indexing
    # ============================================================================

    @mcp.tool()
    def scan_framework(root: str = ".cursor") -> dict:
        """
        Scan .cursor directory and return asset counts.
        
        Args:
            root: Path to .cursor directory
        
        Returns:
            Totals for skills, rules, agents, etc.
        """
        idx = _get_indexer(root)
        idx.scan()
        return {"totals": idx.result.totals} if idx.result else {}

    @mcp.tool()
    def discover_skills(request: str, root: str = ".cursor") -> list[dict]:
        """
        Discover relevant skills for a request.
        
        Args:
            request: Natural language request
            root: Path to .cursor directory
        
        Returns:
            List of matched skills with scores
        """
        discovery = _get_skill_discovery(root)
        matches = discovery.find_skills(request)
        return [
            {
                "name": m.name,
                "path": m.path,
                "score": m.score,
                "tags": m.tags
            }
            for m in matches
        ]

    @mcp.tool()
    def get_skill_graph(root: str = ".cursor") -> dict:
        """
        Get skill dependency graph.
        
        Args:
            root: Path to .cursor directory
        
        Returns:
            Nodes and edges for skill dependencies
        """
        from cursor_framework.skill_discovery import SkillRegistry
        
        registry = SkillRegistry()
        skills = registry.get_all()
        
        nodes = []
        for s in skills:
            is_agent = "agents/" in s.path
            nodes.append({
                "id": s.name,
                "kind": "agent" if is_agent else "skill",
                "version": s.version,
                "tags": s.tags[:5],
                "path": s.path
            })
        
        edges = []
        for s in skills:
            for dep in s.dependencies:
                if dep in registry._skills:
                    edges.append({"source": s.name, "target": dep, "kind": "dependency"})
        
        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges
        }

    # ============================================================================
    # MCP Tools - Code Graph
    # ============================================================================

    @mcp.tool()
    def scan_code_graph(root: str = ".") -> dict:
        """
        Scan project code and build dependency graph.
        
        Args:
            root: Project root directory
        
        Returns:
            Module count, dependencies, languages
        """
        graph = _get_code_graph(root)
        result = graph.scan()
        return result.to_dict() if hasattr(result, 'to_dict') else {
            "module_count": result.module_count if hasattr(result, 'module_count') else 0,
            "dependency_count": result.dependency_count if hasattr(result, 'dependency_count') else 0,
            "languages": result.languages if hasattr(result, 'languages') else {}
        }

    @mcp.tool()
    def find_related_files(file: str, root: str = ".") -> list[str]:
        """
        Find files related to a given file via dependency graph.
        
        Args:
            file: File path or module name
            root: Project root directory
        
        Returns:
            List of related file paths
        """
        graph = _get_code_graph(root)
        if graph.result is None:
            graph.scan()
        
        module_name = Path(file).stem
        module = graph.find_module(module_name)
        if not module:
            return []
        
        deps = graph.find_dependents(module.path)
        return [d.path for d in deps[:10]]

    # ============================================================================
    # MCP Tools - Session Memory
    # ============================================================================

    @mcp.tool()
    def mark_file_read(
        file_path: str,
        tokens: int = 0,
        context_lines: int = 0,
        root: str = ".",
        memory_path: str = ".cache/session_memory.json"
    ) -> dict:
        """
        Mark a file as read for session tracking.
        
        Args:
            file_path: Path to the file
            tokens: Token count used
            context_lines: Lines of context read
            root: Project root
            memory_path: Session memory cache path
        
        Returns:
            Whether this was a new read
        """
        integration = _get_cursor_integration(root, memory_path)
        is_new = integration.mark_file_read(file_path, tokens, context_lines)
        return {"new_read": is_new, "file": file_path}

    @mcp.tool()
    def check_file_fresh(
        file_path: str,
        root: str = ".",
        memory_path: str = ".cache/session_memory.json"
    ) -> dict:
        """
        Check if a cached file has changed.
        
        Args:
            file_path: Path to check
            root: Project root
            memory_path: Session memory cache path
        
        Returns:
            Whether file is fresh (unchanged)
        """
        integration = _get_cursor_integration(root, memory_path)
        is_fresh = integration.check_file_freshness(file_path)
        return {"fresh": is_fresh, "file": file_path}

    @mcp.tool()
    def get_session_stats(root: str = ".", memory_path: str = ".cache/session_memory.json") -> dict:
        """
        Get session memory statistics.
        
        Args:
            root: Project root
            memory_path: Session memory cache path
        
        Returns:
            Files read, tokens used, cache hit rate
        """
        integration = _get_cursor_integration(root, memory_path)
        stats = integration.session_memory.get_stats()
        return stats

    # ============================================================================
    # MCP Tools - Context Generation
    # ============================================================================

    @mcp.tool()
    def build_context(
        file_path: str,
        max_tokens: int = 4000,
        root: str = ".",
        memory_path: str = ".cache/session_memory.json"
    ) -> str:
        """
        Build context prompt for a specific file.
        
        Args:
            file_path: Current file being edited
            max_tokens: Max tokens for context
            root: Project root
            memory_path: Session memory cache path
        
        Returns:
            Context string with session info and related files
        """
        integration = _get_cursor_integration(root, memory_path)
        return integration.build_context_prompt(file_path, max_tokens)

    @mcp.tool()
    def dump_context(
        output_path: str = ".cursor/context.json",
        root: str = ".",
        memory_path: str = ".cache/session_memory.json"
    ) -> str:
        """
        Dump current session context to file.
        
        Args:
            output_path: Output file path
            root: Project root
            memory_path: Session memory cache path
        
        Returns:
            Path to dumped file
        """
        integration = _get_cursor_integration(root, memory_path)
        path = integration.dump_context(output_path)
        return str(path)

    # ============================================================================
    # MCP Resources
    # ============================================================================

    @mcp.resource("framework://stats")
    def stats_resource() -> str:
        """Framework statistics as a resource."""
        from cursor_framework.workflow import Workflow
        wf = Workflow()
        return json.dumps(wf.stats(), indent=2)

    @mcp.resource("framework://skills")
    def skills_resource() -> str:
        """List all available skills."""
        from cursor_framework.skill_discovery import SkillRegistry
        registry = SkillRegistry()
        skills = registry.get_all()
        return json.dumps([{"name": s.name, "path": s.path} for s in skills], indent=2)

# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Cursor Framework MCP Server")
    parser.add_argument("--root", default=".cursor", help="Path to .cursor directory")
    parser.add_argument("--memory-path", default=".cache/memory.json", help="Memory cache path")
    parser.add_argument("--port", type=int, default=8765, help="Port for stdio mode")
    
    args = parser.parse_args()
    
    if HAS_FASTMCP:
        mcp.run(transport="stdio")
    else:
        print("ERROR: fastmcp required. Install with: pip install fastmcp", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
