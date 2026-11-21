"""
Unsplash Image Provider

High-quality photo sharing platform.
API: https://unsplash.com/developers
"""

import os
from typing import Optional
import httpx
from . import ImageProvider, ImageResult, ImageSearchQuery, ImageSearchResponse, ImageOrientation, ImageLicense


class UnsplashProvider(ImageProvider):
    """Unsplash image search provider."""
    
    name = "unsplash"
    display_name = "Unsplash"
    priority = 5  # Highest priority - excellent quality
    
    BASE_URL = "https://api.unsplash.com"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.environ.get("UNSPLASH_API_KEY"))
        self.client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def search(self, query: ImageSearchQuery) -> ImageSearchResponse:
        """Search Unsplash for images."""
        if not self.is_available():
            return ImageSearchResponse(
                query=query.query,
                images=[],
                total=0,
                page=query.page,
                pages=0,
                provider=self.name,
                error="API key not configured"
            )
        
        headers = {
            "Authorization": f"Client-ID {self.api_key}",
            "Accept-Version": "v1"
        }
        
        params = {
            "query": query.query,
            "per_page": min(query.limit, 30),
            "page": query.page,
        }
        
        # Orientation filter
        if query.orientation != ImageOrientation.ANY:
            params["orientation"] = query.orientation.value
        
        # Color filter
        if query.colors:
            params["color"] = query.colors[0]
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/search/photos",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 429:
                    return ImageSearchResponse(
                        query=query.query,
                        images=[],
                        total=0,
                        page=query.page,
                        pages=0,
                        provider=self.name,
                        error="Rate limit exceeded"
                    )
                
                response.raise_for_status()
                data = response.json()
                
                images = [
                    self.normalize_result(photo)
                    for photo in data.get("results", [])
                ]
                
                # Update rate limit info
                self._rate_limit_remaining = int(response.headers.get("X-Ratelimit-Remaining", -1))
                
                return ImageSearchResponse(
                    query=query.query,
                    images=images,
                    total=data.get("total", 0),
                    page=data.get("total_pages", query.page),
                    pages=data.get("total_pages", 1),
                    provider=self.name
                )
                
        except httpx.HTTPError as e:
            return ImageSearchResponse(
                query=query.query,
                images=[],
                total=0,
                page=query.page,
                pages=0,
                provider=self.name,
                error=str(e)
            )
    
    def normalize_result(self, raw_result: dict) -> ImageResult:
        """Normalize Unsplash photo to ImageResult."""
        urls = raw_result.get("urls", {})
        user = raw_result.get("user", {})
        links = raw_result.get("links", {})
        
        return ImageResult(
            url=urls.get("raw", urls.get("full", "")),
            thumbnail_url=urls.get("small", urls.get("thumb", "")),
            width=int(raw_result.get("width", 0)),
            height=int(raw_result.get("height", 0)),
            source="Unsplash",
            source_url=links.get("html", ""),
            author=user.get("name", ""),
            author_url=user.get("links", {}).get("html", ""),
            license=ImageLicense.FREE,
            provider=self.name,
            title=raw_result.get("description") or raw_result.get("alt_description", ""),
            alt_text=raw_result.get("alt_description", ""),
            color=raw_result.get("color", ""),
            aspect_ratio=raw_result.get("width", 1) / max(raw_result.get("height", 1), 1)
        )
    
    def supports_color(self) -> bool:
        return True
    
    def supports_orientation(self, orientation: ImageOrientation) -> bool:
        return True
