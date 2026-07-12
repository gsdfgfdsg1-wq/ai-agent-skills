#!/usr/bin/env python3
"""terraform-plan-summarizer — parse terraform plan JSON and summarize changes.

Usage:
    python summarize_plan.py PLAN_FILE [-] [--json] [--exit-code] [--filter ACTION]

Parses terraform plan JSON output and produces a concise summary.
"""

import argparse
import json
import os
import sys


def _extract_changes(plan_data):
    """Extract resource changes from terraform plan JSON."""
    changes = plan_data.get("resource_changes", [])
    if not changes:
        # Try planned_values format
        planned = plan_data.get("planned_values", {})
        if planned:
            return [], "planned_values format not fully supported, use terraform show -json"

    results = []
    for rc in changes:
        change = rc.get("change", {})
        actions = change.get("actions", [])
        if not actions or actions == ["no-op"]:
            continue

        resource = {
            "address": rc.get("address", "unknown"),
            "type": rc.get("type", "unknown"),
            "name": rc.get("name", "unknown"),
            "provider": rc.get("provider_name", "unknown"),
            "actions": actions,
            "force_new": change.get("force_new", False),
        }

        # For updates, show what changed
        if "update" in actions:
            before = change.get("before", {}) or {}
            after = change.get("after", {}) or {}
            if isinstance(before, dict) and isinstance(after, dict):
                diff_keys = sorted(set(after.keys()) - set(before.keys()) |
                                   set(k for k in set(before.keys()) & set(after.keys())
                                       if before.get(k) != after.get(k)))
                resource["changed_fields"] = diff_keys[:10]

        results.append(resource)
    return results, None


def _group_by_action(changes):
    """Group changes by primary action."""
    groups = {"create": [], "update": [], "delete": [], "recreate": [], "other": []}
    for c in changes:
        actions = c["actions"]
        if actions == ["create"]:
            groups["create"].append(c)
        elif actions == ["delete"]:
            groups["delete"].append(c)
        elif actions == ["update"]:
            groups["update"].append(c)
        elif "delete" in actions and "create" in actions:
            groups["recreate"].append(c)
        else:
            groups["other"].append(c)
    return groups


def _type_distribution(changes):
    """Count changes by resource type."""
    type_counts = {}
    for c in changes:
        t = c["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    return dict(sorted(type_counts.items(), key=lambda x: -x[1]))


def _text_report(groups, type_dist, changes):
    """Render text summary."""
    lines = []
    total = len(changes)
    lines.append(f"Terraform Plan Summary: {total} change(s)\n")

    action_labels = {
        "create": ("will be created", "+"),
        "update": ("will be updated", "~"),
        "delete": ("will be destroyed", "-"),
        "recreate": ("will be recreated (force-new)", "!"),
        "other": ("other action", "*"),
    }

    for action, (label, icon) in action_labels.items():
        items = groups[action]
        if not items:
            continue
        lines.append(f"  {icon} {len(items)} {label}:")
        for item in items[:10]:
            force = " (force-new)" if item.get("force_new") and action == "update" else ""
            fields = ""
            if "changed_fields" in item:
                fields = f" [{', '.join(item['changed_fields'][:5])}]"
            lines.append(f"    {icon} {item['address']}{force}{fields}")
        if len(items) > 10:
            lines.append(f"    ... and {len(items) - 10} more")
        lines.append("")

    lines.append("  Resource type distribution:")
    for t, count in list(type_dist.items())[:10]:
        lines.append(f"    {t}: {count}")

    # Danger highlights
    destructive = groups["delete"] + groups["recreate"]
    force_updates = [c for c in groups["update"] if c.get("force_new")]
    if destructive or force_updates:
        lines.append("\n  WARNING: Destructive changes detected:")
        for c in destructive[:5]:
            lines.append(f"    - {c['address']}")
        for c in force_updates[:5]:
            lines.append(f"    ~ {c['address']} (force-new)")
        total_destructive = len(destructive) + len(force_updates)
        if total_destructive > 10:
            lines.append(f"    ... and {total_destructive - 10} more")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Parse terraform plan JSON and summarize changes."
    )
    ap.add_argument("file", help="terraform plan JSON file, or '-' for stdin")
    ap.add_argument("--json", action="store_true", help="output JSON summary")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit 1 if destructive changes (delete/recreate/force-new) found")
    ap.add_argument("--filter", choices=["create", "update", "delete", "recreate"],
                    help="only show changes of this action type")
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
        plan_data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON input: {e}", file=sys.stderr)
        sys.exit(2)

    changes, err = _extract_changes(plan_data)
    if err:
        print(f"Warning: {err}", file=sys.stderr)

    # Filter
    if args.filter:
        changes = [c for c in changes if args.filter in c["actions"]]

    groups = _group_by_action(changes)
    type_dist = _type_distribution(changes)

    if args.json:
        output = {
            "total": len(changes),
            "groups": {k: len(v) for k, v in groups.items()},
            "type_distribution": type_dist,
            "changes": changes,
            "has_destructive": bool(groups["delete"] or groups["recreate"] or
                                    any(c.get("force_new") for c in groups.get("update", []))),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(_text_report(groups, type_dist, changes))

    if args.exit_code:
        destructive = groups["delete"] + groups["recreate"]
        force_updates = [c for c in groups["update"] if c.get("force_new")]
        if destructive or force_updates:
            count = len(destructive) + len(force_updates)
            print(f"\nCI FAILED: {count} destructive change(s) detected.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
