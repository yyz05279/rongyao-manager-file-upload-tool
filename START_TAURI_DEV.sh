#!/bin/bash

# 熔盐管理文件上传工具 - Tauri 开发启动脚本
# 用途: 快速启动 Tauri 项目的开发环境

set -e

PROJECT_ROOT="/Users/yyz/Desktop/熔盐管理文件上传工具"
TAURI_APP="$PROJECT_ROOT/tauri-app"

echo "🚀 熔盐管理文件上传工具 - Tauri 开发启动"
echo "======================================"
echo ""

# 第 1 步: 检查环境
echo "📋 检查环境..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

if ! command -v rustc &> /dev/null; then
    echo "❌ Rust 未安装"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"
echo "✅ Rust 版本: $(rustc --version)"
echo ""

# 第 2 步: 进入项目目录
echo "📂 进入项目目录: $TAURI_APP"
cd "$TAURI_APP"
echo "✅ 当前目录: $(pwd)"
echo ""

# 第 3 步: 检查依赖
echo "📦 检查依赖..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  npm 依赖未安装，正在安装..."
    npm install
else
    echo "✅ npm 依赖已安装"
fi
echo ""

# 第 4 步: 验证项目文件
echo "✔️ 验证项目文件..."
files_to_check=(
    "src/App.jsx"
    "src/main.jsx"
    "src/stores/authStore.js"
    "src/services/api.js"
    "src/components/LoginForm.jsx"
    "src/components/UploadForm.jsx"
    "src-tauri/src/main.rs"
    "src-tauri/Cargo.toml"
    "package.json"
    "vite.config.js"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ 缺少文件: $file"
        exit 1
    fi
done
echo ""

# 第 5 步: 启动开发服务器
echo "🎬 启动 Tauri 开发服务器..."
echo ""
echo "预期结果:"
echo "  • Vite 前端服务器启动 (http://localhost:5173)"
echo "  • Rust 后端编译"
echo "  • Tauri 应用窗口打开"
echo "  • React 组件热加载可用"
echo ""
echo "======================================"
echo ""

# 启动 npm run dev
npm run dev

# 如果开发服务器关闭
echo ""
echo "✅ Tauri 开发服务器已关闭"
echo ""
