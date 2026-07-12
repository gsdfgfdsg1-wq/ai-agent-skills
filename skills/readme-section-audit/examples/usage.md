# Usage

Audit a README that must contain `Summary`, `Installation`, and `Usage`, with a Summary paragraph from 40 through 180 characters:

```bash
python scripts/readme_section_audit.py README.md \
  --required-section Summary \
  --required-section Installation \
  --required-section Usage \
  --summary-section Summary \
  --min-summary-length 40 \
  --max-summary-length 180 \
  --json
```

A passing JSON result is:

```json
{
  "valid": true,
  "error_count": 0,
  "errors": []
}
```

A duplicate `## Usage` heading is reported as `duplicate_heading`. A missing required heading is `required_section`. Summary limits count normalized characters: leading and trailing whitespace are removed, and consecutive whitespace becomes one space.

Use in CI by relying on the process result: `0` passes, `1` reports audit violations, and `2` reports bad arguments or unreadable input.
