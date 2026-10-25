# Validate Framework Script

<#
.SYNOPSIS
    Validate Vibe Code Framework structure.

.DESCRIPTION
    Checks that all required files exist and are properly formatted.

.PARAMETER Path
    Path to framework root
    Default: Script directory

.PARAMETER Fix
    Auto-fix common issues
    Default: false

.EXAMPLE
    .\validate.ps1
    Validate framework structure

.EXAMPLE
    .\validate.ps1 -Fix
    Validate and auto-fix issues
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Path = (Split-Path $PSScriptRoot -Parent),

    [Parameter(Mandatory=$false)]
    [string]$ManifestPath = '',
    
    [Parameter(Mandatory=$false)]
    [switch]$Fix = $false
)

$ErrorCount = 0
$WarningCount = 0
$FixedCount = 0

if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path $Path '00-governance\resource-manifest.json'
}

function Write-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

function Write-Info($message) {
    Write-Host "ℹ️  $message" -ForegroundColor Cyan
}

function Write-Warning($message) {
    Write-Host "⚠️  $message" -ForegroundColor Yellow
    $script:WarningCount++
}

function Write-Error($message) {
    Write-Host "❌ $message" -ForegroundColor Red
    $script:ErrorCount++
}

# Required structure
$RequiredFiles = @{
    "Root" = @(
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md"
    )
    "00-governance" = @(
        "README.md",
        "resource-manifest.json",
        "BASELINE.md"
    )
    "01-core-rules" = @(
        "01-principles.md",
        "02-security.md",
        "03-code-quality.md",
        "04-architecture.md",
        "05-git-workflow.md",
        "README.md"
    )
    "02-stacks" = @(
        "README.md",
        "aspnetcore\README.md",
        "database\README.md",
        "vue3-typescript\README.md"
    )
    "03-skills" = @(
        "SKILL-FORMAT.md",
        "create-feature\SKILL.md",
        "create-api\SKILL.md",
        "create-ui\SKILL.md",
        "database-migration\SKILL.md",
        "code-review\SKILL.md",
        "debug-error\SKILL.md",
        "fullstack-web\SKILL.md",
        "security-scan\SKILL.md",
        "testing\SKILL.md",
        "README.md"
    )
    "04-agents" = @(
        "architect.md",
        "frontend.md",
        "backend.md",
        "database.md",
        "reviewer.md",
        "README.md"
    )
    "05-workflows" = @(
        "new-project.md",
        "new-feature.md",
        "bug-fix.md",
        "release.md",
        "README.md"
    )
    "06-templates" = @(
        "vue-component.md",
        "api-endpoint.md",
        "database-schema.md",
        "README.md"
    )
    "07-adapters" = @(
        "cursor\README.md",
        "cursor\AGENTS.md",
        "cursor\rules\core.mdc",
        "claude-code\README.md",
        "codex\README.md",
        "copilot\README.md",
        "copilot\copilot-instructions.md",
        "windsurf\README.md",
        "antigravity\README.md",
        "README.md"
    )
    "08-scripts" = @(
        "sync-adapters.ps1",
        "sync-adapters.sh",
        "install.ps1",
        "inventory.ps1",
        "preflight.ps1",
        "rollback-target.ps1",
        "validate.ps1",
        "README.md"
    )
}

function Validate-File {
    param($FilePath, $Required)
    
    $fullPath = Join-Path $Path $FilePath
    
    if (Test-Path $fullPath) {
        # Check file is not empty
        $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue
        if ([string]::IsNullOrWhiteSpace($content)) {
            Write-Error "Empty file: $FilePath"
            return $false
        }
        
        Write-Success "OK: $FilePath"
        return $true
    } else {
        if ($Required) {
            Write-Error "Missing: $FilePath"
            return $false
        } else {
            Write-Warning "Optional missing: $FilePath"
            return $true
        }
    }
}

