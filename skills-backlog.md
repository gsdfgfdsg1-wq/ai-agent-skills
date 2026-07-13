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
| done | TODO/FIXME 扫描器 | 扫描代码中 TODO/FIXME/HACK/XXX 注释并分类汇总 | todo-scanner |
| done | Shell 脚本静态检查 | 对 bash/sh 脚本做常见陷阱检查（未引用变量、未双引号等） | shellcheck-lite |
| done | Cron 表达式校验 | 校验 cron 表达式语法、范围并给出下次执行时间 | cron-validator |
| done | JWT 解码器 | 解码 JWT 令牌展示 header/payload，无需密钥验证 | jwt-decoder |
| done | YAML 代码检查 | 检查 YAML 文件的缩进、尾空格、Tab、重复键等常见问题 | yaml-linter |
| done | Markdown 风格检查 | 检查 Markdown 的行长度、标题层级、空白等风格问题 | markdown-linter |
| done | 日志摘要分析 | 按 level/pattern 解析和汇总日志文件 | log-parser |
| done | JSON Schema 校验 | 用 JSON Schema 校验 JSON 文件的字段类型、必填项和约束 | json-schema-linter |
| done | OpenAPI 转 Markdown | 将 OpenAPI/Swagger JSON 转为可读 Markdown 文档 | openapi-to-markdown |
| done | SVG 精简优化 | 移除 SVG 中的元数据/注释/空白，输出精简 SVG | svg-optimizer |
| done | npm 审计摘要 | 解析 npm audit 输出，按严重性分类汇总 | npm-audit-summary |
| done | 依赖图生成 | 分析 package.json / requirements.txt 生成依赖关系数据 | dep-graph-generator |
| done | HTTP 安全头检查 | 检查 URL 返回的 HTTP 安全响应头 | http-header-checker |
| done | SSL 证书检查 | 检查域名的 SSL 证书有效期和基本信息 | ssl-cert-checker |
| done | DNS 记录查询 | 查询域名的 A/CNAME/MX/TXT 等 DNS 记录 | dns-lookup |
| done | IP 地理查询 | 查询 IP 地址的地理位置信息 | ip-geo-lookup |
| done | CSS 未使用选择器 | 在 HTML 中查找未被引用的 CSS 选择器 | css-unused-finder |
| done | HTML 压缩 | 移除 HTML 中的空白/注释，输出压缩版本 | html-minifier |
| done | SQL 注入扫描 | 在代码中搜索潜在 SQL 注入模式 | sql-injection-scanner |
| done | Terraform Plan 摘要 | 解析 terraform plan JSON 输出，生成变更摘要 | terraform-plan-summarizer |
| done | K8s Manifest 检查 | 检查 Kubernetes YAML 的资源限制、标签等最佳实践 | k8s-manifest-lint |
| done | 正则表达式测试 | 用正则匹配样本字符串，输出匹配结果 | regex-tester |
| done | Base64 编解码 | 编码/解码 base64，自动检测编码格式 | base64-toolkit |
| done | Dotenv 对比 | 对比不同环境的 .env 文件，输出差异 | dotenv-comparator |
| done | Git 分支清理 | 查找已合并的本地分支和过期远程分支 | git-branch-cleaner |
| done | Swagger 转 Markdown | 同 openapi-to-markdown 的 OpenAPI 2.0 版本 | swagger-to-markdown |
| done | 图片元数据提取 | 提取图片的 EXIF/尺寸/格式信息 | image-meta-scraper |
| done | TODO 转 Issue | 将代码中的 TODO 注释转为 GitHub Issue 格式 | todo-to-issue |
| done | 死代码检测 | 检测 Python 中未使用的导入和不可达代码 | py-dead-code |
| done | 包体积趋势 | 对比两次构建的产物体积，输出涨跌报告 | bundle-size-delta |
| done | 文件哈希校验 | 计算和验证文件 MD5/SHA1/SHA256/SHA512 哈希 | hash-checker |
| done | 时间戳转换 | 在 Unix 时间戳、ISO 8601、可读日期之间互相转换 | timestamp-converter |
| done | 颜色格式转换 | 在 HEX/RGB/HSL 颜色格式之间互相转换 | color-converter |
| done | JSONPath 查询 | 用 JSONPath 表达式查询 JSON/JSONL 文件 | json-path-query |
| done | CSV 转 JSON | 将 CSV 文件转为 JSON，支持类型推断 | csv-to-json |
| done | URL 编解码 | 编码/解码 URL 和查询参数 | url-encoder |
| done | JSON 扁平化 | 将嵌套 JSON 展开/还原为扁平键值结构 | json-flattener |
| done | XML 转 JSON | 将 XML 文件转换为 JSON 格式 | xml-to-json |
| done | UUID 生成与校验 | 生成 UUID v4/v5 并校验 UUID 格式 | uuid-generator |
| done | Gzip 压缩工具 | 压缩/解压 gzip 文件 | gzip-toolkit |
| done | MIME 类型检测 | 根据文件内容/扩展名检测 MIME 类型 | mime-type-checker |
| done | Unicode 字符查询 | 查询 Unicode 字符的名称、分类和码位 | unicode-info |
| done | Python 依赖提取 | 从 Python 源码中提取 import 生成 requirements | pip-req-extractor |
| done | Nginx 配置检查 | 检查 nginx 配置文件的常见问题 | nginx-config-lint |
| done | Docker Compose 检查 | 检查 docker-compose YAML 的最佳实践 | docker-compose-lint |
| done | Makefile 检查 | 检查 Makefile 的常见问题和风格 | makefile-lint |
| done | JSON 排序 | 递归排序 JSON 键名 | json-sort |
| done | CSV 合并 | 按共同键列合并多个 CSV 文件 | csv-merge |
| done | 文本差异比较 | 逐词文本差异对比，分类增删改 | text-diff |
| done | UTF-8 校验 | 验证文件是否为有效 UTF-8 编码 | utf8-validator |
| done | INI 配置解析 | 解析和校验 INI 配置文件 | ini-parser |
| done | TOML 检查 | 检查和校验 TOML 配置文件 | toml-linter |
| pending | 端口检查 | 检查主机指定 TCP 端口是否开放 | port-checker |
| pending | Markdown 转 HTML | 将 Markdown 转为独立 HTML 文件 | markdown-to-html |
| pending | HTML 表格提取 | 从 HTML 中提取表格数据为 CSV/JSON | html-table-extractor |
| pending | JSON Patch | 应用 RFC 6902 JSON Patch 操作 | json-patch |
| pending | Dotenv 文档生成 | 从 .env 文件生成文档 | envdoc |
| pending | QR 码生成 | 从文本/URL 生成 SVG 格式 QR 码 | qr-code-generator |
| pending | Tar 归档工具 | 列出/解压/创建 tar 归档 | tar-toolkit |
| pending | 差异高亮 | 生成带颜色高亮的并排差异对比 | diff-highlight |
