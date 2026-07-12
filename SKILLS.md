# 技能目录 (Skills Catalog)

> 自动生成，共 21 个技能模块。请勿手动编辑，运行 `python tools/build_catalog.py` 更新。

| 模块 | 说明 |
| --- | --- |
| [a11y-audit](skills/a11y-audit/) | Statically audit HTML for common accessibility issues including missing document language, image alt text, control labels, accessible button names, heading jumps, and duplicate IDs. |
| [api-contract-test](skills/api-contract-test/) | Validate HTTP response status codes and JSON bodies against OpenAPI 3 JSON response schemas without external dependencies. Supports local refs and common JSON Schema constraints. |
| [broken-markdown-links](skills/broken-markdown-links/) | This skill should be used when checking local relative Markdown file links and heading anchors for broken references, including JSON output and CI exit codes. |
| [bundle-file-report](skills/bundle-file-report/) | This skill should be used when recursively ranking file sizes in a build or bundle directory, reporting the largest files, limiting output to Top N entries, or exporting file-size reports as JSON. |
| [changelog-generator](skills/changelog-generator/) | Generate grouped Markdown changelogs from git history using Conventional Commit messages. Supports revision ranges, release versions, dates, short hashes, and file output without dependencies. |
| [conventional-commit](skills/conventional-commit/) | Validate and generate commit messages that follow the Conventional Commits 1.0.0 specification — type(scope)!: description format, body wrapping, footers. |
| [csv-schema-audit](skills/csv-schema-audit/) | This skill should be used when auditing CSV headers and null values against a small JSON column schema, including required columns and duplicate-header detection. |
| [dockerfile-lint](skills/dockerfile-lint/) | Statically check Dockerfiles for common image security, reproducibility, and size issues without external dependencies. Supports JSON results and CI exit thresholds. |
| [env-schema-checker](skills/env-schema-checker/) | This skill should be used when validating a dotenv file against a JSON Schema, including required environment variables, disallowed keys, and basic value types. |
| [gitignore-audit](skills/gitignore-audit/) | This skill should be used when finding tracked Git files that match repository .gitignore rules and need cleanup review, including CI-friendly JSON output. |
| [http-fixture-redactor](skills/http-fixture-redactor/) | This skill should be used when redacting sensitive values in JSON HTTP fixtures by recursive field name or field-name regular expression matching. |
| [i18n-extractor](skills/i18n-extractor/) | This skill should be used when extracting user-facing literal strings from JavaScript or TypeScript t(...) and i18n.t(...) calls into a unique JSON translation catalog. |
| [json-config-diff](skills/json-config-diff/) | This skill should be used when comparing two JSON configuration files and reporting added, removed, or changed settings in text or JSON format. |
| [jsonl-deduper](skills/jsonl-deduper/) | This skill should be used when removing duplicate JSONL records by a specified dotted object key while keeping either the first or last occurrence and producing JSON statistics. |
| [license-auditor](skills/license-auditor/) | Audit local Node.js and Python dependency license metadata against allow and deny policies without external services. Supports strict mode, JSON, and CI exit codes. |
| [openapi-path-inventory](skills/openapi-path-inventory/) | This skill should be used when reading an OpenAPI JSON document to inventory HTTP methods, paths, operation IDs, and tags, optionally filtered by tag. |
| [perf-budget](skills/perf-budget/) | This skill should be used when checking individual file sizes against performance budgets, defining file-size rules, producing machine-readable JSON results, or enforcing size limits in CI. |
| [pr-review-checklist](skills/pr-review-checklist/) | Review pull request changes against a practical checklist for test coverage, documentation, dependencies, delivery files, and sensitive paths. Supports git diff, stdin, JSON, and CI exit codes. |
| [readme-section-audit](skills/readme-section-audit/) | This skill should be used when checking a Markdown README for required H2 sections, duplicate headings, and a bounded summary length in CI or local validation. |
| [release-note-linter](skills/release-note-linter/) | This skill should be used when linting Markdown release notes for version and date headings, required sections, unreleased markers, and consistent issue reference style in CI or local checks. |
| [secret-leak-scanner](skills/secret-leak-scanner/) | 扫描代码库中的 API Key、私钥、Token 等敏感凭证，支持 CI 退出码与 JSON 输出，防止密钥泄露被提交到仓库。 |
