# ============================================================
# MEMORY BUILDER SCRIPT
# ============================================================
# Purpose: Build and update memory indexes
# Language: PowerShell
# Created: 2026-06-23
# ============================================================

param(
    [string]$MemoryPath = ".cursor/memory",
    [switch]$Full
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

function Initialize-SQLiteDB {
    param([string]$Path, [string]$Schema)

    if (-not (Test-Path $Path)) {
        Write-Log "Creating SQLite database: $Path"
        # SQLite schema would be executed here
        # For now, we verify the schema file exists
        if (Test-Path $Schema) {
            Write-Log "Schema found: $Schema" "SUCCESS"
        }
    }
}

Write-Log "Memory Builder started"
Write-Log "Memory Path: $MemoryPath"

# Ensure memory directory exists
if (-not (Test-Path $MemoryPath)) {
    New-Item -ItemType Directory -Path $MemoryPath -Force | Out-Null
}

# Ensure subdirectories exist
$subdirs = @("session-summary", "architecture-history", "decision-history", "bug-history", "schema")
foreach ($subdir in $subdirs) {
    $path = Join-Path $MemoryPath $subdir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Initialize SQLite databases
$schemaPath = Join-Path $MemoryPath "schema"
$dbFiles = @("decisions", "bugs", "prompt-cache", "knowledge", "embeddings", "sessions")
foreach ($db in $dbFiles) {
    $schema = Join-Path $schemaPath "$db.schema.sql"
    if (Test-Path $schema) {
        Write-Log "Database schema ready: $db" "SUCCESS"
    } else {
        Write-Log "Schema not found: $db" "WARN"
    }
}

# Build memory index
$index = @{
    built_at = (Get-Date).ToString("o")
    version = "1.0.0"
    components = @{
        session_summary = @{
            count = (Get-ChildItem -Path (Join-Path $MemoryPath "session-summary") -File -ErrorAction SilentlyContinue | Measure-Object).Count
        }
        architecture_history = @{
            count = (Get-ChildItem -Path (Join-Path $MemoryPath "architecture-history") -File -ErrorAction SilentlyContinue | Measure-Object).Count
        }
        decision_history = @{
            count = (Get-ChildItem -Path (Join-Path $MemoryPath "decision-history") -File -ErrorAction SilentlyContinue | Measure-Object).Count
        }
        bug_history = @{
            count = (Get-ChildItem -Path (Join-Path $MemoryPath "bug-history") -File -ErrorAction SilentlyContinue | Measure-Object).Count
        }
        sqlite_databases = $dbFiles
    }
}

$indexPath = Join-Path $MemoryPath "memory-index.json"
$index | ConvertTo-Json -Depth 10 | Out-File -FilePath $indexPath -Encoding UTF8

Write-Log "Memory index built!" "SUCCESS"
Write-Log "Session summaries: $($index.components.session_summary.count)"
Write-Log "Architecture history: $($index.components.architecture_history.count)"
Write-Log "Decision history: $($index.components.decision_history.count)"
Write-Log "Bug history: $($index.components.bug_history.count)"
Write-Log "SQLite databases: $($dbFiles.Count)"
