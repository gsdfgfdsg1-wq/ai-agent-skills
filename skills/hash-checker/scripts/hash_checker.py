#!/usr/bin/env python3
"""Hash Checker — compute and verify file/text hashes (MD5/SHA1/SHA256/SHA512)."""

import argparse
import hashlib
import json
import os
import sys

ALGORITHMS = ("md5", "sha1", "sha256", "sha512")


def _hash_bytes(data: bytes, algorithm: str) -> str:
    """Return hex digest of *data* using *algorithm*."""
    return hashlib.new(algorithm, data).hexdigest()


def _hash_file(path: str, algorithm: str) -> str:
    """Return hex digest of the file at *path* using *algorithm*."""
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _exit(msg: str, code: int = 1) -> None:
    """Print error message to stderr and exit."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


# ── Subcommand handlers ──────────────────────────────────────────────


def cmd_compute(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.file):
        _exit(f"file not found: {args.file}")

    digest = _hash_file(args.file, args.algorithm)

    if args.json:
        print(json.dumps({
            "file": args.file,
            "algorithm": args.algorithm,
            "hash": digest,
        }, indent=2))
    else:
        print(f"{digest}  {args.file}")


def cmd_verify(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.file):
        _exit(f"file not found: {args.file}")

    digest = _hash_file(args.file, args.algorithm)
    matched = digest.lower() == args.hash.lower()

    if args.json:
        print(json.dumps({
            "file": args.file,
            "algorithm": args.algorithm,
            "expected": args.hash,
            "actual": digest,
            "match": matched,
        }, indent=2))
    else:
        status = "MATCH" if matched else "MISMATCH"
        print(f"{status}: {args.file}")
        print(f"  expected: {args.hash}")
        print(f"  actual:   {digest}")

    sys.exit(0 if matched else 2)


def cmd_text(args: argparse.Namespace) -> None:
    data = args.string.encode("utf-8")
    digest = _hash_bytes(data, args.algorithm)

    if args.json:
        print(json.dumps({
            "text": args.string,
            "algorithm": args.algorithm,
            "hash": digest,
        }, indent=2))
    else:
        print(f"{digest}  (text)")


# ── CLI definition ────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hash_checker",
        description="Compute and verify file/text hashes (MD5/SHA1/SHA256/SHA512).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── compute ───────────────────────────────────────────────────────
    p_compute = subparsers.add_parser("compute", help="Compute hash of a file.")
    p_compute.add_argument("--file", required=True, help="Path to the file.")
    p_compute.add_argument(
        "--algorithm",
        choices=ALGORITHMS,
        default="sha256",
        help="Hash algorithm (default: sha256).",
    )
    p_compute.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output results as JSON.",
    )
    p_compute.set_defaults(func=cmd_compute)

    # ── verify ────────────────────────────────────────────────────────
    p_verify = subparsers.add_parser("verify", help="Verify a file against a known hash.")
    p_verify.add_argument("--file", required=True, help="Path to the file.")
    p_verify.add_argument("--hash", required=True, help="Expected hash string.")
    p_verify.add_argument(
        "--algorithm",
        choices=ALGORITHMS,
        default="sha256",
        help="Hash algorithm (default: sha256).",
    )
    p_verify.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output results as JSON.",
    )
    p_verify.set_defaults(func=cmd_verify)

    # ── text ──────────────────────────────────────────────────────────
    p_text = subparsers.add_parser("text", help="Compute hash of a text string.")
    p_text.add_argument("-s", "--string", required=True, help="Text string to hash.")
    p_text.add_argument(
        "--algorithm",
        choices=ALGORITHMS,
        default="sha256",
        help="Hash algorithm (default: sha256).",
    )
    p_text.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output results as JSON.",
    )
    p_text.set_defaults(func=cmd_text)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
