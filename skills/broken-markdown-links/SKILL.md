---
name: broken-markdown-links
description: This skill should be used when checking local relative Markdown file links and heading anchors for broken references, including JSON output and CI exit codes.
agent_created: true
---

# Broken Markdown Links

Check local relative Markdown links and anchors without accessing the network. Use the bundled standard-library Python script to validate file targets, page-local anchors, and anchors in linked Markdown files.

## Workflow

1. Run `python scripts/check_markdown_links.py PATH`, where `PATH` is a Markdown file or directory.
2. Review every reported source file, line, target, and failure reason.
3. Pass `--json` for structured CI output.
4. Treat exit code `0` as no broken local Markdown links, `1` as one or more link failures, and `2` as an invalid input path or unreadable Markdown file.

Check Markdown inline links and reference definitions that point to targets such as `guide.md#install`. Ignore web URLs, email links, absolute paths, protocol-relative URLs, and image links. Resolve relative targets from the source Markdown file. Derive anchors from ATX headings by lowercasing text, removing Markdown formatting and punctuation, and replacing whitespace with hyphens.

See [examples/usage.md](examples/usage.md) for commands and sample output. Run `scripts/check_markdown_links.py --help` for all options.

## Limits

Keep the checker focused on local repository documentation. It does not fetch remote URLs, interpret HTML anchors, validate generated sites, or fully implement every Markdown dialect.