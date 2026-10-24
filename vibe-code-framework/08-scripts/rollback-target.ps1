# Target-only rollback and restore verification.

<#!
.SYNOPSIS
    Snapshot, restore, or verify one explicitly selected adapter target.

.DESCRIPTION
    Creates a content-addressed backup of one target directory and restores
    only that directory. The Resource Hub and repository-wide .cursor tree
    are intentionally rejected as targets.

.PARAMETER Mode
    Snapshot, Restore, or Verify.

.PARAMETER TargetPath
    The exact affected consumer/adapter directory. Do not pass a repository
    root or the whole .cursor directory.

.PARAMETER BackupPath
    A caller-owned backup directory outside the Resource Hub.

.PARAMETER FrameworkPath
    Resource Hub root. Defaults to the parent of this script directory.

.PARAMETER ConfirmRestore
    Required for Restore because restoring replaces the selected target
    contents. The replacement remains limited to TargetPath.
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('Snapshot', 'Restore', 'Verify')]
    [string]$Mode,

    [Parameter(Mandatory=$true)]
    [string]$TargetPath,

    [Parameter(Mandatory=$true)]
    [string]$BackupPath,

    [Parameter(Mandatory=$false)]
    [string]$FrameworkPath = (Split-Path $PSScriptRoot -Parent),

    [Parameter(Mandatory=$false)]
    [switch]$ConfirmRestore
)

$ErrorActionPreference = 'Stop'

function Get-FullPath {
    param([string]$Path, [bool]$MustExist = $false)

    if ($MustExist) {
        return [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $Path).Path)
    }
    return [IO.Path]::GetFullPath($Path)
}

