"""
Session Memory Module

Tracks file reads during a Cursor session to avoid redundant re-reads.
Stores session state in `.cache/session_memory.json` with LRU cache support.

Features:
    - Track file reads with token counts
    - Fast lookup API (<10ms target)
    - LRU cache for recent files
    - Token usage summary per file
    - Session context preservation

Usage:
    >>> from cursor_framework.session_memory import SessionMemory
    >>> mem = SessionMemory()
    >>> mem.mark_file_read("path/to/file.cs", tokens=1500)
    True
    >>> mem.was_read("path/to/file.cs")
    True
    >>> mem.get_recent_files(limit=5)
    ['path/to/file.cs', ...]
    >>> mem.get_token_summary()
    {'total_tokens': 5000, 'files_read': 10, 'avg_tokens_per_file': 500}

    # CLI:
    >>> python -m cursor_framework session-stats
    >>> python -m cursor_framework session-clear
"""

from __future__ import annotations

import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


# Default cache settings
DEFAULT_CACHE_SIZE = 1000  # Max files in LRU cache
DEFAULT_TOKEN_LIMIT = 100000  # Warn if total tokens exceed this


@dataclass
class FileRead:
    """Record of a file read operation."""
    path: str
    tokens: int
    timestamp: str
    read_count: int = 1
    context_lines: int = 0
    hash: str = ""  # File content hash for change detection


@dataclass
class ContextChunk:
    """A context chunk sent to LLM."""
    file_path: str
    lines: tuple[int, int]  # (start, end) line numbers
    tokens: int
    timestamp: str
    purpose: str = ""  # e.g., "import_resolution", "code_review"


@dataclass
class SessionStats:
    """Session memory statistics."""
    total_files_read: int = 0
    total_tokens: int = 0
    unique_files: int = 0
    avg_tokens_per_file: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    cache_hit_rate: float = 0.0
    session_duration_seconds: float = 0.0
    reads_per_file: dict[str, int] = field(default_factory=dict)


