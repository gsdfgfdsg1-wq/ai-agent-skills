---
name: pip-req-extractor
description: Extract Python import statements from source files and generate requirements without external dependencies.
license: MIT
---

# Pip Requirements Extractor

> Scan Python source files for import statements and generate a requirements.txt file.

## When to Use / Triggers

- Extract third-party imports from a Python project.
- Generate an initial requirements.txt from source code.
- Audit which third-party packages a codebase depends on.

## Capabilities

- `extract`: scan Python files/directories and output third-party imports.
- `--output` write results to a file (requirements.txt format).
- `--include-stdlib` also list standard-library modules.
- `--json` for machine-readable output.
- Auto-detects stdlib vs third-party using Python's `sys.stdlib_module_names`.

## Usage

```bash
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path src/
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path main.py --output requirements.txt
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/pip_req_extractor.py --help` for all options.
