#!/usr/bin/env python3
"""Look up common TCP and UDP service ports without network access."""

from __future__ import annotations

import argparse
import json
from typing import Any

SERVICES: tuple[tuple[int, str, str, str], ...] = (
    (20, "tcp", "ftp-data", "File Transfer Protocol data"),
    (21, "tcp", "ftp", "File Transfer Protocol control"),
    (22, "tcp", "ssh", "Secure Shell"),
    (23, "tcp", "telnet", "Telnet"),
    (25, "tcp", "smtp", "Simple Mail Transfer Protocol"),
    (53, "tcp", "dns", "Domain Name System"),
    (53, "udp", "dns", "Domain Name System"),
    (67, "udp", "dhcp-server", "Dynamic Host Configuration Protocol server"),
    (68, "udp", "dhcp-client", "Dynamic Host Configuration Protocol client"),
    (69, "udp", "tftp", "Trivial File Transfer Protocol"),
    (80, "tcp", "http", "Hypertext Transfer Protocol"),
    (88, "tcp", "kerberos", "Kerberos authentication"),
    (88, "udp", "kerberos", "Kerberos authentication"),
    (110, "tcp", "pop3", "Post Office Protocol version 3"),
    (111, "tcp", "rpcbind", "ONC RPC port mapper"),
    (111, "udp", "rpcbind", "ONC RPC port mapper"),
    (123, "udp", "ntp", "Network Time Protocol"),
    (135, "tcp", "msrpc", "Microsoft RPC endpoint mapper"),
    (137, "udp", "netbios-ns", "NetBIOS name service"),
    (138, "udp", "netbios-dgm", "NetBIOS datagram service"),
    (139, "tcp", "netbios-ssn", "NetBIOS session service"),
    (143, "tcp", "imap", "Internet Message Access Protocol"),
    (161, "udp", "snmp", "Simple Network Management Protocol"),
    (162, "udp", "snmptrap", "Simple Network Management Protocol trap"),
    (179, "tcp", "bgp", "Border Gateway Protocol"),
    (389, "tcp", "ldap", "Lightweight Directory Access Protocol"),
    (389, "udp", "ldap", "Lightweight Directory Access Protocol"),
    (443, "tcp", "https", "HTTP over TLS"),
    (445, "tcp", "microsoft-ds", "Microsoft Directory Services"),
    (465, "tcp", "smtps", "SMTP over implicit TLS"),
    (500, "udp", "isakmp", "Internet Security Association and Key Management Protocol"),
    (514, "udp", "syslog", "System logging"),
    (587, "tcp", "submission", "Mail message submission"),
    (631, "tcp", "ipp", "Internet Printing Protocol"),
    (636, "tcp", "ldaps", "LDAP over TLS"),
    (993, "tcp", "imaps", "IMAP over TLS"),
    (995, "tcp", "pop3s", "POP3 over TLS"),
    (1080, "tcp", "socks", "SOCKS proxy"),
    (1194, "udp", "openvpn", "OpenVPN"),
    (1433, "tcp", "ms-sql-s", "Microsoft SQL Server"),
    (1521, "tcp", "oracle", "Oracle database listener"),
    (2049, "tcp", "nfs", "Network File System"),
    (2049, "udp", "nfs", "Network File System"),
    (2375, "tcp", "docker", "Docker remote API"),
    (2376, "tcp", "docker-tls", "Docker remote API over TLS"),
    (3306, "tcp", "mysql", "MySQL database"),
    (3389, "tcp", "rdp", "Remote Desktop Protocol"),
    (5432, "tcp", "postgresql", "PostgreSQL database"),
    (5672, "tcp", "amqp", "Advanced Message Queuing Protocol"),
    (5900, "tcp", "vnc", "Virtual Network Computing"),
    (6379, "tcp", "redis", "Redis"),
    (6443, "tcp", "kubernetes-api", "Kubernetes API server"),
    (8080, "tcp", "http-alt", "Alternative HTTP"),
    (8443, "tcp", "https-alt", "Alternative HTTPS"),
    (9090, "tcp", "prometheus", "Prometheus metrics"),
    (27017, "tcp", "mongodb", "MongoDB database"),
)


def lookup(query: str, protocol: str | None) -> list[dict[str, Any]]:
    """Find matching entries by exact port or case-insensitive service name."""
    normalized_query = query.strip().lower()
    is_port_query = normalized_query.isdecimal()
    results = []
    for port, item_protocol, service, description in SERVICES:
        if protocol and item_protocol != protocol:
            continue
        matches = port == int(normalized_query) if is_port_query else normalized_query in service.lower()
        if matches:
            results.append(
                {"port": port, "protocol": item_protocol, "service": service, "description": description}
            )
    return results


def format_text(query: str, results: list[dict[str, Any]]) -> str:
    """Format lookup results for a terminal."""
    if not results:
        return f"No common service mapping found for: {query}"
    width = max(len(str(item["port"])) for item in results)
    lines = ["PORT  PROTOCOL  SERVICE         DESCRIPTION"]
    for item in results:
        lines.append(
            f"{item['port']:>{width}}  {item['protocol']:<8}  {item['service']:<14}  {item['description']}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Look up common offline TCP/UDP port-service mappings.")
    parser.add_argument("query", help="Port number or service name")
    parser.add_argument("--protocol", choices=("tcp", "udp"), help="Limit results to one protocol")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output")
    args = parser.parse_args()

    results = lookup(args.query, args.protocol)
    if args.as_json:
        print(json.dumps({"query": args.query, "protocol": args.protocol, "results": results}, indent=2))
    else:
        print(format_text(args.query, results))
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
