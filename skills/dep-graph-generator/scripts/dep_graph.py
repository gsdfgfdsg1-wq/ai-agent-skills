#!/usr/bin/env python3
"""dep-graph-generator — parse package.json / requirements.txt and output dependency graph data.

Usage:
    python dep_graph.py DEP_FILE [--format json|dot|text] [--depth N]

Supports:
  - package.json  → reads dependencies + devDependencies, resolves node_modules
  - requirements.txt → one dep per line (pkg==ver, pkg>=ver, pkg~=ver, pkg)
"""

import argparse
import json
import os
import re
import sys


def _parse_package_json(path):
    """Parse package.json and return {name: [deps...]} adjacency."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    name = data.get("name", os.path.basename(os.path.dirname(os.path.abspath(path))))
    deps = {}
    all_deps = {}
    all_deps.update(data.get("dependencies", {}))
    all_deps.update(data.get("devDependencies", {}))

    deps[name] = sorted(all_deps.keys())

    # Try resolving nested deps from node_modules
    base_dir = os.path.dirname(os.path.abspath(path))
    nm_dir = os.path.join(base_dir, "node_modules")
    if os.path.isdir(nm_dir):
        for dep_name in all_deps:
            dep_pkg = os.path.join(nm_dir, dep_name, "package.json")
            if os.path.isfile(dep_pkg):
                try:
                    with open(dep_pkg, "r", encoding="utf-8") as f:
                        sub = json.load(f)
                    sub_deps = list(sub.get("dependencies", {}).keys())
                    deps[dep_name] = sorted(sub_deps)
                except (json.JSONDecodeError, OSError):
                    deps[dep_name] = []
            else:
                deps[dep_name] = []

    return name, deps


def _parse_requirements_txt(path):
    """Parse requirements.txt and return {root: [deps...]} adjacency."""
    root = os.path.basename(os.path.dirname(os.path.abspath(path)))
    deps_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Extract package name (before version specifier)
            m = re.match(r"^([A-Za-z0-9_.-]+)", line)
            if m:
                deps_list.append(m.group(1))
    deps = {root: sorted(deps_list)}
    return root, deps


def _to_text(root, deps, depth, current_depth=0, visited=None):
    """Render indented text tree."""
    if visited is None:
        visited = set()
    lines = []
    indent = "  " * current_depth
    children = deps.get(root, [])
    for child in children:
        marker = ""
        if child in visited:
            marker = " (see above)"
        lines.append(f"{indent}- {child}{marker}")
        if depth is not None and current_depth >= depth - 1:
            continue
        if child not in visited and child in deps:
            visited.add(child)
            lines.extend(_to_text(child, deps, depth, current_depth + 1, visited))
            visited.discard(child)
    return lines


def _to_dot(root, deps):
    """Render DOT (Graphviz) format."""
    lines = ["digraph deps {", "  rankdir=LR;"]
    edges = set()
    for parent, children in deps.items():
        for child in children:
            edges.add((parent, child))
    for a, b in sorted(edges):
        lines.append(f'  "{a}" -> "{b}";')
    lines.append("}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Parse package.json or requirements.txt and output dependency graph data."
    )
    ap.add_argument("file", help="package.json or requirements.txt path")
    ap.add_argument(
        "--format",
        choices=["json", "dot", "text"],
        default="text",
        help="output format (default: text)",
    )
    ap.add_argument("--depth", type=int, default=None, help="max traversal depth")
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    basename = os.path.basename(args.file).lower()
    if basename == "package.json":
        root, deps = _parse_package_json(args.file)
    elif basename in ("requirements.txt", "requirements.in", "constraints.txt"):
        root, deps = _parse_requirements_txt(args.file)
    else:
        # Try to guess
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                first_char = f.read(1)
            if first_char == "{":
                root, deps = _parse_package_json(args.file)
            else:
                root, deps = _parse_requirements_txt(args.file)
        except Exception:
            print("Error: cannot determine file format", file=sys.stderr)
            sys.exit(2)

    if args.format == "json":
        print(json.dumps({"root": root, "graph": deps}, indent=2, ensure_ascii=False))
    elif args.format == "dot":
        print(_to_dot(root, deps))
    else:
        print(root)
        for line in _to_text(root, deps, args.depth):
            print(line)


if __name__ == "__main__":
    main()
