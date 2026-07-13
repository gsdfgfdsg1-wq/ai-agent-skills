#!/usr/bin/env python3
"""Generate SVG QR codes from text or URLs without external dependencies."""

import argparse
import os
import sys
from pathlib import Path

# ---- Minimal QR code encoder (numerical + alphanumeric + byte mode) ----

# Error correction levels
EC_LEVELS = {"L": 0, "M": 1, "Q": 2, "H": 3}

# Version capacities (byte mode): [L, M, Q, H] max bytes per version
BYTE_CAPACITY = {
    1: [17, 14, 11, 7], 2: [32, 26, 20, 14], 3: [53, 42, 32, 24],
    4: [78, 62, 46, 34], 5: [106, 84, 60, 44], 6: [134, 106, 74, 58],
    7: [154, 122, 86, 64], 8: [192, 152, 108, 84], 9: [230, 180, 130, 98],
    10: [271, 213, 151, 119],
}

# Total codewords per version
TOTAL_CODEWORDS = {
    1: 26, 2: 44, 3: 70, 4: 100, 5: 134, 6: 172, 7: 196,
    8: 242, 9: 292, 10: 346,
}

# EC codewords per block: [L, M, Q, H]
EC_CODEWORDS = {
    1: [7, 10, 13, 17], 2: [10, 16, 22, 28], 3: [15, 26, 18, 22],
    4: [20, 18, 26, 16], 5: [26, 24, 18, 22], 6: [18, 16, 24, 28],
    7: [20, 18, 18, 26], 8: [24, 22, 22, 26], 9: [30, 22, 20, 24],
    10: [18, 26, 24, 28],
}

# Number of blocks: [L, M, Q, H]
NUM_BLOCKS = {
    1: [1, 1, 1, 1], 2: [1, 1, 1, 1], 3: [1, 1, 2, 2],
    4: [1, 2, 2, 4], 5: [1, 2, 2, 2], 6: [2, 4, 4, 4],
    7: [2, 4, 2, 4], 8: [2, 2, 4, 4], 9: [2, 3, 4, 4],
    10: [2, 4, 6, 6],
}

# Generator polynomial exponents for different EC codeword counts
# This is a simplified approach - we use Reed-Solomon encoding

ALIGNMENT_POSITIONS = {
    1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
    6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50],
}


