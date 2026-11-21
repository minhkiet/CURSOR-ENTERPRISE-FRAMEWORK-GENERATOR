"""Tests for image-related MCP configuration generation."""

import unittest
from pathlib import Path

from tools.mcp_config_generator import McpConfigGenerator


class TestImageMcpConfig(unittest.TestCase):
    def test_generator_adds_pinterest_server(self):
        repo_root = Path(__file__).resolve().parent.parent
        generator = McpConfigGenerator(str(repo_root), target="cursor")

        generator.add_pinterest()

        server = generator.config.to_dict()["mcpServers"]["pinterest"]
        self.assertEqual(server["command"], generator.python_cmd)
        self.assertTrue(any("pinterest_server.py" in arg for arg in server["args"]))
        self.assertIn("PYTHONPATH", server["env"])


if __name__ == "__main__":
    unittest.main()
