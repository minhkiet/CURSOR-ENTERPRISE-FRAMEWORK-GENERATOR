#!/usr/bin/env python3
"""
Cursor Enterprise Framework - Local Setup Installer
====================================================
Creates a standalone .exe to install .cursor to any project.

Usage:
    python setup_exe_builder.py        # Build the .exe
    cursor-setup.exe [ProjectPath]     # Run the installer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

try:
    import PyInstaller.__main__
except ImportError:
    print("[X] PyInstaller not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    import PyInstaller.__main__

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
CURSOR_SOURCE = SCRIPT_DIR / ".cursor"
SETUP_SCRIPT = SCRIPT_DIR / "setup_local_installer.py"
DIST_FOLDER = SCRIPT_DIR / "dist"

def create_installer_script():
    """Create the standalone installer script that will be compiled to .exe"""
    
    installer_code = '''#!/usr/bin/env python3
"""
Cursor Enterprise Framework - Standalone Installer
==================================================
This script is compiled into a standalone .exe
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Source .cursor location (relative to exe or hardcoded)
SOURCE_ROOT = Path(r"D:\\PROJECTS\\CURSORS\\CURSOR ENTERPRISE FRAMEWORK GENERATOR")
CURSOR_SOURCE = SOURCE_ROOT / ".cursor"

# Colors for terminal output
class Colors:
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'

def log(msg, level="info"):
    colors = {
        "info": Colors.OKCYAN,
        "success": Colors.OKGREEN,
        "warning": Colors.WARNING,
        "error": Colors.FAIL,
        "header": Colors.HEADER + Colors.BOLD
    }
    color = colors.get(level, Colors.OKCYAN)
    prefix = {
        "info": "[...]",
        "success": "[OK] ",
        "warning": "[!] ",
        "error": "[X] ",
        "header": "\\n" + "="*50
    }
    prefix_char = prefix.get(level, "[...]")
    print(f"{color}{prefix_char} {msg}{Colors.ENDC}")

def get_components():
    """Get available .cursor components"""
    components = []
    if CURSOR_SOURCE.exists():
        for item in CURSOR_SOURCE.iterdir():
            if item.is_dir():
                file_count = sum(1 for _ in item.rglob("*") if _.is_file())
                components.append({
                    "name": item.name,
                    "path": item,
                    "files": file_count
                })
    return components

def discover_projects():
    """Find projects in common locations"""
    search_paths = [
        Path("D:/PROJECTS"),
        Path("C:/Projects"),
        Path("C:/Dev"),
        Path("D:/Dev"),
    ]
    
    projects_with_cursor = []
    projects_without_cursor = []
    
    for search_path in search_paths:
        if search_path.exists():
            for item in search_path.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    cursor_path = item / ".cursor"
                    info = {"name": item.name, "path": item}
                    if cursor_path.exists():
                        projects_with_cursor.append(info)
                    else:
                        projects_without_cursor.append(info)
    
    return projects_with_cursor, projects_without_cursor

def install_cursor(target_path, force=False, backup=True):
    """Install .cursor to target project"""
    target_cursor = Path(target_path) / ".cursor"
    
    # Validate target
    if not Path(target_path).exists():
        return False, "Target path does not exist"
    
    # Handle existing .cursor
    if target_cursor.exists():
        if not force:
            return False, "Target already has .cursor. Use -Force to overwrite."
        
        if backup:
            backup_path = target_cursor.parent / f".cursor.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            log(f"Creating backup at: {backup_path}", "info")
            shutil.copytree(target_cursor, backup_path)
            log("Backup created successfully", "success")
        
        log("Removing existing .cursor...", "info")
        shutil.rmtree(target_cursor)
    
    # Copy .cursor
    log(f"Installing .cursor to: {target_path}", "info")
    try:
        shutil.copytree(CURSOR_SOURCE, target_cursor)
        file_count = sum(1 for _ in target_cursor.rglob("*") if _.is_file())
        return True, f"Installed successfully! ({file_count} files)"
    except Exception as e:
        return False, f"Installation failed: {e}"

