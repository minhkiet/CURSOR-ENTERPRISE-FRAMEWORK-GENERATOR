# sync-repos.ps1 - Sync conventions and skills from remote repositories
# Usage: .\sync-repos.ps1 [-Repo <name>] [-Force] [-DryRun]
#
# Supported repos:
#   - thaofvn-coca06/2026 (AGENTS.md, CLAUDE.md conventions)
#   - mikiarlo3/ai-copywriter (SKILL.md, references copywriting)
#   - virgiliojr94/book-to-skill (SKILL.md, convert books to skills)
#   - all (default - sync all)

param(
    [ValidateSet("thaofvn-coca06/2026", "mikiarlo3/ai-copywriter", "virgiliojr94/book-to-skill", "AminBlg/SimpleEnglish", "Nutlope/hallmark", "nextlevelbuilder/ui-ux-pro-max-skill", "all")]
    [string]$Repo = "all",
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$ScriptDir = $PSScriptRoot
$TargetDir = Split-Path $ScriptDir -Parent

$Repos = @{
    "thaofvn-coca06/2026" = @{
        Branch = "main"
        Files = @{
            "AGENTS.md" = Join-Path $TargetDir "AGENTS.md"
            "CLAUDE.md" = Join-Path $TargetDir "CLAUDE.md"
            "README.md" = Join-Path $TargetDir "README.md"
        }
        DestDir = $TargetDir
    }
    "mikiarlo3/ai-copywriter" = @{
        Branch = "claude/humanizer-copywriting-skill-u5x4vd"
        Files = @{
            "SKILL.md" = Join-Path $TargetDir "skills\ai-copywriter\SKILL.md"
            "AGENTS.md" = Join-Path $TargetDir "skills\ai-copywriter\AGENTS.md"
            "references\linkedin-virality.md" = Join-Path $TargetDir "skills\ai-copywriter\references\linkedin-virality.md"
            "references\strategic-blog-template.md" = Join-Path $TargetDir "skills\ai-copywriter\references\strategic-blog-template.md"
        }
        DestDir = Join-Path $TargetDir "skills\ai-copywriter"
    }
    "virgiliojr94/book-to-skill" = @{
        Branch = "master"
        Files = @{
            "SKILL.md" = Join-Path $TargetDir "skills\book-to-skill\SKILL.md"
            "CHANGELOG.md" = Join-Path $TargetDir "skills\book-to-skill\CHANGELOG.md"
        }
        DestDir = Join-Path $TargetDir "skills\book-to-skill"
    }
    "AminBlg/SimpleEnglish" = @{
        Branch = "main"
        Files = @{
            "SKILL.md" = Join-Path $TargetDir "skills\simple-english\SKILL.md"
        }
        DestDir = Join-Path $TargetDir "skills\simple-english"
    }
    "Nutlope/hallmark" = @{
        Branch = "main"
        Files = @{
            "SKILL.md" = Join-Path $TargetDir "skills\hallmark\SKILL.md"
            "ROADMAP.md" = Join-Path $TargetDir "skills\hallmark\ROADMAP.md"
        }
        DestDir = Join-Path $TargetDir "skills\hallmark"
    }
    "nextlevelbuilder/ui-ux-pro-max-skill" = @{
        Branch = "main"
        Files = @{
            "skill.json" = Join-Path $TargetDir "skills\ui-ux-pro-max\skill.json"
        }
        # Copy data và scripts từ src/
        CopyDirs = @(
            @{ Remote = "src/ui-ux-pro-max/data"; Local = Join-Path $TargetDir "skills\ui-ux-pro-max\data" },
            @{ Remote = "src/ui-ux-pro-max/scripts"; Local = Join-Path $TargetDir "skills\ui-ux-pro-max\scripts" }
        )
        DestDir = Join-Path $TargetDir "skills\ui-ux-pro-max"
    }
}

Write-Host "=== Sync Repos Script ===" -ForegroundColor Cyan
Write-Host "Target: $Repo" -ForegroundColor Yellow
Write-Host ""

$reposToSync = if ($Repo -eq "all") { $Repos.Keys } else { @($Repo) }

foreach ($repoKey in $reposToSync) {
    $repo = $Repos[$repoKey]
    Write-Host "=== Syncing $repoKey ===" -ForegroundColor Green
    
    $apiUrl = "https://api.github.com/repos/$repoKey/contents"
    $headers = @{ "Accept" = "application/vnd.github.v3+json" }
    
    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Headers $headers
        $remoteFiles = $response | Where-Object { $_.type -eq "file" }
    } catch {
        Write-Warning "Failed to fetch $repoKey: $_"
        continue
    }
    
    Write-Host "Remote files: $($remoteFiles.Count)" -ForegroundColor Gray
    
    $updated = 0
    $skipped = 0
    
    foreach ($file in $remoteFiles) {
        $localPath = $repo.Files[$file.name]
        
        # Handle subdirectory files
        if (-not $localPath) {
            $relativePath = $file.path -replace "$repoKey/", ""
            $localPath = Join-Path $repo.DestDir $relativePath
        }
        
        if (-not $localPath) {
            Write-Host "  [SKIP] $($file.name) - no local mapping" -ForegroundColor DarkGray
            $skipped++
            continue
        }
        
        # Ensure directory exists
        $destDir = Split-Path $localPath -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        
        $downloadUrl = $file.download_url
        
        if (-not $Force -and (Test-Path $localPath)) {
            $localHash = (Get-FileHash $localPath -Algorithm SHA256 -ErrorAction SilentlyContinue).Hash
            
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would update: $($file.name)" -ForegroundColor Yellow
                continue
            }
            
            try {
                $tempPath = "$env:TEMP\sync_repo_$([guid]::NewGuid().ToString('N')).tmp"
                Invoke-WebRequest -Uri $downloadUrl -OutFile $tempPath -UseBasicParsing
                $remoteHash = (Get-FileHash $tempPath -Algorithm SHA256).Hash
                
                if ($localHash -ne $remoteHash) {
                    Write-Host "  [UPDATE] $($file.name)" -ForegroundColor Green
                    Copy-Item $tempPath $localPath -Force
                    $updated++
                } else {
                    Write-Host "  [SKIP] $($file.name) - no changes" -ForegroundColor DarkGray
                    $skipped++
                }
                Remove-Item $tempPath -Force -ErrorAction SilentlyContinue
            } catch {
                Write-Warning "  [ERROR] Failed to update $($file.name): $_"
            }
        } else {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would create: $($file.name)" -ForegroundColor Yellow
                continue
            }
            
            try {
                Write-Host "  [CREATE] $($file.name)" -ForegroundColor Green
                Invoke-WebRequest -Uri $downloadUrl -OutFile $localPath -UseBasicParsing
                $updated++
            } catch {
                Write-Warning "  [ERROR] Failed to create $($file.name): $_"
            }
        }
    }
    
    Write-Host ""
    Write-Host "  Updated: $updated | Skipped: $skipped" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "=== Done ===" -ForegroundColor Green
