# ============================================================
# CEF - Main Quick Launcher (PowerShell)
# Version: 4.2.0
# ============================================================
# Quick access to all CEF commands
# ============================================================
# Usage:
#   .\go.ps1 dev          - Start Vue dev server
#   .\go.ps1 build        - Build Vue app
#   .\go.ps1 deploy       - Build + Deploy to Vercel
#   .\go.ps1 setup        - Install framework to user profile
#   .\go.ps1 help         - Show this help
# ============================================================

param(
    [string]$Command = "help"
)

$ErrorActionPreference = "Continue"
$scriptDir = $PSScriptRoot

switch ($Command.ToLower()) {
    "dev" {
        Set-Location "$scriptDir\cursor_framework_web"
        & "$scriptDir\cursor_framework_web\go.ps1"
    }
    "build" {
        Set-Location "$scriptDir\cursor_framework_web"
        npm run build
    }
    "preview" {
        Set-Location "$scriptDir\cursor_framework_web"
        & "$scriptDir\cursor_framework_web\preview.ps1"
    }
    "deploy" {
        Set-Location "$scriptDir\cursor_framework_web"
        & "$scriptDir\cursor_framework_web\run.ps1"
    }
    "setup" {
        & "$scriptDir\setup-user.ps1"
    }
    default {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host "  CEF - Quick Launcher Help" -ForegroundColor Cyan
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  Usage: .\go.ps1 [command]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  Commands:" -ForegroundColor White
        Write-Host "    dev          - Start Vue dev server" -ForegroundColor Gray
        Write-Host "    build        - Build Vue app for production" -ForegroundColor Gray
        Write-Host "    preview      - Preview built app" -ForegroundColor Gray
        Write-Host "    deploy       - Build + Deploy to Vercel" -ForegroundColor Gray
        Write-Host "    setup        - Install framework to user profile" -ForegroundColor Gray
        Write-Host "    help         - Show this help" -ForegroundColor Gray
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host "  Vue App Commands (cursor_framework_web folder):" -ForegroundColor Cyan
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "    .\go.ps1 dev     - Start dev server" -ForegroundColor Gray
        Write-Host "    .\go.ps1 build  - Production build" -ForegroundColor Gray
        Write-Host "    .\go.ps1 preview - Preview built app" -ForegroundColor Gray
        Write-Host ""
    }
}
