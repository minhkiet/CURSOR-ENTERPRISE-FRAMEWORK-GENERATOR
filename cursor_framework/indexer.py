"""
Cursor Asset Indexer Module

Scans `.cursor/` directory and produces a machine-readable index (INDEX.json)
plus a human-readable summary (INDEX.md). Designed for fast lookup, low token
cost, and accurate counts — no hardcoded skill lists.

Features:
    - Single-pass scan of `.cursor/` categories (rules/skills/agents/...)
    - YAML frontmatter parsing (description, version, tags) without PyYAML
    - JSON + Markdown output for both machine and human consumption
    - Optional CLI: `python -m cursor_framework.indexer`

Usage:
    >>> from cursor_framework import Indexer
    >>> idx = Indexer(root=".cursor")
    >>> idx.scan()
    >>> idx.write_json()
    >>> idx.write_markdown()
    >>> idx.stats
    {'rules': 0, 'skills': 50, 'agents': 1, ...}
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# Categories we track. Anything outside this list still appears under "other".
CATEGORIES = (
    "agents",
    "commands",
    "hooks",
    "knowledge",
    "memory",
    "prompts",
    "references",
    "rules",
    "scripts",
    "skills",
    "templates",
    "workflows",
)


@dataclass
class AssetEntry:
    """One indexed file or directory."""

    name: str
    path: str
    category: str
    kind: str  # "file" or "directory"
    description: str = ""
    version: str = ""
    tags: list[str] = field(default_factory=list)
    size_bytes: int = 0


@dataclass
class IndexResult:
    """Full index output."""

    root: str
    scanned_at: str
    categories: dict[str, list[AssetEntry]] = field(default_factory=dict)
    totals: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "scanned_at": self.scanned_at,
            "totals": self.totals,
            "categories": {
                cat: [asdict(e) for e in entries]
                for cat, entries in self.categories.items()
            },
        }


# ponytail: hand-rolled YAML frontmatter parser — avoids PyYAML dep,
# handles the small subset our assets actually use.
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Parse simple YAML frontmatter. Returns lowercase keys."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}

    block = match.group(1)
    out: dict[str, str] = {}
    current_key: Optional[str] = None
    current_list: list[str] = []

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") or line.startswith("- "):
            value = line.lstrip("- ").strip()
            if current_key:
                current_list.append(value.strip('"').strip("'"))
            continue
        if ":" in line:
            if current_key and current_list:
                out[current_key] = ", ".join(current_list)
                current_list = []
            key, _, value = line.partition(":")
            key = key.strip().lower()
            value = value.strip()
            if not value:
                current_key = key
                current_list = []
            else:
                out[key] = value.strip('"').strip("'")
                current_key = None
    if current_key and current_list:
        out[current_key] = ", ".join(current_list)
    return out


def _read_description_from_md(path: Path) -> str:
    """First non-empty paragraph after frontmatter, capped to 200 chars."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

    meta = _parse_frontmatter(text)
    if meta.get("description"):
        return meta["description"][:200]

    body = _FRONTMATTER_RE.sub("", text, count=1)
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        return line[:200]
    return ""


def _entry_from_skill_dir(path: Path, root: Path) -> AssetEntry:
    """Build entry from a skill folder by reading its SKILL.md."""
    skill_md = path / "SKILL.md"
    meta: dict[str, str] = {}
    if skill_md.exists():
        try:
            meta = _parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            meta = {}

    tags_raw = meta.get("tags", "")
    tags = (
        [t.strip().strip("[]") for t in tags_raw.split(",") if t.strip().strip("[]")]
        if tags_raw
        else []
    )

    total_size = 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total_size += child.stat().st_size
            except OSError:
                pass

    return AssetEntry(
        name=path.name,
        path=str(path.relative_to(root)),
        category="skills",
        kind="directory",
        description=meta.get("description", "")[:200],
        version=meta.get("version", ""),
        tags=tags,
        size_bytes=total_size,
    )


