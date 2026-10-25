#!/usr/bin/env bash
# ============================================================
# CEF Vue App - Quick Dev Launcher (Unix)
# Version: 1.0.0
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v node >/dev/null 2>&1; then
    echo "[ERROR] Node.js is not installed!"
    echo "Please install from: https://nodejs.org/"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "[INFO] Installing dependencies..."
    npm install
fi

echo
echo "================================================"
echo "  Starting CEF Vue App Dev Server..."
echo "================================================"
echo
echo "  Local:   http://localhost:5173"
echo
echo "  Press Ctrl+C to stop"
echo

npm run dev