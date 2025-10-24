# 🚀 Windows 打包快速参考卡片

> ⚠️ **重要提示**: 本文档仅适用于 **Windows 系统**。
> 如果你在 macOS 上，请参考 `docs/macOS打包完成总结.md`

## 5 秒快速打包

**方式 1：最简单（推荐）**

```
双击 build_windows.bat
完成！
```

**方式 2：命令行**

```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name="熔盐管理文件上传工具" main.py
```

---

## 关键信息速查表

| 项目            | 说明                            |
| --------------- | ------------------------------- |
| **工作目录**    | 项目根目录                      |
| **打包脚本**    | `build_windows.bat`             |
| **输出位置**    | `dist\熔盐管理文件上传工具.exe` |
| **打包时间**    | 2-5 分钟                        |
| **文件大小**    | ~100-150 MB                     |
| **Python 版本** | 3.9+                            |
| **依赖管理**    | `requirements.txt`              |

---

## 常见命令速查

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 简单打包
pyinstaller --onefile --windowed --name="熔盐管理文件上传工具" main.py

# 3. 使用配置文件打包
pyinstaller 熔盐管理文件上传工具.spec

# 4. 清理构建文件
rmdir /s /q build dist
del 熔盐管理文件上传工具.spec

# 5. 运行程序
.\dist\熔盐管理文件上传工具.exe
```

---

## PyInstaller 参数速查

| 参数              | 说明                     |
| ----------------- | ------------------------ |
| `--onefile`       | 单个可执行文件           |
| `--windowed`      | GUI 模式（无命令行窗口） |
| `--name="APP名"`  | 设置应用名称             |
| `--icon=path.ico` | 添加应用图标             |
| `--add-data`      | 包含数据文件             |
| `--hidden-import` | 隐藏导入模块             |

---

## 常见问题速查

### ❌ 问题 1：ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### ❌ 问题 2：PyInstaller 未安装

```bash
pip install PyInstaller>=6.0.0
```

### ❌ 问题 3：打包失败

```bash
rmdir /s /q build dist
pyinstaller --onefile --windowed --name="熔盐管理文件上传工具" main.py
```

### ❌ 问题 4：.exe 文件过大

正常现象，PyQt6 依赖库大。可启用 UPX 压缩或接受现状。

---

## 必要文件检查清单

- ✅ `main.py` - 主入口文件
- ✅ `requirements.txt` - 依赖清单
- ✅ `熔盐管理文件上传工具.spec` - 打包配置（可选）
- ✅ `build_windows.bat` - 快速打包脚本
- ✅ `services/` 文件夹 - 业务逻辑
- ✅ `ui/` 文件夹 - 界面文件

---

## 环境检查命令

```bash
# 检查 Python
python --version

# 检查 pip
pip --version

# 检查依赖安装
pip list | findstr PyQt6

# 检查 PyInstaller
pip list | findstr PyInstaller
```

---

## 分发清单

打包完成后，只需分发：

- ✅ `dist\熔盐管理文件上传工具.exe`

无需分发：

- ❌ build 文件夹
- ❌ .spec 文件
- ❌ 源代码
- ❌ 其他临时文件

---

## 详细文档

查看完整指南：📖 [Windows 打包完整指南.md](./Windows打包完整指南.md)

---

**快速导航**

- [项目说明](./项目说明.md)
- [快速修复指南](./快速修复指南.md)
- [调试说明](./调试说明.md)
- [目录索引](./目录索引.md)

---

**最后更新**: 2025 年 10 月 24 日
