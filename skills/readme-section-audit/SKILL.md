---
name: readme-section-audit
description: This skill should be used when checking a Markdown README for required H2 sections, duplicate headings, and a bounded summary length in CI or local validation.
agent_created: true
---

# README Section Audit

Audit a README deterministically with the bundled standard-library Python script. Apply this skill when a repository requires a consistent top-level README structure without introducing a Markdown parser dependency.

## Workflow

1. Define required H2 section names with repeated `--required-section` arguments.
2. Set `--summary-section` to the H2 whose first non-empty, non-heading paragraph must meet the summary limit.
3. Set `--min-summary-length` and/or `--max-summary-length` when a bounded summary is required.
4. Run `scripts/readme_section_audit.py README.md` locally or in CI.
5. Treat exit code `0` as passing, `1` as policy violations, and `2` as invalid arguments or unreadable input.
6. Pass `--json` for one machine-readable JSON result on standard output.

## Rules

Recognize ATX H2 headings only: lines that begin with `## `, allowing up to three leading spaces and optional closing `#` markers. Compare headings after trimming whitespace and closing markers, case-insensitively.

Report each repeated H2 heading as `duplicate_heading`. Report each configured heading not found as `required_section`. Extract the summary from the first non-empty, non-heading paragraph after `--summary-section`; normalize internal whitespace before measuring its character count. Treat a missing summary section or missing summary paragraph as an audit error when a summary length limit is configured.

See [examples/usage.md](examples/usage.md) for commands and expected JSON. Run `scripts/readme_section_audit.py --help` for all options.

## Limits

Keep the audit intentionally narrow. It does not rewrite Markdown, validate heading nesting, parse Setext headings, or evaluate links and formatting.
