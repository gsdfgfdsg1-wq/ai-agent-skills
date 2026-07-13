---
name: slug-generator
description: Generate URL-safe slugs from text with transliteration, custom separators, and case control without external dependencies.
license: MIT
---

# Slug Generator

> Generate URL-safe slugs from text — handles Unicode transliteration, custom separators, max length, and case control.

## When to Use / Triggers

- Generate URL slugs from blog post titles.
- Create filename-safe identifiers from user input.
- Normalize text for use in URLs or file paths.

## Capabilities

- `generate`: create a slug from input text.
- `batch`: generate slugs for multiple strings from a file.
- Unicode-aware basic transliteration.
- Custom separator, max length, case control.
- `--json` machine-readable output.

## Usage

```bash
python skills/slug-generator/scripts/slug_gen.py generate --text "Hello, World! 2024"
python skills/slug-generator/scripts/slug_gen.py generate --text "中文标题" --separator "_"
python skills/slug-generator/scripts/slug_gen.py batch --file titles.txt
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/slug_gen.py --help` for all options.
