#!/usr/bin/env python3
"""
Cursor Enterprise Framework - Standalone Installer v1.0.0
========================================================
Compiled .exe for installing .cursor to any project.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURATION - Update this path to your Cursor Enterprise Framework location
# =============================================================================
SOURCE_ROOT = Path(r"D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR")
CURSOR_SOURCE = SOURCE_ROOT / ".cursor"

# =============================================================================
# COLORS
# =============================================================================
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
                components.append({"name": item.name, "path": item, "files": file_count})
    return components

def discover_projects():
    """Find projects in common locations"""
    search_paths = [
        Path("D:/PROJECTS"),
        Path("C:/Projects"),
        Path("C:/Dev"),
        Path("D:/Dev"),
    ]
    with_cursor, without_cursor = [], []
    for sp in search_paths:
        if sp.exists():
            for item in sp.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    info = {"name": item.name, "path": item}
                    if (item / ".cursor").exists():
                        with_cursor.append(info)
                    else:
                        without_cursor.append(info)
    return with_cursor, without_cursor

def install_cursor(target_path, force=False, backup=True):
    """Install .cursor to target project"""
    target_cursor = Path(target_path) / ".cursor"
    if not Path(target_path).exists():
        return False, "Target path does not exist"
    if target_cursor.exists():
        if not force:
            return False, "Target already has .cursor. Use -Force to overwrite."
        if backup:
            bp = target_cursor.parent / f".cursor.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            log(f"Creating backup: {bp}", "info")
            shutil.copytree(target_cursor, bp)
            log("Backup created", "success")
        shutil.rmtree(target_cursor)
    try:
        shutil.copytree(CURSOR_SOURCE, target_cursor)
        fc = sum(1 for _ in target_cursor.rglob("*") if _.is_file())
        return True, f"Installed! ({fc} files)"
    except Exception as e:
        return False, f"Failed: {e}"

def main():
    print()
    print("=" * 50)
    print("  CURSOR ENTERPRISE FRAMEWORK - SETUP WIZARD")
    print("=" * 50)
    print()
    
    args = sys.argv[1:]
    target_path = None
    force = any(a.lower() in ("-force", "/force") for a in args)
    nobackup = any(a.lower() in ("-nobackup", "/nobackup", "-nb") for a in args)
    list_mode = any(a.lower() in ("-list", "/list", "--list") for a in args)
    help_mode = any(a.lower() in ("-help", "/help", "-h", "--help") for a in args)
    
    for arg in args:
        if not arg.startswith("-"):
            target_path = arg
            break
    
    log("Source: " + str(CURSOR_SOURCE), "header")
    log("Components:", "header")
    for c in get_components():
        log(f"  [{c['name']}] - {c['files']} files", "info")
    print()
    
    if help_mode or len(args) == 0:
        log("Usage:", "header")
        print()
        print("  cursor-setup.exe <ProjectPath> [Options]")
        print()
        log("Options:", "info")
        print("  -Force      Overwrite existing .cursor")
        print("  -NoBackup   Skip backup (with -Force)")
        print("  -List       List all projects in D:/Projects")
        print()
        log("Examples:", "info")
        print('  cursor-setup.exe "D:\\Projects\\MyApp"')
        print('  cursor-setup.exe "D:\\Projects\\MyApp" -Force')
        print("  cursor-setup.exe -List")
        print()
        return
    
    if list_mode:
        log("Discovering projects...", "info")
        print()
        with_c, without_c = discover_projects()
        log("WITH .cursor:", "header")
        for p in with_c:
            print(f"  + {p['name']}")
        print()
        log("WITHOUT .cursor:", "header")
        for p in without_c:
            print(f"  - {p['name']}")
        print()
        return
    
    if not target_path:
        log("Usage: cursor-setup.exe <ProjectPath>", "warning")
        print('  Example: cursor-setup.exe "D:\\Projects\\MyApp"')
        return
    
    if not CURSOR_SOURCE.exists():
        log(f"Source .cursor not found: {CURSOR_SOURCE}", "error")
        log("Update SOURCE_ROOT in the script", "error")
        sys.exit(1)
    
    success, msg = install_cursor(target_path, force=force, backup=not nobackup)
    if success:
        log(msg, "success")
        print()
    else:
        log(msg, "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
