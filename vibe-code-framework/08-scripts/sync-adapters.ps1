# Sync Adapters Script - Full Version

<#
.SYNOPSIS
    Sync Vibe Code Framework adapters to tool-specific format.

.DESCRIPTION
    Converts source content from 01-core-rules, 03-skills, 04-agents, 05-workflows
    to tool-specific format (Cursor, Claude Code, Codex, Copilot, Windsurf, Antigravity)

.PARAMETER Tool
    The tool to sync adapters for: Cursor, ClaudeCode, Codex, Copilot, Windsurf, Antigravity, All
    Default: All

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
    .\sync-adapters.ps1 -Tool Cursor
    Sync all content to Cursor format

.EXAMPLE
    .\sync-adapters.ps1 -Tool All
    Sync to all supported tools
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('Cursor', 'ClaudeCode', 'Codex', 'Copilot', 'Windsurf', 'Antigravity', 'All')]
    [string]$Tool = 'All',
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('rules', 'skills', 'agents', 'workflows', 'all')]
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

function Write-Error($message) {
    Write-Host "❌ $message" -ForegroundColor Red
}

# Tool configurations
$ToolConfigs = @{
    Cursor = @{
        Rules = @{
            Source = "01-core-rules"
            Target = ".cursor\rules"
            Extension = ".mdc"
            Description = "Cursor Rules"
            HasFrontmatter = $true
        }
        Skills = @{
            Source = "03-skills"
            Target = ".cursor\skills"
            Extension = ".md"
            Description = "Cursor Skills"
        }
        Agents = @{
            Source = "04-agents"
            Target = ".cursor\agents"
            Extension = ".md"
            Description = "Cursor Agents"
        }
        Files = @(
            @{ Source = "07-adapters\cursor\AGENTS.md"; Target = ".cursor\AGENTS.md" }
        )
    }
    ClaudeCode = @{
        Rules = @{
            Source = "01-core-rules"
            Target = ".claude\rules"
            Extension = ".md"
            Description = "Claude Code Rules"
        }
        Skills = @{
            Source = "03-skills"
            Target = ".claude\skills"
            Extension = ".md"
            Description = "Claude Code Skills"
        }
        Agents = @{
            Source = "04-agents"
            Target = ".claude\agents"
            Extension = ".md"
            Description = "Claude Code Agents"
        }
        Files = @(
            @{ Source = "CLAUDE.md"; Target = ".claude\CLAUDE.md" }
        )
    }
    Codex = @{
        Skills = @{
            Source = "03-skills"
            Target = ".agents\skills"
            Extension = ".md"
            Description = "Codex Skills"
        }
        Agents = @{
            Source = "04-agents"
            Target = ".agents\agents"
            Extension = ".md"
            Description = "Codex Agents"
        }
        Files = @(
            @{ Source = "AGENTS.md"; Target = ".agents\AGENTS.md" }
        )
    }
    Copilot = @{
        Files = @(
            @{ Source = "07-adapters\copilot\copilot-instructions.md"; Target = ".github\copilot-instructions.md" }
        )
    }
    Windsurf = @{
        Rules = @{
            Source = "01-core-rules"
            Target = ".windsurf\rules"
            Extension = ".md"
            Description = "Windsurf Rules"
        }
    }
    Antigravity = @{
        Files = @(
            @{ Source = "GEMINI.md"; Target = ".antigravity\GEMINI.md" }
        )
    }
}

function Sync-Rules {
    param($Config, $SourcePath, $TargetPath)
    
    if (-not $Config) {
        Write-Warning "No rules config for this tool"
        return
    }
    
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
        $content = Get-Content $_.FullName -Raw
        
        # Add frontmatter for Cursor
        if ($Config.HasFrontmatter -and -not $content.StartsWith("---")) {
            $frontmatter = @"
---
description: $([System.IO.Path]::GetFileNameWithoutExtension($_.Name))
trigger: ""
version: 1.0.0
---

"@
            $content = $frontmatter + $content
        }
        
        $content | Set-Content -Path $targetFile -NoNewline
        Write-Success "Synced: $($_.Name) → $([System.IO.Path]::GetFileName($targetFile))"
    }
}

