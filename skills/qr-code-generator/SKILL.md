---
name: qr-code-generator
description: Generate SVG-format QR codes from text or URLs without external dependencies.
license: MIT
---

# QR Code Generator

> Generate QR codes in SVG format from text or URLs with configurable error correction, size, and color.

## When to Use / Triggers

- Generate QR codes for URLs, Wi-Fi credentials, contact info.
- Create QR codes for print or digital display.
- Batch-generate QR codes from a list.

## Capabilities

- `generate`: generate a QR code from text/URL.
- `batch`: generate QR codes from a file (one per line).
- `--output` output SVG file path.
- `--size` module size in pixels (default 10).
- `--level` error correction level: L, M, Q, H (default M).
- `--fg` foreground color (default #000000).
- `--bg` background color (default #FFFFFF).

## Usage

```bash
python skills/qr-code-generator/scripts/qr_gen.py generate --text "https://example.com" --output qr.svg
python skills/qr-code-generator/scripts/qr_gen.py batch --file urls.txt --output-dir ./qrcodes
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/qr_gen.py --help` for all options.
