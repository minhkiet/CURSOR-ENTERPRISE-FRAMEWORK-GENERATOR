# Skill Dependency Auto-Installer for Windows (PowerShell)
# Part of Cursor Enterprise Framework

param(
    [Parameter(Position=0)]
    [ValidateSet("check", "install", "install-all", "list")]
    [string]$Command = "",
    
    [Parameter(Position=1)]
    [string]$SkillName = ""
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path $ScriptDir "skill-dependencies.json"

# Colors
function Write-ColorOutput {
    param([string]$Text, [string]$Color = "White")
    $colorMap = @{
        "Success" = "Green"
        "Error" = "Red"
        "Warning" = "Yellow"
        "Info" = "Cyan"
        "Header" = "Magenta"
    }
    Write-Host $Text -ForegroundColor ($colorMap[$Color] ?? "White")
}

function Read-Manifest {
    if (-not (Test-Path $ManifestPath)) {
        Write-ColorOutput "Warning: Manifest not found at $ManifestPath" "Warning"
        return @{ skills = @{} }
    }
    return Get-Content $ManifestPath -Raw | ConvertFrom-Json
}

function Get-PythonPackageVersion {
    param([string]$PackageName)
    try {
        $result = pip show $PackageName 2>$null
        if ($LASTEXITCODE -eq 0) {
            $version = ($result | Select-String "Version:").ToString().Split(":")[1].Trim()
            return @{ installed = $true; version = $version }
        }
    }
    catch {}
    return @{ installed = $false; version = $null }
}

function Get-NodePackageVersion {
    param([string]$PackageName)
    try {
        $result = npm list $PackageName --depth=0 2>$null
        if ($LASTEXITCODE -eq 0 -and $result -match $PackageName) {
            return @{ installed = $true; version = "installed" }
        }
    }
    catch {}
    return @{ installed = $false; version = $null }
}

function Test-Tesseract {
    try {
        $result = tesseract --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return @{ installed = $true; version = ($result -split "`n")[0] }
        }
    }
    catch {}
    return @{ installed = $false; version = $null }
}

function Get-OS {
    if ($IsWindows -or (-not $IsMacOS -and -not $IsLinux)) {
        return "windows"
    }
    elseif ($IsMacOS) {
        return "macos"
    }
    else {
        return "linux"
    }
}

function Test-SkillDependencies {
    param([string]$SkillName)
    
    $manifest = Read-Manifest
    $skills = $manifest.skills.PSObject.Properties
    
    $skill = $skills | Where-Object { $_.Name -eq $SkillName } | Select-Object -First 1
    
    if (-not $skill) {
        Write-ColorOutput "Skill not found: $SkillName" "Error"
        return
    }
    
    $skillData = $skill.Value
    $dependencies = $skillData.dependencies
    
    $pythonMissing = @()
    $nodeMissing = @()
    $systemMissing = @()
    
    Write-ColorOutput "`n============================================================" "Header"
    Write-ColorOutput "Dependency Check: $($skillData.name)" "Header"
    Write-ColorOutput "============================================================" "Header"
    
    # Check Python dependencies
    if ($dependencies.python) {
        foreach ($pkg in $dependencies.python.packages) {
            $check = Get-PythonPackageVersion $pkg.name
            if (-not $check.installed) {
                $pythonMissing += $pkg
                Write-ColorOutput "  [MISSING] Python: $($pkg.name)" "Warning"
            }
            else {
                Write-ColorOutput "  [OK] Python: $($pkg.name) ($($check.version))" "Success"
            }
        }
    }
    
    # Check Node dependencies
    if ($dependencies.node) {
        foreach ($pkg in $dependencies.node.packages) {
            $check = Get-NodePackageVersion $pkg.name
            if (-not $check.installed) {
                $nodeMissing += $pkg
                Write-ColorOutput "  [MISSING] Node: $($pkg.name)" "Warning"
            }
            else {
                Write-ColorOutput "  [OK] Node: $($pkg.name) ($($check.version))" "Success"
            }
        }
    }
    
    # Check System dependencies
    if ($dependencies.system) {
        $os = Get-OS
        if ($dependencies.system.$os) {
            $sysDep = $dependencies.system.$os
            
            if ($SkillName -match "ocr") {
                $check = Test-Tesseract
                if (-not $check.installed) {
                    $systemMissing += $sysDep
                    Write-ColorOutput "  [MISSING] System: $($sysDep.name)" "Warning"
                }
                else {
                    Write-ColorOutput "  [OK] System: $($sysDep.name)" "Success"
                }
            }
        }
    }
    
    # Summary
    $totalMissing = $pythonMissing.Count + $nodeMissing.Count + $systemMissing.Count
    
    Write-ColorOutput "`n------------------------------------------------------------" "Header"
    if ($totalMissing -eq 0) {
        Write-ColorOutput "✅ All dependencies satisfied!" "Success"
    }
    else {
        Write-ColorOutput "⚠️  Missing dependencies: $totalMissing" "Warning"
        Write-ColorOutput "`nRun: .\.cursor\scripts\skill-installer.ps1 -Command install -SkillName $SkillName" "Info"
    }
}

