---
name: perf-budget
description: This skill should be used when checking individual file sizes against performance budgets, defining file-size rules, producing machine-readable JSON results, or enforcing size limits in CI.
agent_created: true
---

# Performance Budget

Check file sizes against explicit performance budgets. Use the bundled script for deterministic local checks and CI enforcement.

## Workflow

1. Identify the build output or other directory to inspect.
2. Define one or more rules with `--rule GLOB=LIMIT`. Match paths relative to the target directory using case-sensitive `fnmatch` glob patterns.
3. Run `scripts/check_perf_budget.py TARGET --rule ...`.
4. Add `--json` for structured output or CI logs that will be parsed by another tool.
5. Treat exit code `0` as passing and exit code `1` as a budget violation. Treat exit code `2` as invalid invocation or an unreadable target.

Require at least one rule. A file matches every applicable rule; the strictest applicable limit determines the result. Files with no matching rule are reported as `unmatched` and do not fail the check.

## Limits

Use a non-negative integer byte count or a binary unit: `B`, `KiB`, `MiB`, or `GiB`. Examples: `180KiB`, `1MiB`, `0B`.

Use `/` in globs on every platform. Examples:

```bash
python scripts/check_perf_budget.py dist \
  --rule '*.js=250KiB' \
  --rule 'assets/*.css=80KiB'
```

Use `**` only where the host `fnmatch` implementation supports the desired pattern; for portable recursive matching, prefer a broad suffix rule such as `*.js` or supply directory-specific rules.

## JSON Contract

Pass `--json` to emit one JSON object to standard output. The object contains:

- `target`: resolved target directory.
- `rules`: parsed rule objects with `glob` and `limit_bytes`.
- `files`: records with `path`, `size_bytes`, `matched_rules`, `limit_bytes`, and `status`.
- `summary`: counts for `checked`, `passing`, `violations`, and `unmatched`.

Statuses are `pass`, `violation`, or `unmatched`. Read `summary.violations` or the process exit code in CI rather than parsing human-readable text.

## CI

Run after assets have been generated and before deployment. Preserve the script exit code unchanged:

```bash
python skills/perf-budget/scripts/check_perf_budget.py build \
  --rule '*.js=300KiB' \
  --rule '*.css=100KiB' \
  --json
```

Do not use a shell wrapper that discards a non-zero status. A violation is an expected CI failure (`1`); malformed rules, missing rules, and nonexistent targets are invocation failures (`2`).

See [examples/usage.md](examples/usage.md) for complete commands and output examples.
