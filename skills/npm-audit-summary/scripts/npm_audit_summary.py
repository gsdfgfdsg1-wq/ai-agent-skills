#!/usr/bin/env python3
"""npm-audit-summary — parse npm audit JSON and summarize by severity.

Usage:
    python npm_audit_summary.py AUDIT_FILE [-] [--threshold LEVEL] [--json] [--top N]

Reads npm audit --json output and produces a grouped summary.
"""

import argparse
import json
import os
import sys

SEVERITY_ORDER = ["critical", "high", "moderate", "low", "info"]
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITY_ORDER)}


def _parse_audit(data):
    """Parse npm audit JSON (v7+ format) and return list of vuln dicts."""
    vulns = []

    # npm audit v7+ format: { vulnerabilities: { <pkg>: { ... } } }
    vulnerabilities = data.get("vulnerabilities", {})
    for pkg_name, info in vulnerabilities.items():
        severity = info.get("severity", "info")
        is_direct = info.get("isDirect", False)
        via = info.get("via", [])
        # via can be a list of strings (paths) or dicts (advisories)
        advisory_ids = []
        for v in via:
            if isinstance(v, dict):
                advisory_ids.append(str(v.get("url", v.get("title", ""))))
            else:
                advisory_ids.append(str(v))
        fix_available = info.get("fixAvailable", False)
        # Some fixAvailable is a dict with info
        if isinstance(fix_available, dict):
            fix_available = True

        vulns.append({
            "package": pkg_name,
            "severity": severity,
            "is_direct": is_direct,
            "via": advisory_ids[:5],  # limit
            "fix_available": bool(fix_available),
        })

    # Legacy npm audit v6 format: { advisories: { <id>: { ... } } }
    if not vulns and "advisories" in data:
        for aid, adv in data.get("advisories", {}).items():
            findings = adv.get("findings", [{}])
            for f in findings:
                for pkg in f.get("paths", []):
                    vulns.append({
                        "package": pkg.split(">")[0] if ">" in pkg else pkg,
                        "severity": adv.get("severity", "info"),
                        "is_direct": len(pkg.split(">")) <= 2,
                        "via": [adv.get("url", adv.get("title", str(aid)))],
                        "fix_available": any(
                            p.get("id") == aid
                            for p in data.get("actions", [])
                            if p.get("action") == "update" or p.get("action") == "install"
                        ),
                    })
            if not findings:
                vulns.append({
                    "package": adv.get("module_name", "unknown"),
                    "severity": adv.get("severity", "info"),
                    "is_direct": False,
                    "via": [adv.get("url", adv.get("title", str(aid)))],
                    "fix_available": False,
                })

    return vulns


def _group_by_severity(vulns):
    groups = {s: [] for s in SEVERITY_ORDER}
    for v in vulns:
        sev = v["severity"].lower()
        if sev not in groups:
            groups.setdefault("info", []).append(v)
            v["severity"] = "info"
        else:
            groups[sev].append(v)
    return groups


def _text_report(groups, top):
    lines = []
    total = sum(len(v) for v in groups.values())
    lines.append(f"npm audit summary: {total} vulnerability(ies)\n")

    for sev in SEVERITY_ORDER:
        items = groups[sev]
        if not items:
            continue
        lines.append(f"  {sev.upper()}: {len(items)}")
        shown = items[:top]
        for v in shown:
            direct = "direct" if v["is_direct"] else "transitive"
            fix = " [fix available]" if v["fix_available"] else ""
            lines.append(f"    - {v['package']} ({direct}){fix}")
        if len(items) > top:
            lines.append(f"    ... and {len(items) - top} more")
        lines.append("")

    fixable = sum(1 for v in sum(groups.values(), []) if v["fix_available"])
    if fixable:
        lines.append(f"  {fixable} of {total} have fixes available.")
    else:
        lines.append("  No automatic fixes available.")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Parse npm audit JSON and summarize vulnerabilities by severity."
    )
    ap.add_argument("file", help="npm audit JSON file, or '-' for stdin")
    ap.add_argument(
        "--threshold",
        choices=SEVERITY_ORDER,
        help="CI threshold: exit 1 if any vulnerability at or above this severity"
    )
    ap.add_argument("--json", action="store_true", help="output JSON summary")
    ap.add_argument("--top", type=int, default=5, help="show top N packages per severity (default: 5)")
    args = ap.parse_args()

    if args.file == "-":
        raw = sys.stdin.read()
    else:
        if not os.path.isfile(args.file):
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON input: {e}", file=sys.stderr)
        sys.exit(2)

    vulns = _parse_audit(data)
    groups = _group_by_severity(vulns)

    if args.json:
        summary = {
            "total": len(vulns),
            "by_severity": {s: len(groups[s]) for s in SEVERITY_ORDER},
            "fixable": sum(1 for v in vulns if v["fix_available"]),
            "vulnerabilities": vulns,
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(_text_report(groups, args.top))

    # CI threshold check
    if args.threshold:
        threshold_rank = SEVERITY_RANK[args.threshold]
        failing = [v for v in vulns if SEVERITY_RANK.get(v["severity"], 99) <= threshold_rank]
        if failing:
            print(f"\nCI FAILED: {len(failing)} vulnerability(ies) at or above '{args.threshold}' threshold.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"\nCI PASSED: no vulnerabilities at or above '{args.threshold}' threshold.")
            sys.exit(0)


if __name__ == "__main__":
    main()
