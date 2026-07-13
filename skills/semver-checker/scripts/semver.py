#!/usr/bin/env python3
"""Parse, compare, and validate semantic version strings without external dependencies."""

import argparse
import json
import re
import sys


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def parse_version(version_str):
    """Parse a semver string into components."""
    m = SEMVER_RE.match(version_str.strip())
    if not m:
        return None
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    prerelease = m.group(4)
    build = m.group(5)
    return {
        "major": major, "minor": minor, "patch": patch,
        "prerelease": prerelease, "build": build,
    }


def version_tuple(v):
    """Get comparable tuple for a parsed version."""
    pre = v["prerelease"]
    if pre is None:
        # No prerelease = higher precedence
        return (v["major"], v["minor"], v["patch"], 1, "")
    else:
        # Prerelease versions have lower precedence
        parts = []
        for p in pre.split("."):
            if p.isdigit():
                parts.append((0, int(p), ""))
            else:
                parts.append((1, 0, p))
        return (v["major"], v["minor"], v["patch"], 0, tuple(parts))


def compare_versions(left, right):
    """Compare two version strings. Returns -1, 0, or 1."""
    lv = parse_version(left)
    rv = parse_version(right)
    if lv is None:
        print(f"Error: invalid semver '{left}'", file=sys.stderr)
        sys.exit(1)
    if rv is None:
        print(f"Error: invalid semver '{right}'", file=sys.stderr)
        sys.exit(1)

    lt = version_tuple(lv)
    rt = version_tuple(rv)

    if lt < rt:
        return -1
    elif lt > rt:
        return 1
    return 0


def parse_range(range_str):
    """Parse a simple semver range into constraints."""
    range_str = range_str.strip()
    constraints = []

    # Handle comma-separated ranges
    for part in range_str.split(","):
        part = part.strip()
        if not part:
            continue

        # Caret range ^X.Y.Z
        if part.startswith("^"):
            v = parse_version(part[1:])
            if v is None:
                continue
            # ^1.2.3 := >=1.2.3 <2.0.0
            # ^0.2.3 := >=0.2.3 <0.3.0
            # ^0.0.3 := >=0.0.3 <0.0.4
            if v["major"] != 0:
                constraints.append((">=", (v["major"], v["minor"], v["patch"])))
                constraints.append(("<", (v["major"] + 1, 0, 0)))
            elif v["minor"] != 0:
                constraints.append((">=", (0, v["minor"], v["patch"])))
                constraints.append(("<", (0, v["minor"] + 1, 0)))
            else:
                constraints.append((">=", (0, 0, v["patch"])))
                constraints.append(("<", (0, 0, v["patch"] + 1)))

        # Tilde range ~X.Y.Z
        elif part.startswith("~"):
            v = parse_version(part[1:])
            if v is None:
                continue
            # ~1.2.3 := >=1.2.3 <1.3.0
            constraints.append((">=", (v["major"], v["minor"], v["patch"])))
            constraints.append(("<", (v["major"], v["minor"] + 1, 0)))

        # >=X.Y.Z
        elif part.startswith(">="):
            v = parse_version(part[2:])
            if v:
                constraints.append((">=", (v["major"], v["minor"], v["patch"])))

        # <=X.Y.Z
        elif part.startswith("<="):
            v = parse_version(part[2:])
            if v:
                constraints.append(("<=", (v["major"], v["minor"], v["patch"])))

        # >X.Y.Z
        elif part.startswith(">") and not part.startswith(">="):
            v = parse_version(part[1:])
            if v:
                constraints.append((">", (v["major"], v["minor"], v["patch"])))

        # <X.Y.Z
        elif part.startswith("<") and not part.startswith("<="):
            v = parse_version(part[1:])
            if v:
                constraints.append(("<", (v["major"], v["minor"], v["patch"])))

        # Exact X.Y.Z
        else:
            v = parse_version(part)
            if v:
                constraints.append(("==", (v["major"], v["minor"], v["patch"])))

    return constraints


