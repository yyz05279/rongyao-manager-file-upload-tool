#!/bin/bash

# setup-gitee.sh - 配置 Gitee 远程仓库
# 使用方法: ./setup-gitee.sh

set -e

echo "🔧 配置 Gitee 远程仓库"
echo "================================"
echo ""

# 检查是否已经配置了 gitee
if git remote | grep -q "gitee"; then
    echo "⚠️  Gitee 远程仓库已存在"
    echo ""
    read -p "是否要更新 Gitee 地址？(y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 0
    fi
    git remote remove gitee
fi

# 获取 Gitee 仓库地址
echo "📝 请输入 Gitee 仓库地址"
echo "示例: https://gitee.com/your-username/your-repo.git"
read -p "Gitee 地址: " gitee_url

if [ -z "$gitee_url" ]; then
    echo "❌ Gitee 地址不能为空"
    exit 1
fi

# 添加 Gitee 远程仓库
echo ""
echo "➕ 添加 Gitee 远程仓库..."
git remote add gitee "$gitee_url"

# 验证
echo ""
echo "✅ Gitee 远程仓库配置成功！"
echo ""
echo "📋 当前远程仓库列表:"
git remote -v

echo ""
echo "💡 提示:"
echo "  - 使用 ./push-all.sh 同时推送到所有远程仓库"
echo "  - 使用 git push gitee main 只推送到 Gitee"
echo "  - 使用 git push origin main 只推送到 GitHub"
echo ""
echo "🎉 配置完成！"

