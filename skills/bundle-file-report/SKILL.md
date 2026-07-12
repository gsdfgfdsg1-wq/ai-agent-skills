---
name: bundle-file-report
description: This skill should be used when recursively ranking file sizes in a build or bundle directory, reporting the largest files, limiting output to Top N entries, or exporting file-size reports as JSON.
agent_created: true
---

# Bundle File Report

Generate a deterministic, recursively collected file-size ranking. Use the bundled standard-library script to identify the largest output files before performance tuning or release review.

## Workflow

1. Select a directory containing generated assets, packages, or another file tree.
2. Run `scripts/bundle_file_report.py TARGET` to rank every discovered file by size.
3. Set `--top N` to restrict the report to the N largest files.
4. Set `--json` when a CI system or downstream tool needs structured data.
5. Use `--include GLOB` one or more times to limit the candidates to paths relative to the target directory.

The script recursively discovers regular files, excludes directories, and sorts records by size descending with path ascending as the deterministic tie-breaker. `--top` must be a non-negative integer. `--top 0` is a valid boundary value and returns an empty file list with full-tree totals.

## Commands

```bash
python scripts/bundle_file_report.py dist --top 20
python scripts/bundle_file_report.py dist --include '*.js' --top 10 --json
```

Use `/` in include patterns. Multiple `--include` arguments are combined as an OR condition. A report with no matching files is successful and returns exit code `0`.

## JSON Contract

Pass `--json` to write one JSON object to standard output. It contains:

- `target`: resolved source directory.
- `includes`: selected include globs; empty means all files.
- `top`: requested limit or `null` when unlimited.
- `files`: ranked records with `path` and `size_bytes`.
- `summary`: `total_files`, `total_size_bytes`, `reported_files`, and `reported_size_bytes`.

`total_*` values describe every included file before applying `--top`; `reported_*` values describe the entries in `files`. Consume the numeric byte counts for automated analysis.

## Exit Codes

- `0`: report generated, including zero matched files.
- `2`: invalid command-line options or a target that is not a readable directory.

Avoid parsing aligned text in automation. Add `--json` and parse the JSON object instead.

See [examples/usage.md](examples/usage.md) for commands and expected output.
