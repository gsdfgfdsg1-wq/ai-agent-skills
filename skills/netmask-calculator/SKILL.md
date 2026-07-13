---
name: netmask-calculator
description: Calculate IPv4 CIDR network details including network address, broadcast address, subnet mask, host range, and host counts in text or JSON without external dependencies.
license: MIT
agent_created: true
---

# Netmask Calculator

> Derive IPv4 subnet details from CIDR notation with a standard-library Python CLI.

## When to Use / Triggers

- Calculate the network and broadcast address for an IPv4 CIDR.
- Convert an IPv4 prefix length to a dotted-decimal netmask.
- Determine the usable host range and host count for a subnet.
- Return subnet facts in JSON for scripts or automation.

## Capabilities

- Accepts an IPv4 CIDR such as `192.168.1.10/24`.
- Normalizes host input to its containing network.
- Shows network address, broadcast address, netmask, hostmask, prefix length, and address counts.
- Handles `/31` and `/32` using their RFC 3021/single-host usable address semantics.
- `--json` emits machine-readable output.

## Usage

```bash
python skills/netmask-calculator/scripts/netmask_calculator.py 192.168.1.10/24
python skills/netmask-calculator/scripts/netmask_calculator.py 10.0.0.0/8 --json
python skills/netmask-calculator/scripts/netmask_calculator.py 203.0.113.0/31
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/netmask_calculator.py --help` for all options.
