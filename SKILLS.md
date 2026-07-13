# 技能目录 (Skills Catalog)

> 自动生成，共 93 个技能模块。请勿手动编辑，运行 `python tools/build_catalog.py` 更新。

| 模块 | 说明 |
| --- | --- |
| [a11y-audit](skills/a11y-audit/) | Statically audit HTML for common accessibility issues including missing document language, image alt text, control labels, accessible button names, heading jumps, and duplicate IDs. |
| [api-contract-test](skills/api-contract-test/) | Validate HTTP response status codes and JSON bodies against OpenAPI 3 JSON response schemas without external dependencies. Supports local refs and common JSON Schema constraints. |
| [base64-toolkit](skills/base64-toolkit/) | Encode and decode Base64 strings with auto-detection, URL-safe mode, and file support without external dependencies. |
| [broken-markdown-links](skills/broken-markdown-links/) | This skill should be used when checking local relative Markdown file links and heading anchors for broken references, including JSON output and CI exit codes. |
| [bundle-file-report](skills/bundle-file-report/) | This skill should be used when recursively ranking file sizes in a build or bundle directory, reporting the largest files, limiting output to Top N entries, or exporting file-size reports as JSON. |
| [bundle-size-delta](skills/bundle-size-delta/) | Compare two build directories and report file-size increases, decreases, and new/removed files with percentage deltas without external dependencies. |
| [changelog-generator](skills/changelog-generator/) | Generate grouped Markdown changelogs from git history using Conventional Commit messages. Supports revision ranges, release versions, dates, short hashes, and file output without dependencies. |
| [chmod-calculator](skills/chmod-calculator/) | Convert Unix file permissions between symbolic and octal notation with detailed breakdowns without external dependencies. |
| [color-converter](skills/color-converter/) | Convert between HEX, RGB, and HSL color formats with validation and preview without external dependencies. |
| [conventional-commit](skills/conventional-commit/) | Validate and generate commit messages that follow the Conventional Commits 1.0.0 specification — type(scope)!: description format, body wrapping, footers. |
| [cron-validator](skills/cron-validator/) | Validate standard 5-field and 6-field cron expressions, check field ranges and syntax, and compute next execution times without external dependencies. |
| [css-unused-finder](skills/css-unused-finder/) | Find CSS selectors in a stylesheet that are not referenced by any HTML files, helping reduce CSS bloat without external dependencies. |
| [csv-filter](skills/csv-filter/) | Filter CSV rows by column value conditions with comparison operators and regex matching without external dependencies. |
| [csv-merge](skills/csv-merge/) | Merge multiple CSV files by a common key column without external dependencies. |
| [csv-schema-audit](skills/csv-schema-audit/) | This skill should be used when auditing CSV headers and null values against a small JSON column schema, including required columns and duplicate-header detection. |
| [csv-to-json](skills/csv-to-json/) | Convert CSV files to JSON with automatic type inference and flexible delimiter support without external dependencies. |
| [dep-graph-generator](skills/dep-graph-generator/) | Analyze package.json or requirements.txt files and output dependency relationship data as JSON, DOT, or text for visualization and auditing. |
| [diff-highlight](skills/diff-highlight/) | Generate side-by-side and unified diffs with color-coded output and statistics without external dependencies. |
| [dns-lookup](skills/dns-lookup/) | Query DNS records (A, AAAA, CNAME, MX, TXT, NS, SOA) for a domain using the system resolver, with JSON and text output. |
| [docker-compose-lint](skills/docker-compose-lint/) | Lint docker-compose YAML files for best practices and common issues without external dependencies. |
| [dockerfile-lint](skills/dockerfile-lint/) | Statically check Dockerfiles for common image security, reproducibility, and size issues without external dependencies. Supports JSON results and CI exit thresholds. |
| [dotenv-comparator](skills/dotenv-comparator/) | Compare two .env files and report added, removed, and changed keys with value diff output without external dependencies. |
| [env-schema-checker](skills/env-schema-checker/) | This skill should be used when validating a dotenv file against a JSON Schema, including required environment variables, disallowed keys, and basic value types. |
| [envdoc](skills/envdoc/) | Generate documentation from .env files with variable names, defaults, and comments without external dependencies. |
| [escape-toolkit](skills/escape-toolkit/) | Escape and unescape strings for C, Python, HTML, JavaScript, and JSON contexts without external dependencies. |
| [git-branch-cleaner](skills/git-branch-cleaner/) | Find merged local branches and stale remote-tracking branches for safe cleanup without external dependencies. |
| [gitignore-audit](skills/gitignore-audit/) | This skill should be used when finding tracked Git files that match repository .gitignore rules and need cleanup review, including CI-friendly JSON output. |
| [gzip-toolkit](skills/gzip-toolkit/) | Compress and decompress files with gzip, inspect archive metadata, and test integrity without external dependencies. |
| [hash-checker](skills/hash-checker/) | Compute and verify file hashes (MD5/SHA1/SHA256/SHA512) without external dependencies. |
| [hex-converter](skills/hex-converter/) | Convert numbers between hexadecimal, binary, decimal, and octal formats without external dependencies. |
| [html-minifier](skills/html-minifier/) | Minify HTML by removing comments, collapsing whitespace, stripping optional tags, and eliminating redundant attributes — no external dependencies. |
| [html-table-extractor](skills/html-table-extractor/) | Extract table data from HTML files and convert to CSV or JSON without external dependencies. |
| [http-fixture-redactor](skills/http-fixture-redactor/) | This skill should be used when redacting sensitive values in JSON HTTP fixtures by recursive field name or field-name regular expression matching. |
| [http-header-checker](skills/http-header-checker/) | Check HTTP security response headers (CSP, HSTS, X-Frame-Options, etc.) for a URL and report missing or misconfigured headers. |
| [i18n-extractor](skills/i18n-extractor/) | This skill should be used when extracting user-facing literal strings from JavaScript or TypeScript t(...) and i18n.t(...) calls into a unique JSON translation catalog. |
| [image-meta-scraper](skills/image-meta-scraper/) | Extract image metadata including dimensions, format, file size, and basic EXIF data from JPEG/PNG/GIF/BMP/WebP files without external dependencies. |
| [ini-parser](skills/ini-parser/) | Parse, validate, and query INI configuration files without external dependencies. |
| [ip-geo-lookup](skills/ip-geo-lookup/) | Look up geographic location, ISP, and ASN info for IP addresses using the free ip-api.com service with JSON and text output. |
| [json-config-diff](skills/json-config-diff/) | This skill should be used when comparing two JSON configuration files and reporting added, removed, or changed settings in text or JSON format. |
| [json-flattener](skills/json-flattener/) | Flatten nested JSON objects to dot-notation key-value pairs and unflatten them back without external dependencies. |
| [json-mask](skills/json-mask/) | Mask sensitive fields in JSON by key name patterns with configurable redaction strategies without external dependencies. |
| [json-patch](skills/json-patch/) | Apply RFC 6902 JSON Patch operations (add, remove, replace, move, copy, test) without external dependencies. |
| [json-path-query](skills/json-path-query/) | Query JSON and JSONL files with JSONPath-like expressions without external dependencies. |
| [json-schema-linter](skills/json-schema-linter/) | Validate JSON files against a JSON Schema — supports type, required, properties, additionalProperties, enum, min/max, pattern, items, and nested objects using only the Python standard library. |
| [json-sort](skills/json-sort/) | Recursively sort JSON object keys alphabetically without external dependencies. |
| [jsonl-deduper](skills/jsonl-deduper/) | This skill should be used when removing duplicate JSONL records by a specified dotted object key while keeping either the first or last occurrence and producing JSON statistics. |
| [jwt-decoder](skills/jwt-decoder/) | Decode and inspect JWT tokens — display header and payload, optionally check expiration, issued-at, and not-before claims without signature verification or external dependencies. |
| [k8s-manifest-lint](skills/k8s-manifest-lint/) | Lint Kubernetes YAML manifests for best practices including resource limits, labels, probes, security contexts, and image tags without external dependencies. |
| [license-auditor](skills/license-auditor/) | Audit local Node.js and Python dependency license metadata against allow and deny policies without external services. Supports strict mode, JSON, and CI exit codes. |
| [line-counter](skills/line-counter/) | Count lines of code, blank lines, and comment lines by file extension without external dependencies. |
| [log-parser](skills/log-parser/) | Parse and summarize log files by level and pattern — supports Python logging, Apache, nginx, and plain prefix formats with level filtering, regex matching, and JSON output. |
| [lorem-generator](skills/lorem-generator/) | Generate Lorem ipsum placeholder text with configurable paragraphs, sentences, and words without external dependencies. |
| [makefile-lint](skills/makefile-lint/) | Lint Makefiles for common issues and best practices without external dependencies. |
| [markdown-linter](skills/markdown-linter/) | Check Markdown files for style issues — trailing whitespace, heading level jumps, long lines, missing EOF newline, multiple blank lines, inline HTML, and more — without external dependencies. |
| [markdown-to-html](skills/markdown-to-html/) | Convert Markdown files to standalone HTML with embedded CSS styling without external dependencies. |
| [markdown-toc](skills/markdown-toc/) | Generate a table of contents from Markdown headings without external dependencies. |
| [mime-type-checker](skills/mime-type-checker/) | Detect file MIME types from content and extension with a built-in mapping database without external dependencies. |
| [nginx-config-lint](skills/nginx-config-lint/) | Lint nginx configuration files for common issues and best practices without external dependencies. |
| [npm-audit-summary](skills/npm-audit-summary/) | Parse npm audit JSON output and summarize vulnerabilities by severity, package, and dependency path for quick triage. |
| [openapi-path-inventory](skills/openapi-path-inventory/) | This skill should be used when reading an OpenAPI JSON document to inventory HTTP methods, paths, operation IDs, and tags, optionally filtered by tag. |
| [openapi-to-markdown](skills/openapi-to-markdown/) | Convert OpenAPI 3 JSON specifications to human-readable Markdown documentation — covers info, servers, endpoints, parameters, request/response schemas, and component definitions without external dependencies. |
| [password-strength](skills/password-strength/) | Analyze password strength with entropy calculation, pattern detection, and scoring without external dependencies. |
| [perf-budget](skills/perf-budget/) | This skill should be used when checking individual file sizes against performance budgets, defining file-size rules, producing machine-readable JSON results, or enforcing size limits in CI. |
| [pip-req-extractor](skills/pip-req-extractor/) | Extract Python import statements from source files and generate requirements without external dependencies. |
| [port-checker](skills/port-checker/) | Check whether TCP ports on a host are open or closed with timeout control and batch scanning without external dependencies. |
| [pr-review-checklist](skills/pr-review-checklist/) | Review pull request changes against a practical checklist for test coverage, documentation, dependencies, delivery files, and sensitive paths. Supports git diff, stdin, JSON, and CI exit codes. |
| [py-dead-code](skills/py-dead-code/) | Detect unused imports and unreachable code in Python files using AST analysis without external dependencies. |
| [qr-code-generator](skills/qr-code-generator/) | Generate SVG-format QR codes from text or URLs without external dependencies. |
| [readme-section-audit](skills/readme-section-audit/) | This skill should be used when checking a Markdown README for required H2 sections, duplicate headings, and a bounded summary length in CI or local validation. |
| [regex-tester](skills/regex-tester/) | Test regular expressions against sample strings, outputting match results, groups, and positions without external dependencies. |
| [release-note-linter](skills/release-note-linter/) | This skill should be used when linting Markdown release notes for version and date headings, required sections, unreleased markers, and consistent issue reference style in CI or local checks. |
| [secret-leak-scanner](skills/secret-leak-scanner/) | 扫描代码库中的 API Key、私钥、Token 等敏感凭证，支持 CI 退出码与 JSON 输出，防止密钥泄露被提交到仓库。 |
| [semver-checker](skills/semver-checker/) | Parse, compare, and validate semantic version strings with range constraint checking without external dependencies. |
| [shellcheck-lite](skills/shellcheck-lite/) | Lightweight static checker for shell scripts — detects unquoted variables, missing shebangs, deprecated backtick syntax, unsafe cd, useless cat and more without external dependencies. |
| [slug-generator](skills/slug-generator/) | Generate URL-safe slugs from text with transliteration, custom separators, and case control without external dependencies. |
| [sql-injection-scanner](skills/sql-injection-scanner/) | Scan source code for potential SQL injection patterns including string concatenation, format strings, and unsafe ORM usage with JSON and CI support. |
| [ssl-cert-checker](skills/ssl-cert-checker/) | Check SSL/TLS certificate validity, expiration, and chain details for a domain without external dependencies. |
| [svg-optimizer](skills/svg-optimizer/) | Remove bloat from SVG files — strip comments, metadata, editor namespaces, default attributes, and excess whitespace to produce smaller SVGs without external dependencies. |
| [swagger-to-markdown](skills/swagger-to-markdown/) | Convert Swagger/OpenAPI 2.0 JSON specifications to human-readable Markdown documentation without external dependencies. |
| [tar-toolkit](skills/tar-toolkit/) | List, create, and extract tar archives with inspection and integrity checking without external dependencies. |
| [terraform-plan-summarizer](skills/terraform-plan-summarizer/) | Parse terraform plan JSON output and generate a concise summary of creates, updates, deletes, and changes for review. |
| [text-diff](skills/text-diff/) | Word-level text diff with categorized additions, deletions, and changes without external dependencies. |
| [timestamp-converter](skills/timestamp-converter/) | Convert between Unix timestamps, ISO 8601, and human-readable date formats without external dependencies. |
| [todo-scanner](skills/todo-scanner/) | Scan a codebase for TODO, FIXME, HACK, XXX and other annotation comments, grouping them by tag and file with JSON, summary, and CI exit-code support. |
| [todo-to-issue](skills/todo-to-issue/) | Scan source code for TODO/FIXME/HACK comments and convert them to GitHub Issue format with labels, assignees, and file references without external dependencies. |
| [toml-linter](skills/toml-linter/) | Lint and validate TOML configuration files for common issues without external dependencies. |
| [unicode-info](skills/unicode-info/) | Look up Unicode character information including name, category, codepoint, and block without external dependencies. |
| [url-encoder](skills/url-encoder/) | Encode and decode URLs and query parameters with component-level control without external dependencies. |
| [utf8-validator](skills/utf8-validator/) | Validate files for correct UTF-8 encoding and report byte-level errors without external dependencies. |
| [uuid-generator](skills/uuid-generator/) | Generate UUID v4 and v5, validate UUID strings, and inspect UUID components without external dependencies. |
| [xml-linter](skills/xml-linter/) | Lint XML files for common issues including unclosed tags, encoding declarations, and well-formedness without external dependencies. |
| [xml-to-json](skills/xml-to-json/) | Convert XML files to JSON format with attribute and namespace handling without external dependencies. |
| [yaml-linter](skills/yaml-linter/) | Check YAML files for common issues — tabs in indentation, trailing whitespace, inconsistent indent, duplicate keys, missing document markers, long lines, and colon spacing — without a full parser or external dependencies. |
