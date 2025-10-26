@echo off
REM 一键安装脚本（Windows）

echo ====================================
echo 熔盐管理文件上传工具 - 自动安装
echo ====================================
echo.

REM 检查Python
echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8或更高版本
    echo 访问：https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [成功] 找到Python版本: %PYTHON_VERSION%

REM 检查pip
echo.
echo [2/4] 检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到pip，正在安装...
    python -m ensurepip --upgrade
)

for /f "tokens=2" %%i in ('pip --version') do set PIP_VERSION=%%i
echo [成功] 找到pip版本: %PIP_VERSION%

REM 升级pip
echo.
echo [3/4] 升级pip到最新版本...
python -m pip install --upgrade pip

REM 安装依赖
echo.
echo [4/4] 安装项目依赖...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [错误] 安装失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ====================================
echo [成功] 安装成功！
echo ====================================
echo.
echo 运行程序：
echo   python main.py
echo.
echo 打包程序：
echo   build_windows.bat
echo.
pause

