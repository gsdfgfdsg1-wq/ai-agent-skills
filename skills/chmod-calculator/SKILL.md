---
name: chmod-calculator
description: Convert Unix file permissions between symbolic and octal notation with detailed breakdowns without external dependencies.
license: MIT
---

# Chmod Calculator

> Convert Unix file permissions between symbolic (rwxr-xr-x) and octal (755) notation with detailed breakdowns of user/group/other permissions.

## When to Use / Triggers

- Convert between octal and symbolic permission notations.
- Understand what a permission value means.
- Calculate combined permissions.
- Verify or design file permission settings.

## Capabilities

- `octal2symbolic`: convert octal (755) to symbolic (rwxr-xr-x).
- `symbolic2octal`: convert symbolic to octal.
- `explain`: explain each permission bit.
- `combine`: combine multiple symbolic changes (e.g., u+x,g-w).
- `--json` machine-readable output.

## Usage

```bash
python skills/chmod-calculator/scripts/chmod_calc.py octal2symbolic --mode 755
python skills/chmod-calculator/scripts/chmod_calc.py symbolic2octal --mode rwxr-xr-x
python skills/chmod-calculator/scripts/chmod_calc.py explain --mode 644
python skills/chmod-calculator/scripts/chmod_calc.py combine --base 644 --changes u+x,g-w
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/chmod_calc.py --help` for all options.
