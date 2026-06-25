"""
Utilities Module

Common utilities for the Cursor Enterprise Framework.
Provides helper functions and classes for various operations.

Features:
    - Text utilities (formatting, validation, sanitization)
    - File utilities (path handling, file operations)
    - Code utilities (pattern matching, formatting)
    - HTTP utilities (request/response helpers)
    - Security utilities (sanitization, validation)

Usage:
    >>> from cursor_framework.utils import sanitize_code, validate_filename
    >>> sanitized = sanitize_code(user_input)
"""

from . import text_utils
from . import file_utils
from . import code_utils
from . import http_utils
from . import security_utils

__all__ = [
    "text_utils",
    "file_utils",
    "code_utils",
    "http_utils",
    "security_utils",
]
