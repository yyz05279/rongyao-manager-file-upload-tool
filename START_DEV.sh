#!/bin/bash

set -e

PROJECT_DIR="/Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app"

echo "🚀 Tauri-App 开发启动脚本"
echo "======================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装"
    exit 1
fi

echo "✅ Node.js 版本: $(node -v)"
echo "✅ npm 版本: $(npm -v)"

# 进入项目目录
cd "$PROJECT_DIR"
echo "📂 进入项目: $PROJECT_DIR"
echo ""

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装 npm 依赖..."
    npm install --legacy-peer-deps
fi

echo ""
echo "🎉 开发环境已就绪！"
echo ""
echo "======================================"
echo "📝 后续步骤:"
echo "======================================"
echo ""
echo "1️⃣ 启动前端开发服务器 (当前终端):"
echo "   npm run dev"
echo ""
echo "2️⃣ 在新终端启动 Rust 后端编译:"
echo "   cd $PROJECT_DIR/src-tauri"
echo "   cargo build"
echo ""
echo "3️⃣ 在另一个终端启动完整 Tauri 应用 (可选):"
echo "   npm run tauri"
echo ""
echo "======================================"
echo "💡 快速命令:"
echo "======================================"
echo "开发:          npm run dev"
echo "构建:          cargo build"
echo "完整打包:      npm run tauri:build"
echo "清理缓存:      cargo clean"
echo ""
echo "准备好了！😎"
