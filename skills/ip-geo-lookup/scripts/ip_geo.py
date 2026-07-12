#!/usr/bin/env python3
"""ip-geo-lookup — look up geographic info for IP addresses.

Usage:
    python ip_geo.py IP [--json] [--fields F1,F2,...]
    python ip_geo.py --file IPS_FILE [--json]

Uses the free ip-api.com HTTP API. Rate limited to 45 requests/minute.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

API_URL = "http://ip-api.com/json/{ip}?fields=status,message,query,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as"

DEFAULT_FIELDS = ["query", "country", "regionName", "city", "lat", "lon", "isp", "org", "as"]


def _lookup_ip(ip):
    """Query ip-api.com for a single IP."""
    url = API_URL.format(ip=ip.strip())
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ip-geo-lookup/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"query": ip, "status": "error", "message": f"HTTP {e.code}"}
    except Exception as e:
        return {"query": ip, "status": "error", "message": str(e)}

    if data.get("status") == "fail":
        return data
    return data


def _format_text(result, fields):
    """Format a single result as text."""
    lines = []
    ip = result.get("query", "unknown")
    if result.get("status") == "fail":
        lines.append(f"  {ip}: lookup failed — {result.get('message', 'unknown error')}")
    else:
        lines.append(f"  {ip}:")
        for f in fields:
            if f in result and result[f]:
                lines.append(f"    {f}: {result[f]}")
    return lines


def main():
    ap = argparse.ArgumentParser(
        description="Look up geographic location info for IP addresses."
    )
    ap.add_argument("ip", nargs="?", help="IP address to look up")
    ap.add_argument("--file", "-f", help="file with one IP per line")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--fields", default=",".join(DEFAULT_FIELDS),
                    help="comma-separated fields to show (default: %(default)s)")
    args = ap.parse_args()

    if not args.ip and not args.file:
        ap.error("provide an IP address or --file")

    fields = [f.strip() for f in args.fields.split(",") if f.strip()]

    # Collect IPs
    ips = []
    if args.ip:
        ips.append(args.ip.strip())
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        ips.append(line)
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)

    if not ips:
        print("Error: no IP addresses to look up", file=sys.stderr)
        sys.exit(2)

    # Query
    results = []
    for ip in ips:
        result = _lookup_ip(ip)
        results.append(result)

    # Output
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            for line in _format_text(r, fields):
                print(line)
            print()


if __name__ == "__main__":
    main()
