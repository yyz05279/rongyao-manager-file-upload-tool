#!/bin/bash
# macOS打包脚本

echo "===================================="
echo "熔盐管理文件上传工具 - macOS打包"
echo "===================================="
echo ""

# 检查PyInstaller是否安装
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[错误] 未安装PyInstaller，正在安装..."
    pip3 install PyInstaller
fi

echo "[1/3] 清理旧的构建文件..."
rm -rf build dist "熔盐管理文件上传工具.spec"

echo "[2/3] 开始打包..."
pyinstaller --onefile \
    --windowed \
    --name="熔盐管理文件上传工具" \
    --clean \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 打包失败！"
    exit 1
fi

echo "[3/3] 打包完成！"

echo ""
echo "===================================="
echo "打包成功！"
echo "应用程序位置：dist/熔盐管理文件上传工具.app"
echo "===================================="
echo ""

# 提示如何运行
echo "运行方式："
echo "1. 双击 dist/熔盐管理文件上传工具.app"
echo "2. 或执行：open dist/熔盐管理文件上传工具.app"
echo ""

