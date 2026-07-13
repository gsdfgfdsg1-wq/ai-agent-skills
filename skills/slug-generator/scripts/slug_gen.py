#!/usr/bin/env python3
"""Generate URL-safe slugs from text without external dependencies."""

import argparse
import json
import re
import sys
import unicodedata


# Basic transliteration map for common non-ASCII characters
TRANSLIT_MAP = {
    "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a",
    "æ": "ae", "ç": "c",
    "è": "e", "é": "e", "ê": "e", "ë": "e",
    "ì": "i", "í": "i", "î": "i", "ï": "i",
    "ñ": "n",
    "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o", "ø": "o",
    "ù": "u", "ú": "u", "û": "u", "ü": "u",
    "ý": "y", "ÿ": "y",
    "ß": "ss",
    "À": "A", "Á": "A", "Â": "A", "Ã": "A", "Ä": "A", "Å": "A",
    "Æ": "AE", "Ç": "C",
    "È": "E", "É": "E", "Ê": "E", "Ë": "E",
    "Ì": "I", "Í": "I", "Î": "I", "Ï": "I",
    "Ñ": "N",
    "Ò": "O", "Ó": "O", "Ô": "O", "Õ": "O", "Ö": "O", "Ø": "O",
    "Ù": "U", "Ú": "U", "Û": "U", "Ü": "U",
    "Ý": "Y",
}


def transliterate(text):
    """Basic transliteration of common accented characters."""
    result = []
    for ch in text:
        if ch in TRANSLIT_MAP:
            result.append(TRANSLIT_MAP[ch])
        else:
            # Try NFKD decomposition and strip combining marks
            decomposed = unicodedata.normalize("NFKD", ch)
            stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
            if stripped and stripped.isascii() and stripped.isalnum():
                result.append(stripped)
            elif ch.isascii():
                result.append(ch)
            # else: non-ASCII, non-transliterable character gets dropped
    return "".join(result)


def generate_slug(text, separator="-", lowercase=True, max_length=0):
    """Generate a URL-safe slug from text."""
    # Transliterate
    slug = transliterate(text)

    # Convert case
    if lowercase:
        slug = slug.lower()

    # Replace non-alphanumeric with separator
    slug = re.sub(r'[^a-zA-Z0-9]+', separator, slug)

    # Remove leading/trailing separators
    slug = slug.strip(separator)

    # Collapse multiple separators
    if separator:
        slug = re.sub(re.escape(separator) + r'+', separator, slug)

    # Truncate to max length at a word boundary
    if max_length and len(slug) > max_length:
        slug = slug[:max_length]
        # Remove trailing partial word
        if separator in slug:
            slug = slug[:slug.rfind(separator)]

    return slug


def cmd_generate(args):
    slug = generate_slug(args.text, args.separator, not args.no_lowercase, args.max_length)

    if args.json:
        print(json.dumps({"input": args.text, "slug": slug}, indent=2))
    else:
        print(slug)


def cmd_batch(args):
    try:
        with open(args.file, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    results = []
    for line in lines:
        slug = generate_slug(line, args.separator, not args.no_lowercase, args.max_length)
        results.append({"input": line, "slug": slug})

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['slug']}  <-  {r['input']}")


def main():
    parser = argparse.ArgumentParser(description="Generate URL-safe slugs from text.")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("generate", help="Generate a slug from text")
    p_gen.add_argument("--text", required=True, help="Text to slugify")
    p_gen.add_argument("--separator", default="-", help="Word separator (default: -)")
    p_gen.add_argument("--no-lowercase", action="store_true", help="Keep original case")
    p_gen.add_argument("--max-length", type=int, default=0, help="Max slug length")
    p_gen.add_argument("--json", action="store_true", help="JSON output")

    p_batch = sub.add_parser("batch", help="Generate slugs from a file of lines")
    p_batch.add_argument("--file", required=True, help="Text file, one line per slug")
    p_batch.add_argument("--separator", default="-", help="Word separator")
    p_batch.add_argument("--no-lowercase", action="store_true", help="Keep original case")
    p_batch.add_argument("--max-length", type=int, default=0, help="Max slug length")
    p_batch.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "batch":
        cmd_batch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
