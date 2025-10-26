#!/bin/bash

# 🚀 Tauri 项目初始化脚本
# 这个脚本会创建一个新的 Tauri 项目

set -e

echo "════════════════════════════════════════════"
echo "🚀 Tauri 项目初始化"
echo "════════════════════════════════════════════"
echo ""

# 确保环境变量设置
source $HOME/.cargo/env

# 验证工具
echo "✅ 检查依赖工具..."
echo "   Rust: $(rustc --version)"
echo "   Cargo: $(cargo --version)"
echo "   Node: $(node --version)"
echo "   npm: $(npm --version)"
echo ""

# 创建项目
PROJECT_DIR="tauri-app"

if [ -d "$PROJECT_DIR" ]; then
    echo "⚠️  目录 $PROJECT_DIR 已存在"
    read -p "是否删除并重建? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
    else
        echo "❌ 取消操作"
        exit 1
    fi
fi

echo "📦 创建 Tauri 项目..."
npm create tauri-app@latest "$PROJECT_DIR" -- \
    --manager npm \
    --ui react \
    --skip-git

cd "$PROJECT_DIR"

echo ""
echo "✅ 项目创建成功！"
echo ""
echo "📂 项目结构:"
echo "   $PROJECT_DIR/"
echo "   ├── src/           (React 前端)"
echo "   ├── src-tauri/     (Rust 后端)"
echo "   └── package.json   (npm 配置)"
echo ""
echo "🚀 后续命令:"
echo "   cd $PROJECT_DIR"
echo "   npm run dev        # 开发模式"
echo "   npm run build      # 生产构建"
echo ""

