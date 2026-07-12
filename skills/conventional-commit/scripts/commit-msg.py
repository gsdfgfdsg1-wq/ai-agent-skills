#!/usr/bin/env python3
"""
Conventional Commit Helper — validate and generate
commit messages following the Conventional Commits 1.0.0 spec.

Usage:
    # Validate a commit message
    python commit-msg.py validate "<message>"

    # Validate from a file (e.g. .git/COMMIT_EDITMSG)
    python commit-msg.py validate --file <path>

    # Generate a commit message
    python commit-msg.py generate --type feat --scope cli --desc "add --dry-run flag"
"""

import argparse
import re
import sys

# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------

ALLOWED_TYPES = [
    "feat", "fix", "docs", "style", "refactor",
    "perf", "test", "build", "ci", "chore", "revert",
]

# Pattern: type(scope)!: description
COMMIT_PATTERN = re.compile(
    r"^(?P<type>" + "|".join(ALLOWED_TYPES) + r")"
    r"(?:\((?P<scope>[^()\s]+)\))?"
    r"(?P<breaking>!)?"
    r":\s+(?P<desc>.+)$"
)

FOOTER_BREAKING = re.compile(r"^BREAKING CHANGE:\s+(.+)$", re.IGNORECASE)
FOOTER_REF = re.compile(r"^(?:Refs?|Closes?|Fixes?|See|Related-to):\s+.+$", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_message(msg: str) -> list[str]:
    """Return a list of error messages (empty means valid)."""
    errors = []
    lines = [l.rstrip("\r\n") for l in msg.split("\n")]

    if not msg.strip():
        return ["Commit message is empty."]

    first = lines[0]
    m = COMMIT_PATTERN.match(first)

    if not m:
        types_str = ", ".join(ALLOWED_TYPES)
        errors.append(
            f"First line must match: type(scope)!: description\n"
            f"  Allowed types: {types_str}\n"
            f"  Got: {first!r}"
        )
        return errors

    # -- type
    t = m.group("type")
    if t not in ALLOWED_TYPES:
        errors.append(f"Unknown type {t!r}. Allowed: {', '.join(ALLOWED_TYPES)}")

    # -- first line length
    if len(first) > 72:
        errors.append(f"First line is {len(first)} chars (max 72).")

    # -- body / footer separator
    body_start = None
    for i, line in enumerate(lines[1:], start=1):
        if line == "":
            body_start = i + 1
            break

    if body_start is not None:
        # body lines should be wrapped at 72
        for j, line in enumerate(lines[body_start:], start=body_start):
            if line.startswith("#"):
                continue
            if len(line) > 72:
                errors.append(f"Line {j+1} is {len(line)} chars (max 72).")

        # validate footers
        in_footer = False
        for j, line in enumerate(lines[body_start:], start=body_start):
            if line == "":
                continue
            if not in_footer:
                # after blank line + first non-blank -> might be footer
                if FOOTER_BREAKING.match(line) or FOOTER_REF.match(line):
                    in_footer = True
                continue
            # subsequent footer lines
            if line.startswith(" "):
                continue  # continuation line
            if not (FOOTER_BREAKING.match(line) or FOOTER_REF.match(line)):
                errors.append(f"Line {j+1}: unexpected footer format {line!r}")

    return errors


def format_errors(errors: list[str]) -> str:
    lines = []
    for e in errors:
        lines.append(f"  ❌ {e}")
    if errors:
        lines.insert(0, f"Found {len(errors)} issue(s):")
    else:
        lines.append("✅ Commit message is valid.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_message(
    type_: str,
    description: str,
    scope: str | None = None,
    breaking: bool = False,
    body: str | None = None,
    footer: str | None = None,
) -> str:
    """Build a Conventional Commit string."""
    if type_ not in ALLOWED_TYPES:
        print(f"Warning: type {type_!r} not in standard list ({', '.join(ALLOWED_TYPES)})",
              file=sys.stderr)

    scope_part = f"({scope})" if scope else ""
    breaking_mark = "!" if breaking else ""
    first = f"{type_}{scope_part}{breaking_mark}: {description}"

    parts = [first]

    if body:
        parts.append("")
        parts.append(body)

    if breaking and not (body and "BREAKING CHANGE" in (footer or "")):
        parts.append("")
        parts.append(f"BREAKING CHANGE: {description}")

    if footer:
        if not body:
            parts.append("")
        parts.append(footer)

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Conventional Commit Helper — validate and generate commit messages."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- validate ---
    val = sub.add_parser("validate", help="Validate a commit message")
    val.add_argument("message", nargs="?", help="Commit message text")
    val.add_argument("--file", "-f", help="Read commit message from file")

    # --- generate ---
    gen = sub.add_parser("generate", help="Generate a commit message")
    gen.add_argument("--type", "-t", required=True, help=f"Commit type ({', '.join(ALLOWED_TYPES)})")
    gen.add_argument("--desc", "-d", required=True, help="Short description (imperative)")
    gen.add_argument("--scope", "-s", help="Scope of the change")
    gen.add_argument("--breaking", "-b", action="store_true", help="Mark as breaking change")
    gen.add_argument("--body", help="Long description body")
    gen.add_argument("--footer", help="Footer (e.g. 'Refs: #123')")

    args = parser.parse_args()

    if args.command == "validate":
        if args.file:
            with open(args.file, encoding="utf-8") as f:
                msg = f.read()
        elif args.message:
            msg = args.message
        else:
            parser.error("Provide a message string or --file <path>")

        errs = validate_message(msg)
        print(format_errors(errs))
        sys.exit(1 if errs else 0)

    elif args.command == "generate":
        result = generate_message(
            type_=args.type,
            description=args.desc,
            scope=args.scope,
            breaking=args.breaking,
            body=args.body,
            footer=args.footer,
        )
        print(result)

    # --- interactive helpers printed by SKILL.md ---


if __name__ == "__main__":
    main()