# Usage Examples

## 1. Basic decode

```bash
python skills/jwt-decoder/scripts/decode_jwt.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

Output:

```text
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```

## 2. Check expiration

```bash
python skills/jwt-decoder/scripts/decode_jwt.py "eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDAwMDAwMDB9.sig" --check-exp
```

Shows the expiration time and whether the token is VALID or EXPIRED.

## 3. JSON output

```bash
python skills/jwt-decoder/scripts/decode_jwt.py "eyJ..." --json --check-exp
```

Returns a JSON object with `valid`, `header`, `payload`, `signature_length`, and optional `expires_at` / `expired` / `issued_at` / `not_before` fields.

## 4. Invalid token

```bash
python skills/jwt-decoder/scripts/decode_jwt.py "not-a-jwt"
```

Returns exit code 1 and an error message (or JSON error with `--json`).
