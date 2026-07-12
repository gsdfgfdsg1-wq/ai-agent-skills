#!/usr/bin/env python3
"""k8s-manifest-lint — lint Kubernetes YAML/JSON manifests for best practices.

Usage:
    python k8s_manifest_lint.py PATH [PATH ...] [--severity LEVEL] [--json] [--quiet]

Checks resource limits, labels, probes, image tags, security contexts, and more.
"""

import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", "charts"}
YAML_EXTS = {".yaml", ".yml"}
JSON_EXTS = {".json"}


def _parse_scalar(val):
    """Parse a YAML scalar value."""
    if not isinstance(val, str):
        return val
    if val in ("true", "True"):
        return True
    if val in ("false", "False"):
        return False
    if val in ("null", "~", ""):
        return None
    # Quoted strings
    if len(val) >= 2:
        if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
            return val[1:-1]
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def _parse_yaml_docs(text):
    """Parse multi-document YAML text into list of dicts.
    Handles the subset commonly used in K8s manifests: nested dicts, lists of dicts, scalars."""
    docs = []
    current_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---":
            if current_lines:
                doc = _parse_yaml_block(current_lines)
                if doc:
                    docs.append(doc)
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        doc = _parse_yaml_block(current_lines)
        if doc:
            docs.append(doc)
    return docs


def _get_indent(line):
    """Get indentation level of a line."""
    return len(line) - len(line.lstrip())


def _parse_yaml_block(lines):
    """Parse a single YAML document into a dict using recursive descent."""
    if not lines:
        return {}

    # Find the minimum indentation to normalize
    non_empty = [l for l in lines if l.strip() and not l.strip().startswith("#")]
    if not non_empty:
        return {}

    # Tokenize lines into (indent, content) pairs
    tokens = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        tokens.append((_get_indent(line), stripped))

    if not tokens:
        return {}

    pos = [0]  # mutable for closure

    def parse_value(indent):
        """Parse a value at the given indent level. Can be dict, list, or scalar."""
        if pos[0] >= len(tokens):
            return None

        cur_indent, cur_content = tokens[pos[0]]

        # If current indent matches, it could be a dict, list, or scalar
        if cur_content.startswith("- "):
            return parse_list(indent)
        elif ":" in cur_content:
            return parse_dict(indent)
        else:
            return parse_scalar_value()

    def parse_scalar_value():
        """Parse a single scalar value from current token."""
        if pos[0] >= len(tokens):
            return None
        _, content = tokens[pos[0]]
        pos[0] += 1
        return _parse_scalar(content)

    def parse_dict(base_indent):
        """Parse a dictionary starting at base_indent."""
        result = {}
        while pos[0] < len(tokens):
            cur_indent, cur_content = tokens[pos[0]]
            if cur_indent < base_indent:
                break
            if cur_indent != base_indent:
                break

            # Must be a key: value line
            if ":" not in cur_content:
                break

            key, _, val = cur_content.partition(":")
            key = key.strip().strip('"').strip("'")
            val = val.strip()

            pos[0] += 1

            if val == "":
                # Value is on next lines (nested)
                if pos[0] < len(tokens):
                    next_indent = tokens[pos[0]][0]
                    if next_indent > cur_indent:
                        result[key] = parse_value(next_indent)
                    else:
                        result[key] = None
                else:
                    result[key] = None
            else:
                result[key] = _parse_scalar(val)

        return result

    def parse_list(base_indent):
        """Parse a list starting at base_indent."""
        result = []
        while pos[0] < len(tokens):
            cur_indent, cur_content = tokens[pos[0]]
            if cur_indent < base_indent:
                break
            if cur_indent != base_indent:
                break

            if not cur_content.startswith("- "):
                break

            item_content = cur_content[2:].strip()
            pos[0] += 1

            if item_content == "":
                # Item content is on next lines
                if pos[0] < len(tokens):
                    next_indent = tokens[pos[0]][0]
                    if next_indent > cur_indent:
                        result.append(parse_value(next_indent))
                    else:
                        result.append(None)
                else:
                    result.append(None)
            elif ":" in item_content:
                # Inline dict start: "key: value" after dash
                # Create a dict from this and continue
                key, _, val = item_content.partition(":")
                key = key.strip().strip('"').strip("'")
                val = val.strip()

                item_dict = {}
                if val == "":
                    # Nested content
                    if pos[0] < len(tokens):
                        next_indent = tokens[pos[0]][0]
                        if next_indent > cur_indent:
                            # The nested content could be more keys at next_indent
                            # Parse remaining keys at the dash+2 indent
                            item_dict[key] = None
                            # Actually the next lines at deeper indent are the value for this key
                            # But they could also be more keys of the same dict
                            # We need to find the effective indent of this list item's dict
                            item_indent = next_indent
                            while pos[0] < len(tokens):
                                ni, nc = tokens[pos[0]]
                                if ni < item_indent:
                                    break
                                if ni == item_indent and ":" in nc:
                                    k2, _, v2 = nc.partition(":")
                                    k2 = k2.strip().strip('"').strip("'")
                                    v2 = v2.strip()
                                    pos[0] += 1
                                    if v2 == "":
                                        if pos[0] < len(tokens) and tokens[pos[0]][0] > ni:
                                            item_dict[k2] = parse_value(tokens[pos[0]][0])
                                        else:
                                            item_dict[k2] = None
                                    else:
                                        item_dict[k2] = _parse_scalar(v2)
                                else:
                                    break
                        else:
                            item_dict[key] = None
                    else:
                        item_dict[key] = None
                else:
                    item_dict[key] = _parse_scalar(val)
                    # Check for more keys at same indent level within this list item
                    item_indent = cur_indent + 2
                    while pos[0] < len(tokens):
                        ni, nc = tokens[pos[0]]
                        if ni < item_indent:
                            break
                        if ni == item_indent and ":" in nc:
                            k2, _, v2 = nc.partition(":")
                            k2 = k2.strip().strip('"').strip("'")
                            v2 = v2.strip()
                            pos[0] += 1
                            if v2 == "":
                                if pos[0] < len(tokens) and tokens[pos[0]][0] > ni:
                                    item_dict[k2] = parse_value(tokens[pos[0]][0])
                                else:
                                    item_dict[k2] = None
                            else:
                                item_dict[k2] = _parse_scalar(v2)
                        else:
                            break

                result.append(item_dict)
            else:
                result.append(_parse_scalar(item_content))

        return result

    base_indent = tokens[0][0]
    return parse_dict(base_indent)


