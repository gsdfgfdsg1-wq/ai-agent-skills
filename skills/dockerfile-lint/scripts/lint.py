#!/usr/bin/env python3
"""A dependency-free Dockerfile best-practices linter.

It is deliberately conservative: each finding is a review prompt rather than
proof that an image is unsafe.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    line: int
    rule: str
    severity: str
    message: str


def logical_lines(text: str) -> list[tuple[int, str]]:
    """Join Dockerfile continuation lines while retaining their first line."""
    result: list[tuple[int, str]] = []
    buffer = ""
    start = 0
    for no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not buffer and (not line or line.startswith("#")):
            continue
        if not buffer:
            start = no
        buffer = f"{buffer} {line}".strip()
        if line.endswith("\\"):
            buffer = buffer[:-1].rstrip()
            continue
        result.append((start, buffer))
        buffer = ""
    if buffer:
        result.append((start, buffer))
    return result


def lint(text: str) -> list[Finding]:
    findings: list[Finding] = []
    instructions = logical_lines(text)
    has_user = False

    for line_no, instruction in instructions:
        parts = instruction.split(maxsplit=1)
        command = parts[0].upper()
        value = parts[1] if len(parts) > 1 else ""
        lower = value.lower()

        if command == "FROM":
            image = value.split(" AS ", 1)[0].split(" as ", 1)[0].strip()
            if "@sha256:" not in image and (":" not in image or image.endswith(":latest")):
                findings.append(Finding(line_no, "DL100", "warning", "Base image is unpinned. Use a version tag or digest for reproducible builds."))
            if image.endswith(":latest"):
                findings.append(Finding(line_no, "DL101", "warning", "Avoid the mutable 'latest' base image tag."))

        if command == "ADD":
            findings.append(Finding(line_no, "DL200", "review", "Prefer COPY over ADD unless tar extraction or remote URL behavior is intentional."))

        if command == "RUN":
            if re.search(r"\b(apt-get|apt)\s+install\b", lower) and "--no-install-recommends" not in lower:
                findings.append(Finding(line_no, "DL300", "review", "apt install should normally use --no-install-recommends to reduce image size."))
            if "apt-get update" in lower and "rm -rf /var/lib/apt/lists" not in lower:
                findings.append(Finding(line_no, "DL301", "review", "Clean apt lists in the same RUN instruction to avoid retaining package indexes."))
            if re.search(r"\b(curl|wget)\b.*\|\s*(sh|bash)", lower):
                findings.append(Finding(line_no, "DL302", "warning", "Downloading and executing a remote script bypasses integrity verification."))
            if "pip install" in lower and "--no-cache-dir" not in lower:
                findings.append(Finding(line_no, "DL303", "review", "Consider pip install --no-cache-dir to avoid retaining wheel caches."))

        if command in {"COPY", "ADD"}:
            if re.search(r"(^|\s)(\.\s|\.\s*$)", value) or value.strip().startswith("."):
                findings.append(Finding(line_no, "DL400", "review", "Copying the full build context may include secrets or unnecessary files. Use .dockerignore and explicit paths."))
            if any(token in lower for token in (".env", "id_rsa", "credentials", "secret")):
                findings.append(Finding(line_no, "DL401", "warning", "Potential credential file is copied into the image."))

        if command == "USER":
            has_user = True
            if lower in {"root", "0"}:
                findings.append(Finding(line_no, "DL500", "warning", "Container explicitly runs as root."))

    if not has_user:
        findings.append(Finding(0, "DL501", "review", "No USER instruction found. Add a non-root runtime user where compatible."))

    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint Dockerfiles for common best-practice issues.")
    parser.add_argument("path", nargs="?", default="Dockerfile", help="Dockerfile path (default: Dockerfile)")
    parser.add_argument("--json", action="store_true", help="Emit JSON findings")
    parser.add_argument("--fail-on", choices=("review", "warning"), help="Exit 1 at or above this severity")
    args = parser.parse_args()

    path = Path(args.path)
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)

    findings = lint(content)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    elif findings:
        for item in findings:
            at = f"line {item.line}" if item.line else "file"
            print(f"[{item.severity.upper()}] {at} {item.rule}: {item.message}")
    else:
        print("PASS: no configured Dockerfile issues found.")

    if args.fail_on:
        rank = {"review": 1, "warning": 2}
        threshold = rank[args.fail_on]
        if any(rank[item.severity] >= threshold for item in findings):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
