# ============================================================
# Cursor Enterprise Framework - GitHub Installer (PowerShell)
# ============================================================
# Supports:
#   - Git clone (full history or shallow)
#   - ZIP download (no git required)
#   - Specific branch/tag
#   - Update checking
# ============================================================
param(
    [Parameter(Position=0)]
    [string]$RepoUrl = "https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR",
    
    [Parameter(Position=1)]
    [string]$Branch = "main",
    
    [Parameter()]
    [ValidateSet("clone", "zip", "auto")]
    [string]$Method = "auto",
    
    [switch]$Force,
    [switch]$CheckUpdate,
    [switch]$SkipCursorCheck,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors for output
function Write-Success { param($msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host "  [INFO] $msg" -ForegroundColor Cyan }
function Write-Warn { param($msg) Write-Host "  [WARN] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "  [ERROR] $msg" -ForegroundColor Red }

# Banner
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Cursor Enterprise Framework v4.2.0 - GitHub Installer" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Info "Repository: $RepoUrl"
Write-Info "Branch:     $Branch"
Write-Info "Method:     $Method"
Write-Info "Target:     $env:USERPROFILE\.cursor"
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    Write-Warn "Running as Administrator - some paths may differ"
}

# Parse repo URL
$parsed = $RepoUrl -replace 'https://github\.com/', '' -replace 'http://github\.com/', '' -replace 'git@github\.com:', ''
$repoPath = $parsed -replace '\.git$', '' -replace '/$', ''
$repoName = ($repoPath -split '/')[-1]

Write-Info "Parsed repo: $repoPath"
Write-Info "Repo name:   $repoName"

$tempDir = Join-Path $env:TEMP "cef-install-$(Get-Date -Format 'yyyyMMddHHmmss')"
$zipUrl = "https://github.com/$repoPath/archive/refs/heads/$Branch.zip"
$zipFile = Join-Path $env:TEMP "$repoName-$Branch.zip"

# Dry run mode
if ($DryRun) {
    Write-Info "[DRY RUN] Would perform the following actions:"
    Write-Host "  - Download from: $zipUrl"
    Write-Host "  - Extract to:     $tempDir"
    Write-Host "  - Install to:     $env:USERPROFILE\.cursor"
    exit 0
}

# Check update mode
if ($CheckUpdate) {
    Write-Host "[CHECK UPDATE]" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "https://api.github.com/repos/$repoPath/releases/latest" -UseBasicParsing 2>$null
        if ($response) {
            $latest = ($response.Content | ConvertFrom-Json)
            Write-Host "  Latest version: $($latest.tag_name)"
            Write-Host "  Released: $($latest.published_at)"
        }
    } catch {
        Write-Warn "Could not check for updates"
    }
    exit 0
}

# Create temp directory
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

try {
    # ============================================================
    # STEP 1: Download/Copy source files
    # ============================================================
    Write-Host "[1/4] Downloading source files..." -ForegroundColor Yellow
    
    $downloaded = $false
    
    if ($Method -eq "clone" -or $Method -eq "auto") {
        $git = Get-Command git -ErrorAction SilentlyContinue
        if ($git) {
            Write-Info "Using git clone..."
            git clone --branch $Branch --depth 1 $RepoUrl $tempDir 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $downloaded = $true
                Write-Success "Clone completed"
            }
        } elseif ($Method -eq "clone") {
            throw "Git is not installed. Please install Git from https://git-scm.com"
        }
    }
    
    if (-not $downloaded) {
        if ($Method -eq "clone") {
            throw "Git clone failed and auto-fallback is disabled"
        }
        
        Write-Info "Using ZIP download..."
        Write-Info "URL: $zipUrl"
        
        try {
            Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing
            Expand-Archive -Path $zipFile -DestinationPath $tempDir -Force
            
            # Find extracted folder
            $extracted = Get-ChildItem -Path $tempDir -Directory | Where-Object { $_.Name -like "*-$Branch" }
            if ($extracted) {
                # Move contents up
                Get-ChildItem -Path $extracted.FullName | Move-Item -Destination $tempDir -Force
                Remove-Item -Path $extracted.FullName -Recurse -Force
            }
            
            $downloaded = $true
            Write-Success "ZIP downloaded and extracted"
        } catch {
            throw "Failed to download ZIP: $_"
        }
    }
    
    # ============================================================
    # STEP 2: Check Cursor status
    # ============================================================
    if (-not $SkipCursorCheck) {
        Write-Host ""
        Write-Host "[2/4] Checking Cursor IDE..." -ForegroundColor Yellow
        
        $cursor = Get-Process -Name "Cursor" -ErrorAction SilentlyContinue
        if ($cursor) {
            Write-Warn "Cursor appears to be running"
            $response = Read-Host "  Continue anyway? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Host "Setup cancelled."
                exit 1
            }
        } else {
            Write-Success "Cursor is not running"
        }
    }
    
    # ============================================================
    # STEP 3: Run setup
    # ============================================================
    Write-Host ""
    Write-Host "[3/4] Running framework setup..." -ForegroundColor Yellow
    
    $setupBat = Join-Path $tempDir "setup.bat"
    if (Test-Path $setupBat) {
        $args = @()
        if ($SkipCursorCheck) { $args += "--no-cursor-check" }
        if ($Force) { $args += "--force" }

        Push-Location $tempDir
        $env:CEF_SOURCE_DIR = $tempDir
        & $setupBat @args
        $setupExit = $LASTEXITCODE
        Remove-Item Env:CEF_SOURCE_DIR -ErrorAction SilentlyContinue
        Pop-Location
        if ($setupExit -ne 0) {
            throw "Setup failed with exit code $setupExit"
        }
    } else {
        Write-Warn "setup.bat not found in downloaded files"
    }
    
    # ============================================================
    # STEP 4: Cleanup
    # ============================================================
    Write-Host ""
    Write-Host "[4/4] Cleaning up..." -ForegroundColor Yellow

    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $zipFile -Force -ErrorAction SilentlyContinue

    Write-Success "Cleanup complete"
    
    # ============================================================
    # Done
    # ============================================================
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  Installation Complete!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Please restart Cursor IDE to load the framework."
    Write-Host ""
    
} catch {
    Write-Err $_.Exception.Message
    Write-Host ""
    Write-Host "Installation failed. Please check:"
    Write-Host "  - Internet connection"
    Write-Host "  - Repository URL: $RepoUrl"
    Write-Host "  - Branch exists:  $Branch"
    Write-Host ""
    
    # Cleanup on failure
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $zipFile -Force -ErrorAction SilentlyContinue
    
    exit 1
}
