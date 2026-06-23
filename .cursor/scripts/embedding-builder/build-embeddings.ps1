# ============================================================
# EMBEDDING BUILDER SCRIPT
# ============================================================
# Purpose: Build embeddings for knowledge base
# Language: PowerShell
# Created: 2026-06-23
# ============================================================

param(
    [string]$InputPath = ".cursor/knowledge",
    [string]$OutputPath = ".cursor/vector-db",
    [string]$Model = "text-embedding-3-small",
    [string]$Dimensions = "1536",
    [switch]$Incremental
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

function Get-TextChunks {
    param([string]$FilePath, [int]$ChunkSize = 500, [int]$Overlap = 50)

    $content = Get-Content $FilePath -Raw
    $lines = $content -split "`n"
    $chunks = @()
    $currentChunk = @()
    $currentLength = 0

    foreach ($line in $lines) {
        $lineLength = $line.Length
        if ($currentLength + $lineLength -gt $ChunkSize) {
            $chunks += $currentChunk -join "`n"
            $currentChunk = $currentChunk[-1..-1]
            if ($currentChunk.Count -gt ($Overlap / 20)) {
                $currentChunk = $currentChunk[(-[Math]::Min($Overlap / 20, $currentChunk.Count))..-1]
            }
            $currentLength = ($currentChunk | ForEach-Object { $_.Length }) -join "+" | Invoke-Expression
        }
        $currentChunk += $line
        $currentLength += $lineLength
    }

    if ($currentChunk.Count -gt 0) {
        $chunks += $currentChunk -join "`n"
    }

    return $chunks
}

function New-Embedding {
    param([string]$Text, [string]$Model, [int]$Dimensions)

    # Placeholder for embedding API call
    # In production, replace with actual OpenAI/Gemini API call
    $embedding = @{
        text = $Text
        model = $Model
        dimensions = $Dimensions
        vector = @()
        created_at = (Get-Date).ToString("o")
    }

    # Generate placeholder vector (random for demo)
    for ($i = 0; $i -lt $Dimensions; $i++) {
        $embedding.vector += [Math]::Round((Get-Random -Minimum -1 -Maximum 1), 4)
    }

    return $embedding
}

Write-Log "Embedding Builder started"
Write-Log "Input: $InputPath"
Write-Log "Output: $OutputPath"
Write-Log "Model: $Model"
Write-Log "Dimensions: $Dimensions"

# Create output directory
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
}

# Get all knowledge files
$files = Get-ChildItem -Path $InputPath -Filter "*.md" -Recurse -File
Write-Log "Found $($files.Count) knowledge files"

$allEmbeddings = @()
$stats = @{
    files_processed = 0
    chunks_created = 0
    errors = 0
}

foreach ($file in $files) {
    try {
        Write-Log "Processing: $($file.FullName)"
        $chunks = Get-TextChunks -FilePath $file.FullName -ChunkSize 500 -Overlap 50

        foreach ($chunk in $chunks) {
            if ($chunk.Length -lt 10) { continue }

            $embedding = New-Embedding -Text $chunk -Model $Model -Dimensions $Dimensions
            $embedding | Add-Member -NotePropertyName "source_file" -NotePropertyValue $file.FullName -PassThru
            $embedding | Add-Member -NotePropertyName "source_domain" -NotePropertyValue ($file.Directory.Name) -PassThru
            $allEmbeddings += $embedding
            $stats.chunks_created++
        }

        $stats.files_processed++
    }
    catch {
        Write-Log "Error processing $($file.FullName): $_" "ERROR"
        $stats.errors++
    }
}

# Save embeddings
$outputFile = Join-Path $OutputPath "embeddings-$((Get-Date).ToString('yyyyMMdd-HHmmss')).json"
$allEmbeddings | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding UTF8

Write-Log "Embedding build complete!" "SUCCESS"
Write-Log "Files processed: $($stats.files_processed)"
Write-Log "Chunks created: $($stats.chunks_created)"
Write-Log "Errors: $($stats.errors)"
Write-Log "Output: $outputFile"
