# 技能目录 (Skills Catalog)

> 自动生成，共 41 个技能模块。请勿手动编辑，运行 `python tools/build_catalog.py` 更新。

| 模块 | 说明 |
| --- | --- |
| [a11y-audit](skills/a11y-audit/) | Statically audit HTML for common accessibility issues including missing document language, image alt text, control labels, accessible button names, heading jumps, and duplicate IDs. |
| [api-contract-test](skills/api-contract-test/) | Validate HTTP response status codes and JSON bodies against OpenAPI 3 JSON response schemas without external dependencies. Supports local refs and common JSON Schema constraints. |
| [broken-markdown-links](skills/broken-markdown-links/) | This skill should be used when checking local relative Markdown file links and heading anchors for broken references, including JSON output and CI exit codes. |
| [bundle-file-report](skills/bundle-file-report/) | This skill should be used when recursively ranking file sizes in a build or bundle directory, reporting the largest files, limiting output to Top N entries, or exporting file-size reports as JSON. |
| [changelog-generator](skills/changelog-generator/) | Generate grouped Markdown changelogs from git history using Conventional Commit messages. Supports revision ranges, release versions, dates, short hashes, and file output without dependencies. |
| [conventional-commit](skills/conventional-commit/) | Validate and generate commit messages that follow the Conventional Commits 1.0.0 specification — type(scope)!: description format, body wrapping, footers. |
| [cron-validator](skills/cron-validator/) | Validate standard 5-field and 6-field cron expressions, check field ranges and syntax, and compute next execution times without external dependencies. |
| [css-unused-finder](skills/css-unused-finder/) | Find CSS selectors in a stylesheet that are not referenced by any HTML files, helping reduce CSS bloat without external dependencies. |
| [csv-schema-audit](skills/csv-schema-audit/) | This skill should be used when auditing CSV headers and null values against a small JSON column schema, including required columns and duplicate-header detection. |
| [dep-graph-generator](skills/dep-graph-generator/) | Analyze package.json or requirements.txt files and output dependency relationship data as JSON, DOT, or text for visualization and auditing. |
| [dns-lookup](skills/dns-lookup/) | Query DNS records (A, AAAA, CNAME, MX, TXT, NS, SOA) for a domain using the system resolver, with JSON and text output. |
| [dockerfile-lint](skills/dockerfile-lint/) | Statically check Dockerfiles for common image security, reproducibility, and size issues without external dependencies. Supports JSON results and CI exit thresholds. |
| [env-schema-checker](skills/env-schema-checker/) | This skill should be used when validating a dotenv file against a JSON Schema, including required environment variables, disallowed keys, and basic value types. |
| [gitignore-audit](skills/gitignore-audit/) | This skill should be used when finding tracked Git files that match repository .gitignore rules and need cleanup review, including CI-friendly JSON output. |
| [html-minifier](skills/html-minifier/) | Minify HTML by removing comments, collapsing whitespace, stripping optional tags, and eliminating redundant attributes — no external dependencies. |
| [http-fixture-redactor](skills/http-fixture-redactor/) | This skill should be used when redacting sensitive values in JSON HTTP fixtures by recursive field name or field-name regular expression matching. |
| [http-header-checker](skills/http-header-checker/) | Check HTTP security response headers (CSP, HSTS, X-Frame-Options, etc.) for a URL and report missing or misconfigured headers. |
| [i18n-extractor](skills/i18n-extractor/) | This skill should be used when extracting user-facing literal strings from JavaScript or TypeScript t(...) and i18n.t(...) calls into a unique JSON translation catalog. |
| [ip-geo-lookup](skills/ip-geo-lookup/) | Look up geographic location, ISP, and ASN info for IP addresses using the free ip-api.com service with JSON and text output. |
| [json-config-diff](skills/json-config-diff/) | This skill should be used when comparing two JSON configuration files and reporting added, removed, or changed settings in text or JSON format. |
| [json-schema-linter](skills/json-schema-linter/) | Validate JSON files against a JSON Schema — supports type, required, properties, additionalProperties, enum, min/max, pattern, items, and nested objects using only the Python standard library. |
| [jsonl-deduper](skills/jsonl-deduper/) | This skill should be used when removing duplicate JSONL records by a specified dotted object key while keeping either the first or last occurrence and producing JSON statistics. |
| [jwt-decoder](skills/jwt-decoder/) | Decode and inspect JWT tokens — display header and payload, optionally check expiration, issued-at, and not-before claims without signature verification or external dependencies. |
| [license-auditor](skills/license-auditor/) | Audit local Node.js and Python dependency license metadata against allow and deny policies without external services. Supports strict mode, JSON, and CI exit codes. |
| [log-parser](skills/log-parser/) | Parse and summarize log files by level and pattern — supports Python logging, Apache, nginx, and plain prefix formats with level filtering, regex matching, and JSON output. |
| [markdown-linter](skills/markdown-linter/) | Check Markdown files for style issues — trailing whitespace, heading level jumps, long lines, missing EOF newline, multiple blank lines, inline HTML, and more — without external dependencies. |
| [npm-audit-summary](skills/npm-audit-summary/) | Parse npm audit JSON output and summarize vulnerabilities by severity, package, and dependency path for quick triage. |
| [openapi-path-inventory](skills/openapi-path-inventory/) | This skill should be used when reading an OpenAPI JSON document to inventory HTTP methods, paths, operation IDs, and tags, optionally filtered by tag. |
| [openapi-to-markdown](skills/openapi-to-markdown/) | Convert OpenAPI 3 JSON specifications to human-readable Markdown documentation — covers info, servers, endpoints, parameters, request/response schemas, and component definitions without external dependencies. |
| [perf-budget](skills/perf-budget/) | This skill should be used when checking individual file sizes against performance budgets, defining file-size rules, producing machine-readable JSON results, or enforcing size limits in CI. |
| [pr-review-checklist](skills/pr-review-checklist/) | Review pull request changes against a practical checklist for test coverage, documentation, dependencies, delivery files, and sensitive paths. Supports git diff, stdin, JSON, and CI exit codes. |
| [readme-section-audit](skills/readme-section-audit/) | This skill should be used when checking a Markdown README for required H2 sections, duplicate headings, and a bounded summary length in CI or local validation. |
| [release-note-linter](skills/release-note-linter/) | This skill should be used when linting Markdown release notes for version and date headings, required sections, unreleased markers, and consistent issue reference style in CI or local checks. |
| [secret-leak-scanner](skills/secret-leak-scanner/) | 扫描代码库中的 API Key、私钥、Token 等敏感凭证，支持 CI 退出码与 JSON 输出，防止密钥泄露被提交到仓库。 |
| [shellcheck-lite](skills/shellcheck-lite/) | Lightweight static checker for shell scripts — detects unquoted variables, missing shebangs, deprecated backtick syntax, unsafe cd, useless cat and more without external dependencies. |
| [sql-injection-scanner](skills/sql-injection-scanner/) | Scan source code for potential SQL injection patterns including string concatenation, format strings, and unsafe ORM usage with JSON and CI support. |
| [ssl-cert-checker](skills/ssl-cert-checker/) | Check SSL/TLS certificate validity, expiration, and chain details for a domain without external dependencies. |
| [svg-optimizer](skills/svg-optimizer/) | Remove bloat from SVG files — strip comments, metadata, editor namespaces, default attributes, and excess whitespace to produce smaller SVGs without external dependencies. |
| [terraform-plan-summarizer](skills/terraform-plan-summarizer/) | Parse terraform plan JSON output and generate a concise summary of creates, updates, deletes, and changes for review. |
| [todo-scanner](skills/todo-scanner/) | Scan a codebase for TODO, FIXME, HACK, XXX and other annotation comments, grouping them by tag and file with JSON, summary, and CI exit-code support. |
| [yaml-linter](skills/yaml-linter/) | Check YAML files for common issues — tabs in indentation, trailing whitespace, inconsistent indent, duplicate keys, missing document markers, long lines, and colon spacing — without a full parser or external dependencies. |
