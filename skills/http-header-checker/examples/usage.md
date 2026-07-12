# Usage Examples

## 1. Basic check

```bash
python skills/http-header-checker/scripts/check_headers.py https://example.com
```

Output:

```text
HTTP Security Header Report for https://example.com

  [-] Content-Security-Policy
  [+] Strict-Transport-Security = max-age=31536000
  [+] X-Frame-Options = DENY
  [+] X-Content-Type-Options = nosniff
  [-] X-XSS-Protection
  [-] Referrer-Policy
  [-] Permissions-Policy

  3 present, 4 missing, 0 misconfigured
```

## 2. JSON output

```bash
python skills/http-header-checker/scripts/check_headers.py https://example.com --json
```

Returns structured JSON with `results`, `present`, `missing`, `misconfigured` counts.

## 3. CI integration

```bash
python skills/http-header-checker/scripts/check_headers.py https://example.com --exit-code
```

Exits with code 1 if any high-severity header is missing.

## 4. Custom timeout

```bash
python skills/http-header-checker/scripts/check_headers.py https://slow-site.com --timeout 30
```
