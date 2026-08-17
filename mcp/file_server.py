"""
File Operations MCP Server

MCP server wrapping cursor_framework file utilities for Cursor IDE.
Provides tools for file operations, search, and path handling.

Usage:
    python file_server.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from fastmcp import FastMCP
    HAS_FASTMCP = True
except ImportError:
    HAS_FASTMCP = False

if HAS_FASTMCP:
    mcp = FastMCP("file-ops")

# Import utilities from cursor_framework
from cursor_framework.utils.file_utils import (
    ensure_dir,
    get_relative_path,
    find_files,
    copy_file,
    move_file,
    delete_file,
    get_file_size,
    get_extension,
    change_extension,
    read_file_safe,
    write_file_safe,
    list_directory,
)

# ============================================================================
# MCP Tools - Basic File Operations
# ============================================================================

if HAS_FASTMCP:

    @mcp.tool()
    def ensure_directory(path: str) -> dict:
        """
        Ensure a directory exists, create if not.
        
        Args:
            path: Directory path to create
        
        Returns:
            Status and path created
        """
        try:
            p = ensure_dir(path)
            return {"success": True, "path": str(p)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def find_files(directory: str, pattern: str = "*", recursive: bool = True) -> list[str]:
        """
        Find files matching a glob pattern.
        
        Args:
            directory: Directory to search
            pattern: Glob pattern (e.g., "*.py", "**/*.ts")
            recursive: Search subdirectories
        
        Returns:
            List of matching file paths
        """
        paths = find_files(directory, pattern, recursive)
        return [str(p) for p in paths]

    @mcp.tool()
    def copy_file(src: str, dst: str, overwrite: bool = False) -> dict:
        """
        Copy a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            overwrite: Overwrite if destination exists
        
        Returns:
            Success status
        """
        success = copy_file(src, dst, overwrite)
        return {"success": success, "src": src, "dst": dst}

    @mcp.tool()
    def move_file(src: str, dst: str, overwrite: bool = False) -> dict:
        """
        Move a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            overwrite: Overwrite if destination exists
        
        Returns:
            Success status
        """
        success = move_file(src, dst, overwrite)
        return {"success": success, "src": src, "dst": dst}

    @mcp.tool()
    def delete_file(path: str) -> dict:
        """
        Delete a file.
        
        Args:
            path: File path to delete
        
        Returns:
            Success status
        """
        success = delete_file(path)
        return {"success": success, "path": path}

    @mcp.tool()
    def get_file_info(path: str) -> dict:
        """
        Get file metadata (size, extension).
        
        Args:
            path: File path
        
        Returns:
            File metadata
        """
        p = Path(path)
        if not p.exists():
            return {"exists": False, "path": path}
        
        return {
            "exists": True,
            "path": str(p),
            "name": p.name,
            "extension": get_extension(p),
            "size": get_file_size(p),
            "is_file": p.is_file(),
            "is_dir": p.is_dir(),
        }

    @mcp.tool()
    def list_dir(
        path: str,
        files_only: bool = False,
        dirs_only: bool = False
    ) -> list[str]:
        """
        List directory contents.
        
        Args:
            path: Directory path
            files_only: Only return files
            dirs_only: Only return directories
        
        Returns:
            List of items in directory
        """
        items = list_directory(path, files_only, dirs_only)
        return [str(p) for p in items]

    @mcp.tool()
    def read_file(path: str, encoding: str = "utf-8") -> dict:
        """
        Safely read file contents.
        
        Args:
            path: File path
            encoding: File encoding
        
        Returns:
            File contents or error
        """
        content = read_file_safe(path, encoding)
        if content is None:
            return {"success": False, "error": "Could not read file"}
        return {"success": True, "content": content, "path": path}

    @mcp.tool()
    def write_file(
        path: str,
        content: str,
        encoding: str = "utf-8"
    ) -> dict:
        """
        Safely write file contents.
        
        Args:
            path: File path
            content: Content to write
            encoding: File encoding
        
        Returns:
            Success status
        """
        success = write_file_safe(path, content, encoding)
        return {"success": success, "path": path}

    @mcp.tool()
    def change_ext(path: str, new_ext: str) -> str:
        """
        Change file extension.
        
        Args:
            path: File path
            new_ext: New extension (with or without dot)
        
        Returns:
            New file path with changed extension
        """
        new_path = change_extension(path, new_ext)
        return str(new_path)

    @mcp.tool()
    def get_relative(from_path: str, to_path: str) -> str:
        """
        Get relative path from one path to another.
        
        Args:
            from_path: Base path
            to_path: Target path
        
        Returns:
            Relative path
        """
        return get_relative_path(from_path, to_path)

    # ============================================================================
    # MCP Tools - Advanced Operations
    # ============================================================================

    @mcp.tool()
    def batch_copy(items: list[dict]) -> list[dict]:
        """
        Batch copy multiple files.
        
        Args:
            items: List of {"src": str, "dst": str, "overwrite": bool}
        
        Returns:
            Results for each copy operation
        """
        results = []
        for item in items:
            src = item.get("src", "")
            dst = item.get("dst", "")
            overwrite = item.get("overwrite", False)
            success = copy_file(src, dst, overwrite)
            results.append({"src": src, "dst": dst, "success": success})
        return results

    @mcp.tool()
    def batch_delete(paths: list[str]) -> list[dict]:
        """
        Batch delete multiple files.
        
        Args:
            paths: List of file paths to delete
        
        Returns:
            Results for each delete operation
        """
        results = []
        for path in paths:
            success = delete_file(path)
            results.append({"path": path, "success": success})
        return results

    @mcp.tool()
    def search_in_files(
        directory: str,
        pattern: str,
        search_text: str,
        recursive: bool = True
    ) -> list[dict]:
        """
        Search for text within files matching a pattern.
        
        Args:
            directory: Directory to search
            pattern: File glob pattern
            search_text: Text to search for
            recursive: Search subdirectories
        
        Returns:
            List of matches with file path and line number
        """
        import re
        matches = []
        files = find_files(directory, pattern, recursive)
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                for i, line in enumerate(content.splitlines(), 1):
                    if search_text in line or (search_text.startswith("/") and re.search(search_text, line)):
                        matches.append({
                            "file": str(file_path),
                            "line": i,
                            "content": line.strip()
                        })
            except Exception:
                continue
        
        return matches

    @mcp.tool()
    def find_duplicates(directory: str, pattern: str = "*") -> list[list[str]]:
        """
        Find duplicate files by content hash.
        
        Args:
            directory: Directory to search
            pattern: File glob pattern
        
        Returns:
            Lists of duplicate file paths
        """
        import hashlib
        from collections import defaultdict
        
        hash_map: dict[str, list[str]] = defaultdict(list)
        files = find_files(directory, pattern, recursive=True)
        
        for file_path in files:
            if not file_path.is_file():
                continue
            try:
                content = file_path.read_bytes()
                h = hashlib.md5(content).hexdigest()
                hash_map[h].append(str(file_path))
            except Exception:
                continue
        
        # Return only groups with duplicates
        return [paths for paths in hash_map.values() if len(paths) > 1]

    @mcp.tool()
    def count_lines(directory: str, pattern: str = "*") -> dict:
        """
        Count lines of code in matching files.
        
        Args:
            directory: Directory to search
            pattern: File glob pattern
        
        Returns:
            Total lines, file counts by extension
        """
        import re
        files = find_files(directory, pattern, recursive=True)
        
        total_lines = 0
        total_files = 0
        by_extension: dict[str, int] = {}
        
        for file_path in files:
            if not file_path.is_file():
                continue
            try:
                ext = file_path.suffix or "no_ext"
                lines = len(file_path.read_text(encoding="utf-8", errors="replace").splitlines())
                total_lines += lines
                total_files += 1
                by_extension[ext] = by_extension.get(ext, 0) + lines
            except Exception:
                continue
        
        return {
            "total_lines": total_lines,
            "total_files": total_files,
            "by_extension": by_extension
        }

    @mcp.tool()
    def tree(directory: str, max_depth: int = 3) -> dict:
        """
        Generate directory tree structure.
        
        Args:
            directory: Root directory
            max_depth: Maximum depth to traverse
        
        Returns:
            Tree structure as nested dict
        """
        def build_tree(path: Path, depth: int) -> dict:
            if depth > max_depth:
                return {"type": "truncated"}
            
            if path.is_file():
                return {"type": "file", "name": path.name}
            
            children = []
            try:
                for item in sorted(path.iterdir()):
                    children.append(build_tree(item, depth + 1))
            except PermissionError:
                return {"type": "error", "message": "Permission denied"}
            
            return {"type": "dir", "name": path.name, "children": children}
        
        return build_tree(Path(directory), 0)

# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="File Operations MCP Server")
    args = parser.parse_args()
    
    if HAS_FASTMCP:
        mcp.run(transport="stdio")
    else:
        print("ERROR: fastmcp required. Install with: pip install fastmcp", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
