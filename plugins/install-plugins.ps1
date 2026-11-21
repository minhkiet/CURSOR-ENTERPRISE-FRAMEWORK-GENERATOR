# ==============================================================================
# Vibe Enterprise Framework - Multi-Tool Vibe Coding Plugin Installer
# ==============================================================================
# Supports: Cursor, Windsurf, Claude Code, Google Antigravity, Cline, Roo Code, Codex, Copilot
# Usage examples:
#   .\plugins\install-plugins.ps1 -Tool All
#   .\plugins\install-plugins.ps1 -Tool Windsurf
#   .\plugins\install-plugins.ps1 -Tool Cursor -Global
#   .\plugins\install-plugins.ps1 -List
# ==============================================================================

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('Cursor', 'Windsurf', 'ClaudeCode', 'Antigravity', 'Cline', 'RooCode', 'Codex', 'Copilot', 'All')]
    [string]$Tool = 'All',

    [Parameter(Mandatory=$false)]
    [switch]$Global,

    [Parameter(Mandatory=$false)]
    [switch]$Force,

    [Parameter(Mandatory=$false)]
    [string]$TargetPath = '',

    [Parameter(Mandatory=$false)]
    [switch]$List
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$PluginsDir = $ScriptDir

function Write-Header($text) {
    Write-Host ""
    Write-Host "══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host "══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success($text) {
    Write-Host "  ✓ $text" -ForegroundColor Green
}

function Write-Info($text) {
    Write-Host "  ℹ $text" -ForegroundColor Gray
}

function Write-Warning($text) {
    Write-Host "  ⚠ $text" -ForegroundColor Yellow
}

function Write-Error($text) {
    Write-Host "  ✗ $text" -ForegroundColor Red
}

# 1. Discover plugins in plugins/
$availablePlugins = Get-ChildItem -Path $PluginsDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "manifest.json")
}

if ($List) {
    Write-Header "Available Vibe Enterprise Framework Plugins"
    Write-Host "Found $($availablePlugins.Count) plugins in: $PluginsDir" -ForegroundColor White
    Write-Host ""
    foreach ($p in $availablePlugins) {
        $manifestPath = Join-Path $p.FullName "manifest.json"
        $desc = ""
        try {
            $json = Get-Content $manifestPath -Raw | ConvertFrom-Json
            $desc = $json.description
            $ver = $json.version
        } catch {}
        Write-Host "  • $($p.Name) (v$ver)" -ForegroundColor Green
        if ($desc) {
            Write-Host "    $desc" -ForegroundColor Gray
        }
    }
    Write-Host ""
    exit 0
}

Write-Header "Vibe Coding Plugin Installer"

$targetRoot = if ($TargetPath) { (Resolve-Path $TargetPath).Path } else { $ProjectRoot }
Write-Info "Target Workspace: $targetRoot"
Write-Info "Mode: $(if ($Global) { 'Global (User Home)' } else { 'Workspace Local' })"
Write-Info "Target Tool(s): $Tool"

# Map tool definitions
$toolConfigs = @{
    'Cursor' = @{
        Name = 'Cursor IDE'
        LocalDir = '.cursor\plugins'
        GlobalDir = if ($env:APPDATA) { Join-Path $env:APPDATA '.cursor\extensions' } else { "$env:USERPROFILE\.cursor\extensions" }
    }
    'Windsurf' = @{
        Name = 'Windsurf / Cascade'
        LocalDir = '.windsurf\plugins'
        GlobalDir = if ($env:APPDATA) { Join-Path $env:APPDATA 'Windsurf\extensions' } else { "$env:USERPROFILE\.windsurf\extensions" }
    }
    'ClaudeCode' = @{
        Name = 'Claude Code'
        LocalDir = '.claude\plugins'
        GlobalDir = "$env:USERPROFILE\.claude\plugins"
    }
    'Antigravity' = @{
        Name = 'Google Antigravity / Gemini CLI'
        LocalDir = '.agents\plugins'
        GlobalDir = "$env:USERPROFILE\.gemini\antigravity\plugins"
    }
    'Cline' = @{
        Name = 'Cline'
        LocalDir = '.cline\plugins'
        GlobalDir = "$env:USERPROFILE\.cline\plugins"
    }
    'RooCode' = @{
        Name = 'Roo Code'
        LocalDir = '.roo\plugins'
        GlobalDir = "$env:USERPROFILE\.roo\plugins"
    }
    'Codex' = @{
        Name = 'Codex Universal'
        LocalDir = '.codex\plugins'
        GlobalDir = "$env:USERPROFILE\.codex\plugins"
    }
    'Copilot' = @{
        Name = 'GitHub Copilot'
        LocalDir = '.github\plugins'
        GlobalDir = "$env:USERPROFILE\.github\plugins"
    }
}

$selectedTools = if ($Tool -eq 'All') {
    @('Cursor', 'Windsurf', 'ClaudeCode', 'Antigravity', 'Cline', 'RooCode', 'Codex')
} else {
    @($Tool)
}

foreach ($tKey in $selectedTools) {
    $cfg = $toolConfigs[$tKey]
    if (-not $cfg) { continue }

    Write-Host ""
    Write-Host "[$($cfg.Name)]" -ForegroundColor Yellow

    $destinationDir = if ($Global) {
        $cfg.GlobalDir
    } else {
        Join-Path $targetRoot $cfg.LocalDir
    }

    if (-not (Test-Path $destinationDir)) {
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
    }

    Write-Info "Destination: $destinationDir"

    foreach ($plugin in $availablePlugins) {
        $targetPluginDir = Join-Path $destinationDir $plugin.Name
        if ((Test-Path $targetPluginDir) -and -not $Force) {
            Write-Host "    · $($plugin.Name): already exists (use -Force to overwrite)" -ForegroundColor DarkGray
        } else {
            Copy-Item -Path $plugin.FullName -Destination $targetPluginDir -Recurse -Force
            Write-Success "Installed plugin: $($plugin.Name) -> $targetPluginDir"
        }
    }
}

Write-Host ""
Write-Host "══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  All requested vibe code plugins installed successfully!" -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
