---
name: k8s-manifest-lint
description: Lint Kubernetes YAML manifests for best practices including resource limits, labels, probes, security contexts, and image tags without external dependencies.
license: MIT
---

# K8s Manifest Lint

> Validate Kubernetes YAML manifests against production-readiness best practices — no kubectl required.

## When to Use / Triggers

- Review K8s manifests before applying to a cluster.
- CI: enforce production-readiness checks on deploy pipelines.
- Audit existing manifests for missing resource limits, labels, or probes.
- Validate Helm chart templates rendered output.

## Capabilities

- Checks for: missing resource limits/requests, missing labels (app, version), missing liveness/readiness probes, `:latest` image tag, running as root, hostNetwork/hostPID, privileged containers, missing namespace.
- Supports multi-document YAML files (`---` separated).
- `--json` for machine-readable output.
- `--severity` filter (error, warning, info).
- Returns non-zero exit code when errors are found (CI friendly).

## Usage

```bash
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py deploy.yaml
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py manifests/ --severity error
python skills/k8s-manifest-lint/scripts/k8s_manifest_lint.py deploy.yaml --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/k8s_manifest_lint.py --help` for all options.
