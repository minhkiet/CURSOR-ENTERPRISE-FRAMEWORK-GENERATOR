"""
Code Graph Module

Indexes project files and builds a dependency graph for Cursor to understand
the codebase structure. Detects imports/exports between files, categorizes
modules, classes, and functions.

Features:
    - Multi-language support (Python, C#, JavaScript, TypeScript, Java)
    - Import/export detection
    - Dependency graph generation
    - JSON output for Cursor consumption
    - File change tracking for auto-update

Usage:
    >>> from cursor_framework.code_graph import CodeGraph
    >>> graph = CodeGraph(root=".")
    >>> graph.scan()
    >>> print(graph.to_json())
    
    # CLI:
    >>> python -m cursor_framework dump-graph --root .

Output structure:
    {
        "project": "Project Name",
        "modules": [
            {
                "name": "installer",
                "path": "cursor-setup-gui-wpf/Services/Installer.cs",
                "type": "csharp",
                "classes": ["Installer", "BackupService"],
                "functions": ["Install()", "Backup()"],
                "imports": ["System.IO", "System.Diagnostics"],
                "exports": ["Installer"]
            }
        ],
        "dependencies": [
            {"from": "MainViewModel.cs", "to": "Installer.cs", "type": "uses"}
        ]
    }
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class LanguageType(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    CSHARP = "csharp"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    UNKNOWN = "unknown"


# Language file extensions mapping
LANGUAGE_EXTENSIONS = {
    ".py": LanguageType.PYTHON,
    ".cs": LanguageType.CSHARP,
    ".js": LanguageType.JAVASCRIPT,
    ".ts": LanguageType.TYPESCRIPT,
    ".tsx": LanguageType.TYPESCRIPT,
    ".jsx": LanguageType.JAVASCRIPT,
    ".java": LanguageType.JAVA,
    ".go": LanguageType.GO,
    ".rs": LanguageType.RUST,
}

# Patterns for detecting imports/exports
IMPORT_PATTERNS = {
    LanguageType.PYTHON: [
        r"^(?:from|import)\s+([a-zA-Z0-9_.]+)",
        r"^import\s+([a-zA-Z0-9_.]+)",
    ],
    LanguageType.CSHARP: [
        r"^using\s+([A-Za-z0-9.]+);",
        r"^\s*(?:public|private|internal)?\s*class\s+(\w+)",
    ],
    LanguageType.JAVASCRIPT: [
        r"^\s*import\s+(?:{[^}]+}|\w+)\s+from\s+['\"]([^'\"]+)['\"]",
        r"^\s*const\s+(\w+)\s*=\s*require\(['\"]([^'\"]+)['\"]\)",
        r"^export\s+(?:default\s+)?(?:class|function|const|async\s+function)\s+(\w+)",
    ],
    LanguageType.TYPESCRIPT: [
        r"^\s*import\s+(?:{[^}]+}|\w+)\s+from\s+['\"]([^'\"]+)['\"]",
        r"^\s*import\s+\*\s+as\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",
        r"^export\s+(?:default\s+)?(?:class|function|const|interface|type)\s+(\w+)",
    ],
    LanguageType.JAVA: [
        r"^package\s+([a-zA-Z0-9.]+)",
        r"^import\s+([a-zA-Z0-9.]+);",
    ],
    LanguageType.GO: [
        r"^package\s+(\w+)",
        r"^\s*import\s+(?:\(\s*)?['\"]([^'\"]+)['\"]",
    ],
    LanguageType.RUST: [
        r"^\s*use\s+([a-zA-Z0-9_:]+)",
        r"^pub\s+(?:fn|struct|enum|trait|mod)\s+(\w+)",
    ],
}

# Patterns for detecting functions/methods
FUNCTION_PATTERNS = {
    LanguageType.PYTHON: [
        r"^\s*(?:async\s+)?def\s+(\w+)\s*\(",
        r"^\s*class\s+(\w+)(?:\(|:)",
    ],
    LanguageType.CSHARP: [
        r"^\s*(?:public|private|protected|internal|static|async)?\s*(?:void|\w+)\s+(\w+)\s*\(",
        r"^\s*(?:public|private|protected|internal)?\s*class\s+(\w+)",
        r"^\s*(?:public|private|protected|internal)?\s*struct\s+(\w+)",
    ],
    LanguageType.JAVASCRIPT: [
        r"^\s*(?:async\s+)?function\s+(\w+)\s*\(",
        r"^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
        r"^\s*(?:class|export\s+class)\s+(\w+)",
    ],
    LanguageType.TYPESCRIPT: [
        r"^\s*(?:async\s+)?function\s+(\w+)\s*\(",
        r"^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
        r"^\s*(?:class|export\s+class|export\s+default\s+class)\s+(\w+)",
        r"^\s*(?:export\s+)?(?:interface|type)\s+(\w+)",
    ],
    LanguageType.JAVA: [
        r"^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:void|\w+)\s+(\w+)\s*\(",
        r"^\s*(?:public|private|protected)?\s*class\s+(\w+)",
    ],
    LanguageType.GO: [
        r"^\s*func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(",
        r"^\s*type\s+(\w+)\s+struct",
    ],
    LanguageType.RUST: [
        r"^\s*(?:pub\s+)?fn\s+(\w+)\s*\(",
        r"^\s*(?:pub\s+)?(?:struct|enum|trait|impl)\s+(\w+)",
    ],
}

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    ".git", ".svn", ".hg",
    "node_modules", "bower_components",
    "vendor", "packages", ".venv", "venv",
    "env", ".env", "__pycache__", ".pytest_cache",
    "bin", "obj", "build", "dist", ".next",
    ".cache", ".temp", "temp", "tmp",
}

# File extensions to scan
SCAN_EXTENSIONS = set(LANGUAGE_EXTENSIONS.keys())


@dataclass
class Module:
    """Represents a code module (file)."""
    name: str
    path: str
    language: str
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    lines: int = 0
    size_bytes: int = 0
    hash: str = ""


@dataclass
class Dependency:
    """Represents a dependency relationship between modules."""
    source: str  # file path
    target: str  # file path
    dep_type: str  # "import", "uses", "extends", "implements"
    target_module: str = ""  # imported module name


@dataclass
class CodeGraphResult:
    """Full code graph output."""
    project: str
    root: str
    scanned_at: str
    languages: dict[str, int]  # language -> file count
    module_count: int = 0
    dependency_count: int = 0
    modules: list[dict] = field(default_factory=list)
    dependencies: list[dict] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "root": self.root,
            "scanned_at": self.scanned_at,
            "languages": self.languages,
            "module_count": self.module_count,
            "dependency_count": self.dependency_count,
            "modules": self.modules,
            "dependencies": self.dependencies,
            "stats": self.stats,
        }


def _detect_language(path: Path) -> LanguageType:
    """Detect programming language from file extension."""
    ext = path.suffix.lower()
    return LANGUAGE_EXTENSIONS.get(ext, LanguageType.UNKNOWN)


def _compute_file_hash(content: str) -> str:
    """Compute MD5 hash of file content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()[:12]


