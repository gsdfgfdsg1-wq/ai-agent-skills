---
name: semver-checker
description: Parse, compare, and validate semantic version strings with range constraint checking without external dependencies.
license: MIT
---

# Semver Checker

> Parse, compare, and validate semantic version strings (SemVer 2.0) with range constraint checking and sorting.

## When to Use / Triggers

- Validate version strings conform to SemVer 2.0.
- Compare which version is newer.
- Check if a version satisfies a range constraint (e.g., ^1.2.0, ~2.0.0).
- Sort a list of version strings.

## Capabilities

- `parse`: parse and display version components.
- `compare`: compare two version strings.
- `satisfies`: check if a version satisfies a range.
- `sort`: sort a list of version strings.
- `--json` machine-readable output.

## Usage

```bash
python skills/semver-checker/scripts/semver.py parse --version "1.2.3-alpha.1+build.123"
python skills/semver-checker/scripts/semver.py compare --left "1.2.3" --right "1.3.0"
python skills/semver-checker/scripts/semver.py satisfies --version "1.2.3" --range "^1.0.0"
python skills/semver-checker/scripts/semver.py sort --versions "1.0.0" "2.0.0" "1.5.0"
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/semver.py --help` for all options.
