---
name: jwt-decoder
description: Decode and inspect JWT tokens — display header and payload, optionally check expiration, issued-at, and not-before claims without signature verification or external dependencies.
license: MIT
---

# JWT Decoder

> Quickly peek inside a JWT — see its header, payload, and expiration status without needing the signing key.

## When to Use / Triggers

- Debugging authentication issues: check what's inside a token.
- Verify token expiration before sending requests.
- Inspect token claims (roles, scopes, issuer) during development.
- CI: validate that generated tokens contain expected claims.

## Capabilities

- Decodes JWS compact serialization tokens (3-part `xxx.yyy.zzz`).
- Displays header (alg, typ) and full payload.
- `--check-exp` evaluates `exp`, `iat`, `nbf` claims against current time.
- `--json` for programmatic consumption.
- No signature verification (safe for inspection only).

## Usage

```bash
# Basic decode
python skills/jwt-decoder/scripts/decode_jwt.py "eyJ..."

# Check expiration
python skills/jwt-decoder/scripts/decode_jwt.py "eyJ..." --check-exp

# JSON output
python skills/jwt-decoder/scripts/decode_jwt.py "eyJ..." --json --check-exp
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/decode_jwt.py --help` for all options.
