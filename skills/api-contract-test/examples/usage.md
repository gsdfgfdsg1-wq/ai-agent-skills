# OpenAPI Contract Test - 使用示例

`openapi.json`：

```json
{
  "openapi": "3.0.3",
  "paths": {
    "/users/{id}": {
      "get": {
        "responses": {
          "200": {
            "description": "User found",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "required": ["id", "email"],
                  "properties": {
                    "id": {"type": "integer", "minimum": 1},
                    "email": {"type": "string", "minLength": 3},
                    "role": {"type": "string", "enum": ["admin", "member"]}
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

`fixtures/user-42.json`：

```json
{"id": 42, "email": "ada@example.com", "role": "admin"}
```

验证：

```bash
python skills/api-contract-test/scripts/check_response.py \
  --spec openapi.json --method GET --path /users/42 --status 200 \
  --body fixtures/user-42.json
```

输出：

```text
PASS: GET /users/42 -> 200 matches the OpenAPI contract.
```

如果响应缺少 `email`，脚本将以退出码 `1` 失败，并输出：

```text
FAIL: 1 contract violation(s) for GET /users/42 -> 200
  - $: missing required property 'email'
```