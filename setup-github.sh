#!/bin/bash
# 设置 GitHub 远程仓库

echo "🔧 设置 GitHub 远程仓库"
echo "=================================="
echo ""

# 检查是否已配置 GitHub
if git remote | grep -q "github"; then
    echo "ℹ️  GitHub 远程仓库已配置："
    git remote get-url github
    echo ""
    read -p "是否要更新 GitHub 仓库地址？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ 保持现有配置"
        exit 0
    fi
    UPDATE_MODE=true
else
    UPDATE_MODE=false
fi

echo ""
echo "请提供 GitHub 仓库信息："
echo ""

# 获取 GitHub 用户名
read -p "GitHub 用户名: " github_username
if [ -z "$github_username" ]; then
    echo "❌ 错误：用户名不能为空"
    exit 1
fi

# 获取仓库名
read -p "仓库名 (默认: rongyao-manager-file-upload-tool): " repo_name
if [ -z "$repo_name" ]; then
    repo_name="rongyao-manager-file-upload-tool"
fi

# 构建仓库 URL
GITHUB_URL="git@github.com:${github_username}/${repo_name}.git"

echo ""
echo "仓库地址: $GITHUB_URL"
echo ""

# 添加或更新远程仓库
if [ "$UPDATE_MODE" = true ]; then
    git remote set-url github $GITHUB_URL
    echo "✅ GitHub 远程仓库已更新"
else
    git remote add github $GITHUB_URL
    echo "✅ GitHub 远程仓库已添加"
fi

echo ""
echo "=================================="
echo "📝 下一步操作："
echo "=================================="
echo ""
echo "1. 在 GitHub 创建仓库（如果还没有）："
echo "   https://github.com/new"
echo "   - 仓库名: $repo_name"
echo "   - 设为 Public（公开仓库才能免费使用 Actions）"
echo "   - 不要初始化 README"
echo ""
echo "2. 推送代码到 GitHub："
echo "   git push github main"
echo ""
echo "3. 启用 GitHub Actions："
echo "   访问 https://github.com/${github_username}/${repo_name}/actions"
echo "   点击 'I understand my workflows, go ahead and enable them'"
echo ""
echo "4. 发布版本（触发自动打包）："
echo "   ./release.sh v1.0.0"
echo ""
echo "详细说明请查看: CI-CD使用指南.md"
echo ""

