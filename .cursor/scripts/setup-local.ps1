# =============================================================================
# CURSOR ENTERPRISE FRAMEWORK - LOCAL SETUP SCRIPT
# =============================================================================
# Purpose: Install .cursor configuration from this project to other projects
# Author: Cursor Enterprise Framework Generator
# Version: 1.0.0
# Date: 2026-06-26
# =============================================================================

param(
    [Parameter(Position=0)]
    [string]$TargetProject,
    
    [Parameter(Position=1)]
    [ValidateSet("all", "rules", "skills", "scripts", "knowledge")]
    [string[]]$Components = @("all"),
    
    [switch]$List,
    [switch]$DryRun,
    [switch]$Force,
    [switch]$Backup,
    [switch]$CreateSymlink
)

# =============================================================================
# CONFIGURATION
# =============================================================================

$SOURCE_ROOT = Split-Path -Parent $PSScriptRoot
$CURSOR_FOLDER = ".cursor"
$BACKUP_SUFFIX = ".backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# =============================================================================
# COLORS & FORMATTING
# =============================================================================

function Write-ColorOutput {
    param(
        [string]$Message,
        [ValidateSet("Info", "Success", "Warning", "Error", "Header")]
        [string]$Type = "Info"
    )
    
    $colors = @{
        "Info"    = @{ Foreground = "Cyan" }
        "Success" = @{ Foreground = "Green" }
        "Warning" = @{ Foreground = "Yellow" }
        "Error"   = @{ Foreground = "Red" }
        "Header"  = @{ Foreground = "Magenta" }
    }
    
    Write-Host $Message -ForegroundColor $colors[$Type].Foreground
}

# =============================================================================
# DISCOVERY FUNCTIONS
# =============================================================================

function Find-CursorProjects {
    <#
    .SYNOPSIS
    Discover all projects in common locations that have .cursor folder
    #>
    
    $locations = @(
        $env:USERPROFILE + "\Documents",
        $env:USERPROFILE + "\Desktop",
        "D:\PROJECTS",
        "C:\Projects",
        "C:\Dev",
        "D:\Dev",
        "D:\Work",
        "C:\Work"
    )
    
    $projects = @()
    
    foreach ($location in $locations) {
        if (Test-Path $location) {
            $items = Get-ChildItem -Path $location -Directory -ErrorAction SilentlyContinue
            foreach ($item in $items) {
                $cursorPath = Join-Path $item.FullName $CURSOR_FOLDER
                if (Test-Path $cursorPath) {
                    $projects += [PSCustomObject]@{
                        Name     = $item.Name
                        Path     = $item.FullName
                        HasCursor = $true
                    }
                }
            }
        }
    }
    
    return $projects
}

function Find-ProjectsWithoutCursor {
    <#
    .SYNOPSIS
    Find projects that don't have .cursor folder
    #>
    
    $locations = @(
        "D:\PROJECTS",
        "C:\Projects",
        "C:\Dev",
        "D:\Dev",
        "D:\Work",
        "C:\Work"
    )
    
    $projects = @()
    
    foreach ($location in $locations) {
        if (Test-Path $location) {
            $items = Get-ChildItem -Path $location -Directory -ErrorAction SilentlyContinue
            foreach ($item in $items) {
                $cursorPath = Join-Path $item.FullName $CURSOR_FOLDER
                if (-not (Test-Path $cursorPath)) {
                    $projects += [PSCustomObject]@{
                        Name     = $item.Name
                        Path     = $item.FullName
                    }
                }
            }
        }
    }
    
    return $projects
}

# =============================================================================
# COMPONENT SELECTION
# =============================================================================

function Get-SourceComponents {
    <#
    .SYNOPSIS
    Get all available components in the source .cursor folder
    #>
    
    $sourcePath = Join-Path $SOURCE_ROOT $CURSOR_FOLDER
    if (-not (Test-Path $sourcePath)) {
        Write-ColorOutput "Source .cursor folder not found at: $sourcePath" -Type Error
        return $null
    }
    
    $components = @()
    
    $items = Get-ChildItem -Path $sourcePath -Directory -ErrorAction SilentlyContinue
    foreach ($item in $items) {
        $components += [PSCustomObject]@{
            Name        = $item.Name
            Path        = $item.FullName
            ItemCount   = (Get-ChildItem -Path $item.FullName -Recurse -File).Count
        }
    }
    
    return $components
}

function Get-SelectedComponents {
    <#
    .SYNOPSIS
    Filter components based on user selection
    #>
    
    $allComponents = Get-SourceComponents
    
    if ($Components -contains "all") {
        return $allComponents
    }
    
    return $allComponents | Where-Object { $Components -contains $_.Name }
}

