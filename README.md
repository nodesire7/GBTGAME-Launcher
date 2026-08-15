# GBTGAME Launcher — GitHub Pages 站点

GBTGAME D加密虚拟化游戏启动器的官方介绍页。

- 页面：<https://nodesire7.github.io/GBTGAME-Launcher/>
- 源仓库（Release 来源）：[nodesire7/GBTGAME-D-Launcher-v3.0](https://github.com/nodesire7/GBTGAME-D-Launcher-v3.0)

## 自动同步流程

源仓库发布新版本（如 v3.0.3）后：

1. `sync-release`（每小时 + 手动触发）从源仓库读取最新 Release
2. 下载 `GBTGAME.D.v3.0.exe` 与 `SHA256SUMS.txt` 到 `release/`
3. 把 Release 与资产镜像到本仓库（同名 tag / 说明 / 资产）
4. `update_release.py` 重写 `index.html` 的版本号、标题、下载链接与版本历史
5. 提交并推送 → `deploy-pages` 自动重新部署 GitHub Pages

## 文件说明

| 路径 | 作用 |
|---|---|
| `index.html` | 页面（含 `AUTO:RELEASE_HISTORY` 标记与 version id，由脚本维护） |
| `scripts/mirror_releases.py` | 拉取源 Release + 下载资产 + 镜像到本仓库 |
| `scripts/update_release.py` | 从 `release/release.json` 重写页面版本信息 |
| `.github/workflows/sync-release.yml` | 每小时同步（也可手动运行） |
| `.github/workflows/deploy-pages.yml` | 部署到 GitHub Pages（Actions 模式） |
| `setup.ps1` | 本机一键初始化（建仓/推码/开 Pages） |

## 环境变量 / Secrets

- `SOURCE_REPO`：源仓库，默认 `nodesire7/GBTGAME-D-Launcher-v3.0`
- `SOURCE_REPO_TOKEN`（可选）：源仓库为公开仓库时无需配置；仅当源仓库设为私有时需要（Contents: Read 权限的 fine-grained PAT）

## 本地手动更新

```powershell
python scripts\mirror_releases.py
python scripts\update_release.py
```
