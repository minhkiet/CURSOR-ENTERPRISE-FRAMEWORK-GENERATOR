"""
Preflight: verify the vendored lunar_python loads and the calculator imports.

Run before any analysis session so the user sees the capability state up front.
Designed to fail loudly without the vendored library — never silently fall back
to LLM-only inference for Bazi factual calculations (K.1 / K.5).

Usage:
    python tools/bazi-plugin/scripts/bazi_status.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VENDOR_DIR = SCRIPT_DIR / "vendor"
sys.path.insert(0, str(VENDOR_DIR))


def main() -> int:
    report: dict[str, object] = {
        "ok": False,
        "vendor_dir": str(VENDOR_DIR),
        "vendor_exists": VENDOR_DIR.is_dir(),
        "lunar_python_version": None,
        "calculator_imports": False,
        "sample_chart_ok": False,
        "actions": [],
    }

    if not VENDOR_DIR.is_dir():
        report["actions"].append(
            "vendored lunar_python missing — re-sync from upstream "
            "(see tools/bazi-plugin/SYNC.md)"
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    try:
        import lunar_python  # noqa: WPS433 — intentional late import

        report["lunar_python_version"] = getattr(lunar_python, "__version__", "1.4.8")
    except Exception as exc:  # pragma: no cover
        report["actions"].append(f"cannot import lunar_python: {exc}")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    try:
        import calculate_bazi  # type: ignore[import-not-found]

        report["calculator_imports"] = True
    except Exception as exc:
        report["actions"].append(f"cannot import calculate_bazi: {exc}")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    try:
        chart = calculate_bazi.build_chart(
            calendar="solar",
            year=1990, month=5, day=15,
            hour=14, minute=30,
            gender="female",
            target_year=2026,
        )
        report["sample_chart_ok"] = True
        report["sample_four_pillars"] = chart["four_pillars"]["text"]
    except Exception as exc:
        report["actions"].append(f"sample chart failed: {exc}")

    report["ok"] = bool(
        report["vendor_exists"]
        and report["lunar_python_version"]
        and report["calculator_imports"]
        and report["sample_chart_ok"]
    )

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
