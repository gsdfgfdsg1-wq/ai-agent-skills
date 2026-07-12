#!/usr/bin/env python3
"""py-dead-code — detect unused imports and unreachable code in Python files.

Usage:
    python py_dead_code.py PATH [PATH ...] [--ignore-imports] [--ignore-unreachable] [--json]

Uses Python's ast module for reliable, dependency-free analysis.
"""

import argparse
import ast
import json
import os
import sys

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".venv", "venv", "env"}
PY_EXT = ".py"

# Built-in names that are always available
BUILTIN_NAMES = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
BUILTIN_NAMES.update({
    "__name__", "__file__", "__doc__", "__package__", "__spec__",
    "__loader__", "__builtins__", "__all__", "__cached__", "__import__",
})


class ImportCollector(ast.NodeVisitor):
    """Collect all import statements and their imported names."""

    def __init__(self):
        self.imports = []  # list of (name, alias_or_name, line)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.name
            used_as = alias.asname or alias.name.split(".")[0]
            self.imports.append((name, used_as, node.lineno))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            name = f"{module}.{alias.name}" if module else alias.name
            used_as = alias.asname or alias.name
            if used_as == "*":
                # Can't track star imports
                continue
            self.imports.append((name, used_as, node.lineno))
        self.generic_visit(node)


class NameCollector(ast.NodeVisitor):
    """Collect all names used in the code (not just defined)."""

    def __init__(self):
        self.used_names = set()

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Collect the root name of chained attributes (e.g., os.path -> os)
        root = node
        while isinstance(root, ast.Attribute):
            root = root.value
        if isinstance(root, ast.Name):
            self.used_names.add(root.id)
        self.generic_visit(node)


class UnreachableCollector(ast.NodeVisitor):
    """Detect unreachable code after return/break/raise/continue."""

    TERMINATORS = (ast.Return, ast.Break, ast.Raise, ast.Continue)

    def __init__(self):
        self.unreachable = []  # list of (line, kind, after_what)

    def _check_body(self, body):
        """Check a list of statements for unreachable code after a terminator."""
        found_terminator = None
        for stmt in body:
            if found_terminator is not None:
                self.unreachable.append(
                    (stmt.lineno, "unreachable_code", found_terminator)
                )
                break  # Only report first unreachable statement
            if isinstance(stmt, self.TERMINATORS):
                kind = type(stmt).__name__.lower()
                found_terminator = kind
            elif isinstance(stmt, ast.If):
                # Check both branches
                self._check_body(stmt.body)
                self._check_body(stmt.orelse)
            elif isinstance(stmt, ast.For) or isinstance(stmt, ast.While):
                self._check_body(stmt.body)
                self._check_body(stmt.orelse)
            elif isinstance(stmt, ast.With):
                self._check_body(stmt.body)
            elif isinstance(stmt, ast.Try):
                self._check_body(stmt.body)
                for handler in stmt.handlers:
                    self._check_body(handler.body)
                self._check_body(stmt.orelse)
                self._check_body(stmt.finalbody)

    def visit_FunctionDef(self, node):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_Module(self, node):
        self._check_body(node.body)


def analyze_file(filepath):
    """Analyze a single Python file for dead code."""
    findings = []

    try:
        with open(filepath, encoding="utf-8") as f:
            source = f.read()
    except (OSError, UnicodeDecodeError) as e:
        return [{"file": filepath, "error": str(e)}]

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        return [{"file": filepath, "error": f"SyntaxError: {e}"}]

    # Collect imports
    imp_collector = ImportCollector()
    imp_collector.visit(tree)

    # Collect used names
    name_collector = NameCollector()
    name_collector.visit(tree)

    # Find unused imports
    for full_name, used_as, line in imp_collector.imports:
        if used_as not in name_collector.used_names and used_as not in BUILTIN_NAMES:
            # Common patterns: TYPE_CHECKING, __all__, etc.
            if used_as == "TYPE_CHECKING":
                continue
            findings.append({
                "file": filepath,
                "line": line,
                "type": "unused_import",
                "name": full_name,
                "used_as": used_as,
                "message": f"Unused import: {full_name} (imported as '{used_as}')",
            })

    # Find unreachable code
    unreach_collector = UnreachableCollector()
    unreach_collector.visit(tree)

    for line, kind, after_what in unreach_collector.unreachable:
        findings.append({
            "file": filepath,
            "line": line,
            "type": kind,
            "after": after_what,
            "message": f"Unreachable code after {after_what} on line {line}",
        })

    return findings


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(PY_EXT):
                yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if fn.endswith(PY_EXT):
                        yield os.path.join(root, fn)


def main():
    ap = argparse.ArgumentParser(
        description="Detect unused imports and unreachable code in Python files."
    )
    ap.add_argument("paths", nargs="+", help="Python files or directories to scan")
    ap.add_argument("--ignore-imports", action="store_true",
                    help="skip unused import detection")
    ap.add_argument("--ignore-unreachable", action="store_true",
                    help="skip unreachable code detection")
    ap.add_argument("--json", action="store_true",
                    help="output JSON results")
    args = ap.parse_args()

    all_findings = []
    for fp in _iter_targets(args.paths):
        findings = analyze_file(fp)
        if args.ignore_imports:
            findings = [f for f in findings if f.get("type") != "unused_import"]
        if args.ignore_unreachable:
            findings = [f for f in findings if f.get("type") != "unreachable_code"]
        all_findings.extend(findings)

    if args.json:
        print(json.dumps(all_findings, indent=2, ensure_ascii=False))
    else:
        if not all_findings:
            print("No dead code found.")
        for f in all_findings:
            if "error" in f:
                print(f"[ERROR] {f['file']}: {f['error']}")
            else:
                print(f"{f['file']}:{f['line']}: {f['message']}")

    sys.exit(1 if any(f.get("type") in ("unused_import", "unreachable_code") for f in all_findings) else 0)


if __name__ == "__main__":
    main()
