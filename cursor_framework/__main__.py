"""
CLI entry point for cursor_framework.

Run modes (minimal, stdlib-only):

    python -m cursor_framework serve [--root .cursor] [--port 8765]
        Start the Dashboard HTTP server (blocks).

    python -m cursor_framework serve-graph [--root .cursor] [--port 8766]
        Start a graph visualization HTTP server: `/` (D3 force-directed UI),
        `/api/graph` (nodes/edges JSON). Blocks.

    python -m cursor_framework ask "your request" [--root .cursor] [--max-tokens 4000]
        Run the Workflow pipeline once and print a JSON summary + context text.

    python -m cursor_framework warm [--root .cursor]
        Force a full index + memory persist, print stats.

    python -m cursor_framework stats [--root .cursor]
        Print current Workflow stats (assets, memory, cache).

    python -m cursor_framework scan [--root .cursor]
        Just scan .cursor/ and print INDEX totals (no files written).

    python -m cursor_framework index [--root .cursor]
        Scan + persist INDEX.json + INDEX.md. Returns paths + counts.

    python -m cursor_framework clear-cache [--root .cursor] [--force] [--dry-run]
        Wipe memory file + INDEX cache. Default dry-run; pass --force to act.

    python -m cursor_framework graph [--root .cursor]
        Build skill dependency graph and print nodes/edges JSON to stdout.

    python -m cursor_framework --version
        Print version and exit.

No third-party deps — argparse + stdlib http.server only.
Designed for `python -m cursor_framework` and the `cursor-framework`
console_scripts entry.
"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

# Windows terminals default to cp1252; skill/context text contains arrows (→)
# and box-drawing chars. Reconfigure to UTF-8 before printing anything.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except (AttributeError, OSError):
    pass

from . import __version__
from .dashboard import Dashboard
from .indexer import Indexer
from .skill_discovery import SkillRegistry, SkillDiscovery
from .workflow import Workflow


def _common_flags() -> argparse.ArgumentParser:
    """Return a parent parser with the flags shared across all subcommands."""
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--root", default=".cursor", help="Path to the .cursor directory (default: ./.cursor)")
    p.add_argument(
        "--memory-path",
        default=".cache/memory.json",
        help="Path to the JSON-backed memory file (default: ./.cache/memory.json)",
    )
    p.add_argument(
        "--max-tokens",
        type=int,
        default=4000,
        help="Token budget for Workflow ask() (default: 4000)",
    )
    return p


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cursor-framework",
        description="Cursor Enterprise Framework CLI",
        parents=[_common_flags()],
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"cursor-framework {__version__}",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    serve = sub.add_parser(
        "serve",
        help="Start the Dashboard HTTP server (blocking)",
        parents=[_common_flags()],
    )
    serve.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    serve.add_argument("--port", type=int, default=8765, help="Bind port (default: 8765)")
    serve.add_argument("--auth-token", default=None, help="If set, require ?token=... on /api/*")

    ask = sub.add_parser(
        "ask",
        help="Run the Workflow once for a request string",
        parents=[_common_flags()],
    )
    ask.add_argument("request", help="Natural-language request to route through the framework")

    sub.add_parser("warm", help="Force a full index + memory persist, print stats", parents=[_common_flags()])
    sub.add_parser("stats", help="Print current Workflow stats", parents=[_common_flags()])
    sub.add_parser("scan", help="Just scan .cursor/ and print INDEX totals", parents=[_common_flags()])

    # index: scan + persist
    sub.add_parser(
        "index",
        help="Scan .cursor/ and write INDEX.json + INDEX.md to the root",
        parents=[_common_flags()],
    )

    # clear-cache: wipe memory + INDEX cache
    clear = sub.add_parser(
        "clear-cache",
        help="Wipe memory file + INDEX cache. Default is dry-run; use --force to delete.",
        parents=[_common_flags()],
    )
    clear.add_argument(
        "--force",
        action="store_true",
        help="Actually delete. Without this flag, only list what would be deleted.",
    )

    # graph: build dependency graph and print JSON
    sub.add_parser(
        "graph",
        help="Print skill dependency graph (nodes/edges) as JSON",
        parents=[_common_flags()],
    )

    # serve-graph: HTTP server with D3 viz page
    graph_serve = sub.add_parser(
        "serve-graph",
        help="Start a graph visualization HTTP server (D3 force-directed)",
        parents=[_common_flags()],
    )
    graph_serve.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    graph_serve.add_argument("--port", type=int, default=8766, help="Bind port (default: 8766)")

    return parser


def _serve(args: argparse.Namespace) -> int:
    wf = Workflow(root=args.root, memory_path=args.memory_path, max_tokens=args.max_tokens)
    wf.warm()  # ponytail: warm before serving so first /api/index is instant
    dashboard = Dashboard(
        root=args.root,
        memory_path=args.memory_path,
        workflow=wf,
        auth_token=args.auth_token,
    )
    print(f"Dashboard serving on http://{args.host}:{args.port}", file=sys.stderr)
    dashboard.serve(host=args.host, port=args.port)
    return 0


def _ask(args: argparse.Namespace) -> int:
    wf = Workflow(root=args.root, memory_path=args.memory_path, max_tokens=args.max_tokens)
    result = wf.ask(args.request)
    summary = {
        "from_cache": result.from_cache,
        "memory_hits": result.memory_hits,
        "memory_misses": result.memory_misses,
        "asset_count": result.asset_count,
        "latency_ms": round(result.latency_ms, 2),
        "context_tokens": result.context.tokens if hasattr(result.context, "tokens") else None,
        "context_text": getattr(result.context, "text", str(result.context)),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _warm(args: argparse.Namespace) -> int:
    wf = Workflow(root=args.root, memory_path=args.memory_path, max_tokens=args.max_tokens)
    stats = wf.warm()
    print(json.dumps(stats, indent=2))
    return 0


def _stats(args: argparse.Namespace) -> int:
    wf = Workflow(root=args.root, memory_path=args.memory_path, max_tokens=args.max_tokens)
    print(json.dumps(wf.stats(), indent=2))
    return 0


def _scan(args: argparse.Namespace) -> int:
    idx = Indexer(args.root)
    idx.scan()
    totals = idx.result.totals if idx.result else {}
    print(json.dumps({"totals": totals}, indent=2))
    return 0


def _index(args: argparse.Namespace) -> int:
    """Scan + persist INDEX.json + INDEX.md, return paths + counts."""
    idx = Indexer(args.root)
    idx.scan()
    json_path = idx.write_json()
    md_path = idx.write_markdown()
    payload = {
        "root": str(Path(args.root).resolve()),
        "assets": idx.result.totals.get("grand_total", 0),
        "totals": idx.result.totals,
        "files": {
            "index_json": str(json_path),
            "index_md": str(md_path),
        },
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _collect_cache_paths(root: Path, memory_path: Path) -> list[Path]:
    """Return the list of cache files the framework writes to disk. Pure function."""
    candidates: list[Path] = []
    memory_file = Path(memory_path)
    if not memory_file.is_absolute():
        memory_file = (Path.cwd() / memory_file).resolve()
    candidates.append(memory_file)

    root_resolved = root if root.is_absolute() else (Path.cwd() / root).resolve()
    for name in ("INDEX.json", "INDEX.md"):
        p = root_resolved / name
        if p not in candidates:
            candidates.append(p)
    return candidates


def _clear_cache(args: argparse.Namespace) -> int:
    """
    List (or with --force, delete) cache files: memory + INDEX artifacts.

    Default is dry-run. --force actually deletes. Exits non-zero if any
    delete fails (so a CI script can detect a half-cleaned cache).
    """
    root = Path(args.root).resolve()
    memory_path = Path(args.memory_path)
    targets = _collect_cache_paths(root, memory_path)

    # ponytail: filter to only what exists, so dry-run is informative
    # rather than listing 4 missing files every time.
    existing = [p for p in targets if p.exists()]
    payload: dict[str, Any] = {
        "would_delete": [str(p) for p in existing],
        "missing": [str(p) for p in targets if p not in existing],
        "force": args.force,
        "dry_run": not args.force,
    }

    if not args.force:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    # Force path: actually delete, report per-file outcome.
    errors: list[str] = []
    for p in existing:
        try:
            p.unlink()
        except OSError as exc:
            errors.append(f"{p}: {exc}")
    payload["deleted"] = [str(p) for p in existing if not errors or str(p) not in "\n".join(errors)]
    payload["errors"] = errors
    payload["dry_run"] = False
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


def _build_graph(root: str) -> dict[str, Any]:
    """
    Build the skill dependency graph.

    Nodes = skills + agents (anything in the registry).
    Edges = explicit `SkillMetadata.dependencies` (solid, primary) +
            co-occurrence from `SkillDiscovery.COMBINATION_RULES` (dashed,
            informational — secondary skills that often run together).

    No text scanning — only structured fields that the framework tracks.
    """
    root_path = Path(root).resolve()
    registry = SkillRegistry()
    skills = registry.get_all()

    nodes: list[dict[str, Any]] = []
    for s in skills:
        # Categorize: agents live under .cursor/agents/, skills under .cursor/skills/.
        is_agent = "agents/" in s.path
        nodes.append({
            "id": s.name,
            "kind": "agent" if is_agent else "skill",
            "version": s.version,
            "tags": s.tags[:8],  # trim for graph readability
            "path": s.path,
        })

    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str]] = set()
    for s in skills:
        for dep in s.dependencies:
            edge = (s.name, dep)
            if edge not in seen_edges and dep in registry._skills:
                seen_edges.add(edge)
                edges.append({"source": s.name, "target": dep, "kind": "dependency"})

    # Secondary edges from combination rules — informational only.
    for rule in SkillDiscovery.COMBINATION_RULES.values():
        primary = rule.get("primary")
        for secondary in rule.get("secondary", []):
            edge = (primary, secondary)
            if edge not in seen_edges and primary in registry._skills and secondary in registry._skills:
                seen_edges.add(edge)
                edges.append({"source": primary, "target": secondary, "kind": "co_occurrence"})

    return {
        "root": str(root_path),
        "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }


def _graph(args: argparse.Namespace) -> int:
    """Print the graph JSON to stdout."""
    print(json.dumps(_build_graph(args.root), indent=2, ensure_ascii=False))
    return 0


# HTML page for / on the graph server. D3 force-directed, CDN-hosted,
# single file, no build step. Keeps `serve-graph` dependency-free.
_GRAPH_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>cursor_framework — Skill Graph</title>
<style>
  body{margin:0;font-family:-apple-system,system-ui,sans-serif;background:#0e1117;color:#c9d1d9}
  svg{display:block}
  .node circle{stroke:#fff;stroke-width:1.5px;cursor:pointer}
  .node.skill circle{fill:#58a6ff}
  .node.agent circle{fill:#f78166}
  .node text{fill:#c9d1d9;font-size:11px;pointer-events:none;paint-order:stroke;stroke:#0e1117;stroke-width:3px}
  .link{stroke:#30363d}
  .link.dep{stroke:#58a6ff;stroke-opacity:.6}
  .link.co{stroke:#f78166;stroke-dasharray:4 3;stroke-opacity:.4}
  #legend{position:fixed;top:12px;right:12px;background:#161b22;border:1px solid #30363d;padding:8px 10px;border-radius:6px;font-size:12px;line-height:1.6}
  #legend span.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}
</style>
</head>
<body>
<svg id="graph" width="100%" height="100vh"></svg>
<div id="legend">
  <div><span class="dot" style="background:#58a6ff"></span>skill</div>
  <div><span class="dot" style="background:#f78166"></span>agent</div>
  <div><span class="dot" style="background:#58a6ff;opacity:.6"></span>dependency</div>
  <div><span class="dot" style="background:#f78166;opacity:.4"></span>co-occurrence</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
fetch("/api/graph").then(r => r.json()).then(g => {
  const svg = d3.select("#graph");
  const w = window.innerWidth, h = window.innerHeight;
  const simulation = d3.forceSimulation(g.nodes)
    .force("link", d3.forceLink(g.edges).id(d => d.id).distance(110))
    .force("charge", d3.forceManyBody().strength(-260))
    .force("center", d3.forceCenter(w / 2, h / 2));
  const link = svg.append("g").selectAll("line")
    .data(g.edges).join("line")
      .attr("class", d => "link " + (d.kind === "dependency" ? "dep" : "co"))
      .attr("stroke-width", 1.4);
  const node = svg.append("g").selectAll("g")
    .data(g.nodes).join("g")
      .attr("class", d => "node " + d.kind)
    .call(d3.drag()
      .on("start", (e,d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
      .on("drag", (e,d) => { d.fx = e.x; d.fy = e.y; })
      .on("end", (e,d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));
  node.append("circle").attr("r", 8);
  node.append("title").text(d => d.id + " (" + d.kind + ", v" + d.version + ")");
  node.append("text").attr("dx", 11).attr("dy", 3).text(d => d.id);
  simulation.on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
  });
  window.addEventListener("resize", () => {
    const w2 = window.innerWidth, h2 = window.innerHeight;
    svg.attr("width", w2).attr("height", h2);
    simulation.force("center", d3.forceCenter(w2 / 2, h2 / 2));
    simulation.alpha(0.3).restart();
  });
});
</script>
</body>
</html>
"""


def _serve_graph(args: argparse.Namespace) -> int:
    """Start a tiny stdlib HTTP server serving the graph JSON + D3 HTML."""
    graph_data = _build_graph(args.root)
    graph_json = json.dumps(graph_data, ensure_ascii=False)
    html = _GRAPH_HTML.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a, **kw):
            pass  # silence

        def _send(self, status, body, mime):
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):  # noqa: N802 (stdlib naming)
            if self.path == "/" or self.path.startswith("/?"):
                self._send(200, html, "text/html; charset=utf-8")
                return
            if self.path.startswith("/api/graph"):
                self._send(200, graph_json.encode("utf-8"), "application/json")
                return
            self._send(404, b"Not found", "text/plain")

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        f"Graph serving on http://{args.host}:{args.port} "
        f"({graph_data['node_count']} nodes, {graph_data['edge_count']} edges)",
        file=sys.stderr,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "serve": _serve,
        "serve-graph": _serve_graph,
        "ask": _ask,
        "warm": _warm,
        "stats": _stats,
        "scan": _scan,
        "index": _index,
        "clear-cache": _clear_cache,
        "graph": _graph,
    }
    return dispatch[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
