---
name: base64-toolkit
description: Encode and decode Base64 strings with auto-detection, URL-safe mode, and file support without external dependencies.
license: MIT
---

# Base64 Toolkit

> Encode, decode, and inspect Base64 — with auto-detection and URL-safe support.

## When to Use / Triggers

- Decode a Base64 string found in configs, JWTs, or environment variables.
- Encode data to Base64 for API payloads or Kubernetes Secrets.
- Auto-detect whether a string is valid Base64.
- Batch encode/decode from a file.

## Capabilities

- `encode`: encode input string or file content to Base64.
- `decode`: decode Base64 string to plaintext (auto-detects URL-safe variant).
- `detect`: check if a string is valid Base64 and report encoding type.
- `--urlsafe` for URL-safe Base64 (uses `-` and `_` instead of `+` and `/`).
- `--file` to read input from a file.
- `--json` for machine-readable output.

## Usage

```bash
python skills/base64-toolkit/scripts/base64_toolkit.py encode -s 'Hello, World!'
python skills/base64-toolkit/scripts/base64_toolkit.py decode -s 'SGVsbG8sIFdvcmxkIQ=='
python skills/base64-toolkit/scripts/base64_toolkit.py detect -s 'SGVsbG8sIFdvcmxkIQ=='
python skills/base64-toolkit/scripts/base64_toolkit.py encode --file input.txt
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/base64_toolkit.py --help` for all options.
