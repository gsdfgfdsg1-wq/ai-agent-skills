#!/usr/bin/env python3
"""Generate Lorem ipsum placeholder text without external dependencies."""

import argparse
import json
import random
import sys


LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "perspiciatis", "unde",
    "omnis", "iste", "natus", "error", "voluptatem", "accusantium", "doloremque",
    "laudantium", "totam", "rem", "aperiam", "eaque", "ipsa", "quae", "ab", "illo",
    "inventore", "veritatis", "quasi", "architecto", "beatae", "vitae", "dicta",
    "explicabo", "nemo", "ipsam", "quia", "voluptas", "aspernatur", "aut", "odit",
    "fugit", "consequuntur", "magni", "dolores", "eos", "ratione", "sequi", "nesciunt",
    "neque", "porro", "quisquam", "dolorem", "adipisci", "numquam", "eius", "modi",
    "tempora", "magnam", "quaerat", "minima", "nostrum", "exercitationem",
    "ullam", "corporis", "suscipit", "laboriosam", "aliquid", "commodi",
    "consequatur", "autem", "vel", "eum", "iure", "quam", "nihil", "impedit",
    "quo", "minus", "quod", "maxime", "placeat", "facere", "possimus", "assumenda",
    "repellendus", "temporibus", "quibusdam", "illum", "fugiat", "voluptas",
    "nulla", "recusandae", "itaque", "earum", "rerum", "hic", "tenetur",
    "sapiente", "delectus", "reiciendis", "voluptatibus", "maiores", "alias",
    "perferendis", "doloribus", "asperiores", "repellat",
]

LOREM_START = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."


def gen_sentence(min_words=5, max_words=15):
    """Generate a single Lorem ipsum sentence."""
    count = random.randint(min_words, max_words)
    words = [random.choice(LOREM_WORDS) for _ in range(count)]
    words[0] = words[0].capitalize()
    return " ".join(words) + "."


def gen_paragraph(min_sentences=3, max_sentences=7):
    """Generate a paragraph of Lorem ipsum."""
    count = random.randint(min_sentences, max_sentences)
    return " ".join(gen_sentence() for _ in range(count))


def cmd_paragraphs(args):
    start = args.start_with_lorem
    result = []
    for i in range(args.count):
        if i == 0 and start:
            result.append(LOREM_START + " " + gen_paragraph())
        else:
            result.append(gen_paragraph())

    if args.json:
        print(json.dumps({"paragraphs": result, "count": len(result)}, indent=2))
    else:
        print("\n\n".join(result))


def cmd_sentences(args):
    result = [gen_sentence() for _ in range(args.count)]
    if args.json:
        print(json.dumps({"sentences": result, "count": len(result)}, indent=2))
    else:
        print(" ".join(result))


def cmd_words(args):
    result = [random.choice(LOREM_WORDS) for _ in range(args.count)]
    if args.json:
        print(json.dumps({"words": result, "count": len(result)}, indent=2))
    else:
        print(" ".join(result))


def main():
    parser = argparse.ArgumentParser(description="Generate Lorem ipsum placeholder text.")
    sub = parser.add_subparsers(dest="command")

    p_para = sub.add_parser("paragraphs", help="Generate paragraphs")
    p_para.add_argument("--count", type=int, default=3, help="Number of paragraphs (default: 3)")
    p_para.add_argument("--start-with-lorem", action="store_true", help="Start with classic opening")
    p_para.add_argument("--json", action="store_true", help="JSON output")

    p_sent = sub.add_parser("sentences", help="Generate sentences")
    p_sent.add_argument("--count", type=int, default=5, help="Number of sentences (default: 5)")
    p_sent.add_argument("--json", action="store_true", help="JSON output")

    p_word = sub.add_parser("words", help="Generate words")
    p_word.add_argument("--count", type=int, default=50, help="Number of words (default: 50)")
    p_word.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "paragraphs":
        cmd_paragraphs(args)
    elif args.command == "sentences":
        cmd_sentences(args)
    elif args.command == "words":
        cmd_words(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
