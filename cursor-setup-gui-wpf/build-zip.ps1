# ============================================================
# Build cursor-setup.zip from .cursor contents and staged MCP tools
# ============================================================
param(
    [string]$Config = "Debug"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# RepoRoot is parent of cursor-setup-gui-wpf
$RepoRoot = Split-Path -Parent $ScriptDir
$SourceDir = Join-Path $RepoRoot ".cursor"
$BuildDir = Join-Path $ScriptDir "bin\$Config\net8.0-windows\win-x64\publish"
$OutputZip = Join-Path $BuildDir "cursor-setup.zip"
$TempZip = Join-Path $env:TEMP "cursor-setup-build-$([System.Guid]::NewGuid().ToString('N')).zip"

Write-Host ""
Write-Host "Cursor Enterprise Framework Packager v4.5.0" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Config : $Config" -ForegroundColor Gray
Write-Host "Source : $SourceDir"
Write-Host "Output : $OutputZip"
Write-Host ""

if (-not (Test-Path $SourceDir)) {
    Write-Host "[ERROR] Source directory not found: $SourceDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $BuildDir)) {
    Write-Host "[ERROR] Build directory not found: $BuildDir" -ForegroundColor Red
    Write-Host "        Run build first: dotnet build" -ForegroundColor Yellow
    exit 1
}

# Stats
Write-Host "[1/6] Gathering framework statistics..." -ForegroundColor Yellow
$categories = @(
    "agents", "cache", "commands", "hooks", "knowledge",
    "memory", "prompts", "references", "rules", "scripts",
    "skills", "templates", "workflows", "mcp"
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
Write-Host "[2/6] Verifying framework integrity..." -ForegroundColor Yellow
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

# MCP tools check
$mcpDir = Join-Path $SourceDir "mcp"
if (Test-Path $mcpDir) {
    $mcpFiles = @(Get-ChildItem -Path $mcpDir -Recurse -File -ErrorAction SilentlyContinue)
    Write-Host "  [OK] MCP directory: $($mcpFiles.Count) files" -ForegroundColor Green
} else {
    Write-Host "  [INFO] MCP directory not found in .cursor (will be copied during build)" -ForegroundColor Gray
}

# Build ZIP
Write-Host ""
Write-Host "[3/6] Creating ZIP archive..." -ForegroundColor Yellow
if (Test-Path $OutputZip) {
    Remove-Item $OutputZip -Force
    Write-Host "  Removed existing zip" -ForegroundColor Gray
}
if (Test-Path $TempZip) { Remove-Item $TempZip -Force }

# Stage .cursor/ + cursor_framework/ into a temp dir so the zip contains
# both the framework rules/skills/agents AND the Python package that the
# WPF GUI's FrameworkRunner expects to find.
$StagingDir = Join-Path $env:TEMP "cursor-setup-staging-$([System.Guid]::NewGuid().ToString('N'))"
New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null

try {
    # Copy framework rules/skills/agents/etc. from the existing consumer
    # boundary. This is read-only; no host .cursor path is modified.
    Copy-Item -Path "$SourceDir\*" -Destination $StagingDir -Recurse -Force

    # Remove generated Python caches from the staged copy only. The source
    # .cursor tree remains untouched and the archive stays portable.
    Get-ChildItem -Path $StagingDir -Recurse -Directory -Force -Filter "__pycache__" |
        Sort-Object FullName -Descending |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
    Get-ChildItem -Path $StagingDir -Recurse -File -Force |
        Where-Object { $_.Extension -in @(".pyc", ".pyo") } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }

    # Stage MCP tools directly into the archive. Do not copy them into the
    # repository's .cursor/mcp first: that would overwrite user state merely
    # to produce a package.
    $stagedMcp = Join-Path $StagingDir "mcp"
    if (Test-Path $stagedMcp) { Remove-Item $stagedMcp -Recurse -Force }
    New-Item -ItemType Directory -Path $stagedMcp -Force | Out-Null
    $mcpSources = @("cursor-framework-mcp", "cursor-autopilot-mcp", "cursor-memory-mcp")
    foreach ($mcp in $mcpSources) {
        $mcpSource = Join-Path $RepoRoot "tools\$mcp"
        if (-not (Test-Path $mcpSource -PathType Container)) {
            Write-Host "  [WARN] MCP source not found: $mcpSource" -ForegroundColor Yellow
            continue
        }
        Copy-Item -Path $mcpSource -Destination (Join-Path $stagedMcp $mcp) -Recurse -Force
        Write-Host "  [OK] Staged MCP: $mcp" -ForegroundColor Green
    }
    # Do not ship interpreter caches in a distributable archive. They are
    # machine-specific, can be stale, and needlessly inflate the package.
    Get-ChildItem -Path $stagedMcp -Recurse -Directory -Force -Filter "__pycache__" |
        Sort-Object FullName -Descending |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
    Get-ChildItem -Path $stagedMcp -Recurse -File -Force |
        Where-Object { $_.Extension -in @(".pyc", ".pyo") } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }
    foreach ($meta in @("mcp-config-template.json", "MCP-INTEGRATION.md")) {
        $metaSource = Join-Path $RepoRoot "tools\$meta"
        if (Test-Path $metaSource -PathType Leaf) {
            Copy-Item -LiteralPath $metaSource -Destination $stagedMcp -Force
        }
    }

    # Bundle Python package so `python -m cursor_framework` works after install.
    $pkgSrc = Join-Path $RepoRoot "cursor_framework"
    if (Test-Path $pkgSrc) {
        $pkgDest = Join-Path $StagingDir "cursor_framework"
        Copy-Item -Path $pkgSrc -Destination $pkgDest -Recurse -Force
        # Strip dev artifacts that bloat the zip and serve no runtime purpose.
        Get-ChildItem -Path $pkgDest -Force |
            Where-Object { $_.Name -in @("__pycache__", "build", "review", "tests", ".cache", "cursor_framework.egg-info") } |
            ForEach-Object { Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
        Get-ChildItem -Path $pkgDest -Recurse -Directory -Force -Filter "__pycache__" |
            ForEach-Object { Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
        Write-Host "  [OK] Bundled cursor_framework Python package" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] cursor_framework package not found at $pkgSrc" -ForegroundColor Yellow
    }

    # Also ship requirements.txt + pyproject.toml at zip root for editable installs.
    foreach ($meta in @("requirements.txt", "pyproject.toml")) {
        $metaSrc = Join-Path $RepoRoot $meta
        if (Test-Path $metaSrc) {
            Copy-Item -Path $metaSrc -Destination $StagingDir -Force
        }
    }

    Compress-Archive -Path "$StagingDir\*" -DestinationPath $TempZip -CompressionLevel Optimal -Force
}
catch {
    Write-Host "[ERROR] Compress-Archive failed: $_" -ForegroundColor Red
    Remove-Item -Path $StagingDir -Recurse -Force -ErrorAction SilentlyContinue
    exit 1
}
finally {
    Remove-Item -Path $StagingDir -Recurse -Force -ErrorAction SilentlyContinue
}

Move-Item -Path $TempZip -Destination $OutputZip -Force

$zipSize = (Get-Item $OutputZip).Length
$zipSizeMB = [Math]::Round($zipSize / 1MB, 2)
Write-Host "  [OK] ZIP archive created: $zipSizeMB MB" -ForegroundColor Green

# Verify structure
Write-Host ""
Write-Host "[4/6] Verifying ZIP structure..." -ForegroundColor Yellow
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
$expectedDirs = @("agents", "commands", "hooks", "knowledge", "memory", "mcp", "prompts", "references", "rules", "scripts", "skills", "templates", "workflows", "cursor_framework")
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

# Write build info
Write-Host ""
Write-Host "[5/6] Writing build metadata..." -ForegroundColor Yellow
$metaPath = Join-Path $BuildDir "cursor-setup-build.json"

# Try to read version from .csproj dynamically, fall back to hardcoded
$csprojPath = Join-Path $ScriptDir "CursorSetupWpf.csproj"
$version = "4.5.0"
if (Test-Path $csprojPath) {
    $csprojContent = Get-Content $csprojPath -Raw
    if ($csprojContent -match '<Version>(.*?)</Version>') {
        $version = $matches[1]
    }
}

$meta = [ordered]@{
    version     = $version
    config      = $Config
    built_at    = (Get-Date).ToString("o")
    source      = $SourceDir
    output      = $OutputZip
    size_bytes  = $zipSize
    size_mb     = $zipSizeMB
    total_files = $total
    categories  = $stats
}
$meta | ConvertTo-Json -Depth 5 | Out-File -FilePath $metaPath -Encoding UTF8
Write-Host "  [OK] Metadata: $metaPath (version $version)" -ForegroundColor Green

# Verify MCP tools
Write-Host ""
Write-Host "[6/6] Verifying MCP tools..." -ForegroundColor Yellow
$mcps = @("cursor-framework-mcp", "cursor-autopilot-mcp", "cursor-memory-mcp")
$mcpFound = 0
foreach ($mcp in $mcps) {
    $mcpPath = Join-Path $verifyDir "mcp\$mcp"
    if (Test-Path $mcpPath) {
        $mcpFiles = @(Get-ChildItem -Path $mcpPath -Recurse -File -ErrorAction SilentlyContinue)
        Write-Host "  [OK] $mcp`: $($mcpFiles.Count) files" -ForegroundColor Green
        $mcpFound++
    } else {
        Write-Host "  [SKIP] $mcp not found in archive (will be added during build)" -ForegroundColor Gray
    }
}

# Cleanup only the temporary verification directory after every check has run.
Remove-Item $verifyDir -Recurse -Force

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Build complete: $OutputZip ($zipSizeMB MB)" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
