# Install Script for Windows

<#
.SYNOPSIS
    Install Vibe Code Framework to target project.

.DESCRIPTION
    Copies framework adapters to the target project's configuration directories.

.PARAMETER Tool
    Tool to install for: Cursor, ClaudeCode, Codex, Copilot, Windsurf, Antigravity, All
    Default: All

.PARAMETER TargetPath
    Path to target project
    Required: an explicit consumer project directory outside the Resource Hub

.PARAMETER Backup
    Create backup before installing
    Default: true

.EXAMPLE
    .\install.ps1 -Tool Cursor -SourcePath "C:\Framework\vibe-code-framework" -TargetPath "C:\Projects\MyApp"
    Install Cursor adapter

.EXAMPLE
    .\install.ps1 -Tool All -SourcePath "C:\Framework\vibe-code-framework" -TargetPath "C:\Projects\MyApp"
    Install all adapters to MyApp project
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('Cursor', 'ClaudeCode', 'Codex', 'Copilot', 'Windsurf', 'Antigravity', 'All')]
    [string]$Tool = 'All',
    
    [Parameter(Mandatory=$false)]
    [string]$TargetPath = '',
    
    [Parameter(Mandatory=$false)]
    [switch]$Backup = $true,
    
    [Parameter(Mandatory=$false)]
    [string]$SourcePath = (Split-Path $PSScriptRoot -Parent),

    [Parameter(Mandatory=$false)]
    [string]$ManifestPath = ''
)

if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path $SourcePath '00-governance\resource-manifest.json'
}

# Colors
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

function Test-ExecutionInput {
    if ([string]::IsNullOrWhiteSpace($TargetPath)) {
        Write-Error "TargetPath is required; provide an explicit consumer project directory"
        return $false
    }

    if (-not (Test-Path -LiteralPath $SourcePath -PathType Container)) {
        Write-Error "SourcePath must be an existing Resource Hub directory: $SourcePath"
        return $false
    }

    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        Write-Error "ManifestPath must point to the canonical Resource Hub manifest: $ManifestPath"
        return $false
    }

    $sourceFullPath = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $SourcePath).Path)
    $targetFullPath = [IO.Path]::GetFullPath($TargetPath)
    $sourcePrefix = $sourceFullPath.TrimEnd('\', '/') + '\'
    $targetPrefix = $targetFullPath.TrimEnd('\', '/') + '\'
    if ($sourceFullPath.Equals($targetFullPath, [StringComparison]::OrdinalIgnoreCase) -or
        $targetFullPath.StartsWith($sourcePrefix, [StringComparison]::OrdinalIgnoreCase) -or
        $sourceFullPath.StartsWith($targetPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        Write-Error "TargetPath must be an external consumer directory, not the Resource Hub or a parent/child of it"
        return $false
    }

    try {
        $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    } catch {
        Write-Error "ManifestPath is not valid JSON: $ManifestPath"
        return $false
    }

    foreach ($requiredPath in $manifest.executionInputContract.sourcePath.mustContain) {
        if (-not (Test-Path -LiteralPath (Join-Path $SourcePath $requiredPath))) {
            Write-Error "SourcePath is missing required canonical path: $requiredPath"
            return $false
        }
    }

    return $true
}

# Install configurations
$InstallConfigs = @{
    Cursor = @{
        Directories = @(
            @{ Source = "07-adapters\cursor\rules"; Target = ".cursor\rules" },
            @{ Source = "07-adapters\cursor"; Target = ".cursor"; FilesOnly = $true }
        )
        Files = @("AGENTS.md")
        Description = "Cursor IDE"
    }
    ClaudeCode = @{
        Directories = @(
            @{ Source = "07-adapters\claude-code"; Target = ".claude" }
        )
        Description = "Claude Code"
    }
    Codex = @{
        Directories = @(
            @{ Source = "07-adapters\codex"; Target = ".agents" }
        )
        Files = @("AGENTS.md")
        Description = "OpenAI Codex"
    }
    Copilot = @{
        Directories = @(
            @{ Source = "07-adapters\copilot"; Target = ".github" }
        )
        Description = "GitHub Copilot"
    }
    Windsurf = @{
        Directories = @(
            @{ Source = "07-adapters\windsurf"; Target = ".windsurf" }
        )
        Description = "Windsurf"
    }
    Antigravity = @{
        Directories = @(
            @{ Source = "07-adapters\antigravity"; Target = ".antigravity" }
        )
        Files = @("GEMINI.md")
        Description = "Google Antigravity"
    }
}

function Backup-Directory {
    param($Path)
    
    if (Test-Path $Path) {
        $backupPath = "$Path.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Write-Info "Creating backup: $backupPath"
        Copy-Item -Path $Path -Destination $backupPath -Recurse -Force
        Write-Success "Backup created: $backupPath"
    }
}

function Install-Tool {
    param($ToolName)
    
    $config = $InstallConfigs[$ToolName]
    if (-not $config) {
        Write-Warning "Unknown tool: $ToolName"
        return
    }
    
    Write-Info ""
    Write-Info "═══════════════════════════════════════════════════"
    Write-Info "  Installing: $ToolName ($($config.Description))"
    Write-Info "═══════════════════════════════════════════════════"
    
    $targetDir = Join-Path $TargetPath ""
    
    # Install directories
    foreach ($dir in $config.Directories) {
        $source = Join-Path $SourcePath $dir.Source
        $target = Join-Path $targetDir $dir.Target
        
        if (Test-Path $source) {
            # Backup existing
            if ($Backup -and (Test-Path $target)) {
                Backup-Directory -Path $target
            }
            
            # Create target directory
            if (-not (Test-Path $target)) {
                New-Item -ItemType Directory -Path $target -Force | Out-Null
            }
            
            # Copy contents
            if ($dir.FilesOnly) {
                # Copy specific files
                Get-ChildItem -Path $source -File | ForEach-Object {
                    Copy-Item -Path $_.FullName -Destination $target -Force
                    Write-Success "Installed: $($_.Name)"
                }
            } else {
                # Copy directory contents
                Copy-Item -Path "$source\*" -Destination $target -Recurse -Force -ErrorAction SilentlyContinue
                Write-Success "Installed: $source → $target"
            }
        } else {
            Write-Warning "Source not found: $source"
        }
    }
    
    # Install root files
    if ($config.Files) {
        foreach ($file in $config.Files) {
            $source = Join-Path $SourcePath $file
            $target = Join-Path $targetDir $file
            
            if (Test-Path $source) {
                if ($Backup -and (Test-Path $target)) {
                    Backup-Directory -Path $target
                }
                Copy-Item -Path $source -Destination $target -Force
                Write-Success "Installed: $file"
            }
        }
    }
    
    Write-Success "Installed: $ToolName"
}

# Main
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "   Vibe Code Framework — Installer" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""
Write-Info "Source: $SourcePath"
Write-Info "Target: $TargetPath"
Write-Info "Tool: $Tool"
Write-Info "Backup: $Backup"
Write-Info "Manifest: $ManifestPath"
Write-Host ""

if (-not (Test-ExecutionInput)) {
    exit 1
}

if (-not (Test-Path $TargetPath)) {
    Write-Info "Creating target directory: $TargetPath"
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

if ($Tool -eq "All") {
    foreach ($toolName in $InstallConfigs.Keys) {
        Install-Tool -ToolName $toolName
    }
} else {
    Install-Tool -ToolName $Tool
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Success "Installation completed!"
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Info "Next steps:"
Write-Info "  1. Review installed files"
Write-Info "  2. Customize for your project"
Write-Info "  3. Commit to version control"
