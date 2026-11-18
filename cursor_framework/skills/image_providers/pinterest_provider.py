"""
Pinterest Image Provider
========================
Searches and extracts high-resolution images from Pinterest without requiring API keys.
"""

from __future__ import annotations

import asyncio
from typing import Optional

from mcp.pinterest_server import PinterestClient
from . import (
    ImageProvider,
    ImageResult,
    ImageSearchQuery,
    ImageSearchResponse,
    ImageOrientation,
    ImageLicense,
)


class PinterestProvider(ImageProvider):
    """Pinterest image search provider."""

    name = "pinterest"
    display_name = "Pinterest"
    priority = 6  # High priority, rich inspirational and aesthetic images

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.client = PinterestClient()

    def is_available(self) -> bool:
        # Pinterest provider runs without requiring an API key
        return True

    def normalize_result(self, raw_result: dict) -> ImageResult:
        """Normalize raw pin dictionary to ImageResult."""
        orig_url = raw_result.get("orig_image_url") or raw_result.get("images", {}).get("orig") or ""
        thumb_url = raw_result.get("images", {}).get("236x") or orig_url
        pinner = raw_result.get("pinner", {}) or {}

        return ImageResult(
            url=orig_url,
            thumbnail_url=thumb_url,
            width=736,
            height=1000,
            source="pinterest",
            source_url=raw_result.get("pin_url", "https://www.pinterest.com/"),
            author=pinner.get("full_name") or pinner.get("username") or "Pinterest User",
            author_url=pinner.get("profile_url", "https://www.pinterest.com/"),
            license=ImageLicense.UNKNOWN,
            provider=self.name,
            title=raw_result.get("title", ""),
            alt_text=raw_result.get("description", ""),
            color=raw_result.get("dominant_color", ""),
        )

    async def search(self, query: ImageSearchQuery) -> ImageSearchResponse:
        """Search Pinterest for pins and return high-resolution images."""
        loop = asyncio.get_event_loop()
        try:
            # Run the synchronous scraper in threadpool to keep async clean
            raw_pins = await loop.run_in_executor(
                None,
                lambda: self.client.search_pins(query=query.query, limit=query.limit)
            )

            images = []
            for pin in raw_pins:
                img_res = self.normalize_result(pin)
                if img_res.url:
                    images.append(img_res)

            return ImageSearchResponse(
                query=query.query,
                images=images,
                total=len(images),
                page=query.page,
                pages=1,
                provider=self.name,
            )
        except Exception as e:
            return ImageSearchResponse(
                query=query.query,
                images=[],
                total=0,
                page=query.page,
                pages=0,
                provider=self.name,
                error=str(e),
            )
