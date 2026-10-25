#!/usr/bin/env bash
# ============================================================
# CEF Vue App - Preview Only (No Deploy)
# Version: 1.0.0
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "dist" ]; then
    echo "[ERROR] No dist folder found!"
    echo "Please run './run.sh' to build first."
    exit 1
fi

echo
echo "================================================"
echo "  CEF Vue App - Preview Mode"
echo "================================================"
echo
echo "  Opening preview at: http://localhost:4173"
echo
echo "  Press Ctrl+C to stop"
echo

npm run preview