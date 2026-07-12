#!/usr/bin/env python3
"""Create the GitHub repo (if needed) and configure the local 'origin' remote.

Reads GH_PAT from environment (or a local .env file). Repo name from REPO_NAME
(default ai-agent-skills) or full REMOTE_URL. Uses only the stdlib (urllib).
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def _api(method, path, token, data=None):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            msg = json.loads(body).get("message", body)
        except Exception:
            msg = body
        return e.code, {"message": msg}


def _me(token):
    code, resp = _api("GET", "/user", token)
    if code == 200:
        return resp.get("login")
    raise RuntimeError(f"github auth failed ({code}): {resp.get('message')}")


def _create_repo(token, name):
    code, resp = _api("POST", "/user/repos", token, {
        "name": name,
        "private": False,
        "description": "A collection of plug-and-play AI Agent skill modules.",
        "auto_init": False,
        "has_issues": True,
    })
    if code in (200, 201):
        return resp.get("clone_url")
    if code == 422 and "already exists" in resp.get("message", "").lower():
        user = _me(token)
        return f"https://github.com/{user}/{name}.git"
    raise RuntimeError(f"create repo failed ({code}): {resp.get('message')}")


def main():
    _load_dotenv()
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("No GH_PAT/GITHUB_TOKEN set; cannot setup remote.")
        sys.exit(1)
    remote_url = os.environ.get("REMOTE_URL")
    name = (remote_url.rstrip("/").split("/")[-1].replace(".git", "")) if remote_url \
        else os.environ.get("REPO_NAME", "ai-agent-skills")
    try:
        user = _me(token)
        url = remote_url or _create_repo(token, name)
    except Exception as e:
        print(f"GitHub API error: {e}")
        sys.exit(1)
    existing = subprocess.run(["git", "remote", "get-url", "origin"],
                              cwd=ROOT, capture_output=True, text=True)
    if existing.returncode != 0:
        subprocess.run(["git", "remote", "add", "origin", url], cwd=ROOT, check=True)
    else:
        subprocess.run(["git", "remote", "set-url", "origin", url], cwd=ROOT, check=True)
    print(f"Remote 'origin' -> {url} (owner: {user})")


if __name__ == "__main__":
    main()
