#!/usr/bin/env python3
"""Generate a Markdown changelog from Conventional Commit history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date


PATTERN = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<desc>.+)$")
SECTIONS = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "refactor": "Refactoring",
    "docs": "Documentation",
    "test": "Tests",
    "build": "Build System",
    "ci": "CI",
    "revert": "Reverts",
    "chore": "Maintenance",
}
ORDER = ["Features", "Bug Fixes", "Performance", "Refactoring", "Documentation", "Tests", "Build System", "CI", "Reverts", "Maintenance", "Other Changes"]


def git_log(revision_range: str | None) -> list[tuple[str, str]]:
    command = ["git", "log", "--format=%H%x1f%s"]
    if revision_range:
        command.append(revision_range)
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git log failed")
    commits = []
    for line in result.stdout.splitlines():
        sha, subject = line.split("\x1f", 1)
        commits.append((sha, subject))
    return commits


def parse(subject: str) -> tuple[str, str, str | None, bool]:
    match = PATTERN.match(subject)
    if not match:
        return "Other Changes", subject, None, False
    kind = match.group("type")
    section = SECTIONS.get(kind, "Other Changes")
    return section, match.group("desc"), match.group("scope"), bool(match.group("breaking"))


def render(commits: list[tuple[str, str]], version: str, release_date: str, include_hash: bool) -> str:
    grouped: dict[str, list[str]] = defaultdict(list)
    breaking: list[str] = []

    for sha, subject in commits:
        section, desc, scope, is_breaking = parse(subject)
        prefix = f"**{scope}:** " if scope else ""
        suffix = f" ({sha[:7]})" if include_hash else ""
        item = f"- {prefix}{desc}{suffix}"
        grouped[section].append(item)
        if is_breaking:
            breaking.append(item)

    title = f"## [{version}] - {release_date}" if version else f"## Unreleased - {release_date}"
    output = [title]
    if not commits:
        output.extend(["", "No changes."])
        return "\n".join(output) + "\n"

    if breaking:
        output.extend(["", "### Breaking Changes", *breaking])
    for section in ORDER:
        items = grouped.get(section)
        if items:
            output.extend(["", f"### {section}", *items])
    return "\n".join(output) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Markdown changelog from Conventional Commit history.")
    parser.add_argument("--range", dest="revision_range", help="Git revision range, e.g. v1.0.0..HEAD")
    parser.add_argument("--version", help="Release version, e.g. 1.2.0")
    parser.add_argument("--date", default=date.today().isoformat(), help="Release date YYYY-MM-DD")
    parser.add_argument("--include-hash", action="store_true", help="Append short commit hashes")
    parser.add_argument("--output", "-o", help="Write changelog to a file instead of stdout")
    args = parser.parse_args()

    try:
        commits = git_log(args.revision_range)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

    content = render(commits, args.version or "", args.date, args.include_hash)
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        print(f"Wrote {args.output}")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
