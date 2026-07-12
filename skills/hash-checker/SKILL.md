---
name: hash-checker
description: Compute and verify file hashes (MD5/SHA1/SHA256/SHA512) without external dependencies.
license: MIT
---

# Hash Checker

> Compute, verify, and inspect file and text hashes — MD5, SHA-1, SHA-256, SHA-512.

## When to Use / Triggers

- Compute the hash of a file or string.
- Verify a downloaded file against a known checksum.
- Batch hash computation from a file.

## Capabilities

- `compute`: compute hash of a file.
- `verify`: verify a file against a known hash.
- `text`: compute hash of a text string.
- `--algorithm` to choose md5, sha1, sha256 (default), or sha512.
- `--json` for machine-readable output.

## Usage

```bash
python skills/hash-checker/scripts/hash_checker.py compute --file example.txt
python skills/hash-checker/scripts/hash_checker.py verify --file example.txt --hash abc123...
python skills/hash-checker/scripts/hash_checker.py text -s 'Hello, World!'
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/hash_checker.py --help` for all options.
