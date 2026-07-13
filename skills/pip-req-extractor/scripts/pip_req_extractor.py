#!/usr/bin/env python3
"""Extract Python import statements from source files and generate requirements."""

import argparse
import ast
import json
import os
import sys
from pathlib import Path

STDLIB_NAMES = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else {
    "abc", "argparse", "ast", "asyncio", "base64", "binascii", "bisect", "calendar",
    "collections", "configparser", "contextlib", "copy", "csv", "datetime", "decimal",
    "difflib", "email", "enum", "fileinput", "fnmatch", "fractions", "functools",
    "glob", "gzip", "hashlib", "heapq", "html", "http", "importlib", "inspect",
    "io", "itertools", "json", "keyword", "linecache", "logging", "math", "mimetypes",
    "multiprocessing", "operator", "os", "pathlib", "pickle", "platform", "pprint",
    "queue", "re", "secrets", "shelve", "shutil", "signal", "socket", "sqlite3",
    "string", "struct", "subprocess", "sys", "tarfile", "tempfile", "textwrap",
    "threading", "time", "token", "tokenize", "traceback", "typing", "unicodedata",
    "unittest", "urllib", "uuid", "warnings", "weakref", "xml", "zipfile", "zlib",
}


def extract_imports(filepath):
    """Extract all top-level import names from a Python file."""
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        print(f"Warning: cannot read {filepath}: {e}", file=sys.stderr)
        return []
    try:
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError as e:
        print(f"Warning: syntax error in {filepath}: {e}", file=sys.stderr)
        return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                imports.append(node.module.split(".")[0])
    return imports


def scan_path(target):
    """Scan a file or directory for Python files."""
    target = Path(target)
    if target.is_file():
        if target.suffix == ".py":
            return [target]
        return []
    py_files = []
    for root, dirs, files in os.walk(target):
        # Skip hidden dirs and common virtual env dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in (
            "__pycache__", "venv", ".venv", "env", ".env", "node_modules", "site-packages"
        )]
        for f in sorted(files):
            if f.endswith(".py"):
                py_files.append(Path(root) / f)
    return py_files


def cmd_extract(args):
    py_files = scan_path(args.path)
    if not py_files:
        print(f"No Python files found in: {args.path}", file=sys.stderr)
        sys.exit(1)

    all_imports = []
    for fp in py_files:
        all_imports.extend(extract_imports(fp))

    third_party = sorted(set(m for m in all_imports if m not in STDLIB_NAMES and not m.startswith("_")))
    stdlib = sorted(set(m for m in all_imports if m in STDLIB_NAMES))

    if args.json:
        result = {
            "source": str(args.path),
            "files_scanned": len(py_files),
            "third_party": third_party,
            "stdlib": stdlib,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Files scanned: {len(py_files)}")
        print(f"Third-party packages ({len(third_party)}):")
        for pkg in third_party:
            print(f"  {pkg}")
        if args.include_stdlib:
            print(f"Standard library ({len(stdlib)}):")
            for pkg in stdlib:
                print(f"  {pkg}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for pkg in third_party:
                f.write(pkg + "\n")
        if not args.json:
            print(f"Written to: {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract Python imports and generate requirements."
    )
    sub = parser.add_subparsers(dest="command")

    p_extract = sub.add_parser("extract", help="Extract imports from Python files")
    p_extract.add_argument("--path", required=True, help="File or directory to scan")
    p_extract.add_argument("--output", help="Write requirements to file")
    p_extract.add_argument("--include-stdlib", action="store_true", help="Include stdlib modules")
    p_extract.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "extract":
        cmd_extract(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
