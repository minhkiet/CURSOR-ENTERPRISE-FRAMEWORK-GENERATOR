# Pre-Commit Hook for Cursor Framework (Windows PowerShell)
# Automatically warms cache and validates skills before commit

param(
    [switch]$SkipFramework,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"

Write-Host "[Cursor Framework] Running pre-commit checks..." -ForegroundColor Yellow

$FRAMEWORK_ROOT = if ($env:FRAMEWORK_ROOT) { $env:FRAMEWORK_ROOT } else { ".cursor" }
$MEMORY_PATH = if ($env:MEMORY_PATH) { $env:MEMORY_PATH } else { ".cache/memory.json" }

# Check if Python is available
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}

if (-not $pythonCmd) {
    Write-Host "Python not found. Skipping framework checks." -ForegroundColor Red
    exit 0
}

# Function to run framework command
function Run-Framework {
    param([string]$Command, [string]$Root = $FRAMEWORK_ROOT)
    & $pythonCmd -m cursor_framework $Command --root $Root 2>$null
}

# Check if cursor_framework module is available
$hasFramework = $false
try {
    $null = & $pythonCmd -c "import cursor_framework" 2>$null
    $hasFramework = $LASTEXITCODE -eq 0
} catch {}

if (-not $hasFramework) {
    Write-Host "cursor_framework not installed. Skipping framework checks." -ForegroundColor Yellow
    exit 0
}

# Run framework stats before commit
Write-Host "[1/3] Checking framework stats..." -ForegroundColor Yellow
$stats = Run-Framework "stats"
if ($LASTEXITCODE -eq 0) {
    $assets = if ($stats -match '"assets_indexed":\s*(\d+)') { $matches[1] } else { "0" }
    Write-Host "Framework loaded: $assets assets indexed" -ForegroundColor Green
} else {
    Write-Host "Could not get framework stats" -ForegroundColor Yellow
}

# Scan for changes in .cursor directory
if (Test-Path $FRAMEWORK_ROOT) {
    Write-Host "[2/3] Scanning framework files..." -ForegroundColor Yellow
    
    # Get git diff
    $changes = 0
    $staged = 0
    
    try {
        $changes = (git diff --name-only 2>$null | Where-Object { $_ -match '^\.cursor/' }).Count
        $staged = (git diff --cached --name-only 2>$null | Where-Object { $_ -match '^\.cursor/' }).Count
    } catch {}
    
    $total = $changes + $staged
    
    if ($total -gt 0) {
        Write-Host "$total framework file(s) changed" -ForegroundColor Green
        
        # Warm cache if framework files changed
        Write-Host "[3/3] Warming framework cache..." -ForegroundColor Yellow
        $null = Run-Framework "warm"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Cache warmed successfully" -ForegroundColor Green
        }
    } else {
        Write-Host "No framework file changes" -ForegroundColor Green
    }
}

# Check for common issues
Write-Host "[Extra] Running validation checks..." -ForegroundColor Yellow

# Check for broken skill references
$indexPath = Join-Path $FRAMEWORK_ROOT "INDEX.json"
if (Test-Path $indexPath) {
    try {
        $null = Get-Content $indexPath -Raw | ConvertFrom-Json -ErrorAction Stop
        Write-Host "INDEX.json is valid JSON" -ForegroundColor Green
    } catch {
        Write-Host "INDEX.json is malformed" -ForegroundColor Red
        Write-Host "Consider running: python -m cursor_framework index" -ForegroundColor Yellow
    }
}

# Check for required directories
$requiredDirs = @("skills", "rules", "agents")
$missing = 0
foreach ($dir in $requiredDirs) {
    $dirPath = Join-Path $FRAMEWORK_ROOT $dir
    if (-not (Test-Path $dirPath)) {
        Write-Host "Missing required directory: $dirPath" -ForegroundColor Red
        $missing++
    }
}

if ($missing -eq 0) {
    Write-Host "All required directories present" -ForegroundColor Green
}

Write-Host "[Cursor Framework] Pre-commit checks completed!" -ForegroundColor Yellow
exit 0
