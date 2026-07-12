---
name: openapi-path-inventory
description: This skill should be used when reading an OpenAPI JSON document to inventory HTTP methods, paths, operation IDs, and tags, optionally filtered by tag.
agent_created: true
---

# OpenAPI Path Inventory

List OpenAPI operations from a JSON document with a deterministic standard-library Python script. Apply this skill to audit endpoint coverage, build an API inventory, or extract a tag-specific operation list.

## Workflow

1. Run `scripts/openapi_path_inventory.py OPENAPI.json` to print a tabular inventory.
2. Pass one or more `--tag` values to retain operations that contain any requested tag.
3. Pass `--json` to emit a structured array for downstream tools.
4. Review operations missing `operationId` or tags as incomplete metadata rather than silently excluding them.

## Behavior

Read JSON OpenAPI documents containing a top-level `paths` object. Inspect standard HTTP operation methods in deterministic method and path order: `GET`, `PUT`, `POST`, `DELETE`, `OPTIONS`, `HEAD`, `PATCH`, and `TRACE`. Ignore path-level metadata and non-operation keys. Report `method`, `path`, `operationId`, and `tags`; use an empty string for missing operation IDs and an empty list for missing tags. Interpret repeated `--tag` filters as an any-match filter. Exit `2` for unreadable or invalid JSON, an invalid OpenAPI shape, or no matching operations after filtering.

See [examples/usage.md](examples/usage.md) for commands and output shape.

## Resource

Run `scripts/openapi_path_inventory.py --help` for all command options.
