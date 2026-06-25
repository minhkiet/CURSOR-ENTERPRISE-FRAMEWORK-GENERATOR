# ============================================================
# CEF - GitHub Quick Install (PowerShell)
# Version: 4.2.0
# ============================================================
# One-command install from GitHub
# ============================================================
# Usage:
#   quick-install.ps1                        - Default repo
#   quick-install.ps1 -RepoUrl "..."         - Custom repo
#   quick-install.ps1 -Branch "develop"      - Custom branch
# ============================================================

param(
    [string]$RepoUrl = "https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR",
    [string]$Branch = "main",
    [switch]$Force,
    [switch]$CheckUpdate
)

$ErrorActionPreference = "Stop"

# Banner
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  CEF - Quick GitHub Install" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Repository: $RepoUrl" -ForegroundColor Gray
Write-Host "Branch:     $Branch" -ForegroundColor Gray
Write-Host "Target:     $env:USERPROFILE\.cursor" -ForegroundColor Gray
Write-Host ""

# Parse repo URL
$parsed = $RepoUrl -replace 'https://github\.com/', '' -replace 'http://github\.com/', '' -replace 'git@github\.com:', ''
$repoPath = $parsed -replace '\.git$', '' -replace '/$', ''
$zipUrl = "https://github.com/$repoPath/archive/refs/heads/$Branch.zip"

Write-Host "[1/3] Downloading framework..." -ForegroundColor Yellow

$tempZip = "$env:TEMP\cef-install.zip"
$tempDir = "$env:TEMP\cef-install"

# Clean up
if (Test-Path $tempZip) { Remove-Item $tempZip -Force }
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }

try {
    Invoke-WebRequest -Uri $zipUrl -OutFile $tempZip -UseBasicParsing
    Write-Host "       Download complete!" -ForegroundColor Green
} catch {
    Write-Host "       [ERROR] Download failed!" -ForegroundColor Red
    Write-Host "       $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/3] Extracting files..." -ForegroundColor Yellow

try {
    Expand-Archive -Path $tempZip -DestinationPath $tempDir -Force
    
    # Find extracted folder
    $extracted = Get-ChildItem -Path $tempDir -Directory | Where-Object { $_.Name -like "*-$Branch" }
    if ($extracted) {
        Get-ChildItem -Path $extracted.FullName | Move-Item -Destination $tempDir -Force
        Remove-Item $extracted.FullName -Recurse -Force
    }
    
    Write-Host "       Extraction complete!" -ForegroundColor Green
} catch {
    Write-Host "       [ERROR] Extraction failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/3] Running setup..." -ForegroundColor Yellow

$setupBat = Join-Path $tempDir "setup.bat"
if (Test-Path $setupBat) {
    $args = @("--no-cursor-check")
    if ($Force) { $args += "--force" }
    
    & $setupBat @args
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "       [WARN] Setup completed with errors." -ForegroundColor Yellow
    } else {
        Write-Host "       Setup complete!" -ForegroundColor Green
    }
} else {
    Write-Host "       [ERROR] setup.bat not found!" -ForegroundColor Red
    exit 1
}

# Cleanup
Write-Host ""
Write-Host "[CLEANUP] Removing temporary files..." -ForegroundColor Gray
Remove-Item $tempZip -Force -ErrorAction SilentlyContinue
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please restart Cursor IDE to load the framework." -ForegroundColor Cyan
Write-Host ""