def _entry_from_file(path: Path, root: Path, category: str) -> AssetEntry:
    """Build entry from a single file (rule/agent/command/...)."""
    description = ""
    version = ""
    tags: list[str] = []
    if path.suffix in {".md", ".mdc"}:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        meta = _parse_frontmatter(text)
        description = meta.get("description", "")[:200]
        version = meta.get("version", "")
        tags_raw = meta.get("tags", "")
        tags = (
            [t.strip().strip("[]") for t in tags_raw.split(",") if t.strip().strip("[]")]
            if tags_raw
            else []
        )

    try:
        size = path.stat().st_size
    except OSError:
        size = 0

    return AssetEntry(
        name=path.name,
        path=str(path.relative_to(root)),
        category=category,
        kind="file",
        description=description,
        version=version,
        tags=tags,
        size_bytes=size,
    )


class Indexer:
    """Scan `.cursor/` once and emit a machine + human index."""

    def __init__(self, root: str | os.PathLike[str] = ".cursor") -> None:
        self.root = Path(root).resolve()
        self.result = IndexResult(
            root=str(self.root),
            scanned_at=datetime.now().isoformat(timespec="seconds"),
            categories={cat: [] for cat in CATEGORIES},
        )

    def scan(self) -> IndexResult:
        """Walk the root once and populate `result.categories` + `result.totals`."""
        if not self.root.exists():
            raise FileNotFoundError(f"Cursor root not found: {self.root}")

        for cat in CATEGORIES:
            cat_dir = self.root / cat
            if not cat_dir.exists():
                continue

            if cat == "skills":
                for child in sorted(cat_dir.iterdir(), key=lambda p: p.name.lower()):
                    if child.is_dir():
                        self.result.categories[cat].append(
                            _entry_from_skill_dir(child, self.root)
                        )
            else:
                for child in sorted(cat_dir.rglob("*"), key=lambda p: str(p).lower()):
                    if not child.is_file():
                        continue
                    self.result.categories[cat].append(
                        _entry_from_file(child, self.root, cat)
                    )

        # ponytail: derive counts in one pass instead of recomputing per category.
        self.result.totals = {
            cat: len(entries) for cat, entries in self.result.categories.items()
        }
        self.result.totals["grand_total"] = sum(self.result.totals.values())
        return self.result

    def write_json(self, out_path: Optional[str | os.PathLike[str]] = None) -> Path:
        """Persist JSON. Default: `<root>/INDEX.json`."""
        target = Path(out_path) if out_path else self.root / "INDEX.json"
        target.write_text(
            json.dumps(self.result.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return target

    def write_markdown(
        self, out_path: Optional[str | os.PathLike[str]] = None
    ) -> Path:
        """Persist a human-readable summary. Default: `<root>/INDEX.md`."""
        target = Path(out_path) if out_path else self.root / "INDEX.md"
        lines: list[str] = [
            "# Cursor Enterprise Framework - Auto Index",
            "",
            f"> Auto-generated: {self.result.scanned_at}",
            f"> Root: `{self.root}`",
            "",
            "## Totals",
            "",
            "| Category | Count |",
            "|----------|-------|",
        ]
        for cat in CATEGORIES:
            lines.append(f"| {cat} | {self.result.totals.get(cat, 0)} |")
        lines.append(f"| **grand_total** | **{self.result.totals.get('grand_total', 0)}** |")

        for cat in CATEGORIES:
            entries = self.result.categories[cat]
            if not entries:
                continue
            lines += ["", f"## {cat.capitalize()} ({len(entries)})", ""]
            lines += ["| Name | Path | Description |", "|------|------|-------------|"]
            for e in entries:
                desc = e.description.replace("|", "\\|")[:120] if e.description else ""
                lines.append(f"| `{e.name}` | `{e.path}` | {desc} |")

        target.write_text("\n".join(lines), encoding="utf-8")
        return target

    @property
    def stats(self) -> dict[str, int]:
        """Shortcut for tests / callers that just want counts."""
        return dict(self.result.totals)


def main() -> int:
    """CLI entry point: `python -m cursor_framework.indexer [root]`."""
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else ".cursor"
    indexer = Indexer(root=root)
    indexer.scan()
    json_path = indexer.write_json()
    md_path = indexer.write_markdown()
    print(f"Indexed {indexer.stats['grand_total']} assets")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")
    print(f"  Totals: {indexer.stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())