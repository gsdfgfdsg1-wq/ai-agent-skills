#!/usr/bin/env python3
"""Audit Node.js and Python dependency license metadata without network access."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_ALLOW = {"MIT", "ISC", "BSD-2-CLAUSE", "BSD-3-CLAUSE", "APACHE-2.0", "MPL-2.0", "PYTHON-2.0"}


@dataclass
class Package:
    ecosystem: str
    name: str
    version: str
    license: str
    source: str


def normalise(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    aliases = {
        "apache 2.0": "APACHE-2.0",
        "apache-2.0": "APACHE-2.0",
        "bsd": "BSD-3-CLAUSE",
        "bsd license": "BSD-3-CLAUSE",
        "mit license": "MIT",
        "python software foundation license": "PYTHON-2.0",
    }
    return aliases.get(value.lower(), value.upper())


def node_packages(root: Path) -> list[Package]:
    base = root / "node_modules"
    if not base.is_dir():
        return []
    records: list[Package] = []
    for manifest in base.glob("*/package.json"):
        if manifest.parent.name.startswith("."):
            continue
        records.extend(read_node_manifest(manifest))
    for manifest in base.glob("@*/*/package.json"):
        records.extend(read_node_manifest(manifest))
    return records


def read_node_manifest(manifest: Path) -> list[Package]:
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    license_value = data.get("license", "UNKNOWN")
    if isinstance(license_value, dict):
        license_value = license_value.get("type", "UNKNOWN")
    if not isinstance(license_value, str):
        license_value = "UNKNOWN"
    return [Package("node", str(data.get("name", manifest.parent.name)), str(data.get("version", "?")), normalise(license_value), str(manifest))]


def python_packages(root: Path) -> list[Package]:
    records: list[Package] = []
    for metadata in root.rglob("*.dist-info/METADATA"):
        try:
            text = metadata.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fields: dict[str, str] = {}
        for line in text.splitlines():
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            if key in {"Name", "Version", "License"} and key not in fields:
                fields[key] = value.strip()
        records.append(Package("python", fields.get("Name", metadata.parent.name), fields.get("Version", "?"), normalise(fields.get("License", "UNKNOWN") or "UNKNOWN"), str(metadata)))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit local Node.js and Python dependency license metadata.")
    parser.add_argument("path", nargs="?", default=".", help="Project or environment root (default: .)")
    parser.add_argument("--allow", help="Comma-separated licenses allowed in strict mode")
    parser.add_argument("--deny", help="Comma-separated licenses to flag")
    parser.add_argument("--strict", action="store_true", help="Flag licenses not present in the allow list")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--fail-on", choices=("warning", "error"), default="error", help="Minimum severity that exits 1")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"ERROR: path does not exist: {root}", file=sys.stderr)
        raise SystemExit(2)

    allowed = {normalise(x) for x in args.allow.split(",")} if args.allow else DEFAULT_ALLOW
    denied = {normalise(x) for x in args.deny.split(",")} if args.deny else set()
    packages = node_packages(root) + python_packages(root)
    findings = []

    for package in packages:
        severity = None
        reason = None
        if package.license in denied:
            severity, reason = "error", "matches deny policy"
        elif package.license == "UNKNOWN":
            severity, reason = "warning", "license metadata is missing or unrecognised"
        elif args.strict and package.license not in allowed:
            severity, reason = "error", "is outside the strict allow list"
        if severity:
            findings.append({"severity": severity, "reason": reason, **asdict(package)})

    payload = {"packages_scanned": len(packages), "findings": findings}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Scanned {len(packages)} package(s).")
        if not findings:
            print("PASS: no license-policy findings.")
        for item in findings:
            print(f"[{item['severity'].upper()}] {item['ecosystem']}:{item['name']}@{item['version']} - {item['license']}: {item['reason']}")

    rank = {"warning": 1, "error": 2}
    threshold = rank[args.fail_on]
    if any(rank[item["severity"]] >= threshold for item in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
