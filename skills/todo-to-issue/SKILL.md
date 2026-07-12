---
name: todo-to-issue
description: Scan source code for TODO/FIXME/HACK comments and convert them to GitHub Issue format with labels, assignees, and file references without external dependencies.
license: MIT
---

# TODO to Issue

> Turn code TODOs into actionable GitHub Issues — right from the terminal.

## When to Use / Triggers

- Generate GitHub Issues from code annotations before a release.
- Track technical debt by converting TODO/FIXME comments to issues.
- CI: alert when new TODOs are introduced.
- Sprint planning: enumerate all pending code annotations.

## Capabilities

- Scans for TODO, FIXME, HACK, XXX, BUG, NOTE comments.
- Generates Markdown in GitHub Issue format (title, body with file link, labels).
- Infers label from annotation type (todo → enhancement, fixme → bug, hack → technical debt).
- `--assignee` to set default assignee.
- `--json` for machine-readable output.
- Supports multiple file extensions (py, js, ts, go, java, rb, sh, etc.).

## Usage

```bash
python skills/todo-to-issue/scripts/todo_to_issue.py src/
python skills/todo-to-issue/scripts/todo_to_issue.py . --assignee octocat --json
python skills/todo-to-issue/scripts/todo_to_issue.py src/ --tags TODO,FIXME
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/todo_to_issue.py --help` for all options.
