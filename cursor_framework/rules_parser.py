"""
Rules Parser Module

Parses and validates .mdc rule files.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RuleMetadata:
    """Metadata from rule file frontmatter."""

    description: str
    created: str
    version: str
    tags: list[str] = field(default_factory=list)


@dataclass
class Rule:
    """Parsed rule file."""

    metadata: RuleMetadata
    content: str
    path: Path
    sections: list[str] = field(default_factory=list)


class RulesParser:
    """Parser for .mdc rule files."""

    FRONTMATTER_PATTERN = r"^---\n(.*?)\n---\n(.*)$"
    TAG_PATTERN = r"\[([^\]]+)\]"

    def __init__(self):
        """Initialize the parser."""
        self._cache: dict[str, Rule] = {}

    def parse_file(self, path: str | Path) -> Optional[Rule]:
        """
        Parse a .mdc rule file.

        Args:
            path: Path to the rule file

        Returns:
            Parsed Rule or None
        """
        path = Path(path)
        content = path.read_text(encoding="utf-8")

        match = re.match(self.FRONTMATTER_PATTERN, content, re.DOTALL)
        if not match:
            return None

        frontmatter = match.group(1)
        body = match.group(2)

        metadata = self._parse_frontmatter(frontmatter)
        sections = self._extract_sections(body)

        return Rule(
            metadata=metadata,
            content=body,
            path=path,
            sections=sections,
        )

    def _parse_frontmatter(self, text: str) -> RuleMetadata:
        """Parse frontmatter YAML-like content."""
        metadata = RuleMetadata(
            description="",
            created="",
            version="",
        )

        for line in text.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip()
                value = value.strip()

                if key == "description":
                    metadata.description = value
                elif key == "created":
                    metadata.created = value
                elif key == "version":
                    metadata.version = value
                elif key == "tags":
                    tags = re.findall(self.TAG_PATTERN, value)
                    metadata.tags = tags

        return metadata

    def _extract_sections(self, content: str) -> list[str]:
        """Extract section headers from content."""
        pattern = r"^##?\s+(.+)$"
        sections = []

        for line in content.split("\n"):
            match = re.match(pattern, line)
            if match:
                sections.append(match.group(1))

        return sections

    def find_rules_by_tag(self, rules_dir: str | Path, tag: str) -> list[Path]:
        """
        Find rules matching a tag.

        Args:
            rules_dir: Directory containing rule files
            tag: Tag to search for

        Returns:
            List of matching rule paths
        """
        rules_dir = Path(rules_dir)
        matches = []

        for mdc_file in rules_dir.rglob("*.mdc"):
            rule = self.parse_file(mdc_file)
            if rule and tag in rule.metadata.tags:
                matches.append(mdc_file)

        return matches


def create_parser() -> RulesParser:
    """Factory function to create a RulesParser."""
    return RulesParser()
