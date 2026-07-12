# Color Converter — Usage Examples

## Example 1: HEX to RGB

Convert a HEX color code to its RGB representation.

```bash
$ python scripts/color_converter.py hex2rgb -s '#FF5733'
RGB: 255, 87, 51
```

Without the `#` prefix:

```bash
$ python scripts/color_converter.py hex2rgb -s 'FF5733'
RGB: 255, 87, 51
```

JSON output:

```bash
$ python scripts/color_converter.py hex2rgb -s '#FF5733' --json
{"rgb": [255, 87, 51]}
```

## Example 2: HEX to HSL

Convert a HEX color to HSL, useful for CSS `hsl()` values.

```bash
$ python scripts/color_converter.py hex2hsl -s '#00FF00'
HSL: 120, 100%, 50%
```

JSON output:

```bash
$ python scripts/color_converter.py hex2hsl -s '#00FF00' --json
{"hsl": [120, 100, 50]}
```

## Example 3: RGB to HEX

Convert RGB channel values to a HEX code, common when working with design tool exports.

```bash
$ python scripts/color_converter.py rgb2hex -r 0 -g 128 -b 255
HEX: #0080FF
```

JSON output:

```bash
$ python scripts/color_converter.py rgb2hex -r 0 -g 128 -b 255 --json
{"hex": "#0080FF"}
```

## Example 4: RGB to HSL

Convert RGB to HSL for use in CSS or design systems that prefer HSL notation.

```bash
$ python scripts/color_converter.py rgb2hsl -r 173 -g 216 -b 230
HSL: 194, 53%, 79%
```

## Example 5: HSL to HEX

Convert an HSL color to its HEX equivalent.

```bash
$ python scripts/color_converter.py hsl2hex -h 11 -s 100 -l 60
HEX: #FF5733
```

## Example 6: HSL to RGB

Convert HSL values to RGB for canvas or pixel-level operations.

```bash
$ python scripts/color_converter.py hsl2rgb -h 240 -s 100 -l 50
RGB: 0, 0, 255
```

## Example 7: Auto-Detect and Convert (HEX input)

The `convert` subcommand detects the input format automatically and outputs all other formats.

```bash
$ python scripts/color_converter.py convert -s '#FF5733'
Detected format: HEX
RGB: 255, 87, 51
HSL: 11, 100%, 60%
```

JSON output includes the detected format:

```bash
$ python scripts/color_converter.py convert -s '#FF5733' --json
{"hex": "#FF5733", "rgb": [255, 87, 51], "hsl": [11, 100, 60], "detected_format": "hex"}
```

## Example 8: Auto-Detect and Convert (RGB input)

```bash
$ python scripts/color_converter.py convert -s 'rgb(0, 128, 255)'
Detected format: RGB
HEX: #0080FF
HSL: 210, 100%, 50%
```

## Example 9: Auto-Detect and Convert (HSL input)

```bash
$ python scripts/color_converter.py convert -s 'hsl(120, 100%, 50%)'
Detected format: HSL
HEX: #00FF00
RGB: 0, 255, 0
```

## Example 10: Validation Errors

Out-of-range RGB value:

```bash
$ python scripts/color_converter.py rgb2hex -r 300 -g 87 -b 51
Error: Red value 300 is out of range (0-255).
```

Invalid HEX format:

```bash
$ python scripts/color_converter.py hex2rgb -s 'GGHHII'
Error: Invalid HEX color: #GGHHII. Expected format #RRGGBB with 6 hex digits.
```

Out-of-range HSL saturation:

```bash
$ python scripts/color_converter.py hsl2rgb -h 11 -s 150 -l 60
Error: Saturation value 150 is out of range (0-100).
```

Unrecognizable format in auto-detect:

```bash
$ python scripts/color_converter.py convert -s 'purple'
Error: Cannot detect color format for: 'purple'. Supported formats: #RRGGBB, rgb(R,G,B), hsl(H,S%,L%)
```
