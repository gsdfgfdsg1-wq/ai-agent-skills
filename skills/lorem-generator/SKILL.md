---
name: lorem-generator
description: Generate Lorem ipsum placeholder text with configurable paragraphs, sentences, and words without external dependencies.
license: MIT
---

# Lorem Ipsum Generator

> Generate Lorem ipsum placeholder text with configurable paragraphs, sentences, and word counts for design mockups and documentation.

## When to Use / Triggers

- Fill mockups with realistic placeholder text.
- Generate test content for layouts and templates.
- Create sample documents for testing.

## Capabilities

- `paragraphs`: generate N paragraphs of Lorem ipsum.
- `sentences`: generate N sentences.
- `words`: generate N words.
- `--start-with-lorem` always begin with "Lorem ipsum dolor sit amet...".
- `--json` machine-readable output.

## Usage

```bash
python skills/lorem-generator/scripts/lorem_gen.py paragraphs --count 3
python skills/lorem-generator/scripts/lorem_gen.py sentences --count 5
python skills/lorem-generator/scripts/lorem_gen.py words --count 50
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/lorem_gen.py --help` for all options.
