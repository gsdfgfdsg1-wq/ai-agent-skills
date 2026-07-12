#!/usr/bin/env python3
"""MIME Type Checker — detect file MIME types from content and extension.

Zero-dependency tool using only Python stdlib modules.
"""

import argparse
import json
import mimetypes
import os
import struct
import sys

# ---------------------------------------------------------------------------
# Magic-byte signature database
# ---------------------------------------------------------------------------
# Each entry: (byte_offset, signature_bytes, mime_type, description)
MAGIC_SIGNATURES = [
    # Images
    (0, b"%PDF", "application/pdf", "PDF document"),
    (0, b"\x89PNG\r\n\x1a\n", "image/png", "PNG image"),
    (0, b"\xff\xd8\xff", "image/jpeg", "JPEG image"),
    (0, b"GIF87a", "image/gif", "GIF image (87a)"),
    (0, b"GIF89a", "image/gif", "GIF image (89a)"),
    (0, b"RIFF", "image/webp", "WebP image (RIFF container)"),  # refined below
    (0, b"BM", "image/bmp", "BMP image"),
    (0, b"\x00\x00\x01\x00", "image/x-icon", "ICO image"),
    # Archives
    (0, b"PK\x03\x04", "application/zip", "ZIP archive"),
    (0, b"PK\x05\x06", "application/zip", "ZIP archive (empty)"),
    (0, b"Rar!\x1a\x07\x00", "application/x-rar-compressed", "RAR archive (v4)"),
    (0, b"Rar!\x1a\x07\x01", "application/x-rar-compressed", "RAR archive (v5)"),
    (0, b"\x37\x7a\xbc\xaf\x27\x1c", "application/x-7z-compressed", "7z archive"),
    (0, b"BZh", "application/x-bzip2", "BZip2 archive"),
    (0, b"\x1f\x8b", "application/gzip", "GZIP archive"),
    (0, b"\xfd\x37\x7a\x58\x5a\x00", "application/x-xz", "XZ archive"),
    # Documents
    (0, b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "application/msword", "MS Office (OLE2)"),
    # Audio/Video
    (0, b"ftyp", "video/mp4", "MP4 video"),  # offset 4, handled separately
    (0, b"\x1a\x45\xdf\xa3", "video/webm", "WebM/Matroska"),
    (0, b"ID3", "audio/mpeg", "MP3 audio (ID3 tag)"),
    (0, b"\xff\xfb", "audio/mpeg", "MP3 audio"),
    (0, b"\xff\xf3", "audio/mpeg", "MP3 audio"),
    (0, b"\xff\xf2", "audio/mpeg", "MP3 audio"),
    (0, b"OggS", "audio/ogg", "OGG audio"),
    (0, b"fLaC", "audio/flac", "FLAC audio"),
    (0, b"RIFF", "audio/wav", "WAV audio"),  # refined below
    # Data
    (0, b"SQLite format 3\x00", "application/x-sqlite3", "SQLite database"),
]

# Maximum bytes we need to read for any signature check
MAX_MAGIC_BYTES = 32


