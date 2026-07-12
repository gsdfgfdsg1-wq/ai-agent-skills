---
name: pr-review-checklist
description: Review pull request changes against a practical checklist for test coverage, documentation, dependencies, delivery files, and sensitive paths. Supports git diff, stdin, JSON, and CI exit codes.
license: MIT
---

# PR Review Checklist

> 将 PR 的文件变更转成可执行的审查清单，在人工 review 前发现测试、文档、依赖和交付风险。

## 何时使用 / 触发条件
- 用户要求审查 PR、检查变更影响或准备合并代码。
- 创建 PR 前，需要确认测试、文档、依赖和工作流变更是否齐全。
- CI 需要对危险文件名或缺失测试给出阻断信号。

## 能力概览
- 从 `git diff <base>...HEAD`、命令行文件列表或 stdin 读取改动。
- 对源码变更但未包含测试、源码变更但未更新文档给出审查提示。
- 标记依赖清单、锁文件、CI 工作流、部署配置、迁移和脚本等高影响文件。
- 对 `.env`、`credentials`、`secret`、私钥等可疑路径给出凭证核查提示。
- 支持 `--json` 供 CI 消费；`--fail-on-warning` 让高风险警告使任务失败。

## 使用方法

```bash
# 审查当前分支相对 main 的改动
python skills/pr-review-checklist/scripts/review.py --base main

# 审查 CI 提供的文件列表
printf "src/auth.py\n.github/workflows/release.yml\n" | \
  python skills/pr-review-checklist/scripts/review.py --stdin --json

# CI 模式：存在 warning 时失败
python skills/pr-review-checklist/scripts/review.py --base origin/main --fail-on-warning
```

## 示例
见 `examples/usage.md`。