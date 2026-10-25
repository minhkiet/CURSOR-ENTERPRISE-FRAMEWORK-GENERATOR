# Cursor Enterprise Framework - MCP Setup Script
# Auto-generated: 2026-08-09
# Run this script to set up all MCP servers

param(
    [switch]$Install,
    [switch]$Update,
    [switch]$Verify,
    [switch]$All
)

$ErrorActionPreference = "Stop"
$WorkspaceRoot = "D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
$McpServers = @(
    "cursor-framework-mcp",
    "cursor-autopilot-mcp", 
    "cursor-memory-mcp"
)

function Write-Step($message) {
    Write-Host "`n[STEP] $message" -ForegroundColor Cyan
}

function Write-Success($message) {
    Write-Host "[OK] $message" -ForegroundColor Green
}

function Write-Error-Message($message) {
    Write-Host "[ERROR] $message" -ForegroundColor Red
}

function Install-McpServer($serverName) {
    $serverPath = Join-Path $WorkspaceRoot "tools\$serverName"
    
    if (-not (Test-Path $serverPath)) {
        Write-Error-Message "$serverName not found at $serverPath"
        return $false
    }
    
    Write-Host "  Installing $serverName..." -NoNewline
    
    # Install dependencies
    $requirementsPath = Join-Path $serverPath "requirements.txt"
    if (Test-Path $requirementsPath) {
        pip install -r $requirementsPath 2>&1 | Out-Null
    }
    
    Write-Success "Installed"
    return $true
}

function Verify-McpServer($serverName) {
    $serverPath = Join-Path $WorkspaceRoot "tools\$serverName\cursor_$($serverName -replace '-mcp', '')_mcp"
    
    # Check if module can be imported
    $testScript = @"
import sys
sys.path.insert(0, r'$serverPath')
from $($serverName -replace '-', '_')_mcp import __version__
print(__version__)
"@
    
    try {
        $version = python -c $testScript 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$serverName v$version"
            return $true
        }
    }
    catch {
        Write-Error-Message "$serverName import failed"
        return $false
    }
    
    Write-Error-Message "$serverName verification failed"
    return $false
}

function Update-McpSettings($mcpConfigPath) {
    Write-Host "  Updating $mcpConfigPath..." -NoNewline
    
    $templatePath = Join-Path $WorkspaceRoot "tools\mcp-config-template.json"
    
    if (-not (Test-Path $templatePath)) {
        Write-Error-Message "Template not found"
        return $false
    }
    
    $targetDir = Split-Path $mcpConfigPath -Parent
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    
    Copy-Item $templatePath $mcpConfigPath -Force
    Write-Success "Updated"
    return $true
}

# Main execution
Write-Host @"

╔══════════════════════════════════════════════════════════════════╗
║     Cursor Enterprise Framework - MCP Setup                     ║
║     Version 1.0.0 | Framework 3.1.0                            ║
╚══════════════════════════════════════════════════════════════════╝

"@

if (-not $Install -and -not $Update -and -not $Verify -and -not $All) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  -Install    : Install all MCP servers"
    Write-Host "  -Update     : Update Cursor MCP settings"
    Write-Host "  -Verify     : Verify MCP servers are working"
    Write-Host "  -All        : Run all steps (Install + Update + Verify)"
    Write-Host ""
    Write-Host "Example: .\setup-mcp.ps1 -All"
    return
}

if ($All -or $Install) {
    Write-Step "Installing MCP Servers"
    Write-Host "Workspace: $WorkspaceRoot`n"
    
    $allSuccess = $true
    foreach ($server in $McpServers) {
        if (-not (Install-McpServer $server)) {
            $allSuccess = $false
        }
    }
    
    if ($allSuccess) {
        Write-Host "`n[SUCCESS] All MCP servers installed" -ForegroundColor Green
    }
    else {
        Write-Host "`n[WARN] Some servers failed to install" -ForegroundColor Yellow
    }
}

if ($All -or $Update) {
    Write-Step "Updating Cursor MCP Settings"
    
    # Determine OS and config path
    if ($IsWindows -or $true) {
        $mcpConfigPath = "$env:USERPROFILE\.cursor\mcp.json"
    }
    else {
        $mcpConfigPath = "$env:HOME/.config/cursor/mcp.json"
    }
    
    Write-Host "Target: $mcpConfigPath"
    
    if (Update-McpSettings $mcpConfigPath) {
        Write-Success "Cursor MCP settings updated"
        Write-Host "`nRestart Cursor to load the new MCP servers." -ForegroundColor Yellow
    }
}

if ($All -or $Verify) {
    Write-Step "Verifying MCP Servers"
    
    $allSuccess = $true
    foreach ($server in $McpServers) {
        if (-not (Verify-McpServer $server)) {
            $allSuccess = $false
        }
    }
    
    if ($allSuccess) {
        Write-Host "`n[SUCCESS] All MCP servers verified" -ForegroundColor Green
    }
    else {
        Write-Host "`n[WARN] Some servers failed verification" -ForegroundColor Yellow
    }
}

Write-Host @"

╔══════════════════════════════════════════════════════════════════╗
║                      MCP Stack Summary                          ║
╠══════════════════════════════════════════════════════════════════╣
║  1. cursor-framework    : Rules, Skills, Agents Registry       ║
║     Tools: get_rule, get_skill, get_agent, analyze_task,        ║
║            load_skill_bundle, get_essential_skills, clear_cache, ║
║            get_framework_status, optimize_framework              ║
║                                                                  ║
║  2. cursor-autopilot    : Auto-Execution Engine               ║
║     Tools: auto_execute, execute_workflow, run_gate_validation,  ║
║            get_workflow_status, abort_workflow, list_workflows,  ║
║            estimate_cost, suggest_optimization                   ║
║                                                                  ║
║  3. cursor-memory       : Context & Memory Management          ║
║     Tools: store_memory, recall_memory, compact_context,          ║
║            summarize_history, get_context_stats, prune_context,  ║
║            export_memory, import_memory, sync_to_disk            ║
║                                                                  ║
║  Total Tools: 26                                                ║
╚══════════════════════════════════════════════════════════════════╝

"@