def _detect_by_magic(filepath):
    """Detect MIME type by reading magic bytes from the file content.

    Returns (mime_type, description) or (None, None).
    """
    try:
        with open(filepath, "rb") as f:
            header = f.read(MAX_MAGIC_BYTES)
    except (OSError, IOError):
        return None, None

    if len(header) < 2:
        return None, None

    # --- Check specific signatures first (offset-based) ---
    for offset, sig, mime, desc in MAGIC_SIGNATURES:
        if offset == 0 and header.startswith(sig):
            # RIFF container: differentiate WebP vs WAV vs AVI
            if sig == b"RIFF" and len(header) >= 12:
                riff_type = header[8:12]
                if riff_type == b"WEBP":
                    return "image/webp", "WebP image"
                elif riff_type == b"WAVE":
                    return "audio/wav", "WAV audio"
                elif riff_type == b"AVI ":
                    return "video/avi", "AVI video"
                else:
                    return "application/octet-stream", f"RIFF container ({riff_type!r})"
            return mime, desc

    # MP4 ftyp box at offset 4
    if len(header) >= 8 and header[4:8] == b"ftyp":
        return "video/mp4", "MP4 video"

    # --- Text-based heuristics (check if content looks like text) ---
    try:
        text_sample = header.decode("utf-8", errors="strict")
    except (UnicodeDecodeError, ValueError):
        # Not valid UTF-8 — treat as unknown binary
        return "application/octet-stream", "Unknown binary data"

    stripped = text_sample.lstrip()
    lower = stripped.lower()

    # XML
    if lower.startswith("<?xml"):
        # Check for specific XML-based formats
        if "<svg" in lower[:200]:
            return "image/svg+xml", "SVG image"
        if "<xhtml" in lower[:200] or "xmlns:xhtml" in lower[:300]:
            return "application/xhtml+xml", "XHTML document"
        return "application/xml", "XML document"

    # HTML
    if lower.startswith("<!doctype html") or lower.startswith("<html"):
        return "text/html", "HTML document"

    # JSON (starts with { or [)
    if stripped and stripped[0] in "{[":
        return "application/json", "JSON data"

    # Shell scripts
    if stripped.startswith("#!"):
        if "python" in lower[:80]:
            return "text/x-python", "Python script"
        if "bash" in lower[:80] or "sh" in lower[:80]:
            return "text/x-shellscript", "Shell script"
        if "node" in lower[:80]:
            return "text/javascript", "JavaScript (Node.js)"
        if "perl" in lower[:80]:
            return "text/x-perl", "Perl script"
        if "ruby" in lower[:80]:
            return "text/x-ruby", "Ruby script"
        return "text/x-shellscript", "Script with shebang"

    # General text
    return "text/plain", "Plain text"


def _detect_by_extension(filepath):
    """Detect MIME type using the file extension via the mimetypes module.

    Returns (mime_type, description) or (None, None).
    """
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type:
        return mime_type, f"Extension: {os.path.splitext(filepath)[1]}"
    return None, None


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_detect(args):
    """Handle the 'detect' subcommand."""
    filepath = args.file

    if not os.path.exists(filepath):
        _error(f"File not found: {filepath}")

    if not os.path.isfile(filepath):
        _error(f"Not a regular file: {filepath}")

    method = args.method
    results = {}

    if method in ("extension", "both"):
        ext_mime, ext_desc = _detect_by_extension(filepath)
        results["extension"] = {"mime": ext_mime, "description": ext_desc}

    if method in ("content", "both"):
        content_mime, content_desc = _detect_by_magic(filepath)
        results["content"] = {"mime": content_mime, "description": content_desc}

    # Determine best/overall result
    if method == "both":
        # Prefer content-based if available and more specific than extension
        content_mime = results.get("content", {}).get("mime")
        ext_mime = results.get("extension", {}).get("mime")

        if content_mime and ext_mime:
            if content_mime == ext_mime:
                best_mime = content_mime
                confidence = "high"
            elif content_mime == "application/octet-stream" and ext_mime:
                best_mime = ext_mime
                confidence = "medium"
            elif ext_mime == "application/octet-stream" and content_mime:
                best_mime = content_mime
                confidence = "medium"
            elif content_mime.startswith("text/") and ext_mime and not ext_mime.startswith("text/"):
                # Extension is more specific (e.g., .py -> text/x-python vs text/plain)
                best_mime = ext_mime
                confidence = "medium"
            else:
                best_mime = content_mime
                confidence = "medium"
        else:
            best_mime = content_mime or ext_mime
            confidence = "low" if best_mime == "application/octet-stream" else "medium"
    else:
        key = "content" if method == "content" else "extension"
        best_mime = results.get(key, {}).get("mime")
        confidence = "high" if best_mime and best_mime != "application/octet-stream" else "low"

    if args.json:
        output = {
            "file": os.path.abspath(filepath),
            "method": method,
            "results": results,
            "best_mime": best_mime,
            "confidence": confidence,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"File:       {os.path.abspath(filepath)}")
        print(f"Method:     {method}")
        if "extension" in results:
            m = results["extension"]["mime"] or "unknown"
            print(f"Extension:  {m}")
        if "content" in results:
            m = results["content"]["mime"] or "unknown"
            print(f"Content:    {m}")
        print(f"Best match: {best_mime or 'unknown'}")
        print(f"Confidence: {confidence}")


