#!/usr/bin/env python3
"""Lint docker-compose YAML files for best practices and common issues."""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_yaml_simple(filepath):
    """Minimal YAML parser for docker-compose structure. Returns nested dicts/lists."""
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    # Use Python's built-in yaml if available, otherwise minimal parser
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        pass

    # Minimal fallback — not a full YAML parser but handles typical compose files
    return _minimal_yaml_parse(text)


def _minimal_yaml_parse(text):
    """Very minimal YAML parser for simple compose files."""
    result = {}
    current_path = []
    indent_stack = [0]

    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        content = stripped.strip()

        if content.endswith(":"):
            key = content[:-1].strip()
            while indent_stack and indent <= indent_stack[-1]:
                indent_stack.pop()
                if current_path:
                    current_path.pop()
            current_path.append(key)
            indent_stack.append(indent)

            # Set nested dict
            d = result
            for k in current_path[:-1]:
                if k not in d:
                    d[k] = {}
                d = d[k]
            if current_path[-1] not in d:
                d[current_path[-1]] = {}
        elif ":" in content:
            key, _, val = content.partition(":")
            key = key.strip()
            val = val.strip()

            while indent_stack and indent <= indent_stack[-1]:
                indent_stack.pop()
                if current_path:
                    current_path.pop()

            d = result
            for k in current_path:
                if k not in d:
                    d[k] = {}
                d = d[k]
            # Try to parse value types
            if val.startswith('"') and val.endswith('"'):
                d[key] = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                d[key] = val[1:-1]
            elif val.lower() == "true":
                d[key] = True
            elif val.lower() == "false":
                d[key] = False
            elif val.lower() == "null":
                d[key] = None
            else:
                try:
                    d[key] = int(val)
                except ValueError:
                    try:
                        d[key] = float(val)
                    except ValueError:
                        d[key] = val

    return result


def lint_compose(filepath):
    """Lint a docker-compose file and return issues."""
    data = parse_yaml_simple(filepath)
    issues = []

    services = data.get("services", {})
    if not services:
        issues.append({"severity": "error", "rule": "no-services", "message": "No services defined"})
        return issues

    for svc_name, svc in services.items():
        if not isinstance(svc, dict):
            continue

        image = svc.get("image", "")
        build = svc.get("build")

        # Check: no image or build
        if not image and not build:
            issues.append({
                "severity": "error",
                "rule": "no-image-or-build",
                "service": svc_name,
                "message": f"service '{svc_name}' has no image or build directive",
            })

        # Check: using latest tag
        if image and (":" not in image or image.endswith(":latest")):
            issues.append({
                "severity": "warning",
                "rule": "latest-tag",
                "service": svc_name,
                "message": f"service '{svc_name}' uses ':latest' tag — pin a specific version",
            })

        # Check: privileged mode
        privileged = svc.get("privileged", False)
        if privileged:
            issues.append({
                "severity": "error",
                "rule": "privileged-mode",
                "service": svc_name,
                "message": f"service '{svc_name}' runs in privileged mode",
            })

        # Check: missing restart policy
        restart = svc.get("restart")
        if not restart:
            issues.append({
                "severity": "info",
                "rule": "no-restart-policy",
                "service": svc_name,
                "message": f"service '{svc_name}' has no restart policy",
            })

        # Check: missing healthcheck for likely long-running services
        healthcheck = svc.get("healthcheck")
        if not healthcheck and image:
            db_keywords = ("postgres", "mysql", "redis", "mongo", "mariadb", "elasticsearch")
            if any(kw in str(image).lower() for kw in db_keywords):
                issues.append({
                    "severity": "warning",
                    "rule": "missing-healthcheck",
                    "service": svc_name,
                    "message": f"service '{svc_name}' is a database-like image without healthcheck",
                })

        # Check: host network mode
        network_mode = svc.get("network_mode", "")
        if network_mode == "host":
            issues.append({
                "severity": "warning",
                "rule": "host-network",
                "service": svc_name,
                "message": f"service '{svc_name}' uses host network mode",
            })

        # Check: ports exposing privileged ports (< 1024)
        ports = svc.get("ports", [])
        if isinstance(ports, list):
            for port in ports:
                port_str = str(port)
                m = re.match(r"^(\d+):", port_str)
                if m and int(m.group(1)) < 1024:
                    issues.append({
                        "severity": "info",
                        "rule": "privileged-port",
                        "service": svc_name,
                        "message": f"service '{svc_name}' exposes privileged port {port_str}",
                    })

        # Check: no volume for database-like services
        volumes = svc.get("volumes", [])
        if not volumes and image:
            if any(kw in str(image).lower() for kw in ("postgres", "mysql", "mongo", "mariadb")):
                issues.append({
                    "severity": "warning",
                    "rule": "no-volume-for-db",
                    "service": svc_name,
                    "message": f"service '{svc_name}' is a database without persistent volumes",
                })

    return issues


def cmd_lint(args):
    issues = lint_compose(args.file)

    if args.json:
        print(json.dumps({"file": str(args.file), "issues": issues}, indent=2, ensure_ascii=False))
    else:
        if not issues:
            print(f"✓ No issues found in {args.file}")
        else:
            print(f"Issues in {args.file}:")
            for issue in issues:
                sym = {"error": "✗", "warning": "⚠", "info": "ℹ"}[issue["severity"]]
                svc = f" [{issue['service']}]" if "service" in issue else ""
                print(f"  {sym}{svc} [{issue['severity']}] {issue['rule']}: {issue['message']}")
            print(f"\nTotal: {len(issues)} issue(s)")

    if any(i["severity"] == "error" for i in issues):
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lint docker-compose YAML files.")
    sub = parser.add_subparsers(dest="command")

    p_lint = sub.add_parser("lint", help="Lint a docker-compose file")
    p_lint.add_argument("--file", required=True, help="docker-compose YAML file")
    p_lint.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "lint":
        cmd_lint(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
