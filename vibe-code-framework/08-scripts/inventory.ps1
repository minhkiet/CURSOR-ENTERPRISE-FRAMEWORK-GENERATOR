# Resource Hub inventory and .cursor classification

<##
.SYNOPSIS
    Inventory the host repository and classify .cursor resources without modifying files.

.PARAMETER ProjectPath
    Host project containing the .cursor boundary.
    Default: parent of the Resource Hub directory.

.PARAMETER OutputPath
    Optional JSON output path. Without it, only a compact summary is printed.
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent),

    [Parameter(Mandatory=$false)]
    [string]$OutputPath = ''
)

$cursorPath = Join-Path $ProjectPath '.cursor'
if (-not (Test-Path -LiteralPath $cursorPath -PathType Container)) {
    Write-Error "Cursor boundary not found: $cursorPath"
    exit 1
}

function Get-Classification {
    param([string]$RelativePath)

    $topLevel = ($RelativePath -split '[\\/]')[0]
    switch ($topLevel.ToLowerInvariant()) {
        'cache' { return 'GENERATED_RESOURCE' }
        'memory' { return 'GENERATED_RESOURCE' }
        'context.json' { return 'GENERATED_RESOURCE' }
        'rules' { return 'CURSOR_SPECIFIC' }
        'agent-skills' { return 'LEGACY_RESOURCE' }
        'agents' { return 'CURSOR_SPECIFIC' }
        'commands' { return 'CURSOR_SPECIFIC' }
        'hooks' { return 'CURSOR_SPECIFIC' }
        'mcp' { return 'CURSOR_SPECIFIC' }
        'scripts' { return 'CURSOR_SPECIFIC' }
        'agents.md' { return 'PROJECT_SPECIFIC' }
        'project.md' { return 'PROJECT_SPECIFIC' }
        'cursor.json' { return 'PROJECT_SPECIFIC' }
        'mcp.json' { return 'PROJECT_SPECIFIC' }
        default { return 'UNKNOWN_RESOURCE' }
    }
}

function Get-ResourceId {
    param([string]$RelativePath)

    $slug = ($RelativePath -replace '[\\/]', '-' -replace '[^A-Za-z0-9_.-]', '-')
    return "cursor-resource-$slug"
}

$records = @(
    Get-ChildItem -LiteralPath $cursorPath -Recurse -File -Force | ForEach-Object {
        $relativePath = [IO.Path]::GetRelativePath($cursorPath, $_.FullName)
        $classification = Get-Classification -RelativePath $relativePath
        $requiresReview = $classification -in @('UNKNOWN_RESOURCE', 'LEGACY_RESOURCE', 'CURSOR_SPECIFIC', 'PROJECT_SPECIFIC')
        [pscustomobject]@{
            resourceId = Get-ResourceId -RelativePath $relativePath
            path = ".cursor/$($relativePath -replace '\\','/')"
            classification = $classification
            sourceType = if ($classification -eq 'GENERATED_RESOURCE') { 'SOT-GENERATED' } else { 'SOT-UNKNOWN' }
            sizeBytes = $_.Length
            canonicalSource = $null
            owner = $null
            maintainer = $null
            consumers = @()
            dependencies = @()
            version = $null
            distributionMethod = $null
            evidenceIds = @()
            reviewStatus = if ($classification -eq 'UNKNOWN_RESOURCE') { 'BLOCKED' } else { 'UNREVIEWED' }
            approvalRequired = $requiresReview
            rollbackRequired = $requiresReview
            notes = if ($classification -eq 'UNKNOWN_RESOURCE') {
                'Classification, owner, dependency, consumer, canonical source, approval, and rollback evidence required; no migration authorized.'
            } else {
                'Inventory observation only; no migration or deletion authorized.'
            }
        }
    }
)

$summary = [ordered]@{
    projectPath = (Resolve-Path -LiteralPath $ProjectPath).Path
    cursorPath = $cursorPath
    resourceCount = $records.Count
    classificationCounts = [ordered]@{}
    reviewQueueCount = @($records | Where-Object { $_.classification -eq 'UNKNOWN_RESOURCE' }).Count
    records = $records
}

foreach ($group in ($records | Group-Object classification | Sort-Object Name)) {
    $summary.classificationCounts[$group.Name] = $group.Count
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    ([pscustomobject]$summary) | Select-Object projectPath, cursorPath, resourceCount, classificationCounts | ConvertTo-Json -Depth 5
} else {
    $outputDirectory = Split-Path -Parent $OutputPath
    if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    ([pscustomobject]$summary) | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputPath -Encoding utf8
    Write-Output "Inventory written: $OutputPath"
}
