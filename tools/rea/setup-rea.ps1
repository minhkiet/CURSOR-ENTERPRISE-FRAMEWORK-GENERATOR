# Setup and Sanity Check for REA in Cursor Enterprise Framework
param(
    [switch]$Rebuild
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  REA (Reverse Engineer Anything) Sanity Check" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Check Node.js
Write-Host "[1/3] Checking Node.js runtime..." -ForegroundColor Yellow
$nodeVersion = node -v 2>$null
if (-not $nodeVersion) {
    Write-Host "ERROR: Node.js is not found on PATH. Please install Node.js >= 22.14." -ForegroundColor Red
    exit 1
}
Write-Host "      Node.js version: $nodeVersion" -ForegroundColor Green

# 2. Check compiled bundle
$reaScript = Join-Path $ScriptDir "scripts\rea.mjs"
$distDir = Join-Path $ScriptDir "dist"

if ($Rebuild -or (-not (Test-Path $distDir))) {
    Write-Host "[2/3] Building REA runtime..." -ForegroundColor Yellow
    Push-Location $ScriptDir
    try {
        npm install --engine-strict=false
        npm run build:cached
    } finally {
        Pop-Location
    }
} else {
    Write-Host "[2/3] Runtime bundle exists: $distDir" -ForegroundColor Green
}

# 3. Test REA CLI execution
Write-Host "[3/3] Running REA CLI version test..." -ForegroundColor Yellow
$reaVer = node $reaScript --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "      REA version: $reaVer" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "  REA is ready for MCP and CLI operations!" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "ERROR: Failed to run REA CLI." -ForegroundColor Red
    exit 1
}
