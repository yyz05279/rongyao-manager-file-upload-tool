@echo off
REM Windows打包脚本

echo ====================================
echo 熔盐管理文件上传工具 - Windows打包
echo ====================================
echo.

REM 检查PyInstaller是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] 未安装PyInstaller，正在安装...
    pip install PyInstaller
)

echo [1/3] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "熔盐管理文件上传工具.spec" del "熔盐管理文件上传工具.spec"

echo [2/3] 开始打包...
pyinstaller --onefile ^
    --windowed ^
    --name="熔盐管理文件上传工具" ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo [3/3] 打包完成！

echo.
echo ====================================
echo 打包成功！
echo 可执行文件位置：dist\熔盐管理文件上传工具.exe
echo ====================================
echo.

pause

