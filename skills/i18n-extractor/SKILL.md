---
name: i18n-extractor
description: This skill should be used when extracting user-facing literal strings from JavaScript or TypeScript t(...) and i18n.t(...) calls into a unique JSON translation catalog.
agent_created: true
---

# I18n Extractor

Extract literal translation strings from JavaScript and TypeScript source before creating or updating a locale catalog.

## Workflow

1. Select a source file or directory containing `.js`, `.jsx`, `.ts`, or `.tsx` files.
2. Run `python scripts/extract.py TARGET`.
3. Redirect standard output to a locale JSON file when needed.
4. Review generated keys and rename them in the catalog only after updating the matching source calls.

## Commands

```bash
python scripts/extract.py src
python scripts/extract.py src/components/Button.tsx > locales/en.json
```

The extractor supports single- and double-quoted literal arguments in `t('...')` and `i18n.t('...')` calls. It ignores template literals, dynamic expressions, comments, duplicate values, and unsupported file types.

## Output Contract

Write one JSON object to standard output. Each key is a deterministic slug derived from the text; append `_2`, `_3`, and so on only when distinct strings normalize to the same key. Each value is the original decoded literal string.

## Exit Codes

- `0`: extraction completed, including no matching strings.
- `2`: invalid target path or unsupported target type.

See [examples/usage.md](examples/usage.md) for sample input and output.
