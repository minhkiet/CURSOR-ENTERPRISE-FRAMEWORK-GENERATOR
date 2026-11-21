"""
Text Utilities

Text processing and formatting utilities.
"""

import re
import unicodedata
from typing import Optional


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: The filename to sanitize

    Returns:
        Sanitized filename
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', "", filename)
    sanitized = sanitized.strip(". ")
    return sanitized[:255]


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Args:
        text: Text to normalize

    Returns:
        Normalized text
    """
    return " ".join(text.split())


def slugify(text: str) -> str:
    """
    Convert text to a URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        URL-friendly slug
    """
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-").lower()


def remove_em_dashes(text: str) -> str:
    """
    Remove em-dashes from text (zero tolerance policy).

    Args:
        text: Text to process

    Returns:
        Text without em-dashes
    """
    return text.replace("\u2014", "-").replace("\u2013", "-").replace("—", "-").replace("–", "-")


def extract_keywords(text: str, min_length: int = 3) -> list[str]:
    """
    Extract keywords from text.

    Args:
        text: Text to extract from
        min_length: Minimum keyword length

    Returns:
        List of keywords
    """
    words = re.findall(r"\b\w+\b", text.lower())
    keywords = [w for w in words if len(w) >= min_length]
    return list(set(keywords))


def highlight_code_blocks(text: str) -> list[tuple[str, str]]:
    """
    Extract code blocks and their languages.

    Args:
        text: Text containing code blocks

    Returns:
        List of (language, code) tuples
    """
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [(lang, code) for lang, code in matches]


def count_words(text: str) -> int:
    """Count words in text."""
    return len(re.findall(r"\b\w+\b", text))


def is_valid_email(email: str) -> bool:
    """Check if email is valid."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url))


def extract_mentions(text: str) -> list[str]:
    """Extract @mentions from text."""
    return re.findall(r"@(\w+)", text)


def extract_hashtags(text: str) -> list[str]:
    """Extract #hashtags from text."""
    return re.findall(r"#(\w+)", text)