def _parse_imports(content: str, language: LanguageType) -> list[str]:
    """Parse imports/exports from file content."""
    imports: list[str] = []
    patterns = IMPORT_PATTERNS.get(language, [])

    for line in content.splitlines():
        line = line.strip()
        for pattern in patterns:
            match = re.match(pattern, line, re.MULTILINE)
            if match:
                groups = match.groups()
                if groups:
                    imp = groups[0].strip()
                    if imp and imp not in imports:
                        imports.append(imp)
                break

    return imports


def _parse_functions_and_classes(content: str, language: LanguageType) -> tuple[list[str], list[str], list[str]]:
    """Parse functions, classes, and exports from file content."""
    classes: list[str] = []
    functions: list[str] = []
    exports: list[str] = []

    patterns = FUNCTION_PATTERNS.get(language, [])
    is_export = language in (LanguageType.JAVASCRIPT, LanguageType.TYPESCRIPT, LanguageType.PYTHON)

    for line in content.splitlines():
        line = line.strip()

        # Check for exports first (JavaScript/TypeScript)
        if is_export:
            export_match = re.match(
                r"export\s+(?:default\s+)?(?:class|function|const|interface|type|async\s+function)\s+(\w+)",
                line
            )
            if export_match:
                exports.append(export_match.group(1))

        # Check for classes/functions
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                name = match.group(1)
                # Determine if it's a class or function based on pattern
                if any(kw in line for kw in ["class ", "struct "]):
                    if name not in classes:
                        classes.append(name)
                else:
                    if name not in functions:
                        functions.append(name + "()")
                break

    return classes, functions, exports


