# ============================================================
# CEF Vue App - Build & Deploy (PowerShell)
# Version: 1.0.0
# ============================================================
# One-command: build + deploy to Vercel
# Usage:
#   .\run.ps1           - Build + deploy to preview
#   .\run.ps1 prod      - Build + deploy to production
# ============================================================

param(
    [string]$Mode = "preview"
)

$ErrorActionPreference = "Stop"
$vueDir = $PSScriptRoot

Set-Location $vueDir

# Check Node.js
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "[ERROR] Node.js is not installed!" -ForegroundColor Red
    exit 1
}

# Install deps if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  CEF Vue App - Build & Deploy" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Step 1: Build
Write-Host "[1/2] Building production..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "      Build complete!" -ForegroundColor Green
Write-Host ""

# Step 2: Deploy
Write-Host "[2/2] Deploying..." -ForegroundColor Yellow

if ($Mode -eq "prod") {
    Write-Host "      Deploying to PRODUCTION..." -ForegroundColor Cyan
    npx vercel --prod
} else {
    Write-Host "      Deploying to PREVIEW..." -ForegroundColor Cyan
    npx vercel
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Done!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
