# Usage

Run the script from any directory with Python 3.9 or later.

## Check a build directory

```bash
python skills/perf-budget/scripts/check_perf_budget.py build \
  --rule '*.js=250KiB' \
  --rule '*.css=100KiB'
```

Example output:

```text
PASS      102400 B <= 256000 B  app.js
VIOLATION 300000 B > 102400 B   styles.css
Summary: 2 checked, 1 passing, 1 violation, 0 unmatched
```

The process exits with `1` because `styles.css` exceeds its limit.

## Emit JSON for CI

```bash
python skills/perf-budget/scripts/check_perf_budget.py dist \
  --rule 'assets/*.js=300KiB' \
  --rule 'assets/*.css=90KiB' \
  --json
```

The output is one JSON object. Use `summary.violations` to publish a metric and the process status to fail the CI job.

## Enforce a zero-byte rule

```bash
python skills/perf-budget/scripts/check_perf_budget.py dist --rule '*.map=0B'
```

This catches source maps that were accidentally included in a production directory.

## Invocation errors

```bash
python skills/perf-budget/scripts/check_perf_budget.py dist --rule '*.js=250KB'
```

`KB` is intentionally rejected. Use binary units such as `KiB` or an exact byte count. Invalid input exits with `2`.