def _normalize_import_path(imp: str, current_file: Path) -> Optional[str]:
    """Normalize import path to a file path."""
    # Remove common prefixes
    imp = imp.replace("./", "").replace("../", "")

    # Handle language-specific path conventions
    if current_file.suffix == ".cs":
        # C# namespace to path conversion
        return imp.replace(".", "/") + ".cs"
    elif current_file.suffix in (".ts", ".tsx", ".js", ".jsx"):
        # JavaScript/TypeScript path handling
        if not imp.endswith((".js", ".ts", ".tsx", ".jsx")):
            for ext in [".ts", ".tsx", ".js", ".jsx"]:
                potential = f"{imp}{ext}"
                if Path(potential).exists():
                    return potential
        return imp
    elif current_file.suffix == ".py":
        # Python path handling
        return imp.replace(".", "/") + ".py"

    return imp


class CodeGraph:
    """
    Scans project files and builds a dependency graph.

    Features:
        - Single-pass scan of all supported file types
        - Import/export detection for multiple languages
        - Dependency graph generation
        - File change tracking via content hashing
    """

    def __init__(
        self,
        root: str | Path = ".",
        exclude_dirs: Optional[set[str]] = None,
        include_hidden: bool = False,
    ) -> None:
        """
        Initialize the code graph scanner.

        Args:
            root: Root directory to scan
            exclude_dirs: Additional directories to exclude
            include_hidden: Whether to include hidden directories
        """
        self.root = Path(root).resolve()
        self.exclude_dirs = (EXCLUDE_DIRS | (exclude_dirs or set()))
        self.include_hidden = include_hidden
        self.modules: list[Module] = []
        self.dependencies: list[Dependency] = []
        self._file_content_cache: dict[str, str] = {}
        self._result: Optional[CodeGraphResult] = None

    def scan(self) -> CodeGraphResult:
        """
        Scan the project and build the dependency graph.

        Returns:
            CodeGraphResult with all modules and dependencies
        """
        self.modules = []
        self.dependencies = []
        self._file_content_cache = {}

        languages: dict[str, int] = defaultdict(int)
        project_name = self.root.name

        # First pass: collect all modules
        for path in self._iter_files():
            if path.is_file():
                module = self._parse_file(path)
                if module:
                    self.modules.append(module)
                    lang = module.language
                    languages[lang] = languages.get(lang, 0) + 1

        # Second pass: build dependency graph
        self._build_dependencies()

        # Build result
        self._result = CodeGraphResult(
            project=project_name,
            root=str(self.root),
            scanned_at=datetime.now().isoformat(timespec="seconds"),
            languages=dict(languages),
            module_count=len(self.modules),
            dependency_count=len(self.dependencies),
            modules=[asdict(m) for m in self.modules],
            dependencies=[
                {
                    "from": d.source,
                    "to": d.target,
                    "type": d.dep_type,
                    "target_module": d.target_module,
                }
                for d in self.dependencies
            ],
            stats=self._compute_stats(),
        )

        return self._result

    def _iter_files(self):
        """Iterate over files, respecting exclusions."""
        try:
            for path in self.root.rglob("*"):
                # Skip excluded directories
                parts = path.parts
                if any(excl in parts for excl in self.exclude_dirs):
                    continue

                # Skip hidden directories unless configured
                if not self.include_hidden:
                    if any(p.startswith(".") and p not in {".", ".."} for p in path.parts):
                        continue

                yield path
        except PermissionError:
            pass

    def _parse_file(self, path: Path) -> Optional[Module]:
        """Parse a single file and extract module info."""
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

        language = _detect_language(path)
        if language == LanguageType.UNKNOWN:
            return None

        # Cache content for dependency resolution
        rel_path = str(path.relative_to(self.root))
        self._file_content_cache[rel_path] = content

        # Parse imports, classes, functions
        imports = _parse_imports(content, language)
        classes, functions, exports = _parse_functions_and_classes(content, language)

        # For C#: classes are also exports
        if language == LanguageType.CSHARP:
            exports.extend(classes)

        try:
            size = path.stat().st_size
        except OSError:
            size = 0

        return Module(
            name=path.stem,
            path=rel_path,
            language=language.value,
            classes=classes,
            functions=functions[:20],  # Limit for performance
            imports=imports[:30],
            exports=exports[:20],
            lines=len(content.splitlines()),
            size_bytes=size,
            hash=_compute_file_hash(content),
        )

    def _build_dependencies(self) -> None:
        """Build dependency relationships between modules."""
        # Create a map of module names to paths for quick lookup
        module_map: dict[str, Module] = {}
        for module in self.modules:
            module_map[module.name.lower()] = module
            # Also map by path stem for exact matches
            path_stem = Path(module.path).stem
            module_map[path_stem.lower()] = module

        # Resolve dependencies
        for module in self.modules:
            content = self._file_content_cache.get(module.path, "")

            for imp in module.imports:
                # Try to find the imported module
                target = self._resolve_import(imp, module.path, module_map)
                if target and target.path != module.path:
                    # Check if dependency already exists
                    exists = any(
                        d.source == module.path and d.target == target.path
                        for d in self.dependencies
                    )
                    if not exists:
                        self.dependencies.append(Dependency(
                            source=module.path,
                            target=target.path,
                            dep_type="imports",
                            target_module=imp,
                        ))

    def _resolve_import(
        self,
        imp: str,
        current_path: str,
        module_map: dict[str, Module],
    ) -> Optional[Module]:
        """Resolve an import to a module."""
        # Direct name match
        imp_lower = imp.lower()
        if imp_lower in module_map:
            return module_map[imp_lower]

        # Try with common suffixes
        for suffix, lang in LANGUAGE_EXTENSIONS.items():
            if suffix.lstrip(".") in imp_lower:
                continue
            name = Path(imp.replace("/", ".")).stem.lower()
            if name in module_map:
                return module_map[name]

        # Try stem matching
        imp_stem = Path(imp).stem.lower()
        if imp_stem in module_map:
            return module_map[imp_stem]

        return None

    def _compute_stats(self) -> dict[str, Any]:
        """Compute summary statistics."""
        total_lines = sum(m.lines for m in self.modules)
        total_size = sum(m.size_bytes for m in self.modules)
        avg_functions = (
            sum(len(m.functions) for m in self.modules) / len(self.modules)
            if self.modules else 0
        )

        return {
            "total_lines": total_lines,
            "total_size_bytes": total_size,
            "avg_functions_per_module": round(avg_functions, 1),
            "avg_lines_per_module": round(total_lines / len(self.modules), 1) if self.modules else 0,
        }

    def to_json(self, indent: int = 2) -> str:
        """Return the graph as JSON string."""
        if self._result is None:
            self.scan()
        return json.dumps(self._result.to_dict(), indent=indent, ensure_ascii=False)

    def to_dict(self) -> dict[str, Any]:
        """Return the graph as a dictionary."""
        if self._result is None:
            self.scan()
        return self._result.to_dict()

    def find_module(self, name: str) -> Optional[Module]:
        """Find a module by name."""
        name_lower = name.lower()
        for module in self.modules:
            if module.name.lower() == name_lower:
                return module
        return None

    def find_dependents(self, module_path: str) -> list[Module]:
        """Find all modules that depend on the given module."""
        return [
            self.modules[i]
            for i, d in enumerate(self.dependencies)
            if d.target == module_path
        ]

    def find_dependencies(self, module_path: str) -> list[Module]:
        """Find all modules that the given module depends on."""
        return [
            self.modules[i]
            for i, d in enumerate(self.dependencies)
            if d.source == module_path
        ]

    def get_reachability(self, start_module: str) -> set[str]:
        """Get all modules reachable from a starting module."""
        reachable: set[str] = {start_module}
        queue = [start_module]

        while queue:
            current = queue.pop(0)
            for dep in self.find_dependencies(current):
                if dep.path not in reachable:
                    reachable.add(dep.path)
                    queue.append(dep.path)

        return reachable

    @property
    def result(self) -> Optional[CodeGraphResult]:
        """Get the scan result."""
        return self._result


