"""Lazy file loader for rules/skills/agents.

Reads the file once, caches the result through `cache.LRUCache`, and tracks
estimated tokens. Files are read fully into memory — they are small markdown
documents. No streaming, no chunking: this is what makes the cache effective.

Skill files starting with `# Alias:` are resolved through their redirect target
so callers always see the real content (the alias file is only a few lines).
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .cache import LRUCache
from .registry import Registry, RegistryItem, build_registry

# Cheap token estimator: ~0.75 tokens / word for English markdown.
_WORD_RE = re.compile(r"\S+")

# Recognise alias files: "# Alias: <name>" with a path somewhere in the body.
_ALIAS_HEADER_RE = re.compile(r"^#\s*Alias:\s*", re.IGNORECASE)
# Match a `.cursor/skills/<name>/SKILL.md` path anywhere in the body — alias
# files put the path on its own line between backticks.
_ALIAS_TARGET_RE = re.compile(r"(\.cursor/skills/[^`\s]+/SKILL\.md)", re.IGNORECASE)


def estimate_tokens(text: str) -> int:
    """Approximate token count for a chunk of text."""
    if not text:
        return 0
    return max(1, int(len(_WORD_RE.findall(text)) * 0.75))


@dataclass
class LoadedItem:
    """Result of a load."""

    item: RegistryItem
    body: str
    tokens: int
    loaded_from_disk: bool  # True if loaded this call, False if cache hit
    resolved_via_alias: bool = False


def _strip_bom(text: str) -> str:
    if text.startswith("\ufeff"):
        return text[1:]
    return text


def _resolve_alias_target(body: str, workspace_root: str) -> Path | None:
    """If `body` is an alias redirect, return the resolved absolute path."""
    body = _strip_bom(body)
    first = body.splitlines()[0] if body else ""
    if not _ALIAS_HEADER_RE.match(first):
        return None
    m = _ALIAS_TARGET_RE.search(body)
    if not m:
        return None
    target_rel = m.group(1).strip()
    # Don't strip leading dots — `.cursor/skills/...` is the real path.
    candidate = Path(workspace_root) / target_rel
    if candidate.exists():
        return candidate
    # Fallback: try the same path with `./` prefix (Windows-safe).
    candidate2 = Path(workspace_root) / ("." + target_rel if not target_rel.startswith(".") else target_rel)
    if candidate2.exists():
        return candidate2
    return None


class Loader:
    """Read items from disk through per-kind LRU caches."""

    def __init__(self, registry: Registry, cache_cfg: dict[str, Any] | None = None) -> None:
        self.registry = registry
        self.workspace_root = registry.workspace_root
        cfg = cache_cfg or {}
        self.rules_cache = LRUCache[str, LoadedItem](
            max_items=int(cfg.get("max_rules", 20)),
            ttl_seconds=float(cfg.get("ttl_seconds", 1800)),
            name="rules",
        )
        self.skills_cache = LRUCache[str, LoadedItem](
            max_items=int(cfg.get("max_skills", 30)),
            ttl_seconds=float(cfg.get("ttl_seconds", 1800)),
            name="skills",
        )
        self.agents_cache = LRUCache[str, LoadedItem](
            max_items=int(cfg.get("max_agents", 10)),
            ttl_seconds=float(cfg.get("ttl_seconds", 1800)),
            name="agents",
        )

    # ------------------------------------------------------------------ public

    def load_rule(self, rule_id: str) -> LoadedItem:
        return self._load(rule_id, "rule", self.rules_cache)

    def load_skill(self, skill_id: str) -> LoadedItem:
        return self._load(skill_id, "skill", self.skills_cache)

    def load_agent(self, agent_id: str) -> LoadedItem:
        return self._load(agent_id, "agent", self.agents_cache)

    def clear(self, kind: str | None = None, key: str | None = None) -> int:
        """Clear cache. If kind+key, drop one entry. If kind only, drop all of kind. Else clear all."""
        caches = {"rule": self.rules_cache, "skill": self.skills_cache, "agent": self.agents_cache}
        if key and kind:
            cache = caches.get(kind)
            return 1 if cache and cache.remove(key) else 0
        if kind:
            cache = caches.get(kind)
            return cache.clear() if cache else 0
        total = 0
        for c in caches.values():
            total += c.clear()
        return total

    def caches(self) -> dict[str, LRUCache]:
        return {"rule": self.rules_cache, "skill": self.skills_cache, "agent": self.agents_cache}

    # ------------------------------------------------------------------ helpers

    def _load(self, identifier: str, kind: str, cache: LRUCache[str, LoadedItem]) -> LoadedItem:
        # Resolve identifier -> RegistryItem
        item = self.registry.lookup(identifier)
        if item is None or item.kind != kind:
            raise KeyError(f"{kind} '{identifier}' not found in registry")
        if not item.exists or not Path(item.abs_path).is_file():
            raise FileNotFoundError(f"{kind} '{identifier}' path missing: {item.abs_path}")

        cached = cache.get(item.id)
        if cached is not None:
            return LoadedItem(item=item, body=cached.body, tokens=cached.tokens, loaded_from_disk=False, resolved_via_alias=cached.resolved_via_alias)

        path = Path(item.abs_path)
        body = _strip_bom(path.read_text(encoding="utf-8", errors="ignore"))
        resolved_via_alias = False

        # Skills: follow alias redirects so the user gets real content.
        if kind == "skill":
            target = _resolve_alias_target(body, self.workspace_root)
            if target is not None:
                body = _strip_bom(target.read_text(encoding="utf-8", errors="ignore"))
                resolved_via_alias = True

        tokens = estimate_tokens(body)
        loaded = LoadedItem(item=item, body=body, tokens=tokens, loaded_from_disk=True, resolved_via_alias=resolved_via_alias)
        cache.put(item.id, loaded, tokens=tokens, metadata={"path": item.path, "kind": kind, "alias": resolved_via_alias})
        return loaded


def make_default_loader(workspace_root: str, cache_cfg: dict[str, Any] | None = None) -> Loader:
    """Convenience: build registry + loader."""
    return Loader(build_registry(workspace_root), cache_cfg)
