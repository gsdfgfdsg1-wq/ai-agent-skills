#!/usr/bin/env python3
"""git-branch-cleaner — find merged local branches and stale remote-tracking branches.

Usage:
    python git_branch_cleaner.py [--stale-days N] [--delete] [--prune-remote] [--json] [--repo PATH]

Works inside any git repository. Uses subprocess to call git commands.
"""

import argparse
import json
import os
import subprocess
import sys


def _git(args, cwd=None):
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True, text=True, cwd=cwd, timeout=30
        )
        return result.stdout.strip(), result.returncode
    except FileNotFoundError:
        print("[ERROR] git is not available in this environment", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("[ERROR] git command timed out", file=sys.stderr)
        sys.exit(1)


def _get_default_branch(cwd=None):
    """Determine the default branch name (main or master)."""
    # Try symbolic ref first
    out, rc = _git(["symbolic-ref", "refs/remotes/origin/HEAD"], cwd=cwd)
    if rc == 0 and out:
        return out.split("/")[-1]
    # Try main then master
    out, rc = _git(["rev-parse", "--verify", "main"], cwd=cwd)
    if rc == 0:
        return "main"
    out, rc = _git(["rev-parse", "--verify", "master"], cwd=cwd)
    if rc == 0:
        return "master"
    return "main"


def _get_merged_branches(default_branch, cwd=None):
    """Get local branches merged into the default branch."""
    out, rc = _git(["branch", "--merged", default_branch], cwd=cwd)
    if rc != 0:
        return []
    branches = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        current = line.startswith("* ")
        name = line.lstrip("* ")
        if name != default_branch:
            branches.append({"name": name, "is_current": current})
    return branches


def _get_stale_remotes(stale_days, cwd=None):
    """Get remote-tracking branches whose remotes are gone."""
    out, rc = _git(["branch", "-r"], cwd=cwd)
    if rc != 0:
        return []
    remotes = []
    for line in out.splitlines():
        line = line.strip()
        if not line or " -> " in line:
            continue
        remotes.append(line)
    return remotes


def _get_stale_local_branches(stale_days, cwd=None):
    """Get local branches with no activity in the last N days."""
    out, rc = _git(["for-each-ref", "--sort=-committerdate",
                     "--format=%(refname:short) %(committerdate:iso8601)",
                     "refs/heads/"], cwd=cwd)
    if rc != 0:
        return []

    from datetime import datetime, timedelta, timezone
    cutoff = datetime.now(timezone.utc) - timedelta(days=stale_days)

    stale = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        name, date_str = parts
        try:
            # Parse ISO-ish date from git
            commit_date = datetime.fromisoformat(date_str.strip())
            if commit_date.tzinfo is None:
                commit_date = commit_date.replace(tzinfo=timezone.utc)
            if commit_date < cutoff:
                stale.append({"name": name, "last_commit": date_str.strip()})
        except (ValueError, TypeError):
            continue
    return stale


def main():
    ap = argparse.ArgumentParser(
        description="Find merged local branches and stale remote-tracking branches."
    )
    ap.add_argument("--stale-days", type=int, default=0,
                    help="find local branches with no commits in N days (0 = disabled)")
    ap.add_argument("--delete", action="store_true",
                    help="delete merged local branches (default: dry-run)")
    ap.add_argument("--prune-remote", action="store_true",
                    help="prune stale remote-tracking references (git remote prune)")
    ap.add_argument("--json", action="store_true",
                    help="output JSON results")
    ap.add_argument("--repo", default=None,
                    help="path to git repository (default: current directory)")
    args = ap.parse_args()

    cwd = args.repo or os.getcwd()

    # Verify git repo
    _, rc = _git(["rev-parse", "--git-dir"], cwd=cwd)
    if rc != 0:
        print("[ERROR] Not a git repository", file=sys.stderr)
        sys.exit(1)

    default_branch = _get_default_branch(cwd)
    merged = _get_merged_branches(default_branch, cwd=cwd)

    result = {
        "default_branch": default_branch,
        "merged_branches": merged,
        "deleted": [],
    }

    if args.stale_days > 0:
        result["stale_branches"] = _get_stale_local_branches(args.stale_days, cwd=cwd)

    # Delete merged branches if requested
    if args.delete and merged:
        for branch in merged:
            if branch["is_current"]:
                continue
            _, rc = _git(["branch", "-d", branch["name"]], cwd=cwd)
            if rc == 0:
                result["deleted"].append(branch["name"])
            else:
                print(f"[WARNING] Could not delete branch: {branch['name']}", file=sys.stderr)

    # Prune remote
    if args.prune_remote:
        _git(["remote", "prune", "origin"], cwd=cwd)
        result["pruned_remote"] = True

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Default branch: {default_branch}")

        if merged:
            print(f"\nMerged branches ({len(merged)}):")
            for b in merged:
                marker = " (current)" if b["is_current"] else ""
                print(f"  - {b['name']}{marker}")
        else:
            print("\nNo merged branches found.")

        if result.get("deleted"):
            print(f"\nDeleted branches ({len(result['deleted'])}):")
            for name in result["deleted"]:
                print(f"  - deleted: {name}")

        if args.stale_days > 0 and result.get("stale_branches"):
            print(f"\nStale branches (> {args.stale_days} days, {len(result['stale_branches'])}):")
            for b in result["stale_branches"]:
                print(f"  - {b['name']} (last: {b['last_commit']})")

        if not args.delete and merged:
            print("\n(dry-run — use --delete to actually remove branches)")


if __name__ == "__main__":
    main()
