#!/usr/bin/env python3
"""Extract literal i18n strings from JavaScript and TypeScript source."""

import argparse
import ast
import json
import re
import sys
from pathlib import Path

SOURCE_SUFFIXES = {".js", ".jsx", ".ts", ".tsx"}
CALL_PATTERN = re.compile(
    r"(?<![\w$.])(?:i18n\s*\.\s*)?t\s*\(\s*"
    r"(?P<quote>['\"])(?P<value>(?:\\.|(?!\1).)*)\1",
    re.DOTALL,
)
COMMENT_PATTERN = re.compile(
    r"//[^\r\n]*|/\*[\s\S]*?\*/",
)


def strip_comments(source: str) -> str:
    """Replace comments with spaces while preserving quoted content."""
    result = []
    index = 0
    quote = None
    while index < len(source):
        char = source[index]
        if quote:
            result.append(char)
            if char == "\\" and index + 1 < len(source):
                result.append(source[index + 1])
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in "'\"`":
            quote = char
            result.append(char)
            index += 1
            continue
        if source.startswith("//", index):
            end = source.find("\n", index)
            if end == -1:
                result.append(" " * (len(source) - index))
                break
            result.append(" " * (end - index))
            index = end
            continue
        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            end = len(source) if end == -1 else end + 2
            result.append("".join("\n" if char == "\n" else " " for char in source[index:end]))
            index = end
            continue
        result.append(char)
        index += 1
    return "".join(result)


def decode_literal(quote: str, value: str) -> str:
    """Decode a JavaScript-style quoted literal using Python's parser."""
    try:
        return ast.literal_eval(quote + value + quote)
    except (SyntaxError, ValueError):
        return value


def iter_source_files(target: Path):
    if target.is_file():
        if target.suffix.lower() not in SOURCE_SUFFIXES:
            raise ValueError(f"unsupported source file: {target}")
        yield target
        return
    if target.is_dir():
        yield from sorted(
            (path for path in target.rglob("*") if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES),
            key=lambda path: path.as_posix(),
        )
        return
    raise ValueError(f"target does not exist: {target}")


def key_for(value: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return key or "translation"


def extract(target: Path) -> dict[str, str]:
    values = set()
    for path in iter_source_files(target):
        source = strip_comments(path.read_text(encoding="utf-8"))
        for match in CALL_PATTERN.finditer(source):
            values.add(decode_literal(match.group("quote"), match.group("value")))

    catalog = {}
    for value in sorted(values):
        base_key = key_for(value)
        key = base_key
        suffix = 2
        while key in catalog:
            key = f"{base_key}_{suffix}"
            suffix += 1
        catalog[key] = value
    return catalog


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract literal strings from t(...) and i18n.t(...) calls as JSON."
    )
    parser.add_argument("target", type=Path, help="JavaScript/TypeScript file or directory to scan")
    args = parser.parse_args()

    try:
        catalog = extract(args.target)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    json.dump(catalog, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
