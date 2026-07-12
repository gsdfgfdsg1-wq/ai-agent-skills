# Usage

Create `openapi.json`:

```json
{
  "openapi": "3.0.3",
  "paths": {
    "/pets": {
      "get": {"operationId": "listPets", "tags": ["pets", "public"]},
      "post": {"operationId": "createPet", "tags": ["pets"]}
    },
    "/status": {"get": {"operationId": "getStatus", "tags": ["system"]}}
  }
}
```

List all operations or only tagged operations:

```bash
python scripts/openapi_path_inventory.py openapi.json
python scripts/openapi_path_inventory.py openapi.json --tag pets --json
```

Text output is tab-separated: `METHOD`, `PATH`, `operationId`, and comma-separated tags. Multiple `--tag` options match operations containing any selected tag. Invalid OpenAPI input and an empty filtered result exit with code `2`.
