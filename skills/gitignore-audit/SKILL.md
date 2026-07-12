---
name: gitignore-audit
description: This skill should be used when finding tracked Git files that match repository .gitignore rules and need cleanup review, including CI-friendly JSON output.
agent_created: true
---

# Gitignore Audit

Audit a Git working tree for files that are both tracked and ignored by the repository's effective `.gitignore` rules. Use the bundled standard-library Python script to produce deterministic findings without changing the index or working tree.

## Workflow

1. Run `python scripts/gitignore_audit.py REPOSITORY` from any location.
2. Review each finding's path and matching ignore rule before deciding whether to untrack it, remove the rule, or retain it intentionally.
3. Pass `--json` when consuming the result in CI or another program.
4. Treat exit code `0` as no tracked ignored files, `1` as findings that need review, and `2` as an invalid repository or Git execution failure.

The script lists tracked files with `git ls-files -z` and sends them to `git check-ignore --no-index -z -v --stdin`. The `--no-index` flag is required because Git otherwise suppresses tracked paths from ignore checks.

See [examples/usage.md](examples/usage.md) for commands and sample output. Run `scripts/gitignore_audit.py --help` for all options.

## Limits

Audit only Git's effective ignore rules for files currently tracked in the selected worktree. Do not use the output as an automatic cleanup command: removal from the index is a repository change and requires review.