function Test-SameOrChildPath {
    param([string]$Candidate, [string]$Root)

    $candidateFull = (Get-FullPath $Candidate).TrimEnd('\', '/')
    $rootFull = (Get-FullPath $Root).TrimEnd('\', '/')
    return $candidateFull.Equals($rootFull, [StringComparison]::OrdinalIgnoreCase) -or
        $candidateFull.StartsWith($rootFull + '\', [StringComparison]::OrdinalIgnoreCase)
}

function Stop-Safely {
    param([string]$Message)
    throw $Message
}

$framework = Get-FullPath $FrameworkPath $true
$target = Get-FullPath $TargetPath $true
$backup = Get-FullPath $BackupPath $false

if (-not (Test-Path -LiteralPath $target -PathType Container)) {
    Stop-Safely "TargetPath must be an existing directory: $target"
}

if (Test-SameOrChildPath $target $framework) {
    Stop-Safely "TargetPath must be outside the Resource Hub: $target"
}

if (Test-SameOrChildPath $framework $target) {
    Stop-Safely "TargetPath must not contain the Resource Hub: $target"
}

if ((Get-FullPath $target).TrimEnd('\', '/') -eq ([IO.Path]::GetPathRoot($target)).TrimEnd('\', '/')) {
    Stop-Safely "TargetPath must be a narrow affected directory, not a filesystem root: $target"
}

if (Test-Path -LiteralPath (Join-Path $target '.git')) {
    Stop-Safely "TargetPath must not be a repository root containing .git: $target"
}

$targetLeaf = Split-Path -Leaf $target
if ($targetLeaf -in @('.git', '.cursor')) {
    Stop-Safely "TargetPath must be a narrow affected directory, not '$targetLeaf': $target"
}

if (Test-SameOrChildPath $backup $target) {
    Stop-Safely "BackupPath must be outside TargetPath: $backup"
}

if (Test-SameOrChildPath $backup $framework) {
    Stop-Safely "BackupPath must be outside the Resource Hub: $backup"
}

$manifestPath = Join-Path $backup 'rollback-manifest.json'
$payloadPath = Join-Path $backup 'payload'

function Get-FileRecords {
    param([string]$Root)

    $rootFull = (Get-FullPath $Root $true).TrimEnd('\', '/')
    $files = @(Get-ChildItem -LiteralPath $rootFull -File -Recurse -Force)
    return @($files | ForEach-Object {
        $relative = $_.FullName.Substring($rootFull.Length).TrimStart('\', '/')
        [pscustomobject]@{
            path = $relative.Replace('\', '/')
            length = $_.Length
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })
}

function Read-RollbackManifest {
    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
        Stop-Safely "Rollback manifest not found: $manifestPath"
    }

    try {
        return Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    } catch {
        Stop-Safely "Rollback manifest is invalid JSON: $manifestPath"
    }
}

function Assert-PayloadMatchesManifest {
    param($Manifest)

    if (-not (Test-Path -LiteralPath $payloadPath -PathType Container)) {
        Stop-Safely "Rollback payload directory not found: $payloadPath"
    }

    $expected = @($Manifest.files)
    $actual = @(Get-FileRecords $payloadPath)
    if ($actual.Count -ne $expected.Count) {
        Stop-Safely "Rollback payload file count differs: expected=$($expected.Count), actual=$($actual.Count)"
    }

    foreach ($record in $expected) {
        $actualRecord = $actual | Where-Object path -eq $record.path | Select-Object -First 1
        if (-not $actualRecord) {
            Stop-Safely "Rollback payload is missing: $($record.path)"
        }
        if ($actualRecord.sha256 -ne $record.sha256 -or [int64]$actualRecord.length -ne [int64]$record.length) {
            Stop-Safely "Rollback payload hash/length mismatch: $($record.path)"
        }
    }
}

function Assert-TargetMatchesManifest {
    param($Manifest)

    $expected = @($Manifest.files)
    $actual = @(Get-FileRecords $target)
    if ($actual.Count -ne $expected.Count) {
        Stop-Safely "Target file count differs: expected=$($expected.Count), actual=$($actual.Count)"
    }

    foreach ($record in $expected) {
        $actualRecord = $actual | Where-Object path -eq $record.path | Select-Object -First 1
        if (-not $actualRecord) {
            Stop-Safely "Target is missing: $($record.path)"
        }
        if ($actualRecord.sha256 -ne $record.sha256 -or [int64]$actualRecord.length -ne [int64]$record.length) {
            Stop-Safely "Target hash/length mismatch: $($record.path)"
        }
    }
}

if ($Mode -eq 'Snapshot') {
    if (Test-Path -LiteralPath $backup) {
        Stop-Safely "BackupPath already exists; refusing to overwrite: $backup"
    }

    $backupParent = Split-Path -Parent $backup
    if (-not (Test-Path -LiteralPath $backupParent -PathType Container)) {
        New-Item -ItemType Directory -Path $backupParent -Force | Out-Null
    }
    New-Item -ItemType Directory -Path $payloadPath -Force | Out-Null

    $records = @(Get-FileRecords $target)
    foreach ($record in $records) {
        $sourceFile = Join-Path $target ($record.path -replace '/', '\')
        $destinationFile = Join-Path $payloadPath ($record.path -replace '/', '\')
        $destinationParent = Split-Path -Parent $destinationFile
        if (-not (Test-Path -LiteralPath $destinationParent -PathType Container)) {
            New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
        }
        Copy-Item -LiteralPath $sourceFile -Destination $destinationFile
    }

    $manifest = [pscustomobject]@{
        schemaVersion = '1.0.0'
        operation = 'target-only-rollback'
        targetPath = $target
        createdAt = (Get-Date).ToUniversalTime().ToString('o')
        files = $records
    }
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
    Assert-PayloadMatchesManifest $manifest
    [pscustomobject]@{
        status = 'PASS'
        mode = $Mode
        targetPath = $target
        backupPath = $backup
        fileCount = $records.Count
        sha256 = (@($records | ForEach-Object { "$($_.path):$($_.sha256)" }) -join '|')
    } | ConvertTo-Json -Depth 5
    exit 0
}

$manifest = Read-RollbackManifest
Assert-PayloadMatchesManifest $manifest

if ($Mode -eq 'Verify') {
    Assert-TargetMatchesManifest $manifest
    [pscustomobject]@{
        status = 'PASS'
        mode = $Mode
        targetPath = $target
        backupPath = $backup
        fileCount = @($manifest.files).Count
        result = 'target matches rollback manifest SHA-256 values'
    } | ConvertTo-Json -Depth 5
    exit 0
}

if (-not $ConfirmRestore) {
    Stop-Safely 'Restore requires -ConfirmRestore because it replaces the selected TargetPath contents'
}

# The target was validated above and this removal is intentionally bounded to
# that exact target; the Resource Hub and repository-wide .cursor tree cannot
# reach this branch because of the path guards.
Get-ChildItem -LiteralPath $target -Force | Remove-Item -Recurse -Force
foreach ($record in @($manifest.files)) {
    $sourceFile = Join-Path $payloadPath ($record.path -replace '/', '\')
    $destinationFile = Join-Path $target ($record.path -replace '/', '\')
    $destinationParent = Split-Path -Parent $destinationFile
    if (-not (Test-Path -LiteralPath $destinationParent -PathType Container)) {
        New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
    }
    Copy-Item -LiteralPath $sourceFile -Destination $destinationFile
}

Assert-TargetMatchesManifest $manifest
[pscustomobject]@{
    status = 'PASS'
    mode = $Mode
    targetPath = $target
    backupPath = $backup
    fileCount = @($manifest.files).Count
    result = 'target restored and SHA-256 values verified'
} | ConvertTo-Json -Depth 5
