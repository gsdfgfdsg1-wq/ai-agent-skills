#!/usr/bin/env python3
"""unicode_info.py — Look up Unicode character information.

Subcommands:
  char      Info about one or more characters
  codepoint Info from a codepoint (U+XXXX or 0xXXXX)
  range     List characters in a codepoint range
  search    Search characters by name pattern
"""

import argparse
import json
import re
import sys
import unicodedata


# ---------------------------------------------------------------------------
# Unicode block detection
# ---------------------------------------------------------------------------

UNICODE_BLOCKS = [
    (0x0000, 0x007F, "Basic Latin"),
    (0x0080, 0x00FF, "Latin-1 Supplement"),
    (0x0100, 0x017F, "Latin Extended-A"),
    (0x0180, 0x024F, "Latin Extended-B"),
    (0x0250, 0x02AF, "IPA Extensions"),
    (0x02B0, 0x02FF, "Spacing Modifier Letters"),
    (0x0300, 0x036F, "Combining Diacritical Marks"),
    (0x0370, 0x03FF, "Greek and Coptic"),
    (0x0400, 0x04FF, "Cyrillic"),
    (0x0500, 0x052F, "Cyrillic Supplement"),
    (0x0530, 0x058F, "Armenian"),
    (0x0590, 0x05FF, "Hebrew"),
    (0x0600, 0x06FF, "Arabic"),
    (0x0700, 0x074F, "Syriac"),
    (0x0780, 0x07BF, "Thaana"),
    (0x0900, 0x097F, "Devanagari"),
    (0x0980, 0x09FF, "Bengali"),
    (0x0A00, 0x0A7F, "Gurmukhi"),
    (0x0A80, 0x0AFF, "Gujarati"),
    (0x0B00, 0x0B7F, "Oriya"),
    (0x0B80, 0x0BFF, "Tamil"),
    (0x0C00, 0x0C7F, "Telugu"),
    (0x0C80, 0x0CFF, "Kannada"),
    (0x0D00, 0x0D7F, "Malayalam"),
    (0x0D80, 0x0DFF, "Sinhala"),
    (0x0E00, 0x0E7F, "Thai"),
    (0x0E80, 0x0EFF, "Lao"),
    (0x0F00, 0x0FFF, "Tibetan"),
    (0x1000, 0x109F, "Myanmar"),
    (0x10A0, 0x10FF, "Georgian"),
    (0x1100, 0x11FF, "Hangul Jamo"),
    (0x1200, 0x137F, "Ethiopic"),
    (0x13A0, 0x13FF, "Cherokee"),
    (0x1400, 0x167F, "Unified Canadian Aboriginal Syllabics"),
    (0x1680, 0x169F, "Ogham"),
    (0x16A0, 0x16FF, "Runic"),
    (0x1700, 0x171F, "Tagalog"),
    (0x1720, 0x173F, "Hanunoo"),
    (0x1740, 0x175F, "Buhid"),
    (0x1760, 0x177F, "Tagbanwa"),
    (0x1780, 0x17FF, "Khmer"),
    (0x1800, 0x18AF, "Mongolian"),
    (0x1900, 0x194F, "Limbu"),
    (0x1950, 0x197F, "Tai Le"),
    (0x1980, 0x19DF, "New Tai Lue"),
    (0x19E0, 0x19FF, "Khmer Symbols"),
    (0x1A00, 0x1A1F, "Buginese"),
    (0x1B00, 0x1B7F, "Balinese"),
    (0x1D00, 0x1D7F, "Phonetic Extensions"),
    (0x1D80, 0x1DBF, "Phonetic Extensions Supplement"),
    (0x1DC0, 0x1DFF, "Combining Diacritical Marks Supplement"),
    (0x1E00, 0x1EFF, "Latin Extended Additional"),
    (0x1F00, 0x1FFF, "Greek Extended"),
    (0x2000, 0x206F, "General Punctuation"),
    (0x2070, 0x209F, "Superscripts and Subscripts"),
    (0x20A0, 0x20CF, "Currency Symbols"),
    (0x20D0, 0x20FF, "Combining Diacritical Marks for Symbols"),
    (0x2100, 0x214F, "Letterlike Symbols"),
    (0x2150, 0x218F, "Number Forms"),
    (0x2190, 0x21FF, "Arrows"),
    (0x2200, 0x22FF, "Mathematical Operators"),
    (0x2300, 0x23FF, "Miscellaneous Technical"),
    (0x2400, 0x243F, "Control Pictures"),
    (0x2440, 0x245F, "Optical Character Recognition"),
    (0x2460, 0x24FF, "Enclosed Alphanumerics"),
    (0x2500, 0x257F, "Box Drawing"),
    (0x2580, 0x259F, "Block Elements"),
    (0x25A0, 0x25FF, "Geometric Shapes"),
    (0x2600, 0x26FF, "Miscellaneous Symbols"),
    (0x2700, 0x27BF, "Dingbats"),
    (0x27C0, 0x27EF, "Miscellaneous Mathematical Symbols-A"),
    (0x27F0, 0x27FF, "Supplemental Arrows-A"),
    (0x2800, 0x28FF, "Braille Patterns"),
    (0x2900, 0x297F, "Supplemental Arrows-B"),
    (0x2980, 0x29FF, "Miscellaneous Mathematical Symbols-B"),
    (0x2A00, 0x2AFF, "Supplemental Mathematical Operators"),
    (0x2B00, 0x2BFF, "Miscellaneous Symbols and Arrows"),
    (0x2C00, 0x2C5F, "Glagolitic"),
    (0x2C60, 0x2C7F, "Latin Extended-C"),
    (0x2C80, 0x2CFF, "Coptic"),
    (0x2D00, 0x2D2F, "Georgian Supplement"),
    (0x2D30, 0x2D7F, "Tifinagh"),
    (0x2DE0, 0x2DFF, "Cyrillic Extended-A"),
    (0x2E00, 0x2E7F, "Supplemental Punctuation"),
    (0x2E80, 0x2EFF, "CJK Radicals Supplement"),
    (0x2F00, 0x2FDF, "Kangxi Radicals"),
    (0x2FF0, 0x2FFF, "Ideographic Description Characters"),
    (0x3000, 0x303F, "CJK Symbols and Punctuation"),
    (0x3040, 0x309F, "Hiragana"),
    (0x30A0, 0x30FF, "Katakana"),
    (0x3100, 0x312F, "Bopomofo"),
    (0x3130, 0x318F, "Hangul Compatibility Jamo"),
    (0x3190, 0x319F, "Kanbun"),
    (0x31A0, 0x31BF, "Bopomofo Extended"),
    (0x31C0, 0x31EF, "CJK Strokes"),
    (0x31F0, 0x31FF, "Katakana Phonetic Extensions"),
    (0x3200, 0x32FF, "Enclosed CJK Letters and Months"),
    (0x3300, 0x33FF, "CJK Compatibility"),
    (0x3400, 0x4DBF, "CJK Unified Ideographs Extension A"),
    (0x4DC0, 0x4DFF, "Yijing Hexagram Symbols"),
    (0x4E00, 0x9FFF, "CJK Unified Ideographs"),
    (0xA000, 0xA48F, "Yi Syllables"),
    (0xA490, 0xA4CF, "Yi Radicals"),
    (0xA4D0, 0xA4FF, "Lisu"),
    (0xA500, 0xA63F, "Vai"),
    (0xA640, 0xA69F, "Cyrillic Extended-B"),
    (0xA700, 0xA71F, "Modifier Tone Letters"),
    (0xA720, 0xA7FF, "Latin Extended-D"),
    (0xA800, 0xA82F, "Syloti Nagri"),
    (0xA840, 0xA87F, "Phags-pa"),
    (0xA880, 0xA8DF, "Saurashtra"),
    (0xA900, 0xA92F, "Kayah Li"),
    (0xA930, 0xA95F, "Rejang"),
    (0xA960, 0xA97F, "Hangul Jamo Extended-A"),
    (0xA980, 0xA9DF, "Javanese"),
    (0xAA00, 0xAA5F, "Cham"),
    (0xAA60, 0xAA7F, "Myanmar Extended-A"),
    (0xAA80, 0xAADF, "Tai Viet"),
    (0xAB00, 0xAB2F, "Ethiopic Extended-A"),
    (0xABC0, 0xABFF, "Meetei Mayek"),
    (0xAC00, 0xD7AF, "Hangul Syllables"),
    (0xD800, 0xDB7F, "High Surrogates"),
    (0xDB80, 0xDBFF, "High Private Use Surrogates"),
    (0xDC00, 0xDFFF, "Low Surrogates"),
    (0xE000, 0xF8FF, "Private Use Area"),
    (0xF900, 0xFAFF, "CJK Compatibility Ideographs"),
    (0xFB00, 0xFB4F, "Alphabetic Presentation Forms"),
    (0xFB50, 0xFDFF, "Arabic Presentation Forms-A"),
    (0xFE00, 0xFE0F, "Variation Selectors"),
    (0xFE10, 0xFE1F, "Vertical Forms"),
    (0xFE20, 0xFE2F, "Combining Half Marks"),
    (0xFE30, 0xFE4F, "CJK Compatibility Forms"),
    (0xFE50, 0xFE6F, "Small Form Variants"),
    (0xFE70, 0xFEFF, "Arabic Presentation Forms-B"),
    (0xFF00, 0xFFEF, "Halfwidth and Fullwidth Forms"),
    (0xFFF0, 0xFFFF, "Specials"),
    (0x10000, 0x1007F, "Linear B Syllabary"),
    (0x10080, 0x100FF, "Linear B Ideograms"),
    (0x10100, 0x1013F, "Aegean Numbers"),
    (0x10140, 0x1018F, "Ancient Greek Numbers"),
    (0x10190, 0x101CF, "Ancient Symbols"),
    (0x101D0, 0x101FF, "Phaistos Disc"),
    (0x10280, 0x1029F, "Lycian"),
    (0x102A0, 0x102DF, "Carian"),
    (0x10300, 0x1032F, "Old Italic"),
    (0x10330, 0x1034F, "Gothic"),
    (0x10380, 0x1039F, "Ugaritic"),
    (0x103A0, 0x103DF, "Old Persian"),
    (0x10400, 0x1044F, "Deseret"),
    (0x10450, 0x1047F, "Shavian"),
    (0x10480, 0x104AF, "Osmanya"),
    (0x10800, 0x1083F, "Cypriot Syllabary"),
    (0x10840, 0x1085F, "Imperial Aramaic"),
    (0x10900, 0x1091F, "Phoenician"),
    (0x10920, 0x1093F, "Lydian"),
    (0x10A00, 0x10A5F, "Kharoshthi"),
    (0x10A60, 0x10A7F, "Old South Arabian"),
    (0x10B00, 0x10B3F, "Avestan"),
    (0x10B40, 0x10B5F, "Inscriptional Parthian"),
    (0x10B60, 0x10B7F, "Inscriptional Pahlavi"),
    (0x10C00, 0x10C4F, "Old Turkic"),
    (0x10E60, 0x10E7F, "Rumi Numeral Symbols"),
    (0x11000, 0x1107F, "Brahmi"),
    (0x11080, 0x110CF, "Kaithi"),
    (0x12000, 0x123FF, "Cuneiform"),
    (0x12400, 0x1247F, "Cuneiform Numbers and Punctuation"),
    (0x13000, 0x1342F, "Egyptian Hieroglyphs"),
    (0x16800, 0x16A3F, "Bamum"),
    (0x1B000, 0x1B0FF, "Kana Supplement"),
    (0x1D000, 0x1D0FF, "Byzantine Musical Symbols"),
    (0x1D100, 0x1D1FF, "Musical Symbols"),
    (0x1D200, 0x1D24F, "Ancient Greek Musical Notation"),
    (0x1D300, 0x1D35F, "Tai Xuan Jing Symbols"),
    (0x1D360, 0x1D37F, "Counting Rod Numerals"),
    (0x1D400, 0x1D7FF, "Mathematical Alphanumeric Symbols"),
    (0x1F000, 0x1F02F, "Mahjong Tiles"),
    (0x1F030, 0x1F09F, "Domino Tiles"),
    (0x1F0A0, 0x1F0FF, "Playing Cards"),
    (0x1F100, 0x1F1FF, "Enclosed Alphanumeric Supplement"),
    (0x1F200, 0x1F2FF, "Enclosed Ideographic Supplement"),
    (0x1F300, 0x1F5FF, "Miscellaneous Symbols and Pictographs"),
    (0x1F600, 0x1F64F, "Emoticons"),
    (0x1F680, 0x1F6FF, "Transport and Map Symbols"),
    (0x1F700, 0x1F77F, "Alchemical Symbols"),
    (0x1F780, 0x1F7FF, "Geometric Shapes Extended"),
    (0x1F800, 0x1F8FF, "Supplemental Arrows-C"),
    (0x1F900, 0x1F9FF, "Supplemental Symbols and Pictographs"),
    (0x20000, 0x2A6DF, "CJK Unified Ideographs Extension B"),
    (0x2A700, 0x2B73F, "CJK Unified Ideographs Extension C"),
    (0x2B740, 0x2B81F, "CJK Unified Ideographs Extension D"),
    (0x2F800, 0x2FA1F, "CJK Compatibility Ideographs Supplement"),
    (0xE0000, 0xE007F, "Tags"),
    (0xE0100, 0xE01EF, "Variation Selectors Supplement"),
    (0xF0000, 0xFFFFD, "Supplementary Private Use Area-A"),
    (0x100000, 0x10FFFD, "Supplementary Private Use Area-B"),
]


