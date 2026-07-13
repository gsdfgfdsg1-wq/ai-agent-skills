# GraphQL Schema Lint Examples

Lint a schema:

```bash
python skills/graphql-schema-lint/scripts/graphql_schema_lint.py schema.graphql
```

Example input:

```graphql
type user {
  UserName: String
}

type user {
  id: ID!
}
```

Example output:

```text
Issues in schema.graphql:
  line 1: [type-name] type name 'user' must use PascalCase
  line 2: [field-name] field name 'UserName' must use lowerCamelCase
  line 5: [type-name] type name 'user' must use PascalCase
  line 5: [duplicate-type-definition] type 'user' was already defined on line 1
Total: 4 issue(s)
```

Apply a line-length limit and emit JSON:

```bash
python skills/graphql-schema-lint/scripts/graphql_schema_lint.py schema.graphql --max-line-length 100 --json
```

The command exits with code `1` when it finds any issue.
