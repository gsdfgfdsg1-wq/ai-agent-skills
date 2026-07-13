---
name: hex-converter
description: Convert numbers between hexadecimal, binary, decimal, and octal formats without external dependencies.
license: MIT
---

# Hex Converter

> Convert numbers between hexadecimal, binary, decimal, and octal formats with bitwise operations support.

## When to Use / Triggers

- Convert between number bases quickly.
- Inspect binary representation of values.
- Calculate bit masks and flags.
- Debug hex/binary values in development.

## Capabilities

- `convert`: convert a number from one base to all other bases.
- `bits`: show binary bit layout with grouping.
- `mask`: compute bitwise AND/OR/XOR on two values.
- `--base` specify input base (auto-detect if omitted).
- `--json` machine-readable output.

## Usage

```bash
python skills/hex-converter/scripts/hex_convert.py convert --value 0xFF
python skills/hex-converter/scripts/hex_convert.py convert --value 255 --base 10
python skills/hex-converter/scripts/hex_convert.py bits --value 0xAB
python skills/hex-converter/scripts/hex_convert.py mask --value-a 0xFF --value-b 0x0F --op and
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/hex_convert.py --help` for all options.
