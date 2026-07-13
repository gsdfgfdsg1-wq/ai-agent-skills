---
name: diff-highlight
description: Generate side-by-side and unified diffs with color-coded output and statistics without external dependencies.
license: MIT
---

# Diff Highlight

> Generate color-coded diffs between two text files with side-by-side view, unified view, and change statistics.

## When to Use / Triggers

- Compare two versions of a file visually.
- Generate highlighted diff output for code reviews.
- Show only changed lines with context.
- Get change statistics (additions, deletions, modifications).

## Capabilities

- `unified`: generate unified diff with color codes.
- `side-by-side`: generate side-by-side diff view.
- `stats`: show only change statistics.
- `--context` lines of context around changes (default 3).
- `--no-color` disable ANSI color codes.
- `--output` write to file.

## Usage

```bash
python skills/diff-highlight/scripts/diff_highlight.py unified --left old.txt --right new.txt
python skills/diff-highlight/scripts/diff_highlight.py side-by-side --left old.txt --right new.txt
python skills/diff-highlight/scripts/diff_highlight.py stats --left old.txt --right new.txt
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/diff_highlight.py --help` for all options.
