# ⚡ 闪退问题快速修复

## 🎯 问题：打包后应用一闪就退出

### 立即修复（2 分钟）

```bash
# 1. 进入项目目录
cd "/Users/yyz/Desktop/熔盐管理文件上传工具"

# 2. 使用打包脚本
./build_macos.sh

# 3. 运行应用
open dist/熔盐管理文件上传工具.app
```

## 🔍 如果还是失败，查看错误信息

```bash
# 运行调试版（会显示详细错误）
./build_macos_debug.sh
./dist/熔盐管理文件上传工具/熔盐管理文件上传工具
```

## 📋 核心文件

| 文件                     | 说明                      |
| ------------------------ | ------------------------- |
| **build_macos.sh**       | ✅ 打包脚本（已优化稳定） |
| **build_macos_debug.sh** | 🔍 调试版打包脚本         |
| **main.py**              | ✅ 添加了完整的错误捕获   |

## 📋 修复了什么？

### 1. ✅ main.py - 添加了完整的错误捕获

```python
# 现在会捕获所有异常并显示详细错误
try:
    # 应用启动代码
    ...
except Exception as e:
    # 显示错误对话框
    QMessageBox.critical(None, "启动错误", f"详细错误：{e}")
```

### 2. ✅ 设置了 Qt 插件路径

```python
# 解决打包后找不到Qt插件的问题
if hasattr(sys, '_MEIPASS'):
    plugin_path = os.path.join(sys._MEIPASS, 'PyQt6', 'Qt6', 'plugins')
    app.addLibraryPath(plugin_path)
```

### 3. ✅ 改进了打包参数

```bash
# 使用更稳定的打包方式
--onedir              # 改用文件夹模式（不用--onefile）
--collect-all PyQt6   # 收集所有PyQt6文件
```

## 🆘 常见问题

### Q: 还是看不到错误信息？

**A**: 在终端直接运行.app 内的可执行文件：

```bash
dist/熔盐管理文件上传工具.app/Contents/MacOS/熔盐管理文件上传工具
```

### Q: 提示"无法打开应用"？

**A**: 移除 macOS 的安全限制：

```bash
xattr -cr "dist/熔盐管理文件上传工具.app"
```

### Q: 提示找不到 Qt 平台插件？

**A**: 已在修复版脚本中解决，使用`--collect-all PyQt6`

### Q: 想要单个文件而不是文件夹？

**A**: 先确保--onedir 版本能正常运行，再尝试--onefile：

```bash
# 修改 build_macos_fixed.sh 中的 --onedir 为 --onefile
# 但注意：--onefile 可能不稳定
```

## 📊 对比：修复前 vs 修复后

| 项目     | 修复前      | 修复后             |
| -------- | ----------- | ------------------ |
| 打包模式 | --onefile   | --onedir（更稳定） |
| Qt 插件  | ❌ 可能缺失 | ✅ 完整收集        |
| 错误捕获 | ❌ 没有     | ✅ 完整捕获        |
| 插件路径 | ❌ 未设置   | ✅ 自动设置        |
| 调试模式 | ❌ 没有     | ✅ 提供调试版      |

## 🎯 测试步骤

### 1. 测试打包

```bash
./build_macos.sh
open dist/熔盐管理文件上传工具.app
```

✅ 应该能看到登录界面

### 2. 测试功能

- [ ] 登录功能正常
- [ ] 文件选择正常
- [ ] 上传功能正常

### 3. 如果还有问题

```bash
# 查看完整错误
./build_macos_debug.sh
./dist/熔盐管理文件上传工具/熔盐管理文件上传工具 2>&1 | tee error.log
```

然后查看`error.log`文件。

## 📚 详细文档

- [完整调试指南](DEBUG.md) - 所有解决方案
- [README](README.md) - 使用说明
- [架构文档](ARCHITECTURE.md) - 技术细节

## 💡 核心原因分析

根据 Context7 搜索结果，PyQt6 打包后闪退的三大原因：

1. **缺少 Qt 平台插件**

   - 解决：使用`--collect-all PyQt6`

2. **未捕获的异常**

   - 解决：在 main.py 添加 try-except

3. **--onefile 模式不稳定**
   - 解决：改用--onedir 模式

---

**现在就试试吧！** 🚀

```bash
./build_macos.sh
```
