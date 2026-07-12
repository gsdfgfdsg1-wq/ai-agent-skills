---
name: conventional-commit
description: Validate and generate commit messages that follow the Conventional Commits 1.0.0 specification — type(scope)!: description format, body wrapping, footers.
license: MIT
---

# Conventional Commit Helper

> 在 git commit 前校验信息是否符合 Conventional Commits 规范，或帮你生成合规的提交信息。

## 何时使用 / 触发条件
- 用户提交代码、创建 PR 前，需要检查 commit message 格式。
- 用户说"帮我写个 commit message"、"生成提交信息"或者"校验这条 commit"。
- CI 中作为 git hook 或 pre-commit 检查，阻止不合规的提交。

## 能力概览
- **校验** commit message 是否符合 Conventional Commits 1.0.0 规范（type、scope、breaking mark、body 72 字换行、footer 格式）。
- **生成** 规范的提交信息（支持 type、scope、breaking、body、footer）。
- 支持的 type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`。
- 校验规则：首行格式、首行 ≤72 字、body/footer ≤72 字、BREAKING CHANGE footer 格式。

## 使用方法

```bash
# 校验一条提交信息
python skills/conventional-commit/scripts/commit-msg.py validate "feat(cli): add dry-run mode"

# 从 COMMIT_EDITMSG 文件读取（适用于 git hook）
python skills/conventional-commit/scripts/commit-msg.py validate --file .git/COMMIT_EDITMSG

# 生成一条提交信息
python skills/conventional-commit/scripts/commit-msg.py generate \
  --type feat --scope auth --desc "implement OAuth2 refresh flow" \
  --body "Adds token refresh logic with automatic retry on 401." \
  --footer "Closes: #42"
```

## 示例
见 `examples/usage.md`。