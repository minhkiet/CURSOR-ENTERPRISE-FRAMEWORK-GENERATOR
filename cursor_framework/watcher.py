"""
File Watcher Module

Polls `.cursor/` for changes (mtime-based) and triggers a callback when
files are added, modified, or deleted. Uses stdlib only — no watchdog dep.

Why polling instead of inotify/FSEvents:
    - Stdlib-only keeps `pyproject.toml` dependencies untouched
    - Polling handles network drives and OneDrive sync folders where
      native events are unreliable
    - 1s poll interval is fine for our asset count (~572 files)

Usage:
    >>> from cursor_framework import Watcher, Indexer
    >>> idx = Indexer(".cursor")
    >>> idx.scan()
    >>> def on_change(changed_paths):
    ...     idx.scan()
    ...     idx.write_json()
    >>> w = Watcher(".cursor", on_change=on_change, interval=2.0)
    >>> w.start()  # non-blocking
    >>> # ... later:
    >>> w.stop()
"""

from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Callable, Iterable


class Watcher:
    """Poll-based filesystem watcher."""

    def __init__(
        self,
        root: str | Path,
        on_change: Callable[[list[Path]], None],
        interval: float = 2.0,
        ignore_globs: Iterable[str] = (".cache", "node_modules"),
    ) -> None:
        self.root = Path(root).resolve()
        self.on_change = on_change
        self.interval = interval
        self.ignore_substrings = tuple(ignore_globs)
        self._snapshot: dict[str, float] = {}
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._changes_detected = 0
        self._scans_run = 0

    def _walk(self) -> dict[str, float]:
        """Return {relative_path: mtime} for every file under root."""
        out: dict[str, float] = {}
        try:
            for p in self.root.rglob("*"):
                if not p.is_file():
                    continue
                rel = str(p.relative_to(self.root))
                if any(s in rel for s in self.ignore_substrings):
                    continue
                try:
                    out[rel] = p.stat().st_mtime
                except OSError:
                    continue
        except OSError:
            return out
        return out

    def _diff(
        self, old: dict[str, float], new: dict[str, float]
    ) -> list[Path]:
        """Compare two snapshots, return absolute paths that changed."""
        changed: list[Path] = []
        for path, mtime in new.items():
            if old.get(path) != mtime:
                changed.append(self.root / path)
        for path in old:
            if path not in new:
                changed.append(self.root / path)
        return changed

    def take_snapshot(self) -> None:
        """Initialize the baseline snapshot. Call once before start()."""
        self._snapshot = self._walk()

    def scan_once(self) -> list[Path] | None:
        """
        Single poll cycle. Returns list of changed paths and fires
        on_change if any. Returns None if no changes.
        """
        self._scans_run += 1
        new = self._walk()
        changed = self._diff(self._snapshot, new)
        if changed:
            self._snapshot = new
            self._changes_detected += len(changed)
            try:
                self.on_change(changed)
            except Exception:
                # ponytail: never let a callback crash the watcher loop.
                pass
            return changed
        return None

    def start(self) -> None:
        """Start background polling. Non-blocking."""
        if self._thread and self._thread.is_alive():
            return
        if not self._snapshot:
            self.take_snapshot()
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop, name="cursor-watcher", daemon=True
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        """Signal the loop to exit and wait briefly."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def _loop(self) -> None:
        while not self._stop_event.is_set():
            self.scan_once()
            # ponytail: sleep in small slices so stop() responds fast.
            self._stop_event.wait(self.interval)

    @property
    def stats(self) -> dict[str, int]:
        """Watcher telemetry for the dashboard."""
        return {
            "scans_run": self._scans_run,
            "changes_detected": self._changes_detected,
            "tracked_files": len(self._snapshot),
        }