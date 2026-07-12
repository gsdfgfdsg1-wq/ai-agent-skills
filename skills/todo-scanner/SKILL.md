---
name: todo-scanner
description: Scan a codebase for TODO, FIXME, HACK, XXX and other annotation comments, grouping them by tag and file with JSON, summary, and CI exit-code support.
license: MIT
---

# TODO Scanner

> Quickly find all TODO/FIXME/HACK/XXX comments in your codebase, grouped by tag and file.

## When to Use / Triggers

- Before a release, audit outstanding TODO items the team left behind.
- In CI, enforce a zero-TODO policy on critical paths.
- Onboarding onto a new codebase, understand hot spots from FIXME/HACK density.
- Sprint planning, quantify and triage outstanding annotations.

## Capabilities

- Scans 6 default tags: TODO, FIXME, HACK, XXX, BUG, NOTE (customizable via `--tags`).
- Auto-skips binary files, `.git`, `node_modules`, `__pycache__`, etc.
- `--json` for machine-readable output; `--summary` for quick counts.
- `--exit-code` for CI integration.

## Usage

```bash
# Scan entire project
python skills/todo-scanner/scripts/scan_todos.py .

# Only FIXME and BUG
python skills/todo-scanner/scripts/scan_todos.py src/ --tags FIXME,BUG

# Summary only
python skills/todo-scanner/scripts/scan_todos.py . --summary

# CI gate
python skills/todo-scanner/scripts/scan_todos.py . --exit-code
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/scan_todos.py --help` for all options.
