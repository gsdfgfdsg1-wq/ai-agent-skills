#!/usr/bin/env python3
"""dns-lookup — query DNS records for a domain.

Usage:
    python dns_lookup.py DOMAIN [--type TYPE] [--all] [--json] [--timeout SECS]

Uses the system DNS resolver via socket and subprocess (nslookup/dig).
"""

import argparse
import json
import socket
import subprocess
import sys
import re

RECORD_TYPES = ("A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA")


def _query_a(domain):
    """Resolve A records via socket."""
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET)
        return list({r[4][0] for r in results})
    except socket.gaierror:
        return []


def _query_aaaa(domain):
    """Resolve AAAA records via socket."""
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET6)
        return list({r[4][0] for r in results})
    except socket.gaierror:
        return []


def _query_cname(domain):
    """Resolve CNAME via socket."""
    try:
        cname = socket.getfqdn(domain)
        if cname != domain:
            # Try gethostbyname_ex which may reveal aliases
            _, aliases, _ = socket.gethostbyname_ex(domain)
            return aliases if aliases else ([cname] if cname != domain else [])
    except socket.gaierror:
        pass
    return []


def _nslookup(domain, rtype):
    """Use nslookup command as fallback for MX, TXT, NS, SOA."""
    try:
        result = subprocess.run(
            ["nslookup", "-type=" + rtype.lower(), domain],
            capture_output=True, text=True, timeout=10, encoding="utf-8", errors="replace"
        )
        output = result.stdout + result.stderr
        records = []
        lines = output.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("Server:") or line.startswith("Address:") or line.startswith("#"):
                continue
            # Match patterns like "mail exchanger = 10 mail.example.com"
            if rtype == "MX" and "mail exchanger" in line.lower():
                m = re.search(r"(\d+)\s+(\S+)", line)
                if m:
                    records.append({"priority": int(m.group(1)), "host": m.group(2)})
            elif rtype == "TXT" and "text =" in line.lower():
                m = re.search(r"text\s*=\s*\"?([^\"]+)\"?", line, re.I)
                if m:
                    records.append(m.group(1).strip('"'))
            elif rtype == "NS" and "nameserver" in line.lower():
                m = re.search(r"nameserver\s*=\s*(\S+)", line, re.I)
                if m:
                    records.append(m.group(1))
            elif rtype == "SOA":
                # SOA has multiple fields
                if "origin" in line.lower() or "serial" in line.lower():
                    records.append(line)
        return records
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def _dig_lookup(domain, rtype):
    """Use dig command as fallback (Unix)."""
    try:
        result = subprocess.run(
            ["dig", "+short", rtype, domain],
            capture_output=True, text=True, timeout=10
        )
        lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
        if rtype == "MX":
            records = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        records.append({"priority": int(parts[0]), "host": parts[1]})
                    except ValueError:
                        records.append({"host": line})
            return records
        return lines
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def _query_records(domain, rtype):
    """Query a specific record type."""
    if rtype == "A":
        return _query_a(domain)
    elif rtype == "AAAA":
        return _query_aaaa(domain)
    elif rtype == "CNAME":
        return _query_cname(domain)
    else:
        # Try nslookup first, then dig
        records = _nslookup(domain, rtype)
        if not records:
            records = _dig_lookup(domain, rtype)
        return records


def main():
    ap = argparse.ArgumentParser(
        description="Query DNS records for a domain using the system resolver."
    )
    ap.add_argument("domain", help="domain name to look up")
    ap.add_argument("--type", "-t", choices=[r.lower() for r in RECORD_TYPES],
                    help="specific record type to query")
    ap.add_argument("--all", action="store_true", help="query all record types")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    types_to_query = RECORD_TYPES if args.all else [args.type.upper()] if args.type else ["A", "AAAA", "MX", "NS", "TXT"]

    results = {}
    for rt in types_to_query:
        results[rt] = _query_records(domain=args.domain, rtype=rt)

    if args.json:
        print(json.dumps({"domain": args.domain, "records": results}, indent=2, ensure_ascii=False))
    else:
        print(f"DNS Lookup for {args.domain}\n")
        for rt in types_to_query:
            records = results[rt]
            if not records:
                print(f"  {rt}: (none found)")
            else:
                print(f"  {rt}:")
                for r in records:
                    if isinstance(r, dict):
                        print(f"    {r}")
                    else:
                        print(f"    {r}")


if __name__ == "__main__":
    main()
