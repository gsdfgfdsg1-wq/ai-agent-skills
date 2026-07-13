---
name: escape-toolkit
description: Escape and unescape strings for C, Python, HTML, JavaScript, and JSON contexts without external dependencies.
license: MIT
---

# Escape Toolkit

> Escape and unescape strings across multiple programming language contexts — C, Python, HTML, JavaScript, and JSON.

## When to Use / Triggers

- Need to embed text in source code strings safely.
- Convert raw text to HTML-safe or URL-safe format.
- Unescape escaped strings back to original form.
- Compare escape rules across languages.

## Capabilities

- `escape`: escape a string for a target context.
- `unescape`: unescape a string from a source context.
- Supports contexts: `c`, `python`, `html`, `js`, `json`.
- `--json` machine-readable output.

## Usage

```bash
python skills/escape-toolkit/scripts/escape_tool.py escape --text 'Hello "world"' --context json
python skills/escape-toolkit/scripts/escape_tool.py unescape --text 'Hello &amp; world' --context html
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/escape_tool.py --help` for all options.
