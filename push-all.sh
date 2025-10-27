#!/bin/bash

# push-all.sh - 同时推送到所有远程仓库（GitHub 和 Gitee）
# 使用方法: ./push-all.sh [分支名] [--with-tags]

set -e

# 默认分支
BRANCH=${1:-main}
PUSH_TAGS=false

# 检查参数
for arg in "$@"; do
    if [ "$arg" = "--with-tags" ] || [ "$arg" = "-t" ]; then
        PUSH_TAGS=true
    fi
done

echo "🚀 同时推送到所有远程仓库"
echo "================================"
echo ""
echo "📋 分支: $BRANCH"
if [ "$PUSH_TAGS" = true ]; then
    echo "🏷️  包含标签: 是"
else
    echo "🏷️  包含标签: 否（使用 --with-tags 或 -t 推送标签）"
fi
echo ""

# 获取所有远程仓库
remotes=$(git remote)

if [ -z "$remotes" ]; then
    echo "❌ 没有配置远程仓库"
    exit 1
fi

echo "📡 远程仓库列表:"
for remote in $remotes; do
    url=$(git remote get-url $remote)
    echo "  - $remote: $url"
done
echo ""

# 推送到每个远程仓库
success_count=0
fail_count=0
failed_remotes=""

for remote in $remotes; do
    echo "📤 推送到 $remote..."
    
    # 推送分支
    if git push $remote $BRANCH; then
        echo "✅ $remote 分支推送成功"
        
        # 如果需要，推送标签
        if [ "$PUSH_TAGS" = true ]; then
            if git push $remote --tags; then
                echo "✅ $remote 标签推送成功"
            else
                echo "⚠️  $remote 标签推送失败（可能没有新标签）"
            fi
        fi
        
        ((success_count++))
    else
        echo "❌ $remote 推送失败"
        failed_remotes="$failed_remotes $remote"
        ((fail_count++))
    fi
    echo ""
done

# 显示结果
echo "================================"
echo "📊 推送结果统计"
echo "================================"
echo "✅ 成功: $success_count"
echo "❌ 失败: $fail_count"

if [ $fail_count -gt 0 ]; then
    echo ""
    echo "⚠️  失败的仓库:$failed_remotes"
    echo ""
    echo "💡 提示:"
    echo "  - 检查网络连接"
    echo "  - 确认有推送权限"
    echo "  - 尝试手动推送: git push <remote> $BRANCH"
    exit 1
else
    echo ""
    echo "🎉 所有远程仓库推送成功！"
fi
