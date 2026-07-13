---
name: port-service-lookup
description: Look up common TCP and UDP port-to-service mappings from an offline built-in table, with protocol filtering and JSON output. This skill should be used when identifying standard service ports without querying a network.
license: MIT
agent_created: true
---

# Port Service Lookup

Look up common TCP and UDP service mappings with the bundled standard-library CLI. Search by numeric port or service name, filter by protocol, and emit text or JSON without making network requests.

## When to Use / Triggers

- Identify a likely standard service for a known port.
- Find common ports assigned to a service name.
- Produce an offline port-service reference for scripts or incident triage.
- Filter a lookup to TCP or UDP mappings.

## Usage

```bash
python skills/port-service-lookup/scripts/port_service_lookup.py 443
python skills/port-service-lookup/scripts/port_service_lookup.py dns --protocol udp
python skills/port-service-lookup/scripts/port_service_lookup.py 53 --json
```

## Output

- Search an embedded table of common well-known and registered service ports.
- Match ports exactly when the query is numeric.
- Match service names case-insensitively when the query is text.
- Restrict results with `--protocol tcp` or `--protocol udp`.
- Return exit status `1` when no mapping matches.

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/port_service_lookup.py --help` for all options.
