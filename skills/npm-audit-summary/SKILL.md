---
name: npm-audit-summary
description: Parse npm audit JSON output and summarize vulnerabilities by severity, package, and dependency path for quick triage.
license: MIT
---

# npm Audit Summary

> Parse `npm audit --json` output and produce a concise, actionable summary grouped by severity.

## When to Use / Triggers

- After running `npm audit --json`, get a human-readable severity breakdown.
- In CI, fail the pipeline when critical or high vulnerabilities exceed a threshold.
- Sprint planning, triage which packages need urgent updates.
- Security review, quickly identify the most vulnerable dependency paths.

## Capabilities

- Parses npm audit JSON (v7+ format) from a file or stdin.
- Groups vulnerabilities by severity (critical / high / moderate / low / info).
- Lists affected packages with direct vs transitive indication.
- `--threshold` to set CI fail threshold (e.g. `high`).
- `--json` for machine-readable output.

## Usage

```bash
# Summarize an audit file
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json

# From stdin
npm audit --json | python skills/npm-audit-summary/scripts/npm_audit_summary.py -

# CI: fail on high or above
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json --threshold high

# JSON output
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/npm_audit_summary.py --help` for all options.
