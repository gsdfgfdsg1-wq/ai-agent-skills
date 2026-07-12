# Usage

Lint a published release note with `Added` and `Fixed` sections:

```bash
python scripts/release_note_linter.py RELEASE_NOTES.md \
  --mode released \
  --required-section Added \
  --required-section Fixed \
  --json
```

A passing document begins with a release title such as:

```markdown
## [v1.4.0] - 2026-07-13

## Added

- Add export support for #42.

## Fixed

- Correct empty response handling for #57.
```

For a pending entry, use `--mode unreleased` and the title `## [Unreleased]`. Use `#123` for issue references. The linter reports `GH-123`, `issue 123`, `#0`, and `text#123` as `issue_reference_style`; fenced code is ignored.

JSON output has `valid`, `error_count`, and `errors`. In CI, exit code `0` passes, `1` denotes lint violations, and `2` denotes invalid arguments or unreadable input.
