---
name: whitespace-remover
description: Remove trailing spaces and tabs, then collapse blank lines at the end of UTF-8 text files using only Python standard library.
license: MIT
---

# whitespace-remover

Normalize text files by removing trailing spaces and tabs from each line and reducing trailing blank lines to a single final newline.

## When to Use

- A formatter or linter reports trailing whitespace.
- Generated text files contain unwanted blank lines at the end.
- You need a non-destructive normalization preview before changing a file.
- A CI check must fail when a file is not normalized.

## Capabilities

| Capability | Description |
|---|---|
| Line cleanup | Removes spaces and tabs at the end of every line. |
| Final newline normalization | Removes all trailing blank lines and leaves one final newline for non-empty content. |
| Check mode | `--check` exits with status `1` when a change is required. |
| Preview mode | `--dry-run` writes normalized content to stdout without editing files. |
| Output modes | Print to stdout, rewrite with `--in-place`, or write to `--output PATH`. |
| Zero dependencies | Uses only `argparse`, `pathlib`, and `sys`. |

## Usage

```bash
python scripts/whitespace_remover.py INPUT [--check | --dry-run | --in-place | --output PATH]
```

| Option | Description |
|---|---|
| `INPUT` | UTF-8 text file to normalize. |
| `--check` | Report whether normalization is required; returns `1` when changes are needed. |
| `--dry-run` | Print the normalized content without writing files. |
| `--in-place` | Rewrite `INPUT` only when its content changes. |
| `--output PATH` | Write normalized content to a separate file. |

Without an output option, normalized content is printed to stdout.

## Examples

Preview a change:

```bash
python scripts/whitespace_remover.py notes.txt --dry-run
```

Fail CI when cleanup is required:

```bash
python scripts/whitespace_remover.py notes.txt --check
```

Rewrite a file:

```bash
python scripts/whitespace_remover.py notes.txt --in-place
```

Write a cleaned copy:

```bash
python scripts/whitespace_remover.py notes.txt --output notes.clean.txt
```

## Reference

- Input and output are UTF-8 text.
- Only spaces and tabs at line ends are removed; indentation and internal whitespace remain unchanged.
- Empty files remain empty. Non-empty content ends with exactly one newline.
- `--check` returns `0` for normalized input and `1` when cleanup is required or the file cannot be read.
- See `examples/usage.md` for complete examples.