function Validate-SKILLFormat {
    param($FilePath)
    
    $fullPath = Join-Path $Path $FilePath
    
    if (-not (Test-Path $fullPath)) {
        return $true  # Already checked in Validate-File
    }
    
    $content = Get-Content $fullPath -Raw
    
    # Check for required sections
    $requiredSections = @(
        "Goal",
        "Trigger",
        "Pre-Check Gates",
        "Process Steps",
        "Post-Check Gates"
    )
    
    $missing = @()
    foreach ($section in $requiredSections) {
        if ($content -notmatch "(?im)^##?\s*$section") {
            $missing += $section
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Warning "SKILL missing sections in $FilePath`: $($missing -join ', ')"
        return $false
    }
    
    return $true
}

function Validate-Frontmatter {
    param($FilePath)
    
    $fullPath = Join-Path $Path $FilePath
    
    if (-not (Test-Path $fullPath)) {
        return $true
    }
    
    # Only .mdc files need frontmatter
    if (-not $FilePath.EndsWith(".mdc")) {
        return $true
    }
    
    $content = Get-Content $fullPath -Raw
    
    if (-not $content.StartsWith("---")) {
        Write-Warning "Missing frontmatter in $FilePath"
        return $false
    }
    
    return $true
}

function Validate-Manifest {
    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        Write-Error "Missing canonical manifest: $ManifestPath"
        return $false
    }

    try {
        $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    } catch {
        Write-Error "Invalid JSON manifest: $ManifestPath"
        return $false
    }

    if ($manifest.canonicalSource.sourceType -ne 'SOT-CANONICAL') {
        Write-Error "Manifest canonicalSource.sourceType must be SOT-CANONICAL"
        return $false
    }

    if (-not $manifest.executionInputContract.requiredInputs -or
        -not $manifest.canonicalLocations.governance) {
        Write-Error "Manifest is missing the execution input contract or canonical locations"
        return $false
    }

    Write-Success "OK: canonical manifest"
    return $true
}

# Main validation
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "   Vibe Code Framework — Validator" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""
Write-Info "Path: $Path"
Write-Info "Manifest: $ManifestPath"
Write-Host ""

# Validate file structure
Write-Info "Validating file structure..."
Write-Host ""

$allFilesValid = Validate-Manifest

foreach ($category in $RequiredFiles.Keys) {
    Write-Info "═══ $category ═══"
    
    foreach ($file in $RequiredFiles[$category]) {
        $relativeFile = if ($category -eq 'Root') { $file } else { Join-Path $category $file }
        $fileValid = Validate-File -FilePath $relativeFile -Required $true
        
        # Validate format for specific file types
        if ($file -like "*\SKILL.md") {
            $null = Validate-SKILLFormat -FilePath $relativeFile
        }
        
        if ($file -like "*.mdc") {
            $null = Validate-Frontmatter -FilePath $relativeFile
        }
        
        if (-not $fileValid) {
            $allFilesValid = $false
        }
    }
    Write-Host ""
}

# Validate adapter mappings
Write-Info "═══ Adapter Mappings ═══"

$cursorRules = Get-ChildItem -Path "$Path\01-core-rules" -Filter "*.md" -File | Where-Object { $_.Name -ne "README.md" }
$adapterRules = Get-ChildItem -Path "$Path\07-adapters\cursor\rules" -Filter "*.mdc" -File

if ($cursorRules.Count -eq $adapterRules.Count) {
    Write-Success "Adapter rules count matches: $($cursorRules.Count)"
} else {
    Write-Warning "Rule count mismatch: Source=$($cursorRules.Count), Adapter=$($adapterRules.Count)"
}

# Check skill directories
Write-Host ""
Write-Info "═══ Skills ═══"

$skills = Get-ChildItem -Path "$Path\03-skills" -Directory -Exclude "README.md"
Write-Info "Found $($skills.Count) skills:"

foreach ($skill in $skills) {
    $skillFile = Join-Path $skill.FullName "SKILL.md"
    if (Test-Path $skillFile) {
        Write-Success "  - $($skill.Name)"
    } else {
        Write-Error "  - $($skill.Name) (missing SKILL.md)"
    }
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "   Validation Summary" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

if ($ErrorCount -eq 0 -and $WarningCount -eq 0) {
    Write-Success "✅ Framework is valid!"
    exit 0
} elseif ($ErrorCount -eq 0) {
    Write-Warning "⚠️  $WarningCount warning(s) found"
    exit 0
} else {
    Write-Error "❌ $ErrorCount error(s), $WarningCount warning(s)"
    exit 1
}
