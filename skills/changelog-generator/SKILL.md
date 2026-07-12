---
name: changelog-generator
description: Generate grouped Markdown changelogs from git history using Conventional Commit messages. Supports revision ranges, release versions, dates, short hashes, and file output without dependencies.
license: MIT
---

# Conventional Changelog Generator

> 从 git 历史自动生成结构化 Markdown 变更日志，按功能、修复、文档、性能等 Conventional Commit 类型分组。

## 何时使用 / 触发条件
- 用户准备发版、创建 release 或需要维护 CHANGELOG。
- 仓库使用 Conventional Commits，想避免手工整理提交历史。
- CI/release 脚本要根据两个 tag 之间的提交生成发布说明。

## 能力概览
- 解析 `type(scope)!: description` 格式的 Conventional Commits。
- 分组：Features、Bug Fixes、Performance、Documentation、CI、Maintenance 等。
- Breaking change 额外汇总；非标准提交进入 Other Changes。
- 支持 `--range v1.0.0..HEAD`、版本、日期、短 hash 和写入文件。

## 使用方法

```bash
# 生成当前历史的 Unreleased 片段
python skills/changelog-generator/scripts/generate.py

# 从上一个 tag 到 HEAD 生成 v1.2.0 的发布说明
python skills/changelog-generator/scripts/generate.py \
  --range v1.1.0..HEAD --version 1.2.0 --include-hash \
  --output CHANGELOG-next.md
```

## 示例
见 `examples/usage.md`。