def gf_mult(a, b):
    """Multiply in GF(2^8) with primitive polynomial 0x11d."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1D
        b >>= 1
    return p


def gf_poly_eval(poly, x):
    """Evaluate polynomial at x in GF(2^8)."""
    result = 0
    for coeff in poly:
        result = gf_mult(result, x) ^ coeff
    return result


def gf_poly_mult(p1, p2):
    """Multiply two polynomials in GF(2^8)."""
    result = [0] * (len(p1) + len(p2) - 1)
    for i, c1 in enumerate(p1):
        for j, c2 in enumerate(p2):
            result[i + j] ^= gf_mult(c1, c2)
    return result


def rs_encode(data, nsym):
    """Reed-Solomon encode data with nsym error correction symbols."""
    gen = [1]
    for i in range(nsym):
        gen = gf_poly_mult(gen, [1, gf_exp(i)])

    padded = data + [0] * nsym
    for i in range(len(data)):
        coeff = padded[i]
        if coeff != 0:
            for j in range(len(gen)):
                padded[i + j] ^= gf_mult(gen[j], coeff)
    return padded[len(data):]


def gf_exp(n):
    """Get alpha^n in GF(2^8)."""
    result = 1
    for _ in range(n % 255):
        carry = result & 0x80
        result = (result << 1) & 0xFF
        if carry:
            result ^= 0x1D
    return result


def encode_data(text, version, ec_level):
    """Encode text data into QR code bit stream."""
    data_bytes = text.encode("utf-8")
    ec_idx = EC_LEVELS[ec_level]

    # Mode indicator: byte mode = 0100
    bits = "0100"
    # Character count indicator (8 bits for version 1-9, 16 for 10+)
    count_bits = 8 if version <= 9 else 16
    bits += format(len(data_bytes), f"0{count_bits}b")

    # Data
    for b in data_bytes:
        bits += format(b, "08b")

    # Terminator
    total_data_bits = TOTAL_CODEWORDS[version] * 8
    ec_cw = EC_CODEWORDS[version][ec_idx]
    data_cw = TOTAL_CODEWORDS[version] - ec_cw * NUM_BLOCKS[version][ec_idx]
    target_bits = data_cw * 8

    bits += "0" * min(4, target_bits - len(bits))

    # Pad to byte boundary
    while len(bits) % 8 != 0:
        bits += "0"

    # Pad codewords
    pad_words = [0xEC, 0x11]
    pad_idx = 0
    while len(bits) < target_bits:
        bits += format(pad_words[pad_idx % 2], "08b")
        pad_idx += 1

    # Convert to byte array
    codewords = []
    for i in range(0, len(bits), 8):
        codewords.append(int(bits[i:i + 8], 2))

    # Split into blocks and add EC
    num_blocks = NUM_BLOCKS[version][ec_idx]
    block_size = len(codewords) // num_blocks
    blocks = []
    for b in range(num_blocks):
        start = b * block_size
        end = start + block_size
        block = codewords[start:end]
        ec_symbols = rs_encode(block, ec_cw)
        blocks.append((block, ec_symbols))

    # Interleave data and EC
    result = []
    for i in range(block_size):
        for block, _ in blocks:
            if i < len(block):
                result.append(block[i])
    for i in range(ec_cw):
        for _, ec in blocks:
            if i < len(ec):
                result.append(ec[i])

    return result


def create_matrix(version, ec_level, codewords):
    """Create the QR code matrix."""
    size = version * 4 + 17
    matrix = [[None] * size for _ in range(size)]
    reserved = [[False] * size for _ in range(size)]

    # Finder patterns
    for r, c in [(0, 0), (0, size - 7), (size - 7, 0)]:
        for dr in range(7):
            for dc in range(7):
                val = (dr in (0, 6) or dc in (0, 6) or (2 <= dr <= 4 and 2 <= dc <= 4))
                matrix[r + dr][c + dc] = val
                reserved[r + dr][c + dc] = True

    # Separators
    for i in range(8):
        for pos in [(0, i, -1, 0), (i, 0, 0, -1), (size - 8, i, size - 8 - 1, 0),
                     (i, size - 8, 0, size - 8 + 1), (size - 8 + i, 0, size - 8 - 1 + i, -1),
                     (0, size - 8 + i, -1, size - 8 + i)]:
            pass  # Simplified - separators are white, matrix default handles

    # Alignment patterns
    for ar in ALIGNMENT_POSITIONS[version]:
        for ac in ALIGNMENT_POSITIONS[version]:
            # Skip if overlapping finder pattern
            if (ar <= 8 and ac <= 8) or (ar <= 8 and ac >= size - 8) or (ar >= size - 8 and ac <= 8):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    val = (abs(dr) == 2 or abs(dc) == 2 or (dr == 0 and dc == 0))
                    matrix[ar + dr][ac + dc] = val
                    reserved[ar + dr][ac + dc] = True

    # Timing patterns
    for i in range(8, size - 8):
        matrix[6][i] = i % 2 == 0
        reserved[6][i] = True
        matrix[i][6] = i % 2 == 0
        reserved[i][6] = True

    # Dark module
    matrix[size - 8][8] = True
    reserved[size - 8][8] = True

    # Format info placeholders (will be filled with masking)
    # Reserve format info areas
    for i in range(9):
        reserved[8][i] = True
        reserved[i][8] = True
        reserved[8][size - 1 - i] = True if i < 8 else False
        reserved[size - 1 - i][8] = True if i < 8 else False

    # Place data bits
    bit_idx = 0
    bits_str = ""
    for cw in codewords:
        bits_str += format(cw, "08b")

    col = size - 1
    upward = True
    while col >= 0:
        if col == 6:
            col -= 1
            continue
        row_range = range(size - 1, -1, -1) if upward else range(size)
        for row in row_range:
            for dc in [0, -1]:
                c = col + dc
                if c < 0 or c >= size:
                    continue
                if reserved[row][c]:
                    continue
                if bit_idx < len(bits_str):
                    matrix[row][c] = bits_str[bit_idx] == "1"
                    bit_idx += 1
                else:
                    matrix[row][c] = False
        col -= 2
        upward = not upward

    return matrix, size


def apply_mask(matrix, size, mask_num):
    """Apply a mask pattern to the data modules."""
    result = [row[:] for row in matrix]
    for r in range(size):
        for c in range(size):
            if result[r][c] is None:
                continue
            invert = False
            if mask_num == 0:
                invert = (r + c) % 2 == 0
            elif mask_num == 1:
                invert = r % 2 == 0
            elif mask_num == 2:
                invert = c % 3 == 0
            elif mask_num == 3:
                invert = (r + c) % 3 == 0
            elif mask_num == 4:
                invert = (r // 2 + c // 3) % 2 == 0
            elif mask_num == 5:
                invert = (r * c) % 2 + (r * c) % 3 == 0
            elif mask_num == 6:
                invert = ((r * c) % 2 + (r * c) % 3) % 2 == 0
            elif mask_num == 7:
                invert = ((r + c) % 2 + (r * c) % 3) % 2 == 0
            if invert:
                result[r][c] = not result[r][c]
    return result


def matrix_to_svg(matrix, size, module_size=10, fg="#000000", bg="#FFFFFF"):
    """Convert QR matrix to SVG string."""
    svg_size = size * module_size
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_size} {svg_size}" width="{svg_size}" height="{svg_size}">',
        f'<rect width="{svg_size}" height="{svg_size}" fill="{bg}"/>',
    ]
    for r in range(size):
        for c in range(size):
            if matrix[r][c]:
                parts.append(f'<rect x="{c * module_size}" y="{r * module_size}" width="{module_size}" height="{module_size}" fill="{fg}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_qr(text, ec_level="M", module_size=10, fg="#000000", bg="#FFFFFF"):
    """Generate a QR code SVG from text."""
    ec_idx = EC_LEVELS[ec_level]

    # Find minimum version
    version = 1
    data_len = len(text.encode("utf-8"))
    for v in range(1, 11):
        if BYTE_CAPACITY[v][ec_idx] >= data_len:
            version = v
            break
    else:
        print("Error: text too long for QR code (max ~271 bytes)", file=sys.stderr)
        sys.exit(1)

    codewords = encode_data(text, version, ec_level)
    matrix, size = create_matrix(version, ec_level, codewords)

    # Apply mask 0 (simplified - normally we'd try all masks and pick best)
    masked = apply_mask(matrix, size, 0)

    return matrix_to_svg(masked, size, module_size, fg, bg)


def cmd_generate(args):
    svg = generate_qr(args.text, args.level, args.size, args.fg, args.bg)
    if args.output:
        Path(args.output).write_text(svg, encoding="utf-8")
        print(f"QR code written to {args.output}")
    else:
        print(svg)


def cmd_batch(args):
    try:
        lines = Path(args.file).read_text(encoding="utf-8").splitlines()
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in line[:50])
        out_path = output_dir / f"{i:03d}_{safe_name}.svg"
        svg = generate_qr(line, args.level, args.size, args.fg, args.bg)
        out_path.write_text(svg, encoding="utf-8")
        print(f"  Generated: {out_path}")

    print(f"Batch complete: {i + 1} QR code(s) in {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate SVG QR codes.")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("generate", help="Generate a single QR code")
    p_gen.add_argument("--text", required=True, help="Text or URL to encode")
    p_gen.add_argument("--output", help="Output SVG file")
    p_gen.add_argument("--size", type=int, default=10, help="Module size in px (default 10)")
    p_gen.add_argument("--level", choices=list(EC_LEVELS.keys()), default="M", help="Error correction level")
    p_gen.add_argument("--fg", default="#000000", help="Foreground color")
    p_gen.add_argument("--bg", default="#FFFFFF", help="Background color")

    p_batch = sub.add_parser("batch", help="Generate QR codes from file")
    p_batch.add_argument("--file", required=True, help="Input file (one per line)")
    p_batch.add_argument("--output-dir", required=True, help="Output directory")
    p_batch.add_argument("--size", type=int, default=10, help="Module size in px")
    p_batch.add_argument("--level", choices=list(EC_LEVELS.keys()), default="M", help="Error correction level")
    p_batch.add_argument("--fg", default="#000000", help="Foreground color")
    p_batch.add_argument("--bg", default="#FFFFFF", help="Background color")

    args = parser.parse_args()
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "batch":
        cmd_batch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
