#!/usr/bin/env python3
"""
Skill Dependency Auto-Installer
Part of Cursor Enterprise Framework

Automatically installs dependencies when skills are triggered.
Checks requirements before running skill tasks.

Usage:
    python skill-installer.py check <skill_name>
    python skill-installer.py install <skill_name>
    python skill-installer.py list
    python skill-installer.py all
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    import importlib.metadata
    PYTHON_VERSION = 3
except ImportError:
    import importlib
    PYTHON_VERSION = 2


class PackageManager(Enum):
    PIP = "pip"
    NPM = "npm"
    YARN = "yarn"
    SYSTEM = "system"


@dataclass
class Package:
    name: str
    version: str
    description: str
    installed: bool = False
    version_installed: Optional[str] = None


@dataclass
class DependencyCheck:
    skill: str
    skill_name: str
    python_missing: List[Package]
    node_missing: List[Package]
    system_missing: List[Package]
    all_satisfied: bool


class SkillDependencyInstaller:
    """Auto-installer for skill dependencies"""
    
    def __init__(self, manifest_path: str = None):
        if manifest_path is None:
            # Default to .cursor/scripts/skill-dependencies.json
            base_dir = Path(__file__).parent.parent
            manifest_path = base_dir / "scripts" / "skill-dependencies.json"
        
        self.manifest_path = Path(manifest_path)
        self.manifest = self._load_manifest()
        self.config = self.manifest.get("autoInstallConfig", {})
    
    def _load_manifest(self) -> dict:
        """Load skill dependencies manifest"""
        if not self.manifest_path.exists():
            print(f"Warning: Manifest not found at {self.manifest_path}")
            return {"skills": {}, "autoInstallConfig": {"enabled": True}}
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _run_command(self, cmd: str, capture: bool = True) -> Tuple[int, str, str]:
        """Run shell command and return exit code, stdout, stderr"""
        try:
            if capture:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                return result.returncode, result.stdout.strip(), result.stderr.strip()
            else:
                return subprocess.call(cmd, shell=True), "", ""
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def _check_python_package(self, package_name: str) -> Tuple[bool, str]:
        """Check if Python package is installed"""
        try:
            if PYTHON_VERSION == 3:
                version = importlib.metadata.version(package_name)
                return True, version
            else:
                # Python 2 fallback
                result = self._run_command(f'pip show {package_name}')
                if result[0] == 0 and result[1]:
                    for line in result[1].split('\n'):
                        if line.startswith('Version:'):
                            return True, line.split(':', 1)[1].strip()
                    return True, "unknown"
                return False, None
        except Exception:
            return False, None
    
    def _check_node_package(self, package_name: str) -> Tuple[bool, str]:
        """Check if Node package is installed"""
        # Check in node_modules
        if Path("node_modules").exists():
            pkg_path = Path("node_modules") / package_name / "package.json"
            if pkg_path.exists():
                try:
                    with open(pkg_path, 'r') as f:
                        data = json.load(f)
                        return True, data.get("version", "unknown")
                except:
                    pass
        
        # Try npm list
        result = self._run_command(f'npm list {package_name} --depth=0 2>/dev/null')
        if result[0] == 0 and package_name in result[1]:
            # Extract version
            for line in result[1].split('\n'):
                if package_name in line and '@' in line:
                    parts = line.split('@')
                    if len(parts) >= 2:
                        return True, parts[-1].strip()
            return True, "installed"
        
        return False, None
    
    def _check_tesseract(self) -> Tuple[bool, str]:
        """Check if Tesseract OCR is installed"""
        code, stdout, stderr = self._run_command("tesseract --version 2>&1")
        if code == 0 and stdout:
            version = stdout.split('\n')[0] if stdout else "installed"
            return True, version
        return False, None
    
    def _get_os(self) -> str:
        """Get current OS"""
        if sys.platform.startswith('win'):
            return 'windows'
        elif sys.platform.startswith('darwin'):
            return 'macos'
        else:
            return 'linux'
    
    def check_skill(self, skill_name: str) -> DependencyCheck:
        """Check dependencies for a specific skill"""
        skills = self.manifest.get("skills", {})
        
        if skill_name not in skills:
            # Try case-insensitive match
            for key in skills:
                if key.lower() == skill_name.lower():
                    skill_name = key
                    break
            else:
                return DependencyCheck(
                    skill=skill_name,
                    skill_name=f"Unknown skill: {skill_name}",
                    python_missing=[],
                    node_missing=[],
                    system_missing=[],
                    all_satisfied=True
                )
        
        skill_data = skills[skill_name]
        dependencies = skill_data.get("dependencies", {})
        
        python_missing = []
        node_missing = []
        system_missing = []
        
        # Check Python dependencies
        if "python" in dependencies:
            for pkg in dependencies["python"].get("packages", []):
                installed, version = self._check_python_package(pkg["name"])
                package = Package(
                    name=pkg["name"],
                    version=pkg.get("version", "latest"),
                    description=pkg.get("description", ""),
                    installed=installed,
                    version_installed=version
                )
                if not installed:
                    python_missing.append(package)
        
        # Check Node dependencies
        if "node" in dependencies:
            for pkg in dependencies["node"].get("packages", []):
                installed, version = self._check_node_package(pkg["name"])
                package = Package(
                    name=pkg["name"],
                    version=pkg.get("version", "latest"),
                    description=pkg.get("description", ""),
                    installed=installed,
                    version_installed=version
                )
                if not installed:
                    node_missing.append(package)
        
        # Check system dependencies
        if "system" in dependencies:
            os_name = self._get_os()
            if os_name in dependencies["system"]:
                sys_dep = dependencies["system"][os_name]
                
                if "tesseract" in skill_name.lower() or "ocr" in skill_name.lower():
                    installed, version = self._check_tesseract()
                    if not installed:
                        system_missing.append(Package(
                            name=sys_dep.get("name", "System dependency"),
                            version="required",
                            description=sys_dep.get("description", "")
                        ))
        
        all_satisfied = len(python_missing) == 0 and len(node_missing) == 0 and len(system_missing) == 0
        
        return DependencyCheck(
            skill=skill_name,
            skill_name=skill_data.get("name", skill_name),
            python_missing=python_missing,
            node_missing=node_missing,
            system_missing=system_missing,
            all_satisfied=all_satisfied
        )
    
    def install_skill(self, skill_name: str, verbose: bool = True) -> bool:
        """Install dependencies for a specific skill"""
        check = self.check_skill(skill_name)
        
        if check.all_satisfied:
            if verbose:
                print(f"✅ {check.skill_name}: All dependencies satisfied")
            return True
        
        if verbose:
            print(f"\n📦 Installing dependencies for: {check.skill_name}")
            print("=" * 50)
        
        success = True
        
        # Install Python packages
        if check.python_missing:
            packages = [pkg.name for pkg in check.python_missing]
            cmd = f"pip install {' '.join(packages)}"
            
            if verbose:
                print(f"\n🐍 Installing Python packages: {', '.join(packages)}")
            
            code, stdout, stderr = self._run_command(cmd)
            
            if code == 0:
                if verbose:
                    print(f"   ✅ Python packages installed successfully")
            else:
                if verbose:
                    print(f"   ❌ Failed: {stderr}")
                success = False
        
        # Install Node packages
        if check.node_missing:
            packages = [pkg.name for pkg in check.node_missing]
            
            if verbose:
                print(f"\n📦 Installing Node packages: {', '.join(packages)}")
            
            # Check if npm or yarn
            code_yarn, _, _ = self._run_command("yarn --version 2>/dev/null")
            if code_yarn == 0:
                cmd = f"yarn add {' '.join(packages)}"
            else:
                cmd = f"npm install {' '.join(packages)}"
            
            code, stdout, stderr = self._run_command(cmd)
            
            if code == 0:
                if verbose:
                    print(f"   ✅ Node packages installed successfully")
            else:
                if verbose:
                    print(f"   ❌ Failed: {stderr}")
                success = False
        
        # Install system packages
        if check.system_missing:
            skills = self.manifest.get("skills", {})
            skill_data = skills.get(skill_name, {})
            deps = skill_data.get("dependencies", {})
            os_name = self._get_os()
            
            if "system" in deps and os_name in deps["system"]:
                sys_dep = deps["system"][os_name]
                install_cmd = sys_dep.get("installCommand", "")
                
                if verbose:
                    print(f"\n🖥️  Installing system package: {sys_dep.get('name', 'System dependency')}")
                    print(f"   Command: {install_cmd}")
                
                if "tesseract" in skill_name.lower():
                    # Special handling for Tesseract
                    if os_name == 'windows':
                        print("   ℹ️  Please download Tesseract from:")
                        print("      https://github.com/UB-Mannheim/tesseract/wiki")
                        print("   Then run the installer and add to PATH")
                    else:
                        code, stdout, stderr = self._run_command(install_cmd)
                        if code == 0:
                            if verbose:
                                print(f"   ✅ System package installed successfully")
                        else:
                            if verbose:
                                print(f"   ⚠️  Manual installation may be required")
                            success = self.config.get("continueOnError", True)
                else:
                    if verbose:
                        print(f"   ℹ️  Manual installation required: {install_cmd}")
        
        return success
    
    def install_all(self, verbose: bool = True) -> Dict[str, bool]:
        """Install all skill dependencies"""
        results = {}
        skills = self.manifest.get("skills", {})
        
        for skill_name in skills:
            if verbose:
                print(f"\n{'='*60}")
            results[skill_name] = self.install_skill(skill_name, verbose)
        
        return results
    
    def list_skills(self) -> List[str]:
        """List all available skills in manifest"""
        return list(self.manifest.get("skills", {}).keys())
    
    def format_check_report(self, check: DependencyCheck) -> str:
        """Format dependency check as a readable report"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📋 Dependency Check: {check.skill_name}")
        lines.append(f"{'='*60}")
        
        if check.all_satisfied:
            lines.append(f"\n✅ All dependencies satisfied!")
            return '\n'.join(lines)
        
        if check.python_missing:
            lines.append(f"\n🐍 Python packages (missing):")
            for pkg in check.python_missing:
                lines.append(f"   • {pkg.name}")
                if pkg.description:
                    lines.append(f"     {pkg.description}")
        
        if check.node_missing:
            lines.append(f"\n📦 Node packages (missing):")
            for pkg in check.node_missing:
                lines.append(f"   • {pkg.name}")
                if pkg.description:
                    lines.append(f"     {pkg.description}")
        
        if check.system_missing:
            lines.append(f"\n🖥️  System packages (missing):")
            for pkg in check.system_missing:
                lines.append(f"   • {pkg.name}")
                if pkg.description:
                    lines.append(f"     {pkg.description}")
        
        lines.append(f"\n💡 Run: python skill-installer.py install {check.skill}")
        
        return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("""
Skill Dependency Auto-Installer
===============================

Usage:
    python skill-installer.py check <skill_name>
    python skill-installer.py install <skill_name>
    python skill-installer.py install-all
    python skill-installer.py list

Examples:
    python skill-installer.py check document-ocr
    python skill-installer.py install document-ocr
    python skill-installer.py install-all
    python skill-installer.py list
""")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    installer = SkillDependencyInstaller()
    
    if command == "check":
        if len(sys.argv) < 3:
            print("Error: Please specify skill name")
            print("Example: python skill-installer.py check document-ocr")
            sys.exit(1)
        
        skill_name = sys.argv[2]
        check = installer.check_skill(skill_name)
        print(installer.format_check_report(check))
    
    elif command == "install":
        if len(sys.argv) < 3:
            print("Error: Please specify skill name")
            print("Example: python skill-installer.py install document-ocr")
            sys.exit(1)
        
        skill_name = sys.argv[2]
        success = installer.install_skill(skill_name)
        
        if success:
            print(f"\n✅ {skill_name} dependencies installed successfully")
        else:
            print(f"\n⚠️  {skill_name} installation completed with warnings")
            sys.exit(1)
    
    elif command in ("install-all", "all"):
        print("🔧 Installing all skill dependencies...")
        results = installer.install_all()
        
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        print(f"\n{'='*60}")
        print(f"📊 Installation Summary: {success_count}/{total_count} skills completed")
        
        for skill, success in results.items():
            status = "✅" if success else "⚠️"
            print(f"   {status} {skill}")
    
    elif command == "list":
        skills = installer.list_skills()
        print("\n📚 Available Skills with Dependencies:")
        print("=" * 50)
        
        for skill_name in skills:
            skill_data = installer.manifest.get("skills", {}).get(skill_name, {})
            print(f"\n• {skill_name}")
            print(f"  {skill_data.get('description', 'No description')}")
            
            deps = skill_data.get("dependencies", {})
            if "python" in deps:
                pkgs = [p["name"] for p in deps["python"].get("packages", [])]
                print(f"  🐍 Python: {', '.join(pkgs)}")
            if "node" in deps:
                pkgs = [p["name"] for p in deps["node"].get("packages", [])]
                print(f"  📦 Node: {', '.join(pkgs)}")
    
    else:
        print(f"Unknown command: {command}")
        print("Use: check, install, install-all, or list")
        sys.exit(1)


if __name__ == "__main__":
    main()
