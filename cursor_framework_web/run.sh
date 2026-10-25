#!/usr/bin/env bash
# ============================================================
# CEF Vue App - Build & Deploy (Unix)
# Version: 1.0.0
# ============================================================
# Usage:
#   ./run.sh          - Build + deploy to preview
#   ./run.sh prod     - Build + deploy to production
# ============================================================

set -euo pipefail

MODE="${1:-preview}"
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
echo "  CEF Vue App - Build & Deploy"
echo "================================================"
echo

# Step 1: Build
echo "[1/2] Building production..."
npm run build

echo "      Build complete!"
echo

# Step 2: Deploy
echo "[2/2] Deploying..."

if [ "$MODE" = "prod" ]; then
    echo "      Deploying to PRODUCTION..."
    npx vercel --prod
else
    echo "      Deploying to PREVIEW..."
    npx vercel
fi

echo
echo "================================================"
echo "  Done!"
echo "================================================"