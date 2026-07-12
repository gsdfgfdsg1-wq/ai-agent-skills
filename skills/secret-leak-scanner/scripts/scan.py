#!/usr/bin/env python3
"""secret-leak-scanner — scan a project for accidentally committed secrets.

Usage:
    python scan.py PATH [PATH ...] [--json] [--exit-code] [--severity MIN]

Severity levels: low | medium | high | critical
When --exit-code is given, exits non-zero if any finding >= --severity
(default: medium).
"""
import argparse
import json
import os
import re
import sys

RULES = [
    ("AWS Access Key ID", "high", re.compile(r"(?<![A-Z0-9])(AKIA|ASIA)[0-9A-Z]{16}")),
    ("AWS Secret Access Key", "critical", re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}")),
    ("Google API Key", "high", re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("GCP Service Account", "critical", re.compile(r"\"type\"\s*:\s*\"service_account\"")),
    ("Private Key (PEM)", "critical", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("Slack Token", "high", re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("Slack Webhook", "high", re.compile(r"https://hooks\.slack\.com/services/T[A-Z0-9]{8,}/[A-Z0-9]{8,}/[A-Z0-9]{16,}")),
    ("Stripe Secret Key", "critical", re.compile(r"sk_live_[0-9a-zA-Z]{24,}")),
    ("Stripe Restricted Key", "high", re.compile(r"rk_live_[0-9a-zA-Z]{24,}")),
    ("GitHub Personal Token", "critical", re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}")),
    ("GitLab PAT", "high", re.compile(r"glpat-[0-9a-zA-Z\-]{20,}")),
    ("npm Token", "high", re.compile(r"npm_[0-9A-Za-z]{36,}")),
    ("OpenAI API Key", "high", re.compile(r"sk-[A-Za-z0-9]{20,}T3BlbkFJ[0-9A-Za-z]{20,}")),
    ("JWT (with secret)", "medium", re.compile(r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")),
    ("Generic secret assignment", "medium", re.compile(r"(?i)(api[_-]?key|client[_-]?secret|secret|token|password|passwd)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}['\"]?")),
    ("High-entropy hex string", "low", re.compile(r"\b[0-9a-f]{32,}\b")),
]

# Lines containing these substrings are treated as rule definitions / comments
# and never reported (prevents the scanner from flagging its own source).
BENIGN_LINE_MARKERS = ("re.compile", "#", "//")

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "__pycache__",
             ".venv", "venv", "target", "bin", "obj"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf",
            ".eot", ".pdf", ".zip", ".gz", ".tar", ".lock", ".exe", ".dll",
            ".so", ".dylib"}
MAX_FILE = 2_000_000  # 2 MB
SEV_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                        continue
                    yield os.path.join(root, fn)


def _scan_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        text = "".join(lines)
    except Exception:
        return []
    if len(text) > MAX_FILE:
        return []
    findings = []
    for name, sev, rx in RULES:
        for m in rx.finditer(text):
            start = m.start()
            line_no = text.count("\n", 0, start) + 1
            line_text = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
            if any(mk in line_text for mk in BENIGN_LINE_MARKERS):
                continue
            snippet = m.group(0)
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            findings.append({"rule": name, "severity": sev,
                             "line": line_no, "match": snippet, "file": path})
    return findings


def main():
    ap = argparse.ArgumentParser(description="Scan a project for leaked secrets.")
    ap.add_argument("paths", nargs="+", help="files or directories to scan")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit non-zero when findings >= --severity")
    ap.add_argument("--severity", default="medium", choices=list(SEV_RANK))
    args = ap.parse_args()

    all_findings = []
    for fp in _iter_targets(args.paths):
        all_findings.extend(_scan_file(fp))

    seen, uniq = set(), []
    for f in all_findings:
        key = (f["file"], f["line"], f["rule"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)

    min_rank = SEV_RANK[args.severity]
    shown = [f for f in uniq if SEV_RANK[f["severity"]] >= min_rank]

    if args.json:
        print(json.dumps(shown, indent=2, ensure_ascii=False))
    elif not shown:
        print(f"No secrets found (>= {args.severity}).")
    else:
        print(f"Found {len(shown)} potential secret(s):\n")
        for f in sorted(shown, key=lambda x: -SEV_RANK[x["severity"]]):
            print(f"[{f['severity'].upper()}] {f['rule']}")
            print(f"  {f['file']}:{f['line']}")
            print(f"  match: {f['match']}\n")

    if args.exit_code and shown:
        sys.exit(1)


if __name__ == "__main__":
    main()
