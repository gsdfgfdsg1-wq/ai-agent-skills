#!/usr/bin/env python3
"""Find tracked files that match effective Git ignore rules."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_git(repository, arguments, input_bytes=None):
    try:
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            input=input_bytes,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise ValueError("cannot run git: {}".format(error))


def audit(repository):
    root = Path(repository)
    if not root.is_dir():
        raise ValueError("repository path is not a directory: {}".format(repository))

    inside_worktree = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside_worktree.returncode != 0 or inside_worktree.stdout.strip() != b"true":
        raise ValueError("not a Git worktree: {}".format(repository))

    tracked = run_git(root, ["ls-files", "-z"])
    if tracked.returncode != 0:
        raise ValueError("git ls-files failed: {}".format(tracked.stderr.decode("utf-8", "replace").strip()))
    if not tracked.stdout:
        return []

    ignored = run_git(root, ["check-ignore", "--no-index", "-z", "-v", "--stdin"], tracked.stdout)
    if ignored.returncode not in (0, 1):
        raise ValueError("git check-ignore failed: {}".format(ignored.stderr.decode("utf-8", "replace").strip()))

    fields = ignored.stdout.split(b"\0")
    if fields and not fields[-1]:
        fields.pop()
    if len(fields) % 4:
        raise ValueError("unexpected git check-ignore output")

    findings = []
    for index in range(0, len(fields), 4):
        source, line, pattern, path = (field.decode("utf-8", "surrogateescape") for field in fields[index:index + 4])
        findings.append({"path": path, "source": source, "line": int(line), "pattern": pattern})
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", help="path to the Git worktree (default: current directory)")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()

    try:
        findings = audit(args.repository)
    except ValueError as error:
        result = {"valid": False, "finding_count": 0, "error": str(error)}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("error: {}".format(error), file=sys.stderr)
        return 2

    result = {"valid": not findings, "finding_count": len(findings), "findings": findings}
    if args.json:
        print(json.dumps(result, indent=2))
    elif findings:
        for finding in findings:
            print("{}: {}:{} ({})".format(finding["path"], finding["source"], finding["line"], finding["pattern"]))
    else:
        print("no tracked files match ignore rules")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
