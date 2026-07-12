---
name: release-note-linter
description: This skill should be used when linting Markdown release notes for version and date headings, required sections, unreleased markers, and consistent issue reference style in CI or local checks.
agent_created: true
---

# Release Note Linter

Lint one Markdown release-note document deterministically with the bundled standard-library Python script. Apply this skill to changelog entries, release PRs, and CI gates that need a compact, explicit release-note contract.

## Workflow

1. Select `--mode released` for a published release or `--mode unreleased` for a pending entry.
2. Require one or more H2 sections with repeated `--required-section` arguments.
3. Run `scripts/release_note_linter.py RELEASE_NOTES.md --mode ...`.
4. Treat exit code `0` as passing, `1` as lint violations, and `2` as invalid arguments or unreadable input.
5. Pass `--json` for one JSON result on standard output for CI processing.

## Rules

Require exactly one release title in the document. Accept a released title only in the form `## [VERSION] - YYYY-MM-DD`, where VERSION is `v` followed by dot-separated numeric components. Require an unreleased title to be exactly `## [Unreleased]` (case-insensitive). Reject an unreleased marker in released mode and reject a released version/date heading in unreleased mode.

Match required sections as H2 headings, case-insensitively, and report missing ones as `required_section`. Ignore headings and fenced code blocks while checking issue references in prose. Accept only `#123` references, with a positive integer and a word boundary after the digits. Report `GH-123`, `issue 123`, `#0`, and embedded forms such as `abc#123` as `issue_reference_style`.

See [examples/usage.md](examples/usage.md) for concrete commands and JSON output. Run `scripts/release_note_linter.py --help` for all options.

## Limits

Keep the linter focused on one release-note document. It does not compare a version to Git tags, validate calendar validity beyond `YYYY-MM-DD` shape, parse Markdown tables, or modify release notes.
