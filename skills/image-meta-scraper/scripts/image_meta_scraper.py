#!/usr/bin/env python3
"""image-meta-scraper — extract image metadata without external dependencies.

Usage:
    python image_meta_scraper.py PATH [PATH ...] [--json] [--top N] [--no-exif]

Reads JPEG, PNG, GIF, BMP, WebP headers natively for dimensions and basic EXIF.
"""

import argparse
import json
import os
import struct
import sys

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


def _read_png_size(data):
    """Read PNG dimensions from IHDR chunk."""
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    width = struct.unpack(">I", data[16:20])[0]
    height = struct.unpack(">I", data[20:24])[0]
    bit_depth = data[24]
    color_type = data[25]
    return {"width": width, "height": height, "bit_depth": bit_depth, "color_type": color_type}


def _read_jpeg_size(data):
    """Read JPEG dimensions from SOF marker."""
    if len(data) < 4 or data[:2] != b'\xff\xd8':
        return None
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF0, SOF1, SOF2 markers
        if marker in (0xC0, 0xC1, 0xC2):
            if i + 9 < len(data):
                height = struct.unpack(">H", data[i+5:i+7])[0]
                width = struct.unpack(">H", data[i+7:i+9])[0]
                return {"width": width, "height": height, "bit_depth": 8}
        # Skip to next marker
        if marker in (0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9):
            i += 2
        elif marker == 0xDA:  # SOS — image data starts
            break
        else:
            if i + 3 < len(data):
                length = struct.unpack(">H", data[i+2:i+4])[0]
                i += 2 + length
            else:
                break
    return None


def _read_gif_size(data):
    """Read GIF dimensions from header."""
    if len(data) < 10:
        return None
    if data[:6] not in (b'GIF87a', b'GIF89a'):
        return None
    width = struct.unpack("<H", data[6:8])[0]
    height = struct.unpack("<H", data[8:10])[0]
    packed = data[10]
    bit_depth = (packed & 0x07) + 1
    return {"width": width, "height": height, "bit_depth": bit_depth}


def _read_bmp_size(data):
    """Read BMP dimensions from header."""
    if len(data) < 26 or data[:2] != b'BM':
        return None
    width = struct.unpack("<i", data[18:22])[0]
    height = abs(struct.unpack("<i", data[22:26])[0])
    bit_depth = struct.unpack("<H", data[28:30])[0]
    return {"width": width, "height": height, "bit_depth": bit_depth}


def _read_webp_size(data):
    """Read WebP dimensions from header."""
    if len(data) < 30 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return None
    chunk = data[12:16]
    if chunk == b'VP8 ':
        # Lossy
        if len(data) >= 30:
            width = struct.unpack("<H", data[26:28])[0] & 0x3FFF
            height = struct.unpack("<H", data[28:30])[0] & 0x3FFF
            return {"width": width, "height": height, "bit_depth": 8}
    elif chunk == b'VP8L':
        # Lossless
        if len(data) >= 25:
            bits = struct.unpack("<I", data[21:25])[0]
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            return {"width": width, "height": height, "bit_depth": 8}
    return None


def _parse_exif(data):
    """Parse basic EXIF data from JPEG file."""
    if data[:2] != b'\xff\xd8':
        return {}
    # Find APP1 marker (0xFFE1)
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0xE1:  # APP1
            length = struct.unpack(">H", data[i+2:i+4])[0]
            exif_data = data[i+4:i+2+length]
            return _parse_exif_app1(exif_data)
        elif marker == 0xDA:
            break
        elif marker in (0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9):
            i += 2
        else:
            if i + 3 < len(data):
                length = struct.unpack(">H", data[i+2:i+4])[0]
                i += 2 + length
            else:
                break
    return {}