function Install-SkillDependencies {
    param([string]$SkillName)
    
    $manifest = Read-Manifest
    $skills = $manifest.skills.PSObject.Properties
    $skill = $skills | Where-Object { $_.Name -eq $SkillName } | Select-Object -First 1
    
    if (-not $skill) {
        Write-ColorOutput "Skill not found: $SkillName" "Error"
        return $false
    }
    
    $skillData = $skill.Value
    $dependencies = $skillData.dependencies
    
    Write-ColorOutput "`n============================================================" "Header"
    Write-ColorOutput "Installing: $($skillData.name)" "Header"
    Write-ColorOutput "============================================================" "Header"
    
    $success = $true
    
    # Install Python packages
    if ($dependencies.python) {
        $packages = $dependencies.python.packages | ForEach-Object { $_.name }
        if ($packages.Count -gt 0) {
            Write-ColorOutput "`n[1/3] Installing Python packages..." "Info"
            Write-Host "   Command: pip install $($packages -join ' ')"
            
            try {
                pip install $packages
                if ($LASTEXITCODE -eq 0) {
                    Write-ColorOutput "   ✅ Python packages installed" "Success"
                }
                else {
                    Write-ColorOutput "   ❌ Python installation failed" "Error"
                    $success = $false
                }
            }
            catch {
                Write-ColorOutput "   ❌ Error: $_" "Error"
                $success = $false
            }
        }
    }
    
    # Install Node packages
    if ($dependencies.node) {
        $packages = $dependencies.node.packages | ForEach-Object { $_.name }
        if ($packages.Count -gt 0) {
            Write-ColorOutput "`n[2/3] Installing Node packages..." "Info"
            
            # Check if npm or yarn
            $useYarn = $null -ne (Get-Command yarn -ErrorAction SilentlyContinue)
            
            if ($useYarn) {
                Write-Host "   Command: yarn add $($packages -join ' ')"
                try {
                    yarn add $packages
                    if ($LASTEXITCODE -eq 0) {
                        Write-ColorOutput "   ✅ Node packages installed" "Success"
                    }
                    else {
                        Write-ColorOutput "   ❌ Node installation failed" "Error"
                        $success = $false
                    }
                }
                catch {
                    Write-ColorOutput "   ❌ Error: $_" "Error"
                    $success = $false
                }
            }
            else {
                Write-Host "   Command: npm install $($packages -join ' ')"
                try {
                    npm install $packages
                    if ($LASTEXITCODE -eq 0) {
                        Write-ColorOutput "   ✅ Node packages installed" "Success"
                    }
                    else {
                        Write-ColorOutput "   ❌ Node installation failed" "Error"
                        $success = $false
                    }
                }
                catch {
                    Write-ColorOutput "   ❌ Error: $_" "Error"
                    $success = $false
                }
            }
        }
    }
    
    # Install System packages
    if ($dependencies.system) {
        $os = Get-OS
        if ($dependencies.system.$os) {
            $sysDep = $dependencies.system.$os
            
            Write-ColorOutput "`n[3/3] Installing System packages..." "Info"
            
            if ($SkillName -match "ocr") {
                $check = Test-Tesseract
                if (-not $check.installed) {
                    Write-ColorOutput "   ℹ️  Tesseract OCR requires manual installation:" "Info"
                    Write-ColorOutput "   Download from: https://github.com/UB-Mannheim/tesseract/releases" "Info"
                    
                    if ($os -eq "windows") {
                        Write-ColorOutput "   After installation, add to PATH environment variable" "Info"
                    }
                    elseif ($os -eq "macos") {
                        Write-Host "   Command: brew install tesseract tesseract-lang"
                        Write-Host "   (Run: brew install tesseract tesseract-lang)"
                    }
                    else {
                        Write-Host "   Command: sudo apt install tesseract-ocr tesseract-ocr-vie"
                        Write-Host "   (Run: sudo apt install tesseract-ocr tesseract-ocr-vie)"
                    }
                }
            }
        }
    }
    
    Write-ColorOutput "`n------------------------------------------------------------" "Header"
    if ($success) {
        Write-ColorOutput "✅ Installation completed!" "Success"
    }
    else {
        Write-ColorOutput "⚠️  Installation completed with warnings" "Warning"
    }
    
    return $success
}

