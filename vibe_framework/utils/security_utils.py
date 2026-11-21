"""
Security Utilities

Security-related helper functions.
"""

import hashlib
import hmac
import re
import secrets
from typing import Optional


def sanitize_html(text: str) -> str:
    """
    Sanitize HTML to prevent XSS.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    dangerous = [
        (r"<script[^>]*>.*?</script>", ""),
        (r"<iframe[^>]*>.*?</iframe>", ""),
        (r"javascript:", ""),
        (r"on\w+\s*=", ""),
    ]

    result = text
    for pattern, replacement in dangerous:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE | re.DOTALL)

    return result


def sanitize_sql(text: str) -> str:
    """
    Basic SQL injection prevention.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    dangerous = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
    result = text
    for pattern in dangerous:
        result = result.replace(pattern, "")
    return result


def generate_token(length: int = 32) -> str:
    """
    Generate a secure random token.

    Args:
        length: Token length in bytes

    Returns:
        Hex-encoded token
    """
    return secrets.token_hex(length)


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """
    Hash a password with salt.

    Args:
        password: Password to hash
        salt: Optional salt (generated if not provided)

    Returns:
        Tuple of (hash, salt)
    """
    if salt is None:
        salt = secrets.token_hex(16)

    hash_obj = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000,
    )
    return hash_obj.hex(), salt


def verify_password(password: str, hash_value: str, salt: str) -> bool:
    """
    Verify a password against hash.

    Args:
        password: Password to verify
        hash_value: Stored hash
        salt: Stored salt

    Returns:
        True if password matches
    """
    computed_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(computed_hash, hash_value)


def verify_hmac(message: str, signature: str, secret: str) -> bool:
    """
    Verify HMAC signature.

    Args:
        message: Original message
        signature: Provided signature
        secret: Secret key

    Returns:
        True if signature valid
    """
    expected = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def generate_hmac(message: str, secret: str) -> str:
    """
    Generate HMAC signature.

    Args:
        message: Message to sign
        secret: Secret key

    Returns:
        HMAC signature
    """
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()


def mask_sensitive(text: str, visible_chars: int = 4) -> str:
    """
    Mask sensitive information.

    Args:
        text: Text to mask
        visible_chars: Number of characters to keep visible

    Returns:
        Masked text
    """
    if len(text) <= visible_chars:
        return "*" * len(text)
    return text[:visible_chars] + "*" * (len(text) - visible_chars)


def is_safe_filename(filename: str) -> bool:
    """
    Check if filename is safe.

    Args:
        filename: Filename to check

    Returns:
        True if safe
    """
    dangerous = ["..", "/", "\\", "\x00", "\n", "\r"]
    for pattern in dangerous:
        if pattern in filename:
            return False

    reserved = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"]
    if filename.upper() in reserved:
        return False

    return True


def validate_api_key_format(key: str) -> bool:
    """
    Validate API key format.

    Args:
        key: API key to validate

    Returns:
        True if format is valid
    """
    if len(key) < 20:
        return False

    pattern = r"^[a-zA-Z0-9_-]+$"
    return bool(re.match(pattern, key))


def redact_pii(text: str) -> str:
    """
    Redact personally identifiable information.

    Args:
        text: Text containing potential PII

    Returns:
        Text with PII redacted
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
    ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"

    text = re.sub(email_pattern, "[EMAIL]", text)
    text = re.sub(phone_pattern, "[PHONE]", text)
    text = re.sub(ssn_pattern, "[SSN]", text)

    return text
