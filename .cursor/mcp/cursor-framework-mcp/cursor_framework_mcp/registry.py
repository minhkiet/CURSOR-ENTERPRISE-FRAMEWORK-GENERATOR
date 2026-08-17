"""Build and query the registry index of available rules/skills/agents.

The registry is built **once** at MCP server start by scanning the workspace
filesystem. It maps ids -> {path, kind, domains, triggers, ...} so the
analyzer and MCP tools can resolve items without touching disk on every call.
"""

from __future__ import annotations

import os
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# --- Trigger keywords grouped by skill/domain ---------------------------------

DOMAIN_TRIGGERS: dict[str, list[str]] = {
    "frontend": ["landing page", "ui", "ux", "css", "react", "next.js", "vue", "tailwind", "design", "responsive", "animation", "hero", "navbar", "dashboard ui", "data table"],
    "backend": ["api", "endpoint", "controller", "service", "nestjs", "laravel", "asp.net", "fastapi", "express", "route", "middleware", "orm", "prisma", "drizzle"],
    "database": ["sql", "postgres", "postgresql", "mysql", "mongodb", "redis", "migration", "schema", "index", "query", "rls", "row level security", "transaction"],
    "security": ["security", "owasp", "xss", "sql injection", "csrf", "ssrf", "xxe", "auth", "authentication", "authorization", "rbac", "jwt", "oauth", "secret", "vulnerability", "pentest", "recon", "nmap", "nuclei"],
    "payment": ["payment", "momo", "sepay", "payos", "zalopay", "vnpay", "vietqr", "stripe", "webhook"],
    "design": ["design", "taste", "anti-slop", "typography", "color", "layout", "aesthetic", "minimalist", "brutalist", "editorial"],
    "performance": ["performance", "core web vitals", "lcp", "inp", "cls", "bundle", "lazy load", "memoization", "render"],
    "ai": ["llm", "openai", "anthropic", "claude", "gemini", "rag", "vector", "embedding", "weknora", "pgvector", "prompt"],
    "infra": ["aws", "azure", "gcp", "cloudflare", "kubernetes", "docker", "terraform", "vercel", "serverless", "lambda", "cloud run"],
    "data": ["etl", "pipeline", "warehouse", "spark", "databricks", "pandas", "polars"],
    "writing": ["copy", "headline", "tagline", "tone", "voice", "humanize"],
    "documentation": ["doc", "readme", "tutorial", "guide", "markdown"],
    "video": ["video", "short video", "9:16", "tiktok", "reels", "sora"],
    "scraping": ["scrape", "crawl", "extract", "playwright", "selenium"],
    "cloning": ["clone", "mirror", "copy site", "duplicate ui"],
    "general": [],
}

# Skill id -> domain mapping (curated from SKILL-INDEX + skill-registry).
SKILL_DOMAINS: dict[str, list[str]] = {
    "karpathy-coding": ["general"],
    "ponytail": ["general"],
    "full-output": ["general"],
    "vibe-coding": ["general"],
    "frontend-taste": ["frontend", "design"],
    "frontend-redesign": ["frontend", "design"],
    "frontend-review": ["frontend"],
    "hallmark": ["frontend", "design"],
    "landing-page-pro": ["frontend"],
    "dashboard-ui": ["frontend"],
    "ui-designer": ["frontend", "design"],
    "ui_visual-explainer": ["general", "writing"],
    "ai-copywriter": ["writing"],
    "simple-english": ["writing", "documentation"],
    "book-to-skill": ["documentation"],
    "security-review": ["security"],
    "vietnam-payment-review": ["payment", "security"],
    "pentest": ["security"],
    "perf-optimization": ["performance"],
    "perf_react-best-practices": ["performance", "frontend"],
    "perf_composition-patterns": ["performance", "frontend"],
    "test_test-analysis": ["general"],
    "perf_perf-optimization": ["performance"],
    "util_stability": ["general"],
    "util_utility-helpers": ["general"],
    "db_data-quality": ["database"],
    "ai_weknora-kb": ["ai", "documentation"],
    "ai_weknora-agent": ["ai"],
    "ai_pixelrag": ["ai"],
    "ai_video-generation": ["video", "ai"],
    "webapp-testing": ["general"],
    "web-scraper": ["scraping"],
    "web-cloner": ["cloning", "frontend"],
    "theme-factory": ["design", "frontend"],
    "canvas-design": ["design", "frontend"],
    "open-design": ["design", "frontend"],
    "visual-explainer": ["writing", "design"],
    "bazi": ["general"],
}

