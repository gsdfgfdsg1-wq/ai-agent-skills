#!/usr/bin/env python3
"""Check local relative Markdown file links and heading anchors."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


INLINE_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "//")


def anchor_slug(text):
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def read_markdown(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError("cannot read Markdown file {}: {}".format(path, error))


def anchors_for(path, cache):
    if path not in cache:
        cache[path] = {anchor_slug(match.group(1)) for match in HEADING.finditer(without_fenced_code(read_markdown(path)))}
    return cache[path]


def line_number(text, offset):
    return text.count("\n", 0, offset) + 1


def without_fenced_code(text):
    lines = text.splitlines(keepends=True)
    hidden = []
    in_fence = False
    for line in lines:
        is_fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if in_fence or is_fence:
            hidden.append(re.sub(r"[^\n]", " ", line))
        else:
            hidden.append(line)
        if is_fence:
            in_fence = not in_fence
    return "".join(hidden)


def link_targets(text):
    searchable = without_fenced_code(text)
    for match in INLINE_LINK.finditer(searchable):
        yield match.group(1).strip(), match.start(1)
    for match in REFERENCE_LINK.finditer(searchable):
        yield match.group(1).strip(), match.start(1)


def is_local_target(target):
    return target and not target.startswith(EXTERNAL_PREFIXES) and not target.startswith("/")


def audit(path):
    selected = Path(path)
    if selected.is_file():
        files = [selected]
    elif selected.is_dir():
        files = sorted(item for item in selected.rglob("*.md") if item.is_file())
    else:
        raise ValueError("path is not a Markdown file or directory: {}".format(path))

    errors = []
    anchor_cache = {}
    for source in files:
        content = read_markdown(source)
        for target, offset in link_targets(content):
            if not is_local_target(target):
                continue
            target_path, separator, raw_anchor = target.partition("#")
            if target_path:
                destination = (source.parent / unquote(target_path)).resolve()
                if not destination.is_file():
                    errors.append({"file": str(source), "line": line_number(content, offset), "target": target,
                                   "reason": "target file not found"})
                    continue
                if destination.suffix.lower() != ".md":
                    continue
            else:
                destination = source.resolve()
            if separator:
                anchor = unquote(raw_anchor)
                if anchor not in anchors_for(destination, anchor_cache):
                    errors.append({"file": str(source), "line": line_number(content, offset), "target": target,
                                   "reason": "target anchor not found"})
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Markdown file or directory to check")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()

    try:
        errors = audit(args.path)
    except ValueError as error:
        result = {"valid": False, "error_count": 1, "errors": [{"reason": str(error)}]}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("error: {}".format(error), file=sys.stderr)
        return 2

    result = {"valid": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print("{}:{}: {} ({})".format(error["file"], error["line"], error["target"], error["reason"]))
    else:
        print("no broken local Markdown links")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
