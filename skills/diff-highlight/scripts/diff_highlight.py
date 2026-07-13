#!/usr/bin/env python3
"""Generate highlighted diffs between two text files without external dependencies."""

import argparse
import difflib
import json
import sys
from pathlib import Path


class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def load_lines(filepath):
    """Load file as list of lines (keeping newlines)."""
    try:
        return Path(filepath).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    except OSError as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def colorize_unified(diff_lines, use_color=True):
    """Add color codes to unified diff output."""
    if not use_color:
        return "".join(diff_lines)

    result = []
    for line in diff_lines:
        line_str = line.rstrip("\n")
        if line.startswith("+++"):
            result.append(f"{Colors.CYAN}{Colors.BOLD}{line_str}{Colors.RESET}\n")
        elif line.startswith("---"):
            result.append(f"{Colors.CYAN}{Colors.BOLD}{line_str}{Colors.RESET}\n")
        elif line.startswith("@@"):
            result.append(f"{Colors.CYAN}{line_str}{Colors.RESET}\n")
        elif line.startswith("+"):
            result.append(f"{Colors.GREEN}{line_str}{Colors.RESET}\n")
        elif line.startswith("-"):
            result.append(f"{Colors.RED}{line_str}{Colors.RESET}\n")
        else:
            result.append(f"{line_str}\n")
    return "".join(result)


def cmd_unified(args):
    left_lines = load_lines(args.left)
    right_lines = load_lines(args.right)

    diff = list(difflib.unified_diff(
        left_lines, right_lines,
        fromfile=args.left, tofile=args.right,
        n=args.context,
    ))

    if not diff:
        print("Files are identical.")
        return

    use_color = not args.no_color
    output = colorize_unified(diff, use_color)

    if args.output:
        # Write without color codes to file
        Path(args.output).write_text("".join(diff), encoding="utf-8")
        print(f"Diff written to {args.output}")
    else:
        print(output, end="")


def cmd_side_by_side(args):
    left_lines = load_lines(args.left)
    right_lines = load_lines(args.right)

    sm = difflib.SequenceMatcher(None, left_lines, right_lines)
    width = args.width or 80
    half = (width - 3) // 2

    use_color = not args.no_color
    output_lines = []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                left = left_lines[i].rstrip("\n")[:half]
                right = right_lines[j1 + (i - i1)].rstrip("\n")[:half]
                output_lines.append(f"{left:<{half}} | {right}")
        elif tag == "replace":
            max_len = max(i2 - i1, j2 - j1)
            for k in range(max_len):
                left = left_lines[i1 + k].rstrip("\n")[:half] if i1 + k < i2 else ""
                right = right_lines[j1 + k].rstrip("\n")[:half] if j1 + k < j2 else ""
                prefix_l = "~" if left else " "
                prefix_r = "~" if right else " "
                if use_color:
                    left_c = f"{Colors.YELLOW}{left}{Colors.RESET}" if left else ""
                    right_c = f"{Colors.YELLOW}{right}{Colors.RESET}" if right else ""
                    output_lines.append(f"{prefix_l}{left_c:<{half + len(Colors.YELLOW) + len(Colors.RESET)}} | {prefix_r}{right_c}")
                else:
                    output_lines.append(f"{prefix_l}{left:<{half}} | {prefix_r}{right}")
        elif tag == "delete":
            for i in range(i1, i2):
                left = left_lines[i].rstrip("\n")[:half]
                if use_color:
                    output_lines.append(f"-{Colors.RED}{left}{Colors.RESET}")
                else:
                    output_lines.append(f"-{left}")
        elif tag == "insert":
            for j in range(j1, j2):
                right = right_lines[j].rstrip("\n")[:half]
                if use_color:
                    output_lines.append(f"{' ' * (half + 2)}| +{Colors.GREEN}{right}{Colors.RESET}")
                else:
                    output_lines.append(f"{' ' * (half + 2)}| +{right}")

    result = "\n".join(output_lines)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(result)


def cmd_stats(args):
    left_lines = load_lines(args.left)
    right_lines = load_lines(args.right)

    sm = difflib.SequenceMatcher(None, left_lines, right_lines)
    added = 0
    deleted = 0
    changed = 0

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            deleted += i2 - i1
        elif tag == "replace":
            left_count = i2 - i1
            right_count = j2 - j1
            changed += min(left_count, right_count)
            if right_count > left_count:
                added += right_count - left_count
            elif left_count > right_count:
                deleted += left_count - right_count

    total = added + deleted + changed

    if args.json:
        print(json.dumps({
            "left": args.left, "right": args.right,
            "added": added, "deleted": deleted, "changed": changed, "total_changes": total,
            "left_lines": len(left_lines), "right_lines": len(right_lines),
        }, indent=2))
    else:
        print(f"Left:  {args.left} ({len(left_lines)} lines)")
        print(f"Right: {args.right} ({len(right_lines)} lines)")
        print(f"Changes: +{added} added  -{deleted} deleted  ~{changed} modified  ({total} total)")


def main():
    parser = argparse.ArgumentParser(description="Generate highlighted diffs.")
    sub = parser.add_subparsers(dest="command")

    p_uni = sub.add_parser("unified", help="Unified diff with color")
    p_uni.add_argument("--left", required=True, help="Left (original) file")
    p_uni.add_argument("--right", required=True, help="Right (modified) file")
    p_uni.add_argument("--context", type=int, default=3, help="Context lines (default 3)")
    p_uni.add_argument("--no-color", action="store_true", help="Disable colors")
    p_uni.add_argument("--output", help="Write to file")

    p_sbs = sub.add_parser("side-by-side", help="Side-by-side diff")
    p_sbs.add_argument("--left", required=True, help="Left file")
    p_sbs.add_argument("--right", required=True, help="Right file")
    p_sbs.add_argument("--width", type=int, default=80, help="Terminal width (default 80)")
    p_sbs.add_argument("--no-color", action="store_true", help="Disable colors")
    p_sbs.add_argument("--output", help="Write to file")

    p_stats = sub.add_parser("stats", help="Change statistics")
    p_stats.add_argument("--left", required=True, help="Left file")
    p_stats.add_argument("--right", required=True, help="Right file")
    p_stats.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "unified":
        cmd_unified(args)
    elif args.command == "side-by-side":
        cmd_side_by_side(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
