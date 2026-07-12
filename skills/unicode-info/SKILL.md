---
name: unicode-info
description: Look up Unicode character information including name, category, codepoint, and block without external dependencies.
license: MIT
---

# unicode-info

A zero-dependency Python skill for looking up Unicode character information. Uses only the Python standard library (`unicodedata`, `argparse`, `json`, `sys`, `re`).

## When to Use

- You need to identify a Unicode character by its appearance or codepoint
- You want to find the official Unicode name, category, or block for a character
- You need to list characters within a Unicode range (e.g., a specific block)
- You want to search for characters by name pattern (e.g., find all "ARROW" characters)
- You are debugging encoding issues and need to inspect character properties
- You need machine-readable JSON output for piping into other tools

## Capabilities

- **char** — Get detailed info about one or more characters directly
- **codepoint** — Look up character info from a codepoint (U+XXXX or 0xXXXX)
- **range** — List characters within a Unicode range with optional limit
- **search** — Search Unicode characters by name pattern with optional category filter
- **Block detection** — Automatically maps codepoints to Unicode block names (Basic Latin, CJK Unified Ideographs, etc.)
- **JSON output** — All subcommands support `--json` for structured output
- **No external dependencies** — Runs with Python 3 standard library only

## Usage

```bash
python scripts/unicode_info.py <subcommand> [options]
```

### Subcommands

| Subcommand | Description |
|---|---|
| `char` | Show info for one or more characters |
| `codepoint` | Show info from a codepoint (U+XXXX or 0xXXXX) |
| `range` | List characters in a codepoint range |
| `search` | Search characters by name pattern |

### Common Options

| Option | Description |
|---|---|
| `--json` | Output in JSON format |
| `--limit N` | Limit number of results (range/search) |
| `--category CAT` | Filter by Unicode category (search) |

## Examples

```bash
# Look up a single character
python scripts/unicode_info.py char -s "A"

# Look up multiple characters
python scripts/unicode_info.py char -s "你好"

# Look up by codepoint
python scripts/unicode_info.py codepoint -s U+4E2D

# List first 10 characters in a range
python scripts/unicode_info.py range --from U+2600 --to U+26FF --limit 10

# Search for arrow characters
python scripts/unicode_info.py search -s "ARROW"

# Search with category filter
python scripts/unicode_info.py search -s "DIGIT" --category Nd
```

## Reference

- Unicode categories: Lu (Letter uppercase), Ll (Letter lowercase), Nd (Number decimal), So (Symbol other), etc.
- Unicode blocks are detected from hardcoded range mappings covering major blocks (Basic Latin through CJK Compatibility Ideographs, etc.)
- Name lookup uses Python's `unicodedata.name()` — characters without official names will raise an error
- Codepoint input accepts both `U+XXXX` and `0xXXXX` formats
