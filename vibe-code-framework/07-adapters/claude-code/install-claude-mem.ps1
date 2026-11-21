<#
.SYNOPSIS
    Automated installer for claude-mem persistent memory engine in Claude Code.
.DESCRIPTION
    Checks runtime prerequisites (Claude CLI, Node/Bun), adds the plugin from
    the marketplace, installs it, and verifies directory structure.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  claude-mem Persistent Memory Installer   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Claude CLI
Write-Host "`n[1/4] Checking Claude CLI..." -ForegroundColor Yellow
$claudeCmd = Get-Command "claude" -ErrorAction SilentlyContinue
if (-not $claudeCmd) {
    Write-Warning "Claude CLI ('claude') not found in PATH."
    Write-Host "If running inside Claude Code, run the following commands in the chat:" -ForegroundColor Gray
    Write-Host "  /plugin marketplace add thedotmack/claude-mem" -ForegroundColor White
    Write-Host "  /plugin install claude-mem" -ForegroundColor White
} else {
    Write-Host "Found Claude CLI at: $($claudeCmd.Source)" -ForegroundColor Green
}

# 2. Check Node / Bun runtime
Write-Host "`n[2/4] Checking Node.js / Bun runtime..." -ForegroundColor Yellow
$nodeCmd = Get-Command "node" -ErrorAction SilentlyContinue
$bunCmd = Get-Command "bun" -ErrorAction SilentlyContinue

if ($bunCmd) {
    Write-Host "Found Bun runtime: $($bunCmd.Source)" -ForegroundColor Green
} elseif ($nodeCmd) {
    Write-Host "Found Node runtime: $($nodeCmd.Source)" -ForegroundColor Green
} else {
    Write-Warning "Neither Node.js nor Bun found. claude-mem background worker requires Node or Bun."
}

# 3. Install Plugin via Claude CLI if available
Write-Host "`n[3/4] Installing claude-mem plugin..." -ForegroundColor Yellow
if ($claudeCmd) {
    try {
        & claude plugin marketplace add thedotmack/claude-mem
        & claude plugin install claude-mem
        Write-Host "Plugin installed successfully via CLI." -ForegroundColor Green
    } catch {
        Write-Warning "Direct CLI plugin install encountered an error: $_"
        Write-Host "You can complete this directly inside your Claude Code session with:" -ForegroundColor Gray
        Write-Host "  /plugin marketplace add thedotmack/claude-mem" -ForegroundColor White
        Write-Host "  /plugin install claude-mem" -ForegroundColor White
    }
} else {
    Write-Host "Please execute inside Claude Code session:" -ForegroundColor White
    Write-Host "  /plugin marketplace add thedotmack/claude-mem" -ForegroundColor Cyan
    Write-Host "  /plugin install claude-mem" -ForegroundColor Cyan
}

# 4. Check local memory storage path
Write-Host "`n[4/4] Verifying local memory storage directory..." -ForegroundColor Yellow
$userProfile = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$claudeMemDir = Join-Path $userProfile ".claude-mem"

if (-not (Test-Path $claudeMemDir)) {
    New-Item -ItemType Directory -Path $claudeMemDir -Force | Out-Null
    Write-Host "Created local memory directory: $claudeMemDir" -ForegroundColor Green
} else {
    Write-Host "Existing memory directory found: $claudeMemDir" -ForegroundColor Green
}

Write-Host "`n[DONE] claude-mem is configured for Vibe Enterprise Framework." -ForegroundColor Green
Write-Host "Web Viewer will be available at: http://localhost:37777 upon worker start." -ForegroundColor Cyan
