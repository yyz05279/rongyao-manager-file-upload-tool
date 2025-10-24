# 打包后应用闪退问题 - 调试指南

## 🔍 问题现象

打包后的.app 应用一闪就退出，页面都看不到。

## 🎯 解决方案

### 方案一：使用打包脚本（推荐）

```bash
chmod +x build_macos.sh
./build_macos.sh
```

**打包特点：**

1. ✅ 改用`--onedir`模式（更稳定）
2. ✅ 添加了所有必要的 Qt 插件
3. ✅ 使用`--collect-all PyQt6`确保所有依赖
4. ✅ main.py 中添加了错误捕获机制
5. ✅ 添加了插件路径设置

### 方案二：使用调试版查看错误（排查问题）

```bash
chmod +x build_macos_debug.sh
./build_macos_debug.sh

# 运行调试版，会显示所有错误信息
./dist/熔盐管理文件上传工具/熔盐管理文件上传工具
```

## 📋 常见原因和解决方法

### 1. 缺少 Qt 平台插件 ❌

**现象：** 提示找不到 Qt 平台插件

**解决：**

```bash
# 使用--collect-all参数
pyinstaller --collect-all PyQt6 main.py
```

### 2. --onefile 模式问题 ❌

**现象：** 使用--onefile 打包后闪退

**解决：** 改用--onedir 模式（已在修复版脚本中使用）

```bash
pyinstaller --onedir --windowed main.py
```

### 3. 未捕获的异常 ❌

**现象：** 程序遇到错误直接退出

**解决：** 已在 main.py 中添加异常捕获（见修复版）

### 4. 缺少执行权限 ❌

**解决：**

```bash
chmod +x dist/熔盐管理文件上传工具.app/Contents/MacOS/熔盐管理文件上传工具
```

### 5. macOS 安全限制 ❌

**解决：**

```bash
# 移除隔离属性
xattr -cr "dist/熔盐管理文件上传工具.app"

# 或在系统偏好设置中允许
# 系统偏好设置 -> 安全性与隐私 -> 通用 -> 仍要打开
```

## 🔧 调试步骤

### 第 1 步：尝试修复版打包

```bash
./build_macos_fixed.sh
open dist/熔盐管理文件上传工具.app
```

### 第 2 步：如果还是失败，运行调试版

```bash
./build_macos_debug.sh
./dist/熔盐管理文件上传工具/熔盐管理文件上传工具
```

查看控制台输出的错误信息。

### 第 3 步：直接在终端运行.app

```bash
# 查看详细错误
dist/熔盐管理文件上传工具.app/Contents/MacOS/熔盐管理文件上传工具
```

### 第 4 步：检查依赖

```bash
# 检查PyQt6是否正确安装
python3 -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"

# 检查openpyxl
python3 -c "import openpyxl; print('openpyxl OK')"

# 检查requests
python3 -c "import requests; print('requests OK')"
```

## 📝 打包参数说明

### 推荐配置

```bash
pyinstaller \
    --name="熔盐管理文件上传工具" \
    --windowed \              # GUI模式，不显示终端
    --onedir \                # 打包为文件夹（更稳定）
    --clean \                 # 清理缓存
    --noconfirm \            # 不询问，直接覆盖
    --collect-all PyQt6 \    # 收集所有PyQt6文件
    --hidden-import openpyxl \
    --hidden-import requests \
    main.py
```

### 调试配置

```bash
pyinstaller \
    --name="熔盐管理文件上传工具" \
    --onedir \                # 打包为文件夹
    --debug=all \            # 启用所有调试信息
    --log-level=DEBUG \      # 详细日志
    --collect-all PyQt6 \
    main.py
```

## 🎯 最佳实践

### 开发阶段

1. 始终在虚拟环境中开发
2. 只安装必要的依赖
3. 定期测试打包

### 打包阶段

1. 优先使用`--onedir`模式
2. 使用`--collect-all`收集框架文件
3. 添加必要的`--hidden-import`
4. 先打包调试版测试

### 发布阶段

1. 测试打包后的应用
2. 在干净的 macOS 系统上测试
3. 检查所有功能是否正常
4. 处理 macOS 安全限制

## 🆘 还是无法解决？

### 查看详细日志

```bash
# 运行时会输出详细信息
./dist/熔盐管理文件上传工具.app/Contents/MacOS/熔盐管理文件上传工具 2>&1 | tee debug.log
```

### 检查.spec 文件

打包后会生成.spec 文件，可以手动编辑后再打包：

```bash
# 编辑.spec文件
vi 熔盐管理文件上传工具.spec

# 使用.spec文件打包
pyinstaller 熔盐管理文件上传工具.spec
```

### 联系支持

如果以上方法都无法解决，请提供：

1. 调试版的完整输出
2. Python 版本
3. PyQt6 版本
4. macOS 版本

```bash
# 收集系统信息
python3 --version
pip3 show PyQt6
sw_vers
```

## 📚 参考资料

- [PyQt6 MySQL 应用 PyInstaller 打包崩溃终极排查](https://www.bytezonex.com/archives/YIbPHCxo.html)
- [PyInstaller 官方文档](https://pyinstaller.org/)
- [PyQt6 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)

---

**快速修复命令：**

```bash
# 1. 使用打包脚本
./build_macos.sh

# 2. 如果失败，查看详细错误
./build_macos_debug.sh
./dist/熔盐管理文件上传工具/熔盐管理文件上传工具
```
