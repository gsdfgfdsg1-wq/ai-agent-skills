# Docker Compose Lint — Usage Examples

## 1. Lint a docker-compose file

```bash
python skills/docker-compose-lint/scripts/docker_compose_lint.py lint --file docker-compose.yml
```

Output:

```
Issues in docker-compose.yml:
  ⚠ [app] [warning] latest-tag: service 'app' uses ':latest' tag — pin a specific version
  ℹ [app] [info] no-restart-policy: service 'app' has no restart policy
  ⚠ [db] [warning] missing-healthcheck: service 'db' is a database-like image without healthcheck
  ⚠ [db] [warning] no-volume-for-db: service 'db' is a database without persistent volumes

Total: 4 issue(s)
```

## 2. JSON output

```bash
python skills/docker-compose-lint/scripts/docker_compose_lint.py lint --file docker-compose.yml --json
```

## Error handling

File not found:

```bash
python skills/docker-compose-lint/scripts/docker_compose_lint.py lint --file missing.yml
```

```
Error: cannot read missing.yml: ...
```
