# ============================================================
# FRAMEWORK PACKAGER SCRIPT
# ============================================================
# Purpose: Package Cursor Enterprise Framework into ZIP
# Language: PowerShell
# Created: 2026-06-23
# ============================================================

param(
    [string]$SourcePath = ".cursor",
    [string]$OutputPath = "cursor-enterprise-framework-v4.zip",
    [string]$FrameworkVersion = "4.0.0",
    [switch]$IncludeScripts,
    [switch]$Verify
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Get-DirectoryStats {
    param([string]$Path, [string]$Filter = "*")

    $files = Get-ChildItem -Path $Path -Filter $Filter -Recurse -File -ErrorAction SilentlyContinue
    $totalSize = ($files | Measure-Object -Property Length -Sum).Sum
    $totalFiles = $files.Count
    $totalLines = 0

    foreach ($file in $files) {
        if ($file.Extension -match '\.(md|mdc|json|sql|ps1)$') {
            $lines = (Get-Content $file.FullName -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
            $totalLines += $lines
        }
    }

    return @{
        files = $totalFiles
        size_bytes = $totalSize
        size_mb = [Math]::Round($totalSize / 1MB, 2)
        lines = $totalLines
    }
}

function Test-FrameworkIntegrity {
    param([string]$Path)

    Write-Log "Verifying framework integrity..."

    $requiredDirs = @(
        "rules", "skills", "memory", "knowledge",
        "prompts", "workflows", "scripts"
    )

    $requiredFiles = @(
        "memory/project-index.json",
        "memory/context-router.json",
        "memory/technology-stack.json",
        "memory/business-rules.json"
    )

    $issues = @()

    foreach ($dir in $requiredDirs) {
        $dirPath = Join-Path $Path $dir
        if (-not (Test-Path $dirPath)) {
            $issues += "Missing directory: $dir"
        }
    }

    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $Path $file
        if (-not (Test-Path $filePath)) {
            $issues += "Missing file: $file"
        }
    }

    if ($issues.Count -gt 0) {
        Write-Log "Integrity issues found:" "WARN"
        foreach ($issue in $issues) {
            Write-Log "  - $issue" "WARN"
        }
        return $false
    }

    Write-Log "Framework integrity verified!" "SUCCESS"
    return $true
}

function Get-FrameworkStats {
    param([string]$Path)

    $stats = @{
        version = $FrameworkVersion
        generated_at = (Get-Date).ToString("o")
        rules = (Get-ChildItem -Path "$Path/rules" -Filter "*.mdc" -ErrorAction SilentlyContinue | Measure-Object).Count
        skills = (Get-ChildItem -Path "$Path/skills" -Filter "*.mdc" -ErrorAction SilentlyContinue | Measure-Object).Count
        knowledge_files = (Get-ChildItem -Path "$Path/knowledge" -Filter "*.md" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        knowledge_domains = (Get-ChildItem -Path "$Path/knowledge" -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
        prompts = (Get-ChildItem -Path "$Path/prompts" -Filter "*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
        workflows = (Get-ChildItem -Path "$Path/workflows" -Filter "*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
        scripts = (Get-ChildItem -Path "$Path/scripts" -Filter "*.ps1" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        memory_json = (Get-ChildItem -Path "$Path/memory" -Filter "*.json" -ErrorAction SilentlyContinue | Measure-Object).Count
        memory_sqlite = (Get-ChildItem -Path "$Path/memory/schema" -Filter "*.sql" -ErrorAction SilentlyContinue | Measure-Object).Count
    }

    return $stats
}

Write-Log "Cursor Enterprise Framework Packager v$FrameworkVersion"
Write-Log "=========================================="

# Verify framework
if ($Verify) {
    $integrity = Test-FrameworkIntegrity -Path $SourcePath
    if (-not $integrity) {
        Write-Log "Framework integrity check failed!" "ERROR"
        exit 1
    }
}

# Get stats
Write-Log "Gathering framework statistics..."
$stats = Get-FrameworkStats -Path $SourcePath

Write-Log "Framework Statistics:"
Write-Log "  Version: v$($stats.version)"
Write-Log "  Generated: $($stats.generated_at)"
Write-Log "  Rules: $($stats.rules)"
Write-Log "  Skills: $($stats.skills)"
Write-Log "  Knowledge Domains: $($stats.knowledge_domains)"
Write-Log "  Knowledge Files: $($stats.knowledge_files)"
Write-Log "  Prompts: $($stats.prompts)"
Write-Log "  Workflows: $($stats.workflows)"
Write-Log "  Scripts: $($stats.scripts)"
Write-Log "  Memory JSON: $($stats.memory_json)"
Write-Log "  Memory SQLite Schemas: $($stats.memory_sqlite)"

# Calculate total
$total = $stats.rules + $stats.skills + $stats.knowledge_files + $stats.prompts + $stats.workflows + $stats.scripts
Write-Log "  Total files: $total"

# Get directory size
$dirStats = Get-DirectoryStats -Path $SourcePath
Write-Log "  Total size: $($dirStats.size_mb) MB"
Write-Log "  Total lines: $($dirStats.lines)"

# Create ZIP
Write-Log "Creating ZIP archive..."
$tempDir = $env:TEMP
$tempZip = Join-Path $tempDir "cursor-framework-temp.zip"

if (Test-Path $OutputPath) {
    Remove-Item $OutputPath -Force
}

Compress-Archive -Path "$SourcePath/*" -DestinationPath $tempZip -Force

# Move to output
Move-Item -Path $tempZip -Destination $OutputPath -Force

$zipSize = (Get-Item $OutputPath).Length
$zipSizeMB = [Math]::Round($zipSize / 1MB, 2)

Write-Log "ZIP archive created: $OutputPath" "SUCCESS"
Write-Log "ZIP size: $zipSizeMB MB"

# Save stats to JSON
$stats | Add-Member -NotePropertyName "zip_file" -NotePropertyValue $OutputPath
$stats | Add-Member -NotePropertyName "zip_size_mb" -NotePropertyValue $zipSizeMB
$stats | Add-Member -NotePropertyName "total_files" -NotePropertyValue $total
$stats | Add-Member -NotePropertyName "total_lines" -NotePropertyValue $dirStats.lines

$statsPath = [System.IO.Path]::ChangeExtension($OutputPath, ".stats.json")
$stats | ConvertTo-Json -Depth 10 | Out-File -FilePath $statsPath -Encoding UTF8

Write-Log "Stats saved to: $statsPath" "SUCCESS"
Write-Log ""
Write-Log "Packaging complete!" "SUCCESS"
Write-Log "=========================================="
