---
name: line-counter
description: Count lines of code, blank lines, and comment lines by file extension without external dependencies.
license: MIT
---

# Line Counter

> Count total lines, code lines, blank lines, and comment lines in a directory, grouped by file extension.

## When to Use / Triggers

- Measure codebase size by file type.
- Track code-to-comment ratio for quality metrics.
- Find which file types dominate a project.
- CI gate on total lines or comment coverage.

## Capabilities

- `count`: count lines in a directory or single file, grouped by extension.
- `summary`: aggregate totals across all extensions.
- `--ext` filter to specific extensions.
- `--exclude` patterns to skip directories.
- `--json` machine-readable output.

## Usage

```bash
python skills/line-counter/scripts/line_counter.py count --path ./src
python skills/line-counter/scripts/line_counter.py count --path ./src --ext .py .js
python skills/line-counter/scripts/line_counter.py summary --path ./src
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/line_counter.py --help` for all options.
