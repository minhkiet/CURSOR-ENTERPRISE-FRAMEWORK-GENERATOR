"""
Prefect Workflow Orchestration Module.

Orchestrates enterprise maintenance pipelines using Prefect flows and tasks:
- Workspace asset scanning & indexing with retries and caching
- Multi-tool vibe coding rule & skill synchronization
- System health auditing and Redis observability checks

Includes zero-dependency fallbacks:
Runs cleanly with standard Python logging if Prefect is not installed.
"""

from __future__ import annotations

import functools
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

logger = logging.getLogger(__name__)

# Check if Prefect is installed
try:
    from prefect import flow as prefect_flow, task as prefect_task, get_run_logger
    HAS_PREFECT = True
except ImportError:
    HAS_PREFECT = False
    prefect_flow = None  # type: ignore[assignment]
    prefect_task = None  # type: ignore[assignment]
    get_run_logger = None  # type: ignore[assignment]

F = TypeVar("F", bound=Callable[..., Any])


def task(
    retries: int = 0,
    retry_delay_seconds: float = 0.0,
    cache_expiration: Optional[timedelta] = None,
    name: Optional[str] = None,
    **kwargs: Any,
) -> Callable[[F], F]:
    """Task decorator: wraps Prefect @task when installed, falls back to direct execution."""
    if HAS_PREFECT and prefect_task is not None:
        return prefect_task(
            name=name,
            retries=retries,
            retry_delay_seconds=retry_delay_seconds,
            cache_expiration=cache_expiration,
            **kwargs,
        )

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **func_kwargs: Any) -> Any:
            attempts = 0
            max_attempts = max(1, retries + 1)
            last_err = None

            while attempts < max_attempts:
                attempts += 1
                try:
                    return fn(*args, **func_kwargs)
                except Exception as err:
                    last_err = err
                    if attempts < max_attempts and retry_delay_seconds > 0:
                        logger.warning(
                            "Task '%s' failed (attempt %d/%d): %s. Retrying in %ss...",
                            fn.__name__, attempts, max_attempts, err, retry_delay_seconds,
                        )
                        time.sleep(retry_delay_seconds)
            raise last_err  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


def flow(
    name: Optional[str] = None,
    log_prints: bool = True,
    **kwargs: Any,
) -> Callable[[F], F]:
    """Flow decorator: wraps Prefect @flow when installed, falls back to direct execution."""
    if HAS_PREFECT and prefect_flow is not None:
        return prefect_flow(name=name, log_prints=log_prints, **kwargs)

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **func_kwargs: Any) -> Any:
            flow_name = name or fn.__name__
            logger.info("Executing flow: %s (Prefect installed: %s)", flow_name, HAS_PREFECT)
            start = time.perf_counter()
            result = fn(*args, **func_kwargs)
            duration = (time.perf_counter() - start) * 1000
            logger.info("Flow '%s' completed successfully in %.1fms", flow_name, duration)
            return result

        return wrapper  # type: ignore[return-value]

    return decorator


def _get_flow_logger() -> Any:
    """Return Prefect run logger if inside a Prefect run, otherwise standard logger."""
    if HAS_PREFECT and get_run_logger is not None:
        try:
            return get_run_logger()
        except Exception:
            return logger
    return logger


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline Tasks
# ─────────────────────────────────────────────────────────────────────────────

@task(retries=2, retry_delay_seconds=1.0, name="scan_workspace_assets")
def scan_workspace_assets(root_path: str = ".cursor") -> dict[str, Any]:
    """Scan the workspace directory for rules, skills, agents, and templates."""
    log = _get_flow_logger()
    log.info("Scanning assets under %s...", root_path)

    from .indexer import Indexer
    indexer = Indexer(root=root_path)
    result = indexer.scan()
    total = result.totals.get("grand_total", 0)

    log.info(
        "Scan complete: %d total assets found (rules: %d, skills: %d, agents: %d)",
        total,
        result.totals.get("rules", 0),
        result.totals.get("skills", 0),
        result.totals.get("agents", 0),
    )
    return {
        "total_assets": total,
        "categories": result.totals,
    }


@task(retries=2, retry_delay_seconds=1.0, name="build_asset_index")
def build_asset_index(root_path: str = ".cursor") -> dict[str, str]:
    """Generate and persist INDEX.json and INDEX.md machine-readable indexes."""
    log = _get_flow_logger()
    log.info("Generating INDEX.json and INDEX.md in %s...", root_path)

    from .indexer import Indexer
    indexer = Indexer(root=root_path)
    indexer.scan()
    json_path = indexer.write_json()
    md_path = indexer.write_markdown()

    log.info("Persisted index files: JSON=%s, Markdown=%s", json_path, md_path)
    return {"json": str(json_path), "markdown": str(md_path)}