function Install-AllDependencies {
    Write-ColorOutput "`n============================================================" "Header"
    Write-ColorOutput "Installing ALL Skill Dependencies" "Header"
    Write-ColorOutput "============================================================" "Header"
    
    $manifest = Read-Manifest
    $skills = $manifest.skills.PSObject.Properties
    
    $results = @{}
    $total = $skills.Count
    $current = 0
    
    foreach ($skill in $skills) {
        $current++
        Write-ColorOutput "`n[$current/$total] $($skill.Name)..." "Info"
        $results[$skill.Name] = Install-SkillDependencies -SkillName $skill.Name
    }
    
    Write-ColorOutput "`n============================================================" "Header"
    Write-ColorOutput "Installation Summary" "Header"
    Write-ColorOutput "============================================================" "Header"
    
    $successCount = ($results.Values | Where-Object { $_ -eq $true }).Count
    Write-ColorOutput "Success: $successCount / $total" "Info"
    
    foreach ($skill in $results.Keys) {
        $status = if ($results[$skill]) { "✅" } else { "⚠️" }
        Write-Host "   $status $skill"
    }
}

function List-Skills {
    $manifest = Read-Manifest
    $skills = $manifest.skills.PSObject.Properties
    
    Write-ColorOutput "`n============================================================" "Header"
    Write-ColorOutput "Available Skills with Dependencies" "Header"
    Write-ColorOutput "============================================================" "Header"
    
    foreach ($skill in $skills) {
        $skillData = $skill.Value
        
        Write-ColorOutput "`n• $($skill.Name)" "Info"
        Write-Host "  $($skillData.description)"
        
        $deps = $skillData.dependencies
        
        if ($deps.python) {
            $pkgs = $deps.python.packages | ForEach-Object { $_.name }
            Write-Host "  🐍 Python: $($pkgs -join ', ')"
        }
        
        if ($deps.node) {
            $pkgs = $deps.node.packages | ForEach-Object { $_.name }
            Write-Host "  📦 Node: $($pkgs -join ', ')"
        }
        
        if ($deps.system) {
            $os = Get-OS
            if ($deps.system.$os) {
                Write-Host "  🖥️  System: $($deps.system.$os.name)"
            }
        }
    }
}

# Main
switch ($Command) {
    "check" {
        if ([string]::IsNullOrEmpty($SkillName)) {
            Write-ColorOutput "Error: Please specify skill name" "Error"
            Write-Host "Example: .\.cursor\scripts\skill-installer.ps1 -Command check -SkillName document-ocr"
            exit 1
        }
        Test-SkillDependencies -SkillName $SkillName
    }
    "install" {
        if ([string]::IsNullOrEmpty($SkillName)) {
            Write-ColorOutput "Error: Please specify skill name" "Error"
            Write-Host "Example: .\.cursor\scripts\skill-installer.ps1 -Command install -SkillName document-ocr"
            exit 1
        }
        $result = Install-SkillDependencies -SkillName $SkillName
        if (-not $result) { exit 1 }
    }
    "install-all" {
        Install-AllDependencies
    }
    "list" {
        List-Skills
    }
    default {
        Write-Host @"
Skill Dependency Auto-Installer
================================

Usage:
    .\.cursor\scripts\skill-installer.ps1 -Command <command> -SkillName <name>

Commands:
    check       Check dependencies for a skill
    install     Install dependencies for a skill
    install-all Install all skill dependencies
    list        List all skills with dependencies

Examples:
    .\.cursor\scripts\skill-installer.ps1 -Command check -SkillName document-ocr
    .\.cursor\scripts\skill-installer.ps1 -Command install -SkillName document-ocr
    .\.cursor\scripts\skill-installer.ps1 -Command install-all
    .\.cursor\scripts\skill-installer.ps1 -Command list

Available Skills:
    document-ocr         - Text extraction from images (Tesseract OCR)
    playwright-web-scraper - Web content extraction
    rag-builder         - RAG pipeline builder
    frontend-taste      - Premium frontend design
    frontend-redesign   - Redesign existing frontend
    security-review     - Security vulnerability assessment
    database-optimization - Database performance tuning
    performance-audit    - Application performance analysis

"@
    }
}
