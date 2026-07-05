#requires -Version 5.1
<#
.SYNOPSIS
    Builds and publishes Cursor Enterprise Framework v5.0.0 to GitHub releases.

.DESCRIPTION
    - Authenticates via gh CLI if not already logged in
    - Creates / overwrites a draft release v5.0.0
    - Uploads cursor-setup.exe + cursor-setup.zip

.NOTES
    Repo's working dir must contain dist/cursor-setup.exe and dist/cursor-setup.zip.
#>

$ErrorActionPreference = 'Stop'

$Repo       = 'minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR'
$Tag        = 'v5.0.0'
$Title      = 'v5.0.0 - Windows GUI installer'
$ExePath    = Join-Path $PSScriptRoot 'dist\cursor-setup.exe'
$ZipPath    = Join-Path $PSScriptRoot 'dist\cursor-setup.zip'
$NotesPath  = Join-Path $PSScriptRoot 'dist\RELEASE-NOTES-v5.0.0.md'

# --- 0. Inputs must exist ---------------------------------------------------
foreach ($p in @($ExePath, $ZipPath, $NotesPath)) {
    if (-not (Test-Path -LiteralPath $p)) {
        throw "Missing required file: $p"
    }
}

# --- 1. Authenticate (interactive) -----------------------------------------
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host '[auth] gh CLI is not authenticated; launching gh auth login ...' -ForegroundColor Yellow
    gh auth login --hostname github.com --git-protocol https --web | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'gh auth login failed.' }
} else {
    Write-Host '[auth] gh CLI already authenticated.' -ForegroundColor Green
}

# --- 2. Confirm we can see the repo ----------------------------------------
gh repo view $Repo --json nameWithOwner | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Cannot access $Repo. Check repository name and permissions." }

# --- 3. Detect existing release ------------------------------------------
$existing = gh release view $Tag --repo $Repo 2>$null
$isUpdate = $LASTEXITCODE -eq 0
if ($isUpdate) {
    Write-Host "[release] Tag $Tag already exists - deleting draft/assets and recreating." -ForegroundColor Yellow
    gh release delete $Tag --repo $Repo --yes | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Failed to delete existing release $Tag." }
}

# --- 4. Create + upload in ONE call ---------------------------------------
# (single-line `gh release create` so we avoid PowerShell backtick pitfall)
$exeSha = (Get-FileHash -LiteralPath $ExePath -Algorithm SHA256).Hash.ToLower()
$zipSha = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLower()

$createCmd = @(
    'release', 'create', $Tag,
    '--repo', $Repo,
    '--title', $Title,
    '--notes-file', $NotesPath,
    $ExePath, $ZipPath
) -join ' '

Write-Host "[release] Running: gh $createCmd" -ForegroundColor Cyan
gh $createCmd.Split(' ')
if ($LASTEXITCODE -ne 0) { throw 'gh release create failed.' }

# --- 5. Verify ------------------------------------------------------------
gh release view $Tag --repo $Repo | Out-Host
Write-Host "[ok] $Tag published with assets." -ForegroundColor Green
Write-Host "  $ExePath ($exeSha)"
Write-Host "  $ZipPath ($zipSha)"
