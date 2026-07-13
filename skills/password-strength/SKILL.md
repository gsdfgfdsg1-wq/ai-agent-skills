---
name: password-strength
description: Analyze password strength with entropy calculation, pattern detection, and scoring without external dependencies.
license: MIT
---

# Password Strength Analyzer

> Analyze password strength by calculating Shannon entropy, detecting common patterns, and producing a composite score with improvement suggestions.

## When to Use / Triggers

- Validate password strength during user registration.
- Audit password policies and compliance.
- Generate strength reports for security reviews.

## Capabilities

- `analyze`: full strength analysis with entropy, patterns, and score.
- `score`: quick 0-100 score only.
- Detects: common passwords, sequential chars, repeated chars, keyboard walks, date patterns.
- `--json` machine-readable output.

## Usage

```bash
python skills/password-strength/scripts/pw_strength.py analyze --password "MyP@ss123!"
python skills/password-strength/scripts/pw_strength.py score --password "abc123"
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/pw_strength.py --help` for all options.