def check_constraint(version_tuple, op, constraint_tuple):
    """Check if a version satisfies a constraint."""
    if op == "==":
        return version_tuple == constraint_tuple
    elif op == ">=":
        return version_tuple >= constraint_tuple
    elif op == "<=":
        return version_tuple <= constraint_tuple
    elif op == ">":
        return version_tuple > constraint_tuple
    elif op == "<":
        return version_tuple < constraint_tuple
    return False


def cmd_parse(args):
    v = parse_version(args.version)
    if v is None:
        print(f"Error: '{args.version}' is not a valid semver string", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(v, indent=2))
    else:
        print(f"Version: {args.version}")
        print(f"  Major:       {v['major']}")
        print(f"  Minor:       {v['minor']}")
        print(f"  Patch:       {v['patch']}")
        print(f"  Prerelease:  {v['prerelease'] or '(none)'}")
        print(f"  Build:       {v['build'] or '(none)'}")


def cmd_compare(args):
    result = compare_versions(args.left, args.right)
    if args.json:
        relation = {1: "greater", 0: "equal", -1: "less"}[result]
        print(json.dumps({"left": args.left, "right": args.right, "result": relation}, indent=2))
    else:
        if result == 1:
            print(f"{args.left} > {args.right}")
        elif result == -1:
            print(f"{args.left} < {args.right}")
        else:
            print(f"{args.left} == {args.right}")


def cmd_satisfies(args):
    v = parse_version(args.version)
    if v is None:
        print(f"Error: invalid semver '{args.version}'", file=sys.stderr)
        sys.exit(1)

    constraints = parse_range(args.range)
    vt = (v["major"], v["minor"], v["patch"])

    # Prerelease versions only match if the range explicitly targets them
    satisfied = all(check_constraint(vt, op, ct) for op, ct in constraints)

    if args.json:
        print(json.dumps({
            "version": args.version, "range": args.range,
            "satisfied": satisfied, "constraints": len(constraints),
        }, indent=2))
    else:
        print(f"{args.version} {'satisfies' if satisfied else 'does NOT satisfy'} {args.range}")


def cmd_sort(args):
    versions = args.versions
    if args.file:
        try:
            versions = Path(args.file).read_text(encoding="utf-8").split()
        except OSError as e:
            print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

    parsed = []
    for v_str in versions:
        v = parse_version(v_str.strip())
        if v is None:
            print(f"Warning: skipping invalid semver '{v_str}'", file=sys.stderr)
            continue
        parsed.append((version_tuple(v), v_str.strip()))

    parsed.sort(key=lambda x: x[0])
    sorted_versions = [v for _, v in parsed]

    if args.json:
        print(json.dumps({"sorted": sorted_versions}, indent=2))
    else:
        for v in sorted_versions:
            print(v)


def main():
    parser = argparse.ArgumentParser(description="Parse, compare, and validate semver strings.")
    sub = parser.add_subparsers(dest="command")

    p_parse = sub.add_parser("parse", help="Parse a version string")
    p_parse.add_argument("--version", required=True, help="Version string")
    p_parse.add_argument("--json", action="store_true", help="JSON output")

    p_cmp = sub.add_parser("compare", help="Compare two versions")
    p_cmp.add_argument("--left", required=True, help="Left version")
    p_cmp.add_argument("--right", required=True, help="Right version")
    p_cmp.add_argument("--json", action="store_true", help="JSON output")

    p_sat = sub.add_parser("satisfies", help="Check if version satisfies range")
    p_sat.add_argument("--version", required=True, help="Version to check")
    p_sat.add_argument("--range", required=True, help="Range (e.g. ^1.0.0, ~2.0.0, >=1.0.0 <2.0.0)")
    p_sat.add_argument("--json", action="store_true", help="JSON output")

    p_sort = sub.add_parser("sort", help="Sort version strings")
    p_sort.add_argument("--versions", nargs="+", help="Version strings")
    p_sort.add_argument("--file", help="File with one version per line")
    p_sort.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "parse":
        cmd_parse(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "satisfies":
        cmd_satisfies(args)
    elif args.command == "sort":
        cmd_sort(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
