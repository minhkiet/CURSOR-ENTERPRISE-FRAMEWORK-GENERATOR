# ============================================================
# Copy-McpTools.ps1
# Stage MCP tools for inclusion in a ZIP without mutating .cursor
# ============================================================
param(
    # Optional safe staging destination. When omitted, a unique temp folder is
    # used. This script intentionally never writes to or deletes .cursor/mcp.
    [string]$DestinationDir = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# RepoRoot is parent of cursor-setup-gui-wpf
$RepoRoot = Split-Path -Parent $ScriptDir
$ToolsDir = Join-Path $RepoRoot "tools"
$McpTargetDir = if ([string]::IsNullOrWhiteSpace($DestinationDir)) {
    Join-Path $env:TEMP "cursor-mcp-staging-$([System.Guid]::NewGuid().ToString('N'))"
} else {
    [System.IO.Path]::GetFullPath($DestinationDir)
}

Write-Host ""
Write-Host "MCP Tools Integration Script v4.5.0" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target : $McpTargetDir"
Write-Host "Source : $ToolsDir"
Write-Host "Safety : .cursor is never modified"
Write-Host ""

# Create only the isolated staging directory.
if (Test-Path $McpTargetDir) {
    Remove-Item -LiteralPath $McpTargetDir -Recurse -Force
}
New-Item -ItemType Directory -Path $McpTargetDir -Force | Out-Null
Write-Host "[CREATE] $McpTargetDir" -ForegroundColor Green

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
    
    # Copy directory
    Copy-Item -Path $srcDir -Destination $destDir -Recurse -Force
    Get-ChildItem -Path $destDir -Recurse -Directory -Force -Filter "__pycache__" |
        Sort-Object FullName -Descending |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
    Get-ChildItem -Path $destDir -Recurse -File -Force |
        Where-Object { $_.Extension -in @(".pyc", ".pyo") } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }
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
Write-Host "Staging : $McpTargetDir" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Return stats for build script
return @{
    TotalServers = $totalCopied
    TotalFiles = $totalFiles
    TargetDir = $McpTargetDir
}
