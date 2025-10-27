#!/bin/bash
# 发布新版本并触发自动打包

echo "🚀 发布新版本"
echo "=================================="
echo ""

# 检查是否提供了版本号
if [ -z "$1" ]; then
    echo "❌ 错误：请提供版本号"
    echo ""
    echo "用法："
    echo "  ./release.sh v1.0.0"
    echo ""
    echo "示例："
    echo "  ./release.sh v1.0.0    # 发布 1.0.0 版本"
    echo "  ./release.sh v2.1.3    # 发布 2.1.3 版本"
    exit 1
fi

VERSION=$1

# 检查版本号格式
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "⚠️  警告：版本号格式建议为 v主版本.次版本.修订号 (例如: v1.0.0)"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 1
    fi
fi

echo "📦 准备发布版本: $VERSION"
echo ""

# 检查标签是否已存在
if git rev-parse $VERSION >/dev/null 2>&1; then
    echo "❌ 错误：标签 $VERSION 已存在"
    echo ""
    echo "可用选项："
    echo "1. 删除旧标签: git tag -d $VERSION && git push gitee :refs/tags/$VERSION"
    echo "2. 使用新的版本号"
    exit 1
fi

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo "📝 检测到未提交的更改："
    git status -s
    echo ""
    read -p "是否要提交这些更改？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Release $VERSION"
        echo "✅ 更改已提交"
    else
        echo "❌ 已取消发布"
        exit 1
    fi
fi
echo ""

# 获取当前分支
BRANCH=$(git branch --show-current)

# 创建标签
echo "🏷️  创建标签: $VERSION"
git tag -a $VERSION -m "Release $VERSION"
echo "✅ 标签创建成功"
echo ""

# 推送到 Gitee（如果配置了）
if git remote | grep -q "gitee"; then
    echo "1️⃣  推送到 Gitee..."
    git push gitee $BRANCH 2>/dev/null || echo "⚠️  Gitee 分支推送失败（可能未配置）"
    git push gitee $VERSION 2>/dev/null || echo "⚠️  Gitee 标签推送失败（可能未配置）"
    echo "✅ Gitee 推送完成"
    echo ""
fi

# 检测 GitHub 远程仓库（支持 github 或 origin）
GITHUB_REMOTE=""
if git remote | grep -q "^github$"; then
    GITHUB_REMOTE="github"
elif git remote | grep -q "^origin$"; then
    # 检查 origin 是否指向 GitHub
    ORIGIN_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ $ORIGIN_URL == *"github.com"* ]]; then
        GITHUB_REMOTE="origin"
    fi
fi

# 推送到 GitHub（触发自动打包）
if [ -n "$GITHUB_REMOTE" ]; then
    echo "2️⃣  推送到 GitHub（将触发自动打包）..."
    git push $GITHUB_REMOTE $BRANCH
    git push $GITHUB_REMOTE $VERSION
    echo "✅ GitHub 推送成功"
    echo ""
    echo "=================================="
    echo "🎉 发布完成！"
    echo "=================================="
    echo ""
    echo "📊 查看自动打包进度："
    GITHUB_URL=$(git remote get-url $GITHUB_REMOTE | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
    echo "   $GITHUB_URL/actions"
    echo ""
    echo "📦 打包完成后，在以下位置下载安装包："
    echo "   $GITHUB_URL/releases/tag/$VERSION"
    echo ""
    echo "⏱️  预计等待时间：15-20 分钟"
    echo ""
    echo "💡 提示："
    echo "  - 首次推送需要在 GitHub 仓库启用 Actions"
    echo "  - 访问仓库 Settings → Actions → General"
    echo "  - 选择 'Allow all actions and reusable workflows'"
else
    echo "⚠️  未配置 GitHub 远程仓库，无法触发自动打包"
    echo ""
    echo "如需使用 GitHub Actions 自动打包："
    echo "1. 确保已在 GitHub 创建仓库"
    echo "2. 添加 GitHub 远程仓库："
    echo "   git remote add origin git@github.com:你的用户名/仓库名.git"
    echo "   或"
    echo "   git remote add github git@github.com:你的用户名/仓库名.git"
    echo "3. 重新运行此脚本"
    echo ""
    echo "=================================="
    echo "✅ 发布完成"
    echo "=================================="
fi

