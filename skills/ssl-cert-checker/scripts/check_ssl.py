#!/usr/bin/env python3
"""ssl-cert-checker — check SSL certificate details for a domain.

Usage:
    python check_ssl.py DOMAIN [--port PORT] [--warn-days N] [--json] [--exit-code]

Connects to the domain, retrieves the certificate, and reports validity info.
"""

import argparse
import json
import socket
import ssl
import sys
from datetime import datetime, timezone


def _check_cert(domain, port, warn_days):
    """Connect and retrieve cert info. Returns dict or raises."""
    ctx = ssl.create_default_context()
    conn = ctx.wrap_socket(socket.socket(), server_hostname=domain)
    conn.settimeout(10)
    try:
        conn.connect((domain, port))
    except Exception as e:
        return {"error": str(e)}

    cert = conn.getpeercert()
    der_cert = conn.getpeercert(binary_form=True)
    conn.close()

    if not cert:
        return {"error": "no certificate returned"}

    # Parse subject/issuer (format: ((('key', 'value'),), (('key2', 'val2'),),))
    def _parse_name(name_tuple):
        result = {}
        for item in name_tuple:
            # Each item may be a nested tuple like (('commonName', 'example.com'),)
            if isinstance(item, tuple):
                for sub in item:
                    if isinstance(sub, tuple) and len(sub) == 2:
                        result[sub[0]] = sub[1]
        return result

    subject = _parse_name(cert.get("subject", ()))
    issuer = _parse_name(cert.get("issuer", ()))

    # Parse dates
    not_before = cert.get("notBefore", "")
    not_after = cert.get("notAfter", "")

    def _parse_date(s):
        for fmt in ("%b %d %H:%M:%S %Y %Z", "%b %d %H:%M:%S %Y"):
            try:
                return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None

    nb = _parse_date(not_before)
    na = _parse_date(not_after)

    now = datetime.now(timezone.utc)
    days_remaining = (na - now).days if na else None

    # SANs
    sans = []
    for ext in cert.get("subjectAltName", ()):
        if ext[0] == "DNS":
            sans.append(ext[1])

    # Key info from der
    key_info = ""
    try:
        from ssl import DER_cert_to_PEM_cert
        pem = DER_cert_to_PEM_cert(der_cert) if der_cert else ""
        key_info = "available" if pem else "unavailable"
    except Exception:
        key_info = "unavailable"

    # Status
    if days_remaining is not None and days_remaining < 0:
        status = "EXPIRED"
    elif days_remaining is not None and days_remaining <= warn_days:
        status = "EXPIRING_SOON"
    else:
        status = "VALID"

    result = {
        "domain": domain,
        "status": status,
        "subject": subject,
        "issuer": issuer,
        "not_before": not_before,
        "not_after": not_after,
        "days_remaining": days_remaining,
        "san_domains": sans,
        "key_info": key_info,
    }
    return result


def main():
    ap = argparse.ArgumentParser(
        description="Check SSL certificate validity and details for a domain."
    )
    ap.add_argument("domain", help="domain name to check")
    ap.add_argument("--port", type=int, default=443, help="port (default: 443)")
    ap.add_argument("--warn-days", type=int, default=30,
                    help="warn if cert expires within N days (default: 30)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit 1 if cert is expired or expiring soon")
    args = ap.parse_args()

    result = _check_cert(args.domain, args.port, args.warn_days)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(2)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"SSL Certificate Report for {args.domain}\n")
        cn = result["subject"].get("commonName", "N/A")
        issuer_cn = result["issuer"].get("commonName", result["issuer"].get("organizationName", "N/A"))
        print(f"  Subject:     {cn}")
        print(f"  Issuer:      {issuer_cn}")
        print(f"  Valid from:  {result['not_before']}")
        print(f"  Valid until: {result['not_after']}")
        print(f"  Days left:   {result['days_remaining']}")
        print(f"  Status:      {result['status']}")
        if result["san_domains"]:
            print(f"  SANs:        {', '.join(result['san_domains'])}")

    if args.exit_code and result["status"] in ("EXPIRED", "EXPIRING_SOON"):
        print(f"\nCI FAILED: certificate is {result['status'].lower()}.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
