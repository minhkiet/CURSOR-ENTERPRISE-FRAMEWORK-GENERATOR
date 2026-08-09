"""FastMCP server entry point for the Cursor Enterprise Framework.

Exposes the following MCP tools:
  - get_rule / get_skill / get_agent
  - analyze_task
  - load_skill_bundle
  - get_essential_skills
  - clear_cache
  - get_framework_status
  - optimize_framework

Run standalone:
    python -m cursor_framework_mcp.server
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "FastMCP is not installed. Install with: pip install -r requirements.txt"
    ) from exc

from .analyzer import AnalysisResult, Suggestion, TaskAnalyzer
from .loader import Loader, make_default_loader
from .optimizer import Optimizer
from .registry import (
    AGENT_DOMAINS,
    ESSENTIAL_SKILLS,
    SKILL_BUNDLES,
    SKILL_DOMAINS,
    build_registry,
    find_workspace_root,
)

log = logging.getLogger("cursor_framework_mcp")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")

DEFAULT_CACHE_CFG: dict[str, Any] = {
    "max_rules": 20,
    "max_skills": 30,
    "max_agents": 10,
    "ttl_seconds": 1800,
}


def _resolve_workspace_root() -> str:
    """Prefer CURSOR_WORKSPACE_ROOT env var, then walk up looking for `.cursor`."""
    env = os.environ.get("CURSOR_WORKSPACE_ROOT")
    if env and Path(env).is_dir():
        return str(Path(env).resolve())
    cwd = os.getcwd()
    found = find_workspace_root(cwd)
    return found


def _to_json(obj: Any) -> str:
    """Stable JSON encoding for FastMCP tool returns."""
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)


def _suggestion_to_dict(s: Suggestion) -> dict:
    return {
        "id": s.id,
        "kind": s.kind,
        "confidence": s.confidence,
        "domains": s.domains,
        "reason": s.reason,
        "path": s.path,
    }


def _analysis_to_dict(result: AnalysisResult) -> dict:
    return {
        "request": result.request,
        "detected_language": result.detected_language,
        "detected_domains": result.detected_domains,
        "is_coding_task": result.is_coding_task,
        "primary": _suggestion_to_dict(result.primary) if result.primary else None,
        "suggestions": [_suggestion_to_dict(s) for s in result.suggestions],
        "essential_skills": [_suggestion_to_dict(s) for s in result.essential_skills],
    }


# ----------------------------------------------------------------- server factory

def create_server(workspace_root: str | None = None, cache_cfg: dict | None = None) -> FastMCP:
    """Build a configured FastMCP server."""
    cfg = {**DEFAULT_CACHE_CFG, **(cache_cfg or {})}
    root = workspace_root or _resolve_workspace_root()
    log.info("Workspace root: %s", root)
    log.info("Cache config: %s", cfg)

    registry = build_registry(root)
    loader = make_default_loader(root, cfg)
    analyzer = TaskAnalyzer(loader)
    optimizer = Optimizer(loader)

    mcp = FastMCP(
        "cursor-framework-mcp",
        instructions=(
            "Cursor Enterprise Framework MCP. Load rules, skills, and agents "
            "on-demand with LRU caching, analyze free-form requests, and "
            "optimize the cache. Workspace root: "
            f"{root}"
        ),
    )

    # ----------------------------------------------------------- get_rule
    @mcp.tool()
    def get_rule(rule_id: str) -> str:
        """Load a `.cursor/rules/*.mdc` rule by id (e.g. 'coding-standards') or path (e.g. '.cursor/rules/coding-standards.mdc')."""
        try:
            loaded = loader.load_rule(rule_id)
        except KeyError as e:
            return _to_json({"error": "not_found", "message": str(e)})
        except FileNotFoundError as e:
            return _to_json({"error": "missing_on_disk", "message": str(e)})
        return _to_json(
            {
                "id": loaded.item.id,
                "kind": "rule",
                "path": loaded.item.path,
                "tokens": loaded.tokens,
                "cache_hit": not loaded.loaded_from_disk,
                "body": loaded.body,
            }
        )

    # ----------------------------------------------------------- get_skill
    @mcp.tool()
    def get_skill(skill_id: str, include_dependencies: bool = False) -> str:
        """Load a `SKILL.md` by id. With `include_dependencies=True`, also load
        any co-required skills (essential overlays + bundle-mates)."""
        try:
            loaded = loader.load_skill(skill_id)
        except KeyError as e:
            return _to_json({"error": "not_found", "message": str(e)})
        except FileNotFoundError as e:
            return _to_json({"error": "missing_on_disk", "message": str(e)})
        result: dict[str, Any] = {
            "id": loaded.item.id,
            "kind": "skill",
            "path": loaded.item.path,
            "tokens": loaded.tokens,
            "cache_hit": not loaded.loaded_from_disk,
            "domains": loaded.item.domains,
            "body": loaded.body,
        }
        if include_dependencies:
            deps: list[dict] = []
            seen = {loaded.item.id}
            # Always include essential overlays
            for ess in ESSENTIAL_SKILLS:
                if ess in seen:
                    continue
                try:
                    dep = loader.load_skill(ess)
                except (KeyError, FileNotFoundError):
                    continue
                deps.append(
                    {
                        "id": dep.item.id,
                        "path": dep.item.path,
                        "tokens": dep.tokens,
                        "cache_hit": not dep.loaded_from_disk,
                    }
                )
                seen.add(dep.item.id)
            # Co-mates from bundle if any
            for bundle_id, members in SKILL_BUNDLES.items():
                if loaded.item.id in members:
                    for mate in members:
                        if mate in seen:
                            continue
                        try:
                            dep = loader.load_skill(mate)
                        except (KeyError, FileNotFoundError):
                            continue
                        deps.append(
                            {
                                "id": dep.item.id,
                                "path": dep.item.path,
                                "tokens": dep.tokens,
                                "bundle": bundle_id,
                                "cache_hit": not dep.loaded_from_disk,
                            }
                        )
                        seen.add(dep.item.id)
            result["dependencies"] = deps
            result["total_tokens"] = loaded.tokens + sum(d["tokens"] for d in deps)
        return _to_json(result)

    # ----------------------------------------------------------- get_agent
    @mcp.tool()
    def get_agent(agent_id: str) -> str:
        """Load an agent persona block from `.cursor/AGENTS.md` by id (e.g. 'security-auditor')."""
        try:
            loaded = loader.load_agent(agent_id)
        except KeyError as e:
            return _to_json({"error": "not_found", "message": str(e)})
        except FileNotFoundError as e:
            return _to_json({"error": "missing_on_disk", "message": str(e)})
        return _to_json(
            {
                "id": loaded.item.id,
                "kind": "agent",
                "path": loaded.item.path,
                "tokens": loaded.tokens,
                "cache_hit": not loaded.loaded_from_disk,
                "body": loaded.body,
            }
        )

    # ----------------------------------------------------------- analyze_task
    @mcp.tool()
    def analyze_task(request: str, top_k: int = 8) -> str:
        """Analyze a free-form user request, return ranked suggestions for rules/skills/agents, and pick a primary one above 0.75 confidence."""
        result = analyzer.analyze(request, top_k=top_k)
        return _to_json(_analysis_to_dict(result))

    # ----------------------------------------------------------- load_skill_bundle
    @mcp.tool()
    def load_skill_bundle(bundle: str) -> str:
        """Pre-load a named bundle ('A'..'E') or a custom list of skill ids."""
        if bundle in SKILL_BUNDLES:
            ids = SKILL_BUNDLES[bundle]
        else:
            # Allow comma-separated custom lists: "karpathy-coding,frontend-taste"
            ids = [s.strip() for s in bundle.split(",") if s.strip()]
        loaded_items: list[dict] = []
        failed: list[str] = []
        total_tokens = 0
        for sid in ids:
            try:
                item = loader.load_skill(sid)
            except (KeyError, FileNotFoundError) as e:
                failed.append(f"{sid}: {e}")
                continue
            total_tokens += item.tokens
            loaded_items.append(
                {
                    "id": item.item.id,
                    "path": item.item.path,
                    "tokens": item.tokens,
                    "cache_hit": not item.loaded_from_disk,
                }
            )
        return _to_json(
            {
                "bundle": bundle,
                "loaded": loaded_items,
                "failed": failed,
                "total_tokens": total_tokens,
            }
        )

    # ----------------------------------------------------------- get_essential_skills
    @mcp.tool()
    def get_essential_skills() -> str:
        """Pre-load the always-on essential overlay skills (karpathy-coding, ponytail, full-output)."""
        items: list[dict] = []
        total = 0
        for sid in ESSENTIAL_SKILLS:
            try:
                loaded = loader.load_skill(sid)
            except (KeyError, FileNotFoundError) as e:
                items.append({"id": sid, "error": str(e)})
                continue
            total += loaded.tokens
            items.append(
                {
                    "id": loaded.item.id,
                    "path": loaded.item.path,
                    "tokens": loaded.tokens,
                    "cache_hit": not loaded.loaded_from_disk,
                }
            )
        return _to_json({"essential_skills": items, "total_tokens": total})

    # ----------------------------------------------------------- clear_cache
    @mcp.tool()
    def clear_cache(kind: str | None = None, key: str | None = None) -> str:
        """Clear cached items. `kind` in {rule, skill, agent}; if `key` is also provided, only that one entry is dropped."""
        if kind and kind not in {"rule", "skill", "agent"}:
            return _to_json({"error": "invalid_kind", "message": f"kind must be rule/skill/agent, got {kind!r}"})
        removed = loader.clear(kind=kind, key=key)
        return _to_json({"removed": removed, "kind": kind, "key": key})

    # ----------------------------------------------------------- get_framework_status
    @mcp.tool()
    def get_framework_status() -> str:
        """Return current memory + token usage, cache stats, and registry summary."""
        snapshot = optimizer.snapshot()
        stats = optimizer.cache_stats()
        return _to_json(
            {
                "workspace_root": root,
                "registry": registry.summary(),
                "totals": {
                    "tokens_in_cache": optimizer.total_tokens(),
                    "items_in_cache": sum(s["size"] for s in stats.values()),
                },
                "cache_stats": stats,
                "cached_items": snapshot,
            }
        )

    # ----------------------------------------------------------- optimize_framework
    @mcp.tool()
    def optimize_framework(idle_threshold_seconds: float = 1800.0, compact_to_ratio: float = 0.6) -> str:
        """Evict expired/idle items, compact caches, and return savings."""
        report = optimizer.optimize(idle_threshold_seconds=idle_threshold_seconds, compact_to_ratio=compact_to_ratio)
        return _to_json(report.to_dict())

    return mcp


# ----------------------------------------------------------------- entry point

def run() -> None:
    """Entry point referenced by plugin.json."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    run()
