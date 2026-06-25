# ============================================================
# CEF - Quick Setup (PowerShell)
# Version: 4.2.0
# ============================================================
# One-command to install/update Cursor Enterprise Framework
# ============================================================
# Usage:
#   .\setup-user.ps1              - Install/Update
#   .\setup-user.ps1 -Force       - Force overwrite
# ============================================================

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$scriptDir = $PSScriptRoot

Set-Location $scriptDir

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  CEF Framework - User Setup (PowerShell)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Cursor is running
$cursor = Get-Process -Name "Cursor" -ErrorAction SilentlyContinue
if ($cursor) {
    Write-Host "[WARN] Cursor appears to be running." -ForegroundColor Yellow
    Write-Host "      It is recommended to close Cursor before setup." -ForegroundColor Yellow
    Write-Host ""
}

if ($Force) {
    Write-Host "[INFO] Force mode enabled" -ForegroundColor Cyan
    & "$scriptDir\setup.bat" --force --no-cursor-check
} else {
    & "$scriptDir\setup.bat" --no-cursor-check
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please restart Cursor IDE to load the framework." -ForegroundColor Cyan
Write-Host ""