def _deep_get(obj, *keys, default=None):
    """Safely traverse nested dicts."""
    current = obj
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k, default)
        else:
            return default
        if current is None:
            return default
    return current


def lint_manifest(doc, filepath="<stdin>"):
    """Lint a single K8s manifest dict, returning list of findings."""
    findings = []
    kind = _deep_get(doc, "kind") or ""
    kind_lower = kind.lower()

    metadata = _deep_get(doc, "metadata") or {}
    name = metadata.get("name", "<unnamed>")

    # Skip if not a known workload kind
    workload_kinds = {"deployment", "statefulset", "daemonset", "job", "cronjob", "pod", "replicaset", "replicationcontroller"}
    if not kind_lower:
        return findings

    # 1. Missing namespace
    if "namespace" not in metadata:
        findings.append(("info", name, kind, "No namespace specified — will use 'default'"))

    # 2. Missing labels on metadata
    labels = metadata.get("labels", {})
    if not labels:
        findings.append(("warning", name, kind, "No labels on metadata"))
    else:
        for req_label in ["app", "app.kubernetes.io/name"]:
            found = req_label in labels or any(req_label in str(v) for v in labels.values())
            if found:
                break
        else:
            findings.append(("info", name, kind, "No 'app' or 'app.kubernetes.io/name' label found"))

    # Check containers in spec
    spec = _deep_get(doc, "spec") or {}

    # For CronJob, containers are nested deeper
    if kind_lower == "cronjob":
        job_spec = _deep_get(doc, "spec", "jobTemplate", "spec", "template", "spec") or {}
    elif kind_lower in workload_kinds:
        job_spec = _deep_get(doc, "spec", "template", "spec") or {}
    else:
        job_spec = spec

    containers = job_spec.get("containers", [])
    if not isinstance(containers, list):
        containers = []

    init_containers = job_spec.get("initContainers", [])
    if not isinstance(init_containers, list):
        init_containers = []

    all_containers = containers + init_containers

    for idx, container in enumerate(all_containers):
        if not isinstance(container, dict):
            continue
        cname = container.get("name", f"container-{idx}")
        prefix = f"{name}/{cname}"

        # 3. :latest image tag
        image = container.get("image", "")
        if isinstance(image, str) and (":" not in image or image.endswith(":latest")):
            findings.append(("error", prefix, kind, "Image uses ':latest' tag or no tag — pin to a specific version"))

        # 4. Missing resource limits (only for main containers, not init)
        if container in containers:
            resources = container.get("resources", {})
            if not isinstance(resources, dict):
                resources = {}
            limits = resources.get("limits", {})
            requests = resources.get("requests", {})
            if not limits:
                findings.append(("error", prefix, kind, "No resource limits defined"))
            if not requests:
                findings.append(("warning", prefix, kind, "No resource requests defined"))

        # 5. Missing probes (only for main containers)
        if container in containers and kind_lower in {"deployment", "statefulset", "daemonset", "pod"}:
            if not container.get("livenessProbe"):
                findings.append(("warning", prefix, kind, "No liveness probe defined"))
            if not container.get("readinessProbe"):
                findings.append(("warning", prefix, kind, "No readiness probe defined"))

        # 6. Security context
        security_context = container.get("securityContext", {})
        if not isinstance(security_context, dict):
            security_context = {}
        if security_context.get("runAsRoot") is True or (not security_context.get("runAsNonRoot") and not security_context.get("runAsUser")):
            findings.append(("info", prefix, kind, "Container may run as root — consider setting runAsNonRoot: true"))

        if security_context.get("privileged"):
            findings.append(("error", prefix, kind, "Container runs in privileged mode"))

        if security_context.get("allowPrivilegeEscalation") is not False:
            findings.append(("warning", prefix, kind, "allowPrivilegeEscalation not explicitly set to false"))

    # 7. Pod-level security
    pod_sec = job_spec.get("securityContext", {})
    if not isinstance(pod_sec, dict):
        pod_sec = {}
    if not pod_sec.get("runAsNonRoot"):
        findings.append(("info", name, kind, "Pod securityContext does not set runAsNonRoot"))

    # 8. hostNetwork / hostPID
    if job_spec.get("hostNetwork"):
        findings.append(("error", name, kind, "hostNetwork is enabled — use with caution"))
    if job_spec.get("hostPID"):
        findings.append(("error", name, kind, "hostPID is enabled — use with caution"))

    return findings


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in (YAML_EXTS | JSON_EXTS):
                        yield os.path.join(root, fn)


