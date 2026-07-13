#!/usr/bin/env python3
"""Summarize commands from Bash or Zsh history text using only the standard library."""

import argparse
import collections
import json
import re
import sys

TIMESTAMP_LINE = re.compile(r"^\s*#\d+\s*$")
ZSH_EXTENDED = re.compile(r"^\s*:\s+\d+:\d+;(.+)$")


def command_name(line):
    """Extract the executable token while tolerating common shell prefixes."""
    text = line.strip()
    if not text:
        return None
    while text.startswith(("sudo ", "command ", "env ")):
        text = text.split(None, 1)[1] if " " in text else ""
    if not text:
        return None
    return text.split(None, 1)[0]


def parse_history(lines):
    commands = []
    ignored = 0
    for raw in lines:
        line = raw.strip()
        if not line or TIMESTAMP_LINE.match(line):
            ignored += 1
            continue
        zsh_match = ZSH_EXTENDED.match(line)
        if zsh_match:
            line = zsh_match.group(1).strip()
        if not line:
            ignored += 1
            continue
        name = command_name(line)
        if name:
            commands.append(name)
        else:
            ignored += 1
    return commands, ignored


def main():
    parser = argparse.ArgumentParser(description="Analyze command frequency in Bash or Zsh history text.")
    parser.add_argument("history", nargs="?", default="-", help="history file path, or - for standard input")
    parser.add_argument("--top", type=int, default=10, help="number of commands to show (default: 10; 0 shows all)")
    parser.add_argument("--json", action="store_true", help="write structured JSON output")
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top must be zero or greater")

    try:
        if args.history == "-":
            lines = sys.stdin.read().splitlines()
            source = "stdin"
        else:
            with open(args.history, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
            source = args.history
    except OSError as error:
        parser.error(f"cannot read {args.history}: {error}")

    commands, ignored = parse_history(lines)
    counts = collections.Counter(commands)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if args.top:
        ranked = ranked[:args.top]
    entries = [{"command": command, "count": count} for command, count in ranked]
    result = {
        "source": source,
        "total_lines": len(lines),
        "ignored_lines": ignored,
        "command_lines": len(commands),
        "unique_commands": len(counts),
        "commands": entries,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"History: {source}")
        print(f"Commands: {len(commands)} total, {len(counts)} unique; {ignored} ignored")
        if entries:
            print("\nCount  Command")
            for entry in entries:
                print(f"{entry['count']:>5}  {entry['command']}")
        else:
            print("\nNo commands found.")


if __name__ == "__main__":
    main()
