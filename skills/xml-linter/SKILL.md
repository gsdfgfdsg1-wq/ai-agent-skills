---
name: xml-linter
description: Lint XML files for common issues including unclosed tags, encoding declarations, and well-formedness without external dependencies.
license: MIT
---

# XML Linter

> Check XML files for common issues — unclosed tags, encoding declarations, duplicate attributes, namespace problems, and well-formedness violations.

## When to Use / Triggers

- Validate XML configuration files before deployment.
- Check for well-formedness issues in XML documents.
- Lint SVG, XHTML, or other XML-based formats.
- CI gate on XML quality.

## Capabilities

- `lint`: check an XML file for issues.
- `check-well-formed`: verify XML well-formedness with detailed error reporting.
- Supports 8+ lint rules.
- `--json` machine-readable output.

## Usage

```bash
python skills/xml-linter/scripts/xml_lint.py lint --file config.xml
python skills/xml-linter/scripts/xml_lint.py check-well-formed --file data.xml
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/xml_lint.py --help` for all options.
