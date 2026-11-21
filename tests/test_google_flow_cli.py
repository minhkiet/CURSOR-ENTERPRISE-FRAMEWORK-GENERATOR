"""Tests for Google Flow image automation helpers."""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.google_flow_cli import (
    DEFAULT_MODEL,
    FLOW_URL,
    build_auto_prompt,
    build_manifest,
    build_project_name,
    open_flow_app,
    parse_args,
    parse_ratio,
    resolve_generation_options,
    size_for_ratio,
    slugify,
    update_asset_index,
    with_ratio,
)


class DummyButton:
    def __init__(self) -> None:
        self.clicked = False

    def click(self) -> None:
        self.clicked = True


class DummyPage:
    def __init__(self) -> None:
        self.goto_urls: list[str] = []
        self.waits: list[int] = []

    def goto(self, url: str, **kwargs: object) -> None:
        self.goto_urls.append(url)

    def wait_for_timeout(self, ms: int) -> None:
        self.waits.append(ms)


class TestGoogleFlowCli(unittest.TestCase):
    def test_resolve_options_from_topic_uses_default_model_and_ratio(self) -> None:
        args = parse_args(["--topic", "Bát tự ngũ hành thập thần", "--dry-run"])

        options = resolve_generation_options(args)

        self.assertEqual(options["model"], DEFAULT_MODEL)
        self.assertEqual(options["ratio"], "1:1")
        self.assertEqual(options["size"], "1024x1024")
        self.assertIn("Bát tự ngũ hành thập thần", options["prompt"])
        self.assertIn("--ar 1:1", options["prompt"])

    def test_parse_ratio_accepts_prompt_markers_and_dimensions(self) -> None:
        self.assertEqual(parse_ratio("hero banner --ar 16:9"), "16:9")
        self.assertEqual(parse_ratio("mobile poster tỷ lệ 9:16"), "9:16")
        self.assertEqual(parse_ratio("ảnh 1920x1080"), "16:9")
        self.assertIsNone(parse_ratio("no ratio here"))

    def test_with_ratio_removes_old_ratio_marker_cleanly(self) -> None:
        prompt = with_ratio("poster event tỷ lệ 9:16, neon style", "9:16")

        self.assertEqual(prompt, "poster event, neon style --ar 9:16")

    def test_explicit_ratio_overrides_prompt_ratio(self) -> None:
        args = parse_args([
            "--topic", "poster", "--ratio", "9:16",
            "--model", "Nano Banana 2.1", "--dry-run",
        ])

        options = resolve_generation_options(args)

        self.assertEqual(options["ratio"], "9:16")
        self.assertEqual(options["size"], "864x1536")
        self.assertIn("--ar 9:16", options["prompt"])

    def test_size_for_ratio_uses_supported_presets(self) -> None:
        self.assertEqual(size_for_ratio("1:1"), "1024x1024")
        self.assertEqual(size_for_ratio("16:9"), "1536x864")
        self.assertEqual(size_for_ratio("4:3"), "1152x864")

    def test_build_auto_prompt_keeps_topic_and_adds_style(self) -> None:
        prompt = build_auto_prompt("bát tự chart", ratio="16:9", style="product")

        self.assertIn("bát tự chart", prompt)
        self.assertIn("premium product photography", prompt)
        self.assertTrue(prompt.endswith("--ar 16:9"))

    def test_open_flow_app_opens_entry_and_waits_for_navigation(self) -> None:
        page = DummyPage()
        button = DummyButton()

        with patch("tools.google_flow_cli.find_button", return_value=button):
            open_flow_app(page, timeout_ms=5000)

        self.assertEqual(page.goto_urls, [FLOW_URL])
        self.assertEqual(page.waits, [1500, 3000])
        self.assertTrue(button.clicked)

    def test_slugify_handles_vietnamese_accents(self) -> None:
        self.assertEqual(
            slugify("Bát tự Ngũ Hành Thập Thần"),
            "bat-tu-ngu-hanh-thap-than",
        )

    def test_build_project_name_uses_system_convention(self) -> None:
        now = datetime(2026, 11, 20, 9, 30, 45, tzinfo=timezone.utc)

        name = build_project_name("Bát tự ngũ hành thập thần", now=now)

        self.assertEqual(name, "flow-bat-tu-ngu-hanh-thap-than-20261120-093045")
        self.assertLessEqual(len(name), 80)

    def test_explicit_project_name_is_slugified_without_timestamp(self) -> None:
        name = build_project_name("ignored", explicit="Bát Tự Demo", now=datetime(2026, 1, 1))

        self.assertEqual(name, "bat-tu-demo")

    def test_build_manifest_matches_asset_pipeline_shape(self) -> None:
        now = datetime(2026, 11, 20, 9, 30, 45, tzinfo=timezone.utc)

        manifest = build_manifest(
            project="flow-demo",
            prompt="bat tu chart",
            source_url="https://flow.google.com/",
            images=[{"name": "hero.png", "path": "public/assets/hero.png", "bytes": 123}],
            now=now,
        )

        self.assertEqual(manifest["project"], "flow-demo")
        self.assertEqual(manifest["source"], "google-flow-ai")
        self.assertEqual(manifest["generated"], "2026-11-20T09:30:45Z")
        self.assertEqual(manifest["assets"][0]["source"], "google-flow-ai")
        self.assertEqual(manifest["assets"][0]["path"], "public/assets/hero.png")

    def test_update_asset_index_dedupes_by_project(self) -> None:
        manifest = build_manifest(
            project="flow-demo",
            prompt="demo",
            source_url="https://flow.google.com/",
            images=[{"name": "a.png", "path": "a.png", "bytes": 1}],
        )

        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "manifest.json"
            update_asset_index(index_path, manifest)
            update_asset_index(index_path, manifest)
            data = json.loads(index_path.read_text(encoding="utf-8"))

        self.assertEqual(len(data["projects"]), 1)
        self.assertEqual(data["projects"][0]["project"], "flow-demo")
        self.assertEqual(data["projects"][0]["assets"][0]["name"], "a.png")


if __name__ == "__main__":
    unittest.main()
