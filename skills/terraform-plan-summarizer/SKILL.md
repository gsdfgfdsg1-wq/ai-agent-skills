---
name: terraform-plan-summarizer
description: Parse terraform plan JSON output and generate a concise summary of creates, updates, deletes, and changes for review.
license: MIT
---

# Terraform Plan Summarizer

> Parse `terraform plan -json` output and produce a concise change summary for review.

## When to Use / Triggers

- Before applying terraform changes, review what will be created/updated/deleted.
- In CI/CD, generate a plan summary as a PR comment.
- Team review, quickly understand blast radius of infrastructure changes.
- Audit, track what resources changed between runs.

## Capabilities

- Parses terraform plan JSON (from `terraform show -json` or `terraform plan -json`).
- Groups changes by action (create, update, delete, recreate).
- Shows resource type distribution.
- Highlights potentially dangerous changes (force-new, destroy).
- `--json` for machine-readable output.
- `--exit-code` for CI integration — fail on destructive changes.

## Usage

```bash
# Summarize a saved plan
python skills/terraform-plan-summarizer/scripts/summarize_plan.py plan.json

# From stdin
terraform show -json plan.tfplan | python skills/terraform-plan-summarizer/scripts/summarize_plan.py -

# Fail on destructive changes
python skills/terraform-plan-summarizer/scripts/summarize_plan.py plan.json --exit-code
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/summarize_plan.py --help` for all options.
