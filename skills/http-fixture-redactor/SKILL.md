---
name: http-fixture-redactor
description: This skill should be used when redacting sensitive values in JSON HTTP fixtures by recursive field name or field-name regular expression matching.
agent_created: true
---

# HTTP Fixture Redactor

Redact sensitive JSON fixture values deterministically with a standard-library Python script. Apply this skill before committing, sharing, or snapshotting HTTP responses that can contain credentials, tokens, identifiers, or contact data.

## Workflow

1. Identify exact case-insensitive field names with `--field`, such as `password`, `token`, or `authorization`.
2. Identify groups of field names with `--field-regex`, such as `(?i)(api[_-]?key|secret)$`.
3. Run `scripts/redact_json_fixture.py INPUT --output OUTPUT` with one or more matching rules.
4. Review the resulting JSON fixture and confirm only intended fields contain the replacement value.
5. Pass `--replacement` to use a value other than `[REDACTED]`.

## Behavior

Traverse JSON objects and arrays recursively. Match object keys only; retain matched keys and replace their entire values without descending into those values. Match `--field` names case-insensitively. Compile every `--field-regex` with Python regular expressions and match it against complete field names. Preserve JSON structure, write UTF-8 formatted JSON, and exit `2` for invalid input, invalid patterns, missing rules, or write errors.

See [examples/usage.md](examples/usage.md) for commands and expected output.

## Resource

Run `scripts/redact_json_fixture.py --help` for all command options.
