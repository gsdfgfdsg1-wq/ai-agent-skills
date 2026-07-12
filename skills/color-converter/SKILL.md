---
name: color-converter
description: Convert between HEX, RGB, and HSL color formats with validation and preview without external dependencies.
license: MIT
---

# color-converter

A zero-dependency color format converter. Supports HEX, RGB, and HSL with full validation, automatic format detection, and JSON output.

## When to Use

- You need to convert a HEX color to RGB or HSL values (e.g., when translating CSS between formats).
- You have RGB values from a design tool and need the HEX code for web use.
- You want to auto-detect a color string's format and get all other representations at once.
- You need validated, script-friendly color output (JSON mode) for automation or piping.
- You are building a style guide or theme system and need consistent color format conversions.

## Capabilities

- **6 directional conversions**: hex2rgb, hex2hsl, rgb2hex, rgb2hsl, hsl2hex, hsl2rgb
- **Auto-detect conversion**: `convert` subcommand detects input format and outputs all other formats
- **JSON output**: `--json` flag for machine-readable output
- **Input validation**: range checks for RGB (0-255), HSL (H: 0-360, S/L: 0-100), and HEX format
- **Error handling**: clear error messages for invalid format, out-of-range values, and missing arguments
- **No external dependencies**: uses only Python stdlib (argparse, json, sys, re)

## Usage

```bash
# Convert HEX to RGB
python scripts/color_converter.py hex2rgb -s '#FF5733'

# Convert HEX to HSL
python scripts/color_converter.py hex2hsl -s '#FF5733'

# Convert RGB to HEX
python scripts/color_converter.py rgb2hex -r 255 -g 87 -b 51

# Convert RGB to HSL
python scripts/color_converter.py rgb2hsl -r 255 -g 87 -b 51

# Convert HSL to HEX
python scripts/color_converter.py hsl2hex -h 11 -s 100 -l 60

# Convert HSL to RGB
python scripts/color_converter.py hsl2rgb -h 11 -s 100 -l 60

# Auto-detect format and convert to all others
python scripts/color_converter.py convert -s '#FF5733'
python scripts/color_converter.py convert -s 'rgb(255, 87, 51)'
python scripts/color_converter.py convert -s 'hsl(11, 100%, 60%)'

# JSON output
python scripts/color_converter.py convert -s '#FF5733' --json
```

## Examples

### Example 1: HEX to RGB

```bash
$ python scripts/color_converter.py hex2rgb -s '#FF5733'
RGB: 255, 87, 51
```

### Example 2: RGB to HSL with JSON

```bash
$ python scripts/color_converter.py rgb2hsl -r 255 -g 87 -b 51 --json
{"hsl": [11, 100, 60]}
```

### Example 3: Auto-detect and convert

```bash
$ python scripts/color_converter.py convert -s 'rgb(255, 87, 51)'
Detected format: RGB
HEX: #FF5733
HSL: 11, 100%, 60%
```

### Example 4: Validation error

```bash
$ python scripts/color_converter.py rgb2hex -r 300 -g 87 -b 51
Error: Red value 300 is out of range (0-255).
```

## Reference

### Subcommands

| Subcommand  | Input                   | Output |
|-------------|-------------------------|--------|
| `hex2rgb`   | `-s '#RRGGBB'`          | RGB    |
| `hex2hsl`   | `-s '#RRGGBB'`          | HSL    |
| `rgb2hex`   | `-r R -g G -b B`        | HEX    |
| `rgb2hsl`   | `-r R -g G -b B`        | HSL    |
| `hsl2hex`   | `-h H -s S -l L`        | HEX    |
| `hsl2rgb`   | `-h H -s S -l L`        | RGB    |
| `convert`   | `-s VALUE`              | All    |

### Global Flags

| Flag      | Description                |
|-----------|----------------------------|
| `--json`  | Output in JSON format      |
| `--help`  | Show help message          |

### Validation Rules

- **HEX**: must match `#RRGGBB` or `RRGGBB` (6 hex digits)
- **RGB**: each channel must be 0-255
- **HSL**: H must be 0-360, S and L must be 0-100
