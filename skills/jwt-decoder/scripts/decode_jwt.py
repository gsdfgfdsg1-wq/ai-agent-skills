#!/usr/bin/env python3
"""jwt-decoder — decode and inspect JWT tokens (no verification).

Usage:
    python decode_jwt.py TOKEN [--json] [--check-exp]

Decodes the header and payload of a JWT (JWS compact serialization) and
optionally checks whether the token has expired. Does NOT verify signatures.
"""

import argparse
import base64
import json
import sys
from datetime import datetime, timezone


def _b64url_decode(data):
    """Decode base64url-encoded string (no padding required)."""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    try:
        return base64.urlsafe_b64decode(data)
    except Exception as e:
        raise ValueError(f"base64url decode failed: {e}")


def decode_jwt(token):
    """Decode a JWT token and return (header, payload, signature_bytes)."""
    parts = token.strip().split(".")
    if len(parts) != 3:
        raise ValueError(f"JWT must have 3 dot-separated parts, got {len(parts)}")

    try:
        header = json.loads(_b64url_decode(parts[0]))
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"invalid JWT header: {e}")

    try:
        payload = json.loads(_b64url_decode(parts[1]))
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"invalid JWT payload: {e}")

    try:
        signature = _b64url_decode(parts[2])
    except ValueError:
        signature = b""

    return header, payload, signature


def _format_timestamp(ts):
    """Format a Unix timestamp to a human-readable string."""
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (OSError, OverflowError, ValueError):
        return str(ts)


def main():
    ap = argparse.ArgumentParser(
        description="Decode and inspect JWT tokens (no signature verification)."
    )
    ap.add_argument("token", help="JWT token string")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--check-exp", action="store_true",
                    help="check if token is expired (based on exp claim)")
    args = ap.parse_args()

    try:
        header, payload, sig = decode_jwt(args.token)
    except ValueError as e:
        if args.json:
            print(json.dumps({"valid": False, "error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    result = {
        "valid": True,
        "header": header,
        "payload": payload,
        "signature_length": len(sig),
    }

    if args.check_exp:
        exp = payload.get("exp")
        iat = payload.get("iat")
        nbf = payload.get("nbf")
        now = datetime.now(tz=timezone.utc).timestamp()

        if exp is not None:
            if isinstance(exp, (int, float)):
                result["expires_at"] = _format_timestamp(exp)
                result["expired"] = now > exp
        if iat is not None and isinstance(iat, (int, float)):
            result["issued_at"] = _format_timestamp(iat)
        if nbf is not None and isinstance(nbf, (int, float)):
            result["not_before"] = _format_timestamp(nbf)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Header:")
        print(json.dumps(header, indent=2, ensure_ascii=False))
        print("\nPayload:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        if args.check_exp:
            exp = payload.get("exp")
            if exp is not None and isinstance(exp, (int, float)):
                status = "EXPIRED" if result.get("expired") else "VALID"
                print(f"\nExpiration: {_format_timestamp(exp)} ({status})")

            iat = payload.get("iat")
            if iat is not None and isinstance(iat, (int, float)):
                print(f"Issued at:  {_format_timestamp(iat)}")

            nbf = payload.get("nbf")
            if nbf is not None and isinstance(nbf, (int, float)):
                print(f"Not before: {_format_timestamp(nbf)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
