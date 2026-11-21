"""
Code Utilities

Code analysis and manipulation utilities.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class CodeIssue:
    """Represents a code issue."""

    line: int
    column: int
    severity: str
    message: str
    rule: str


def detect_language(code: str) -> str:
    """
    Detect programming language from code.

    Args:
        code: Code to analyze

    Returns:
        Detected language
    """
    patterns = {
        "python": [r"def \w+\(", r"import ", r"from \w+ import", r"if __name__"],
        "javascript": [r"const ", r"let ", r"function ", r"=>", r"console\."],
        "typescript": [r": string", r": number", r"interface \w+", r"type \w+"],
        "java": [r"public class", r"private ", r"System\.out", r"@Override"],
        "csharp": [r"public class", r"namespace ", r"using System", r"Console\."],
        "go": [r"func ", r"package ", r"fmt\.", r"import \("],
        "rust": [r"fn ", r"let mut", r"impl ", r"use std"],
        "html": [r"<!DOCTYPE", r"<html", r"<div", r"<span"],
        "css": [r"\{[\s\S]*?\}", r"@media", r"\.[a-zA-Z]+[\s]*\{", r"#[a-zA-Z]+[\s]*\{"],
    }

    scores: dict[str, int] = {lang: 0 for lang in patterns}

    for lang, lang_patterns in patterns.items():
        for pattern in lang_patterns:
            if re.search(pattern, code):
                scores[lang] += 1

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "unknown"


def extract_imports(code: str) -> list[str]:
    """
    Extract import statements from code.

    Args:
        code: Code to analyze

    Returns:
        List of imports
    """
    patterns = [
        r"import\s+([\w.]+)",
        r"from\s+([\w.]+)\s+import",
        r"require\s*\(\s*['\"]([^'\"]+)['\"]",
        r"use\s+([\w\\]+);",
    ]

    imports = []
    for pattern in patterns:
        imports.extend(re.findall(pattern, code))
    return imports


def extract_functions(code: str) -> list[dict]:
    """
    Extract function definitions from code.

    Args:
        code: Code to analyze

    Returns:
        List of function info dicts
    """
    patterns = [
        (r"(?:def|function|fn)\s+(\w+)\s*\([^)]*\)", "named"),
        (r"(?:const|let|var)\s+(\w+)\s*=\s*(?:function|async)", "arrow"),
        (r"class\s+(\w+)", "class"),
    ]

    functions = []
    for pattern, func_type in patterns:
        for match in re.finditer(pattern, code):
            functions.append({
                "name": match.group(1),
                "type": func_type,
                "line": code[: match.start()].count("\n") + 1,
            })
    return functions


def check_em_dashes(code: str) -> list[CodeIssue]:
    """
    Check for em-dashes (zero tolerance).

    Args:
        code: Code to check

    Returns:
        List of issues found
    """
    issues = []
    lines = code.split("\n")

    for i, line in enumerate(lines, 1):
        if "\u2014" in line or "\u2013" in line or "—" in line:
            issues.append(CodeIssue(
                line=i,
                column=line.index("—") + 1 if "—" in line else 0,
                severity="error",
                message="Em-dash found (zero tolerance)",
                rule="no-em-dash",
            ))
    return issues


def check_todo_comments(code: str) -> list[CodeIssue]:
    """
    Check for TODO/FIXME comments.

    Args:
        code: Code to check

    Returns:
        List of TODO comments found
    """
    issues = []
    patterns = [
        r"//.*?(TODO|FIXME|HACK|XXX)",
        r"#.*?(TODO|FIXME|HACK|XXX)",
        r"/\*.*?(TODO|FIXME|HACK|XXX)",
    ]

    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity="warning",
                    message=f"Comment contains: {re.search(pattern, line, re.IGNORECASE).group(1)}",
                    rule="no-todo",
                ))
    return issues


def check_placeholder_patterns(code: str) -> list[CodeIssue]:
    """
    Check for placeholder/skeleton code patterns.

    Args:
        code: Code to check

    Returns:
        List of issues found
    """
    issues = []
    patterns = [
        r"//\s*\.\.\.",
        r"//\s*rest of code",
        r"//\s*implement here",
        r"//\s*\[skipped\]",
        r"/\*\s*\.\.\.\s*\*/",
    ]

    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity="error",
                    message="Placeholder pattern found",
                    rule="no-placeholder",
                ))
    return issues


def check_ai_slop_patterns(code: str) -> list[CodeIssue]:
    """
    Check for AI slop patterns.

    Args:
        code: Code to check

    Returns:
        List of issues found
    """
    issues = []
    patterns = [
        r"(?i)(elevate|seamless|unleash|next-gen|game-changer)",
        r"(?i)(jane doe|acme corp|lorem ipsum)",
        r"(?i)(quietly in use at)",
    ]

    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        for pattern in patterns:
            if re.search(pattern, line):
                issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity="warning",
                    message="AI slop pattern detected",
                    rule="no-ai-slop",
                ))
    return issues


def count_code_lines(code: str) -> dict[str, int]:
    """
    Count lines of code by type.

    Args:
        code: Code to count

    Returns:
        Dictionary with line counts
    """
    # ponytail: splitlines() is line-counting-friendly — it ignores the
    # trailing empty entry that split("\n") produces after a final "\n".
    # "code" excludes both blanks and comments (matches test expectation).
    lines = code.splitlines()
    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    comment = 0
    in_multiline = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("/*"):
            in_multiline = True
            comment += 1
        elif stripped.startswith("*/"):
            in_multiline = False
            comment += 1
        elif in_multiline:
            comment += 1
        elif stripped.startswith("//") or stripped.startswith("#"):
            comment += 1

    return {
        "total": total,
        "blank": blank,
        "code": total - blank - comment,
        "comment": comment,
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable form."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