class SessionMemory:
    """
    Tracks file reads during a Cursor coding session.

    Provides fast lookup to avoid re-reading files already in context.
    Implements LRU cache for efficient memory management.

    Target: <10ms lookup time for was_read() and get_context()
    """

    def __init__(
        self,
        cache_path: str | Path = ".cache/session_memory.json",
        max_cache_size: int = DEFAULT_CACHE_SIZE,
        token_limit: int = DEFAULT_TOKEN_LIMIT,
    ) -> None:
        """
        Initialize session memory.

        Args:
            cache_path: Path to persist session memory JSON
            max_cache_size: Maximum number of files in LRU cache
            token_limit: Warning threshold for total token usage
        """
        self._cache_path = Path(cache_path)
        self._max_cache_size = max_cache_size
        self._token_limit = token_limit

        # LRU cache: OrderedDict for O(1) access and eviction
        self._reads: OrderedDict[str, FileRead] = OrderedDict()

        # Context chunks for LLM context building
        self._contexts: dict[str, list[ContextChunk]] = {}

        # Statistics
        self._total_tokens = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._session_start = time.time()
        self._file_hash: dict[str, str] = {}  # path -> content hash

        # Load persisted state
        self._load()

    def _load(self) -> None:
        """Load session memory from disk."""
        if not self._cache_path.exists():
            return

        try:
            data = json.loads(self._cache_path.read_text(encoding="utf-8"))

            # Restore reads
            reads_data = data.get("reads", {})
            for path, read_data in reads_data.items():
                self._reads[path] = FileRead(
                    path=path,
                    tokens=read_data.get("tokens", 0),
                    timestamp=read_data.get("timestamp", ""),
                    read_count=read_data.get("read_count", 1),
                    context_lines=read_data.get("context_lines", 0),
                    hash=read_data.get("hash", ""),
                )

            # Restore contexts
            contexts_data = data.get("contexts", {})
            for path, chunks in contexts_data.items():
                self._contexts[path] = [
                    ContextChunk(
                        file_path=c.get("file_path", path),
                        lines=tuple(c.get("lines", [0, 0])),
                        tokens=c.get("tokens", 0),
                        timestamp=c.get("timestamp", ""),
                        purpose=c.get("purpose", ""),
                    )
                    for c in chunks
                ]

            # Restore stats
            self._total_tokens = data.get("total_tokens", 0)
            self._cache_hits = data.get("cache_hits", 0)
            self._cache_misses = data.get("cache_misses", 0)
            session_start = data.get("session_start", None)
            if session_start:
                self._session_start = datetime.fromisoformat(session_start).timestamp()

            self._file_hash = data.get("file_hashes", {})

            logger.debug(
                "Loaded session memory: %d files, %d tokens",
                len(self._reads),
                self._total_tokens,
            )
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Failed to load session memory: %s", e)

    def _save(self) -> None:
        """Persist session memory to disk."""
        try:
            self._cache_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert reads to serializable dict
            reads_dict = {}
            for path, read in self._reads.items():
                reads_dict[path] = {
                    "path": read.path,
                    "tokens": read.tokens,
                    "timestamp": read.timestamp,
                    "read_count": read.read_count,
                    "context_lines": read.context_lines,
                    "hash": read.hash,
                }

            # Convert contexts to serializable dict
            contexts_dict = {}
            for path, chunks in self._contexts.items():
                contexts_dict[path] = [
                    {
                        "file_path": c.file_path,
                        "lines": list(c.lines),
                        "tokens": c.tokens,
                        "timestamp": c.timestamp,
                        "purpose": c.purpose,
                    }
                    for c in chunks
                ]

            data = {
                "reads": reads_dict,
                "contexts": contexts_dict,
                "total_tokens": self._total_tokens,
                "cache_hits": self._cache_hits,
                "cache_misses": self._cache_misses,
                "session_start": datetime.fromtimestamp(self._session_start).isoformat(),
                "file_hashes": self._file_hash,
                "saved_at": datetime.now().isoformat(timespec="seconds"),
            }

            self._cache_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            logger.debug("Saved session memory to %s", self._cache_path)
        except OSError as e:
            logger.warning("Failed to save session memory: %s", e)

    def mark_file_read(
        self,
        file_path: str,
        tokens: int,
        context_lines: int = 0,
        content_hash: str = "",
        save: bool = True,
    ) -> bool:
        """
        Mark a file as read.

        Args:
            file_path: Path to the file that was read
            tokens: Number of tokens in the file
            context_lines: Number of lines read from the file
            content_hash: Content hash for change detection
            save: Whether to persist immediately

        Returns:
            True if this is a new read, False if already cached
        """
        path_key = str(Path(file_path).resolve())

        # Check if already in cache (LRU update)
        if path_key in self._reads:
            read = self._reads[path_key]
            read.read_count += 1
            read.timestamp = datetime.now().isoformat(timespec="seconds")
            # Move to end (most recent)
            self._reads.move_to_end(path_key)
            self._cache_hits += 1
            return False

        # New file read
        self._reads[path_key] = FileRead(
            path=path_key,
            tokens=tokens,
            timestamp=datetime.now().isoformat(timespec="seconds"),
            read_count=1,
            context_lines=context_lines,
            hash=content_hash,
        )

        # Update total tokens
        self._total_tokens += tokens

        # Store content hash for change detection
        if content_hash:
            self._file_hash[path_key] = content_hash

        # LRU eviction
        while len(self._reads) > self._max_cache_size:
            evicted_key, evicted_read = self._reads.popitem(last=False)
            self._total_tokens -= evicted_read.tokens
            logger.debug("Evicted %s from session memory (LRU)", evicted_key)

        if save:
            self._save()

        return True

    def was_read(self, file_path: str) -> bool:
        """
        Check if a file was already read in this session.

        Args:
            file_path: Path to check

        Returns:
            True if file was read, False otherwise
        """
        path_key = str(Path(file_path).resolve())

        if path_key in self._reads:
            # Move to end (mark as recently accessed)
            self._reads.move_to_end(path_key)
            self._cache_hits += 1
            return True

        self._cache_misses += 1
        return False

    def get_read(self, file_path: str) -> Optional[FileRead]:
        """
        Get the FileRead record for a file.

        Args:
            file_path: Path to the file

        Returns:
            FileRead record or None if not found
        """
        path_key = str(Path(file_path).resolve())
        read = self._reads.get(path_key)

        if read:
            self._reads.move_to_end(path_key)
            self._cache_hits += 1
        else:
            self._cache_misses += 1

        return read

    def get_context(self, file_path: str) -> Optional[dict[str, Any]]:
        """
        Get cached context for a file.

        Args:
            file_path: Path to the file

        Returns:
            Dict with context info or None
        """
        path_key = str(Path(file_path).resolve())
        read = self._reads.get(path_key)

        if not read:
            self._cache_misses += 1
            return None

        contexts = self._contexts.get(path_key, [])

        self._reads.move_to_end(path_key)
        self._cache_hits += 1

        return {
            "path": read.path,
            "tokens": read.tokens,
            "read_count": read.read_count,
            "last_read": read.timestamp,
            "contexts": [asdict(c) for c in contexts],
            "hash": read.hash,
        }

    def add_context_chunk(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        tokens: int,
        purpose: str = "",
    ) -> None:
        """
        Add a context chunk for a file.

        Args:
            file_path: Path to the file
            start_line: Start line number
            end_line: End line number
            tokens: Token count for this chunk
            purpose: Why this chunk was used
        """
        path_key = str(Path(file_path).resolve())

        if path_key not in self._contexts:
            self._contexts[path_key] = []

        self._contexts[path_key].append(ContextChunk(
            file_path=path_key,
            lines=(start_line, end_line),
            tokens=tokens,
            timestamp=datetime.now().isoformat(timespec="seconds"),
            purpose=purpose,
        ))

    def get_recent_files(self, limit: int = 10) -> list[str]:
        """
        Get recently read files.

        Args:
            limit: Maximum number of files to return

        Returns:
            List of file paths (most recent first)
        """
        # Return keys from OrderedDict (most recent = end)
        return list(reversed(list(self._reads.keys())))[:limit]

    def get_token_summary(self) -> dict[str, Any]:
        """
        Get token usage summary.

        Returns:
            Dict with token statistics
        """
        total_files = len(self._reads)
        avg_tokens = (
            self._total_tokens / total_files if total_files > 0 else 0
        )

        cache_total = self._cache_hits + self._cache_misses
        cache_hit_rate = (
            self._cache_hits / cache_total if cache_total > 0 else 0.0
        )

        return {
            "total_tokens": self._total_tokens,
            "files_read": total_files,
            "unique_files": total_files,
            "avg_tokens_per_file": round(avg_tokens, 1),
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "cache_hit_rate": round(cache_hit_rate * 100, 1),
            "token_limit": self._token_limit,
            "token_limit_exceeded": self._total_tokens > self._token_limit,
            "session_duration_seconds": round(time.time() - self._session_start, 1),
        }

    def get_stats(self) -> SessionStats:
        """
        Get full session statistics.

        Returns:
            SessionStats dataclass
        """
        summary = self.get_token_summary()

        return SessionStats(
            total_files_read=sum(r.read_count for r in self._reads.values()),
            total_tokens=self._total_tokens,
            unique_files=summary["files_read"],
            avg_tokens_per_file=summary["avg_tokens_per_file"],
            cache_hits=self._cache_hits,
            cache_misses=self._cache_misses,
            cache_hit_rate=summary["cache_hit_rate"],
            session_duration_seconds=summary["session_duration_seconds"],
            reads_per_file={p: r.read_count for p, r in self._reads.items()},
        )

    def check_file_changed(self, file_path: str, current_hash: str) -> bool:
        """
        Check if a file has changed since last read.

        Args:
            file_path: Path to the file
            current_hash: Current content hash

        Returns:
            True if file changed, False if unchanged
        """
        path_key = str(Path(file_path).resolve())
        stored_hash = self._file_hash.get(path_key, "")

        if not stored_hash:
            return True  # Never read

        return stored_hash != current_hash

    def clear_session(self, save: bool = True) -> dict[str, Any]:
        """
        Clear all session memory.

        Args:
            save: Whether to persist empty state

        Returns:
            Dict with cleared statistics
        """
        stats = self.get_token_summary()

        self._reads.clear()
        self._contexts.clear()
        self._total_tokens = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._session_start = time.time()
        self._file_hash.clear()

        if save:
            self._save()

        logger.info("Session memory cleared")

        return {
            "cleared": True,
            "files_cleared": stats["files_read"],
            "tokens_cleared": stats["total_tokens"],
        }

    def remove_file(self, file_path: str, save: bool = True) -> bool:
        """
        Remove a specific file from session memory.

        Args:
            file_path: Path to remove
            save: Whether to persist

        Returns:
            True if file was removed, False if not found
        """
        path_key = str(Path(file_path).resolve())

        if path_key in self._reads:
            read = self._reads.pop(path_key)
            self._total_tokens -= read.tokens
            self._contexts.pop(path_key, None)
            self._file_hash.pop(path_key, None)

            if save:
                self._save()

            return True

        return False

    def export_context(self) -> dict[str, Any]:
        """
        Export current session context for Cursor.

        Returns:
            Dict suitable for `.cursor/context.json`
        """
        recent_files = self.get_recent_files(limit=50)

        return {
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "session_duration_seconds": round(time.time() - self._session_start, 1),
            "total_tokens": self._total_tokens,
            "files_read": len(self._reads),
            "recent_files": recent_files,
            "reads": {
                path: {
                    "tokens": read.tokens,
                    "read_count": read.read_count,
                    "last_read": read.timestamp,
                }
                for path, read in self._reads.items()
            },
            "token_summary": self.get_token_summary(),
        }

    def __len__(self) -> int:
        """Return number of files in cache."""
        return len(self._reads)

    def __contains__(self, file_path: str) -> bool:
        """Check if file is in cache."""
        return str(Path(file_path).resolve()) in self._reads


