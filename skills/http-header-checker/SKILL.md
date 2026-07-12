---
name: http-header-checker
description: Check HTTP security response headers (CSP, HSTS, X-Frame-Options, etc.) for a URL and report missing or misconfigured headers.
license: MIT
---

# HTTP Header Checker

> Fetch a URL and audit its HTTP security response headers against best practices.

## When to Use / Triggers

- Before launch, verify your site sets all recommended security headers.
- After infrastructure changes, confirm headers are still present.
- Security audit, quickly identify missing X-Frame-Options, CSP, HSTS, etc.
- Compare security posture across environments (staging vs production).

## Capabilities

- Checks 10+ security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy, Permissions-Policy, etc.
- Follows redirects (configurable max).
- `--json` for machine-readable output.
- `--exit-code` for CI integration — fails if any recommended header is missing.
- `--timeout` for request timeout.

## Usage

```bash
# Check a URL
python skills/http-header-checker/scripts/check_headers.py https://example.com

# JSON output
python skills/http-header-checker/scripts/check_headers.py https://example.com --json

# CI gate
python skills/http-header-checker/scripts/check_headers.py https://example.com --exit-code
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/check_headers.py --help` for all options.
