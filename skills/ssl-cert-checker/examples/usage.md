# Usage Examples

## 1. Basic certificate check

```bash
python skills/ssl-cert-checker/scripts/check_ssl.py example.com
```

Output:

```text
SSL Certificate Report for example.com

  Subject:     www.example.com
  Issuer:      DigiCert TLS RSA SHA256 2020 CA1
  Valid from:  Jan 15 00:00:00 2025 GMT
  Valid until: Feb 15 23:59:59 2026 GMT
  Days left:   217
  Status:      VALID
  SANs:        www.example.com, example.com
```

## 2. Custom warning threshold

```bash
python skills/ssl-cert-checker/scripts/check_ssl.py example.com --warn-days 14
```

## 3. JSON output

```bash
python skills/ssl-cert-checker/scripts/check_ssl.py example.com --json
```

## 4. CI integration

```bash
python skills/ssl-cert-checker/scripts/check_ssl.py example.com --exit-code --warn-days 7
echo $?
# 0 if valid, 1 if expired or expiring within 7 days
```

## 5. Custom port

```bash
python skills/ssl-cert-checker/scripts/check_ssl.py mail.example.com --port 993
```
