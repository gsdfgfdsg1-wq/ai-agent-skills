#!/usr/bin/env python3
"""bundle-size-delta — compare two build directories and report size deltas.

Usage:
    python bundle_size_delta.py DIR_A DIR_B [--threshold PCT] [--json] [--sort FIELD] [--top N]

Reports file-size increases, decreases, added, and removed files between two directories.
"""

import argparse
import json
import os
import sys

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__"}


def _scan_dir(dirpath):
    """Recursively scan a directory and return {relative_path: size}."""
    result = {}
    if not os.path.isdir(dirpath):
        return result
    for root, dirs, files in os.walk(dirpath):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, dirpath).replace("\\", "/")
            try:
                result[rel] = os.path.getsize(fp)
            except OSError:
                pass
    return result


def compare_dirs(dir_a, dir_b, threshold_pct=0, sort_by="path", top_n=0):
    """Compare two directories and return delta report."""
    files_a = _scan_dir(dir_a)
    files_b = _scan_dir(dir_b)

    paths_a = set(files_a.keys())
    paths_b = set(files_b.keys())

    common = paths_a & paths_b
    added = sorted(paths_b - paths_a)
    removed = sorted(paths_a - paths_b)

    increased = []
    decreased = []
    unchanged = []

    for rel in sorted(common):
        size_a = files_a[rel]
        size_b = files_b[rel]
        delta = size_b - size_a
        pct = ((delta / size_a) * 100) if size_a > 0 else (100.0 if size_b > 0 else 0)

        if delta > 0:
            if pct >= threshold_pct:
                increased.append({
                    "file": rel,
                    "size_a": size_a,
                    "size_b": size_b,
                    "delta": delta,
                    "pct": round(pct, 1),
                })
        elif delta < 0:
            if abs(pct) >= threshold_pct:
                decreased.append({
                    "file": rel,
                    "size_a": size_a,
                    "size_b": size_b,
                    "delta": delta,
                    "pct": round(pct, 1),
                })
        else:
            unchanged.append({"file": rel, "size": size_a})

    # Sort
    sort_key = {
        "path": lambda x: x["file"],
        "delta": lambda x: abs(x["delta"]),
        "size": lambda x: x.get("size_b", x.get("size_a", 0)),
    }.get(sort_by, lambda x: x["file"])

    increased.sort(key=sort_key, reverse=(sort_by in ("delta", "size")))
    decreased.sort(key=sort_key, reverse=(sort_by in ("delta", "size")))

    added_entries = [{"file": f, "size_b": files_b[f]} for f in added]
    removed_entries = [{"file": f, "size_a": files_a[f]} for f in removed]

    total_a = sum(files_a.values())
    total_b = sum(files_b.values())
    total_delta = total_b - total_a
    total_pct = ((total_delta / total_a) * 100) if total_a > 0 else 0

    result = {
        "dir_a": dir_a,
        "dir_b": dir_b,
        "total_a": total_a,
        "total_b": total_b,
        "total_delta": total_delta,
        "total_pct": round(total_pct, 1),
        "increased": increased,
        "decreased": decreased,
        "added": added_entries,
        "removed": removed_entries,
        "unchanged_count": len(unchanged),
    }

    if top_n > 0:
        result["increased"] = increased[:top_n]
        result["decreased"] = decreased[:top_n]

    return result


def _human_size(n):
    """Convert bytes to human-readable size."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main():
    ap = argparse.ArgumentParser(
        description="Compare two build directories and report size deltas."
    )
    ap.add_argument("dir_a", help="first (baseline) directory")
    ap.add_argument("dir_b", help="second (current) directory")
    ap.add_argument("--threshold", type=float, default=0,
                    help="minimum percentage change to report (default: 0)")
    ap.add_argument("--json", action="store_true",
                    help="output JSON results")
    ap.add_argument("--sort", choices=["path", "delta", "size"], default="path",
                    help="sort results by field (default: path)")
    ap.add_argument("--top", type=int, default=0,
                    help="limit to top N changes per category")
    ap.add_argument("--fail-threshold", type=float, default=0,
                    help="exit 1 if any file increases by more than PCT%% (CI gate)")
    args = ap.parse_args()

    if not os.path.isdir(args.dir_a):
        print(f"[ERROR] Directory not found: {args.dir_a}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.dir_b):
        print(f"[ERROR] Directory not found: {args.dir_b}", file=sys.stderr)
        sys.exit(1)

    result = compare_dirs(args.dir_a, args.dir_b,
                          threshold_pct=args.threshold,
                          sort_by=args.sort,
                          top_n=args.top)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Comparing {args.dir_a}/ vs {args.dir_b}/")
        print(f"Total: {_human_size(result['total_a'])} -> {_human_size(result['total_b'])} "
              f"(delta: {_human_size(result['total_delta'])}, {result['total_pct']:+.1f}%)")
        print()

        if result["increased"]:
            print(f"Increased ({len(result['increased'])}):")
            for f in result["increased"]:
                print(f"  + {f['file']}: {_human_size(f['size_a'])} -> {_human_size(f['size_b'])} "
                      f"({_human_size(f['delta'])}, {f['pct']:+.1f}%)")
            print()

        if result["decreased"]:
            print(f"Decreased ({len(result['decreased'])}):")
            for f in result["decreased"]:
                print(f"  - {f['file']}: {_human_size(f['size_a'])} -> {_human_size(f['size_b'])} "
                      f"({_human_size(f['delta'])}, {f['pct']:+.1f}%)")
            print()

        if result["added"]:
            print(f"Added ({len(result['added'])}):")
            for f in result["added"]:
                print(f"  + {f['file']}: {_human_size(f['size_b'])} (new)")
            print()

        if result["removed"]:
            print(f"Removed ({len(result['removed'])}):")
            for f in result["removed"]:
                print(f"  - {f['file']}: {_human_size(f['size_a'])} (gone)")
            print()

        print(f"Unchanged: {result['unchanged_count']} file(s)")

    # CI gate
    if args.fail_threshold > 0:
        violations = [f for f in result["increased"] if f["pct"] > args.fail_threshold]
        if violations:
            print(f"\nFAIL: {len(violations)} file(s) exceed {args.fail_threshold}% increase threshold",
                  file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
