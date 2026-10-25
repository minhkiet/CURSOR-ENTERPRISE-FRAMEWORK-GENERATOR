# Quick Setup Script for All Utilities
# Installs MCP servers, plugins, hooks, and commands

param(
    [switch]$All,
    [switch]$Mcp,
    [switch]$Plugins,
    [switch]$Hooks,
    [switch]$Commands,
    [switch]$Scripts,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
$SETUP_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Text)
    Write-Host "  ○ $Text" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Text)
    Write-Host "  ✓ $Text" -ForegroundColor Green
}

function Write-Error {
    param([string]$Text)
    Write-Host "  ✗ $Text" -ForegroundColor Red
}

# If no switches specified, show help
if (-not ($All -or $Mcp -or $Plugins -or $Hooks -or $Commands -or $Scripts)) {
    $All = $true
}

Write-Header "Cursor Framework Utilities Setup"

# Get project root
$ProjectRoot = if ($env:CURSOR_PROJECT_ROOT) { $env:CURSOR_PROJECT_ROOT } else { $SETUP_DIR }
$CursorDir = Join-Path $ProjectRoot ".cursor"

# ============================================================================
# MCP Setup
# ============================================================================
if ($All -or $Mcp) {
    Write-Header "Setting up MCP Servers"
    
    $mcpSource = Join-Path $SETUP_DIR "mcp"
    $mcpDest = Join-Path $ProjectRoot "mcp"
    
    if ($Uninstall) {
        if (Test-Path $mcpDest) {
            Remove-Item $mcpDest -Recurse -Force
            Write-Success "Removed MCP directory"
        }
    } else {
        # Copy MCP files
        if (Test-Path $mcpSource) {
            Copy-Item $mcpSource $mcpDest -Recurse -Force -ErrorAction SilentlyContinue
            Write-Success "MCP servers installed to: $mcpDest"
            
            # Show config instructions
            Write-Host ""
            Write-Host "To enable MCP servers in Cursor:" -ForegroundColor White
            Write-Host "  1. Open Cursor Settings (Ctrl+,)" -ForegroundColor Gray
            Write-Host "  2. Search for 'MCP'" -ForegroundColor Gray
            Write-Host "  3. Click 'Edit in settings.json'" -ForegroundColor Gray
            Write-Host "  4. Add the config from: mcp/mcp_config.json" -ForegroundColor Gray
            Write-Host ""
        } else {
            Write-Error "MCP source not found"
        }
    }
}

# ============================================================================
# Plugins Setup
# ============================================================================
if ($All -or $Plugins) {
    Write-Header "Setting up Cursor Plugins"
    
    $pluginsSource = Join-Path $SETUP_DIR "plugins"
    $cursorPlugins = if ($env:APPDATA) { Join-Path $env:APPDATA ".cursor\extensions" } else { "$env:USERPROFILE\.cursor\extensions" }
    
    if ($Uninstall) {
        $pluginName = "cursor-framework-quick-actions"
        $pluginPath = Join-Path $cursorPlugins $pluginName
        if (Test-Path $pluginPath) {
            Remove-Item $pluginPath -Recurse -Force
            Write-Success "Removed plugin: $pluginName"
        }
    } else {
        if (Test-Path $pluginsSource) {
            # Create plugin directory
            if (-not (Test-Path $cursorPlugins)) {
                New-Item -ItemType Directory -Path $cursorPlugins -Force | Out-Null
            }
            
            $pluginDest = Join-Path $cursorPlugins "cursor-framework-quick-actions"
            Copy-Item $pluginsSource $pluginDest -Recurse -Force
            Write-Success "Plugin installed to: $pluginDest"
            
            Write-Host ""
            Write-Host "Plugin 'cursor-framework-quick-actions' installed!" -ForegroundColor Green
            Write-Host "Restart Cursor to activate the plugin." -ForegroundColor Yellow
        }
    }
}

