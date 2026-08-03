# ============================================================
# Build cursor-setup.zip from latest .cursor contents
# ============================================================
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SourceDir = Join-Path $RepoRoot ".cursor"
$BuildDir = Join-Path $ScriptDir "bin\Debug\net8.0-windows\win-x64"
$OutputZip = Join-Path $BuildDir "cursor-setup.zip"
$TempZip = Join-Path $env:TEMP "cursor-setup-build-$([System.Guid]::NewGuid().ToString('N')).zip"

if (-not (Test-Path $SourceDir)) {
    Write-Host "[ERROR] Source directory not found: $SourceDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $BuildDir)) {
    Write-Host "[ERROR] Build directory not found: $BuildDir" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Cursor Enterprise Framework Packager v4.3.0" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Source : $SourceDir"
Write-Host "Output : $OutputZip"
Write-Host ""

# Stats
Write-Host "[1/5] Gathering framework statistics..." -ForegroundColor Yellow
$categories = @(
    "agents", "cache", "commands", "hooks", "knowledge",
    "memory", "prompts", "references", "rules", "scripts",
    "skills", "templates", "workflows"
)
$stats = [ordered]@{}
foreach ($cat in $categories) {
    $catPath = Join-Path $SourceDir $cat
    if (Test-Path $catPath) {
        $files = @(Get-ChildItem -Path $catPath -Recurse -File -ErrorAction SilentlyContinue)
        $stats[$cat] = $files.Count
    } else {
        $stats[$cat] = 0
    }
}
$stats["AGENTS.md"] = if (Test-Path (Join-Path $SourceDir "AGENTS.md")) { 1 } else { 0 }
$stats["cursor.json"] = if (Test-Path (Join-Path $SourceDir "cursor.json")) { 1 } else { 0 }

$total = ($stats.Values | Measure-Object -Sum).Sum
Write-Host "  Total files: $total" -ForegroundColor Green
foreach ($k in $stats.Keys) {
    Write-Host ("  {0,-12}: {1}" -f $k, $stats[$k])
}

# Integrity check
Write-Host ""
Write-Host "[2/5] Verifying framework integrity..." -ForegroundColor Yellow
$requiredDirs = @("rules", "skills", "agents", "memory", "knowledge", "scripts")
$issues = @()
foreach ($dir in $requiredDirs) {
    if (-not (Test-Path (Join-Path $SourceDir $dir))) {
        $issues += "Missing directory: $dir"
    }
}
if ($issues.Count -gt 0) {
    Write-Host "[WARN] Integrity issues:" -ForegroundColor Yellow
    foreach ($i in $issues) { Write-Host "  - $i" -ForegroundColor Yellow }
} else {
    Write-Host "  [OK] All required directories present" -ForegroundColor Green
}

# Build ZIP
Write-Host ""
Write-Host "[3/5] Creating ZIP archive..." -ForegroundColor Yellow
if (Test-Path $OutputZip) {
    Remove-Item $OutputZip -Force
    Write-Host "  Removed existing zip" -ForegroundColor Gray
}
if (Test-Path $TempZip) { Remove-Item $TempZip -Force }

# Use Compress-Archive with the wildcard so the entries are at the root
# (matching the format the installer expects)
try {
    Compress-Archive -Path "$SourceDir\*" -DestinationPath $TempZip -CompressionLevel Optimal -Force
}
catch {
    Write-Host "[ERROR] Compress-Archive failed: $_" -ForegroundColor Red
    exit 1
}

Move-Item -Path $TempZip -Destination $OutputZip -Force

$zipSize = (Get-Item $OutputZip).Length
$zipSizeMB = [Math]::Round($zipSize / 1MB, 2)
Write-Host "  [OK] ZIP archive created: $zipSizeMB MB" -ForegroundColor Green

# Verify structure
Write-Host ""
Write-Host "[4/5] Verifying ZIP structure..." -ForegroundColor Yellow
$verifyDir = Join-Path $env:TEMP "cursor-setup-verify-$([System.Guid]::NewGuid().ToString('N'))"
if (Test-Path $verifyDir) { Remove-Item $verifyDir -Recurse -Force }
New-Item -ItemType Directory -Path $verifyDir | Out-Null
Expand-Archive -Path $OutputZip -DestinationPath $verifyDir -Force

$topLevel = @(Get-ChildItem $verifyDir)
Write-Host "  Top-level entries: $($topLevel.Count)"
$dirs = ($topLevel | Where-Object { $_.PSIsContainer }).Count
$files = ($topLevel | Where-Object { -not $_.PSIsContainer }).Count
Write-Host "  Directories: $dirs"
Write-Host "  Files: $files"

# Check expected categories
$expectedDirs = @("agents", "commands", "hooks", "knowledge", "memory", "prompts", "references", "rules", "scripts", "skills", "templates", "workflows")
$missingDirs = @()
foreach ($d in $expectedDirs) {
    if (-not (Test-Path (Join-Path $verifyDir $d))) {
        $missingDirs += $d
    }
}
if ($missingDirs.Count -gt 0) {
    Write-Host "  [WARN] Missing expected directories: $($missingDirs -join ', ')" -ForegroundColor Yellow
} else {
    Write-Host "  [OK] All expected directories present" -ForegroundColor Green
}

# Cleanup
Remove-Item $verifyDir -Recurse -Force

# Write build info
Write-Host ""
Write-Host "[5/5] Writing build metadata..." -ForegroundColor Yellow
$metaPath = Join-Path $BuildDir "cursor-setup-build.json"
$meta = [ordered]@{
    version     = "4.3.0"
    built_at    = (Get-Date).ToString("o")
    source      = $SourceDir
    output      = $OutputZip
    size_bytes  = $zipSize
    size_mb     = $zipSizeMB
    total_files = $total
    categories  = $stats
}
$meta | ConvertTo-Json -Depth 5 | Out-File -FilePath $metaPath -Encoding UTF8
Write-Host "  [OK] Metadata: $metaPath" -ForegroundColor Green

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Build complete: $OutputZip ($zipSizeMB MB)" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""