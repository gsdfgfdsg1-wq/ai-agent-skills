# 技能生产待办（Backlog）

自动化流水线每次运行会挑选第一个 `pending` 的点子，生产完成后标记为 `done`。

| 状态 | 技能点子 | 解决的问题 | slug |
| --- | --- | --- | --- |
| done | 密钥泄露扫描器 | 扫描代码库中的 API Key / 私钥等敏感信息 | secret-leak-scanner |
| done | 约定式提交助手 | 生成符合 Conventional Commits 的提交信息 | conventional-commit |
| done | PR 审查清单 | 提交前自动对照常见 PR 审查项 | pr-review-checklist |
| done | Dockerfile 最佳实践检查 | 检查 Dockerfile 的安全与体积问题 | dockerfile-lint |
| done | OpenAPI 契约测试 | 校验实现与 API 契约是否一致 | api-contract-test |
| done | 变更日志生成器 | 根据 git 历史自动生成 CHANGELOG | changelog-generator |
| done | 依赖许可证审计 | 检查依赖的许可证是否合规 | license-auditor |
| done | 无障碍审计 | 检查前端常见 a11y 问题 | a11y-audit |
| done | 性能预算检查 | CI 中校验包体积/性能预算 | perf-budget |
| done | 构建产物体积报告 | 递归统计并排序构建产物的文件体积 | bundle-file-report |
| done | i18n 文案抽取 | 从代码中抽取待翻译文案 | i18n-extractor |
| done | 环境变量 Schema 校验 | 校验 dotenv 必填键、允许键与基础类型 | env-schema-checker |
| done | JSON 配置差异 | 递归输出 JSON 配置的新增、删除和变更 | json-config-diff |
| done | CSV Schema 审计 | 校验 CSV 表头、必填列和非空规则 | csv-schema-audit |
| done | JSONL 去重 | 按 dotted key 对 JSONL 数据去重 | jsonl-deduper |
| done | Gitignore 审计 | 发现已跟踪但应被 ignore 的文件 | gitignore-audit |
| done | Markdown 链接检查 | 检查本地 Markdown 文件与锚点链接 | broken-markdown-links |
| done | HTTP Fixture 脱敏 | 按字段名和正则递归脱敏 JSON fixture | http-fixture-redactor |
| done | OpenAPI 路径清单 | 输出 OpenAPI 方法、路径、标签和 operationId | openapi-path-inventory |
| done | README 章节审计 | 校验 README 的必需章节、重复标题和摘要 | readme-section-audit |
| done | 发布说明检查 | 校验版本发布说明的标题、章节和 issue 引用 | release-note-linter |