@task(retries=1, retry_delay_seconds=1.0, name="warm_memory_cache")
def warm_memory_cache(root_path: str = ".cursor", memory_path: str = ".cache/memory.json") -> dict[str, Any]:
    """Pre-warm workflow memory cache for instantaneous responses."""
    log = _get_flow_logger()
    log.info("Warming workflow memory store at %s...", memory_path)

    from .workflow import Workflow
    wf = Workflow(root=root_path, memory_path=memory_path, strict_persist=True)
    res = wf.warm()
    assets = res.get("assets_indexed", res.get("assets", 0))
    entries = res.get("memory_entries", res.get("entries", 0))
    log.info("Warm complete: %d assets indexed, %d entries in memory cache", assets, entries)
    return res


@task(retries=1, name="detect_vibe_tools_task")
def detect_vibe_tools_task(workspace_root: Optional[str] = None) -> list[str]:
    """Detect all active vibe coding tools in workspace."""
    log = _get_flow_logger()
    from .vibe_sync import VibeDetector
    detector = VibeDetector(workspace_root)
    active = detector.detect_active_tools()
    tool_names = [t.value for t in active]
    log.info("Detected %d active vibe tools: %s", len(tool_names), ", ".join(tool_names) if tool_names else "none")
    return tool_names


@task(retries=2, retry_delay_seconds=1.0, name="sync_vibe_tools_task")
def sync_vibe_tools_task(
    tools: Optional[list[str]] = None,
    workspace_root: Optional[str] = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Generate tool-native instruction files for detected vibe tools."""
    log = _get_flow_logger()
    from .vibe_sync import VibeSyncEngine, VibeTool

    engine = VibeSyncEngine(workspace_root)
    parsed_tools = [VibeTool(t) for t in tools] if tools else None
    report = engine.sync(tools=parsed_tools, dry_run=dry_run)

    log.info(
        "Vibe sync complete: %d files modified for tools %s (dry_run=%s)",
        len(report.files_modified),
        [t.value for t in report.synced_tools],
        dry_run,
    )
    return report.to_dict()


@task(name="check_redis_health_task")
def check_redis_health_task(redis_url: Optional[str] = None) -> dict[str, Any]:
    """Inspect Redis health and collect observability metrics."""
    log = _get_flow_logger()
    from .redis_store import RedisObservability

    obs = RedisObservability(redis_url=redis_url)
    metrics = obs.collect_metrics()

    log.info(
        "Redis status: connected=%s, memory=%s, hit_ratio=%.1f%%, alerts=%d",
        metrics.is_connected,
        metrics.used_memory_human,
        metrics.hit_ratio * 100,
        len(metrics.alerts),
    )
    return metrics.to_dict()


# ─────────────────────────────────────────────────────────────────────────────
# Orchestration Flows
# ─────────────────────────────────────────────────────────────────────────────

@flow(name="index_and_warm_flow", log_prints=True)
def index_and_warm_flow(
    root_path: str = ".cursor",
    memory_path: str = ".cache/memory.json",
) -> dict[str, Any]:
    """Flow 1: Complete indexing, machine cache generation, and memory warm-up."""
    scan_res = scan_workspace_assets(root_path)
    index_res = build_asset_index(root_path)
    warm_res = warm_memory_cache(root_path, memory_path)
    return {
        "status": "success",
        "scan": scan_res,
        "indexes": index_res,
        "warm": warm_res,
    }


@flow(name="vibe_sync_flow", log_prints=True)
def vibe_sync_flow(
    tools: Optional[list[str]] = None,
    workspace_root: Optional[str] = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Flow 2: Automated multi-tool vibe coding synchronization."""
    detected = detect_vibe_tools_task(workspace_root)
    target_tools = tools if tools else detected
    sync_res = sync_vibe_tools_task(tools=target_tools, workspace_root=workspace_root, dry_run=dry_run)
    return {
        "status": "success",
        "detected_tools": detected,
        "sync_result": sync_res,
    }


@flow(name="health_flow", log_prints=True)
def health_flow(redis_url: Optional[str] = None) -> dict[str, Any]:
    """Flow 3: Comprehensive system health and observability check."""
    redis_res = check_redis_health_task(redis_url)
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "prefect_active": HAS_PREFECT,
        "redis": redis_res,
    }


@flow(name="full_maintenance_pipeline", log_prints=True)
def full_maintenance_pipeline(
    root_path: str = ".cursor",
    memory_path: str = ".cache/memory.json",
    workspace_root: Optional[str] = None,
    redis_url: Optional[str] = None,
) -> dict[str, Any]:
    """Flow 4: End-to-end maintenance pipeline combining indexing, vibe sync, and health checks."""
    idx = index_and_warm_flow(root_path, memory_path)
    vibe = vibe_sync_flow(workspace_root=workspace_root)
    health = health_flow(redis_url)
    return {
        "status": "completed",
        "pipeline": "full_maintenance",
        "indexing": idx,
        "vibe_sync": vibe,
        "health": health,
    }
