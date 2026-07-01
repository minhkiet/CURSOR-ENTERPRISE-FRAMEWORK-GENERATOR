# Cursor Enterprise Framework - Build Setup Script
# Builds cursor-setup.exe with .cursor packaged as ZIP sidecar

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "============================================================"
Write-Host "  Building cursor-setup.exe"
Write-Host "============================================================"
Write-Host ""

$ProjectDir = "D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
$CSPROJ = "$ProjectDir\cursor-setup-gui\CursorSetup.csproj"
$CURSOR_SRC = "$ProjectDir\.cursor"
$OUTPUT = "$ProjectDir\cursor-setup.exe"
$OUTPUT_ZIP = "$ProjectDir\cursor-setup.zip"

# Check .NET SDK
try {
    $dotnetVersion = dotnet --version 2>$null
    Write-Host "[INFO] .NET SDK version: $dotnetVersion"
} catch {
    Write-Host "[ERROR] .NET SDK not found."
    exit 1
}

if (-not (Test-Path $CSPROJ)) {
    Write-Host "[ERROR] CursorSetup.csproj not found"
    exit 1
}

if (-not (Test-Path $CURSOR_SRC)) {
    Write-Host "[ERROR] .cursor folder not found"
    exit 1
}

Write-Host "[INFO] Project: $CSPROJ"
Write-Host "[INFO] Source:  $CURSOR_SRC"
Write-Host "[INFO] Output:  $OUTPUT"
Write-Host ""

# ============================================================
# STEP 1: Create ZIP of .cursor
# ============================================================
Write-Host "[STEP 1/4] Creating ZIP archive..."

$fileCount = (Get-ChildItem $CURSOR_SRC -Recurse -File).Count
Write-Host "  Found $fileCount files to package"

# Remove old zip
if (Test-Path $OUTPUT_ZIP) { Remove-Item $OUTPUT_ZIP }

# Create ZIP
Compress-Archive -Path "$CURSOR_SRC\*" -DestinationPath $OUTPUT_ZIP -CompressionLevel Optimal

$zipSize = [math]::Round((Get-Item $OUTPUT_ZIP).Length / 1KB)
$zipSizeMB = [math]::Round((Get-Item $OUTPUT_ZIP).Length / 1MB, 2)
Write-Host "  Created cursor-setup.zip: $zipSize KB ($zipSizeMB MB)"
Write-Host ""

# ============================================================
# STEP 2: Build Release
# ============================================================
Write-Host "[STEP 2/4] Building Release..."

$binDir = "$ProjectDir\cursor-setup-gui\bin"
if (Test-Path $binDir) { Remove-Item $binDir -Recurse -Force }

dotnet build $CSPROJ -c Release
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed"
    exit 1
}
Write-Host "  Build succeeded."
Write-Host ""

# ============================================================
# STEP 3: Copy exe and zip to root
# ============================================================
Write-Host "[STEP 3/4] Copying files to root..."

$EXE_PATH = "$ProjectDir\cursor-setup-gui\bin\Release\net8.0-windows\win-x64\cursor-setup.exe"
if (Test-Path $EXE_PATH) {
    Copy-Item $EXE_PATH $OUTPUT -Force
    Write-Host "  Copied cursor-setup.exe"
} else {
    Write-Host "[ERROR] Exe not found: $EXE_PATH"
    exit 1
}

# Check if zip exists (already there from step 1)
if (Test-Path $OUTPUT_ZIP) {
    Write-Host "  cursor-setup.zip already in place"
}
Write-Host ""

# ============================================================
# STEP 4: Summary
# ============================================================
Write-Host "[STEP 4/4] Summary..."

$exeSize = (Get-Item $OUTPUT).Length
$exeSizeKB = [math]::Round($exeSize / 1KB)

Write-Host ""
Write-Host "============================================================"
Write-Host "  Build completed successfully!"
Write-Host "============================================================"
Write-Host ""
Write-Host "  Output Files:"
Write-Host "    - cursor-setup.exe  ($exeSizeKB KB) - GUI Installer"
Write-Host "    - cursor-setup.zip  ($zipSize KB)   - Framework content"
Write-Host ""
Write-Host "  Total: $fileCount files from .cursor"
Write-Host ""
Write-Host "  Usage: Run cursor-setup.exe, it will extract cursor-setup.zip"
Write-Host "         to the selected .cursor folder."
Write-Host ""
