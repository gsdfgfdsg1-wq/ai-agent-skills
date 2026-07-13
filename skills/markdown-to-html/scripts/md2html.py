#!/usr/bin/env python3
"""Convert Markdown files to standalone HTML without external dependencies."""

import argparse
import html
import re
import sys
from pathlib import Path

STYLES = {
    "plain": """body{font-family:system-ui,sans-serif;max-width:800px;margin:2em auto;padding:0 1em;line-height:1.6;color:#333}
h1,h2,h3{border-bottom:1px solid #eee;padding-bottom:0.3em}
code{background:#f4f4f4;padding:0.2em 0.4em;border-radius:3px;font-size:0.9em}
pre{background:#f4f4f4;padding:1em;overflow-x:auto;border-radius:5px}
pre code{background:none;padding:0}
blockquote{border-left:4px solid #ddd;margin:0;padding-left:1em;color:#666}
table{border-collapse:collapse;margin:1em 0}
th,td{border:1px solid #ddd;padding:0.5em 1em}
img{max-width:100%}""",
    "github": """body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;max-width:980px;margin:0 auto;padding:45px;font-size:16px;line-height:1.6;color:#24292e}
h1{font-size:2em;border-bottom:1px solid #eaecef;padding-bottom:0.3em}
h2{font-size:1.5em;border-bottom:1px solid #eaecef;padding-bottom:0.3em}
h3{font-size:1.25em}
code{background:#f6f8fa;padding:0.2em 0.4em;border-radius:3px;font-size:85%}
pre{background:#f6f8fa;padding:16px;overflow:auto;border-radius:6px;line-height:1.45}
pre code{background:none;padding:0;font-size:100%}
blockquote{border-left:4px solid #dfe2e5;margin:0 0 16px;padding:0 1em;color:#6a737d}
table{border-collapse:collapse;margin:16px 0}
th,td{border:1px solid #dfe2e5;padding:6px 13px}
tr:nth-child(even){background:#f6f8fa}
img{max-width:100%;box-sizing:content-box}
a{color:#0366d6;text-decoration:none}
a:hover{text-decoration:underline}
ul,ol{padding-left:2em}""",
    "dark": """body{font-family:system-ui,sans-serif;max-width:800px;margin:2em auto;padding:0 1em;line-height:1.6;color:#c9d1d9;background:#0d1117}
h1,h2,h3{border-bottom:1px solid #21262d;padding-bottom:0.3em;color:#f0f6fc}
code{background:#161b22;padding:0.2em 0.4em;border-radius:3px;font-size:0.9em}
pre{background:#161b22;padding:1em;overflow-x:auto;border-radius:5px}
pre code{background:none;padding:0}
blockquote{border-left:4px solid #30363d;margin:0;padding-left:1em;color:#8b949e}
table{border-collapse:collapse;margin:1em 0}
th,td{border:1px solid #30363d;padding:0.5em 1em}
a{color:#58a6ff}""",
}


def md_to_html(text):
    """Convert basic Markdown to HTML (no external deps)."""
    lines = text.split("\n")
    out = []
    i = 0
    in_list = False
    in_ol = False
    in_code_block = False
    code_content = []
    code_lang = ""

    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
                code_content = []
                i += 1
                continue
            else:
                in_code_block = False
                escaped = html.escape("\n".join(code_content))
                cls = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                out.append(f"<pre><code{cls}>{escaped}</code></pre>")
                i += 1
                continue

        if in_code_block:
            code_content.append(line)
            i += 1
            continue

        # Close lists
        if in_list and not re.match(r"^\s*[-*+]\s", line):
            out.append("</ul>")
            in_list = False
        if in_ol and not re.match(r"^\s*\d+\.\s", line):
            out.append("</ol>")
            in_ol = False

        # Headings
        hm = re.match(r"^(#{1,6})\s+(.+)$", line)
        if hm:
            level = len(hm.group(1))
            content = inline_md(hm.group(2))
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^(\*{3,}|-{3,}|_{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # Unordered list
        lm = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if lm:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_md(lm.group(1))}</li>")
            i += 1
            continue

        # Ordered list
        om = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if om:
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline_md(om.group(2))}</li>")
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            content = inline_md(line.lstrip(">").strip())
            out.append(f"<blockquote><p>{content}</p></blockquote>")
            i += 1
            continue

        # Table
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|", lines[i + 1]):
            table_html, consumed = parse_table(lines, i)
            out.append(table_html)
            i += consumed
            continue

        # Paragraph
        stripped = line.strip()
        if stripped:
            out.append(f"<p>{inline_md(stripped)}</p>")
        else:
            out.append("")

        i += 1

    if in_list:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")

    return "\n".join(out)


