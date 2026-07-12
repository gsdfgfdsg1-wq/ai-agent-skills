---
name: git-branch-cleaner
description: Find merged local branches and stale remote-tracking branches for safe cleanup without external dependencies.
license: MIT
---

# Git Branch Cleaner

> Find merged and stale Git branches — prune safely before they pile up.

## When to Use / Triggers

- Clean up local branches already merged into main/master.
- Find remote-tracking branches that no longer exist on the remote.
- CI: alert when stale branches accumulate.
- Pre-release housekeeping.

## Capabilities

- Lists local branches merged into the default branch (main/master).
- Lists remote-tracking branches whose remote counterparts are gone.
- `--stale-days N` to find branches not updated in N days.
- `--delete` to actually delete merged local branches (otherwise dry-run).
- `--prune-remote` to prune stale remote-tracking references.
- `--json` for machine-readable output.

## Usage

```bash
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py --stale-days 30
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py --delete --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/git_branch_cleaner.py --help` for all options.
