# One-liner installation for Cursor Enterprise Framework
# Usage: irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex
# Update: irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex -Update

param(
    [string]$RepoUrl = "https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR",
    [string]$Branch = "main",
    [switch]$Force,
    [switch]$Update
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Cursor Enterprise Framework - Quick Install" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Update mode - pull latest from git if installed
if ($Update) {
    $cefDir = "$env:USERPROFILE\.cursor"
    $gitDir = Join-Path $cefDir ".cursor"

    if (Test-Path $gitDir) {
        Write-Host "[UPDATE] Checking for updates..." -ForegroundColor Yellow
        try {
            Push-Location $gitDir
            git fetch origin
            $localHash = git rev-parse HEAD
            $remoteHash = git rev-parse "origin/$Branch"

            if ($localHash -ne $remoteHash) {
                Write-Host "      New version available! Updating..." -ForegroundColor Cyan
                git pull origin $Branch
                Write-Host "      Update complete!" -ForegroundColor Green
            } else {
                Write-Host "      Already up to date." -ForegroundColor Green
            }
            Pop-Location
            exit 0
        } catch {
            Pop-Location
            Write-Host "      ERROR: Could not update. Run fresh install instead." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "      Framework not installed. Running fresh install..." -ForegroundColor Yellow
    }
}

$parsed = $RepoUrl -replace 'https://github\.com/', '' -replace 'http://github\.com/', ''
$repoPath = $parsed -replace '\.git$', '' -replace '/$', ''
$zipUrl = "https://github.com/$repoPath/archive/refs/heads/$Branch.zip"

Write-Host "Repository: $RepoUrl" -ForegroundColor Gray
Write-Host "Branch:    $Branch" -ForegroundColor Gray
Write-Host "Target:    $env:USERPROFILE\.cursor" -ForegroundColor Gray
Write-Host ""

# Download
Write-Host "[1/3] Downloading framework..." -ForegroundColor Yellow
$tempZip = "$env:TEMP\cef-$([System.Guid]::NewGuid().ToString('N')).zip"
$tempDir = "$env:TEMP\cef-install"

try {
    Invoke-WebRequest -Uri $zipUrl -OutFile $tempZip -UseBasicParsing
    Write-Host "      Download complete." -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Could not download from GitHub." -ForegroundColor Red
    Write-Host "      Please check your internet connection and repository URL." -ForegroundColor Red
    exit 1
}

# Extract
Write-Host "[2/3] Extracting files..." -ForegroundColor Yellow
if (Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

try {
    Expand-Archive -Path $tempZip -DestinationPath $tempDir -Force
    $extracted = Get-ChildItem -Path $tempDir -Directory | Where-Object { $_.Name -like "*-$Branch" }
    if ($extracted) {
        Get-ChildItem -Path $extracted.FullName | Move-Item -Destination $tempDir -Force
        Remove-Item -Path $extracted.FullName -Recurse -Force
    }
    Write-Host "      Extraction complete." -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Could not extract files." -ForegroundColor Red
    exit 1
}

# Run setup
Write-Host "[3/3] Running setup..." -ForegroundColor Yellow
$setupBat = Join-Path $tempDir "setup.bat"
if (Test-Path $setupBat) {
    $args = @("--no-cursor-check")
    if ($Force) { $args += "--force" }
    
    & $setupBat @args
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      WARNING: Setup completed with errors." -ForegroundColor Yellow
    } else {
        Write-Host "      Setup complete!" -ForegroundColor Green
    }
} else {
    Write-Host "      ERROR: setup.bat not found in downloaded files." -ForegroundColor Red
    exit 1
}

# Cleanup
Remove-Item -Path $tempZip -Force -ErrorAction SilentlyContinue
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please restart Cursor IDE to load the framework."
Write-Host ""
