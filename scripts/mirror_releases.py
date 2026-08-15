#!/usr/bin/env python3
"""Mirror the latest release from the source launcher repo.

- Reads the releases of the source repository (default:
  nodesire7/GBTGAME-D-Launcher-v3.0) through the GitHub API.
  All API calls go through the `gh` CLI, so any authenticated gh session
  works (locally or on Actions); the source repo is public and readable by
  any token. SOURCE_REPO_TOKEN is only needed if the source ever goes
  private.
- Downloads the EXE and SHA256SUMS.txt assets into release/.
- Writes release/release.json (latest release + history list) consumed by
  update_release.py.
- When running inside GitHub Actions (GITHUB_ACTIONS=true), additionally
  mirrors the latest release and its assets INTO this repository with the
  runner's token, so the page's download link stays inside the pages repo.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = os.environ.get("SOURCE_REPO", "nodesire7/GBTGAME-D-Launcher-v3.0")
SOURCE_TOKEN = os.environ.get("SOURCE_REPO_TOKEN") or ""
ROOT = Path(__file__).resolve().parent.parent
RELEASE_DIR = ROOT / "release"
KEEP_ASSETS = ("GBTGAME.D.v3.0.exe", "SHA256SUMS.txt")


def gh(args, binary_stdout=None):
    if not shutil.which("gh"):
        raise RuntimeError("gh CLI not found")
    env = dict(os.environ)
    # The runner's GITHUB_TOKEN is scoped to THIS repo only: it returns 404
    # for any other repository (even public ones). Source-repo calls must
    # therefore either use SOURCE_REPO_TOKEN or go unauthenticated.
    if SOURCE_TOKEN:
        env["GH_TOKEN"] = SOURCE_TOKEN
    else:
        env.pop("GH_TOKEN", None)
        env.pop("GITHUB_TOKEN", None)
    if binary_stdout is not None:
        with open(binary_stdout, "wb") as f:
            p = subprocess.run(["gh", "api"] + args, env=env, stdout=f,
                               stderr=subprocess.PIPE)
        if p.returncode != 0:
            raise RuntimeError("gh api failed")
        return None
    p = subprocess.run(["gh", "api"] + args, env=env, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"gh api failed: {p.stderr.decode('utf-8', 'replace').strip()}")
    return json.loads(p.stdout.decode("utf-8") or "null")


def main():
    RELEASE_DIR.mkdir(exist_ok=True)
    releases = gh([f"repos/{SOURCE}/releases?per_page=20"])
    if not releases:
        sys.exit("source repo returned no releases")
    latest = releases[0]
    tag = latest["tag_name"]
    history = [{
        "tag": r["tag_name"],
        "name": r.get("name") or r["tag_name"],
        "body": r.get("body") or "",
        "published": r.get("published_at") or "",
        "commit": (r.get("target_commitish") or "")[:7],
    } for r in releases]

    assets = []
    for a in latest.get("assets", []):
        if a["name"] not in KEEP_ASSETS:
            continue
        dest = RELEASE_DIR / a["name"]
        if dest.exists() and dest.stat().st_size == a["size"]:
            print(f"skip {a['name']} (already present, size matches)")
        else:
            print(f"downloading {a['name']} ({a['size']} bytes)")
            gh([f"repos/{SOURCE}/releases/assets/{a['id']}",
                "-H", "Accept: application/octet-stream"],
               binary_stdout=str(dest))
        assets.append({"name": a["name"], "size": a["size"]})

    data = {
        "source": SOURCE,
        "tag": tag,
        "name": latest.get("name") or tag,
        "body": latest.get("body") or "",
        "published": latest.get("published_at") or "",
        "commit": (latest.get("target_commitish") or "")[:7],
        "assets": assets,
        "history": history,
    }
    (RELEASE_DIR / "release.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"release.json written for {tag}")

    if os.environ.get("GITHUB_ACTIONS") == "true":
        files = [str(RELEASE_DIR / a["name"]) for a in assets]
        if not files:
            print("no assets to mirror, skipping repo release")
            return
        code, _ = subprocess.run(["gh", "release", "view", tag],
                                 capture_output=True, text=True).returncode, None
        r = subprocess.run(["gh", "release", "view", tag],
                           capture_output=True, text=True)
        if r.returncode == 0:
            out = subprocess.run(
                ["gh", "release", "upload", tag] + files + ["--clobber"],
                capture_output=True, text=True)
            print(f"uploaded assets to existing release {tag}: "
                  f"{(out.stdout or '')}{(out.stderr or '')}")
        else:
            out = subprocess.run(
                ["gh", "release", "create", tag] + files +
                ["--title", data["name"], "--notes", data["body"]],
                capture_output=True, text=True)
            print(f"created release {tag}: "
                  f"{(out.stdout or '')}{(out.stderr or '')}")


if __name__ == "__main__":
    main()
