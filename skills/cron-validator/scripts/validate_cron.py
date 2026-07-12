#!/usr/bin/env python3
"""cron-validator — validate cron expressions and compute next run times.

Usage:
    python validate_cron.py EXPR [--next N] [--json]

Supports standard 5-field cron (min hour dom month dow) and 6-field (sec min hour dom month dow).
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

# Field definitions for 5-field cron
FIELD_DEFS_5 = [
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day_of_month", 1, 31),
    ("month", 1, 12),
    ("day_of_week", 0, 6),
]

FIELD_DEFS_6 = [
    ("second", 0, 59),
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day_of_month", 1, 31),
    ("month", 1, 12),
    ("day_of_week", 0, 6),
]

DOW_NAMES = {
    "SUN": "0", "MON": "1", "TUE": "2", "WED": "3",
    "THU": "4", "FRI": "5", "SAT": "6",
}
MONTH_NAMES = {
    "JAN": "1", "FEB": "2", "MAR": "3", "APR": "4",
    "MAY": "5", "JUN": "6", "JUL": "7", "AUG": "8",
    "SEP": "9", "OCT": "10", "NOV": "11", "DEC": "12",
}


def _resolve_names(field, text):
    text = text.upper()
    if field == "day_of_week":
        for name, val in DOW_NAMES.items():
            text = text.replace(name, val)
    elif field == "month":
        for name, val in MONTH_NAMES.items():
            text = text.replace(name, val)
    return text


def _parse_field(field, text, lo, hi):
    """Parse a single cron field, returning a sorted set of valid values."""
    text = _resolve_names(field, text)
    values = set()

    for part in text.split(","):
        step = 1
        if "/" in part:
            range_part, step_str = part.split("/", 1)
            try:
                step = int(step_str)
            except ValueError:
                raise ValueError(f"invalid step value: {step_str}")
            if step < 1:
                raise ValueError(f"step must be >= 1, got {step}")
        else:
            range_part = part

        if range_part == "*":
            start, end = lo, hi
        elif "-" in range_part:
            parts = range_part.split("-", 1)
            try:
                start, end = int(parts[0]), int(parts[1])
            except ValueError:
                raise ValueError(f"invalid range: {range_part}")
        else:
            try:
                start = end = int(range_part)
            except ValueError:
                raise ValueError(f"invalid value: {range_part}")

        if start < lo or end > hi:
            raise ValueError(f"value out of range [{lo}-{hi}]: {range_part}")
        if start > end:
            raise ValueError(f"start > end in range: {range_part}")

        for v in range(start, end + 1, step):
            values.add(v)

    return sorted(values)


def validate_cron(expr):
    """Validate a cron expression and return parsed fields or raise ValueError."""
    parts = expr.strip().split()
    if len(parts) == 5:
        field_defs = FIELD_DEFS_5
    elif len(parts) == 6:
        field_defs = FIELD_DEFS_6
    else:
        raise ValueError(
            f"expected 5 or 6 fields, got {len(parts)}"
        )

    parsed = {}
    for (name, lo, hi), text in zip(field_defs, parts):
        parsed[name] = _parse_field(name, text, lo, hi)

    return parsed, len(parts)


def _compute_next(parsed, n_fields, after=None):
    """Compute the next execution time after `after` (default: now)."""
    if after is None:
        after = datetime.now().replace(second=0, microsecond=0)
    if n_fields == 5:
        after = after.replace(second=0)

    # Brute-force search (max 366 days forward)
    delta = timedelta(minutes=1) if n_fields == 5 else timedelta(seconds=1)
    candidate = after + delta
    limit = after + timedelta(days=366)

    while candidate <= limit:
        if candidate.month not in parsed["month"]:
            # Jump to next valid month
            next_month = None
            for m in parsed["month"]:
                if m > candidate.month:
                    next_month = m
                    break
            if next_month is None:
                candidate = candidate.replace(
                    year=candidate.year + 1, month=parsed["month"][0], day=1, hour=0, minute=0, second=0
                )
            else:
                candidate = candidate.replace(month=next_month, day=1, hour=0, minute=0, second=0)
            continue

        if candidate.day not in parsed["day_of_month"]:
            candidate += timedelta(days=1)
            candidate = candidate.replace(hour=0, minute=0, second=0)
            continue

        if candidate.hour not in parsed["hour"]:
            candidate += timedelta(hours=1)
            candidate = candidate.replace(minute=0, second=0)
            continue

        if candidate.minute not in parsed["minute"]:
            candidate += timedelta(minutes=1)
            candidate = candidate.replace(second=0)
            continue

        if n_fields == 6 and candidate.second not in parsed["second"]:
            candidate += timedelta(seconds=1)
            continue

        # Check day_of_week (0=Sun)
        dow = candidate.isoweekday() % 7  # 0=Sun
        if dow not in parsed["day_of_week"]:
            candidate += timedelta(days=1)
            candidate = candidate.replace(hour=0, minute=0, second=0)
            continue

        return candidate

    return None


def main():
    ap = argparse.ArgumentParser(
        description="Validate cron expressions and compute next run times."
    )
    ap.add_argument("expr", help="cron expression (5 or 6 fields)")
    ap.add_argument("--next", type=int, default=0,
                    help="show next N execution times (default: 0 = validate only)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    try:
        parsed, n_fields = validate_cron(args.expr)
    except ValueError as e:
        if args.json:
            print(json.dumps({"valid": False, "error": str(e)}))
        else:
            print(f"Invalid: {e}", file=sys.stderr)
        return 1

    result = {"valid": True, "fields": n_fields, "parsed": {k: v for k, v in parsed.items()}}

    if args.next > 0:
        times = []
        after = None
        for _ in range(args.next):
            nxt = _compute_next(parsed, n_fields, after)
            if nxt is None:
                break
            times.append(nxt.isoformat())
            after = nxt
        result["next_runs"] = times

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Valid cron expression ({n_fields} fields)")
        if args.next > 0:
            print("\nNext runs:")
            for t in result.get("next_runs", []):
                print(f"  {t}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
