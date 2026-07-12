---
name: api-contract-test
description: Validate HTTP response status codes and JSON bodies against OpenAPI 3 JSON response schemas without external dependencies. Supports local refs and common JSON Schema constraints.
license: MIT
---

# OpenAPI Contract Test

> 将真实接口响应与 OpenAPI 3 契约比对，及时发现状态码、内容类型和 JSON 数据结构漂移。

## 何时使用 / 触发条件
- 用户需要验证 API 实现是否仍符合 OpenAPI 契约。
- 后端改动、接口回归或发布前需要做响应 smoke test。
- CI 中已有响应 fixture，想加入轻量且不依赖第三方包的契约门禁。

## 能力概览
- 支持 OpenAPI 3 **JSON** 文档与本地 `$ref`。
- 校验 method、带 `{pathParam}` 的路径、响应状态码和 `application/json` 内容类型。
- 校验 schema 的 `type`、`required`、`properties`、`items`、`enum`、可空和基础长度/数值约束。
- 退出码：`0` 通过，`1` 契约不匹配，`2` 规范或调用参数不匹配。

## 使用方法

```bash
python skills/api-contract-test/scripts/check_response.py \
  --spec openapi.json --method GET --path /users/42 --status 200 \
  --body fixtures/user-42.json --content-type application/json
```

当前版本刻意只解析 JSON；如规范是 YAML，请先在 CI 中转换为 JSON，保持此工具零依赖。

## 示例
见 `examples/usage.md`。