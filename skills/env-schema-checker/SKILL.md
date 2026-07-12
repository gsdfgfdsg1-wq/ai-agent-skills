---
name: env-schema-checker
description: This skill should be used when validating a dotenv file against a JSON Schema, including required environment variables, disallowed keys, and basic value types.
agent_created: true
---

# Env Schema Checker

Validate a dotenv file with a deterministic standard-library Python script. Use this skill before deployment, configuration review, or CI checks.

## Workflow

1. Create a JSON Schema object with `required`, `properties`, and `additionalProperties: false` when unknown keys must fail.
2. Run `scripts/validate_env.py` with the dotenv and schema files.
3. Treat exit code `0` as valid, `1` as validation failures, and `2` as input or schema errors.
4. Pass `--json` when a program needs the result.

## Supported Rules

Support top-level `required`, `properties`, and `additionalProperties`. Support property `type` values `string`, `boolean`, `integer`, `number`, `array`, `object`, and `null`, plus `enum` and string `minLength`.

Parse `array` and `object` values as JSON. Parse boolean values as `true` or `false`. See [examples/usage.md](examples/usage.md) for a complete schema and commands.

## Resource

Run `scripts/validate_env.py --help` for command options.
