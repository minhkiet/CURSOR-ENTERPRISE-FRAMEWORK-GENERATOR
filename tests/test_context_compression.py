"""Regression tests for skill-aware context compression."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vibe_framework.context_builder import ContextBuilder


def _skill_text(name: str) -> str:
    repeated = "- Keep layout calm readable clear hierarchy alpha beta gamma delta\n"
    return (
        "# Taste Frontend Skill\n\n"
        "## Section\n\n"
        "```css\n"
        "color: red;\n"
        "```\n\n"
        + repeated * 80
        + f"END {name}\n"
    )


class ContextCompressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        root = self.base / ".cursor"
        for name in ("ui_frontend-taste", "ui_frontend-redesign"):
            skill_dir = root / "skills" / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(_skill_text(name), encoding="utf-8")
        self.root = root

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_compression_keeps_one_complete_skill_block(self) -> None:
        cb = ContextBuilder(root=self.root, max_tokens=2000)
        result = cb.build("redesign landing page", max_skills=2)

        self.assertTrue(result.truncated)
        self.assertLessEqual(result.tokens, 2000)
        self.assertEqual(result.text.count("## Skill:"), 1)
        self.assertEqual(result.text.count("## Section"), 1)
        self.assertNotIn("## Summary", result.text)
        self.assertEqual(result.text.count("```") % 2, 0)
        self.assertTrue(
            "END ui_frontend-taste" in result.text
            or "END ui_frontend-redesign" in result.text
        )
        self.assertEqual(result.skill_count, 1)
        self.assertEqual(len(result.skills_used), 1)


if __name__ == "__main__":
    unittest.main()
