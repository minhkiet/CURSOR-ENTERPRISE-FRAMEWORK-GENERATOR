# ============================================================
# KNOWLEDGE COMPILER SCRIPT
# ============================================================
# Purpose: Compile and merge knowledge documents
# Language: PowerShell
# Created: 2026-06-23
# ============================================================

param(
    [string]$KnowledgePath = ".cursor/knowledge",
    [string]$OutputPath = ".cursor/cache/compiled",
    [string]$Format = "json",
    [switch]$Verbose
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

function Get-KnowledgeFiles {
    param([string]$Path)
    Get-ChildItem -Path $Path -Filter "*.md" -Recurse -File
}

function Merge-KnowledgeDocument {
    param([string]$Domain, [string]$OutputPath)
    $domainPath = Join-Path $KnowledgePath $Domain
    if (-not (Test-Path $domainPath)) {
        Write-Log "Domain not found: $Domain" "WARN"
        return
    }

    $files = Get-KnowledgeFiles $domainPath
    $merged = @{
        domain = $Domain
        compiled_at = (Get-Date).ToString("o")
        file_count = $files.Count
        sections = @{}
    }

    foreach ($file in $files) {
        $sectionName = $file.BaseName
        $content = Get-Content $file.FullName -Raw
        $merged.sections[$sectionName] = @{
            path = $file.FullName
            content = $content
            size = $content.Length
            lines = (Get-Content $file.FullName).Count
        }
        Write-Log "Merged: $($file.Name)" -Level "SUCCESS"
    }

    $merged | ConvertTo-Json -Depth 10
}

function New-KnowledgeIndex {
    param([string]$KnowledgePath)

    $index = @{
        generated_at = (Get-Date).ToString("o")
        domains = @{}
        total_files = 0
    }

    $domains = Get-ChildItem -Path $KnowledgePath -Directory
    foreach ($domain in $domains) {
        $files = Get-KnowledgeFiles $domain.FullName
        $index.domains[$domain.Name] = @{
            file_count = $files.Count
            files = @($files | ForEach-Object { $_.Name })
        }
        $index.total_files += $files.Count
    }

    $index | ConvertTo-Json -Depth 10
}

Write-Log "Starting Knowledge Compiler"
Write-Log "Knowledge Path: $KnowledgePath"
Write-Log "Output Path: $OutputPath"

# Create output directory
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
}

# Generate index
Write-Log "Generating knowledge index..."
$index = New-KnowledgeIndex -KnowledgePath $KnowledgePath
$indexPath = Join-Path $OutputPath "knowledge-index.json"
$index | Out-File -FilePath $indexPath -Encoding UTF8
Write-Log "Index saved to: $indexPath" "SUCCESS"

# Compile each domain
Write-Log "Compiling domains..."
$domains = Get-ChildItem -Path $KnowledgePath -Directory
foreach ($domain in $domains) {
    Write-Log "Compiling domain: $($domain.Name)"
    $compiled = Merge-KnowledgeDocument -Domain $domain.Name -OutputPath $OutputPath
    $domainPath = Join-Path $OutputPath "$($domain.Name).json"
    $compiled | Out-File -FilePath $domainPath -Encoding UTF8
    Write-Log "Domain compiled: $domainPath" "SUCCESS"
}

# Generate summary
$summary = @{
    compiled_at = (Get-Date).ToString("o")
    total_domains = $domains.Count
    total_files = $index.total_files
    output_path = $OutputPath
}
$summaryPath = Join-Path $OutputPath "summary.json"
$summary | ConvertTo-Json | Out-File -FilePath $summaryPath -Encoding UTF8

Write-Log "Knowledge compilation complete!" "SUCCESS"
Write-Log "Total domains: $($domains.Count)"
Write-Log "Total files: $($index.total_files)"
