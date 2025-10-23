#!/bin/bash
# macOS调试版打包脚本（用于查看详细错误信息）

echo "===================================="
echo "熔盐管理文件上传工具 - macOS调试版打包"
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

echo "[2/3] 开始打包调试版（不使用--windowed，显示控制台）..."
pyinstaller \
    --name="熔盐管理文件上传工具" \
    --onedir \
    --clean \
    --noconfirm \
    --debug=all \
    --log-level=DEBUG \
    --add-data "parse_daily_report_excel.py:." \
    --add-data "convert_to_api_format.py:." \
    --hidden-import "PyQt6.QtCore" \
    --hidden-import "PyQt6.QtGui" \
    --hidden-import "PyQt6.QtWidgets" \
    --hidden-import "openpyxl" \
    --hidden-import "requests" \
    --collect-all PyQt6 \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 打包失败！"
    exit 1
fi

echo "[3/3] 打包完成！"

echo ""
echo "===================================="
echo "调试版打包成功！"
echo "===================================="
echo ""
echo "运行调试版（会显示所有错误信息）："
echo "  ./dist/熔盐管理文件上传工具/熔盐管理文件上传工具"
echo ""
echo "或者："
echo "  cd dist/熔盐管理文件上传工具"
echo "  ./熔盐管理文件上传工具"
echo ""

