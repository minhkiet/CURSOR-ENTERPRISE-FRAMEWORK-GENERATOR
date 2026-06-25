"""
File Utilities

File operations and path handling utilities.
"""

import os
import shutil
from pathlib import Path
from typing import Optional


def ensure_dir(path: str | Path) -> Path:
    """
    Ensure directory exists, create if not.

    Args:
        path: Directory path

    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_relative_path(path: str | Path, base: str | Path) -> str:
    """
    Get relative path from base.

    Args:
        path: Target path
        base: Base path

    Returns:
        Relative path string
    """
    return str(Path(path).relative_to(base))


def find_files(
    directory: str | Path,
    pattern: str = "*",
    recursive: bool = True,
) -> list[Path]:
    """
    Find files matching pattern in directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern
        recursive: Search recursively

    Returns:
        List of matching paths
    """
    directory = Path(directory)
    if recursive:
        return list(directory.rglob(pattern))
    return list(directory.glob(pattern))


def copy_file(src: str | Path, dst: str | Path, overwrite: bool = False) -> bool:
    """
    Copy file from source to destination.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Overwrite if exists

    Returns:
        True if successful
    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        return False

    if dst.exists() and not overwrite:
        return False

    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    return True


def move_file(src: str | Path, dst: str | Path, overwrite: bool = False) -> bool:
    """
    Move file from source to destination.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Overwrite if exists

    Returns:
        True if successful
    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        return False

    if dst.exists() and not overwrite:
        return False

    ensure_dir(dst.parent)
    shutil.move(str(src), str(dst))
    return True


def delete_file(path: str | Path) -> bool:
    """
    Delete a file.

    Args:
        path: File path

    Returns:
        True if successful
    """
    path = Path(path)
    if path.exists() and path.is_file():
        path.unlink()
        return True
    return False


def get_file_size(path: str | Path) -> int:
    """Get file size in bytes."""
    return Path(path).stat().st_size


def get_extension(path: str | Path) -> str:
    """Get file extension without dot."""
    return Path(path).suffix.lstrip(".")


def change_extension(path: str | Path, new_ext: str) -> Path:
    """Change file extension."""
    path = Path(path)
    new_ext = new_ext.lstrip(".")
    return path.with_suffix(f".{new_ext}")


def read_file_safe(path: str | Path, encoding: str = "utf-8") -> Optional[str]:
    """
    Safely read file contents.

    Args:
        path: File path
        encoding: File encoding

    Returns:
        File contents or None if error
    """
    try:
        return Path(path).read_text(encoding=encoding)
    except Exception:
        return None


def write_file_safe(path: str | Path, content: str, encoding: str = "utf-8") -> bool:
    """
    Safely write file contents.

    Args:
        path: File path
        content: Content to write
        encoding: File encoding

    Returns:
        True if successful
    """
    try:
        path = Path(path)
        ensure_dir(path.parent)
        path.write_text(content, encoding=encoding)
        return True
    except Exception:
        return False


def list_directory(
    path: str | Path,
    files_only: bool = False,
    dirs_only: bool = False,
) -> list[Path]:
    """
    List directory contents.

    Args:
        path: Directory path
        files_only: Only return files
        dirs_only: Only return directories

    Returns:
        List of paths
    """
    path = Path(path)
    items = []
    for item in path.iterdir():
        if files_only and item.is_file():
            items.append(item)
        elif dirs_only and item.is_dir():
            items.append(item)
        elif not files_only and not dirs_only:
            items.append(item)
    return items
