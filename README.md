# AI Agent Skills 🤖

> 一套即插即用的 AI Agent 技能模块集合。让 Claude Code / Cursor / Codex / WorkBuddy 等智能体，读一个 `SKILL.md` 就秒变领域专家。

每个技能模块都是**自包含、可直接运行**的：包含能力说明（`SKILL.md`）、可复用脚本（`scripts/`）和真实示例（`examples/`）。目标是持续产出高质量、解决实际问题的小工具，回馈开发者社区。

## ✨ 为什么会有这个仓库

- **即插即用**：把目录丢进智能体的 skills 目录就能用，零配置。
- **可运行、非纯提示词**：核心能力由真实脚本承载，可单独在终端使用。
- **持续更新**：通过自动化流水线，定期新增并验证新模块。

## 📦 如何使用

**Claude Code / Cursor / Codex**
```bash
# 复制你需要的技能到项目的 skills 目录
cp -r skills/secret-leak-scanner ~/.claude/skills/
```

**WorkBuddy**
```bash
cp -r skills/secret-leak-scanner ~/.workbuddy/skills/
```

**直接用脚本（不依赖任何智能体）**
```bash
python skills/secret-leak-scanner/scripts/scan.py ./your-project
```

## 🗂️ 技能目录

<!-- CATALOG_START -->

| 模块 | 说明 |
| --- | --- |
| [a11y-audit](skills/a11y-audit/) | Statically audit HTML for common accessibility issues including missing document language, image alt text, control labels, accessible button names, heading jumps, and duplicate IDs. |
| [api-contract-test](skills/api-contract-test/) | Validate HTTP response status codes and JSON bodies against OpenAPI 3 JSON response schemas without external dependencies. Supports local refs and common JSON Schema constraints. |
| [bundle-file-report](skills/bundle-file-report/) | This skill should be used when recursively ranking file sizes in a build or bundle directory, reporting the largest files, limiting output to Top N entries, or exporting file-size reports as JSON. |
| [changelog-generator](skills/changelog-generator/) | Generate grouped Markdown changelogs from git history using Conventional Commit messages. Supports revision ranges, release versions, dates, short hashes, and file output without dependencies. |
| [conventional-commit](skills/conventional-commit/) | Validate and generate commit messages that follow the Conventional Commits 1.0.0 specification — type(scope)!: description format, body wrapping, footers. |
| [dockerfile-lint](skills/dockerfile-lint/) | Statically check Dockerfiles for common image security, reproducibility, and size issues without external dependencies. Supports JSON results and CI exit thresholds. |
| [i18n-extractor](skills/i18n-extractor/) | This skill should be used when extracting user-facing literal strings from JavaScript or TypeScript t(...) and i18n.t(...) calls into a unique JSON translation catalog. |
| [license-auditor](skills/license-auditor/) | Audit local Node.js and Python dependency license metadata against allow and deny policies without external services. Supports strict mode, JSON, and CI exit codes. |
| [perf-budget](skills/perf-budget/) | This skill should be used when checking individual file sizes against performance budgets, defining file-size rules, producing machine-readable JSON results, or enforcing size limits in CI. |
| [pr-review-checklist](skills/pr-review-checklist/) | Review pull request changes against a practical checklist for test coverage, documentation, dependencies, delivery files, and sensitive paths. Supports git diff, stdin, JSON, and CI exit codes. |
| [secret-leak-scanner](skills/secret-leak-scanner/) | 扫描代码库中的 API Key、私钥、Token 等敏感凭证，支持 CI 退出码与 JSON 输出，防止密钥泄露被提交到仓库。 |

<!-- CATALOG_END -->

## 🛠️ 仓库自带的流水线工具

| 工具 | 作用 |
| --- | --- |
| `tools/scaffold_skill.py` | 按模板生成新技能骨架 |
| `tools/validate_skills.py` | 校验所有技能结构与脚本语法 |
| `tools/build_catalog.py` | 重新生成 `SKILLS.md` 与 README 目录 |
| `tools/publish.py` | 校验 → 生成目录 → 提交 →（有 token 时）推送 |

一键发布：
```bash
python tools/publish.py
```

## 🤝 贡献

欢迎提 Issue / PR，或把你写的技能按同样结构丢进 `skills/`。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 许可证

MIT —— 随便用，留个 ⭐ 就好。
