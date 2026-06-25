# ============================================================
# CEF Vue App - Preview Built App (PowerShell)
# Version: 1.0.0
# ============================================================
# One-command to preview built app locally
# ============================================================

$ErrorActionPreference = "Stop"
$vueDir = $PSScriptRoot

Set-Location $vueDir

# Check dist folder
if (-not (Test-Path "dist")) {
    Write-Host "[ERROR] No dist folder found!" -ForegroundColor Red
    Write-Host "Please run 'run.ps1' to build first." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  CEF Vue App - Preview Mode" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Opening preview at: http://localhost:4173" -ForegroundColor Cyan
Write-Host "  Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

npm run preview
