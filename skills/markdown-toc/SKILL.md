---
name: markdown-toc
description: Generate a table of contents from Markdown headings without external dependencies.
license: MIT
---

# Markdown TOC Generator

> Generate a table of contents (TOC) from Markdown heading structure with configurable depth and link styles.

## When to Use / Triggers

- Add a TOC to a long Markdown document.
- Extract heading structure for navigation.
- Validate heading hierarchy in documentation.

## Capabilities

- `generate`: produce a Markdown TOC from headings.
- `check`: validate heading hierarchy (no level jumps > 1).
- `--max-depth` limit heading levels included.
- `--no-links` output plain text without anchor links.
- `--json` machine-readable output.

## Usage

```bash
python skills/markdown-toc/scripts/md_toc.py generate --file README.md
python skills/markdown-toc/scripts/md_toc.py generate --file README.md --max-depth 3
python skills/markdown-toc/scripts/md_toc.py check --file README.md
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/md_toc.py --help` for all options.
