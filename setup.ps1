# GBTGAME-Launcher Pages 一键初始化脚本
# 用法（在已登录 gh 的本机，于本仓库目录内）：
#   .\setup.ps1
#   .\setup.ps1 -SourceToken "github_pat_xxx"   # 源仓库设为私有时提供

param(
    [string]$Owner = "nodesire7",
    [string]$Repo = "GBTGAME-Launcher",
    [string]$SourceToken = ""
)

$ErrorActionPreference = "Stop"
$full = "$Owner/$Repo"

gh auth status | Out-Null
if ($LASTEXITCODE -ne 0) { throw "请先运行 gh auth login" }

# 1. 创建仓库并推送当前目录
if (-not (gh repo view $full 2>$null)) {
    gh repo create $full --public --source . --push --description "GBTGAME Launcher GitHub Pages（自动同步源仓库 Release）"
} else {
    git push
}

# 2. 源仓库 token（可选；源仓库公开时无需配置）
if ($SourceToken) {
    gh secret set SOURCE_REPO_TOKEN --body $SourceToken -R $full
    Write-Host "SOURCE_REPO_TOKEN 已写入"
} else {
    Write-Host "未提供 SourceToken：源仓库为公开仓库，无需配置"
}

# 3. 启用 GitHub Pages（Actions 模式）
gh api "repos/$full/pages" --method POST -f "build_type=workflow" | Out-Null
Write-Host "GitHub Pages 已启用（Actions 构建）"

# 4. 触发同步 + 部署
gh workflow run sync-release.yml -R $full
Write-Host "已触发 sync-release；完成后 deploy-pages 会自动部署"
Write-Host "页面地址：https://$Owner.github.io/$Repo/"