function Sync-Skills {
    param($Config, $SourcePath, $TargetPath)
    
    if (-not $Config) {
        Write-Warning "No skills config for this tool"
        return
    }
    
    $sourceDir = Join-Path $SourcePath $Config.Source
    $targetDir = Join-Path $TargetPath $Config.Target
    
    Write-Info "Syncing skills: $sourceDir → $targetDir"
    
    if (-not (Test-Path $sourceDir)) {
        Write-Warning "Source not found: $sourceDir"
        return
    }
    
    Get-ChildItem -Path $sourceDir -Directory -Exclude "README.md", "SKILL-FORMAT.md" | ForEach-Object {
        $targetSkillDir = Join-Path $targetDir $_.Name
        $skillFile = Join-Path $_.FullName "SKILL.md"
        
        if (-not (Test-Path $targetSkillDir)) {
            New-Item -ItemType Directory -Path $targetSkillDir -Force | Out-Null
        }
        
        if (Test-Path $skillFile) {
            Copy-Item -Path $skillFile -Destination $targetSkillDir -Force
            Write-Success "Synced: $($_.Name)/SKILL.md"
        }
    }
}

function Sync-Agents {
    param($Config, $SourcePath, $TargetPath)
    
    if (-not $Config) {
        Write-Warning "No agents config for this tool"
        return
    }
    
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

function Sync-Files {
    param($Files, $SourcePath, $TargetPath)
    
    if (-not $Files) {
        return
    }
    
    foreach ($file in $Files) {
        $sourceFile = Join-Path $SourcePath $file.Source
        $targetFile = Join-Path $TargetPath $file.Target
        
        if (-not (Test-Path $sourceFile)) {
            Write-Warning "Source file not found: $sourceFile"
            continue
        }
        
        $targetDir = Split-Path $targetFile -Parent
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        
        Copy-Item -Path $sourceFile -Destination $targetFile -Force
        Write-Success "Synced: $file.Source → $file.Target"
    }
}

function Sync-Tool {
    param($ToolName)
    
    if (-not $ToolConfigs.ContainsKey($ToolName)) {
        Write-Warning "Tool not supported: $ToolName"
        return
    }
    
    $config = $ToolConfigs[$ToolName]
    Write-Info ""
    Write-Info "═══════════════════════════════════════════════════"
    Write-Info "  Syncing: $ToolName"
    Write-Info "═══════════════════════════════════════════════════"
    
    if ($Category -eq "all" -or $Category -eq "rules") {
        Sync-Rules -Config $config.Rules -SourcePath $SourcePath -TargetPath $TargetPath
    }
    
    if ($Category -eq "all" -or $Category -eq "skills") {
        Sync-Skills -Config $config.Skills -SourcePath $SourcePath -TargetPath $TargetPath
    }
    
    if ($Category -eq "all" -or $Category -eq "agents") {
        Sync-Agents -Config $config.Agents -SourcePath $SourcePath -TargetPath $TargetPath
    }
    
    if ($config.Files) {
        Sync-Files -Files $config.Files -SourcePath $SourcePath -TargetPath $TargetPath
    }
    
    Write-Success "Completed: $ToolName"
}

# Main
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "   Vibe Code Framework — Adapter Sync" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""
Write-Info "Source: $SourcePath"
Write-Info "Target: $TargetPath"
Write-Info "Tool: $Tool"
Write-Info "Category: $Category"
Write-Host ""

if ($Tool -eq "All") {
    foreach ($toolName in $ToolConfigs.Keys) {
        Sync-Tool -ToolName $toolName
    }
} else {
    Sync-Tool -ToolName $Tool
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Success "All syncs completed!"
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