# =============================================================================
# BACKUP FUNCTIONS
# =============================================================================

function Backup-ExistingCursor {
    <#
    .SYNOPSIS
    Backup existing .cursor folder before overwriting
    #>
    
    param(
        [Parameter(Mandatory)]
        [string]$ProjectPath
    )
    
    $cursorPath = Join-Path $ProjectPath $CURSOR_FOLDER
    
    if (-not (Test-Path $cursorPath)) {
        return $null
    }
    
    $backupPath = $cursorPath + $BACKUP_SUFFIX
    
    Write-ColorOutput "Creating backup at: $backupPath" -Type Info
    
    try {
        Copy-Item -Path $cursorPath -Destination $backupPath -Recurse -Force
        return $backupPath
    }
    catch {
        Write-ColorOutput "Failed to create backup: $_" -Type Error
        return $null
    }
}

function Restore-Backup {
    <#
    .SYNOPSIS
    Restore backup of .cursor folder
    #>
    
    param(
        [Parameter(Mandatory)]
        [string]$ProjectPath,
        
        [Parameter(Mandatory)]
        [string]$BackupPath
    )
    
    $cursorPath = Join-Path $ProjectPath $CURSOR_FOLDER
    
    if (Test-Path $cursorPath) {
        Remove-Item -Path $cursorPath -Recurse -Force
    }
    
    Copy-Item -Path $BackupPath -Destination $cursorPath -Recurse -Force
}

# =============================================================================
# INSTALLATION FUNCTIONS
# =============================================================================

function Install-CursorToProject {
    <#
    .SYNOPSIS
    Install .cursor components to target project
    #>
    
    param(
        [Parameter(Mandatory)]
        [string]$TargetPath,
        
        [switch]$Symlink
    )
    
    $sourcePath = Join-Path $SOURCE_ROOT $CURSOR_FOLDER
    $targetCursorPath = Join-Path $TargetPath $CURSOR_FOLDER
    
    # Validate source
    if (-not (Test-Path $sourcePath)) {
        Write-ColorOutput "Source .cursor not found: $sourcePath" -Type Error
        return $false
    }
    
    # Validate target
    if (-not (Test-Path $TargetPath)) {
        Write-ColorOutput "Target project not found: $TargetPath" -Type Error
        return $false
    }
    
    # Check existing .cursor
    $existingCursor = Test-Path $targetCursorPath
    
    if ($existingCursor -and -not $Force) {
        if (-not $Backup) {
            Write-ColorOutput "Target already has .cursor. Use -Backup to backup first, or -Force to overwrite." -Type Warning
            return $false
        }
        
        $backupPath = Backup-ExistingCursor -ProjectPath $TargetPath
        if (-not $backupPath) {
            Write-ColorOutput "Backup failed. Aborting." -Type Error
            return $false
        }
        Write-ColorOutput "Backup created: $backupPath" -Type Success
    }
    elseif ($existingCursor -and $Force) {
        if ($Backup) {
            $backupPath = Backup-ExistingCursor -ProjectPath $TargetPath
            Write-ColorOutput "Backup created: $backupPath" -Type Success
        }
        Remove-Item -Path $targetCursorPath -Recurse -Force
    }
    
    # Get selected components
    $selectedComponents = Get-SelectedComponents
    
    if ($DryRun) {
        Write-ColorOutput "`n[DRY RUN] Would install:" -Type Header
        foreach ($comp in $selectedComponents) {
            Write-Host "  - $($comp.Name) ($($comp.ItemCount) files)"
        }
        return $true
    }
    
    # Create .cursor folder
    if (-not (Test-Path $targetCursorPath)) {
        New-Item -Path $targetCursorPath -ItemType Directory | Out-Null
    }
    
    # Install components
    $successCount = 0
    foreach ($component in $selectedComponents) {
        $sourceCompPath = Join-Path $sourcePath $component.Name
        $targetCompPath = Join-Path $targetCursorPath $component.Name
        
        Write-ColorOutput "Installing $($component.Name)..." -Type Info
        
        if ($Symlink -and -not $DryRun) {
            # Create symlink
            try {
                if (Test-Path $targetCompPath) {
                    Remove-Item -Path $targetCompPath -Recurse -Force
                }
                New-Item -Path $targetCompPath -ItemType SymbolicLink -Value $sourceCompPath | Out-Null
                Write-ColorOutput "  Created symlink: $targetCompPath -> $sourceCompPath" -Type Success
                $successCount++
            }
            catch {
                Write-ColorOutput "  Symlink failed (may need admin): $_" -Type Warning
                # Fallback to copy
                Copy-Item -Path $sourceCompPath -Destination $targetCompPath -Recurse -Force
                Write-ColorOutput "  Copied instead" -Type Success
                $successCount++
            }
        }
        else {
            # Copy
            Copy-Item -Path $sourceCompPath -Destination $targetCompPath -Recurse -Force
            Write-ColorOutput "  Copied $($component.ItemCount) files" -Type Success
            $successCount++
        }
    }
    
    Write-ColorOutput "`nSuccessfully installed $successCount/$($selectedComponents.Count) components" -Type Success
    
    return $true
}

# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

function Show-Header {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║        CURSOR ENTERPRISE FRAMEWORK - LOCAL SETUP WIZARD              ║" -ForegroundColor Magenta
    Write-Host "╚══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
}

function Show-Help {
    @"

USAGE:
    .\setup-local.ps1 [OPTIONS]

OPTIONS:
    <TargetProject>       Project path or name to install to
    -List                List all available projects
    -Components <items>  Select components: all, rules, skills, scripts, knowledge
    -DryRun              Show what would be installed without installing
    -Backup              Create backup before overwriting
    -Force               Overwrite existing .cursor without prompting
    -CreateSymlink       Create symbolic links instead of copying
    -Help                Show this help message

EXAMPLES:
    # Install all .cursor to a project
    .\setup-local.ps1 "D:\Projects\MyApp"

    # List all projects
    .\setup-local.ps1 -List

    # Install only rules and skills
    .\setup-local.ps1 "D:\Projects\MyApp" -Components rules,skills

    # Dry run to see what would happen
    .\setup-local.ps1 "D:\Projects\MyApp" -DryRun

    # Install with backup
    .\setup-local.ps1 "D:\Projects\MyApp" -Backup -Force

    # Create symlinks (good for development)
    .\setup-local.ps1 "D:\Projects\MyApp" -CreateSymlink

"@
}

function Show-SourceInfo {
    Write-ColorOutput "Source: $SOURCE_ROOT" -Type Header
    Write-ColorOutput "Available Components:" -Type Header
    $components = Get-SourceComponents
    foreach ($comp in $components) {
        Write-Host "  [$($comp.Name)] - $($comp.ItemCount) files"
    }
    Write-Host ""
}

function Show-ProjectList {
    Write-ColorOutput "`n=== PROJECTS WITH .CURSOR ===" -Type Header
    $withCursor = Find-CursorProjects
    foreach ($proj in $withCursor) {
        Write-Host "  [+] $($proj.Name) - $($proj.Path)"
    }
    
    Write-ColorOutput "`n=== PROJECTS WITHOUT .CURSOR ===" -Type Header
    $withoutCursor = Find-ProjectsWithoutCursor
    foreach ($proj in $withoutCursor) {
        Write-Host "  [-] $($proj.Name) - $($proj.Path)"
    }
    
    Write-Host ""
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

function Main {
    Show-Header
    
    # Show help if requested
    if ($MyInvocation.BoundParameters.Keys -contains "Help" -or $args -contains "-Help" -or $args -contains "/?" -or $args -contains "--help") {
        Show-Help
        return
    }
    
    # List mode
    if ($List) {
        Show-SourceInfo
        Show-ProjectList
        return
    }
    
    # Show source info
    Show-SourceInfo
    
    # Resolve target project
    if (-not $TargetProject) {
        Write-ColorOutput "Please specify a target project." -Type Warning
        Write-Host "Use -List to see available projects, or provide a path."
        Write-Host ""
        Show-Help
        return
    }
    
    # Check if target is a path or project name
    if (Test-Path $TargetProject) {
        $targetPath = $TargetProject
    }
    else {
        # Try to find by name in common locations
        $locations = @("D:\PROJECTS", "C:\Projects", "C:\Dev", "D:\Dev", "D:\Work")
        $found = $false
        
        foreach ($loc in $locations) {
            $potentialPath = Join-Path $loc $TargetProject
            if (Test-Path $potentialPath) {
                $targetPath = $potentialPath
                $found = $true
                break
            }
        }
        
        if (-not $found) {
            Write-ColorOutput "Project not found: $TargetProject" -Type Error
            Write-Host "Use -List to see available projects."
            return
        }
    }
    
    Write-ColorOutput "Target: $targetPath" -Type Header
    
    # Run installation
    $result = Install-CursorToProject -TargetPath $targetPath -Symlink:$CreateSymlink
    
    if ($result) {
        Write-ColorOutput "`nSetup completed successfully!" -Type Success
        
        if ($CreateSymlink) {
            Write-ColorOutput "Note: Symlinks will stay synced with source automatically." -Type Info
        }
    }
    else {
        Write-ColorOutput "`nSetup failed. See errors above." -Type Error
    }
}

# Run
Main @args
