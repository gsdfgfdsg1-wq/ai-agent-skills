---
name: nginx-config-lint
description: Lint nginx configuration files for common issues and best practices without external dependencies.
license: MIT
---

# Nginx Config Lint

> Check nginx configuration files for common misconfigurations, security issues, and style problems.

## When to Use / Triggers

- Review nginx config before deployment.
- Audit existing nginx configurations for security gaps.
- Enforce consistent nginx config style.

## Capabilities

- `lint`: check an nginx config file for issues.
- Checks: missing server_name, root inside server, autoindex on, missing access_log,
  hardcoded secrets, missing SSL directives on port 443, duplicate directives, etc.
- `--json` for machine-readable output.
- `--severity` filter by severity (info, warning, error).

## Usage

```bash
python skills/nginx-config-lint/scripts/nginx_config_lint.py lint --file nginx.conf
python skills/nginx-config-lint/scripts/nginx_config_lint.py lint --file sites-enabled/app.conf --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/nginx_config_lint.py --help` for all options.
