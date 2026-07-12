"""
Dashboard Module

Tiny stdlib HTTP server exposing the framework's INDEX.json and runtime
stats as JSON, plus a single-page HTML dashboard.

Endpoints:
    GET /              → static HTML (cursor_framework/dashboard/index.html)
    GET /api/index     → INDEX.json contents (asset counts, categories)
    GET /api/stats     → live runtime stats (memory hits, watcher scans, etc.)
    GET /api/memory    → MemoryManager entries (sample, capped)

Usage:
    >>> from cursor_framework import Dashboard
    >>> d = Dashboard(root=".cursor", memory_path=".cache/memory.json")
    >>> d.serve(port=8765)  # blocking

For non-blocking use in an existing thread:
    >>> import threading
    >>> threading.Thread(target=d.serve, kwargs={"port": 8765}, daemon=True).start()
"""

from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse, parse_qs

from .indexer import Indexer
from .memory_manager import MemoryManager
from .memory_store import MemoryStore

if TYPE_CHECKING:
    from .workflow import Workflow


class Dashboard:
    """HTTP dashboard backed by Indexer + MemoryManager + Watcher."""

    def __init__(
        self,
        root: str | Path = ".cursor",
        memory_path: str | Path = ".cache/memory.json",
        static_dir: str | Path | None = None,
        workflow: "Workflow | None" = None,
        auth_token: str | None = None,
    ) -> None:
        """
        Args:
            auth_token: If set, all API endpoints require `?token=<value>`.
                The HTML page at `/` stays open so a logged-in user can
                bookmark it with the token in URL bar. Default: None
                (no auth, suitable for localhost-only use).
        """
        self.root = Path(root).resolve()
        self.memory_path = Path(memory_path)
        self.static_dir = (
            Path(static_dir).resolve()
            if static_dir
            else (Path(__file__).parent / "dashboard").resolve()
        )
        self.workflow = workflow  # optional live stats source
        self.auth_token = auth_token

    def _read_index(self) -> dict | None:
        index_path = self.root / "INDEX.json"
        if not index_path.exists():
            return None
        try:
            with index_path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, json.JSONDecodeError):
            return None

    def _read_memory(self) -> dict:
        if not self.memory_path.exists():
            return {"entries": 0, "hits": 0, "misses": 0, "tokens_saved": 0}
        m = MemoryManager()
        MemoryStore(self.memory_path).load_into(m)
        return {
            "entries": sum(len(t) for t in m._storage.values()),
            "hits": m._hits,
            "misses": m._misses,
            "tokens_saved": m._total_tokens_saved,
        }

    def _stats(self) -> dict:
        # ponytail: when wired to a Workflow with auto-watch, the watcher
        # invalidates self.workflow._index on file change. Rebuild now so
        # /api/stats reflects the current disk state instead of stale data.
        if self.workflow is not None and self.workflow._index is None:
            try:
                self.workflow._ensure_index()
            except Exception:
                pass  # non-fatal: fall through to INDEX.json on disk
        idx_data = self._read_index()
        totals = idx_data.get("totals", {}) if idx_data else {}
        mem = self._read_memory()
        out = {
            "assets_indexed": totals.get("grand_total", 0),
            "categories": {k: v for k, v in totals.items() if k != "grand_total"},
            "memory": mem,
            "index_fresh": idx_data is not None,
        }
        if self.workflow is not None:
            try:
                out["workflow"] = self.workflow.stats()
            except Exception:
                out["workflow"] = {}
        return out

    def _serve_static(self, rel_path: str) -> tuple[bytes, str] | None:
        # ponytail: serve only files inside self.static_dir (no traversal).
        target = (self.static_dir / rel_path).resolve()
        if not str(target).startswith(str(self.static_dir)):
            return None
        if not target.is_file():
            return None
        mime, _ = mimetypes.guess_type(target.name)
        try:
            return target.read_bytes(), mime or "application/octet-stream"
        except OSError:
            return None

    def _make_handler(self):
        dashboard = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):  # silence stderr noise
                pass

            def _send(self, status: int, body: bytes, mime: str) -> None:
                self.send_response(status)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
                parsed = urlparse(self.path)
                path = parsed.path
                query = parse_qs(parsed.query)

                # ponytail: cheap synchronous auth check first — no point
                # doing any work for an unauthorized caller. Token can come
                # via query string (for browser <script src="?token=...">)
                # or X-Auth-Token header (for API clients).
                token = (query.get("token", [None])[0]
                         or self.headers.get("X-Auth-Token"))
                if dashboard.auth_token and token != dashboard.auth_token:
                    self._send(401, b'{"error":"unauthorized"}', "application/json")
                    return

                if path == "/" or path == "/index.html":
                    body = dashboard._serve_static("index.html")
                    if body:
                        self._send(200, body[0], body[1])
                    else:
                        self._send(404, b"Dashboard HTML not found", "text/plain")
                    return

                if path == "/api/index":
                    # ponytail: if workflow invalidated index, rebuild
                    # so the dashboard reflects fresh state on this request.
                    if dashboard.workflow is not None and dashboard.workflow._index is None:
                        try:
                            dashboard.workflow._ensure_index()
                            dashboard.workflow._index.write_json()
                        except Exception:
                            pass
                    data = dashboard._read_index()
                    if data is None:
                        self._send(404, b'{"error":"no index"}', "application/json")
                    else:
                        self._send(200, json.dumps(data).encode("utf-8"), "application/json")
                    return

                if path == "/api/stats":
                    self._send(
                        200,
                        json.dumps(dashboard._stats()).encode("utf-8"),
                        "application/json",
                    )
                    return

                if path == "/api/memory":
                    self._send(
                        200,
                        json.dumps(dashboard._read_memory()).encode("utf-8"),
                        "application/json",
                    )
                    return

                # fallback: static asset (e.g. style.css)
                rel = path.lstrip("/")
                if rel and not rel.startswith("api/"):
                    body = dashboard._serve_static(rel)
                    if body:
                        self._send(200, body[0], body[1])
                        return

                self._send(404, b"Not found", "text/plain")

        return Handler

    def serve(self, host: str = "127.0.0.1", port: int = 8765) -> None:
        """Block forever serving dashboard until interrupted."""
        server = ThreadingHTTPServer((host, port), self._make_handler())
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()