---
name: markdown-linter
description: Check Markdown files for style issues — trailing whitespace, heading level jumps, long lines, missing EOF newline, multiple blank lines, inline HTML, and more — without external dependencies.
license: MIT
---

# Markdown Linter

> A zero-dependency Markdown linter that enforces consistent style across your documentation.

## When to Use / Triggers

- Enforce documentation style in CI pipelines.
- Before publishing docs, catch formatting issues.
- Code review: automatically flag Markdown anti-patterns.
- Maintain consistent heading hierarchy across a large docs site.

## Capabilities

- 11 rules: trailing whitespace (MD001), multiple blank lines (MD002), long lines (MD003), heading level jumps (MD005), multiple H1 (MD006), setext headings (MD007), missing heading space (MD008), inline HTML (MD009), missing EOF newline (MD010), first-line heading (MD011).
- Skips content inside fenced code blocks.
- Configurable line length with `--max-line`.
- `--json` output; `--severity` filter; `--exit-code` for CI.

## Usage

```bash
# Check all Markdown files
python skills/markdown-linter/scripts/lint_markdown.py .

# Specific file
python skills/markdown-linter/scripts/lint_markdown.py README.md

# Warnings and errors only
python skills/markdown-linter/scripts/lint_markdown.py docs/ --severity warning

# Custom line length
python skills/markdown-linter/scripts/lint_markdown.py . --max-line 100
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/lint_markdown.py --help` for all options.