# Agent id -> domain mapping.
AGENT_DOMAINS: dict[str, list[str]] = {
    "code-reviewer": ["general"],
    "test-engineer": ["general"],
    "security-auditor": ["security"],
    "web-performance-auditor": ["performance", "frontend"],
    "ui-designer": ["frontend", "design"],
    "frontend-architect": ["frontend"],
    "backend-reviewer": ["backend"],
    "database-reviewer": ["database"],
    "api-designer": ["backend"],
    "debugger": ["general"],
    "refactor-specialist": ["general"],
    "deployment-engineer": ["infra"],
    "devops-engineer": ["infra"],
    "doc-writer": ["documentation"],
    "marketing-strategist": ["writing"],
    "agent-api-security": ["security", "backend"],
    "migration-specialist": ["database", "backend"],
}


# Skill bundles (from SKILL-INDEX §"Bundles").
SKILL_BUNDLES: dict[str, list[str]] = {
    "A": [  # Web & Dashboard
        "frontend-taste", "landing-page-pro", "dashboard-ui",
        "hallmark", "frontend-review", "perf_react-best-practices",
        "perf_composition-patterns",
    ],
    "B": [  # Full-Stack
        "frontend-taste", "dashboard-ui", "full-output", "karpathy-coding",
        "ponytail", "vibe-coding", "util_stability",
    ],
    "C": [  # AI/ML
        "ai_weknora-kb", "ai_weknora-agent", "ai_pixelrag",
        "ai_video-generation",
    ],
    "D": [  # Database
        "db_data-quality", "frontend-review", "karpathy-coding",
    ],
    "E": [  # Infrastructure
        "perf-optimization", "util_stability", "karpathy-coding",
    ],
}

ESSENTIAL_SKILLS: list[str] = ["karpathy-coding", "ponytail", "full-output"]


@dataclass
class RegistryItem:
    """A single discoverable resource."""

    id: str
    kind: str  # "rule" | "skill" | "agent"
    path: str  # relative to workspace
    abs_path: str  # absolute path
    domains: list[str] = field(default_factory=list)
    triggers: list[str] = field(default_factory=list)
    role: str = "primary"  # primary | secondary | mandatory | overlay
    exists: bool = True


@dataclass
class Registry:
    """In-memory index of rules, skills, agents."""

    workspace_root: str
    rules: dict[str, RegistryItem] = field(default_factory=dict)
    skills: dict[str, RegistryItem] = field(default_factory=dict)
    agents: dict[str, RegistryItem] = field(default_factory=dict)
    by_path: dict[str, RegistryItem] = field(default_factory=dict)
    _lock: threading.RLock = field(default_factory=threading.RLock)

    # ------------------------------------------------------------------ lookup

    def lookup(self, key: str) -> RegistryItem | None:
        """Find by id or relative path. Returns None when missing."""
        with self._lock:
            # Direct id hit (rules/skills/agents)
            for store in (self.rules, self.skills, self.agents):
                if key in store:
                    return store[key]
            # Path lookup (relative path, normalised)
            norm = key.replace("\\", "/").lstrip("/")
            if norm in self.by_path:
                return self.by_path[norm]
            # Try fuzzy id match (e.g. "ui_frontend-taste" -> "frontend-taste")
            lower = key.lower().replace("_", "-")
            for store in (self.skills, self.agents, self.rules):
                for item_id, item in store.items():
                    if item_id.lower().endswith(lower) or lower.endswith(item_id.lower()):
                        return item
            return None

    def search(self, query: str, kind: str | None = None, limit: int = 20) -> list[RegistryItem]:
        q = query.lower().strip()
        if not q:
            return []
        results: list[tuple[int, RegistryItem]] = []
        stores: Iterable[tuple[str, dict[str, RegistryItem]]]
        if kind:
            stores = [(kind, getattr(self, kind))]
        else:
            stores = [("rule", self.rules), ("skill", self.skills), ("agent", self.agents)]
        for _kind, store in stores:
            for item in store.values():
                score = _score(item, q)
                if score > 0:
                    results.append((score, item))
        results.sort(key=lambda x: (-x[0], x[1].id))
        return [item for _, item in results[:limit]]

    # ------------------------------------------------------------------ stats

    def summary(self) -> dict:
        with self._lock:
            return {
                "workspace_root": self.workspace_root,
                "rules": len(self.rules),
                "skills": len(self.skills),
                "agents": len(self.agents),
                "total": len(self.rules) + len(self.skills) + len(self.agents),
            }


def _score(item: RegistryItem, query: str) -> int:
    if query in item.id.lower():
        return 100
    if query in item.path.lower():
        return 50
    if any(query in t.lower() for t in item.triggers):
        return 30
    if any(query in d.lower() for d in item.domains):
        return 20
    return 0


# ---------------------------------------------------------------------- builder

