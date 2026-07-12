---
name: ssl-cert-checker
description: Check SSL/TLS certificate validity, expiration, and chain details for a domain without external dependencies.
license: MIT
---

# SSL Certificate Checker

> Connect to a domain and inspect its SSL certificate — expiration, issuer, SANs, and chain validity.

## When to Use / Triggers

- Before certificate expiration, get early warnings.
- After deploying a new cert, verify it's correctly installed.
- Periodic monitoring, check all your domains' cert status.
- Debugging, inspect SANs and issuer to troubleshoot cert mismatch.

## Capabilities

- Checks certificate expiration and warns if expiring within configurable days.
- Displays issuer, subject, SANs, and key info.
- `--warn-days` to set warning threshold for expiration.
- `--json` for machine-readable output.
- `--exit-code` for CI integration.

## Usage

```bash
# Check a domain
python skills/ssl-cert-checker/scripts/check_ssl.py example.com

# Warn if expiring within 14 days
python skills/ssl-cert-checker/scripts/check_ssl.py example.com --warn-days 14

# JSON output
python skills/ssl-cert-checker/scripts/check_ssl.py example.com --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/check_ssl.py --help` for all options.
