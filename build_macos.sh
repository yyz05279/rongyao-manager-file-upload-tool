#!/bin/bash
# macOS打包脚本（修复版 - 解决闪退问题）

echo "===================================="
echo "熔盐管理文件上传工具 - macOS打包（修复版）"
echo "===================================="
echo ""

# 检查PyInstaller是否安装
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[错误] 未安装PyInstaller，正在安装..."
    pip3 install PyInstaller
fi

echo "[1/4] 清理旧的构建文件..."
rm -rf build dist "熔盐管理文件上传工具.spec"

echo "[2/4] 获取PyQt6插件路径..."
PYQT6_PATH=$(python3 -c "import PyQt6; import os; print(os.path.dirname(PyQt6.__file__))")
echo "PyQt6路径: $PYQT6_PATH"

echo "[3/4] 开始打包（使用--onefile模式）..."
pyinstaller \
    --name="熔盐管理文件上传工具" \
    --windowed \
    --onefile \
    --clean \
    --noconfirm \
    --add-data "parse_daily_report_excel.py:." \
    --add-data "convert_to_api_format.py:." \
    --hidden-import "PyQt6.QtCore" \
    --hidden-import "PyQt6.QtGui" \
    --hidden-import "PyQt6.QtWidgets" \
    --hidden-import "openpyxl" \
    --hidden-import "requests" \
    --exclude-module "PyQt6.Qt6" \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 打包失败！"
    exit 1
fi

echo "[4/4] 打包完成！"

echo ""
echo "===================================="
echo "打包成功！"
echo "应用程序位置：dist/熔盐管理文件上传工具.app"
echo "===================================="
echo ""
echo "测试运行："
echo "  open dist/熔盐管理文件上传工具.app"
echo ""
echo "如果仍有问题，请在终端直接运行查看错误："
echo "  dist/熔盐管理文件上传工具.app/Contents/MacOS/熔盐管理文件上传工具"
echo ""

