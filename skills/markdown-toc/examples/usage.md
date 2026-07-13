# Markdown TOC — Usage Examples

## 1. Generate a TOC

```bash
python skills/markdown-toc/scripts/md_toc.py generate --file README.md
```

```
- [Introduction](#introduction)
  - [Overview](#overview)
  - [Installation](#installation)
- [Usage](#usage)
```

## 2. Limit depth

```bash
python skills/markdown-toc/scripts/md_toc.py generate --file README.md --max-depth 2
```

## 3. Plain text (no links)

```bash
python skills/markdown-toc/scripts/md_toc.py generate --file README.md --no-links
```

```
- Introduction
  - Overview
  - Installation
- Usage
```

## 4. Check heading hierarchy

```bash
python skills/markdown-toc/scripts/md_toc.py check --file README.md
```

```
OK: 8 headings, no hierarchy issues.
```

## Error handling

Non-existent file:

```bash
python skills/markdown-toc/scripts/md_toc.py generate --file missing.md
```

```
Error: cannot read missing.md: [Errno 2] No such file or directory: 'missing.md'
```