def get_unicode_block(codepoint):
    """Return the Unicode block name for a given codepoint."""
    for start, end, name in UNICODE_BLOCKS:
        if start <= codepoint <= end:
            return name
    return "Unknown"


# ---------------------------------------------------------------------------
# Character info helpers
# ---------------------------------------------------------------------------

CATEGORY_NAMES = {
    "Lu": "Letter, Uppercase",
    "Ll": "Letter, Lowercase",
    "Lt": "Letter, Titlecase",
    "Lm": "Letter, Modifier",
    "Lo": "Letter, Other",
    "Mn": "Mark, Nonspacing",
    "Mc": "Mark, Spacing Combining",
    "Me": "Mark, Enclosing",
    "Nd": "Number, Decimal Digit",
    "Nl": "Number, Letter",
    "No": "Number, Other",
    "Pc": "Punctuation, Connector",
    "Pd": "Punctuation, Dash",
    "Ps": "Punctuation, Open",
    "Pe": "Punctuation, Close",
    "Pi": "Punctuation, Initial Quote",
    "Pf": "Punctuation, Final Quote",
    "Po": "Punctuation, Other",
    "Sm": "Symbol, Math",
    "Sc": "Symbol, Currency",
    "Sk": "Symbol, Modifier",
    "So": "Symbol, Other",
    "Zs": "Separator, Space",
    "Zl": "Separator, Line",
    "Zp": "Separator, Paragraph",
    "Cc": "Other, Control",
    "Cf": "Other, Format",
    "Cs": "Other, Surrogate",
    "Co": "Other, Private Use",
    "Cn": "Other, Not Assigned",
}


