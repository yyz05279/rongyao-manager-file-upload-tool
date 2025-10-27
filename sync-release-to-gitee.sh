#!/bin/bash

# sync-release-to-gitee.sh - 同步 GitHub Release 到 Gitee
# 使用方法: ./sync-release-to-gitee.sh <version>
# 示例: ./sync-release-to-gitee.sh v1.0.0

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "❌ 请提供版本号"
    echo "用法: $0 <version>"
    echo "示例: $0 v1.0.0"
    exit 1
fi

echo "🔄 同步 GitHub Release 到 Gitee"
echo "================================"
echo "版本: $VERSION"
echo ""

# 检查是否配置了 Gitee
if ! git remote | grep -q "gitee"; then
    echo "❌ 未配置 Gitee 远程仓库"
    echo "请先运行: ./setup-gitee.sh"
    exit 1
fi

# 检查 Gitee CLI 工具
if ! command -v gh &> /dev/null && ! command -v curl &> /dev/null; then
    echo "❌ 需要安装 gh 或 curl"
    exit 1
fi

echo "📋 步骤:"
echo "1. 确保标签已推送到 Gitee"
echo "2. 从 GitHub 获取 Release 信息"
echo "3. 在 Gitee 创建对应的 Release"
echo "4. 下载并上传构建产物"
echo ""

read -p "继续？(y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# 1. 推送标签到 Gitee
echo "📤 推送标签到 Gitee..."
git push gitee $VERSION 2>/dev/null || echo "⚠️  标签可能已存在"

# 2. 获取 GitHub Release 信息
echo "📥 获取 GitHub Release 信息..."

# 使用 gh CLI（如果可用）
if command -v gh &> /dev/null; then
    RELEASE_INFO=$(gh release view $VERSION --json name,body,isDraft,isPrerelease)
    RELEASE_NAME=$(echo $RELEASE_INFO | jq -r '.name')
    RELEASE_BODY=$(echo $RELEASE_INFO | jq -r '.body')
    IS_PRERELEASE=$(echo $RELEASE_INFO | jq -r '.isPrerelease')
else
    echo "⚠️  未安装 gh CLI，使用默认信息"
    RELEASE_NAME="$VERSION"
    RELEASE_BODY="Release $VERSION"
    IS_PRERELEASE=false
fi

echo "  名称: $RELEASE_NAME"
echo "  版本: $VERSION"
echo ""

# 3. 创建 Gitee Release（需要手动操作）
echo "📝 创建 Gitee Release（需要手动操作）"
echo "================================"
echo ""
echo "请按照以下步骤操作："
echo ""
echo "1. 打开 Gitee 仓库页面"
GITEE_URL=$(git remote get-url gitee | sed 's/\.git$//')
echo "   $GITEE_URL"
echo ""
echo "2. 点击 '发行版' -> '创建发行版'"
echo ""
echo "3. 填写以下信息:"
echo "   - 标签: $VERSION"
echo "   - 标题: $RELEASE_NAME"
echo "   - 描述: $RELEASE_BODY"
echo ""
echo "4. 上传构建产物（可选）"
echo "   产物位置: tauri-app/src-tauri/target/release/bundle/"
echo ""

# 如果有 GitHub Release 产物，提示下载
if command -v gh &> /dev/null; then
    echo "💡 提示: 可以从 GitHub 下载产物"
    echo "   gh release download $VERSION"
    echo ""
fi

echo "📋 快速链接:"
echo "  - GitHub Release: https://github.com/YOUR-USERNAME/YOUR-REPO/releases/tag/$VERSION"
echo "  - Gitee 发行版: $GITEE_URL/releases"
echo ""
echo "✅ 标签已推送到 Gitee"
echo "🔗 请在浏览器中完成 Release 创建"

