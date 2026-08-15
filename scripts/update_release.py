#!/usr/bin/env python3
"""Rewrite index.html from release/release.json (written by mirror_releases.py).

Updates: <title>, meta description, current-version ids, download link,
release history section (between the AUTO:RELEASE_HISTORY markers) and the
footer version. History only includes v3.x tags.
"""
import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
JSON = ROOT / "release" / "release.json"


def load():
    if not JSON.exists():
        sys.exit("release/release.json missing - run mirror_releases.py first")
    return json.loads(JSON.read_text(encoding="utf-8"))


def repl_id(text, id_, inner):
    pat = re.compile(
        r'(<[^>]*\bid="' + re.escape(id_) + r'"[^>]*>)(.*?)(</[^>]*>)', re.S)
    return pat.sub(lambda m: m.group(1) + inner + m.group(3), text, count=1)


def bullets(body):
    out = []
    for line in (body or "").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- ") or line.startswith("* "):
            line = line[2:].strip()
            if line:
                out.append(line)
    return out


def main():
    data = load()
    tag = data["tag"]
    html = HTML.read_text(encoding="utf-8")

    html = re.sub(
        r'<title>.*?</title>',
        f'<title>GBTGAME Launcher {tag} - D加密虚拟化游戏启动器</title>',
        html, count=1)
    html = re.sub(
        r'(content="GBTGAME D加密虚拟化游戏启动器 )v[\d.]+',
        r'\g<1>' + tag, html, count=1)
    html = repl_id(html, "current-version-chip", f"{tag} Latest")
    html = repl_id(html, "current-version-hero", f"GBTGAME Launcher {tag}")
    html = repl_id(html, "current-version-download", tag)
    html = repl_id(html, "github-release-meta", f"自动同步最新发布 · {tag}")
    html = repl_id(html, "current-version-download-note",
                   f"GBTGAME Launcher {tag}")
    html = repl_id(html, "latest-version", tag)
    html = repl_id(html, "current-version-footer",
                   f"D加密虚拟化游戏启动器 · {tag}")
    html = re.sub(
        r'alt="GBTGAME Launcher v[\d.]+ 主界面"',
        f'alt="GBTGAME Launcher {tag} 主界面"', html, count=1)
    html = re.sub(
        r'releases/download/[^/"\']+/GBTGAME\.D\.v3\.0\.exe',
        f'releases/download/{tag}/GBTGAME.D.v3.0.exe', html, count=1)

    # history: only v3.x releases, newest first
    entries = []
    v3 = [r for r in data["history"] if r["tag"].startswith("v3.")]
    for i, rel in enumerate(v3):
        badge = ('<span class="latest-badge">LATEST</span>'
                 if i == 0 else '')
        code = rel.get("commit") or ""
        code_span = (f'<span class="release-code">{code}</span>'
                     if code else '')
        items = bullets(rel.get("body"))
        if not items:
            items = ["详见 GitHub Release 说明。"]
        lis = "\n".join(
            f"<li>{html_mod.escape(x)}</li>" for x in items)
        entries.append(
            f'<div class="release{" latest" if i == 0 else ""}">\n'
            f'<div class="release-head">\n'
            f'<h3>{rel["tag"]}</h3>\n'
            f'{badge}\n{code_span}\n'
            f'</div>\n\n<ul>\n{lis}\n</ul>\n\n</div>')
    body = "\n\n".join(entries)
    html = re.sub(
        r'<!-- AUTO:RELEASE_HISTORY:START -->.*?<!-- AUTO:RELEASE_HISTORY:END -->',
        '<!-- AUTO:RELEASE_HISTORY:START -->\n\n' + body +
        '\n\n<!-- AUTO:RELEASE_HISTORY:END -->',
        html, count=1, flags=re.S)

    HTML.write_text(html, encoding="utf-8")
    print(f"index.html updated -> {tag}")


if __name__ == "__main__":
    main()
