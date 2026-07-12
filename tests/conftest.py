"""Shared pytest fixtures.

Strategy: ONE sandbox per test session (function-scope was 5.7s/test due
to copytree of 572 files). Tests that mutate the sandbox create temp files
under their own subdir so they don't race.

ponytail: profile before optimize. copytree 5.7s > scan 0.5s.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REAL_CURSOR = PROJECT_ROOT / ".cursor"
SANDBOX_ROOT = PROJECT_ROOT / "_pytest_sandbox"


@pytest.fixture(scope="session")
def sandbox_cursor() -> Path:
    """Shared copy of .cursor/ for the whole session (session-scope)."""
    if not REAL_CURSOR.exists():
        pytest.skip("production .cursor/ not found")
    if SANDBOX_ROOT.exists():
        shutil.rmtree(SANDBOX_ROOT)
    SANDBOX_ROOT.mkdir(parents=True)
    sandbox = SANDBOX_ROOT / ".cursor"
    shutil.copytree(REAL_CURSOR, sandbox)
    yield sandbox
    # Cleanup at session end.
    shutil.rmtree(SANDBOX_ROOT, ignore_errors=True)


@pytest.fixture
def sandbox_writable(sandbox_cursor: Path, tmp_path: Path) -> Path:
    """Per-test writable scratch dir under the sandbox for file-mutation tests."""
    scratch = sandbox_cursor / "_scratch" / tmp_path.name
    scratch.mkdir(parents=True, exist_ok=True)
    yield scratch
    shutil.rmtree(scratch, ignore_errors=True)


@pytest.fixture
def memory_path(tmp_path: Path) -> Path:
    """Fresh memory.json path under tmp_path."""
    return tmp_path / "memory.json"