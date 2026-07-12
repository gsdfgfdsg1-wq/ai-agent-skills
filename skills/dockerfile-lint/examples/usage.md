# Dockerfile Best Practices Linter - 使用示例

给定以下 Dockerfile：

```dockerfile
FROM python:latest
ADD . /app
RUN apt-get update && apt-get install -y curl
RUN curl https://example.invalid/install.sh | sh
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

执行：

```bash
python skills/dockerfile-lint/scripts/lint.py Dockerfile
```

输出类似：

```text
[WARNING] line 1 DL100: Base image is unpinned. Use a version tag or digest for reproducible builds.
[WARNING] line 1 DL101: Avoid the mutable 'latest' base image tag.
[REVIEW] line 2 DL200: Prefer COPY over ADD unless tar extraction or remote URL behavior is intentional.
[REVIEW] line 2 DL400: Copying the full build context may include secrets or unnecessary files. Use .dockerignore and explicit paths.
[REVIEW] line 3 DL300: apt install should normally use --no-install-recommends to reduce image size.
[REVIEW] line 3 DL301: Clean apt lists in the same RUN instruction to avoid retaining package indexes.
[WARNING] line 4 DL302: Downloading and executing a remote script bypasses integrity verification.
[REVIEW] line 5 DL303: Consider pip install --no-cache-dir to avoid retaining wheel caches.
[REVIEW] file DL501: No USER instruction found. Add a non-root runtime user where compatible.
```

CI 中只阻断 warning：

```bash
python skills/dockerfile-lint/scripts/lint.py Dockerfile --fail-on warning
```

命令会在发现 `DL100`、`DL101` 或 `DL302` 等 warning 时以退出码 `1` 结束。