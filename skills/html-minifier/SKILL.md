---
name: html-minifier
description: Minify HTML by removing comments, collapsing whitespace, stripping optional tags, and eliminating redundant attributes — no external dependencies.
license: MIT
---

# HTML Minifier

> Reduce HTML file size by stripping comments, collapsing whitespace, removing optional tags, and more.

## When to Use / Triggers

- Before deployment, minify static HTML to reduce payload.
- Build pipeline step for static site generators.
- Performance optimization, measure size reduction from minification.
- Compare minified vs original for critical rendering path analysis.

## Capabilities

- Removes HTML comments (optionally preserves conditional/IE comments).
- Collapses whitespace between tags.
- Strips optional closing tags (p, li, etc.).
- Removes empty attributes (e.g., `style=""`).
- Removes attribute quotes where safe.
- `--stats` to show size reduction.
- Reads from file or stdin, writes to file or stdout.

## Usage

```bash
# Minify to stdout
python skills/html-minifier/scripts/minify_html.py index.html

# Write to file
python skills/html-minifier/scripts/minify_html.py index.html -o index.min.html

# Show stats
python skills/html-minifier/scripts/minify_html.py index.html --stats

# From stdin
cat index.html | python skills/html-minifier/scripts/minify_html.py -
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/minify_html.py --help` for all options.
