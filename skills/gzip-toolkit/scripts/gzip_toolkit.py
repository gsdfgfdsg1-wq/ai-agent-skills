#!/usr/bin/env python3
"""gzip-toolkit: Compress, decompress, inspect, and test gzip files using only the Python standard library."""

import argparse
import gzip
import json
import os
import struct
import sys


def _die(message, json_mode=False):
    """Print an error message and exit with code 1."""
    if json_mode:
        print(json.dumps({"success": False, "error": message}))
    else:
        print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def _output(data, json_mode):
    """Print result in the requested format."""
    if json_mode:
        print(json.dumps(data, indent=2))
    else:
        for key, value in data.items():
            if key == "success":
                continue
            print(f"{key}: {value}")


def _parse_gzip_mtime(filepath):
    """Extract the modification time from a gzip file header.

    The gzip header format (RFC 1952):
      Offset 4, 4 bytes: modification time (Unix timestamp, little-endian).
    A value of 0 means no mtime is set.
    """
    try:
        with open(filepath, "rb") as f:
            header = f.read(10)
            if len(header) < 10 or header[:2] != b"\x1f\x8b":
                return None
            mtime_bytes = header[4:8]
            mtime = struct.unpack("<I", mtime_bytes)[0]
            return mtime if mtime != 0 else None
    except Exception:
        return None


def cmd_compress(args):
    """Compress a file to gzip format."""
    json_mode = args.json
    input_path = args.file
    level = args.level
    output_path = args.output

    if not os.path.isfile(input_path):
        _die(f"File not found: {input_path}", json_mode)

    if not 1 <= level <= 9:
        _die(f"Invalid compression level: {level} (must be 1-9)", json_mode)

    if output_path is None:
        output_path = input_path + ".gz"

    if os.path.exists(output_path):
        _die(f"Output file already exists: {output_path}", json_mode)

    original_size = os.path.getsize(input_path)

    try:
        with open(input_path, "rb") as f_in:
            with gzip.open(output_path, "wb", compresslevel=level) as f_out:
                while True:
                    chunk = f_in.read(65536)
                    if not chunk:
                        break
                    f_out.write(chunk)
    except Exception as e:
        _die(f"Compression failed: {e}", json_mode)

    compressed_size = os.path.getsize(output_path)
    ratio = (compressed_size / original_size * 100) if original_size > 0 else 0.0

    result = {
        "success": True,
        "input_file": input_path,
        "output_file": output_path,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": f"{ratio:.1f}%",
        "level": level,
    }
    _output(result, json_mode)


