"""
Tests for Pinterest MCP Server and PinterestClient
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from mcp.pinterest_server import (
    PinterestClient,
    search_pins,
    get_board_pins,
    get_user_pins,
    get_pin_details,
    extract_from_url,
    download_images,
    ALLOWED_IMAGE_HOSTS,
)


class TestPinterestClient(unittest.TestCase):
    def setUp(self):
        self.client = PinterestClient()

    def test_build_image_variants_from_thumbnail(self):
        raw = {"236x": {"url": "https://i.pinimg.com/236x/89/60/1a/89601a78a992d2618ba24e7f99417b92.jpg"}}
        variants = self.client._build_image_variants(raw)
        self.assertIn("orig", variants)
        self.assertIn("736x", variants)
        self.assertIn("474x", variants)
        self.assertEqual(
            variants["orig"],
            "https://i.pinimg.com/originals/89/60/1a/89601a78a992d2618ba24e7f99417b92.jpg"
        )
        self.assertEqual(
            variants["736x"],
            "https://i.pinimg.com/736x/89/60/1a/89601a78a992d2618ba24e7f99417b92.jpg"
        )

    def test_resolve_pin_id(self):
        # Pure numeric
        self.assertEqual(self.client.resolve_pin_id("424605071146368277"), "424605071146368277")
        # Full URL with trailing slash
        url1 = "https://www.pinterest.com/pin/424605071146368277/"
        self.assertEqual(self.client.resolve_pin_id(url1), "424605071146368277")
        # URL without trailing slash
        url2 = "https://www.pinterest.com/pin/424605071146368277"
        self.assertEqual(self.client.resolve_pin_id(url2), "424605071146368277")

    def test_download_image_domain_guard(self):
        # Untrusted domain must raise ValueError
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "hack.jpg"
            with self.assertRaises(ValueError) as ctx:
                self.client.download_image("https://malicious-site.com/image.jpg", out_path)
            self.assertIn("Untrusted image domain", str(ctx.exception))


class TestPinterestMcpTools(unittest.TestCase):
    def test_search_pins_tool(self):
        res_str = search_pins(query="minimalist interior", limit=3)
        res = json.loads(res_str)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["query"], "minimalist interior")
        self.assertGreater(len(res["pins"]), 0)
        first_pin = res["pins"][0]
        self.assertTrue(first_pin["image_url"].startswith("http"))
        self.assertIn("all_resolutions", first_pin)

    def test_get_pin_details_tool(self):
        res_str = get_pin_details("424605071146368277")
        res = json.loads(res_str)
        self.assertEqual(res["status"], "success")
        pin = res["pin"]
        self.assertEqual(pin["id"], "424605071146368277")
        self.assertTrue(len(pin["orig_image_url"]) > 0)

    def test_extract_from_url_routing(self):
        # Pin URL
        pin_url = "https://www.pinterest.com/pin/424605071146368277/"
        res_str = extract_from_url(pin_url)
        res = json.loads(res_str)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["type"], "pin")

        # Search URL
        search_url = "https://www.pinterest.com/search/pins/?q=minimalist+logo"
        search_res = json.loads(extract_from_url(search_url, limit=2))
        self.assertEqual(search_res["status"], "success")
        self.assertIn("pins", search_res)

    def test_download_images_path_traversal_guard(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Using valid pinimg domain
            urls = ["https://i.pinimg.com/originals/89/60/1a/89601a78a992d2618ba24e7f99417b92.jpg"]
            res_str = download_images(
                image_urls=urls,
                output_folder=tmpdir,
                filename_prefix="test_pin"
            )
            res = json.loads(res_str)
            self.assertEqual(res["status"], "success")
            self.assertEqual(res["downloaded_count"], 1)
            saved_file = Path(res["downloaded"][0]["path"])
            self.assertTrue(saved_file.exists())
            self.assertGreater(saved_file.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
