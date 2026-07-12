---
name: bundle-size-delta
description: Compare two build directories and report file-size increases, decreases, and new/removed files with percentage deltas without external dependencies.
license: MIT
---

# Bundle Size Delta

> Compare two builds side by side — spot size regressions before they ship.

## When to Use / Triggers

- Compare current build vs previous build in CI.
- Track bundle size changes across releases.
- Alert on file size increases beyond a threshold.
- Pre-deploy quality gate for asset size.

## Capabilities

- Recursively scans two directories and matches files by relative path.
- Reports: increased, decreased, added (new in B), removed (missing from B).
- `--threshold PCT` to filter only changes above a percentage.
- `--json` for machine-readable output.
- `--sort` by delta, size, or path.
- Exit code 1 if any file exceeds threshold increase.

## Usage

```bash
python skills/bundle-size-delta/scripts/bundle_size_delta.py build-v1/ build-v2/
python skills/bundle-size-delta/scripts/bundle_size_delta.py dist-old/ dist/ --threshold 10 --json
python skills/bundle-size-delta/scripts/bundle_size_delta.py prev/ curr/ --sort delta
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/bundle_size_delta.py --help` for all options.
