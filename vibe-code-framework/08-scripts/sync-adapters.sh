#!/usr/bin/env pwsh
# Sync Adapters Script for Unix/macOS (PowerShell Core)

<#
.SYNOPSIS
    Sync Vibe Code Framework adapters to tool-specific format.

.DESCRIPTION
    Converts source content from 01-core-rules, 03-skills, 04-agents
    to tool-specific format (Cursor, Claude Code, Codex, etc.)

.PARAMETER Tool
    The tool to sync adapters for: cursor, claude, codex, all
    Default: all

.PARAMETER Category
    The category to sync: rules, skills, agents, all
    Default: all

.PARAMETER SourcePath
    Path to the framework source
    Default: Script directory

.PARAMETER TargetPath
    Path to the target project
    Default: Parent of SourcePath

.EXAMPLE
    ./sync-adapters.ps1 -Tool cursor
    Sync all content to Cursor format

.EXAMPLE
    ./sync-adapters.sh --tool claude
    Sync all content to Claude Code format
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('cursor', 'claude', 'codex', 'copilot', 'all')]
    [string]$Tool = 'all',
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('rules', 'skills', 'agents', 'all')]
    [string]$Category = 'all',
    
    [Parameter(Mandatory=$false)]
    [string]$SourcePath = $PSScriptRoot,
    
    [Parameter(Mandatory=$false)]
    [string]$TargetPath = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
)

# Colors for output
function Write-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

function Write-Info($message) {
    Write-Host "ℹ️  $message" -ForegroundColor Cyan
}

function Write-Warning($message) {
    Write-Host "⚠️  $message" -ForegroundColor Yellow
}

# Tool configurations
$ToolConfigs = @{
    cursor = @{
        Rules = @{
            Source = "01-core-rules"
            Target = ".cursor/rules"
            Extension = ".mdc"
        }
        Skills = @{
            Source = "03-skills"
            Target = ".cursor/skills"
            Extension = ".md"
        }
        Agents = @{
            Source = "04-agents"
            Target = ".cursor/agents"
            Extension = ".md"
        }
    }
    claude = @{
        Rules = @{
            Source = "01-core-rules"
            Target = ".claude/rules"
            Extension = ".md"
        }
        Skills = @{
            Source = "03-skills"
            Target = ".claude/skills"
            Extension = ".md"
        }
        Agents = @{
            Source = "04-agents"
            Target = ".claude/agents"
            Extension = ".md"
        }
    }
}

function Sync-Rules {
    param($Config, $SourcePath, $TargetPath)
    
    $sourceDir = Join-Path $SourcePath $Config.Source
    $targetDir = Join-Path $TargetPath $Config.Target
    
    Write-Info "Syncing rules: $sourceDir → $targetDir"
    
    if (-not (Test-Path $sourceDir)) {
        Write-Warning "Source not found: $sourceDir"
        return
    }
    
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    
    Get-ChildItem -Path $sourceDir -Filter "*.md" -File -Exclude "README.md" | ForEach-Object {
        $targetFile = Join-Path $targetDir ($_.BaseName + $Config.Extension)
        Copy-Item -Path $_.FullName -Destination $targetFile -Force
        Write-Success "Synced: $($_.Name)"
    }
}

function Sync-Skills {
    param($Config, $SourcePath, $TargetPath)
    
    $sourceDir = Join-Path $SourcePath $Config.Source
    $targetDir = Join-Path $TargetPath $Config.Target
    
    Write-Info "Syncing skills: $sourceDir → $targetDir"
    
    if (-not (Test-Path $sourceDir)) {
        Write-Warning "Source not found: $sourceDir"
        return
    }
    
    Get-ChildItem -Path $sourceDir -Directory -Exclude "README.md" | ForEach-Object {
        $targetSkillDir = Join-Path $targetDir $_.Name
        if (-not (Test-Path $targetSkillDir)) {
            New-Item -ItemType Directory -Path $targetSkillDir -Force | Out-Null
        }
        
        $skillFile = Join-Path $_.FullName "SKILL.md"
        if (Test-Path $skillFile) {
            Copy-Item -Path $skillFile -Destination $targetSkillDir -Force
            Write-Success "Synced: $($_.Name)/SKILL.md"
        }
    }
}

function Sync-Agents {
    param($Config, $SourcePath, $TargetPath)
    
    $sourceDir = Join-Path $SourcePath $Config.Source
    $targetDir = Join-Path $TargetPath $Config.Target
    
    Write-Info "Syncing agents: $sourceDir → $targetDir"
    
    if (-not (Test-Path $sourceDir)) {
        Write-Warning "Source not found: $sourceDir"
        return
    }
    
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    
    Get-ChildItem -Path $sourceDir -Filter "*.md" -File -Exclude "README.md" | ForEach-Object {
        $targetFile = Join-Path $targetDir $_.Name
        Copy-Item -Path $_.FullName -Destination $targetFile -Force
        Write-Success "Synced: $($_.Name)"
    }
}

function Sync-Tool {
    param($ToolName)
    
    if (-not $ToolConfigs.ContainsKey($ToolName)) {
        Write-Warning "Tool not supported: $ToolName"
        return
    }
    
    $config = $ToolConfigs[$ToolName]
    Write-Info "=== Syncing $ToolName ==="
    
    if ($Category -eq "all" -or $Category -eq "rules") {
        Sync-Rules -Config $config.Rules -SourcePath $SourcePath -TargetPath $TargetPath
    }
    
    if ($Category -eq "all" -or $Category -eq "skills") {
        Sync-Skills -Config $config.Skills -SourcePath $SourcePath -TargetPath $TargetPath
    }
    
    if ($Category -eq "all" -or $Category -eq "agents") {
        Sync-Agents -Config $config.Agents -SourcePath $SourcePath -TargetPath $TargetPath
    }
}

# Main
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "   Vibe Code Framework — Adapter Sync" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

if ($Tool -eq "all") {
    foreach ($toolName in $ToolConfigs.Keys) {
        Write-Host ""
        Sync-Tool -ToolName $toolName
    }
} else {
    Sync-Tool -ToolName $Tool
}

Write-Host ""
Write-Success "Sync completed!"
