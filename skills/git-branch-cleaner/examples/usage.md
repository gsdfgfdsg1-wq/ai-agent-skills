# Usage Examples

## 1. Dry run — list merged branches

```bash
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py
```

Output:

```text
Default branch: main

Merged branches (2):
  - feature/login
  - fix/header-bug

(dry-run — use --delete to actually remove branches)
```

## 2. Delete merged branches

```bash
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py --delete
```

Deletes all local branches that have been merged into the default branch.

## 3. Find stale branches

```bash
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py --stale-days 30
```

Lists local branches with no commits in the last 30 days.

## 4. JSON output

```bash
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py --json
```

Returns JSON with default_branch, merged_branches, and optionally stale_branches.

## 5. Prune stale remote-tracking references

```bash
python skills/git-branch-cleaner/scripts/git_branch_cleaner.py --prune-remote
```

Runs `git remote prune origin` to clean up remote-tracking branches whose remotes are gone.
