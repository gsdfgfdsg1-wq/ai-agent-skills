---
name: tar-toolkit
description: List, create, and extract tar archives with inspection and integrity checking without external dependencies.
license: MIT
---

# Tar Toolkit

> List, create, and extract tar/gz/bz2 archives with content inspection, size reporting, and integrity validation.

## When to Use / Triggers

- List contents of tar archives without extracting.
- Create tar/gz archives from directories.
- Extract specific files from tar archives.
- Inspect archive metadata and sizes.

## Capabilities

- `list`: list archive contents.
- `create`: create a tar/gz/bz2 archive.
- `extract`: extract an archive.
- `info`: show archive metadata and size summary.
- `--format` archive format: tar, tar.gz, tar.bz2.
- `--verbose` show detailed output.

## Usage

```bash
python skills/tar-toolkit/scripts/tar_tool.py list --archive backup.tar.gz
python skills/tar-toolkit/scripts/tar_tool.py create --source ./mydir --output archive.tar.gz
python skills/tar-toolkit/scripts/tar_tool.py extract --archive backup.tar.gz --output ./extracted
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/tar_tool.py --help` for all options.
