---
name: dockerfile-lint
description: Statically check Dockerfiles for common image security, reproducibility, and size issues without external dependencies. Supports JSON results and CI exit thresholds.
license: MIT
---

# Dockerfile Best Practices Linter

> 在构建镜像前检查 Dockerfile 的可复现性、最小化和安全运行原则，避免常见的镜像交付问题。

## 何时使用 / 触发条件
- 用户修改 Dockerfile、准备构建或发布容器镜像。
- PR 涉及镜像构建、部署或供应链风险审查。
- CI 需要一个无需安装外部 linter 的 Dockerfile 基础门禁。

## 能力概览
- 检查未固定或 `latest` 的基础镜像。
- 检查 `ADD` 的误用、全量构建上下文复制和疑似凭证文件复制。
- 检查 apt/pip 缓存、远程脚本直接执行、未声明非 root 用户。
- `--json` 输出适合 CI 归档，`--fail-on` 可按 review/warning 阈值使构建失败。

## 使用方法

```bash
# 检查默认 Dockerfile
python skills/dockerfile-lint/scripts/lint.py

# 检查指定文件并输出 JSON
python skills/dockerfile-lint/scripts/lint.py docker/Dockerfile --json

# CI：warning 时失败
python skills/dockerfile-lint/scripts/lint.py Dockerfile --fail-on warning
```

## 示例
见 `examples/usage.md`。