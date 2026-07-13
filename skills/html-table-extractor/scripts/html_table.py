#!/usr/bin/env python3
"""Extract table data from HTML files and convert to CSV or JSON."""

import argparse
import csv
import html
import io
import json
import re
import sys
from pathlib import Path


def extract_tables(html_text):
    """Extract all tables from HTML text. Returns list of list-of-lists."""
    tables = []
    # Find all <table>...</table> blocks (non-greedy)
    table_pattern = re.compile(r"<table[^>]*>(.*?)</table>", re.S | re.I)
    for tm in table_pattern.finditer(html_text):
        table_html = tm.group(1)
        rows = []
        # Find all <tr>...</tr>
        tr_pattern = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
        for trm in tr_pattern.finditer(table_html):
            row = []
            # Match <th> and <td>
            cell_pattern = re.compile(r"<(t[dh])[^>]*>(.*?)</\1>", re.S | re.I)
            for cm in cell_pattern.finditer(trm.group(1)):
                cell_text = clean_html(cm.group(2))
                row.append(cell_text)
            if row:
                rows.append(row)
        if rows:
            tables.append(rows)
    return tables


def clean_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tables_to_csv(tables, output=None, table_index=None):
    """Convert tables to CSV format."""
    target = tables if table_index is None else [tables[table_index]]
    out_parts = []
    for idx, rows in enumerate(target):
        if len(target) > 1:
            out_parts.append(f"# Table {idx}")
        # Normalize column count
        max_cols = max(len(r) for r in rows) if rows else 0
        for r in rows:
            while len(r) < max_cols:
                r.append("")
        buf = io.StringIO()
        writer = csv.writer(buf)
        for r in rows:
            writer.writerow(r)
        out_parts.append(buf.getvalue())
    result = "\n".join(out_parts)
    if output:
        Path(output).write_text(result, encoding="utf-8")
        print(f"Written to {output}")
    else:
        print(result, end="")


def tables_to_json(tables, output=None, table_index=None):
    """Convert tables to JSON format."""
    result = []
    target = tables if table_index is None else [tables[table_index]]
    for idx, rows in enumerate(target):
        if not rows:
            continue
        headers = rows[0]
        data = []
        for row in rows[1:]:
            record = {}
            for i, h in enumerate(headers):
                record[h] = row[i] if i < len(row) else ""
            data.append(record)
        result.append({"table_index": table_index if table_index is not None else idx, "headers": headers, "rows": data})
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if output:
        Path(output).write_text(text, encoding="utf-8")
        print(f"Written to {output}")
    else:
        print(text)


def cmd_extract(args):
    try:
        html_text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    tables = extract_tables(html_text)
    if not tables:
        print("No tables found in the HTML file.", file=sys.stderr)
        sys.exit(1)

    if args.table is not None:
        if args.table < 0 or args.table >= len(tables):
            print(f"Error: table index {args.table} out of range (0-{len(tables)-1})", file=sys.stderr)
            sys.exit(1)

    if args.format == "csv":
        tables_to_csv(tables, args.output, args.table)
    else:
        tables_to_json(tables, args.output, args.table)


def cmd_list(args):
    try:
        html_text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    tables = extract_tables(html_text)
    if not tables:
        print("No tables found.")
        return

    for i, rows in enumerate(tables):
        cols = max(len(r) for r in rows) if rows else 0
        headers = rows[0] if rows else []
        print(f"Table {i}: {len(rows)} rows x {cols} cols — headers: {headers[:5]}")


def main():
    parser = argparse.ArgumentParser(description="Extract tables from HTML files.")
    sub = parser.add_subparsers(dest="command")

    p_extract = sub.add_parser("extract", help="Extract tables from HTML")
    p_extract.add_argument("--file", required=True, help="HTML file")
    p_extract.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format")
    p_extract.add_argument("--table", type=int, help="Specific table index (0-based)")
    p_extract.add_argument("--output", help="Write to file instead of stdout")

    p_list = sub.add_parser("list", help="List tables in HTML file")
    p_list.add_argument("--file", required=True, help="HTML file")

    args = parser.parse_args()
    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
