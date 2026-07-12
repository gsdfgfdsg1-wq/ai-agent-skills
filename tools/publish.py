#!/usr/bin/env python3
"""The publish step of the skill pipeline.

1. Validate all skills (must pass).
2. Rebuild the catalog.
3. Commit everything to the local repo.
4. If GH_PAT (or GITHUB_TOKEN) is set:
     - ensure 'origin' remote exists (auto-create public repo via API if needed)
     - push to GitHub

Degrades gracefully: without a token/remote it simply commits locally and
reports the skip, so the pipeline never breaks offline.
"""
import datetime
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")


def _load_dotenv():
    envf = os.path.join(ROOT, ".env")
    if os.path.isfile(envf):
        with open(envf, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v


def run(cmd):
    # timeout keeps the pipeline from hanging forever if the network is blocked
    # (e.g. in a sandboxed automation environment) — it fails fast instead.
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=120)


def main():
    _load_dotenv()
    # 1. validate
    r = run([sys.executable, os.path.join(TOOLS, "validate_skills.py")])
    print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    # 2. catalog
    run([sys.executable, os.path.join(TOOLS, "build_catalog.py")])

    # 3. commit
    run(["git", "add", "-A"])
    today = datetime.date.today().isoformat()
    st = run(["git", "status", "--short"])
    if not st.stdout.splitlines():
        print("Nothing new to commit locally; proceeding to push step.")
    else:
        c = run(["git", "commit", "-m", f"chore: sync skills + catalog ({today})"])
        print(c.stdout.strip() or c.stderr.strip())

    # 4. push (always attempted when a token is available, even if there was
    #    nothing new to commit locally — e.g. first run needs to create the
    #    remote repo and push the initial history).
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Skipped push: set GH_PAT (and optionally REPO_NAME/REMOTE_URL) to enable auto-push.")
        return

    remote = run(["git", "remote", "get-url", "origin"])
    if remote.returncode != 0:
        sr = run([sys.executable, os.path.join(TOOLS, "setup_remote.py")])
        print(sr.stdout.strip() or sr.stderr.strip())
        remote = run(["git", "remote", "get-url", "origin"])

    if remote.returncode != 0:
        print("Skipped push: could not determine remote.")
        return

    url = remote.stdout.strip()
    try:
        if url.startswith("https://") and "@" not in url:
            # origin has no credentials yet — inject the token.
            authed = url.replace("https://", f"https://x-access-token:{token}@", 1)
            p = run(["git", "push", authed, "main"])
        else:
            # origin already carries credentials (e.g. set during a previous
            # push) — use it directly to avoid double-injecting the token.
            p = run(["git", "push", url, "main"])
    except subprocess.TimeoutExpired:
        print("Push timed out (network likely blocked). Committed locally; "
              "re-run publish.py with network access to push.")
        return
    out = (p.stdout or p.stderr).strip()
    print(out)
    print("Pushed to origin." if p.returncode == 0 else "Push failed (see above).")


if __name__ == "__main__":
    main()
