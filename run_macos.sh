#!/bin/bash

# macOS 快速启动脚本

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$APP_DIR/dist/熔盐管理文件上传工具"

if [ ! -f "$EXECUTABLE" ]; then
    echo "❌ 错误: 找不到可执行文件"
    echo "位置: $EXECUTABLE"
    echo ""
    echo "请先运行打包脚本:"
    echo "  bash build_macos.sh"
    exit 1
fi

echo "🚀 启动熔盐管理文件上传工具..."
echo "应用路径: $EXECUTABLE"
echo ""

# 运行应用
exec "$EXECUTABLE"