def char_info(ch):
    """Build a dict with all info for a single character."""
    cp = ord(ch)
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = f"<unnamed U+{cp:04X}>"
    category = unicodedata.category(ch)
    bidirectional = unicodedata.bidirectional(ch)
    combining = unicodedata.combining(ch)
    block = get_unicode_block(cp)
    return {
        "character": ch,
        "codepoint": f"U+{cp:04X}",
        "name": name,
        "category": category,
        "category_name": CATEGORY_NAMES.get(category, category),
        "bidirectional": bidirectional,
        "combining_class": combining,
        "block": block,
        "decimal": cp,
        "hex": f"0x{cp:X}",
        "octal": f"0o{cp:o}",
    }


def format_char_info(info):
    """Format a single character info dict as a human-readable string."""
    lines = [
        f"Character:     {info['character']}",
        f"Codepoint:     {info['codepoint']}",
        f"Name:          {info['name']}",
        f"Category:      {info['category']} ({info['category_name']})",
        f"Bidirectional: {info['bidirectional']}",
        f"Combining:     {info['combining_class']}",
        f"Block:         {info['block']}",
        f"Decimal:       {info['decimal']}",
        f"Hex:           {info['hex']}",
        f"Octal:         {info['octal']}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Codepoint parsing
# ---------------------------------------------------------------------------

def parse_codepoint(s):
    """Parse a codepoint string like U+4E2D or 0x4E2D into an integer."""
    s = s.strip()
    m = re.match(r"^[Uu]\+([0-9A-Fa-f]{1,6})$", s)
    if m:
        return int(m.group(1), 16)
    m = re.match(r"^0[xX]([0-9A-Fa-f]{1,6})$", s)
    if m:
        return int(m.group(1), 16)
    raise ValueError(f"Invalid codepoint format: {s!r}  (expected U+XXXX or 0xXXXX)")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_char(args):
    """Handle the 'char' subcommand."""
    s = args.s
    if not s:
        print("Error: no character provided via -s", file=sys.stderr)
        sys.exit(1)
    results = [char_info(ch) for ch in s]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for i, info in enumerate(results):
            if i > 0:
                print()
            print(format_char_info(info))


def cmd_codepoint(args):
    """Handle the 'codepoint' subcommand."""
    raw = args.s
    if not raw:
        print("Error: no codepoint provided via -s", file=sys.stderr)
        sys.exit(1)
    try:
        cp = parse_codepoint(raw)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    if cp > 0x10FFFF:
        print(f"Error: codepoint {raw} is beyond Unicode range (max U+10FFFF)", file=sys.stderr)
        sys.exit(1)
    try:
        ch = chr(cp)
    except ValueError:
        print(f"Error: cannot create character from codepoint {raw}", file=sys.stderr)
        sys.exit(1)
    info = char_info(ch)
    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print(format_char_info(info))


def cmd_range(args):
    """Handle the 'range' subcommand."""
    try:
        cp_from = parse_codepoint(args.from_cp)
    except ValueError as e:
        print(f"Error: invalid --from value: {e}", file=sys.stderr)
        sys.exit(1)
    try:
        cp_to = parse_codepoint(args.to_cp)
    except ValueError as e:
        print(f"Error: invalid --to value: {e}", file=sys.stderr)
        sys.exit(1)
    if cp_from > cp_to:
        print("Error: --from must be <= --to", file=sys.stderr)
        sys.exit(1)
    if cp_to > 0x10FFFF:
        print(f"Error: --to is beyond Unicode range (max U+10FFFF)", file=sys.stderr)
        sys.exit(1)
    limit = args.limit
    results = []
    for cp in range(cp_from, cp_to + 1):
        ch = chr(cp)
        results.append(char_info(ch))
        if len(results) >= limit:
            break
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for i, info in enumerate(results):
            if i > 0:
                print()
            print(format_char_info(info))
        total = cp_to - cp_from + 1
        shown = len(results)
        if shown < total:
            print(f"\n... showing {shown} of {total} characters (use --limit to show more)")


def cmd_search(args):
    """Handle the 'search' subcommand."""
    pattern = args.s
    if not pattern:
        print("Error: no search pattern provided via -s", file=sys.stderr)
        sys.exit(1)
    limit = args.limit
    category_filter = args.category
    regex = re.compile(pattern, re.IGNORECASE)
    results = []
    # Scan the BMP and a reasonable portion of SMP
    for cp in range(0x0000, 0x10000):
        ch = chr(cp)
        if category_filter and unicodedata.category(ch) != category_filter:
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if regex.search(name):
            results.append(char_info(ch))
            if len(results) >= limit:
                break
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        if not results:
            print(f"No characters found matching pattern {pattern!r}")
            return
        for i, info in enumerate(results):
            cp_str = info["codepoint"]
            name = info["name"]
            cat = info["category"]
            block = info["block"]
            print(f"{cp_str}  {info['character']}  {name}  [{cat}]  {block}")
        print(f"\nFound {len(results)} result(s)")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="unicode_info",
        description="Look up Unicode character information without external dependencies.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command")

    # char
    p_char = subparsers.add_parser("char", help="Info about one or more characters")
    p_char.add_argument("-s", required=True, help="One or more characters to look up")
    p_char.add_argument("--json", action="store_true", help="Output as JSON")
    p_char.set_defaults(func=cmd_char)

    # codepoint
    p_cp = subparsers.add_parser("codepoint", help="Info from a codepoint (U+XXXX or 0xXXXX)")
    p_cp.add_argument("-s", required=True, help="Codepoint to look up (e.g. U+4E2D or 0x4E2D)")
    p_cp.add_argument("--json", action="store_true", help="Output as JSON")
    p_cp.set_defaults(func=cmd_codepoint)

    # range
    p_range = subparsers.add_parser("range", help="List characters in a codepoint range")
    p_range.add_argument("--from", dest="from_cp", required=True,
                         help="Start codepoint (e.g. U+2600)")
    p_range.add_argument("--to", dest="to_cp", required=True,
                         help="End codepoint (e.g. U+26FF)")
    p_range.add_argument("--limit", type=int, default=50,
                         help="Max number of characters to list (default: 50)")
    p_range.add_argument("--json", action="store_true", help="Output as JSON")
    p_range.set_defaults(func=cmd_range)

    # search
    p_search = subparsers.add_parser("search", help="Search characters by name pattern")
    p_search.add_argument("-s", required=True, help="Name pattern to search (regex)")
    p_search.add_argument("--category", default=None,
                          help="Filter by Unicode category (e.g. Nd, Lu, So)")
    p_search.add_argument("--limit", type=int, default=20,
                          help="Max number of results (default: 20)")
    p_search.add_argument("--json", action="store_true", help="Output as JSON")
    p_search.set_defaults(func=cmd_search)

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
