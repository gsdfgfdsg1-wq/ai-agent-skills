---
name: hosts-file-parser
description: Parse and validate hosts files, collecting IP-to-alias mappings while identifying duplicate mappings and malformed entries. This skill should be used when auditing, migrating, or debugging hosts file content.
license: MIT
agent_created: true
---

# Hosts File Parser

Parse a hosts-format text file with the bundled standard-library CLI. Validate IPv4 and IPv6 addresses, collect address-to-alias records, and report duplicate mappings or malformed entries.

## When to Use / Triggers

- Audit a hosts file before deploying it to endpoints.
- Extract address and hostname aliases from hosts-format text.
- Find duplicate mappings or invalid addresses and aliases.
- Convert hosts-file validation results to JSON for automation.

## Usage

```bash
python skills/hosts-file-parser/scripts/hosts_file_parser.py /etc/hosts
python skills/hosts-file-parser/scripts/hosts_file_parser.py hosts.txt --json
python skills/hosts-file-parser/scripts/hosts_file_parser.py - --json < hosts.txt
```

## Output

- Treat the first non-comment token as an IPv4 or IPv6 address.
- Treat remaining tokens as hostname aliases.
- Mark repeated address-and-alias pairs as duplicates.
- Report missing aliases, invalid addresses, and invalid aliases as invalid entries.
- Return exit status `1` when invalid entries exist; still emit the complete report.

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/hosts_file_parser.py --help` for all options.
