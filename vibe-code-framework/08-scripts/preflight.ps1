# Resource Hub acceptance preflight

<##
.SYNOPSIS
    Check the conditions that gate whole-ecosystem acceptance.

.PARAMETER FrameworkPath
    Resource Hub root. Defaults to the parent of this script directory.

.PARAMETER ProjectPath
    Host project containing the .cursor boundary.
    Defaults to the parent of the Resource Hub directory.

.PARAMETER PythonPath
    Explicit Python interpreter to use for the runtime check. If omitted, a
    usable bundled interpreter is preferred over the Windows Store shim.

.PARAMETER OperationalOnly
    Evaluate the safe additive Resource Hub execution path without treating
    the blocked .cursor migration as an operational dependency. This mode
    never grants migration approval and always reports migrationAllowed=false.
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$FrameworkPath = (Split-Path $PSScriptRoot -Parent),

    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent),

    [Parameter(Mandatory=$false)]
    [string]$PythonPath = '',

    [Parameter(Mandatory=$false)]
    [switch]$OperationalOnly
)

$manifestPath = Join-Path $FrameworkPath '00-governance\resource-manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$results = [System.Collections.Generic.List[object]]::new()

function Add-ConditionResult {
    param(
        [string]$ConditionId,
        [ValidateSet('PASS', 'BLOCKED', 'PENDING', 'FAIL')]
        [string]$Status,
        [string]$Details
    )

    $results.Add([pscustomobject]@{
        conditionId = $ConditionId
        status = $Status
        details = $Details
    })
}

# Runtime and pytest are checked by execution, not by the presence of a shim.
function Resolve-PythonExecutable {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        if (Test-Path -LiteralPath $RequestedPath -PathType Leaf) {
            return (Resolve-Path -LiteralPath $RequestedPath).Path
        }
        return $null
    }

    # Prefer project-local environments with installed test dependencies. A
    # valid base interpreter without pytest must not shadow a usable .venv.
    $candidates = @(
        (Join-Path $ProjectPath '.venv\Scripts\python.exe'),
        (Join-Path $ProjectPath 'venv\Scripts\python.exe')
    )
    $localPython = Get-Command python -ErrorAction SilentlyContinue
    if ($localPython) { $candidates += $localPython.Source }
    if ($env:USERPROFILE) {
        $runtimeRoot = Join-Path $env:USERPROFILE '.cache\codex-runtimes'
        if (Test-Path -LiteralPath $runtimeRoot) {
            $candidates += Get-ChildItem -LiteralPath $runtimeRoot -Filter python.exe -File -Recurse -ErrorAction SilentlyContinue |
                Where-Object { $_.FullName -match '\\dependencies\\python\\python\.exe$' } |
                Select-Object -ExpandProperty FullName
        }
    }
    foreach ($candidate in ($candidates | Select-Object -Unique)) {
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { continue }
        $probe = (& $candidate --version 2>&1 | Out-String).Trim()
        if ($probe -match '^Python\s+\d+\.\d+') { return $candidate }
    }
    return $null
}

$python = Resolve-PythonExecutable $PythonPath
if (-not $python) {
    Add-ConditionResult 'COND-RUNTIME-001' 'BLOCKED' 'no usable Python interpreter was found; pass -PythonPath to an approved interpreter'
} else {
    $versionOutput = (& $python --version 2>&1 | Out-String).Trim()
    $versionMatch = [regex]::Match($versionOutput, 'Python\s+(\d+)\.(\d+)')
    if (-not $versionMatch.Success) {
        Add-ConditionResult 'COND-RUNTIME-001' 'BLOCKED' "python is not a usable interpreter: $versionOutput"
    } elseif ([version]::new([int]$versionMatch.Groups[1].Value, [int]$versionMatch.Groups[2].Value) -lt [version]'3.10') {
        Add-ConditionResult 'COND-RUNTIME-001' 'BLOCKED' "Python $versionOutput is below the required 3.10"
    } else {
        $pytestOutput = (& $python -m pytest --version 2>&1 | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) {
            Add-ConditionResult 'COND-RUNTIME-001' 'BLOCKED' "pytest is unavailable: $pytestOutput"
        } else {
            Add-ConditionResult 'COND-RUNTIME-001' 'PASS' "usable interpreter and pytest found: $versionOutput"
        }
    }
}

$inventoryScript = Join-Path $FrameworkPath '08-scripts\inventory.ps1'
$inventory = & $inventoryScript -ProjectPath $ProjectPath | ConvertFrom-Json
if ($inventory.classificationCounts.UNKNOWN_RESOURCE -eq 0) {
    Add-ConditionResult 'COND-INVENTORY-001' 'PASS' "all $($inventory.resourceCount) .cursor resources are classified"
} else {
    Add-ConditionResult 'COND-INVENTORY-001' 'BLOCKED' "$($inventory.classificationCounts.UNKNOWN_RESOURCE) .cursor resources remain UNKNOWN_RESOURCE"
}

$records = $manifest.recordLocations
function Read-RecordFile {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    try { return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json }
    catch { return $null }
}