def load_graph(path: str | Path) -> Optional[CodeGraphResult]:
    """
    Load a previously saved graph from JSON file.

    Args:
        path: Path to the JSON file

    Returns:
        CodeGraphResult or None if file doesn't exist
    """
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return CodeGraphResult(
            project=data.get("project", ""),
            root=data.get("root", ""),
            scanned_at=data.get("scanned_at", ""),
            languages=data.get("languages", {}),
            module_count=data.get("module_count", 0),
            dependency_count=data.get("dependency_count", 0),
            modules=data.get("modules", []),
            dependencies=data.get("dependencies", []),
            stats=data.get("stats", {}),
        )
    except (OSError, json.JSONDecodeError):
        return None


def save_graph(graph: CodeGraphResult, path: str | Path) -> Path:
    """
    Save a graph to JSON file.

    Args:
        graph: CodeGraphResult to save
        path: Output file path

    Returns:
        Path to the saved file
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(graph.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def main() -> int:
    """CLI entry point: `python -m cursor_framework.code_graph [root]`."""
    import argparse

    parser = argparse.ArgumentParser(description="Code Graph Indexer")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--minify", action="store_true", help="Minify JSON output")
    args = parser.parse_args()

    graph = CodeGraph(root=args.root)
    result = graph.scan()

    indent = None if args.minify else 2
    output = json.dumps(result.to_dict(), indent=indent, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Graph saved to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
