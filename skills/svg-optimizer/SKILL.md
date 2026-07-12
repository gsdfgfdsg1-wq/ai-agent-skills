---
name: svg-optimizer
description: Remove bloat from SVG files — strip comments, metadata, editor namespaces, default attributes, and excess whitespace to produce smaller SVGs without external dependencies.
license: MIT
---

# SVG Optimizer

> Shrink your SVGs by stripping editor bloat — no Node.js or svgo required.

## When to Use / Triggers

- Optimize SVG assets before deploying to production.
- CI: enforce SVG size budgets.
- Remove Inkscape/Illustrator metadata from designer handoffs.
- Batch-optimize an icon library.

## Capabilities

- Removes: XML comments, editor metadata (Inkscape, Sodipodi), editor namespace declarations, default attribute values, XML declarations, DOCTYPE.
- `--aggressive` mode: also removes empty groups, `<title>`, and `<desc>`.
- `--in-place` to overwrite; `--output` for a separate directory.
- `--json` for machine-readable size stats.
- Reports before/after sizes and savings percentage.

## Usage

```bash
# Check savings (no write)
python skills/svg-optimizer/scripts/optimize_svg.py icons/

# Write optimized files to output dir
python skills/svg-optimizer/scripts/optimize_svg.py icons/ -o dist/icons/

# In-place optimization
python skills/svg-optimizer/scripts/optimize_svg.py logo.svg --in-place

# Aggressive mode
python skills/svg-optimizer/scripts/optimize_svg.py . --aggressive --in-place
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/optimize_svg.py --help` for all options.