def inline_md(text):
    """Process inline Markdown: bold, italic, code, links, images."""
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Images before links
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    return text


def parse_table(lines, start):
    """Parse a Markdown table and return HTML."""
    header_cells = [c.strip() for c in lines[start].strip().strip("|").split("|")]
    i = start + 1
    # Skip separator
    if i < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|", lines[i]):
        i += 1
    rows = []
    while i < len(lines) and "|" in lines[i] and lines[i].strip():
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        rows.append(cells)
        i += 1
    consumed = i - start

    parts = ["<table><thead><tr>"]
    for cell in header_cells:
        parts.append(f"<th>{inline_md(cell)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for cell in row:
            parts.append(f"<td>{inline_md(cell)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts), consumed


def generate_toc(md_text):
    """Generate a table of contents from Markdown headings."""
    toc_items = []
    for m in re.finditer(r"^(#{1,6})\s+(.+)$", md_text, re.M):
        level = len(m.group(1))
        title = m.group(2).strip()
        anchor = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
        toc_items.append(f'{"  " * (level - 1)}<li><a href="#{anchor}">{inline_md(title)}</a></li>')
    if not toc_items:
        return ""
    return '<nav class="toc"><h2>Table of Contents</h2><ul>' + "".join(toc_items) + "</ul></nav>"


def add_heading_ids(html_text):
    """Add id attributes to heading tags for TOC linking."""
    def replacer(m):
        tag = m.group(1)
        content = m.group(2)
        anchor = re.sub(r"<[^>]+>", "", content)
        anchor = re.sub(r"[^\w\s-]", "", anchor.lower()).replace(" ", "-")
        return f'<{tag} id="{anchor}">{content}</{tag}>'
    return re.sub(r"<(h[1-6])>(.+?)</\1>", replacer, html_text)


def cmd_convert(args):
    try:
        md_text = Path(args.file).read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    body = md_to_html(md_text)

    if args.toc:
        toc = generate_toc(md_text)
        body = toc + "\n" + body

    body = add_heading_ids(body)

    style = STYLES.get(args.style, STYLES["plain"])
    title = html.escape(args.title or Path(args.file).stem)

    toc_css = (
        ".toc{background:#f8f9fa;border:1px solid #e1e4e8;border-radius:6px;padding:1em;margin-bottom:2em}"
        ".toc ul{list-style:none;padding-left:1em}"
        ".toc a{text-decoration:none}"
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{style}
{toc_css}
</style>
</head>
<body>
{body}
</body>
</html>"""

    if args.output:
        try:
            Path(args.output).write_text(page, encoding="utf-8")
            print(f"Written to {args.output}")
        except OSError as e:
            print(f"Error: cannot write {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(page)


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to standalone HTML.")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("convert", help="Convert a Markdown file to HTML")
    p.add_argument("--file", required=True, help="Input Markdown file")
    p.add_argument("--style", choices=list(STYLES.keys()), default="plain", help="CSS style (default: plain)")
    p.add_argument("--toc", action="store_true", help="Insert table of contents")
    p.add_argument("--title", help="HTML page title (default: filename stem)")
    p.add_argument("--output", help="Output HTML file (default: stdout)")

    args = parser.parse_args()
    if args.command == "convert":
        cmd_convert(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
