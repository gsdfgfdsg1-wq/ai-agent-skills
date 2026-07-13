#!/usr/bin/env python3
"""Word-level text diff with categorized additions, deletions, and changes."""

import argparse
import json
import sys
from pathlib import Path


def read_input(filepath=None, string=None):
    """Read text from file or string argument."""
    if string is not None:
        return string
    if filepath:
        try:
            return Path(filepath).read_text(encoding="utf-8")
        except (OSError, IOError) as e:
            print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
            sys.exit(1)
    return ""


def lcs_table(a, b):
    """Build LCS dynamic programming table."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def compute_diff(a, b):
    """Compute word-level diff using LCS. Returns list of (tag, word) tuples."""
    dp = lcs_table(a, b)
    result = []
    i, j = len(a), len(b)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            result.append(("equal", a[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            result.append(("add", b[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j - 1] < dp[i - 1][j]):
            result.append(("del", a[i - 1]))
            i -= 1

    result.reverse()
    return result


def merge_adjacent(diff_list):
    """Merge adjacent add/del pairs into 'change' operations."""
    result = []
    i = 0
    while i < len(diff_list):
        tag, word = diff_list[i]
        if tag == "del":
            # Look ahead for adjacent add
            del_words = [word]
            j = i + 1
            while j < len(diff_list) and diff_list[j][0] == "del":
                del_words.append(diff_list[j][1])
                j += 1
            add_words = []
            while j < len(diff_list) and diff_list[j][0] == "add":
                add_words.append(diff_list[j][1])
                j += 1
            if add_words:
                result.append(("change", del_words, add_words))
            else:
                for w in del_words:
                    result.append(("del", w))
            i = j
        elif tag == "add":
            add_words = [word]
            j = i + 1
            while j < len(diff_list) and diff_list[j][0] == "add":
                add_words.append(diff_list[j][1])
                j += 1
            for w in add_words:
                result.append(("add", w))
            i = j
        else:
            result.append(("equal", word))
            i += 1
    return result


def cmd_diff(args):
    text1 = read_input(args.file1, args.s1)
    text2 = read_input(args.file2, args.s2)

    words1 = text1.split()
    words2 = text2.split()

    raw_diff = compute_diff(words1, words2)
    merged = merge_adjacent(raw_diff)

    # Stats
    adds = sum(1 for d in merged if d[0] == "add")
    dels = sum(1 for d in merged if d[0] == "del")
    changes = sum(1 for d in merged if d[0] == "change")
    equals = sum(1 for d in merged if d[0] == "equal")

    if args.json:
        ops = []
        for d in merged:
            if d[0] == "change":
                ops.append({"op": "change", "from": d[1], "to": d[2]})
            else:
                ops.append({"op": d[0], "word": d[1]})
        result = {
            "stats": {"adds": adds, "dels": dels, "changes": changes, "equals": equals},
            "diff": ops,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Color output
        for d in merged:
            if d[0] == "equal":
                print(f"  {d[1]}", end="")
            elif d[0] == "add":
                print(f"  [+{d[1]}]", end="")
            elif d[0] == "del":
                print(f"  [-{d[1]}]", end="")
            elif d[0] == "change":
                print(f"  [{'/'.join(d[1])}→{'/'.join(d[2])}]", end="")
        print()
        print(f"\nStats: {adds} added, {dels} deleted, {changes} changed, {equals} unchanged")


def main():
    parser = argparse.ArgumentParser(description="Word-level text diff.")
    sub = parser.add_subparsers(dest="command")

    p_diff = sub.add_parser("diff", help="Compare two texts")
    p_diff.add_argument("--file1", help="First file")
    p_diff.add_argument("--file2", help="Second file")
    p_diff.add_argument("--s1", help="First string")
    p_diff.add_argument("--s2", help="Second string")
    p_diff.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "diff":
        if not args.file1 and args.s1 is None:
            print("Error: provide --file1 or --s1", file=sys.stderr)
            sys.exit(1)
        if not args.file2 and args.s2 is None:
            print("Error: provide --file2 or --s2", file=sys.stderr)
            sys.exit(1)
        cmd_diff(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
