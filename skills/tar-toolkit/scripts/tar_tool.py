#!/usr/bin/env python3
"""List, create, and extract tar archives without external dependencies."""

import argparse
import json
import os
import sys
import tarfile
from pathlib import Path


def cmd_list(args):
    try:
        with tarfile.open(args.archive, "r:*") as tf:
            members = tf.getmembers()
    except (OSError, tarfile.TarError) as e:
        print(f"Error: cannot open {args.archive}: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        items = []
        for m in members:
            items.append({
                "name": m.name,
                "size": m.size,
                "type": "dir" if m.isdir() else "file",
                "mode": oct(m.mode),
                "mtime": m.mtime,
            })
        print(json.dumps({"archive": args.archive, "entries": items}, indent=2))
    else:
        print(f"Archive: {args.archive}")
        print(f"{'Type':<6} {'Size':>12} {'Name'}")
        print(f"{'----':<6} {'----':>12} {'----'}")
        for m in members:
            t = "dir" if m.isdir() else "file"
            size_str = str(m.size) if not m.isdir() else "-"
            print(f"{t:<6} {size_str:>12} {m.name}")
        print(f"\nTotal: {len(members)} entries")


def cmd_create(args):
    source = Path(args.source)
    if not source.exists():
        print(f"Error: source '{args.source}' does not exist", file=sys.stderr)
        sys.exit(1)

    mode = {"tar": "w", "tar.gz": "w:gz", "tar.bz2": "w:bz2"}.get(args.format, "w:gz")
    output = args.output
    if not output:
        output = str(source.name) + "." + args.format.replace(".", "_")

    try:
        with tarfile.open(output, mode) as tf:
            if source.is_file():
                tf.add(str(source), arcname=source.name)
            else:
                for root, dirs, files in os.walk(str(source)):
                    for d in dirs:
                        full = os.path.join(root, d)
                        tf.add(full, arcname=os.path.relpath(full, str(source.parent)))
                    for f in files:
                        full = os.path.join(root, f)
                        tf.add(full, arcname=os.path.relpath(full, str(source.parent)))
        size = Path(output).stat().st_size
        print(f"Created: {output} ({size} bytes)")
    except (OSError, tarfile.TarError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_extract(args):
    output_dir = args.output or "."
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        with tarfile.open(args.archive, "r:*") as tf:
            # Security: prevent path traversal
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    print(f"Warning: skipping unsafe path: {member.name}", file=sys.stderr)
                    continue
            safe_members = [m for m in tf.getmembers()
                           if not m.name.startswith("/") and ".." not in m.name]
            tf.extractall(path=output_dir, members=safe_members)
        print(f"Extracted {len(safe_members)} entries to {output_dir}")
    except (OSError, tarfile.TarError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_info(args):
    try:
        with tarfile.open(args.archive, "r:*") as tf:
            members = tf.getmembers()
    except (OSError, tarfile.TarError) as e:
        print(f"Error: cannot open {args.archive}: {e}", file=sys.stderr)
        sys.exit(1)

    total_size = sum(m.size for m in members if not m.isdir())
    file_count = sum(1 for m in members if not m.isdir())
    dir_count = sum(1 for m in members if m.isdir())
    archive_size = Path(args.archive).stat().st_size
    ratio = (1 - archive_size / total_size) * 100 if total_size > 0 else 0

    if args.json:
        print(json.dumps({
            "archive": args.archive,
            "archive_size": archive_size,
            "total_content_size": total_size,
            "compression_ratio": round(ratio, 1),
            "file_count": file_count,
            "dir_count": dir_count,
        }, indent=2))
    else:
        print(f"Archive: {args.archive}")
        print(f"Archive size:     {archive_size:,} bytes")
        print(f"Content size:     {total_size:,} bytes")
        print(f"Compression:      {ratio:.1f}%")
        print(f"Files:            {file_count}")
        print(f"Directories:      {dir_count}")


def main():
    parser = argparse.ArgumentParser(description="Tar archive toolkit.")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="List archive contents")
    p_list.add_argument("--archive", required=True, help="Archive file")
    p_list.add_argument("--json", action="store_true", help="JSON output")

    p_create = sub.add_parser("create", help="Create an archive")
    p_create.add_argument("--source", required=True, help="Source file or directory")
    p_create.add_argument("--output", help="Output archive path")
    p_create.add_argument("--format", choices=["tar", "tar.gz", "tar.bz2"], default="tar.gz", help="Format")

    p_extract = sub.add_parser("extract", help="Extract an archive")
    p_extract.add_argument("--archive", required=True, help="Archive file")
    p_extract.add_argument("--output", help="Output directory (default: current)")

    p_info = sub.add_parser("info", help="Show archive info")
    p_info.add_argument("--archive", required=True, help="Archive file")
    p_info.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "list":
        cmd_list(args)
    elif args.command == "create":
        cmd_create(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "info":
        cmd_info(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
