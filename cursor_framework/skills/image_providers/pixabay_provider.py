"""
Pixabay Image Provider

Free image and video platform.
API: https://pixabay.com/api/docs/
"""

import os
from typing import Optional
import httpx
from . import ImageProvider, ImageResult, ImageSearchQuery, ImageSearchResponse, ImageOrientation, ImageLicense


class PixabayProvider(ImageProvider):
    """Pixabay image search provider."""
    
    name = "pixabay"
    display_name = "Pixabay"
    priority = 15  # Medium priority
    
    BASE_URL = "https://pixabay.com/api"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.environ.get("PIXABAY_API_KEY"))
        self.client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def search(self, query: ImageSearchQuery) -> ImageSearchResponse:
        """Search Pixabay for images."""
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
        
        params = {
            "key": self.api_key,
            "q": query.query,
            "per_page": min(query.limit, 200),
            "page": query.page,
            "image_type": "photo",
        }
        
        # Orientation filter
        if query.orientation != ImageOrientation.ANY:
            orientation_map = {
                ImageOrientation.LANDSCAPE: "horizontal",
                ImageOrientation.PORTRAIT: "vertical",
                ImageOrientation.SQUARISH: "vertical",  # Pixabay doesn't have squarish
            }
            params["orientation"] = orientation_map.get(query.orientation, "all")
        
        # Color filter
        if query.colors:
            params["colors"] = ",".join(query.colors[:3])  # Pixabay supports multiple colors
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.BASE_URL,
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
                    self.normalize_result(hit)
                    for hit in data.get("hits", [])
                ]
                
                return ImageSearchResponse(
                    query=query.query,
                    images=images,
                    total=data.get("totalHits", 0),
                    page=query.page,
                    pages=data.get("totalHits", 0) // min(query.limit, 200) + 1,
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
        """Normalize Pixabay hit to ImageResult."""
        return ImageResult(
            url=raw_result.get("largeURL") or raw_result.get("fullHDURL", ""),
            thumbnail_url=raw_result.get("previewURL", ""),
            width=raw_result.get("imageWidth", 0),
            height=raw_result.get("imageHeight", 0),
            source="Pixabay",
            source_url=raw_result.get("pageURL", ""),
            author=raw_result.get("user", ""),
            author_url=f"https://pixabay.com/users/{raw_result.get('user', '')}",
            license=ImageLicense.FREE,
            provider=self.name,
            title=raw_result.get("tags", ""),
            alt_text=raw_result.get("tags", ""),
            color="",
            aspect_ratio=raw_result.get("imageWidth", 1) / max(raw_result.get("imageHeight", 1), 1)
        )
    
    def supports_color(self) -> bool:
        return True
    
    def supports_orientation(self, orientation: ImageOrientation) -> bool:
        return True