def _parse_exif_app1(data):
    """Parse EXIF APP1 data for key fields."""
    result = {}
    if not data.startswith(b'Exif\x00\x00'):
        return result
    tiff = data[6:]

    if len(tiff) < 14:
        return result

    # Byte order
    if tiff[:2] == b'II':
        endian = '<'
    elif tiff[:2] == b'MM':
        endian = '>'
    else:
        return result

    # IFD0 offset
    ifd0_offset = struct.unpack(endian + "I", tiff[4:8])[0]

    def read_ifd(offset):
        if offset + 2 > len(tiff):
            return {}
        entries = {}
        count = struct.unpack(endian + "H", tiff[offset:offset+2])[0]
        for j in range(count):
            entry_offset = offset + 2 + j * 12
            if entry_offset + 12 > len(tiff):
                break
            tag = struct.unpack(endian + "H", tiff[entry_offset:entry_offset+2])[0]
            fmt = struct.unpack(endian + "H", tiff[entry_offset+2:entry_offset+4])[0]
            count_val = struct.unpack(endian + "I", tiff[entry_offset+4:entry_offset+8])[0]
            value_offset = entry_offset + 8

            # Known tags
            tag_names = {
                0x010F: "Make",
                0x0110: "Model",
                0x0112: "Orientation",
                0x0132: "DateTime",
                0x8769: "ExifIFDPointer",
                0x8825: "GPSInfoPointer",
            }
            if tag not in tag_names:
                continue

            name = tag_names[tag]

            if tag == 0x8769 or tag == 0x8825:
                # Pointer to sub-IFD
                ptr = struct.unpack(endian + "I", tiff[value_offset:value_offset+4])[0]
                sub = read_ifd(ptr)
                if tag == 0x8825:
                    entries["GPS"] = sub
                else:
                    entries.update(sub)
                continue

            # Read string values
            if fmt == 2:  # ASCII
                if count_val <= 4:
                    val = tiff[value_offset:value_offset+count_val].decode("ascii", errors="replace").rstrip('\x00')
                else:
                    actual_offset = struct.unpack(endian + "I", tiff[value_offset:value_offset+4])[0]
                    if actual_offset + count_val <= len(tiff):
                        val = tiff[actual_offset:actual_offset+count_val].decode("ascii", errors="replace").rstrip('\x00')
                    else:
                        val = None
                if val:
                    entries[name] = val
            elif fmt == 3:  # SHORT
                entries[name] = struct.unpack(endian + "H", tiff[value_offset:value_offset+2])[0]

        return entries

    result = read_ifd(ifd0_offset)
    return result


def get_image_metadata(filepath, include_exif=True):
    """Extract metadata from an image file."""
    result = {"file": filepath}

    try:
        file_size = os.path.getsize(filepath)
        result["file_size"] = file_size
        result["file_size_human"] = _human_size(file_size)
    except OSError:
        result["error"] = "Cannot read file"
        return result

    ext = os.path.splitext(filepath)[1].lower()
    result["extension"] = ext

    try:
        with open(filepath, "rb") as f:
            header = f.read(65536)  # Read enough for headers and basic EXIF
    except Exception as e:
        result["error"] = str(e)
        return result

    dim_info = None
    if ext in (".jpg", ".jpeg"):
        result["format"] = "JPEG"
        dim_info = _read_jpeg_size(header)
        if include_exif:
            result["exif"] = _parse_exif(header)
    elif ext == ".png":
        result["format"] = "PNG"
        dim_info = _read_png_size(header)
    elif ext == ".gif":
        result["format"] = "GIF"
        dim_info = _read_gif_size(header)
    elif ext == ".bmp":
        result["format"] = "BMP"
        dim_info = _read_bmp_size(header)
    elif ext == ".webp":
        result["format"] = "WebP"
        dim_info = _read_webp_size(header)
    else:
        result["format"] = "Unknown"

    if dim_info:
        result.update(dim_info)

    return result


def _human_size(n):
    """Convert bytes to human-readable size."""
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in IMAGE_EXTS:
                        yield os.path.join(root, fn)


def main():
    ap = argparse.ArgumentParser(
        description="Extract image metadata without external dependencies."
    )
    ap.add_argument("paths", nargs="+", help="image files or directories to scan")
    ap.add_argument("--json", action="store_true", help="output JSON results")
    ap.add_argument("--top", type=int, default=0,
                    help="limit to top N largest images")
    ap.add_argument("--no-exif", action="store_true",
                    help="skip EXIF parsing (faster)")
    args = ap.parse_args()

    results = []
    for fp in _iter_targets(args.paths):
        meta = get_image_metadata(fp, include_exif=not args.no_exif)
        results.append(meta)

    # Sort by file size descending
    results.sort(key=lambda x: x.get("file_size", 0), reverse=True)

    if args.top > 0:
        results = results[:args.top]

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            if "error" in r:
                print(f"[ERROR] {r['file']}: {r['error']}")
                continue
            dims = f"{r.get('width', '?')}x{r.get('height', '?')}" if r.get("width") else "unknown dimensions"
            fmt = r.get("format", "?")
            size = r.get("file_size_human", "?")
            print(f"{r['file']}: {fmt} {dims} {size}")
            exif = r.get("exif", {})
            if exif:
                for k, v in exif.items():
                    if isinstance(v, dict):
                        print(f"  {k}: {json.dumps(v)}")
                    else:
                        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
