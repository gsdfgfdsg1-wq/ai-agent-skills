# Usage Examples

## 1. Lint a single manifest

```bash
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py deploy.yaml
```

Output:

```text
[ERROR] deploy.yaml/web (Deployment) — Image uses ':latest' tag or no tag — pin to a specific version
[ERROR] deploy.yaml/web (Deployment) — No resource limits defined
[WARNING] deploy.yaml/web (Deployment) — No resource requests defined
[WARNING] deploy.yaml/web (Deployment) — No liveness probe defined
[WARNING] deploy.yaml/web (Deployment) — No readiness probe defined

5 finding(s): 2 error(s), 3 warning(s), 0 info
```

## 2. Lint a directory (CI mode — errors only)

```bash
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py manifests/ --severity error
```

Only errors are shown; exit code is non-zero if any errors exist.

## 3. JSON output

```bash
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py deploy.yaml --json
```

Returns a JSON array of findings with file, severity, target, kind, and message fields.

## 4. Quiet mode (no summary)

```bash
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py deploy.yaml --quiet
```

Suppresses the summary line at the end.
