# Usage

Run from the repository root or provide an explicit repository path:

```bash
python scripts/gitignore_audit.py .
```

A clean repository prints:

```text
no tracked files match ignore rules
```

Request CI-friendly JSON:

```bash
python scripts/gitignore_audit.py . --json
```

Example finding:

```json
{
  "valid": false,
  "finding_count": 1,
  "findings": [
    {
      "path": "build/cache.db",
      "source": ".gitignore",
      "line": 3,
      "pattern": "build/"
    }
  ]
}
```

The command exits `0` when there are no findings, `1` when tracked files match ignore rules, and `2` when the target is not a usable Git worktree or Git returns an operational error. Review each result before running a cleanup command such as `git rm --cached`.