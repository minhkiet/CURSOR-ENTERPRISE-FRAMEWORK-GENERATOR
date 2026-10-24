"""
Image Search Skill - Multi-Provider Abstraction Layer

Provides unified image search across multiple providers with:
- Provider fallback (A → B → C → D)
- Deduplication
- Relevance filtering
- Rate limit handling
- Timeout and retry logic

Usage:
    >>> from cursor_framework.skills.image_search import ImageSearchSkill
    >>> skill = ImageSearchSkill()
    >>> results = await skill.search("modern dashboard", limit=20)
    >>> print(f"Found {len(results.images)} images")
"""

import asyncio
import hashlib
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Optional

from .image_providers import (
    ImageProvider,
    ImageResult,
    ImageSearchQuery,
    ImageSearchResponse,
    ImageOrientation,
    ImageLicense,
)
from .image_providers.pexels_provider import PexelsProvider
from .image_providers.unsplash_provider import UnsplashProvider
from .image_providers.pixabay_provider import PixabayProvider


@dataclass
class SearchMetadata:
    """Metadata for a search operation."""
    query: str
    total_providers: int
    successful_providers: int
    failed_providers: list[str]
    total_images_found: int
    deduplicated_count: int
    response_time_ms: float
    cache_hit: bool


@dataclass
class ImageSearchResult:
    """Enhanced search result with metadata."""
    query: str
    images: list[ImageResult]
    metadata: SearchMetadata
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "query": self.query,
            "images": [
                {
                    "url": img.url,
                    "thumbnailUrl": img.thumbnail_url,
                    "width": img.width,
                    "height": img.height,
                    "source": img.source,
                    "sourceUrl": img.source_url,
                    "author": img.author,
                    "authorUrl": img.author_url,
                    "license": img.license.value,
                    "provider": img.provider,
                    "title": img.title,
                    "altText": img.alt_text,
                    "color": img.color,
                    "aspectRatio": round(img.aspect_ratio, 2),
                    "score": round(img.score, 3),
                }
                for img in self.images
            ],
            "metadata": {
                "totalProviders": self.metadata.total_providers,
                "successfulProviders": self.metadata.successful_providers,
                "failedProviders": self.metadata.failed_providers,
                "totalImagesFound": self.metadata.total_images_found,
                "deduplicatedCount": self.metadata.deduplicated_count,
                "responseTimeMs": round(self.metadata.response_time_ms, 2),
                "cacheHit": self.metadata.cache_hit,
            }
        }


