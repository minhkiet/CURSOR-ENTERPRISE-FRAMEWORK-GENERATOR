#!/usr/bin/env python
"""
Skill Installer Tool

Installs skills from git repositories or local paths.
Supports skill discovery, dependency resolution, and skill management.

Usage:
    python skill_installer.py install --repo owner/repo --skill skill-id
    python skill_installer.py list --available
    python skill_installer.py search "keyword"
    python skill_installer.py uninstall --skill skill-id
"""

import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


@dataclass
class SkillInfo:
    """Skill metadata."""
    id: str
    name: str
    description: str
    path: str
    source: str
    installed: bool = False


class SkillImportError(RuntimeError):
    """Raised when an external skill cannot be imported safely."""


@dataclass(frozen=True)
class GitHubSkillImportResult:
    """Auditable result of an additive GitHub skill import."""

    skill_id: str
    destination: str
    source_repository: str
    source_path: str
    source_ref: str
    content_sha256: str
    provenance_path: str
    status: str


class GitHubSkillImporter:
    """Import one real skill directory from GitHub into the canonical hub.

    The importer is deliberately append-only. It never overwrites an existing
    skill, never deletes a source, and records external provenance separately
    from approval records. Imported content is treated as UTF-8 data, not code
    to execute.
    """

    MAX_FILES = 200
    MAX_FILE_BYTES = 5 * 1024 * 1024
    MAX_TOTAL_BYTES = 20 * 1024 * 1024

    def __init__(
        self,
        workspace_root: Path,
        target_dir: Optional[Path] = None,
        provenance_path: Optional[Path] = None,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.target_dir = (target_dir or self.workspace_root / "vibe-code-framework" / "03-skills").resolve()
        self.provenance_path = (
            provenance_path
            or self.workspace_root
            / "vibe-code-framework"
            / "00-governance"
            / "records"
            / "external-skills.json"
        ).resolve()
        self._opener = opener

        for path, label in ((self.target_dir, "target"), (self.provenance_path, "provenance")):
            if not self._is_within_workspace(path):
                raise SkillImportError(f"{label} must stay inside the workspace: {path}")

    def _is_within_workspace(self, path: Path) -> bool:
        try:
            path.relative_to(self.workspace_root)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_repository(value: str) -> tuple[str, str]:
        """Return validated ``(owner, repository)`` from a GitHub reference."""
        raw = value.strip()
        if raw.startswith("git@github.com:"):
            raw = raw.split(":", 1)[1]
        elif "://" in raw:
            parsed = urlparse(raw)
            if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
                raise SkillImportError("repository URL must use https://github.com")
            raw = parsed.path.lstrip("/")
        raw = raw.rstrip("/")
        if raw.endswith(".git"):
            raw = raw[:-4]
        parts = raw.split("/")
        if len(parts) != 2 or not all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in parts):
            raise SkillImportError("repository must be owner/repository or an HTTPS GitHub URL")
        return parts[0], parts[1]

    @staticmethod
    def normalize_skill_path(value: str) -> str:
        path = value.strip().replace("\\", "/").strip("/")
        if path in ("", "."):
            return ""
        pieces = path.split("/")
        if any(piece in ("", ".", "..") for piece in pieces):
            raise SkillImportError("skill path must be relative and cannot contain . or ..")
        return "/".join(pieces)

    def _request_bytes(self, url: str) -> bytes:
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "cursor-enterprise-framework-skill-importer/1.0",
            },
        )
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            request.add_header("Authorization", f"Bearer {github_token}")
        try:
            with self._opener(request, timeout=30) as response:
                payload = response.read(self.MAX_FILE_BYTES + 1)
        except (HTTPError, URLError, OSError) as exc:
            raise SkillImportError(f"GitHub request failed for {url}: {exc}") from exc
        if len(payload) > self.MAX_FILE_BYTES:
            raise SkillImportError(f"remote file exceeds {self.MAX_FILE_BYTES} bytes: {url}")
        return payload

    def _request_json(self, url: str) -> Any:
        payload = self._request_bytes(url)
        try:
            return json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SkillImportError(f"GitHub returned invalid JSON for {url}") from exc

    def _contents_url(self, owner: str, repo: str, path: str, ref: str) -> str:
        encoded_path = "/".join(quote(part, safe="") for part in path.split("/") if part)
        base = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/contents"
        if encoded_path:
            base += f"/{encoded_path}"
        return f"{base}?ref={quote(ref, safe='')}"

    def _download_url(self, entry: dict[str, Any]) -> str:
        download_url = entry.get("download_url")
        parsed = urlparse(download_url or "")
        if parsed.scheme != "https" or parsed.netloc.lower() != "raw.githubusercontent.com":
            raise SkillImportError("refusing a file download outside raw.githubusercontent.com")
        return download_url

    def _walk(self, owner: str, repo: str, path: str, ref: str, seen: list[dict[str, Any]]) -> None:
        if len(seen) >= self.MAX_FILES:
            raise SkillImportError(f"skill contains more than {self.MAX_FILES} files")
        payload = self._request_json(self._contents_url(owner, repo, path, ref))
        entries = payload if isinstance(payload, list) else [payload]
        for entry in entries:
            if not isinstance(entry, dict):
                raise SkillImportError("GitHub returned an invalid contents entry")
            entry_type = entry.get("type")
            entry_path = entry.get("path")
            if not isinstance(entry_path, str):
                raise SkillImportError("GitHub contents entry has no valid path")
            if entry_type == "dir":
                self._walk(owner, repo, entry_path, ref, seen)
            elif entry_type == "file":
                seen.append(entry)
                if len(seen) > self.MAX_FILES:
                    raise SkillImportError(f"skill contains more than {self.MAX_FILES} files")
            else:
                raise SkillImportError(f"unsupported GitHub entry type: {entry_type}")

    def _resolve_root(self, owner: str, repo: str, skill_path: str, ref: str) -> str:
        if skill_path:
            payload = self._request_json(self._contents_url(owner, repo, skill_path, ref))
            if isinstance(payload, dict) and payload.get("type") == "file":
                if payload.get("name") != "SKILL.md":
                    raise SkillImportError("--skill-path file must be SKILL.md")
                return posixpath.dirname(skill_path)
            if isinstance(payload, list):
                return skill_path
            raise SkillImportError("--skill-path must point to a directory or SKILL.md")

        entries: list[dict[str, Any]] = []
        self._walk(owner, repo, "", ref, entries)
        candidates = sorted(
            posixpath.dirname(entry["path"])
            for entry in entries
            if posixpath.basename(entry["path"]) == "SKILL.md"
        )
        if len(candidates) != 1:
            shown = ", ".join(candidates[:10]) or "none"
            raise SkillImportError(
                "repository must contain exactly one SKILL.md when --skill-path is omitted; "
                f"candidates: {shown}"
            )
        return candidates[0]

    def _read_skill(self, owner: str, repo: str, root: str, ref: str) -> tuple[dict[str, bytes], str]:
        entries: list[dict[str, Any]] = []
        self._walk(owner, repo, root, ref, entries)
        files: dict[str, bytes] = {}
        total = 0
        for entry in entries:
            entry_path = entry["path"]
            prefix = f"{root}/" if root else ""
            if not entry_path.startswith(prefix):
                raise SkillImportError(f"GitHub path escaped skill root: {entry_path}")
            relative = entry_path[len(prefix):]
            if not relative or relative.startswith("/") or ".." in relative.split("/"):
                raise SkillImportError(f"unsafe relative skill path: {relative}")
            payload = self._request_bytes(self._download_url(entry))
            try:
                payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise SkillImportError(f"skill file is not UTF-8 text: {relative}") from exc
            total += len(payload)
            if total > self.MAX_TOTAL_BYTES:
                raise SkillImportError(f"skill exceeds {self.MAX_TOTAL_BYTES} total bytes")
            files[relative] = payload
        if "SKILL.md" not in files:
            raise SkillImportError(f"skill root has no SKILL.md: {root or '/'}")
        return files, root

    @staticmethod
    def _skill_id(content: bytes, fallback: str) -> str:
        text = content.decode("utf-8")
        frontmatter = re.search(r"(?ms)^---\s*\n(.*?)\n---\s*$", text)
        name = ""
        if frontmatter:
            match = re.search(r"(?m)^name:\s*([^\n#]+)", frontmatter.group(1))
            if match:
                name = match.group(1).strip().strip("'\"")
        if not name:
            heading = re.search(r"(?m)^#\s+(.+?)\s*$", text)
            name = heading.group(1).strip() if heading else fallback
        skill_id = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not skill_id:
            raise SkillImportError("could not derive a safe skill id from SKILL.md")
        return skill_id[:80].rstrip("-")

    def _read_provenance(self) -> dict[str, Any]:
        if self.provenance_path.exists():
            try:
                data = json.loads(self.provenance_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise SkillImportError(f"invalid provenance registry: {self.provenance_path}") from exc
        else:
            data = {"schemaVersion": "1.0.0", "records": []}
        if not isinstance(data, dict) or not isinstance(data.get("records"), list):
            raise SkillImportError("provenance registry must contain a records array")
        return data

    @staticmethod
    def _ensure_source_is_new(data: dict[str, Any], record: dict[str, Any]) -> None:
        for existing in data["records"]:
            if not isinstance(existing, dict):
                raise SkillImportError("provenance registry records must be objects")
            if (
                existing.get("sourceRepository") == record["sourceRepository"]
                and existing.get("sourcePath") == record["sourcePath"]
                and existing.get("version") == record["version"]
            ):
                raise SkillImportError("this GitHub skill source/ref is already recorded")

    def _append_provenance(self, record: dict[str, Any]) -> None:
        self.provenance_path.parent.mkdir(parents=True, exist_ok=True)
        data = self._read_provenance()
        self._ensure_source_is_new(data, record)
        data["records"].append(record)
        serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=self.provenance_path.parent, delete=False
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(serialized)
        os.replace(temp_path, self.provenance_path)

    def import_skill(
        self,
        repository: str,
        skill_path: str = "",
        ref: str = "main",
        name: str = "",
        dry_run: bool = False,
    ) -> GitHubSkillImportResult:
        owner, repo = self.parse_repository(repository)
        normalized_path = self.normalize_skill_path(skill_path)
        ref_parts = ref.replace("\\", "/").split("/")
        if not ref or any(part in ("", ".", "..") for part in ref_parts):
            raise SkillImportError("ref must be a non-empty branch or tag name without path traversal")
        root = self._resolve_root(owner, repo, normalized_path, ref)
        files, resolved_root = self._read_skill(owner, repo, root, ref)
        skill_id = (
            re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:80].rstrip("-")
            if name
            else self._skill_id(files["SKILL.md"], posixpath.basename(root) or repo)
        )
        if not skill_id:
            raise SkillImportError("--name produced an empty skill id")
        destination = self.target_dir / skill_id
        if destination.exists():
            raise SkillImportError(f"refusing to overwrite existing skill: {destination}")

        digest = hashlib.sha256()
        for relative in sorted(files):
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(files[relative])
        source_repo = f"{owner}/{repo}"
        record = {
            "resourceId": f"external-skill-{skill_id}",
            "resourceType": "skill",
            "canonicalSource": f"https://github.com/{source_repo}/tree/{ref}/{resolved_root}" if resolved_root else f"https://github.com/{source_repo}/tree/{ref}",
            "sourceType": "SOT-EXTERNAL",
            "owner": "EXTERNAL_OWNER_UNCONFIRMED",
            "maintainer": "PENDING_ASSIGNMENT",
            "consumers": ["vibe-code-framework Resource Hub"],
            "version": ref,
            "sourceRepository": source_repo,
            "sourcePath": resolved_root,
            "contentSha256": digest.hexdigest(),
            "importedAt": datetime.now(timezone.utc).isoformat(),
            "approvalStatus": "NOT_GRANTED",
            "verificationStatus": "PENDING_REVIEW",
            "notes": "Additive import only; no .cursor migration or destructive replacement was performed.",
        }

        if dry_run:
            self._ensure_source_is_new(self._read_provenance(), record)
            return GitHubSkillImportResult(
                skill_id=skill_id,
                destination=str(destination),
                source_repository=source_repo,
                source_path=resolved_root,
                source_ref=ref,
                content_sha256=digest.hexdigest(),
                provenance_path=str(self.provenance_path),
                status="DRY_RUN",
            )

        self.target_dir.mkdir(parents=True, exist_ok=True)
        temp_dir = Path(tempfile.mkdtemp(prefix=f".{skill_id}-", dir=self.target_dir))
        try:
            for relative, payload in files.items():
                output = temp_dir / Path(relative)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(payload)
            try:
                os.rename(temp_dir, destination)
            except FileExistsError as exc:
                raise SkillImportError(f"refusing to overwrite existing skill: {destination}") from exc
        except Exception:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise

        self._append_provenance(record)
        return GitHubSkillImportResult(
            skill_id=skill_id,
            destination=str(destination),
            source_repository=source_repo,
            source_path=resolved_root,
            source_ref=ref,
            content_sha256=digest.hexdigest(),
            provenance_path=str(self.provenance_path),
            status="IMPORTED",
        )


