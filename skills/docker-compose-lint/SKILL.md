---
name: docker-compose-lint
description: Lint docker-compose YAML files for best practices and common issues without external dependencies.
license: MIT
---

# Docker Compose Lint

> Check docker-compose YAML files for common misconfigurations and best practice violations.

## When to Use / Triggers

- Validate docker-compose.yml before deployment.
- Audit Compose files for security and reliability issues.
- Enforce Compose best practices.

## Capabilities

- `lint`: check a docker-compose YAML file.
- Checks: missing image pin, using latest tag, privileged mode, missing healthcheck,
  no restart policy, exposed privileged ports, missing volume mounts for DBs, etc.
- `--json` for machine-readable output.

## Usage

```bash
python skills/docker-compose-lint/scripts/docker_compose_lint.py lint --file docker-compose.yml
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/docker_compose_lint.py --help` for all options.
