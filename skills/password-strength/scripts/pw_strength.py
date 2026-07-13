#!/usr/bin/env python3
"""Analyze password strength with entropy, pattern detection, and scoring without external dependencies."""

import argparse
import json
import math
import re
import sys


COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "monkey", "master",
    "dragon", "111111", "baseball", "iloveyou", "trustno1", "sunshine",
    "ashley", "football", "shadow", "123123", "654321", "superman",
    "qazwsx", "michael", "password1", "password123", "letmein", "admin",
    "welcome", "login", "princess", "starwars", "1q2w3e4r",
}

KEYBOARD_ROWS = [
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234567890",
]


def calc_entropy(password):
    """Calculate Shannon entropy of the password."""
    if not password:
        return 0.0
    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset_size += 32
    if charset_size == 0:
        return 0.0
    return len(password) * math.log2(charset_size)


def detect_patterns(password):
    """Detect common weakness patterns."""
    findings = []
    pw_lower = password.lower()

    # Common password
    if pw_lower in COMMON_PASSWORDS:
        findings.append({"pattern": "common-password", "severity": "critical", "detail": f"'{pw_lower}' is in common password list"})

    # Sequential characters (abc, 123, etc.)
    for length in range(4, 2, -1):
        for i in range(len(password) - length + 1):
            segment = password[i:i + length]
            if segment.isdigit() and len(set(int(c) for c in segment)) > 1:
                diffs = [int(segment[j+1]) - int(segment[j]) for j in range(len(segment)-1)]
                if all(d == diffs[0] for d in diffs):
                    findings.append({"pattern": "sequential-digits", "severity": "warning", "detail": f"'{segment}' is a sequential digit pattern"})
                    break
            if segment.isalpha():
                ords = [ord(c) for c in segment.lower()]
                diffs = [ords[j+1] - ords[j] for j in range(len(ords)-1)]
                if all(d == 1 for d in diffs):
                    findings.append({"pattern": "sequential-chars", "severity": "warning", "detail": f"'{segment}' is sequential letters"})
                    break

    # Repeated characters
    for m in re.finditer(r'(.)\1{2,}', password):
        findings.append({"pattern": "repeated-chars", "severity": "warning", "detail": f"'{m.group()}' has repeated character '{m.group(1)}'"})

    # Keyboard walks
    for row in KEYBOARD_ROWS:
        for length in range(5, 3, -1):
            for i in range(len(row) - length + 1):
                seq = row[i:i + length]
                if seq in pw_lower:
                    findings.append({"pattern": "keyboard-walk", "severity": "warning", "detail": f"'{seq}' is a keyboard pattern"})
                rev = seq[::-1]
                if rev in pw_lower and rev != seq:
                    findings.append({"pattern": "keyboard-walk", "severity": "warning", "detail": f"'{rev}' is a reverse keyboard pattern"})

    # Date patterns
    if re.search(r'(19|20)\d{2}', password):
        findings.append({"pattern": "date-pattern", "severity": "info", "detail": "Contains a year (19xx/20xx)"})
    if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])', password):
        findings.append({"pattern": "date-pattern", "severity": "info", "detail": "Contains a possible date (MMDD)"})

    # Length issues
    if len(password) < 8:
        findings.append({"pattern": "short-length", "severity": "critical", "detail": f"Password is only {len(password)} chars (minimum 8 recommended)"})
    elif len(password) < 12:
        findings.append({"pattern": "marginal-length", "severity": "info", "detail": f"Password is {len(password)} chars (12+ recommended)"})

    # Character variety
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", password))
    variety = sum([has_lower, has_upper, has_digit, has_special])
    if variety < 3:
        findings.append({"pattern": "low-variety", "severity": "warning", "detail": f"Only {variety}/4 character types used (lowercase, uppercase, digits, special)"})

    return findings


def calc_score(password):
    """Calculate a 0-100 strength score."""
    if not password:
        return 0

    score = 0

    # Length scoring (up to 30 points)
    length = len(password)
    if length >= 16:
        score += 30
    elif length >= 12:
        score += 25
    elif length >= 8:
        score += 15
    elif length >= 6:
        score += 5

    # Character variety (up to 25 points)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", password))
    variety = sum([has_lower, has_upper, has_digit, has_special])
    score += variety * 6 + (1 if variety == 4 else 0)

    # Entropy bonus (up to 25 points)
    entropy = calc_entropy(password)
    if entropy >= 80:
        score += 25
    elif entropy >= 60:
        score += 20
    elif entropy >= 40:
        score += 12
    elif entropy >= 25:
        score += 5

    # Pattern penalties
    patterns = detect_patterns(password)
    for p in patterns:
        if p["severity"] == "critical":
            score -= 20
        elif p["severity"] == "warning":
            score -= 10
        elif p["severity"] == "info":
            score -= 3

    # Unique character ratio bonus (up to 20 points)
    if length > 0:
        unique_ratio = len(set(password)) / length
        score += int(unique_ratio * 20)

    return max(0, min(100, score))


def strength_label(score):
    """Map score to a strength label."""
    if score >= 80:
        return "very-strong"
    if score >= 60:
        return "strong"
    if score >= 40:
        return "moderate"
    if score >= 20:
        return "weak"
    return "very-weak"


def cmd_analyze(args):
    pw = args.password
    entropy = calc_entropy(pw)
    patterns = detect_patterns(pw)
    score = calc_score(pw)
    label = strength_label(score)

    result = {
        "length": len(pw),
        "entropy_bits": round(entropy, 1),
        "score": score,
        "strength": label,
        "patterns": patterns,
        "character_types": {
            "lowercase": bool(re.search(r"[a-z]", pw)),
            "uppercase": bool(re.search(r"[A-Z]", pw)),
            "digits": bool(re.search(r"[0-9]", pw)),
            "special": bool(re.search(r"[^a-zA-Z0-9]", pw)),
        },
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Password: {'*' * len(pw)}")
        print(f"  Length:      {result['length']}")
        print(f"  Entropy:     {result['entropy_bits']} bits")
        print(f"  Score:       {score}/100 ({label})")
        print(f"  Char types:  {sum(v for v in result['character_types'].values())}/4")
        if patterns:
            print(f"  Patterns ({len(patterns)}):")
            for p in patterns:
                print(f"    [{p['severity'].upper()}] {p['detail']}")


def cmd_score(args):
    score = calc_score(args.password)
    label = strength_label(score)
    if args.json:
        print(json.dumps({"score": score, "strength": label}, indent=2))
    else:
        print(f"{score}/100 ({label})")


def main():
    parser = argparse.ArgumentParser(description="Analyze password strength.")
    sub = parser.add_subparsers(dest="command")

    p_analyze = sub.add_parser("analyze", help="Full strength analysis")
    p_analyze.add_argument("--password", required=True, help="Password to analyze")
    p_analyze.add_argument("--json", action="store_true", help="JSON output")

    p_score = sub.add_parser("score", help="Quick 0-100 score")
    p_score.add_argument("--password", required=True, help="Password to score")
    p_score.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "score":
        cmd_score(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
