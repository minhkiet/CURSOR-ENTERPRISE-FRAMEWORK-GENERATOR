"""
Image Provider Base Interface

Abstract base class for all image search providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class ImageOrientation(Enum):
    """Image orientation filter."""
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARISH = "squarish"
    ANY = "any"


class ImageLicense(Enum):
    """Image license types."""
    COMMERCIAL = "commercial"
    COMMERCIAL_ATTRIBUTION = "commercial_attribution"
    FREE = "free"
    CREATIVE_COMMONS = "creative_commons"
    UNKNOWN = "unknown"


@dataclass
class ImageResult:
    """Single image result from a provider."""
    url: str
    thumbnail_url: str
    width: int
    height: int
    source: str
    source_url: str
    author: str
    author_url: str
    license: ImageLicense
    provider: str
    title: str = ""
    alt_text: str = ""
    color: str = ""
    aspect_ratio: float = field(default=0.0)
    score: float = 1.0
    fetched_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.aspect_ratio == 0 and self.width > 0:
            self.aspect_ratio = self.width / self.height


@dataclass
class ImageSearchQuery:
    """Query parameters for image search."""
    query: str
    orientation: ImageOrientation = ImageOrientation.ANY
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    min_aspect_ratio: Optional[float] = None
    max_aspect_ratio: Optional[float] = None
    colors: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    limit: int = 20
    page: int = 1


@dataclass
class ImageSearchResponse:
    """Response from image search."""
    query: str
    images: list[ImageResult]
    total: int
    page: int
    pages: int
    provider: str
    error: Optional[str] = None
    cached: bool = False
    response_time_ms: float = 0.0


class ImageProvider(ABC):
    """Abstract base class for image search providers."""
    
    name: str = "base"
    display_name: str = "Base Provider"
    priority: int = 100  # Lower = tried first
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._rate_limit_remaining: int = -1
        self._rate_limit_reset: Optional[datetime] = None
    
    @abstractmethod
    async def search(self, query: ImageSearchQuery) -> ImageSearchResponse:
        """Search for images matching the query."""
        pass
    
    @abstractmethod
    def normalize_result(self, raw_result: dict) -> ImageResult:
        """Normalize raw provider result to ImageResult."""
        pass
    
    def is_available(self) -> bool:
        """Check if provider is available (has API key or doesn't need one)."""
        return True
    
    def get_rate_limit_remaining(self) -> int:
        """Get remaining API calls before rate limit."""
        return self._rate_limit_remaining
    
    def supports_orientation(self, orientation: ImageOrientation) -> bool:
        """Check if provider supports orientation filter."""
        return True
    
    def supports_color(self) -> bool:
        """Check if provider supports color filter."""
        return False
    
    def supports_categories(self) -> bool:
        """Check if provider supports category filter."""
        return False
