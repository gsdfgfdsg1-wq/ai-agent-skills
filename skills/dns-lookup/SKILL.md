---
name: dns-lookup
description: Query DNS records (A, AAAA, CNAME, MX, TXT, NS, SOA) for a domain using the system resolver, with JSON and text output.
license: MIT
---

# DNS Lookup

> Query common DNS record types for a domain using the system resolver — no external dependencies.

## When to Use / Triggers

- Debug DNS resolution issues for your domain.
- Verify DNS changes after updating records.
- Audit MX records for email deliverability.
- Check TXT records for SPF/DKIM/DMARC configuration.
- Security review, verify NS and SOA records.

## Capabilities

- Queries A, AAAA, CNAME, MX, TXT, NS, SOA record types.
- Uses Python's built-in `socket` and `subprocess` for resolution.
- `--type` to query a specific record type or `--all` for everything.
- `--json` for machine-readable output.
- Works cross-platform (Windows/macOS/Linux).

## Usage

```bash
# All records
python skills/dns-lookup/scripts/dns_lookup.py example.com

# Specific type
python skills/dns-lookup/scripts/dns_lookup.py example.com --type MX

# JSON output
python skills/dns-lookup/scripts/dns_lookup.py example.com --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/dns_lookup.py --help` for all options.