class SkillInstaller:
    """Skill installation and management tool."""
    
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.skills_dir = self.workspace_root / ".agents" / "skills"
        # Do not create a consumer directory merely to inspect or import into
        # the canonical Resource Hub. `install` creates it when needed.
        
        # Predefined skill registry
        self.registry = {
            # Zalo Integration
            "zalo-api": {
                "name": "Zalo API Integration",
                "description": "Zalo API integration for messaging, OA management, and social features",
                "repo": "thaofvn-coca06/zalo-mcp",
                "path": "skills/zalo-api"
            },
            # Telegram Integration
            "telegram-bot": {
                "name": "Telegram Bot",
                "description": "Telegram Bot API integration for chatbots and automation",
                "repo": "mcp-servers/telegram-mcp",
                "path": "skills/telegram-bot"
            },
            # Facebook Integration
            "facebook-api": {
                "name": "Facebook Graph API",
                "description": "Facebook Graph API integration for pages, groups, and marketing",
                "repo": "mcp-servers/facebook-mcp",
                "path": "skills/facebook-api"
            },
            # Google Integration
            "google-api": {
                "name": "Google APIs",
                "description": "Google APIs integration (Gmail, Drive, Calendar, Sheets)",
                "repo": "mcp-servers/google-mcp",
                "path": "skills/google-api"
            },
            # Shopee Integration
            "shopee-api": {
                "name": "Shopee Seller API",
                "description": "Shopee API integration for seller operations and product management",
                "repo": "mcp-servers/shopee-mcp",
                "path": "skills/shopee-api"
            },
            # Cursor Framework
            "cursor-framework": {
                "name": "Cursor Framework",
                "description": "Cursor Enterprise Framework - rules, skills, agents registry",
                "repo": "thaofvn-coca06/2026",
                "path": "cursor_framework"
            },
        }
    
    def list_installed(self) -> list[SkillInfo]:
        """List all installed skills."""
        skills = []
        
        if not self.skills_dir.exists():
            return skills
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skills.append(SkillInfo(
                        id=skill_dir.name,
                        name=skill_dir.name,
                        description="See SKILL.md",
                        path=str(skill_dir),
                        source="local",
                        installed=True
                    ))
        
        return skills
    
    def list_available(self) -> list[SkillInfo]:
        """List all available skills from registry."""
        skills = []
        installed = {s.id for s in self.list_installed()}
        
        for skill_id, info in self.registry.items():
            skills.append(SkillInfo(
                id=skill_id,
                name=info["name"],
                description=info["description"],
                path=info["path"],
                source=info["repo"],
                installed=skill_id in installed
            ))
        
        return skills
    
    def search(self, query: str) -> list[SkillInfo]:
        """Search skills by keyword."""
        query_lower = query.lower()
        all_skills = self.list_available()
        
        return [
            s for s in all_skills
            if query_lower in s.id.lower() 
            or query_lower in s.name.lower()
            or query_lower in s.description.lower()
        ]
    
    def install(self, skill_id: str, force: bool = False) -> bool:
        """Install a skill from registry."""
        if skill_id not in self.registry:
            print(f"ERROR: Skill '{skill_id}' not found in registry")
            print("Available skills:")
            for sid in self.registry:
                print(f"  - {sid}")
            return False
        
        info = self.registry[skill_id]
        dest_dir = self.skills_dir / skill_id
        
        if dest_dir.exists() and not force:
            print(f"Skill '{skill_id}' already installed at {dest_dir}")
            print("Use --force to reinstall")
            return False
        
        # Create skill directory
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Write SKILL.md
        skill_content = f"""# {info['name']}

{info['description']}

## Metadata

- **ID**: {skill_id}
- **Source**: {info['repo']}
- **Installed**: {Path.cwd()}

## Usage

This skill provides integration with {info['name']}.

## Configuration

See official documentation at: https://github.com/{info['repo']}
"""
        
        skill_file = dest_dir / "SKILL.md"
        skill_file.write_text(skill_content, encoding="utf-8")
        
        # Create LICENSE
        license_content = f"""MIT License

Copyright (c) 2026 Cursor Enterprise Framework

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""
        
        (dest_dir / "LICENSE").write_text(license_content, encoding="utf-8")
        
        print(f"Installed {info['name']} to {dest_dir}")
        return True

    def add_from_github(
        self,
        repository: str,
        skill_path: str = "",
        ref: str = "main",
        target_dir: Optional[str] = None,
        name: str = "",
        dry_run: bool = False,
    ) -> GitHubSkillImportResult:
        """Add a GitHub skill to the canonical Resource Hub."""
        resolved_target = (
            (self.workspace_root / target_dir).resolve()
            if target_dir and not Path(target_dir).is_absolute()
            else Path(target_dir).resolve()
            if target_dir
            else self.workspace_root / "vibe-code-framework" / "03-skills"
        )
        importer = GitHubSkillImporter(self.workspace_root, target_dir=resolved_target)
        return importer.import_skill(
            repository, skill_path=skill_path, ref=ref, name=name, dry_run=dry_run
        )
    
    def uninstall(self, skill_id: str) -> bool:
        """Uninstall a skill."""
        skill_dir = self.skills_dir / skill_id
        
        if not skill_dir.exists():
            print(f"Skill '{skill_id}' is not installed")
            return False
        
        # Confirm
        confirm = input(f"Uninstall '{skill_id}'? [y/N] ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return False
        
        shutil.rmtree(skill_dir)
        print(f"Uninstalled {skill_id}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Skill Installer for Cursor Enterprise Framework"
    )
    
    sub = parser.add_subparsers(dest="cmd", help="Commands")
    
    # install
    install = sub.add_parser("install", help="Install a skill")
    install.add_argument("--skill", "-s", required=True, help="Skill ID to install")
    install.add_argument("--force", "-f", action="store_true", help="Force reinstall")

    # add from GitHub
    add_github = sub.add_parser(
        "add-github",
        help="Add one real SKILL.md directory from GitHub to the canonical Resource Hub",
    )
    add_github.add_argument("--repo", required=True, help="GitHub owner/repository or HTTPS URL")
    add_github.add_argument(
        "--skill-path",
        default="",
        help="Repository-relative skill directory or SKILL.md path; omit only when repo has one skill",
    )
    add_github.add_argument("--ref", default="main", help="Branch or tag (default: main)")
    add_github.add_argument(
        "--target",
        default="vibe-code-framework/03-skills",
        help="Workspace-relative destination (default: vibe-code-framework/03-skills)",
    )
    add_github.add_argument("--name", default="", help="Optional destination skill id")
    add_github.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and validate without writing skill files or provenance",
    )
    
    # uninstall
    uninstall = sub.add_parser("uninstall", help="Uninstall a skill")
    uninstall.add_argument("--skill", "-s", required=True, help="Skill ID to uninstall")
    
    # list
    list_parser = sub.add_parser("list", help="List skills")
    list_parser.add_argument("--installed", "-i", action="store_true", help="Show installed only")
    list_parser.add_argument("--available", "-a", action="store_true", help="Show available only")
    
    # search
    search = sub.add_parser("search", help="Search skills")
    search.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    
    installer = SkillInstaller()
    
    if args.cmd == "install":
        success = installer.install(args.skill, args.force)
        return 0 if success else 1

    elif args.cmd == "add-github":
        try:
            result = installer.add_from_github(
                repository=args.repo,
                skill_path=args.skill_path,
                ref=args.ref,
                target_dir=args.target,
                name=args.name,
                dry_run=args.dry_run,
            )
        except SkillImportError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
        return 0
    
    elif args.cmd == "uninstall":
        success = installer.uninstall(args.skill)
        return 0 if success else 1
    
    elif args.cmd == "list":
        if args.installed:
            skills = installer.list_installed()
            print("=== Installed Skills ===")
        elif args.available:
            skills = installer.list_available()
            print("=== Available Skills ===")
        else:
            skills = installer.list_available()
            print("=== All Skills ===")
        
        for s in skills:
            status = "✓" if s.installed else "○"
            print(f"{status} {s.id}")
            print(f"   {s.name}")
            print(f"   {s.description}")
            print()
        return 0
    
    elif args.cmd == "search":
        skills = installer.search(args.query)
        if not skills:
            print(f"No skills found matching '{args.query}'")
            return 1
        
        print(f"=== Search Results for '{args.query}' ===")
        for s in skills:
            status = "✓" if s.installed else "○"
            print(f"{status} {s.id} - {s.name}")
        return 0
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
