# QR Code Generator — Usage Examples

## 1. Generate a QR code for a URL

```bash
python skills/qr-code-generator/scripts/qr_gen.py generate --text "https://example.com" --output qr.svg
```

```
QR code written to qr.svg
```

## 2. Generate with high error correction

```bash
python skills/qr-code-generator/scripts/qr_gen.py generate --text "Hello World" --level H --output qr.svg
```

## 3. Custom colors

```bash
python skills/qr-code-generator/scripts/qr_gen.py generate --text "Test" --fg "#1a73e8" --bg "#f8f9fa" --output qr.svg
```

## 4. Batch generate from file

```bash
python skills/qr-code-generator/scripts/qr_gen.py batch --file urls.txt --output-dir ./qrcodes
```

```
  Generated: ./qrcodes/000_https___example_com.svg
  Generated: ./qrcodes/001_https___github_com.svg
Batch complete: 2 QR code(s) in ./qrcodes
```

## Error handling

Text too long:

```bash
python skills/qr-code-generator/scripts/qr_gen.py generate --text "<very long text>"
```

```
Error: text too long for QR code (max ~271 bytes)
```
