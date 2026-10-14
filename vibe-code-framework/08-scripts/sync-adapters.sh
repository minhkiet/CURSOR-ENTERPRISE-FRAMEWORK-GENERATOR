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
    [string]$SourcePath = (Split-Path $PSScriptRoot -Parent),
    
    [Parameter(Mandatory=$false)]
    [string]$TargetPath = $PWD.Path,

    [Parameter(Mandatory=$false)]
    [string]$ManifestPath = '',

    [Parameter(Mandatory=$false)]
    [switch]$AllowOverwrite
)

if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path $SourcePath '00-governance/resource-manifest.json'
}

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

function Test-ExecutionInput {
    if (-not (Test-Path -LiteralPath $SourcePath -PathType Container)) {
        Write-Host "❌ SourcePath must be an existing Resource Hub directory: $SourcePath" -ForegroundColor Red
        return $false
    }

    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        Write-Host "❌ ManifestPath must point to the canonical Resource Hub manifest: $ManifestPath" -ForegroundColor Red
        return $false
    }

    if (-not (Test-Path -LiteralPath $TargetPath -PathType Container)) {
        Write-Host "❌ TargetPath must be an existing consumer project directory: $TargetPath" -ForegroundColor Red
        return $false
    }

    $sourceFullPath = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $SourcePath).Path)
    $targetFullPath = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $TargetPath).Path)
    if ($sourceFullPath -eq $targetFullPath) {
        Write-Host "❌ TargetPath must not be the Resource Hub SourcePath" -ForegroundColor Red
        return $false
    }

    try {
        $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    } catch {
        Write-Host "❌ ManifestPath is not valid JSON: $ManifestPath" -ForegroundColor Red
        return $false
    }

    foreach ($requiredPath in $manifest.executionInputContract.sourcePath.mustContain) {
        if (-not (Test-Path -LiteralPath (Join-Path $SourcePath $requiredPath))) {
            Write-Host "❌ SourcePath is missing required canonical path: $requiredPath" -ForegroundColor Red
            return $false
        }
    }

    return $true
}

function Test-TargetFileWrite {
    param([string]$TargetFile)

    if ((Test-Path -LiteralPath $TargetFile -PathType Leaf) -and -not $AllowOverwrite) {
        Write-Warning "Target exists; skipped (pass -AllowOverwrite to replace): $TargetFile"
        return $false
    }

    return $true
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
    
    Get-ChildItem -LiteralPath $sourceDir -File | Where-Object { $_.Extension -eq '.md' -and $_.Name -ne 'README.md' } | ForEach-Object {
        $targetFile = Join-Path $targetDir ($_.BaseName + $Config.Extension)
        if (-not (Test-TargetFileWrite -TargetFile $targetFile)) { return }
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
    
    Get-ChildItem -LiteralPath $sourceDir -Directory | Where-Object { $_.Name -ne 'README.md' } | ForEach-Object {
        $targetSkillDir = Join-Path $targetDir $_.Name
        if (-not (Test-Path $targetSkillDir)) {
            New-Item -ItemType Directory -Path $targetSkillDir -Force | Out-Null
        }
        
        $skillFile = Join-Path $_.FullName "SKILL.md"
        if (Test-Path $skillFile) {
            $targetFile = Join-Path $targetSkillDir 'SKILL.md'
            if (-not (Test-TargetFileWrite -TargetFile $targetFile)) { return }
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
    
    Get-ChildItem -LiteralPath $sourceDir -File | Where-Object { $_.Extension -eq '.md' -and $_.Name -ne 'README.md' } | ForEach-Object {
        $targetFile = Join-Path $targetDir $_.Name
        if (-not (Test-TargetFileWrite -TargetFile $targetFile)) { return }
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

Write-Info "Source: $SourcePath"
Write-Info "Target: $TargetPath"
Write-Info "Manifest: $ManifestPath"
Write-Info "AllowOverwrite: $AllowOverwrite"

if (-not (Test-ExecutionInput)) {
    exit 1
}

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
