#!/usr/bin/env python3
"""Review a pull request's changed files against practical repository checks.

This script intentionally produces review prompts, not a merge decision. It can
consume a file list from stdin or obtain it from git diff.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath


TEST_MARKERS = ("test", "tests", "spec", "__tests__")
DOC_FILES = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "docs"}
DEPENDENCY_FILES = {
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "requirements.txt", "poetry.lock", "Pipfile.lock", "go.mod", "go.sum",
    "composer.json", "composer.lock",
}
RISKY_PREFIXES = (".github/workflows/", "infra/", "deploy/", "migrations/", "scripts/")
SENSITIVE_NAMES = (".env", "credentials", "secret", "private_key", "id_rsa")


@dataclass
class Finding:
    level: str
    check: str
    message: str


def get_changed_files(base: str) -> list[str]:
    command = ["git", "diff", "--name-only", f"{base}...HEAD"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def has_test_file(files: list[str]) -> bool:
    return any(any(marker in PurePosixPath(path).parts for marker in TEST_MARKERS) for path in files)


def is_doc_file(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return path in DOC_FILES or "docs" in parts or path.lower().endswith((".md", ".mdx", ".rst"))


def review(files: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    if not files:
        return [Finding("warning", "changes", "No changed files were found.")]

    source_files = [p for p in files if p.endswith((".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".php", ".rb", ".java", ".cs"))]
    test_files = [p for p in files if any(marker in PurePosixPath(p).parts for marker in TEST_MARKERS)]
    docs = [p for p in files if is_doc_file(p)]

    findings.append(Finding("pass", "changes", f"Reviewing {len(files)} changed file(s)."))

    if source_files and not test_files:
        findings.append(Finding("warning", "tests", "Source files changed but no test file is included. Confirm test coverage or explain why it is unnecessary."))
    else:
        findings.append(Finding("pass", "tests", "Test coverage was included or no source file changed."))

    if any(path in DEPENDENCY_FILES for path in files):
        lockfiles = [p for p in files if p.endswith((".lock", ".json")) and p in DEPENDENCY_FILES]
        if lockfiles:
            findings.append(Finding("review", "dependencies", f"Dependency manifest or lockfile changed: {', '.join(lockfiles)}. Review version, license, and supply-chain impact."))

    if any(path.startswith(RISKY_PREFIXES) for path in files):
        risky = [p for p in files if p.startswith(RISKY_PREFIXES)]
        findings.append(Finding("review", "delivery", f"Deployment, workflow, migration, or script files changed: {', '.join(risky)}. Confirm rollback and least-privilege implications."))

    sensitive = [p for p in files if any(name in p.lower() for name in SENSITIVE_NAMES)]
    if sensitive:
        findings.append(Finding("warning", "secrets", f"Potentially sensitive path changed: {', '.join(sensitive)}. Verify that no credential values are present."))
    else:
        findings.append(Finding("pass", "secrets", "No obviously sensitive filenames were changed."))

    if source_files and not docs:
        findings.append(Finding("review", "documentation", "Source files changed without documentation updates. Check public API, configuration, and operator impact."))
    else:
        findings.append(Finding("pass", "documentation", "Documentation changed or no source file requires review."))

    return findings


def format_text(findings: list[Finding]) -> str:
    icons = {"pass": "PASS", "warning": "WARN", "review": "REVIEW"}
    return "\n".join(f"[{icons[item.level]}] {item.check}: {item.message}" for item in findings)


def main() -> None:
    parser = argparse.ArgumentParser(description="Review changed files against a PR checklist.")
    parser.add_argument("--base", default="main", help="Git base ref used for git diff (default: main)")
    parser.add_argument("--files", nargs="*", help="Explicit changed file paths; skips git diff")
    parser.add_argument("--stdin", action="store_true", help="Read newline-delimited paths from stdin")
    parser.add_argument("--json", action="store_true", help="Emit JSON findings")
    parser.add_argument("--fail-on-warning", action="store_true", help="Exit 1 if a warning is found")
    args = parser.parse_args()

    try:
        if args.stdin:
            files = [line.strip().replace("\\", "/") for line in sys.stdin if line.strip()]
        elif args.files is not None and args.files:
            files = [path.replace("\\", "/") for path in args.files]
        else:
            files = get_changed_files(args.base)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

    findings = review(files)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    else:
        print(format_text(findings))

    if args.fail_on_warning and any(item.level == "warning" for item in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
