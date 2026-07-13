# Diff Highlight — Usage Examples

## 1. Unified diff with colors

```bash
python skills/diff-highlight/scripts/diff_highlight.py unified --left old.txt --right new.txt
```

## 2. Side-by-side diff

```bash
python skills/diff-highlight/scripts/diff_highlight.py side-by-side --left old.txt --right new.txt
```

## 3. Change statistics

```bash
python skills/diff-highlight/scripts/diff_highlight.py stats --left old.txt --right new.txt
```

```
Left:  old.txt (42 lines)
Right: new.txt (45 lines)
Changes: +5 added  -2 deleted  ~3 modified  (10 total)
```

## 4. JSON statistics

```bash
python skills/diff-highlight/scripts/diff_highlight.py stats --left old.txt --right new.txt --json
```

## 5. No color output (for piping)

```bash
python skills/diff-highlight/scripts/diff_highlight.py unified --left old.txt --right new.txt --no-color
```

## Error handling

Missing file:

```bash
python skills/diff-highlight/scripts/diff_highlight.py unified --left missing.txt --right new.txt
```

```
Error: cannot read missing.txt: [Errno 2] No such file or directory
```
