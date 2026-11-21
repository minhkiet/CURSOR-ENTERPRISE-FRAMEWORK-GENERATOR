"""Regression tests for multi-tool vibe sync and plugin installation."""

from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from vibe_framework.__main__ import main
from vibe_framework.vibe_sync import DEFAULT_PLUGIN_TOOLS, TOOL_SPECS, VibeSyncEngine, VibeTool


class VibeSyncSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self._tmp.name)
        self.engine = VibeSyncEngine(self.workspace)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _clear_runtime_signals(self) -> dict[str, str]:
        return {
            var: ""
            for spec in TOOL_SPECS.values()
            for var in spec.env_vars
        }

    def _make_plugin_source(self) -> Path:
        source = self.workspace / "plugin-source"
        plugin = source / "demo-plugin"
        plugin.mkdir(parents=True)
        manifest = {
            "name": "demo",
            "main": "index.js",
            "activationEvents": ["onStartupFinished"],
            "contributes": {"commands": []},
        }
        (plugin / "manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        return source

    def test_existing_custom_config_is_not_overwritten_without_force(self) -> None:
        config = self.workspace / ".cursorrules"
        config.write_text("# project-specific rules\n", encoding="utf-8")

        report = self.engine.sync(tools=[VibeTool.CURSOR], force=False)

        self.assertEqual(config.read_text(encoding="utf-8"), "# project-specific rules\n")
        self.assertEqual(report.files_modified[0].action, "skipped")

    def test_force_overwrites_existing_config(self) -> None:
        config = self.workspace / ".cursorrules"
        config.write_text("# stale rules\n", encoding="utf-8")

        report = self.engine.sync(tools=[VibeTool.CURSOR], force=True)

        self.assertIn("Vibe Enterprise Framework", config.read_text(encoding="utf-8"))
        self.assertEqual(report.files_modified[0].action, "updated")

    def test_new_config_reports_created(self) -> None:
        report = self.engine.sync(tools=[VibeTool.CURSOR], force=False)

        self.assertEqual(report.files_modified[0].action, "created")

    def test_plugin_dry_run_does_not_write(self) -> None:
        source = self._make_plugin_source()

        result = self.engine.install_plugins(
            tools=[VibeTool.CURSOR],
            source_dir=source,
            dry_run=True,
        )

        self.assertTrue(result["success"])
        self.assertTrue(result["dry_run"])
        self.assertFalse((self.workspace / ".cursor" / "plugins").exists())
        plugin_result = result["results"]["cursor"]["plugins"][0]
        self.assertEqual(plugin_result["status"], "would_install")

    def test_vscode_plugin_installed_for_editor_runtime(self) -> None:
        source = self._make_plugin_source()

        result = self.engine.install_plugins(
            tools=[VibeTool.CURSOR],
            source_dir=source,
        )

        self.assertEqual(result["results"]["cursor"]["plugins"][0]["status"], "installed")
        self.assertTrue((self.workspace / ".cursor" / "plugins" / "demo-plugin").exists())

    def test_vscode_plugin_skipped_for_agent_runtime(self) -> None:
        source = self._make_plugin_source()

        result = self.engine.install_plugins(
            tools=[VibeTool.CLAUDE_CODE],
            source_dir=source,
        )

        tool_result = result["results"]["claude-code"]
        self.assertEqual(tool_result["status"], "skipped")
        self.assertIn("VS Code", tool_result["reason"])
        self.assertFalse((self.workspace / ".claude" / "plugins").exists())

    def test_adapter_directory_is_not_runtime_active(self) -> None:
        (self.workspace / ".cursor").mkdir()
        (self.workspace / ".claude").mkdir()

        with patch.dict(os.environ, self._clear_runtime_signals()):
            active = self.engine.detector.detect_runtime_tools()

        self.assertEqual(active, [])

    def test_default_plugin_targets_cover_supported_runtimes(self) -> None:
        source = self._make_plugin_source()

        with patch.dict(os.environ, self._clear_runtime_signals()):
            result = self.engine.install_plugins(source_dir=source, dry_run=True)

        expected = {tool.value for tool in DEFAULT_PLUGIN_TOOLS}
        self.assertEqual(set(result["results"]), expected)

    def test_cli_json_reports_failure_with_nonzero_exit(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        missing = self.workspace / "missing-plugins"

        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main([
                "vibe", "install-plugins",
                "--workspace", str(self.workspace),
                "--plugins-dir", str(missing),
                "--tool", "cursor",
                "--json",
            ])

        self.assertEqual(code, 1)
        payload = json.loads(stdout.getvalue())
        self.assertFalse(payload["success"])

    def test_cli_json_dry_run_succeeds(self) -> None:
        source = self._make_plugin_source()
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            code = main([
                "vibe", "install-plugins",
                "--workspace", str(self.workspace),
                "--plugins-dir", str(source),
                "--tool", "cursor",
                "--dry-run",
                "--json",
            ])

        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertTrue(payload["dry_run"])
        self.assertFalse((self.workspace / ".cursor" / "plugins").exists())


if __name__ == "__main__":
    unittest.main()
