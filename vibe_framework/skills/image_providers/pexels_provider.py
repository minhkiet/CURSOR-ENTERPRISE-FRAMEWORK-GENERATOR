"""
Pexels Image Provider

Free image search provider with high-quality photos.
API: https://www.pexels.com/api/
"""

import os
from typing import Optional
import httpx
from . import ImageProvider, ImageResult, ImageSearchQuery, ImageSearchResponse, ImageOrientation, ImageLicense


class PexelsProvider(ImageProvider):
    """Pexels image search provider."""
    
    name = "pexels"
    display_name = "Pexels"
    priority = 10  # High priority - good free tier
    
    BASE_URL = "https://api.pexels.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.environ.get("PEXELS_API_KEY"))
        self.client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def search(self, query: ImageSearchQuery) -> ImageSearchResponse:
        """Search Pexels for images."""
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
            "Authorization": self.api_key
        }
        
        params = {
            "query": query.query,
            "per_page": min(query.limit, 80),
            "page": query.page,
        }
        
        # Orientation filter
        if query.orientation != ImageOrientation.ANY:
            orientation_map = {
                ImageOrientation.LANDSCAPE: "landscape",
                ImageOrientation.PORTRAIT: "portrait",
                ImageOrientation.SQUARISH: "squarish",
            }
            params["orientation"] = orientation_map.get(query.orientation, "landscape")
        
        # Color filter
        if query.colors:
            params["color"] = query.colors[0]  # Pexels only supports one color
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/search",
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
                    for photo in data.get("photos", [])
                ]
                
                # Filter by dimensions if specified
                if query.min_width:
                    images = [img for img in images if img.width >= query.min_width]
                if query.max_width:
                    images = [img for img in images if img.width <= query.max_width]
                if query.min_height:
                    images = [img for img in images if img.height >= query.min_height]
                if query.max_height:
                    images = [img for img in images if img.height <= query.max_height]
                
                # Update rate limit info
                if "X-RateLimit-Remaining" in response.headers:
                    self._rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
                
                return ImageSearchResponse(
                    query=query.query,
                    images=images,
                    total=data.get("total_results", 0),
                    page=data.get("page", query.page),
                    pages=data.get("total_results", 0) // min(query.limit, 80) + 1,
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
        """Normalize Pexels photo to ImageResult."""
        src = raw_result.get("src", {})
        return ImageResult(
            url=src.get("original", src.get("large2x", "")),
            thumbnail_url=src.get("tiny", src.get("medium", "")),
            width=raw_result.get("width", 0),
            height=raw_result.get("height", 0),
            source="Pexels",
            source_url=raw_result.get("url", ""),
            author=raw_result.get("photographer", ""),
            author_url=raw_result.get("photographer_url", ""),
            license=ImageLicense.FREE,
            provider=self.name,
            title=raw_result.get("alt", ""),
            alt_text=raw_result.get("alt", ""),
            color=raw_result.get("avg_color", ""),
            aspect_ratio=raw_result.get("width", 1) / max(raw_result.get("height", 1), 1)
        )
    
    def supports_color(self) -> bool:
        return True
    
    def supports_orientation(self, orientation: ImageOrientation) -> bool:
        return True
