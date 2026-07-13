---
name: graphql-schema-lint
description: Lint GraphQL SDL schema files for basic type and field naming, duplicate definitions, unmatched braces, and optional line-length limits without graphql dependencies.
license: MIT
agent_created: true
---

# GraphQL Schema Lint

Perform practical text-based checks on GraphQL Schema Definition Language files without installing `graphql`. Report structural and naming problems suitable for local validation and CI.

## When to Use

- Check GraphQL SDL files before schema publication.
- Enforce basic naming conventions in a lightweight CI job.
- Inspect generated schema files where a full GraphQL parser is unavailable.

## Usage

```bash
python skills/graphql-schema-lint/scripts/graphql_schema_lint.py schema.graphql
python skills/graphql-schema-lint/scripts/graphql_schema_lint.py schema.graphql --max-line-length 100
python skills/graphql-schema-lint/scripts/graphql_schema_lint.py schema.graphql --json
```

Return exit code `1` when any issue is found and `0` when the file is clean.

## Rules

- Named type definitions and extensions must use PascalCase names.
- Field names must use lowerCamelCase names.
- A named type may be defined only once.
- Braces must be balanced after stripping comments and string literals.
- `--max-line-length` reports lines that exceed the requested limit.

## Scope

Treat the file as GraphQL SDL text rather than a complete GraphQL parser. Handle ordinary `type`, `interface`, `input`, `enum`, `union`, `scalar`, `directive`, and `schema` declarations plus their extensions.

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/graphql_schema_lint.py --help` for command options.