def cmd_decompress(args):
    """Decompress a gzip file."""
    json_mode = args.json
    input_path = args.file
    output_path = args.output

    if not os.path.isfile(input_path):
        _die(f"File not found: {input_path}", json_mode)

    if not input_path.endswith(".gz"):
        _die(f"Not a gzip file (missing .gz extension): {input_path}", json_mode)

    # Verify it's actually a gzip file
    try:
        with open(input_path, "rb") as f:
            magic = f.read(2)
            if magic != b"\x1f\x8b":
                _die(f"Not a gzip file (invalid magic bytes): {input_path}", json_mode)
    except Exception as e:
        _die(f"Cannot read file: {e}", json_mode)

    if output_path is None:
        output_path = input_path[:-3]  # strip .gz
        if not output_path:
            _die(f"Cannot derive output path from: {input_path}", json_mode)

    if os.path.exists(output_path):
        _die(f"Output file already exists: {output_path}", json_mode)

    try:
        with gzip.open(input_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                while True:
                    chunk = f_in.read(65536)
                    if not chunk:
                        break
                    f_out.write(chunk)
    except gzip.BadGzipFile:
        _die(f"Corrupt gzip file: {input_path}", json_mode)
    except Exception as e:
        _die(f"Decompression failed: {e}", json_mode)

    output_size = os.path.getsize(output_path)

    result = {
        "success": True,
        "input_file": input_path,
        "output_file": output_path,
        "output_size": output_size,
    }
    _output(result, json_mode)


def cmd_inspect(args):
    """Inspect gzip file metadata."""
    json_mode = args.json
    input_path = args.file

    if not os.path.isfile(input_path):
        _die(f"File not found: {input_path}", json_mode)

    # Verify gzip magic bytes
    try:
        with open(input_path, "rb") as f:
            magic = f.read(2)
            if magic != b"\x1f\x8b":
                _die(f"Not a gzip file (invalid magic bytes): {input_path}", json_mode)
    except Exception as e:
        _die(f"Cannot read file: {e}", json_mode)

    compressed_size = os.path.getsize(input_path)
    mtime = _parse_gzip_mtime(input_path)

    # Determine original (uncompressed) size
    # The gzip format stores the original size modulo 2^32 in the last 4 bytes.
    # For files > 4 GB this wraps; we read it anyway as a best-effort value.
    try:
        with gzip.open(input_path, "rb") as f:
            # Read all data to determine size (only reliable way for full accuracy)
            original_size = 0
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                original_size += len(chunk)
    except gzip.BadGzipFile:
        _die(f"Corrupt gzip file: {input_path}", json_mode)
    except Exception as e:
        _die(f"Inspection failed: {e}", json_mode)

    ratio = (compressed_size / original_size * 100) if original_size > 0 else 0.0

    mtime_str = None
    if mtime is not None:
        import datetime
        mtime_str = datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    result = {
        "success": True,
        "file": input_path,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": f"{ratio:.1f}%",
        "modification_time": mtime_str if mtime_str else "not set",
    }
    _output(result, json_mode)


def cmd_test(args):
    """Test gzip file integrity."""
    json_mode = args.json
    input_path = args.file

    if not os.path.isfile(input_path):
        _die(f"File not found: {input_path}", json_mode)

    # Check magic bytes first
    try:
        with open(input_path, "rb") as f:
            magic = f.read(2)
            if magic != b"\x1f\x8b":
                _die(f"Not a gzip file (invalid magic bytes): {input_path}", json_mode)
    except Exception as e:
        _die(f"Cannot read file: {e}", json_mode)

    # Attempt full decompression to verify integrity
    try:
        with gzip.open(input_path, "rb") as f:
            while f.read(65536):
                pass
    except gzip.BadGzipFile as e:
        _die(f"Integrity check failed: {e}", json_mode)
    except Exception as e:
        _die(f"Integrity check failed: {e}", json_mode)

    result = {
        "success": True,
        "file": input_path,
        "integrity": "OK",
    }
    _output(result, json_mode)


def main():
    parser = argparse.ArgumentParser(
        prog="gzip_toolkit",
        description="Compress, decompress, inspect, and test gzip files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")

    # compress
    p_compress = subparsers.add_parser("compress", help="Compress a file to gzip format")
    p_compress.add_argument("--file", required=True, help="Input file path")
    p_compress.add_argument("--output", default=None, help="Output file path (default: INPUT.gz)")
    p_compress.add_argument("--level", type=int, default=6, help="Compression level 1-9 (default: 6)")
    p_compress.add_argument("--json", action="store_true", help="Output results as JSON")

    # decompress
    p_decompress = subparsers.add_parser("decompress", help="Decompress a gzip file")
    p_decompress.add_argument("--file", required=True, help="Input gzip file path")
    p_decompress.add_argument("--output", default=None, help="Output file path (default: strip .gz)")
    p_decompress.add_argument("--json", action="store_true", help="Output results as JSON")

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect gzip file metadata")
    p_inspect.add_argument("--file", required=True, help="Input gzip file path")
    p_inspect.add_argument("--json", action="store_true", help="Output results as JSON")

    # test
    p_test = subparsers.add_parser("test", help="Test gzip file integrity")
    p_test.add_argument("--file", required=True, help="Input gzip file path")
    p_test.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    commands = {
        "compress": cmd_compress,
        "decompress": cmd_decompress,
        "inspect": cmd_inspect,
        "test": cmd_test,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
