# Usage Examples

## 1. Dry run — check savings

```bash
python skills/svg-optimizer/scripts/optimize_svg.py icons/
```

Output:

```text
icons/logo.svg: 12450 -> 8320 (saved 4130 bytes (33.2%))
icons/arrow.svg: 1520 -> 980 (saved 540 bytes (35.5%))
```

## 2. Write optimized files to a directory

```bash
python skills/svg-optimizer/scripts/optimize_svg.py icons/ -o dist/icons/
```

Optimized files are written to `dist/icons/` without modifying originals.

## 3. In-place optimization

```bash
python skills/svg-optimizer/scripts/optimize_svg.py logo.svg --in-place
```

Overwrites the original file with the optimized version.

## 4. Aggressive mode

```bash
python skills/svg-optimizer/scripts/optimize_svg.py . --aggressive --in-place
```

Removes additional elements like empty groups, titles, and descriptions.

## 5. JSON output

```bash
python skills/svg-optimizer/scripts/optimize_svg.py icons/ --json
```

Returns a JSON array with `file`, `original_size`, `optimized_size`, `savings_bytes`, `savings_pct` per file.
