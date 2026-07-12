# 技能生产待办（Backlog）

自动化流水线每次运行会挑选第一个 `pending` 的点子，生产完成后标记为 `done`。

| 状态 | 技能点子 | 解决的问题 | slug |
| --- | --- | --- | --- |
| done | 密钥泄露扫描器 | 扫描代码库中的 API Key / 私钥等敏感信息 | secret-leak-scanner |
| done | 约定式提交助手 | 生成符合 Conventional Commits 的提交信息 | conventional-commit |
| done | PR 审查清单 | 提交前自动对照常见 PR 审查项 | pr-review-checklist |
| done | Dockerfile 最佳实践检查 | 检查 Dockerfile 的安全与体积问题 | dockerfile-lint |
| done | OpenAPI 契约测试 | 校验实现与 API 契约是否一致 | api-contract-test |
| pending | 变更日志生成器 | 根据 git 历史自动生成 CHANGELOG | changelog-generator |
| pending | 依赖许可证审计 | 检查依赖的许可证是否合规 | license-auditor |
| pending | 无障碍审计 | 检查前端常见 a11y 问题 | a11y-audit |
| pending | 性能预算检查 | CI 中校验包体积/性能预算 | perf-budget |
| pending | i18n 文案抽取 | 从代码中抽取待翻译文案 | i18n-extractor |
