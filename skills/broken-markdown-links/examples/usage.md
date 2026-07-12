# Usage

Check every Markdown file below a documentation directory:

```bash
python scripts/check_markdown_links.py docs
```

Check one file and emit JSON for CI:

```bash
python scripts/check_markdown_links.py README.md --json
```

A valid link can point at a local file and heading:

```markdown
[Install](guide/setup.md#quick-start)
```

Example JSON failure:

```json
{
  "valid": false,
  "error_count": 1,
  "errors": [
    {
      "file": "README.md",
      "line": 12,
      "target": "guide/setup.md#quick-start",
      "reason": "target anchor not found"
    }
  ]
}
```

The command exits `0` when every checked local Markdown link resolves, `1` when it reports broken links, and `2` for invalid input or unreadable source files. HTTP(S), mailto, absolute, and image links are intentionally ignored.