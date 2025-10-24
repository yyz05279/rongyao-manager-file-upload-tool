#!/bin/bash

# 🚀 Tauri 迁移启动脚本
# 这个脚本会自动检查环境并帮助你开始迁移

set -e

echo "═══════════════════════════════════════════════════════"
echo "🚀 Tauri 迁移启动向导"
echo "═══════════════════════════════════════════════════════"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Node.js
echo -e "${BLUE}[1/5]${NC} 检查 Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅${NC} Node.js 已安装: $NODE_VERSION"
else
    echo -e "${RED}❌${NC} Node.js 未安装"
    echo "请访问 https://nodejs.org 安装 Node.js 18+"
    exit 1
fi

# 检查 Rust
echo ""
echo -e "${BLUE}[2/5]${NC} 检查 Rust..."
if command -v rustc &> /dev/null; then
    RUST_VERSION=$(rustc --version)
    echo -e "${GREEN}✅${NC} Rust 已安装: $RUST_VERSION"
else
    echo -e "${YELLOW}⚠️${NC} Rust 未安装"
    echo ""
    echo "安装 Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
    echo -e "${GREEN}✅${NC} Rust 安装完成"
fi

# 检查 Tauri CLI
echo ""
echo -e "${BLUE}[3/5]${NC} 检查 Tauri CLI..."
if cargo tauri --version &> /dev/null 2>&1; then
    TAURI_VERSION=$(cargo tauri --version)
    echo -e "${GREEN}✅${NC} Tauri CLI 已安装: $TAURI_VERSION"
else
    echo -e "${YELLOW}⚠️${NC} Tauri CLI 未安装"
    echo "安装 Tauri CLI..."
    cargo install tauri-cli
    echo -e "${GREEN}✅${NC} Tauri CLI 安装完成"
fi

# 检查 npm 依赖
echo ""
echo -e "${BLUE}[4/5]${NC} 检查 npm 依赖..."
if [ -f "package.json" ]; then
    echo -e "${GREEN}✅${NC} 项目已初始化"
else
    echo -e "${YELLOW}⚠️${NC} 项目未初始化"
    echo "需要运行: cargo tauri init"
fi

# 总结
echo ""
echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}✅ 环境检查完成${NC}"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📖 后续步骤:"
echo ""
echo "1️⃣  如果还未初始化项目，运行:"
echo "   ${BLUE}cargo tauri init${NC}"
echo ""
echo "2️⃣  然后参考文档进行迁移:"
echo "   ${BLUE}TAURI_QUICKSTART.md${NC}     - 30 分钟快速上手"
echo "   ${BLUE}docs/Tauri迁移方案.md${NC}  - 详细迁移指南"
echo ""
echo "3️⃣  开发时运行:"
echo "   ${BLUE}cargo tauri dev${NC}"
echo ""
echo "4️⃣  生产打包:"
echo "   ${BLUE}cargo tauri build${NC}"
echo ""
echo "💡 需要帮助?"
echo "   查看: ${BLUE}README_TAURI.md${NC}"
echo ""

