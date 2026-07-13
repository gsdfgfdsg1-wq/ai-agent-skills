#!/usr/bin/env python3
"""Check TCP port connectivity on local or remote hosts."""

import argparse
import json
import socket
import sys


def check_port(host, port, timeout=3):
    """Check if a TCP port is open. Returns (port, open, latency_ms)."""
    import time
    start = time.monotonic()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
        latency = (time.monotonic() - start) * 1000
        return port, result == 0, round(latency, 1)
    except socket.gaierror:
        return port, False, 0
    except socket.timeout:
        return port, False, round(timeout * 1000, 1)
    except OSError:
        return port, False, 0


def cmd_check(args):
    port, is_open, latency = check_port(args.host, args.port, args.timeout)
    status = "OPEN" if is_open else "CLOSED"
    if args.json:
        print(json.dumps({"host": args.host, "port": port, "status": status, "latency_ms": latency}, indent=2))
    else:
        print(f"{args.host}:{port} — {status} ({latency}ms)")
    if not is_open:
        sys.exit(1)


def cmd_range(args):
    results = []
    for p in range(args.start, args.end + 1):
        port, is_open, latency = check_port(args.host, p, args.timeout)
        if args.open_only and not is_open:
            continue
        results.append({"port": port, "status": "OPEN" if is_open else "CLOSED", "latency_ms": latency})

    if args.json:
        print(json.dumps({"host": args.host, "results": results}, indent=2))
    else:
        for r in results:
            print(f"{args.host}:{r['port']} — {r['status']} ({r['latency_ms']}ms)")

    open_count = sum(1 for r in results if r["status"] == "OPEN")
    if not args.json:
        print(f"\nScanned {len(results)} port(s): {open_count} open, {len(results) - open_count} closed")


def cmd_batch(args):
    pairs = []
    if args.pairs:
        for pair in args.pairs:
            if ":" not in pair:
                print(f"Error: invalid pair '{pair}', expected host:port", file=sys.stderr)
                sys.exit(1)
            h, p = pair.rsplit(":", 1)
            try:
                pairs.append((h, int(p)))
            except ValueError:
                print(f"Error: invalid port in '{pair}'", file=sys.stderr)
                sys.exit(1)
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" not in line:
                        continue
                    h, p = line.rsplit(":", 1)
                    try:
                        pairs.append((h, int(p)))
                    except ValueError:
                        continue
        except OSError as e:
            print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: provide --pairs or --file", file=sys.stderr)
        sys.exit(1)

    results = []
    for h, p in pairs:
        port, is_open, latency = check_port(h, p, args.timeout)
        if args.open_only and not is_open:
            continue
        results.append({"host": h, "port": port, "status": "OPEN" if is_open else "CLOSED", "latency_ms": latency})

    if args.json:
        print(json.dumps({"results": results}, indent=2))
    else:
        for r in results:
            print(f"{r['host']}:{r['port']} — {r['status']} ({r['latency_ms']}ms)")


def main():
    parser = argparse.ArgumentParser(description="Check TCP port connectivity.")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="Check a single port")
    p_check.add_argument("--host", required=True, help="Hostname or IP")
    p_check.add_argument("--port", type=int, required=True, help="Port number")
    p_check.add_argument("--timeout", type=float, default=3, help="Socket timeout in seconds (default 3)")
    p_check.add_argument("--json", action="store_true", help="JSON output")

    p_range = sub.add_parser("range", help="Scan a range of ports")
    p_range.add_argument("--host", required=True, help="Hostname or IP")
    p_range.add_argument("--start", type=int, required=True, help="Start port")
    p_range.add_argument("--end", type=int, required=True, help="End port (inclusive)")
    p_range.add_argument("--timeout", type=float, default=3, help="Socket timeout in seconds (default 3)")
    p_range.add_argument("--json", action="store_true", help="JSON output")
    p_range.add_argument("--open-only", action="store_true", help="Only show open ports")

    p_batch = sub.add_parser("batch", help="Check multiple host:port pairs")
    p_batch.add_argument("--pairs", nargs="+", help="host:port pairs")
    p_batch.add_argument("--file", help="File with host:port lines")
    p_batch.add_argument("--timeout", type=float, default=3, help="Socket timeout in seconds (default 3)")
    p_batch.add_argument("--json", action="store_true", help="JSON output")
    p_batch.add_argument("--open-only", action="store_true", help="Only show open ports")

    args = parser.parse_args()
    if args.command == "check":
        cmd_check(args)
    elif args.command == "range":
        cmd_range(args)
    elif args.command == "batch":
        cmd_batch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
