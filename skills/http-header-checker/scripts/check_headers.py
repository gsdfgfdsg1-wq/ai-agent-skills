#!/usr/bin/env python3
"""http-header-checker — check HTTP security response headers for a URL.

Usage:
    python check_headers.py URL [--json] [--exit-code] [--timeout SECS] [--max-redirects N]

Fetches the URL and reports on the presence and quality of security headers.
"""

import argparse
import json
import ssl
import sys
from http.client import HTTPSConnection, HTTPConnection
from urllib.parse import urlparse

SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "severity": "high",
        "description": "Prevents XSS and data injection by controlling resource loading.",
    },
    "Strict-Transport-Security": {
        "severity": "high",
        "description": "Forces HTTPS connections for future visits.",
    },
    "X-Frame-Options": {
        "severity": "medium",
        "description": "Prevents clickjacking by controlling iframe embedding.",
    },
    "X-Content-Type-Options": {
        "severity": "medium",
        "description": "Prevents MIME-type sniffing (should be 'nosniff').",
    },
    "X-XSS-Protection": {
        "severity": "low",
        "description": "Legacy XSS filter (modern browsers use CSP instead).",
    },
    "Referrer-Policy": {
        "severity": "medium",
        "description": "Controls how much referrer info is shared cross-origin.",
    },
    "Permissions-Policy": {
        "severity": "medium",
        "description": "Controls which browser features the page can use.",
    },
    "Cross-Origin-Opener-Policy": {
        "severity": "low",
        "description": "Isolates browsing context from cross-origin documents.",
    },
    "Cross-Origin-Resource-Policy": {
        "severity": "low",
        "description": "Prevents cross-origin resource loading.",
    },
    "Cross-Origin-Embedder-Policy": {
        "severity": "low",
        "description": "Controls cross-origin resource embedding.",
    },
}


def _fetch_headers(url, timeout, max_redirects):
    """Fetch URL headers using http.client (no external deps)."""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)

    host = parsed.hostname
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    headers = {}
    redirects_left = max_redirects
    current_url = url

    while redirects_left >= 0:
        parsed = urlparse(current_url)
        host = parsed.hostname
        port = parsed.port
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        try:
            if parsed.scheme == "https":
                ctx = ssl.create_default_context()
                conn = HTTPSConnection(host, port=port or 443, timeout=timeout, context=ctx)
            else:
                conn = HTTPConnection(host, port=port or 80, timeout=timeout)
            conn.request("HEAD", path, headers={"User-Agent": "http-header-checker/1.0"})
            resp = conn.getresponse()
        except Exception as e:
            return None, str(e)

        # Collect headers
        resp_headers = {k: v for k, v in resp.getheaders()}

        # Follow redirects
        if resp.status in (301, 302, 303, 307, 308):
            location = resp_headers.get("Location", resp_headers.get("location", ""))
            if not location:
                break
            if location.startswith("/"):
                location = f"{parsed.scheme}://{parsed.netloc}{location}"
            current_url = location
            redirects_left -= 1
            conn.close()
            continue

        conn.close()
        return resp_headers, None

    return None, "too many redirects"


def _check_headers(resp_headers):
    """Check security headers and return results list."""
    results = []
    # Header names are case-insensitive in HTTP; normalize to title-case lookup
    header_map = {}
    for k, v in resp_headers.items():
        header_map[k.lower()] = v

    for header, info in SECURITY_HEADERS.items():
        value = header_map.get(header.lower())
        if value is None:
            status = "MISSING"
        elif header == "X-Content-Type-Options" and value.lower() != "nosniff":
            status = "MISCONFIGURED"
        elif header == "X-Frame-Options" and value.lower() not in ("deny", "sameorigin"):
            status = "MISCONFIGURED"
        elif header == "Strict-Transport-Security" and "max-age" not in value.lower():
            status = "MISCONFIGURED"
        else:
            status = "OK"
        results.append({
            "header": header,
            "status": status,
            "severity": info["severity"],
            "description": info["description"],
            "value": value,
        })
    return results


def main():
    ap = argparse.ArgumentParser(
        description="Check HTTP security response headers for a URL."
    )
    ap.add_argument("url", help="URL to check")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit 1 if any high-severity header is missing")
    ap.add_argument("--timeout", type=int, default=10, help="request timeout in seconds (default: 10)")
    ap.add_argument("--max-redirects", type=int, default=5, help="max redirects to follow (default: 5)")
    args = ap.parse_args()

    resp_headers, err = _fetch_headers(args.url, args.timeout, args.max_redirects)
    if err:
        print(f"Error fetching {args.url}: {err}", file=sys.stderr)
        sys.exit(2)

    results = _check_headers(resp_headers)

    if args.json:
        output = {
            "url": args.url,
            "results": results,
            "present": sum(1 for r in results if r["status"] == "OK"),
            "missing": sum(1 for r in results if r["status"] == "MISSING"),
            "misconfigured": sum(1 for r in results if r["status"] == "MISCONFIGURED"),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"HTTP Security Header Report for {args.url}\n")
        for r in results:
            icon = {"OK": "+", "MISSING": "-", "MISCONFIGURED": "!"}[r["status"]]
            line = f"  [{icon}] {r['header']}"
            if r["status"] == "OK":
                line += f" = {r['value']}"
            elif r["status"] == "MISCONFIGURED":
                line += f" = {r['value']} (expected different value)"
            print(line)
        present = sum(1 for r in results if r["status"] == "OK")
        missing = sum(1 for r in results if r["status"] == "MISSING")
        misconf = sum(1 for r in results if r["status"] == "MISCONFIGURED")
        print(f"\n  {present} present, {missing} missing, {misconf} misconfigured")

    if args.exit_code:
        high_missing = any(
            r["status"] in ("MISSING", "MISCONFIGURED") and r["severity"] == "high"
            for r in results
        )
        if high_missing:
            print("\nCI FAILED: high-severity security headers missing or misconfigured.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