$conflictPath = Join-Path $FrameworkPath $records.conflictRegister
$conflictRegister = Read-RecordFile $conflictPath
if (-not $conflictRegister) {
    Add-ConditionResult 'COND-CONFLICT-001' 'BLOCKED' "missing or invalid conflict register: $($records.conflictRegister)"
} elseif ($conflictRegister.status -ne 'PASS') {
    Add-ConditionResult 'COND-CONFLICT-001' 'BLOCKED' "conflict register is not approved: status=$($conflictRegister.status)"
} else {
    Add-ConditionResult 'COND-CONFLICT-001' 'PASS' "approved conflict register: $($records.conflictRegister)"
}

$approvalPath = Join-Path $FrameworkPath $records.approvalRegister
$approvalRegister = Read-RecordFile $approvalPath
$approvalCount = if ($approvalRegister -and $approvalRegister.records) { @($approvalRegister.records).Count } else { 0 }
if (-not $approvalRegister) {
    Add-ConditionResult 'COND-APPROVAL-001' 'PENDING' "missing or invalid approval register: $($records.approvalRegister)"
} elseif ($approvalRegister.status -ne 'APPROVED' -or $approvalCount -eq 0) {
    Add-ConditionResult 'COND-APPROVAL-001' 'PENDING' "no real approval is recorded; status=$($approvalRegister.status), records=$approvalCount"
} else {
    Add-ConditionResult 'COND-APPROVAL-001' 'PASS' "approved approval register: $($records.approvalRegister)"
}

$rollbackPath = Join-Path $FrameworkPath $records.rollbackProcedure
$rollbackText = if (Test-Path -LiteralPath $rollbackPath -PathType Leaf) { Get-Content -LiteralPath $rollbackPath -Raw } else { '' }
$evidencePath = Join-Path $FrameworkPath $records.evidenceRegister
$evidenceRegister = Read-RecordFile $evidencePath
$rollbackEvidence = if ($evidenceRegister -and $evidenceRegister.records) {
    @($evidenceRegister.records | Where-Object {
        $_.criterion -eq 'COND-ROLLBACK-001' -and
        $_.status -eq 'PASS' -and
        [int]$_.exitCode -eq 0 -and
        $_.result -match '(?i)restore[d]? .*SHA-256|SHA-256 .*restore'
    })
} else { @() }
if (-not $rollbackText) {
    Add-ConditionResult 'COND-ROLLBACK-001' 'BLOCKED' "missing rollback procedure: $($records.rollbackProcedure)"
} elseif ($rollbackText -notmatch '(?i)dry-run|restore verification|executed verification') {
    Add-ConditionResult 'COND-ROLLBACK-001' 'BLOCKED' "rollback procedure is incomplete or unverified: $($records.rollbackProcedure)"
} elseif ($rollbackEvidence.Count -gt 0) {
    Add-ConditionResult 'COND-ROLLBACK-001' 'PASS' "target-only rollback and restore evidence recorded: $($rollbackEvidence[0].evidenceId)"
} else {
    Add-ConditionResult 'COND-ROLLBACK-001' 'BLOCKED' "procedure exists but valid target-only restore evidence is not recorded: $($records.evidenceRegister)"
}

$requiredAcceptanceEvidence = @(
    'EVD-VERIFY-006',
    'EVD-VERIFY-009',
    'EVD-ADAPTER-SMOKE-004',
    'EVD-BUILD-WEB-001',
    'EVD-BUILD-WPF-001'
)
$acceptanceRecords = if ($evidenceRegister -and $evidenceRegister.records) {
    @($evidenceRegister.records | Where-Object { $_.evidenceId -in $requiredAcceptanceEvidence })
} else { @() }
$missingAcceptanceEvidence = @($requiredAcceptanceEvidence | Where-Object {
    $record = $acceptanceRecords | Where-Object evidenceId -eq $_ | Select-Object -First 1
    -not $record -or $record.status -ne 'PASS' -or [int]$record.exitCode -ne 0
})
if ($missingAcceptanceEvidence.Count -eq 0) {
    Add-ConditionResult 'COND-ACCEPTANCE-001' 'PASS' 'validator, tests, adapter smoke, web build, and WPF build evidence are PASS'
} else {
    Add-ConditionResult 'COND-ACCEPTANCE-001' 'BLOCKED' "missing or failed acceptance evidence: $($missingAcceptanceEvidence -join ', ')"
}

$overall = if ($results | Where-Object status -eq 'FAIL') { 'FAIL' } elseif ($results | Where-Object status -eq 'BLOCKED') { 'BLOCKED' } elseif ($results | Where-Object status -eq 'PENDING') { 'BLOCKED' } else { 'PASS' }
$operationalIds = @('COND-RUNTIME-001', 'COND-ROLLBACK-001', 'COND-ACCEPTANCE-001')
$operationalResults = @($results | Where-Object conditionId -in $operationalIds)
$operationalOverall = if ($operationalResults | Where-Object status -eq 'FAIL') { 'FAIL' } elseif ($operationalResults | Where-Object status -ne 'PASS') { 'BLOCKED' } else { 'PASS' }
$verdict = if ($OperationalOnly) { $operationalOverall } else { $overall }
[pscustomobject]@{
    verdict = $verdict
    scope = if ($OperationalOnly) { 'OPERATIONAL_ONLY' } else { 'WHOLE_ECOSYSTEM' }
    migrationAllowed = $false
    wholeEcosystemVerdict = $overall
    checkedAt = (Get-Date).ToUniversalTime().ToString('o')
    conditions = $results
} | ConvertTo-Json -Depth 5

if ($verdict -ne 'PASS') { exit 1 }
