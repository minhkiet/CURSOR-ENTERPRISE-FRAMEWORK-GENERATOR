"""
Pinterest MCP Server
====================
Model Context Protocol (MCP) server for searching, browsing, extracting, and downloading
high-resolution images from Pinterest (https://www.pinterest.com/).

Provides tools for:
- Searching pins by keyword with full image resolutions (orig, 736x, 474x, 236x)
- Extracting pins from user profiles and boards
- Resolving pin details and metadata by ID or URL (including pin.it short links)
- Smart URL routing (pin, board, user, search)
- Safe, verified image downloading with SSRF and path-traversal guards

Usage:
    python pinterest_server.py
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import logging
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add paths to sys.path
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

_mcp_dir = Path(__file__).resolve().parent
if str(_mcp_dir) not in sys.path:
    sys.path.insert(0, str(_mcp_dir))

# Logger setup (stderr only - stdout is reserved for MCP JSON-RPC protocol)
logger = logging.getLogger("pinterest_mcp")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# MCP server import
try:
    from mcp.server.fastmcp import FastMCP
except Exception:
    try:
        from fastmcp import FastMCP
    except Exception:
        try:
            from mcp_runtime import UniversalMcpServer as FastMCP
        except ImportError:
            from cursor_framework.mcp_runtime import UniversalMcpServer as FastMCP

mcp = FastMCP("pinterest")

# Constants
DEFAULT_TIMEOUT = 20
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024  # 25 MB max
ALLOWED_IMAGE_HOSTS = (
    "pinimg.com",
    "i.pinimg.com",
    "s-media-cache-ak0.pinimg.com",
    "pinterest.com",
    "www.pinterest.com",
)
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


class PinterestClient:
    """
    Core Pinterest scraper and API client using standard library only.
    Zero external dependencies required.
    """

    BASE_URL = "https://www.pinterest.com"
    WIDGETS_URL = "https://widgets.pinterest.com"

    def __init__(self, user_agent: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT):
        self.user_agent = user_agent or DEFAULT_USER_AGENT
        self.timeout = timeout
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self._warmed_up = False

    def _get_headers(self, source_url: str = "/", is_xhr: bool = False) -> Dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"{self.BASE_URL}/",
            "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        }
        if is_xhr:
            headers.update({
                "Host": "www.pinterest.com",
                "Accept": "application/json, text/javascript, */*, q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "X-Pinterest-AppState": "active",
                "X-Pinterest-Pws-Handler": "www/search/[scope].js",
                "X-Pinterest-Source-Url": source_url,
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
            })
        else:
            headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            })
        return headers

    def _warmup_search(self, query: str) -> None:
        """Establish session cookies for Pinterest search queries."""
        if self._warmed_up and len(self.cookie_jar) > 0:
            return
        source_url = f"/search/pins/?q={urllib.parse.quote(query)}&rs=typed"
        warmup_req = urllib.request.Request(
            f"{self.BASE_URL}{source_url}",
            headers=self._get_headers(source_url, is_xhr=False)
        )
        try:
            with self.opener.open(warmup_req, timeout=self.timeout) as resp:
                resp.read(4096)  # Read small chunk to process set-cookie
            self._warmed_up = True
        except Exception as e:
            logger.warning(f"Pinterest warm-up request warning: {e}")

    @staticmethod
    def _build_image_variants(raw_images: Dict[str, Any], raw_url: Optional[str] = None) -> Dict[str, str]:
        """Derive standard image resolution URLs (orig, 736x, 474x, 236x)."""
        variants: Dict[str, str] = {}
        if isinstance(raw_images, dict):
            for key, val in raw_images.items():
                if isinstance(val, dict) and "url" in val:
                    variants[key] = val["url"]
                elif isinstance(val, str):
                    variants[key] = val

        # If original is missing but another resolution exists, upgrade it
        candidate_url = variants.get("orig") or variants.get("originals") or raw_url
        if not candidate_url:
            for size_key in ("736x", "564x", "474x", "236x", "170x"):
                if size_key in variants:
                    candidate_url = variants[size_key]
                    break

        if candidate_url and ("originals" not in variants and "orig" not in variants):
            orig_url = re.sub(r'/(?:\d+x)/', '/originals/', candidate_url)
            variants["orig"] = orig_url
            variants["originals"] = orig_url

        if "orig" in variants and "736x" not in variants:
            variants["736x"] = re.sub(r'/originals/', '/736x/', variants["orig"])
        if "orig" in variants and "474x" not in variants:
            variants["474x"] = re.sub(r'/originals/', '/474x/', variants["orig"])
        if "orig" in variants and "236x" not in variants:
            variants["236x"] = re.sub(r'/originals/', '/236x/', variants["orig"])

        return variants

    def search_pins(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search Pinterest pins by keyword.
        Returns a list of structured pin records.
        """
        self._warmup_search(query)
        source_url = f"/search/pins/?q={urllib.parse.quote(query)}&rs=typed"

        payload = {
            "options": {
                "applied_unified_filters": None,
                "appliedProductFilters": "---",
                "article": None,
                "auto_correction_disabled": False,
                "corpus": None,
                "customized_rerank_type": None,
                "domains": None,
                "filters": None,
                "journey_depth": None,
                "page_size": str(min(max(limit, 1), 50)),
                "price_max": None,
                "price_min": None,
                "query_pin_sigs": None,
                "query": urllib.parse.quote(query),
                "redux_normalize_feed": True,
                "request_params": None,
                "rs": "typed",
                "scope": "pins",
                "selected_one_bar_modules": None,
                "source_id": None,
                "source_module_id": None,
                "seoDrawerEnabled": False,
                "source_url": urllib.parse.quote_plus(source_url),
                "top_pin_id": None,
                "top_pin_ids": None,
            },
            "context": {},
        }

        encoded = urllib.parse.quote_plus(json.dumps(payload).replace(" ", ""))
        encoded = (
            encoded.replace("%2520", "%20")
            .replace("%252F", "%2F")
            .replace("%253F", "%3F")
            .replace("%252520", "%2520")
            .replace("%253D", "%3D")
            .replace("%2526", "%26")
        )

        time_epoch = int(time.time() * 1000)
        api_url = (
            f"{self.BASE_URL}/resource/BaseSearchResource/get/"
            f"?source_url={urllib.parse.quote_plus(source_url)}&data={encoded}&_={time_epoch}"
        )

        headers = self._get_headers(source_url=source_url, is_xhr=True)
        req = urllib.request.Request(api_url, headers=headers)

        with self.opener.open(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        raw_results = data.get("resource_response", {}).get("data", {}).get("results", [])
        pins: List[Dict[str, Any]] = []

        for item in raw_results:
            pin_id = str(item.get("id") or "")
            if not pin_id:
                continue

            images_dict = self._build_image_variants(item.get("images", {}))
            
            # Check story_pin_data if standard images are missing
            if not images_dict.get("orig") and "story_pin_data" in item:
                pages = item.get("story_pin_data", {}).get("pages", [])
                for page in pages:
                    p_imgs = page.get("image_adjusted", {}).get("images", {})
                    p_variants = self._build_image_variants(p_imgs)
                    if p_variants.get("orig"):
                        images_dict = p_variants
                        break

            orig_url = images_dict.get("orig") or images_dict.get("736x") or ""
            # Only include pins that have a valid image URL
            if not orig_url:
                continue

            title = item.get("title") or item.get("grid_title") or item.get("heading") or ""
            desc = item.get("description") or ""
            dominant_color = item.get("dominant_color") or ""
            pinner = item.get("pinner", {}) or {}
            pinner_info = {
                "username": pinner.get("username", ""),
                "full_name": pinner.get("full_name", ""),
                "profile_url": f"https://www.pinterest.com/{pinner.get('username', '')}/" if pinner.get("username") else "",
            }

            pins.append({
                "id": pin_id,
                "title": title,
                "description": desc,
                "pin_url": f"https://www.pinterest.com/pin/{pin_id}/",
                "dominant_color": dominant_color,
                "images": images_dict,
                "orig_image_url": orig_url,
                "pinner": pinner_info,
            })

            if len(pins) >= limit:
                break

        return pins

    def get_board_pins(self, username: str, board: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Fetch pins from a user's board via the official widget endpoint.
        """
        clean_user = username.strip().strip("/")
        clean_board = board.strip().strip("/")
        api_url = f"{self.WIDGETS_URL}/v3/pidgets/boards/{clean_user}/{clean_board}/pins/"

        req = urllib.request.Request(api_url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        raw_pins = data.get("data", {}).get("pins", [])
        pins: List[Dict[str, Any]] = []

        for item in raw_pins:
            pin_id = str(item.get("id") or "")
            images_dict = self._build_image_variants(item.get("images", {}))
            title = item.get("title") or item.get("description") or ""
            desc = item.get("description") or ""
            pinner = item.get("pinner", {}) or {}

            pins.append({
                "id": pin_id,
                "title": title,
                "description": desc,
                "pin_url": f"https://www.pinterest.com/pin/{pin_id}/" if pin_id else "",
                "dominant_color": item.get("dominant_color") or "",
                "images": images_dict,
                "orig_image_url": images_dict.get("orig") or images_dict.get("736x") or "",
                "pinner": {
                    "username": pinner.get("username", clean_user),
                    "full_name": pinner.get("full_name", ""),
                },
            })

            if len(pins) >= limit:
                break

        return pins

    def get_user_pins(self, username: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Fetch recent pins from a user profile via the official widget endpoint.
        """
        clean_user = username.strip().strip("/")
        api_url = f"{self.WIDGETS_URL}/v3/pidgets/users/{clean_user}/pins/"

        req = urllib.request.Request(api_url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        raw_pins = data.get("data", {}).get("pins", [])
        pins: List[Dict[str, Any]] = []

        for item in raw_pins:
            pin_id = str(item.get("id") or "")
            images_dict = self._build_image_variants(item.get("images", {}))
            title = item.get("title") or item.get("description") or ""
            desc = item.get("description") or ""
            pinner = item.get("pinner", {}) or {}

            pins.append({
                "id": pin_id,
                "title": title,
                "description": desc,
                "pin_url": f"https://www.pinterest.com/pin/{pin_id}/" if pin_id else "",
                "dominant_color": item.get("dominant_color") or "",
                "images": images_dict,
                "orig_image_url": images_dict.get("orig") or images_dict.get("736x") or "",
                "pinner": {
                    "username": pinner.get("username", clean_user),
                    "full_name": pinner.get("full_name", ""),
                },
            })

            if len(pins) >= limit:
                break

        return pins

    def resolve_pin_id(self, pin_id_or_url: str) -> str:
        """Extract a numeric pin ID from a string, full URL, or short link."""
        input_str = pin_id_or_url.strip()

        # If already pure digits
        if input_str.isdigit():
            return input_str

        # If short link (pin.it/...), follow redirects to get final URL
        if "pin.it" in input_str:
            try:
                req = urllib.request.Request(
                    input_str,
                    headers={"User-Agent": self.user_agent}
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    input_str = resp.geturl()
            except Exception as e:
                logger.warning(f"Failed to follow pin.it redirect: {e}")

        # Regex match pin ID
        match = re.search(r'/pin/(\d+)', input_str)
        if match:
            return match.group(1)

        match_num = re.search(r'(\d{10,25})', input_str)
        if match_num:
            return match_num.group(1)

        return input_str

    def get_pin_details(self, pin_id_or_url: str) -> Dict[str, Any]:
        """
        Get full metadata and highest-resolution images for a specific pin.
        """
        pin_id = self.resolve_pin_id(pin_id_or_url)
        api_url = f"{self.WIDGETS_URL}/v3/pidgets/pins/info/?pin_ids={pin_id}"

        req = urllib.request.Request(api_url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        pin_list = data.get("data", [])
        if not pin_list or not isinstance(pin_list, list):
            raise ValueError(f"Pin '{pin_id}' not found or invalid response")

        pin = pin_list[0]
        if "error" in pin:
            raise ValueError(f"Pinterest error for Pin '{pin_id}': {pin.get('error')}")

        images_dict = self._build_image_variants(pin.get("images", {}))

        # Check for story pins or nested original images
        story_pages = pin.get("story_pin_data", {}).get("pages", [])
        story_images = []
        for page in story_pages:
            p_imgs = page.get("image_adjusted", {}).get("images", {})
            for k, val in p_imgs.items():
                if isinstance(val, dict) and "url" in val:
                    story_images.append(val["url"])
                    if k in ("originals", "orig") and "orig" not in images_dict:
                        images_dict["orig"] = val["url"]

        pinner = pin.get("pinner", {}) or {}
        return {
            "id": pin.get("id", pin_id),
            "title": pin.get("title") or pin.get("description") or "",
            "description": pin.get("description") or "",
            "link": pin.get("link") or "",
            "pin_url": f"https://www.pinterest.com/pin/{pin.get('id', pin_id)}/",
            "domain": pin.get("domain") or "",
            "dominant_color": pin.get("dominant_color") or "",
            "repin_count": pin.get("repin_count", 0),
            "images": images_dict,
            "orig_image_url": images_dict.get("orig") or images_dict.get("736x") or "",
            "story_images": story_images,
            "pinner": {
                "username": pinner.get("username", ""),
                "full_name": pinner.get("full_name", ""),
                "profile_url": f"https://www.pinterest.com/{pinner.get('username', '')}/" if pinner.get("username") else "",
            },
        }

    def download_image(self, image_url: str, output_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Download a single image with security guards.
        """
        parsed = urllib.parse.urlparse(image_url)
        if not any(parsed.netloc.endswith(allowed) for allowed in ALLOWED_IMAGE_HOSTS):
            raise ValueError(f"Untrusted image domain: {parsed.netloc}. Only Pinterest domains allowed.")

        out = Path(output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)

        req = urllib.request.Request(
            image_url,
            headers={
                "User-Agent": self.user_agent,
                "Referer": f"{self.BASE_URL}/",
            }
        )

        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            content = resp.read(MAX_DOWNLOAD_BYTES + 1)
            if len(content) > MAX_DOWNLOAD_BYTES:
                raise ValueError(f"Image exceeds maximum size limit of {MAX_DOWNLOAD_BYTES // (1024*1024)}MB")

        with open(out, "wb") as f:
            f.write(content)

        return {
            "url": image_url,
            "path": str(out),
            "size_bytes": len(content),
            "filename": out.name,
        }


# Singleton client instance
_client = PinterestClient()


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
def search_pins(query: str, limit: int = 25, resolution: str = "orig") -> str:
    """
    Search Pinterest pins by keyword or topic.

    Args:
        query: Search term (e.g., 'minimalist landing page', 'modern architecture', 'dashboard ui')
        limit: Maximum number of pins to return (default 25, max 50)
        resolution: Preferred image resolution ('orig', '736x', '474x', '236x'). Default is 'orig' (highest resolution).

    Returns:
        JSON string containing list of pins with id, title, description, pin_url, dominant_color, image URLs, and pinner info.
    """
    try:
        pins = _client.search_pins(query=query, limit=limit)
        results = []
        for p in pins:
            img_url = p["images"].get(resolution) or p["orig_image_url"]
            results.append({
                "id": p["id"],
                "title": p["title"],
                "description": p["description"],
                "image_url": img_url,
                "pin_url": p["pin_url"],
                "dominant_color": p["dominant_color"],
                "all_resolutions": p["images"],
                "pinner": p["pinner"],
            })
        return json.dumps({
            "status": "success",
            "query": query,
            "count": len(results),
            "pins": results,
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"search_pins failed: {e}", exc_info=True)
        return json.dumps({"status": "error", "message": str(e), "query": query}, indent=2)


@mcp.tool()
def get_board_pins(username: str, board: str, limit: int = 25, resolution: str = "orig") -> str:
    """
    Get pins from a public Pinterest board.

    Args:
        username: Pinterest username (e.g., 'canva', 'pinterest')
        board: Board slug or name (e.g., 'design-trends', 'official-news')
        limit: Maximum number of pins to return (default 25)
        resolution: Preferred image resolution ('orig', '736x', '474x', '236x')

    Returns:
        JSON string containing board pins with metadata and image URLs.
    """
    try:
        pins = _client.get_board_pins(username=username, board=board, limit=limit)
        results = []
        for p in pins:
            img_url = p["images"].get(resolution) or p["orig_image_url"]
            results.append({
                "id": p["id"],
                "title": p["title"],
                "description": p["description"],
                "image_url": img_url,
                "pin_url": p["pin_url"],
                "dominant_color": p["dominant_color"],
                "all_resolutions": p["images"],
                "pinner": p["pinner"],
            })
        return json.dumps({
            "status": "success",
            "username": username,
            "board": board,
            "count": len(results),
            "pins": results,
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"get_board_pins failed: {e}", exc_info=True)
        return json.dumps({"status": "error", "message": str(e), "username": username, "board": board}, indent=2)


@mcp.tool()
def get_user_pins(username: str, limit: int = 25, resolution: str = "orig") -> str:
    """
    Get recent pins created or saved by a Pinterest user.

    Args:
        username: Pinterest username (e.g., 'canva', 'airbnb')
        limit: Maximum number of pins to return (default 25)
        resolution: Preferred image resolution ('orig', '736x', '474x', '236x')

    Returns:
        JSON string containing user pins with metadata and image URLs.
    """
    try:
        pins = _client.get_user_pins(username=username, limit=limit)
        results = []
        for p in pins:
            img_url = p["images"].get(resolution) or p["orig_image_url"]
            results.append({
                "id": p["id"],
                "title": p["title"],
                "description": p["description"],
                "image_url": img_url,
                "pin_url": p["pin_url"],
                "dominant_color": p["dominant_color"],
                "all_resolutions": p["images"],
                "pinner": p["pinner"],
            })
        return json.dumps({
            "status": "success",
            "username": username,
            "count": len(results),
            "pins": results,
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"get_user_pins failed: {e}", exc_info=True)
        return json.dumps({"status": "error", "message": str(e), "username": username}, indent=2)


@mcp.tool()
def get_pin_details(pin_id_or_url: str) -> str:
    """
    Get full metadata and original high-resolution image for a specific Pinterest pin.

    Args:
        pin_id_or_url: Pin ID (e.g., '424605071146368277') or URL (e.g., 'https://www.pinterest.com/pin/424605071146368277/' or 'https://pin.it/xyz')

    Returns:
        JSON string with complete pin details, full-size image URL, dimensions, and author info.
    """
    try:
        details = _client.get_pin_details(pin_id_or_url)
        return json.dumps({
            "status": "success",
            "pin": details,
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"get_pin_details failed: {e}", exc_info=True)
        return json.dumps({"status": "error", "message": str(e), "input": pin_id_or_url}, indent=2)


@mcp.tool()
def extract_from_url(url: str, limit: int = 25) -> str:
    """
    Smart Pinterest URL extractor. Automatically detects whether the URL is a Pin,
    Board, User profile, or Search URL, and extracts images and metadata accordingly.

    Args:
        url: Any Pinterest URL (e.g., 'https://www.pinterest.com/pin/123/', 'https://pin.it/xyz',
             'https://www.pinterest.com/username/boardname/', 'https://www.pinterest.com/username/',
             or 'https://www.pinterest.com/search/pins/?q=query')
        limit: Maximum pins to return if URL is a board/user/search (default 25)

    Returns:
        JSON string with extracted images, pins, or details.
    """
    try:
        clean_url = url.strip()

        # Case 1: Short link pin.it or pin page
        if "pin.it" in clean_url or "/pin/" in clean_url:
            details = _client.get_pin_details(clean_url)
            return json.dumps({
                "status": "success",
                "type": "pin",
                "pin": details,
            }, indent=2, ensure_ascii=False)

        # Case 2: Search URL
        if "/search/pins/" in clean_url:
            parsed = urllib.parse.urlparse(clean_url)
            qs = urllib.parse.parse_qs(parsed.query)
            query = qs.get("q", [""])[0]
            if query:
                return search_pins(query=query, limit=limit)

        # Case 3: Profile or Board URL
        parsed = urllib.parse.urlparse(clean_url)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) == 1:
            # User profile: /username
            return get_user_pins(username=parts[0], limit=limit)
        elif len(parts) >= 2:
            # Board: /username/boardname
            return get_board_pins(username=parts[0], board=parts[1], limit=limit)

        return json.dumps({
            "status": "error",
            "message": f"Unable to determine Pinterest resource type from URL: {url}",
        }, indent=2)
    except Exception as e:
        logger.error(f"extract_from_url failed: {e}", exc_info=True)
        return json.dumps({"status": "error", "message": str(e), "url": url}, indent=2)


@mcp.tool()
def download_images(
    image_urls: List[str],
    output_folder: str = "assets/pinterest",
    filename_prefix: str = "pinterest"
) -> str:
    """
    Safely download Pinterest images to a local directory.

    Args:
        image_urls: List of image URLs (usually from search_pins, get_pin_details, etc.)
        output_folder: Destination folder on disk (e.g. 'assets/images' or 'public/pinterest')
        filename_prefix: Prefix for saved image files (default 'pinterest')

    Returns:
        JSON string summarizing downloaded files, paths, and total bytes.
    """
    try:
        target_dir = Path(output_folder).resolve()
        target_dir.mkdir(parents=True, exist_ok=True)

        downloaded = []
        errors = []

        for i, url in enumerate(image_urls):
            try:
                # Determine extension
                clean_url = url.split("?")[0]
                ext = ".jpg"
                if clean_url.endswith(".png"):
                    ext = ".png"
                elif clean_url.endswith(".webp"):
                    ext = ".webp"

                filename = f"{filename_prefix}_{i + 1:03d}{ext}"
                out_path = target_dir / filename

                # Ensure path traversal guard
                if not str(out_path.resolve()).startswith(str(target_dir)):
                    errors.append({"url": url, "error": "Path traversal attempt detected"})
                    continue

                res = _client.download_image(url, out_path)
                downloaded.append(res)
            except Exception as item_err:
                errors.append({"url": url, "error": str(item_err)})

        return json.dumps({
            "status": "success",
            "output_folder": str(target_dir),
            "total_requested": len(image_urls),
            "downloaded_count": len(downloaded),
            "downloaded": downloaded,
            "errors": errors,
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"download_images failed: {e}", exc_info=True)
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Pinterest MCP Server")
    parser.add_argument("--test-search", help="Test search directly via CLI")
    parser.add_argument("--test-pin", help="Test pin lookup directly via CLI")
    args = parser.parse_args()

    if args.test_search:
        print(search_pins(args.test_search, limit=5))
        return

    if args.test_pin:
        print(get_pin_details(args.test_pin))
        return

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