class ImageSearchSkill:
    """
    Multi-provider image search skill with fallback, deduplication, and caching.
    
    Features:
    - Automatic provider fallback (tries providers in priority order)
    - Content-based deduplication across providers
    - Relevance scoring and filtering
    - In-memory cache with TTL
    - Rate limit awareness
    - Timeout and retry handling
    
    Provider Priority (lower = tried first):
    1. Unsplash (priority 5) - Best quality, requires API key
    2. Pexels (priority 10) - Good quality, free tier available
    3. Pixabay (priority 15) - Large library, requires API key
    """
    
    DEFAULT_TIMEOUT = 10.0  # seconds per provider
    DEFAULT_RETRIES = 1
    CACHE_TTL = 300  # 5 minutes
    MAX_CACHE_SIZE = 1000
    
    def __init__(
        self,
        pexels_key: Optional[str] = None,
        unsplash_key: Optional[str] = None,
        pixabay_key: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_RETRIES,
    ):
        """Initialize the image search skill with provider API keys."""
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize providers
        self.providers: list[ImageProvider] = []
        
        unsplash = UnsplashProvider(unsplash_key)
        if unsplash.is_available():
            self.providers.append(unsplash)
        
        pexels = PexelsProvider(pexels_key)
        if pexels.is_available():
            self.providers.append(pexels)
        
        pixabay = PixabayProvider(pixabay_key)
        if pixabay.is_available():
            self.providers.append(pixabay)
        
        # Sort by priority (lower = tried first)
        self.providers.sort(key=lambda p: p.priority)
        
        # Cache
        self._cache: deque = deque(maxlen=self.MAX_CACHE_SIZE)
        self._cache_index: dict[str, tuple[datetime, ImageSearchResult]] = {}
    
    def _cache_key(self, query: ImageSearchQuery) -> str:
        """Generate cache key for a query."""
        key_parts = [
            query.query,
            query.orientation.value,
            str(query.min_width or ""),
            str(query.max_width or ""),
            str(query.colors[:2] if query.colors else ""),
            str(query.limit),
            str(query.page),
        ]
        return hashlib.md5("|".join(key_parts).encode()).hexdigest()
    
    def _get_cached(self, query: ImageSearchQuery) -> Optional[ImageSearchResult]:
        """Get cached result if exists and not expired."""
        key = self._cache_key(query)
        if key in self._cache_index:
            cached_time, result = self._cache_index[key]
            if datetime.now() - cached_time < timedelta(seconds=self.CACHE_TTL):
                return result
            else:
                # Remove expired entry
                del self._cache_index[key]
                if key in self._cache:
                    self._cache.remove(key)
        return None
    
    def _set_cached(self, query: ImageSearchQuery, result: ImageSearchResult):
        """Cache a search result."""
        key = self._cache_key(query)
        self._cache_index[key] = (datetime.now(), result)
        self._cache.append(key)
    
    async def _search_provider(
        self,
        provider: ImageProvider,
        query: ImageSearchQuery
    ) -> ImageSearchResponse:
        """Search a single provider with timeout and retry."""
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                async with asyncio.timeout(self.timeout):
                    return await provider.search(query)
            except asyncio.TimeoutError:
                last_error = f"Timeout after {self.timeout}s"
            except Exception as e:
                last_error = str(e)
            
            if attempt < self.max_retries:
                await asyncio.sleep(0.5 * (attempt + 1))  # Exponential backoff
        
        return ImageSearchResponse(
            query=query.query,
            images=[],
            total=0,
            page=query.page,
            pages=0,
            provider=provider.name,
            error=last_error
        )
    
    def _deduplicate(self, images: list[ImageResult]) -> list[ImageResult]:
        """Remove duplicate images based on URL similarity."""
        seen_hashes: set[str] = set()
        unique_images: list[ImageResult] = []
        
        for img in images:
            # Create a hash based on image dimensions and approximate URL
            # This handles cases where same image appears with different URLs
            url_hash = hashlib.md5(
                f"{img.width}x{img.height}|{img.source}".encode()
            ).hexdigest()[:16]
            
            if url_hash not in seen_hashes:
                seen_hashes.add(url_hash)
                unique_images.append(img)
        
        return unique_images
    
    def _rank_images(
        self,
        images: list[ImageResult],
        query: ImageSearchQuery
    ) -> list[ImageResult]:
        """Rank images by relevance to query."""
        query_terms = set(query.query.lower().split())
        
        for img in images:
            score = 1.0
            
            # Boost by title/alt text match
            text = f"{img.title} {img.alt_text}".lower()
            matches = sum(1 for term in query_terms if term in text)
            score += matches * 0.2
            
            # Boost by quality (prefer larger images for most use cases)
            if img.width >= 1920:
                score += 0.3
            elif img.width >= 1280:
                score += 0.2
            elif img.width >= 800:
                score += 0.1
            
            # Boost by aspect ratio (prefer 16:9 for most use cases)
            if 1.5 <= img.aspect_ratio <= 2.0:
                score += 0.2
            
            # Boost by color match if specified
            if query.colors and img.color:
                for color in query.colors:
                    if color.lower() in img.color.lower():
                        score += 0.1
                        break
            
            img.score = min(score, 1.5)  # Cap at 1.5
        
        # Sort by score descending
        return sorted(images, key=lambda img: img.score, reverse=True)
    
    def _filter_by_dimensions(
        self,
        images: list[ImageResult],
        query: ImageSearchQuery
    ) -> list[ImageResult]:
        """Filter images by dimension constraints."""
        filtered = images
        
        if query.min_width:
            filtered = [img for img in filtered if img.width >= query.min_width]
        if query.max_width:
            filtered = [img for img in filtered if img.width <= query.max_width]
        if query.min_height:
            filtered = [img for img in filtered if img.height >= query.min_height]
        if query.max_height:
            filtered = [img for img in filtered if img.height <= query.max_height]
        
        # Aspect ratio filter
        if query.min_aspect_ratio:
            filtered = [
                img for img in filtered
                if img.aspect_ratio >= query.min_aspect_ratio
            ]
        if query.max_aspect_ratio:
            filtered = [
                img for img in filtered
                if img.aspect_ratio <= query.max_aspect_ratio
            ]
        
        return filtered
    
    async def search(
        self,
        query: str,
        limit: int = 20,
        orientation: ImageOrientation = ImageOrientation.ANY,
        min_width: Optional[int] = None,
        max_width: Optional[int] = None,
        min_height: Optional[int] = None,
        max_height: Optional[int] = None,
        colors: Optional[list[str]] = None,
        categories: Optional[list[str]] = None,
        page: int = 1,
        use_cache: bool = True,
    ) -> ImageSearchResult:
        """
        Search for images across all available providers.
        
        Args:
            query: Search query string
            limit: Maximum number of images to return
            orientation: Preferred image orientation
            min_width: Minimum image width
            max_width: Maximum image width
            min_height: Minimum image height
            max_height: Maximum image height
            colors: Preferred colors (hex codes)
            categories: Image categories to search
            page: Page number for pagination
            use_cache: Whether to use cached results
        
        Returns:
            ImageSearchResult with images and metadata
        """
        start_time = time.perf_counter()
        
        # Build query object
        search_query = ImageSearchQuery(
            query=query,
            orientation=orientation,
            min_width=min_width,
            max_width=max_width,
            min_height=min_height,
            max_height=max_height,
            colors=colors or [],
            categories=categories or [],
            limit=limit,
            page=page,
        )
        
        # Check cache
        if use_cache:
            cached = self._get_cached(search_query)
            if cached:
                cached.metadata.cache_hit = True
                return cached
        
        # Collect images from all providers
        all_images: list[ImageResult] = []
        failed_providers: list[str] = []
        successful_providers = 0
        
        # If no providers available, return empty result
        if not self.providers:
            metadata = SearchMetadata(
                query=query,
                total_providers=0,
                successful_providers=0,
                failed_providers=["No providers configured"],
                total_images_found=0,
                deduplicated_count=0,
                response_time_ms=(time.perf_counter() - start_time) * 1000,
                cache_hit=False,
            )
            return ImageSearchResult(
                query=query,
                images=[],
                metadata=metadata,
            )
        
        # Search all providers concurrently
        tasks = [
            self._search_provider(provider, search_query)
            for provider in self.providers
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response in enumerate(responses):
            provider = self.providers[i]
            
            if isinstance(response, Exception):
                failed_providers.append(f"{provider.name}: {str(response)}")
                continue
            
            if response.error:
                failed_providers.append(f"{provider.name}: {response.error}")
                continue
            
            successful_providers += 1
            all_images.extend(response.images)
        
        # Deduplicate
        original_count = len(all_images)
        all_images = self._deduplicate(all_images)
        deduplicated_count = original_count - len(all_images)
        
        # Filter by dimensions
        all_images = self._filter_by_dimensions(all_images, search_query)
        
        # Rank by relevance
        all_images = self._rank_images(all_images, search_query)
        
        # Limit results
        all_images = all_images[:limit]
        
        # Build metadata
        metadata = SearchMetadata(
            query=query,
            total_providers=len(self.providers),
            successful_providers=successful_providers,
            failed_providers=failed_providers,
            total_images_found=len(all_images),
            deduplicated_count=deduplicated_count,
            response_time_ms=(time.perf_counter() - start_time) * 1000,
            cache_hit=False,
        )
        
        result = ImageSearchResult(
            query=query,
            images=all_images,
            metadata=metadata,
        )
        
        # Cache result
        if use_cache:
            self._set_cached(search_query, result)
        
        return result
    
    def get_available_providers(self) -> list[dict]:
        """Get list of configured providers."""
        return [
            {
                "name": p.name,
                "displayName": p.display_name,
                "available": p.is_available(),
                "rateLimitRemaining": p.get_rate_limit_remaining(),
            }
            for p in self.providers
        ]
    
    def clear_cache(self) -> int:
        """Clear the search cache. Returns number of entries cleared."""
        count = len(self._cache_index)
        self._cache.clear()
        self._cache_index.clear()
        return count


# Export main class
__all__ = ["ImageSearchSkill", "ImageSearchResult", "SearchMetadata"]
