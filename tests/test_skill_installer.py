"""Tests for the append-only GitHub skill importer."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.skill_installer import GitHubSkillImporter, SkillImportError


class _Response:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _limit: int = -1) -> bytes:
        return self.payload


def _fake_opener(request, timeout=30):
    assert timeout == 30
    url = request.full_url
    if "/contents/skills/demo?ref=main" in url:
        return _Response(
            json.dumps(
                [
                    {
                        "type": "file",
                        "path": "skills/demo/SKILL.md",
                        "name": "SKILL.md",
                        "download_url": "https://raw.githubusercontent.com/acme/framework/main/skills/demo/SKILL.md",
                    },
                    {
                        "type": "dir",
                        "path": "skills/demo/references",
                        "name": "references",
                    },
                ]
            ).encode()
        )
    if "/contents/skills/demo/references?ref=main" in url:
        return _Response(
            json.dumps(
                [
                    {
                        "type": "file",
                        "path": "skills/demo/references/guide.md",
                        "name": "guide.md",
                        "download_url": "https://raw.githubusercontent.com/acme/framework/main/skills/demo/references/guide.md",
                    }
                ]
            ).encode()
        )
    if url.endswith("/skills/demo/SKILL.md"):
        return _Response(b"---\nname: github-demo\n---\n\n# Demo\n")
    if url.endswith("/skills/demo/references/guide.md"):
        return _Response(b"# Guide\n")
    raise AssertionError(f"unexpected URL: {url}")


def test_imports_real_skill_and_records_external_provenance(tmp_path: Path):
    importer = GitHubSkillImporter(tmp_path, opener=_fake_opener)

    result = importer.import_skill("https://github.com/acme/framework", "skills/demo")

    destination = tmp_path / "vibe-code-framework" / "03-skills" / "github-demo"
    assert result.skill_id == "github-demo"
    assert (destination / "SKILL.md").read_text(encoding="utf-8").startswith("---")
    assert (destination / "references" / "guide.md").exists()

    provenance = json.loads(result.provenance_path and Path(result.provenance_path).read_text(encoding="utf-8"))
    assert len(provenance["records"]) == 1
    assert provenance["records"][0]["sourceType"] == "SOT-EXTERNAL"
    assert provenance["records"][0]["approvalStatus"] == "NOT_GRANTED"


def test_importer_refuses_overwrite(tmp_path: Path):
    destination = tmp_path / "vibe-code-framework" / "03-skills" / "github-demo"
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text("existing", encoding="utf-8")
    importer = GitHubSkillImporter(tmp_path, opener=_fake_opener)

    with pytest.raises(SkillImportError, match="overwrite"):
        importer.import_skill("acme/framework", "skills/demo")


def test_importer_dry_run_does_not_write(tmp_path: Path):
    importer = GitHubSkillImporter(tmp_path, opener=_fake_opener)

    result = importer.import_skill("acme/framework", "skills/demo", dry_run=True)

    assert result.status == "DRY_RUN"
    assert not (tmp_path / "vibe-code-framework" / "03-skills" / "github-demo").exists()
    assert not Path(result.provenance_path).exists()


def test_repository_and_path_validation():
    assert GitHubSkillImporter.parse_repository("acme/framework.git") == ("acme", "framework")
    with pytest.raises(SkillImportError):
        GitHubSkillImporter.parse_repository("https://example.com/acme/framework")
    with pytest.raises(SkillImportError):
        GitHubSkillImporter.normalize_skill_path("skills/../secret")
