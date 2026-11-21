"""
Skills Parser Module

Parses and validates .mdc skill files.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SkillMetadata:
    """Metadata from skill file frontmatter."""

    description: str
    version: str
    tags: list[str] = field(default_factory=list)


@dataclass
class Skill:
    """Parsed skill file."""

    metadata: SkillMetadata
    content: str
    path: Path
    pre_review_sections: list[str] = field(default_factory=list)
    post_review_sections: list[str] = field(default_factory=list)


class SkillsParser:
    """Parser for skill .mdc files."""

    FRONTMATTER_PATTERN = r"^---\n(.*?)\n---\n(.*)$"
    TAG_PATTERN = r"\[([^\]]+)\]"

    def __init__(self):
        """Initialize the parser."""
        self._cache: dict[str, Skill] = {}

    def parse_file(self, path: str | Path) -> Optional[Skill]:
        """
        Parse a skill .mdc file.

        Args:
            path: Path to the skill file

        Returns:
            Parsed Skill or None
        """
        path = Path(path)
        content = path.read_text(encoding="utf-8")

        match = re.match(self.FRONTMATTER_PATTERN, content, re.DOTALL)
        if not match:
            return None

        frontmatter = match.group(1)
        body = match.group(2)

        metadata = self._parse_frontmatter(frontmatter)
        pre_sections = self._extract_sections_by_keyword(body, "Pre-Review")
        post_sections = self._extract_sections_by_keyword(body, "Post-Review")

        return Skill(
            metadata=metadata,
            content=body,
            path=path,
            pre_review_sections=pre_sections,
            post_review_sections=post_sections,
        )

    def _parse_frontmatter(self, text: str) -> SkillMetadata:
        """Parse frontmatter content."""
        metadata = SkillMetadata(
            description="",
            version="",
        )

        for line in text.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip()
                value = value.strip()

                if key == "description":
                    metadata.description = value
                elif key == "version":
                    metadata.version = value
                elif key == "tags":
                    tags = re.findall(self.TAG_PATTERN, value)
                    metadata.tags = tags

        return metadata

    def _extract_sections_by_keyword(
        self, content: str, keyword: str
    ) -> list[str]:
        """Extract sections related to a keyword."""
        sections = []
        in_section = False

        for line in content.split("\n"):
            if keyword in line:
                in_section = True
                continue

            if in_section:
                if line.startswith("## ") or line.startswith("# "):
                    break
                if line.strip() and not line.startswith("-"):
                    sections.append(line.strip())

        return sections

    def parse_skills_directory(
        self, skills_dir: str | Path
    ) -> dict[str, Skill]:
        """
        Parse all skills in a directory.

        Args:
            skills_dir: Directory containing skill files

        Returns:
            Dictionary mapping skill names to parsed skills
        """
        skills_dir = Path(skills_dir)
        skills = {}

        for mdc_file in skills_dir.rglob("SKILL.md"):
            skill = self.parse_file(mdc_file)
            if skill:
                skill_name = mdc_file.parent.name
                skills[skill_name] = skill

        return skills


def create_skills_parser() -> SkillsParser:
    """Factory function to create a SkillsParser."""
    return SkillsParser()
