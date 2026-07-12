---
name: css-unused-finder
description: Find CSS selectors in a stylesheet that are not referenced by any HTML files, helping reduce CSS bloat without external dependencies.
license: MIT
---

# CSS Unused Selector Finder

> Compare CSS selectors against HTML files to find unused rules — reduce CSS bloat.

## When to Use / Triggers

- Before release, audit CSS for unused selectors to reduce file size.
- After a refactoring, find dead CSS left behind.
- Performance optimization, measure and eliminate CSS bloat.
- Code review, identify selectors that may need cleanup.

## Capabilities

- Parses CSS files and extracts class selectors, ID selectors, and tag selectors.
- Scans HTML files for class, id, and tag usage.
- Reports selectors found in CSS but not in any HTML.
- `--json` for machine-readable output.
- `--exit-code` for CI integration.
- Handles simple compound selectors and pseudo-elements/pseudo-classes.

## Usage

```bash
# Find unused selectors
python skills/css-unused-finder/scripts/find_unused.py style.css --html src/

# Multiple CSS files
python skills/css-unused-finder/scripts/find_unused.py a.css b.css --html index.html about.html

# JSON output
python skills/css-unused-finder/scripts/find_unused.py style.css --html . --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/find_unused.py --help` for all options.
