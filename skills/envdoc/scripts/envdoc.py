#!/usr/bin/env python3
"""Generate documentation from .env files without external dependencies."""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_env(filepath):
    """Parse a .env file and return list of (key, value, comment, line_no)."""
    entries = []
    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    current_comment = []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            current_comment = []
            continue
        if stripped.startswith("#"):
            current_comment.append(stripped.lstrip("#").strip())
            continue
        # KEY=VALUE or KEY:VALUE
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*[=:]\s*(.*)$", stripped)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            # Remove surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            comment = " ".join(current_comment) if current_comment else ""
            entries.append((key, value, comment, i))
            current_comment = []
        else:
            current_comment = []
    return entries


def cmd_generate(args):
    entries = parse_env(args.file)
    required = set(args.required.split(",")) if args.required else set()

    lines = ["# Environment Variables", "", f"Auto-generated from `{args.file}`.", ""]
    lines.append("| Variable | Default | Required | Description |")
    lines.append("| --- | --- | --- | --- |")

    for key, value, comment, line_no in entries:
        req = "Yes" if key in required else "No"
        default = f"`{value}`" if value else "_empty_"
        desc = comment or ""
        lines.append(f"| `{key}` | {default} | {req} | {desc} |")

    lines.append("")
    if required:
        lines.append(f"**Required variables:** {', '.join(f'`{k}`' for k in sorted(required))}")
        lines.append("")

    result = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(result)


def cmd_example(args):
    entries = parse_env(args.file)
    lines = []
    for key, value, comment, _ in entries:
        if comment:
            lines.append(f"# {comment}")
        # Show placeholder for non-empty values, empty for empty
        if value:
            lines.append(f"{key}=")
        else:
            lines.append(f"{key}=")
        lines.append("")

    result = "\n".join(lines).rstrip() + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(result, end="")


def cmd_audit(args):
    entries = parse_env(args.file)
    required = set(args.required.split(",")) if args.required else set()

    defined_keys = {e[0] for e in entries}
    missing = required - defined_keys
    extra = defined_keys - required if required else set()

    if args.json:
        print(json.dumps({
            "total": len(entries),
            "required": sorted(required),
            "defined": sorted(defined_keys),
            "missing": sorted(missing),
            "extra": sorted(extra),
        }, indent=2))
    else:
        print(f"Total variables: {len(entries)}")
        print(f"Required: {len(required)}")
        print(f"Defined: {len(defined_keys)}")
        if missing:
            print(f"Missing required: {', '.join(sorted(missing))}")
        if extra and required:
            print(f"Non-required defined: {', '.join(sorted(extra))}")

    if missing:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate documentation from .env files.")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("generate", help="Generate Markdown docs")
    p_gen.add_argument("--file", required=True, help=".env file")
    p_gen.add_argument("--required", default="", help="Comma-separated list of required variable names")
    p_gen.add_argument("--output", help="Output file")

    p_ex = sub.add_parser("example", help="Generate .env.example")
    p_ex.add_argument("--file", required=True, help=".env file")
    p_ex.add_argument("--output", help="Output file")

    p_audit = sub.add_parser("audit", help="Audit required variables")
    p_audit.add_argument("--file", required=True, help=".env file")
    p_audit.add_argument("--required", default="", help="Comma-separated list of required variable names")
    p_audit.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "example":
        cmd_example(args)
    elif args.command == "audit":
        cmd_audit(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