def main():
    print()
    print("=" * 50)
    print("  CURSOR ENTERPRISE FRAMEWORK - SETUP WIZARD")
    print("=" * 50)
    print()
    
    # Parse arguments
    args = sys.argv[1:]
    target_path = None
    force = "-Force" in args or "-force" in args
    backup = not ("-NoBackup" in args or "-nobackup" in args)
    list_mode = "-List" in args or "-list" in args or "--list" in args
    
    # Find target path
    for arg in args:
        if not arg.startswith("-"):
            target_path = arg
            break
    
    # Show header
    log("Source: " + str(CURSOR_SOURCE), "header")
    log("Available components:", "header")
    
    components = get_components()
    for comp in components:
        log(f"  [{comp['name']}] - {comp['files']} files", "info")
    
    print()
    
    # List mode
    if list_mode:
        log("Discovering projects...", "info")
        print()
        
        with_cursor, without_cursor = discover_projects()
        
        log("Projects WITH .cursor:", "header")
        for p in with_cursor:
            print(f"  + {p['name']} ({p['path']})")
        
        print()
        log("Projects WITHOUT .cursor:", "header")
        for p in without_cursor:
            print(f"  - {p['name']} ({p['path']})")
        
        print()
        return
    
    # Require target path
    if not target_path:
        log("Usage: cursor-setup.exe <ProjectPath> [Options]", "warning")
        print()
        log("Options:", "info")
        print("  -Force      Overwrite existing .cursor")
        print("  -NoBackup   Skip backup before overwriting")
        print("  -List       List all projects")
        print()
        log("Examples:", "info")
        print("  cursor-setup.exe D:\\\\Projects\\\\MyApp")
        print("  cursor-setup.exe D:\\\\Projects\\\\MyApp -Force")
        print("  cursor-setup.exe -List")
        print()
        return
    
    # Validate source exists
    if not CURSOR_SOURCE.exists():
        log(f"Source .cursor not found at: {CURSOR_SOURCE}", "error")
        log("Please update SOURCE_ROOT in the script", "error")
        sys.exit(1)
    
    # Run installation
    success, message = install_cursor(target_path, force=force, backup=backup)
    
    if success:
        log(message, "success")
        print()
    else:
        log(message, "error")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    # Write installer script
    with open(SETUP_SCRIPT, "w", encoding="utf-8") as f:
        f.write(installer_code)
    
    print(f"[OK] Created installer script: {SETUP_SCRIPT}")

def build_exe():
    """Build the .exe using PyInstaller"""
    
    if not CURSOR_SOURCE.exists():
        print(f"[X] Source .cursor not found at: {CURSOR_SOURCE}")
        return False
    
    log("Building standalone .exe...", "header")
    
    # PyInstaller arguments
    args = [
        str(SETUP_SCRIPT),
        "--name=cursor-setup",
        "--onefile",
        "--console",
        f"--distpath={DIST_FOLDER}",
        f"--workpath={SCRIPT_DIR}/build",
        "--clean",
        "--noconfirm",
        # Embed source path
        f"--add-data={CURSOR_SOURCE};.cursor_source",
    ]
    
    try:
        PyInstaller.__main__.run(args)
        log("Build completed successfully!", "success")
        
        # Find the exe
        exe_path = DIST_FOLDER / "cursor-setup.exe"
        if exe_path.exists():
            log(f"Executable: {exe_path}", "success")
            return True
    except Exception as e:
        log(f"Build failed: {e}", "error")
        return False
    
    return False

def main():
    print()
    print("=" * 50)
    print("  CURSOR SETUP EXE BUILDER")
    print("=" * 50)
    print()
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        log("PyInstaller found", "success")
    except ImportError:
        log("PyInstaller not found. Installing...", "info")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        log("PyInstaller installed", "success")
    
    # Create installer script
    create_installer_script()
    
    # Build exe
    if build_exe():
        print()
        log("Done! You can now run:", "success")
        print(f"  {DIST_FOLDER / 'cursor-setup.exe'}")
        print()
    else:
        print()
        log("Build failed. Check errors above.", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
