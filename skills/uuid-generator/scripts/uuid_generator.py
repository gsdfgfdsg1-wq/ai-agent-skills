#!/usr/bin/env python3
"""UUID generator, validator, and inspector — stdlib only."""

import argparse
import json
import sys
import uuid


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

NAMESPACE_MAP = {
    "dns": uuid.NAMESPACE_DNS,
    "url": uuid.NAMESPACE_URL,
    "oid": uuid.NAMESPACE_OID,
    "null": uuid.UUID("00000000-0000-0000-0000-000000000000"),
}

VARIANT_NAMES = {
    uuid.RESERVED_NCS: "reserved (NCS)",
    uuid.RFC_4122: "RFC 4122",
    uuid.RESERVED_MICROSOFT: "reserved (Microsoft)",
    uuid.RESERVED_FUTURE: "reserved (future)",
}


def _parse_uuid(s: str):
    """Return a uuid.UUID or raise ValueError with a clear message."""
    try:
        return uuid.UUID(s)
    except ValueError:
        raise ValueError(f"Invalid UUID string: '{s}'")


def _uuid_to_dict(u: uuid.UUID) -> dict:
    return {
        "uuid": str(u),
        "version": u.version,
        "variant": VARIANT_NAMES.get(u.variant, str(u.variant)),
        "hex": u.hex,
        "int": u.int,
        "urn": u.urn,
        "fields": {
            "time_low": u.time_low,
            "time_mid": u.time_mid,
            "time_hi_version": u.time_hi_version,
            "clock_seq_hi_variant": u.clock_seq_hi_variant,
            "clock_seq_low": u.clock_seq_low,
            "node": u.node,
        },
    }


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_generate(args: argparse.Namespace) -> None:
    if args.version not in (4, 5):
        print(f"Error: unsupported version '{args.version}'. Choose 4 or 5.", file=sys.stderr)
        sys.exit(1)

    if args.version == 5:
        if not args.name:
            print("Error: --name is required for v5 UUIDs.", file=sys.stderr)
            sys.exit(1)
        if not args.namespace:
            print("Error: --namespace is required for v5 UUIDs.", file=sys.stderr)
            sys.exit(1)
        if args.namespace not in NAMESPACE_MAP:
            ns_keys = ", ".join(NAMESPACE_MAP)
            print(f"Error: invalid namespace '{args.namespace}'. Choose from: {ns_keys}", file=sys.stderr)
            sys.exit(1)

    results = []
    for _ in range(args.count):
        if args.version == 4:
            u = uuid.uuid4()
        else:
            ns = NAMESPACE_MAP[args.namespace]
            u = uuid.uuid5(ns, args.name)

        if args.upper:
            results.append(str(u).upper())
        else:
            results.append(str(u))

    if args.json:
        payload = [{"uuid": r, "version": args.version} for r in results]
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            print(r)


def cmd_validate(args: argparse.Namespace) -> None:
    try:
        u = _parse_uuid(args.uuid_string)
    except ValueError as exc:
        if args.json:
            print(json.dumps({"valid": False, "error": str(exc)}, indent=2))
        else:
            print(f"Invalid: {exc}")
        sys.exit(0)

    if args.json:
        print(json.dumps({"valid": True, "version": u.version, "variant": VARIANT_NAMES.get(u.variant, str(u.variant))}, indent=2))
    else:
        print(f"Valid UUID — version {u.version}, variant {VARIANT_NAMES.get(u.variant, str(u.variant))}")


def cmd_inspect(args: argparse.Namespace) -> None:
    try:
        u = _parse_uuid(args.uuid_string)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    info = _uuid_to_dict(u)

    # Add time / node for time-based UUIDs (v1)
    if u.version == 1:
        info["time"] = u.time
        info["time_as_datetime"] = str(uuid.UUID(int=u.int).time)  # 60-bit timestamp
        info["node"] = u.node
        info["clock_seq"] = u.clock_seq

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"UUID:     {info['uuid']}")
        print(f"Version:  {info['version']}")
        print(f"Variant:  {info['variant']}")
        print(f"Hex:      {info['hex']}")
        print(f"URN:      {info['urn']}")
        print("Fields:")
        for k, v in info["fields"].items():
            print(f"  {k:24s} {v}")
        if u.version == 1:
            print(f"Time:     {info.get('time')}")
            print(f"Node:     {info.get('node')}")
            print(f"ClockSeq: {info.get('clock_seq')}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uuid_generator",
        description="Generate, validate, and inspect UUIDs (v4/v5). No external dependencies.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- generate ---------------------------------------------------------
    gen = sub.add_parser("generate", help="Generate new UUIDs")
    gen.add_argument("--version", type=int, default=4, choices=[4, 5], help="UUID version (default: 4)")
    gen.add_argument("--namespace", choices=list(NAMESPACE_MAP), help="Namespace for v5: dns, url, oid, null")
    gen.add_argument("--name", help="Name string for v5")
    gen.add_argument("--count", type=int, default=1, help="Number of UUIDs to generate (default: 1)")
    gen.add_argument("--upper", action="store_true", help="Output uppercase hex")
    gen.add_argument("--json", action="store_true", help="Output as JSON")

    # -- validate ---------------------------------------------------------
    val = sub.add_parser("validate", help="Validate a UUID string")
    val.add_argument("-s", dest="uuid_string", required=True, help="UUID string to validate")
    val.add_argument("--json", action="store_true", help="Output as JSON")

    # -- inspect ----------------------------------------------------------
    insp = sub.add_parser("inspect", help="Inspect UUID components")
    insp.add_argument("-s", dest="uuid_string", required=True, help="UUID string to inspect")
    insp.add_argument("--json", action="store_true", help="Output as JSON")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "generate": cmd_generate,
        "validate": cmd_validate,
        "inspect": cmd_inspect,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