def create_session_memory(
    cache_path: str | Path = ".cache/session_memory.json",
) -> SessionMemory:
    """
    Factory function to create SessionMemory.

    Args:
        cache_path: Path to persistence file

    Returns:
        Configured SessionMemory instance
    """
    return SessionMemory(cache_path=cache_path)


def main() -> int:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Session Memory CLI")
    parser.add_argument("--cache-path", default=".cache/session_memory.json",
                        help="Path to session memory file")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # stats command
    sub.add_parser("stats", help="Show session memory statistics")

    # clear command
    clear = sub.add_parser("clear", help="Clear session memory")
    clear.add_argument("--force", action="store_true", help="Skip confirmation")

    # export command
    sub.add_parser("export", help="Export session context")

    args = parser.parse_args()

    mem = SessionMemory(cache_path=args.cache_path)

    if args.cmd == "stats":
        stats = mem.get_stats()
        print(json.dumps(asdict(stats), indent=2, ensure_ascii=False))
        return 0

    elif args.cmd == "clear":
        if args.force:
            result = mem.clear_session()
            print(json.dumps(result, indent=2))
        else:
            print("Use --force to confirm clearing session memory")
            return 1
        return 0

    elif args.cmd == "export":
        context = mem.export_context()
        print(json.dumps(context, indent=2, ensure_ascii=False))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