_RULE_ID_RE = re.compile(r"^[#]\s*(.+)$", re.MULTILINE)
_FRONTMATTER_DESC_RE = re.compile(r"description:\s*(.+)$", re.MULTILINE)
_ALIAS_TARGET_RE = re.compile(r"use:\s*\n*\s*`?([^`\n]+/SKILL\.md)`?", re.IGNORECASE)


def build_registry(workspace_root: str) -> Registry:
    """Scan `.cursor/rules`, `.cursor/skills`, `.cursor/agents` and index items."""
    root = Path(workspace_root).resolve()
    rules_dir = root / ".cursor" / "rules"
    skills_dir = root / ".cursor" / "skills"
    agents_dir = root / ".cursor" / "agents"

    reg = Registry(workspace_root=str(root))

    if rules_dir.is_dir():
        for path in sorted(rules_dir.rglob("*.mdc")):
            item = _index_rule(path, root)
            reg.rules[item.id] = item
            reg.by_path[item.path] = item

    if skills_dir.is_dir():
        # Two-pass index: index canonical files normally; for alias files
        # (.cursor/skills/<folder>/SKILL.md where folder is just a redirect),
        # also register the friendly alias folder name so users can request
        # either id. The loader follows the redirect transparently.
        alias_folders: dict[str, str] = {}  # alias folder name -> redirect target path
        for path in skills_dir.rglob("SKILL.md"):
            try:
                head = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            first_line = head.splitlines()[0] if head else ""
            if first_line.lstrip("\ufeff").lower().startswith("# alias:"):
                m = _ALIAS_TARGET_RE.search(head)
                if m:
                    alias_folders[path.parent.name] = m.group(1).strip()
        for path in sorted(skills_dir.rglob("SKILL.md")):
            item = _index_skill(path, root)
            reg.skills[item.id] = item
            reg.by_path[item.path] = item
            # If this folder is an alias, also register it under its raw folder
            # name (e.g. "karpathy-coding") so users can ask for either id.
            if path.parent.name in alias_folders:
                friendly = path.parent.name
                if friendly != item.id and friendly not in reg.skills:
                    friendly_item = RegistryItem(
                        id=friendly,
                        kind="skill",
                        path=item.path,
                        abs_path=item.abs_path,
                        domains=item.domains,
                        triggers=item.triggers,
                        role=item.role,
                        exists=True,
                    )
                    reg.skills[friendly] = friendly_item
                    reg.by_path[friendly_item.path + "#" + friendly] = friendly_item

    if agents_dir.is_dir():
        # Agents may be either one big AGENTS.md or per-agent files
        md_files = sorted(agents_dir.rglob("*.md"))
        for path in md_files:
            for item in _index_agents(path, root):
                reg.agents[item.id] = item
                reg.by_path[item.path] = item

    return reg


def _index_rule(path: Path, root: Path) -> RegistryItem:
    rel = path.relative_to(root).as_posix()
    item_id = path.stem
    domains: list[str] = []
    triggers: list[str] = []
    role = "primary"
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines()[:40]:
            low = line.lower()
            if low.startswith("tags:"):
                tags = [t.strip().strip("[],") for t in line.split(":", 1)[1].split(",")]
                for tag in tags:
                    if tag in DOMAIN_TRIGGERS:
                        domains.extend(DOMAIN_TRIGGERS[tag])
                triggers.extend(tags)
    except OSError:
        pass
    if not domains:
        domains = ["general"]
    return RegistryItem(
        id=item_id,
        kind="rule",
        path=rel,
        abs_path=str(path),
        domains=list(dict.fromkeys(domains)),
        triggers=list(dict.fromkeys(triggers)),
        role=role,
        exists=path.exists(),
    )


def _index_skill(path: Path, root: Path) -> RegistryItem:
    rel = path.relative_to(root).as_posix()
    folder = path.parent.name  # e.g. "ui_frontend-taste"
    item_id = folder.split("_", 1)[-1] if "_" in folder else folder
    domains = list(SKILL_DOMAINS.get(item_id, []))
    triggers: list[str] = []
    role = "primary"
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines()[:80]:
            low = line.lower()
            if "mandatory" in low:
                role = "mandatory"
            elif "overlay" in low:
                role = "overlay"
            elif "secondary" in low:
                role = "secondary"
            # Heuristic: any word with a hyphen in the first 80 lines is treated as a trigger.
            for tok in re.findall(r"[a-z][a-z0-9-]{3,}", low):
                if tok not in triggers and len(tok) <= 40:
                    triggers.append(tok)
    except OSError:
        pass
    if not domains:
        domains = ["general"]
    return RegistryItem(
        id=item_id,
        kind="skill",
        path=rel,
        abs_path=str(path),
        domains=list(dict.fromkeys(domains)),
        triggers=list(dict.fromkeys(triggers))[:40],
        role=role,
        exists=path.exists(),
    )


