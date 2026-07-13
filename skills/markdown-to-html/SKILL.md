---
name: markdown-to-html
description: Convert Markdown files to standalone HTML with embedded CSS styling without external dependencies.
license: MIT
---

# Markdown to HTML

> Convert Markdown text to a self-contained HTML file with optional CSS styling, code highlighting, and table of contents generation.

## When to Use / Triggers

- Convert Markdown documentation to viewable HTML.
- Generate standalone HTML reports from Markdown.
- Create styled HTML pages from README files.

## Capabilities

- `convert`: convert a Markdown file to HTML.
- `--style` choose built-in style (github, plain, dark).
- `--toc` insert a table of contents.
- `--title` set the HTML page title.
- `--output` output file path (default: stdout).

## Usage

```bash
python skills/markdown-to-html/scripts/md2html.py convert --file README.md
python skills/markdown-to-html/scripts/md2html.py convert --file README.md --style github --toc --output readme.html
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/md2html.py --help` for all options.
