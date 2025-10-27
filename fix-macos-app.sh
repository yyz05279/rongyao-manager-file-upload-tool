#!/bin/bash
# macOS 应用打开问题快速修复脚本
# 用途：移除从网络下载的应用的隔离属性，允许应用运行

echo "🔧 macOS 应用打开问题修复工具"
echo "=================================="
echo ""

# 检查是否提供了应用路径
if [ -z "$1" ]; then
    echo "📱 使用方法："
    echo "  ./fix-macos-app.sh <应用路径>"
    echo ""
    echo "💡 示例："
    echo "  ./fix-macos-app.sh \"熔盐管理文件上传工具.app\""
    echo "  ./fix-macos-app.sh \"/path/to/熔盐管理文件上传工具.app\""
    echo ""
    echo "🔍 或者自动查找并修复本项目的应用："
    echo "  ./fix-macos-app.sh auto"
    echo ""
    exit 1
fi

# 自动模式：查找项目中的应用
if [ "$1" == "auto" ]; then
    echo "🔍 自动查找应用..."
    
    # 优先查找 Tauri 应用
    APP_PATH=$(find tauri-app/src-tauri/target -name "*.app" -type d 2>/dev/null | grep -E "(release|debug)/bundle" | head -n 1)
    
    # 如果未找到 Tauri 应用，查找 Python 应用
    if [ -z "$APP_PATH" ]; then
        APP_PATH=$(find python-app/dist -name "*.app" -type d 2>/dev/null | head -n 1)
    fi
    
    if [ -z "$APP_PATH" ]; then
        echo "❌ 未找到应用，请确保已经打包"
        echo ""
        echo "💡 提示：运行打包脚本"
        echo "  Tauri 应用:"
        echo "    cd tauri-app && npm run tauri build"
        echo ""
        echo "  Python 应用:"
        echo "    cd python-app && bash build_macos.sh"
        exit 1
    fi
    
    echo "✅ 找到应用: $APP_PATH"
    echo ""
else
    APP_PATH="$1"
fi

# 检查应用是否存在
if [ ! -e "$APP_PATH" ]; then
    echo "❌ 错误：应用不存在"
    echo "   路径: $APP_PATH"
    exit 1
fi

# 检查是否是目录
if [ ! -d "$APP_PATH" ]; then
    echo "❌ 错误：路径不是一个应用包"
    echo "   路径: $APP_PATH"
    exit 1
fi

echo "🔧 正在修复应用: $(basename "$APP_PATH")"
echo ""

# 显示当前的隔离属性
echo "📋 当前属性："
xattr "$APP_PATH" 2>/dev/null || echo "  无扩展属性"
echo ""

# 移除隔离属性
echo "🧹 移除隔离属性..."
xattr -cr "$APP_PATH"

if [ $? -eq 0 ]; then
    echo "✅ 修复成功！"
    echo ""
    
    # 再次显示属性确认
    ATTRS=$(xattr "$APP_PATH" 2>/dev/null)
    if [ -z "$ATTRS" ]; then
        echo "✅ 确认：已移除所有隔离属性"
    else
        echo "⚠️  剩余属性："
        echo "$ATTRS"
    fi
    echo ""
    
    echo "=================================="
    echo "🎉 应用现在可以正常打开了！"
    echo "=================================="
    echo ""
    echo "🚀 打开应用："
    echo "  open \"$APP_PATH\""
    echo ""
    
    # 询问是否立即打开
    read -p "是否立即打开应用？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📱 正在打开应用..."
        open "$APP_PATH"
    fi
else
    echo "❌ 修复失败"
    echo ""
    echo "💡 请尝试手动修复："
    echo "  1. 右键点击应用"
    echo "  2. 选择'打开'"
    echo "  3. 在对话框中点击'打开'"
    echo ""
    echo "或者使用 sudo 权限："
    echo "  sudo xattr -cr \"$APP_PATH\""
    exit 1
fi

echo ""
echo "📚 更多信息请查看："
echo "  docs/macOS应用无法打开解决方案.md"

