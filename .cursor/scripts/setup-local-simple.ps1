# Cursor Enterprise Framework - Local Setup
# ==========================================

# Script này cài đặt .cursor configuration từ CURSOR ENTERPRISE FRAMEWORK GENERATOR
# sang các project khác trong máy.

param(
    [string]$ProjectPath = "",
    [switch]$List,
    [switch]$DryRun,
    [switch]$Force,
    [switch]$Backup
)

$ErrorActionPreference = "Continue"

# Colors
function Write-Step { param([string]$m) Write-Host "[...] $m" -ForegroundColor Cyan }
function Write-Success { param([string]$m) Write-Host "[OK] $m" -ForegroundColor Green }
function Write-Warn { param([string]$m) Write-Host "[!] $m" -ForegroundColor Yellow }
function Write-Fail { param([string]$m) Write-Host "[X] $m" -ForegroundColor Red }

# Paths
$SOURCE_ROOT = "D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
$CURSOR_SRC = Join-Path $SOURCE_ROOT ".cursor"
$CONFIG_FILE = Join-Path $SOURCE_ROOT ".cursor\scripts\setup-local-config.json"

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  CURSOR ENTERPRISE - LOCAL SETUP" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

# List mode
if ($List) {
    Write-Step "Discovering projects..."
    
    $searchPaths = @(
        "D:\PROJECTS",
        "C:\Projects",
        "C:\Dev",
        "D:\Dev"
    )
    
    Write-Host "`nProjects WITH .cursor:" -ForegroundColor Yellow
    foreach ($path in $searchPaths) {
        if (Test-Path $path) {
            Get-ChildItem $path -Directory | ForEach-Object {
                $cursorPath = Join-Path $_.FullName ".cursor"
                if (Test-Path $cursorPath) {
                    Write-Host "  + $($_.Name)" -ForegroundColor Green
                }
            }
        }
    }
    
    Write-Host "`nProjects WITHOUT .cursor:" -ForegroundColor Yellow
    foreach ($path in $searchPaths) {
        if (Test-Path $path) {
            Get-ChildItem $path -Directory | ForEach-Object {
                $cursorPath = Join-Path $_.FullName ".cursor"
                if (-not (Test-Path $cursorPath)) {
                    Write-Host "  - $($_.Name)" -ForegroundColor Gray
                }
            }
        }
    }
    
    Write-Host ""
    exit 0
}

# Validate source
if (-not (Test-Path $CURSOR_SRC)) {
    Write-Fail "Source .cursor not found at: $CURSOR_SRC"
    exit 1
}

Write-Step "Source: $CURSOR_SRC"

# Get components
Write-Step "Available components:"
$components = Get-ChildItem $CURSOR_SRC -Directory
foreach ($comp in $components) {
    $count = (Get-ChildItem $comp.FullName -Recurse -File).Count
    Write-Host "  [$($comp.Name)] - $count files" -ForegroundColor White
}

# Require project path
if (-not $ProjectPath) {
    Write-Warn "Usage: .\setup-local.ps1 <ProjectPath>"
    Write-Host "Example: .\setup-local.ps1 `"D:\Projects\MyApp`""
    Write-Host "Run with -List to see available projects"
    exit 1
}

# Resolve path
if (-not (Test-Path $ProjectPath)) {
    Write-Fail "Project not found: $ProjectPath"
    exit 1
}

Write-Step "Target: $ProjectPath"

$TARGET_CURSOR = Join-Path $ProjectPath ".cursor"

# Handle existing .cursor
if (Test-Path $TARGET_CURSOR) {
    if (-not $Force) {
        Write-Warn "Target already has .cursor folder"
        Write-Host "Use -Force to overwrite or -Backup to backup first"
        exit 1
    }
    
    if ($Backup) {
        $backupPath = "$TARGET_CURSOR.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Write-Step "Creating backup at: $backupPath"
        Copy-Item $TARGET_CURSOR $backupPath -Recurse -Force
        Write-Success "Backup created"
    }
    
    Write-Step "Removing existing .cursor..."
    Remove-Item $TARGET_CURSOR -Recurse -Force
}

if ($DryRun) {
    Write-Step "[DRY RUN] Would copy all components to: $ProjectPath"
    exit 0
}

# Copy
Write-Step "Installing .cursor to: $ProjectPath"

try {
    Copy-Item $CURSOR_SRC $TARGET_CURSOR -Recurse -Force
    
    $copiedCount = (Get-ChildItem $TARGET_CURSOR -Recurse -File).Count
    Write-Success "Installed successfully! ($copiedCount files)"
}
catch {
    Write-Fail "Installation failed: $_"
    exit 1
}

Write-Host ""
