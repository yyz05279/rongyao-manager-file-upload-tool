#!/bin/bash
# 一键安装脚本（macOS/Linux）

echo "===================================="
echo "熔盐管理文件上传工具 - 自动安装"
echo "===================================="
echo ""

# 检查Python版本
echo "[1/4] 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ 找到Python版本: $PYTHON_VERSION"
else
    echo "✗ 未找到Python3，请先安装Python 3.8或更高版本"
    echo "访问：https://www.python.org/downloads/"
    exit 1
fi

# 检查pip
echo ""
echo "[2/4] 检查pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    echo "✓ 找到pip版本: $PIP_VERSION"
else
    echo "✗ 未找到pip3，正在安装..."
    python3 -m ensurepip --upgrade
fi

# 升级pip
echo ""
echo "[3/4] 升级pip到最新版本..."
pip3 install --upgrade pip

# 安装依赖
echo ""
echo "[4/4] 安装项目依赖..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "===================================="
    echo "✓ 安装成功！"
    echo "===================================="
    echo ""
    echo "运行程序："
    echo "  python3 main.py"
    echo ""
    echo "打包程序："
    echo "  ./build_macos.sh"
    echo ""
else
    echo ""
    echo "✗ 安装失败，请检查错误信息"
    exit 1
fi