# ============================================================================
# Hooks Setup
# ============================================================================
if ($All -or $Hooks) {
    Write-Header "Setting up Git Hooks"
    
    $hooksSource = Join-Path $SETUP_DIR "hooks"
    $gitHooksDir = Join-Path $ProjectRoot ".git\hooks"
    
    if ($Uninstall) {
        @("pre-commit", "post-commit", "pre-push") | ForEach-Object {
            $hook = $_
            $hookPath = Join-Path $gitHooksDir $hook
            if (Test-Path $hookPath) {
                $content = Get-Content $hookPath -Raw -ErrorAction SilentlyContinue
                if ($content -match "Cursor Framework") {
                    Remove-Item $hookPath -Force
                    Write-Success "Removed hook: $hook"
                }
            }
        }
    } else {
        if (Test-Path $gitHooksDir) {
            # Install PowerShell hooks
            @("pre-commit.ps1", "post-commit.ps1", "pre-push.ps1") | ForEach-Object {
                $ps1 = $_
                $hookName = $ps1 -replace '\.ps1$', ''
                $destPath = Join-Path $gitHooksDir $ps1
                
                if (Test-Path (Join-Path $hooksSource $ps1)) {
                    Copy-Item (Join-Path $hooksSource $ps1) $destPath -Force
                    Write-Success "Installed: $ps1"
                }
            }
            
            # Create wrapper hooks for Git Bash compatibility
            @("pre-commit", "post-commit", "pre-push") | ForEach-Object {
                $hook = $_
                $wrapperPath = Join-Path $gitHooksDir $hook
                $ps1Path = Join-Path $hooksSource "$hook.ps1"
                
                if (Test-Path $ps1Path) {
                    $wrapper = @"
#!/bin/bash
# Cursor Framework Hook: $hook
powershell.exe -ExecutionPolicy Bypass -File "$ps1Path"
exit $?
"@
                    Set-Content -Path $wrapperPath -Value $wrapper -Force
                    Write-Success "Created wrapper: $hook"
                }
            }
            
            Write-Host ""
            Write-Success "Git hooks installed to: $gitHooksDir"
        } else {
            Write-Error "Git hooks directory not found. Initialize git first."
        }
    }
}

# ============================================================================
# Commands Setup
# ============================================================================
if ($All -or $Commands) {
    Write-Header "Setting up Slash Commands"
    
    $commandsSource = Join-Path $SETUP_DIR "commands"
    
    if ($Uninstall) {
        if (Test-Path $commandsSource) {
            Get-ChildItem $commandsSource -Filter "*.md" | ForEach-Object {
                $dest = Join-Path $CursorDir "commands\$($_.Name)"
                if (Test-Path $dest) {
                    Remove-Item $dest -Force
                    Write-Success "Removed: $($_.Name)"
                }
            }
        }
    } else {
        if (-not (Test-Path $CursorDir)) {
            New-Item -ItemType Directory -Path $CursorDir -Force | Out-Null
        }
        
        $commandsDest = Join-Path $CursorDir "commands"
        if (-not (Test-Path $commandsDest)) {
            New-Item -ItemType Directory -Path $commandsDest -Force | Out-Null
        }
        
        if (Test-Path $commandsSource) {
            Copy-Item "$commandsSource\*.md" $commandsDest -Force
            $count = (Get-ChildItem $commandsSource -Filter "*.md").Count
            Write-Success "Installed $count slash commands"
        }
    }
}

# ============================================================================
# Scripts Setup
# ============================================================================
if ($All -or $Scripts) {
    Write-Header "Setting up Utility Scripts"
    
    $scriptsSource = Join-Path $SETUP_DIR "scripts"
    $scriptsDest = Join-Path $ProjectRoot "scripts"
    
    if ($Uninstall) {
        $utils = Join-Path $scriptsDest "framework-utils.ps1"
        if (Test-Path $utils) {
            Remove-Item $utils -Force
            Write-Success "Removed: framework-utils.ps1"
        }
    } else {
        if (-not (Test-Path $scriptsDest)) {
            New-Item -ItemType Directory -Path $scriptsDest -Force | Out-Null
        }
        
        $utils = Join-Path $scriptsSource "framework-utils.ps1"
        if (Test-Path $utils) {
            Copy-Item $utils $scriptsDest -Force
            Write-Success "Installed: framework-utils.ps1"
            
            Write-Host ""
            Write-Host "Usage:" -ForegroundColor White
            Write-Host "  .\scripts\framework-utils.ps1 warm" -ForegroundColor Gray
            Write-Host "  .\scripts\framework-utils.ps1 stats" -ForegroundColor Gray
            Write-Host "  .\scripts\framework-utils.ps1 dashboard" -ForegroundColor Gray
        }
    }
}

# ============================================================================
# Summary
# ============================================================================
Write-Header "Setup Complete"

if (-not $Uninstall) {
    Write-Host "Installed components:" -ForegroundColor Green
    if ($All -or $Mcp) { Write-Host "  • MCP Servers" -ForegroundColor White }
    if ($All -or $Plugins) { Write-Host "  • Cursor Plugins" -ForegroundColor White }
    if ($All -or $Hooks) { Write-Host "  • Git Hooks" -ForegroundColor White }
    if ($All -or $Commands) { Write-Host "  • Slash Commands" -ForegroundColor White }
    if ($All -or $Scripts) { Write-Host "  • Utility Scripts" -ForegroundColor White }
    
    Write-Host ""
    Write-Host "Quick commands:" -ForegroundColor Yellow
    Write-Host "  .\scripts\framework-utils.ps1 warm      # Warm cache" -ForegroundColor Gray
    Write-Host "  .\scripts\framework-utils.ps1 stats     # View stats" -ForegroundColor Gray
    Write-Host "  .\scripts\framework-utils.ps1 dashboard # Open dashboard" -ForegroundColor Gray
} else {
    Write-Host "Uninstallation complete!" -ForegroundColor Green
}

Write-Host ""
