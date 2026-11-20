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
    search_videos,
    get_pin_video,
    download_video,
    ALLOWED_IMAGE_HOSTS,
    ALLOWED_VIDEO_HOSTS,
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

    def test_download_video_domain_guard(self):
        # Untrusted domain must raise ValueError
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "hack.mp4"
            with self.assertRaises(ValueError) as ctx:
                self.client.download_video("https://malicious-site.com/video.mp4", out_path)
            self.assertIn("Untrusted video domain", str(ctx.exception))

    def test_extract_video_info_formats(self):
        mock_item = {
            "videos": {
                "video_list": {
                    "V_EXP3": {
                        "url": "https://v1.pinimg.com/videos/mc/expMp4/abc_t1.mp4",
                        "width": 720,
                        "height": 1280,
                        "duration": 15000,
                        "thumbnail": "https://i.pinimg.com/thumb.jpg",
                    },
                    "V_HLSV4": {
                        "url": "https://v1.pinimg.com/videos/mc/hls/abc.m3u8",
                        "width": 720,
                        "height": 1280,
                        "duration": 15000,
                        "thumbnail": "https://i.pinimg.com/thumb.jpg",
                    }
                }
            }
        }
        vinfo = self.client._extract_video_info(mock_item)
        self.assertIsNotNone(vinfo)
        self.assertTrue(vinfo["has_video"])
        self.assertEqual(vinfo["duration_seconds"], 15.0)
        self.assertIn("V_EXP3", vinfo["formats"])
        self.assertTrue(vinfo["best_video_url"].endswith(".mp4"))



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

    def test_search_videos_tool(self):
        res_str = search_videos(query="motion graphic", limit=2)
        res = json.loads(res_str)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["query"], "motion graphic")
        self.assertGreaterEqual(len(res["videos"]), 1)
        first_video = res["videos"][0]
        self.assertIn("video", first_video)
        self.assertTrue(first_video["video"]["has_video"])
        self.assertTrue(first_video["video"]["best_video_url"].startswith("http"))

    def test_get_pin_video_non_video_pin(self):
        # Existing test pin is an image pin
        res_str = get_pin_video("424605071146368277")
        res = json.loads(res_str)
        self.assertEqual(res["status"], "not_found")
        self.assertIn("does not contain video streams", res["message"])


    def test_download_video_guard_tool(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            res_str = download_video("https://untrusted-domain.com/vid.mp4", output_folder=tmpdir)
            res = json.loads(res_str)
            self.assertEqual(res["status"], "error")
            self.assertIn("Untrusted video domain", res["message"])

    def test_download_video_mocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "video.mp4")
            fake_bytes = b"\x00\x00\x00 ftypiso6" + b"A" * 1024
            mock_resp = MagicMock()
            mock_resp.headers = {"Content-Length": str(len(fake_bytes))}
            mock_resp.read.side_effect = [fake_bytes, b""]
            mock_resp.__enter__.return_value = mock_resp

            with patch("urllib.request.urlopen", return_value=mock_resp):
                res_str = download_video(
                    "https://v1.pinimg.com/videos/mc/test.mp4",
                    output_folder=tmpdir,
                    filename="video.mp4"
                )
                res = json.loads(res_str)
                self.assertEqual(res["status"], "success")
                self.assertEqual(res["downloaded"]["size_bytes"], len(fake_bytes))
                self.assertTrue(os.path.exists(out_file))
                self.assertEqual(os.path.getsize(out_file), len(fake_bytes))



if __name__ == "__main__":
    unittest.main()
