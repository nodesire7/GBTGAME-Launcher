#!/usr/bin/env python3
"""Temp: rewrite version fields + history from source repo releases."""
import html as html_mod
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
SOURCE = "nodesire7/GBTGAME-D-Launcher-v3.0"

p = subprocess.run(["gh", "api", f"repos/{SOURCE}/releases?per_page=20"],
                   capture_output=True)
releases = json.loads(p.stdout.decode("utf-8"))
latest = releases[0]
tag = latest["tag_name"]
exe_name = next((a["name"] for a in latest.get("assets", [])
                 if a["name"].startswith("GBTGAME.D.")), "GBTGAME.D.v3.0.exe")

def repl_id(text, id_, inner):
    pat = re.compile(r'(<[^>]*\bid="' + re.escape(id_) + r'"[^>]*>)(.*?)(</[^>]*>)', re.S)
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

html = HTML.read_text(encoding="utf-8")
html = re.sub(r'<title>.*?</title>',
              f'<title>GBTGAME Launcher {tag} - D加密虚拟化游戏启动器</title>',
              html, count=1)
html = re.sub(r'(content="GBTGAME D加密虚拟化游戏启动器 )v[\d.]+',
              r'\g<1>' + tag, html, count=1)
html = repl_id(html, "current-version-chip", f"{tag} Latest")
html = repl_id(html, "current-version-hero", f"GBTGAME Launcher {tag}")
html = repl_id(html, "current-version-download", tag)
html = repl_id(html, "github-release-meta", f"自动同步最新发布 · {tag}")
html = repl_id(html, "current-version-download-note", f"GBTGAME Launcher {tag}")
html = repl_id(html, "latest-version", tag)
html = repl_id(html, "current-version-footer", f"D加密虚拟化游戏启动器 · {tag}")
html = re.sub(r'alt="GBTGAME Launcher v[\d.]+ 主界面"',
              f'alt="GBTGAME Launcher {tag} 主界面"', html, count=1)
html = re.sub(r'releases/download/[^/"\']+/GBTGAME\.D\.v3\.0(\.\d+)?\.exe',
              f'releases/download/{tag}/{exe_name}', html, count=1)

v3 = [r for r in releases if r["tag_name"].startswith("v3.")]
entries = []
for i, rel in enumerate(v3):
    badge = '<span class="latest-badge">LATEST</span>' if i == 0 else ''
    code = (rel.get("target_commitish") or "")[:7]
    code_span = f'<span class="release-code">{code}</span>' if code else ''
    items = bullets(rel.get("body")) or ["详见 GitHub Release 说明。"]
    lis = "\n".join(f"<li>{html_mod.escape(x)}</li>" for x in items)
    entries.append(
        f'<div class="release{" latest" if i == 0 else ""}">\n'
        f'<div class="release-head">\n<h3>{rel["tag_name"]}</h3>\n'
        f'{badge}\n{code_span}\n</div>\n\n<ul>\n{lis}\n</ul>\n\n</div>')
html = re.sub(
    r'<!-- AUTO:RELEASE_HISTORY:START -->.*?<!-- AUTO:RELEASE_HISTORY:END -->',
    '<!-- AUTO:RELEASE_HISTORY:START -->\n\n' + "\n\n".join(entries) +
    '\n\n<!-- AUTO:RELEASE_HISTORY:END -->', html, count=1, flags=re.S)

HTML.write_text(html, encoding="utf-8")
print("updated to", tag, "| exe:", exe_name,
      "| video kept:", "BV1mDgK6ZE5z" in html,
      "| cn ok:", "下载 GBTGAME Launcher" in html)
