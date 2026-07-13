---
name: utf8-validator
description: Validate files for correct UTF-8 encoding and report byte-level errors without external dependencies.
license: MIT
---

# UTF-8 Validator

> Validate that files are properly UTF-8 encoded, reporting any byte-level encoding errors.

## When to Use / Triggers

- Check if a file is valid UTF-8 before processing.
- Detect encoding issues in text files.
- Validate files in CI for encoding correctness.

## Capabilities

- `validate`: check a file for UTF-8 validity.
- `--bom` check for UTF-8 BOM presence.
- `--json` machine-readable output.
- Reports byte offset and hex of invalid sequences.

## Usage

```bash
python skills/utf8-validator/scripts/utf8_validator.py validate --file data.txt
python skills/utf8-validator/scripts/utf8_validator.py validate --file *.txt --bom --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/utf8_validator.py --help` for all options.
