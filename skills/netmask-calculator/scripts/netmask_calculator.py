#!/usr/bin/env python3
"""Calculate IPv4 network details from CIDR notation."""

import argparse
import ipaddress
import json
import sys
from typing import Any


def calculate(cidr: str) -> dict[str, Any]:
    """Return network information for an IPv4 CIDR."""
    network = ipaddress.IPv4Network(cidr, strict=False)
    if network.prefixlen == 32:
        first_host = str(network.network_address)
        last_host = str(network.network_address)
        usable_hosts = 1
    elif network.prefixlen == 31:
        first_host = str(network.network_address)
        last_host = str(network.broadcast_address)
        usable_hosts = 2
    else:
        first_host = str(network.network_address + 1)
        last_host = str(network.broadcast_address - 1)
        usable_hosts = network.num_addresses - 2

    return {
        "input": cidr,
        "cidr": str(network),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "hostmask": str(network.hostmask),
        "prefix_length": network.prefixlen,
        "total_addresses": network.num_addresses,
        "usable_host_count": usable_hosts,
        "first_host": first_host,
        "last_host": last_host,
    }


def print_text(result: dict[str, Any]) -> None:
    print(f"CIDR:              {result['cidr']}")
    print(f"Network address:   {result['network_address']}")
    print(f"Broadcast address: {result['broadcast_address']}")
    print(f"Netmask:           {result['netmask']} (/{result['prefix_length']})")
    print(f"Hostmask:          {result['hostmask']}")
    print(f"Total addresses:   {result['total_addresses']}")
    print(f"Usable hosts:      {result['usable_host_count']}")
    print(f"Host range:        {result['first_host']} - {result['last_host']}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate IPv4 network, broadcast, mask, and host range from CIDR."
    )
    parser.add_argument("cidr", help="IPv4 CIDR, for example 192.168.1.10/24")
    parser.add_argument("--json", action="store_true", help="print JSON output")
    args = parser.parse_args()

    try:
        result = calculate(args.cidr)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as exc:
        print(f"error: invalid IPv4 CIDR '{args.cidr}': {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