def cmd_lookup(args):
    """Handle the 'lookup' subcommand."""
    ext = args.extension.lstrip(".")

    # Initialize mimetypes to ensure common types are loaded
    mimetypes.init()

    # Try both with and without dot
    mime_type = mimetypes.types_map.get(f".{ext}")
    if not mime_type:
        # Search through all known types
        for key, value in mimetypes.types_map.items():
            if key.lstrip(".") == ext:
                mime_type = value
                break

    if not mime_type:
        _error(f"Unknown extension: .{ext}")

    if args.json:
        output = {
            "extension": ext,
            "mime_type": mime_type,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Extension: .{ext}")
        print(f"MIME type: {mime_type}")


def cmd_ext(args):
    """Handle the 'ext' subcommand."""
    mime_type = args.mime_type

    # Initialize mimetypes
    mimetypes.init()

    extensions = mimetypes.guess_all_extensions(mime_type, strict=False)

    if not extensions:
        # Try case-insensitive search
        lower = mime_type.lower()
        for key, value in mimetypes.types_map.items():
            if value.lower() == lower:
                if key not in extensions:
                    extensions.append(key)

    if not extensions:
        _error(f"Unknown MIME type: {mime_type}")

    # Normalize: remove leading dots, deduplicate, sort
    ext_list = sorted({e.lstrip(".") for e in extensions})

    if args.json:
        output = {
            "mime_type": mime_type,
            "extensions": ext_list,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"MIME type:  {mime_type}")
        print(f"Extensions: {', '.join(ext_list)}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _error(message):
    """Print error message and exit with code 1."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="mime_type_checker",
        description="Detect file MIME types from content and extension with a built-in mapping database.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # --- detect ---
    detect_parser = subparsers.add_parser(
        "detect",
        help="Detect MIME type of a file",
        description="Detect the MIME type of a file using extension, content magic bytes, or both.",
    )
    detect_parser.add_argument(
        "--file",
        required=True,
        help="Path to the file to detect",
    )
    detect_parser.add_argument(
        "--method",
        choices=["content", "extension", "both"],
        default="both",
        help="Detection method (default: both)",
    )
    detect_parser.add_argument(
        "--json",
        action="store_true",
        dest="json",
        help="Output result as JSON",
    )

    # --- lookup ---
    lookup_parser = subparsers.add_parser(
        "lookup",
        help="Lookup MIME type by extension",
        description="Look up the MIME type for a given file extension.",
    )
    lookup_parser.add_argument(
        "-s",
        dest="extension",
        required=True,
        help='File extension without leading dot (e.g., "py", "json")',
    )
    lookup_parser.add_argument(
        "--json",
        action="store_true",
        dest="json",
        help="Output result as JSON",
    )

    # --- ext ---
    ext_parser = subparsers.add_parser(
        "ext",
        help="Find extensions for a MIME type",
        description="Find all known file extensions for a given MIME type.",
    )
    ext_parser.add_argument(
        "-s",
        dest="mime_type",
        required=True,
        help='MIME type string (e.g., "application/json")',
    )
    ext_parser.add_argument(
        "--json",
        action="store_true",
        dest="json",
        help="Output result as JSON",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    dispatch = {
        "detect": cmd_detect,
        "lookup": cmd_lookup,
        "ext": cmd_ext,
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