def _load_docs(filepath):
    """Load documents from a YAML or JSON file."""
    try:
        with open(filepath, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return [], str(e)

    ext = os.path.splitext(filepath)[1].lower()
    if ext in JSON_EXTS:
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data, None
            return [data], None
        except json.JSONDecodeError as e:
            return [], f"Invalid JSON: {e}"
    else:
        # YAML
        docs = _parse_yaml_docs(text)
        return docs, None


def main():
    ap = argparse.ArgumentParser(
        description="Lint Kubernetes YAML/JSON manifests for best practices."
    )
    ap.add_argument("paths", nargs="+", help="K8s YAML/JSON files or directories to lint")
    ap.add_argument("--severity", choices=["error", "warning", "info"],
                    default="info", help="minimum severity to report (default: info)")
    ap.add_argument("--json", action="store_true", help="output JSON results")
    ap.add_argument("--quiet", action="store_true", help="suppress summary")
    args = ap.parse_args()

    severity_order = {"error": 0, "warning": 1, "info": 2}
    min_sev = severity_order[args.severity]

    all_findings = []
    for fp in _iter_targets(args.paths):
        docs, err = _load_docs(fp)
        if err:
            all_findings.append({"file": fp, "error": err})
            continue

        for doc in docs:
            if not isinstance(doc, dict) or not doc:
                continue
            findings = lint_manifest(doc, fp)
            for sev, target, kind, msg in findings:
                if severity_order.get(sev, 2) <= min_sev:
                    all_findings.append({
                        "file": fp,
                        "severity": sev,
                        "target": target,
                        "kind": kind,
                        "message": msg,
                    })

    error_count = sum(1 for f in all_findings if isinstance(f, dict) and f.get("severity") == "error")
    warning_count = sum(1 for f in all_findings if isinstance(f, dict) and f.get("severity") == "warning")
    info_count = sum(1 for f in all_findings if isinstance(f, dict) and f.get("severity") == "info")

    if args.json:
        print(json.dumps(all_findings, indent=2, ensure_ascii=False))
    else:
        for f in all_findings:
            if "error" in f and "severity" not in f:
                print(f"[ERROR] {f['file']}: {f['error']}")
            else:
                sev = f["severity"].upper()
                print(f"[{sev}] {f['file']}: {f['target']} ({f['kind']}) — {f['message']}")

    if not args.quiet:
        total = error_count + warning_count + info_count
        print(f"\n{total} finding(s): {error_count} error(s), {warning_count} warning(s), {info_count} info")

    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
