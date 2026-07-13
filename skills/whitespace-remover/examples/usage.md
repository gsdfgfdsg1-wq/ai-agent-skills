# whitespace-remover Usage Examples

## Input

Suppose `draft.txt` contains trailing spaces, tabs, and extra blank lines:

```text
First line   
Second line	


```

## Preview without writing

```bash
python scripts/whitespace_remover.py draft.txt --dry-run
```

Output:

```text
First line
Second line
```

## Check from CI

```bash
python scripts/whitespace_remover.py draft.txt --check
```

For the input above, the command writes this to stderr and exits with status `1`:

```text
needs normalization: draft.txt
```

After normalization, `--check` prints `already normalized: draft.txt` and exits with status `0`.

## Rewrite the source file

```bash
python scripts/whitespace_remover.py draft.txt --in-place
```

The command rewrites `draft.txt` with normalized content only when it changed.

## Write a separate file

```bash
python scripts/whitespace_remover.py draft.txt --output draft.cleaned.txt
```

`draft.txt` is unchanged and `draft.cleaned.txt` contains the normalized content.

## Pipe normalized content

Without a write option, output goes to stdout:

```bash
python scripts/whitespace_remover.py draft.txt > draft.cleaned.txt
```
