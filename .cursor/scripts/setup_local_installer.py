#!/usr/bin/env python3
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

# Source .cursor location - resolved at runtime
_EXE_DIR = Path(sys.argv[0]).parent.resolve() if hasattr(sys, 'frozen') else Path(__file__).parent.resolve()
_MEI_PASS = getattr(sys, '_MEIPASS', str(_EXE_DIR))

# Find .cursor source: prefer bundled (_MEIPASS), fall back to exe-adjacent
_CURSOR_BUNDLED = Path(_MEI_PASS) / '.cursor_source'
_CURSOR_ADJACENT = _EXE_DIR / '.cursor'

if _CURSOR_BUNDLED.exists():
    SOURCE_ROOT = _EXE_DIR  # exe dir contains the bundled .cursor_source
    CURSOR_SOURCE = _CURSOR_BUNDLED
elif _CURSOR_ADJACENT.exists():
    SOURCE_ROOT = _EXE_DIR
    CURSOR_SOURCE = _CURSOR_ADJACENT
else:
    # Last resort: try relative path from script location
    SCRIPT_DIR = Path(__file__).parent.resolve()
    SOURCE_ROOT = SCRIPT_DIR
    CURSOR_SOURCE = SOURCE_ROOT / '.cursor'

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

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
        "header": "\n" + "="*50
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
        print("  cursor-setup.exe D:\\Projects\\MyApp")
        print("  cursor-setup.exe D:\\Projects\\MyApp -Force")
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