def _index_agents(path: Path, root: Path) -> list[RegistryItem]:
    """Index agent files.

    Two shapes:
      - `AGENTS.md`: top-level `### <Persona Name>` headings each describe one persona.
      - `agent_<name>.md`: one file = one persona. Do not split on inner `###` layer
        sections (those are review layers, not separate personas).
    """
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    items: list[RegistryItem] = []

    # Per-agent files: one file = one persona.
    if path.stem.startswith("agent_") or path.stem.startswith("agents_") or path.name != "AGENTS.md":
        item_id = _slugify_agent_id(path.stem)
        domains, triggers, role = _parse_agent_frontmatter(text)
        items.append(
            RegistryItem(
                id=item_id,
                kind="agent",
                path=rel,
                abs_path=str(path),
                domains=domains or ["general"],
                triggers=triggers,
                role=role,
                exists=True,
            )
        )
        return items

    # AGENTS.md: split on `### <Title Case Phrase>` headings only.
    sections = re.split(r"(?m)^### ([A-Z][^\n]+)$", text)
    if len(sections) <= 1:
        item_id = _slugify_agent_id(path.stem)
        items.append(
            RegistryItem(
                id=item_id,
                kind="agent",
                path=rel,
                abs_path=str(path),
                domains=["general"],
                triggers=[],
                role="primary",
                exists=True,
            )
        )
        return items
    for i in range(1, len(sections), 2):
        name = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        slug = _slugify_agent_id(name)
        if not slug:
            continue
        domains, triggers, role = _parse_agent_body(name, body)
        items.append(
            RegistryItem(
                id=slug,
                kind="agent",
                path=rel,
                abs_path=str(path),
                domains=domains or ["general"],
                triggers=triggers,
                role=role,
                exists=True,
            )
        )
    return items


def _slugify_agent_id(text: str) -> str:
    """Normalise 'agent_api-security' / 'API Security Auditor Agent' -> 'api-security-auditor'."""
    s = text.strip().lower()
    s = re.sub(r"^agent[_\s]+", "", s)
    s = re.sub(r"\s+agent$", "", s)
    s = re.sub(r"[^a-z0-9-]+", "-", s).strip("-")
    return s


def _parse_agent_frontmatter(text: str) -> tuple[list[str], list[str], str]:
    """Pull YAML-ish fields from the front-matter of an agent_*.md file."""
    domains: list[str] = []
    triggers: list[str] = []
    role = "primary"
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            front = text[3:end]
            for line in front.splitlines():
                line = line.strip()
                if line.startswith("domains:"):
                    raw = line.split(":", 1)[1]
                    domains = [d.strip() for d in re.findall(r"[A-Za-z][A-Za-z0-9_-]*", raw)]
                elif line.startswith("triggers:"):
                    continue  # triggers listed on following lines
                elif line.startswith("role:"):
                    role = line.split(":", 1)[1].strip() or "primary"
                elif line.startswith("-") and triggers is not None:
                    triggers.append(line.lstrip("- ").strip().strip("'\""))
            # Triggers may also appear under triggers: as a block list — collect them.
            in_triggers = False
            for line in front.splitlines():
                if line.strip().startswith("triggers:"):
                    in_triggers = True
                    continue
                if in_triggers:
                    if not line.startswith(" ") and not line.startswith("\t"):
                        in_triggers = False
                        continue
                    tok = line.strip().lstrip("-").strip().strip("'\"")
                    if tok:
                        triggers.append(tok)
    return domains, triggers, role


def _parse_agent_body(name: str, body: str) -> tuple[list[str], list[str], str]:
    domains: list[str] = []
    triggers: list[str] = []
    role = "primary"
    # Domain hints based on persona name keywords.
    lowered = name.lower()
    for keyword, doms in AGENT_DOMAINS.items():
        if keyword in lowered or keyword.replace("-", " ") in lowered:
            domains.extend(doms)
    # Heuristic triggers: pull quoted / hyphen keywords from the first 30 lines.
    for line in body.splitlines()[:30]:
        line = line.strip()
        if line.startswith("-") or line.startswith("*"):
            tok = line.lstrip("-* ").strip().strip("'\"")
            if 3 <= len(tok) <= 40:
                triggers.append(tok)
    return domains, triggers, role


# ---------------------------------------------------------------------- helpers

def find_workspace_root(start: str | os.PathLike[str] = ".") -> str:
    """Walk up from `start` looking for `.cursor/rules`."""
    p = Path(start).resolve()
    for parent in [p, *p.parents]:
        if (parent / ".cursor" / "rules").is_dir():
            return str(parent)
    return str(p)
