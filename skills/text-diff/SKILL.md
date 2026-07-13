---
name: text-diff
description: Word-level text diff with categorized additions, deletions, and changes without external dependencies.
license: MIT
---

# Text Diff

> Compare two texts word-by-word, categorizing additions, deletions, and changes.

## When to Use / Triggers

- Compare two versions of a document or config.
- Show word-level diff between text strings.
- Generate structured diff output for processing.

## Capabilities

- `diff`: compare two text inputs.
- `--file1` / `--file2` input files.
- `--s1` / `--s2` input strings (alternative to files).
- `--json` structured output with counts.
- Uses longest common subsequence (LCS) for word-level diff.

## Usage

```bash
python skills/text-diff/scripts/text_diff.py diff --file1 v1.txt --file2 v2.txt
python skills/text-diff/scripts/text_diff.py diff --s1 "hello world" --s2 "hello earth"
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/text_diff.py --help` for all options.
