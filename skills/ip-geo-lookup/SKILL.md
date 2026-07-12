---
name: ip-geo-lookup
description: Look up geographic location, ISP, and ASN info for IP addresses using the free ip-api.com service with JSON and text output.
license: MIT
---

# IP Geo Lookup

> Query IP addresses for geographic location, ISP, and ASN information using the free ip-api.com API.

## When to Use / Triggers

- Analyze server access logs by geographic origin.
- Verify that your VPN or proxy is working (check your public IP).
- Investigate suspicious IPs in security logs.
- Enrich log data with geolocation for dashboards.

## Capabilities

- Single IP or batch from a file (one IP per line).
- Queries ip-api.com free tier (rate-limited to 45 req/min for HTTP).
- Returns country, region, city, lat/lon, ISP, org, and ASN.
- `--json` for machine-readable output.
- `--fields` to select specific output fields.
- Graceful error handling for invalid IPs and rate limits.

## Usage

```bash
# Single IP
python skills/ip-geo-lookup/scripts/ip_geo.py 8.8.8.8

# From file
python skills/ip-geo-lookup/scripts/ip_geo.py --file ips.txt

# JSON output
python skills/ip-geo-lookup/scripts/ip_geo.py 8.8.8.8 --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/ip_geo.py --help` for all options.
