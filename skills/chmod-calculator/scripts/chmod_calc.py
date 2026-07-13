#!/usr/bin/env python3
"""Convert Unix file permissions between symbolic and octal notation without external dependencies."""

import argparse
import json
import re
import sys


PERM_BITS = {"r": 4, "w": 2, "x": 1, "s": 0, "S": 0, "t": 0, "T": 0}
SPECIAL_MAP = {"s": 1, "S": 1, "t": 1, "T": 1}


def octal_to_symbolic(octal_str):
    """Convert octal permission string to symbolic."""
    octal_str = octal_str.strip()
    # Handle 3 or 4 digit octal
    if len(octal_str) == 3:
        special = 0
        digits = [int(c) for c in octal_str]
    elif len(octal_str) == 4:
        special = int(octal_str[0])
        digits = [int(c) for c in octal_str[1:]]
    else:
        return None, f"Invalid octal mode '{octal_str}': must be 3 or 4 digits"

    for d in digits:
        if d < 0 or d > 7:
            return None, f"Invalid octal digit '{d}'"

    result = ""
    categories = ["user", "group", "other"]
    for i, (d, cat) in enumerate(zip(digits, categories)):
        r = "r" if d & 4 else "-"
        w = "w" if d & 2 else "-"
        # Handle setuid/setgid/sticky
        if i == 0 and special & 4:  # setuid
            x = "s" if d & 1 else "S"
        elif i == 1 and special & 2:  # setgid
            x = "s" if d & 1 else "S"
        elif i == 2 and special & 1:  # sticky
            x = "t" if d & 1 else "T"
        else:
            x = "x" if d & 1 else "-"
        result += r + w + x

    return result, None


def symbolic_to_octal(symbolic):
    """Convert symbolic permission string to octal."""
    symbolic = symbolic.strip()
    if len(symbolic) == 9:
        # rwxr-xr-x format
        pass
    elif len(symbolic) == 10 and symbolic[0] in "d-":
        symbolic = symbolic[1:]  # skip file type indicator
    else:
        return None, f"Invalid symbolic mode '{symbolic}': must be 9 characters"

    special = 0
    digits = []

    for i in range(3):
        chunk = symbolic[i * 3:i * 3 + 3]
        val = 0
        if chunk[0] == "r":
            val += 4
        elif chunk[0] != "-":
            return None, f"Invalid char '{chunk[0]}' at position {i * 3}"

        if chunk[1] == "w":
            val += 2
        elif chunk[1] != "-":
            return None, f"Invalid char '{chunk[1]}' at position {i * 3 + 1}"

        if chunk[2] == "x":
            val += 1
        elif chunk[2] == "s":
            val += 1
            if i == 0:
                special |= 4  # setuid
            elif i == 1:
                special |= 2  # setgid
        elif chunk[2] == "S":
            if i == 0:
                special |= 4
            elif i == 1:
                special |= 2
        elif chunk[2] == "t":
            val += 1
            special |= 1  # sticky
        elif chunk[2] == "T":
            special |= 1
        elif chunk[2] != "-":
            return None, f"Invalid char '{chunk[2]}' at position {i * 3 + 2}"

        digits.append(val)

    if special:
        return f"{special}{digits[0]}{digits[1]}{digits[2]}", None
    return f"{digits[0]}{digits[1]}{digits[2]}", None


def explain_permissions(mode_str):
    """Explain each permission component."""
    # First determine if octal or symbolic
    if mode_str.isdigit():
        symbolic, err = octal_to_symbolic(mode_str)
        if err:
            return None, err
        octal = mode_str
    else:
        octal, err = symbolic_to_octal(mode_str)
        if err:
            return None, err
        symbolic = mode_str.strip()
        if len(symbolic) == 10 and symbolic[0] in "d-":
            symbolic = symbolic[1:]

    result = {"octal": octal, "symbolic": symbolic, "breakdown": []}
    cats = ["user (owner)", "group", "other"]
    for i, cat in enumerate(cats):
        chunk = symbolic[i * 3:i * 3 + 3]
        perms = []
        if chunk[0] == "r":
            perms.append("read")
        if chunk[1] == "w":
            perms.append("write")
        if chunk[2] in ("x", "s", "t"):
            perms.append("execute")
        if chunk[2] == "s" and i < 2:
            perms.append("set" + ("uid" if i == 0 else "gid"))
        if chunk[2] == "S" and i < 2:
            perms.append("set" + ("uid" if i == 0 else "gid") + " (no execute)")
        if chunk[2] == "t":
            perms.append("sticky bit")
        if chunk[2] == "T":
            perms.append("sticky bit (no execute)")
        result["breakdown"].append({"category": cat, "permissions": perms or ["none"]})

    return result, None


