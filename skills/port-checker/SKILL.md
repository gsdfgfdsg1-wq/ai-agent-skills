---
name: port-checker
description: Check whether TCP ports on a host are open or closed with timeout control and batch scanning without external dependencies.
license: MIT
---

# Port Checker

> Check TCP port connectivity on local or remote hosts with batch scanning, timeout control, and JSON output.

## When to Use / Triggers

- Verify that a service is listening on a specific port.
- Batch-check a range of ports on a host.
- Validate firewall rules by testing port reachability.
- CI gate: ensure required ports are open before deployment.

## Capabilities

- `check`: check a single host:port combination.
- `range`: scan a range of ports on a host.
- `batch`: check multiple host:port pairs from a file or arguments.
- `--timeout` socket timeout in seconds (default 3).
- `--json` machine-readable output.
- `--open-only` only show open ports.

## Usage

```bash
python skills/port-checker/scripts/port_checker.py check --host localhost --port 8080
python skills/port-checker/scripts/port_checker.py range --host localhost --start 8000 --end 9000
python skills/port-checker/scripts/port_checker.py batch --pairs localhost:80 localhost:443 localhost:8080
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/port_checker.py --help` for all options.
