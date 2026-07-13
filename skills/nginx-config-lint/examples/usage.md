# Nginx Config Lint — Usage Examples

## 1. Lint an nginx config file

```bash
python skills/nginx-config-lint/scripts/nginx_config_lint.py lint --file nginx.conf
```

Output:

```
Issues in nginx.conf:
  ⚠ L3: [warning] missing-server-name: server block missing server_name directive
  ✗ L7: [error] hardcoded-secret: possible hardcoded secret found: api_key abc123def;
  ℹ L3: [info] missing-access-log: server block missing access_log directive

Total: 3 issue(s)
```

## 2. JSON output

```bash
python skills/nginx-config-lint/scripts/nginx_config_lint.py lint --file nginx.conf --json
```

```json
{
  "file": "nginx.conf",
  "issues": [
    {"line": 3, "severity": "warning", "rule": "missing-server-name", "message": "server block missing server_name directive"},
    {"line": 7, "severity": "error", "rule": "hardcoded-secret", "message": "possible hardcoded secret found: api_key abc123def;"}
  ]
}
```

## 3. Filter by severity

```bash
python skills/nginx-config-lint/scripts/nginx_config_lint.py lint --file nginx.conf --severity error
```

## Error handling

File not found:

```bash
python skills/nginx-config-lint/scripts/nginx_config_lint.py lint --file missing.conf
```

```
Error: cannot read missing.conf: [Errno 2] No such file or directory: 'missing.conf'
```