def apply_symbolic_changes(base_octal, changes_str):
    """Apply symbolic changes like u+x,g-w to a base octal mode."""
    # Parse base
    if len(base_octal) == 3:
        digits = [int(c) for c in base_octal]
        special = 0
    elif len(base_octal) == 4:
        special = int(base_octal[0])
        digits = [int(c) for c in base_octal[1:]]
    else:
        return None, f"Invalid base mode '{base_octal}'"

    changes = changes_str.split(",")
    for change in changes:
        change = change.strip()
        m = re.match(r"^([ugoa]+)([+-=])([rwxst]+)$", change)
        if not m:
            return None, f"Invalid change '{change}'"

        who = m.group(1)
        op = m.group(2)
        what = m.group(3)

        # Expand 'a' to 'ugo'
        targets = set()
        for c in who:
            if c == "a":
                targets.update([0, 1, 2])
            elif c == "u":
                targets.add(0)
            elif c == "g":
                targets.add(1)
            elif c == "o":
                targets.add(2)

        perm_val = 0
        for c in what:
            if c == "r":
                perm_val |= 4
            elif c == "w":
                perm_val |= 2
            elif c == "x":
                perm_val |= 1
            elif c == "s":
                perm_val |= 1
                special |= (4 if 0 in targets else 0) | (2 if 1 in targets else 0)
            elif c == "t":
                perm_val |= 1
                special |= 1

        for t in targets:
            if op == "+":
                digits[t] |= perm_val
            elif op == "-":
                digits[t] &= ~perm_val
            elif op == "=":
                digits[t] = perm_val

    if special:
        return f"{special}{digits[0]}{digits[1]}{digits[2]}", None
    return f"{digits[0]}{digits[1]}{digits[2]}", None


def cmd_octal2symbolic(args):
    result, err = octal_to_symbolic(args.mode)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps({"octal": args.mode, "symbolic": result}, indent=2))
    else:
        print(f"{args.mode} → {result}")


def cmd_symbolic2octal(args):
    result, err = symbolic_to_octal(args.mode)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps({"symbolic": args.mode, "octal": result}, indent=2))
    else:
        print(f"{args.mode} → {result}")


def cmd_explain(args):
    result, err = explain_permissions(args.mode)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Mode: {result['octal']} ({result['symbolic']})")
        for bd in result["breakdown"]:
            print(f"  {bd['category']}: {', '.join(bd['permissions'])}")


def cmd_combine(args):
    result, err = apply_symbolic_changes(args.base, args.changes)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    symbolic, _ = octal_to_symbolic(result)
    if args.json:
        print(json.dumps({"base": args.base, "changes": args.changes, "result_octal": result, "result_symbolic": symbolic}, indent=2))
    else:
        print(f"{args.base} + {args.changes} → {result} ({symbolic})")


def main():
    parser = argparse.ArgumentParser(description="Unix permission mode calculator.")
    sub = parser.add_subparsers(dest="command")

    p_o2s = sub.add_parser("octal2symbolic", help="Octal to symbolic")
    p_o2s.add_argument("--mode", required=True, help="Octal mode (e.g., 755)")
    p_o2s.add_argument("--json", action="store_true", help="JSON output")

    p_s2o = sub.add_parser("symbolic2octal", help="Symbolic to octal")
    p_s2o.add_argument("--mode", required=True, help="Symbolic mode (e.g., rwxr-xr-x)")
    p_s2o.add_argument("--json", action="store_true", help="JSON output")

    p_exp = sub.add_parser("explain", help="Explain permissions")
    p_exp.add_argument("--mode", required=True, help="Octal or symbolic mode")
    p_exp.add_argument("--json", action="store_true", help="JSON output")

    p_comb = sub.add_parser("combine", help="Apply symbolic changes")
    p_comb.add_argument("--base", required=True, help="Base octal mode")
    p_comb.add_argument("--changes", required=True, help="Changes (e.g., u+x,g-w)")
    p_comb.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "octal2symbolic":
        cmd_octal2symbolic(args)
    elif args.command == "symbolic2octal":
        cmd_symbolic2octal(args)
    elif args.command == "explain":
        cmd_explain(args)
    elif args.command == "combine":
        cmd_combine(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
