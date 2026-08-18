# ============================================================
# Copy-McpTools.ps1
# Copy MCP tools to .cursor/mcp for inclusion in ZIP
# ============================================================
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# RepoRoot is parent of cursor-setup-gui-wpf
$RepoRoot = Split-Path -Parent $ScriptDir
$CursorDir = Join-Path $RepoRoot ".cursor"
$McpTargetDir = Join-Path $CursorDir "mcp"
$ToolsDir = Join-Path $RepoRoot "tools"

Write-Host ""
Write-Host "MCP Tools Integration Script v4.4.0" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target : $McpTargetDir"
Write-Host "Source : $ToolsDir"
Write-Host ""

# Create .cursor directory if not exists
if (-not (Test-Path $CursorDir)) {
    New-Item -ItemType Directory -Path $CursorDir -Force | Out-Null
    Write-Host "[CREATE] $CursorDir" -ForegroundColor Green
}

# Create .cursor/mcp directory if not exists
if (-not (Test-Path $McpTargetDir)) {
    New-Item -ItemType Directory -Path $McpTargetDir -Force | Out-Null
    Write-Host "[CREATE] $McpTargetDir" -ForegroundColor Green
} else {
    Write-Host "[EXISTS] $McpTargetDir" -ForegroundColor Gray
}

# MCP servers to copy
$mcps = @(
    "cursor-framework-mcp",
    "cursor-autopilot-mcp",
    "cursor-memory-mcp"
)

$totalFiles = 0
$totalCopied = 0

foreach ($mcp in $mcps) {
    $srcDir = Join-Path $ToolsDir $mcp
    $destDir = Join-Path $McpTargetDir $mcp
    
    if (-not (Test-Path $srcDir)) {
        Write-Host "[SKIP] $mcp not found at $srcDir" -ForegroundColor Yellow
        continue
    }
    
    # Remove existing directory
    if (Test-Path $destDir) {
        Remove-Item -Path $destDir -Recurse -Force
        Write-Host "[REMOVE] $destDir" -ForegroundColor Gray
    }
    
    # Copy directory
    Copy-Item -Path $srcDir -Destination $destDir -Recurse -Force
    $files = @(Get-ChildItem -Path $destDir -Recurse -File -ErrorAction SilentlyContinue)
    $totalFiles += $files.Count
    $totalCopied++
    Write-Host "[COPY] $mcp ($($files.Count) files)" -ForegroundColor Green
}

# Copy MCP config template
$configSrc = Join-Path $ToolsDir "mcp-config-template.json"
$configDest = Join-Path $McpTargetDir "mcp-config-template.json"
if (Test-Path $configSrc) {
    Copy-Item -Path $configSrc -Destination $configDest -Force
    Write-Host "[COPY] mcp-config-template.json" -ForegroundColor Green
    $totalFiles++
}

# Copy MCP integration docs
$docSrc = Join-Path $ToolsDir "MCP-INTEGRATION.md"
$docDest = Join-Path $McpTargetDir "MCP-INTEGRATION.md"
if (Test-Path $docSrc) {
    Copy-Item -Path $docSrc -Destination $docDest -Force
    Write-Host "[COPY] MCP-INTEGRATION.md" -ForegroundColor Green
    $totalFiles++
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Complete: $totalCopied MCP servers, $totalFiles files" -ForegroundColor Green
Write-Host "Location: $McpTargetDir" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Return stats for build script
return @{
    TotalServers = $totalCopied
    TotalFiles = $totalFiles
    TargetDir = $McpTargetDir
}
