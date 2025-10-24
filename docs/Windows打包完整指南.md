# 🪟 Windows 打包完整指南

> ⚠️ **重要提示**: 本文档仅适用于 **Windows 系统**。
>
> - 如果你在 **macOS** 上，请使用 `build_macos.sh` 脚本，详见 `docs/macOS打包完成总结.md`
> - 如果你在 **Linux** 上，请参考 PyInstaller 官方文档
>
> Windows 打包**必须在 Windows 系统上执行**，因为 PyInstaller 会根据当前操作系统生成对应平台的可执行文件。
> 在 macOS 上运行打包命令会生成 macOS 可执行文件，不会产生 .exe 文件。

## 📋 前提条件

### 1. 系统要求

- **操作系统**: Windows 7 或更高版本
- **Python 版本**: 3.9 或更高版本（推荐 3.10+）
- **磁盘空间**: 至少 2GB 可用空间

### 2. 依赖环境检查

在 PowerShell 或 CMD 中验证 Python 安装：

```bash
# 检查 Python 版本
python --version

# 检查 pip 是否可用
pip --version
```

## 🛠️ 快速打包步骤（推荐）

### 方案 A：使用现成脚本（最简单）

#### 步骤 1：在 Windows 资源管理器中打开项目目录

```
C:\Users\YourUsername\Desktop\熔盐管理文件上传工具
```

#### 步骤 2：双击运行打包脚本

找到 `build_windows.bat` 文件，双击运行。

该脚本会自动：

- ✅ 检查 PyInstaller 是否安装
- ✅ 自动安装缺失的依赖
- ✅ 清理旧的构建文件
- ✅ 开始打包
- ✅ 显示打包结果

#### 步骤 3：等待打包完成

```
====================================
打包成功！
可执行文件位置：dist\熔盐管理文件上传工具.exe
====================================
```

可执行文件已生成在 `dist\熔盐管理文件上传工具.exe`

---

### 方案 B：使用命令行（更灵活）

#### 步骤 1：打开 PowerShell 或 CMD

在项目目录中按 `Shift + 右键` → 选择"在此处打开 PowerShell 窗口"

#### 步骤 2：安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt

# 或手动安装
pip install PyQt6>=6.6.0
pip install requests>=2.31.0
pip install openpyxl>=3.1.0
pip install PyInstaller>=6.0.0
```

#### 步骤 3：执行打包命令

**简单打包（推荐）**：

```bash
pyinstaller --onefile --windowed --name="熔盐管理文件上传工具" main.py
```

**参数说明**：

- `--onefile` - 生成单个可执行文件（包含所有依赖）
- `--windowed` - 使用 GUI 模式（无命令行窗口）
- `--name="熔盐管理文件上传工具"` - 设置应用名称

#### 步骤 4：等待构建完成

打包过程通常需要 2-5 分钟，取决于电脑性能。

#### 步骤 5：验证输出

打包完成后，可执行文件位于：

```
dist\熔盐管理文件上传工具.exe
```

---

## 📁 打包后的文件结构

```
项目根目录/
├── dist/
│   ├── 熔盐管理文件上传工具.exe    ← 可执行文件（推荐分发这个）
│   └── ... （其他依赖文件）
├── build/
│   └── 熔盐管理文件上传工具/
│       └── ... （构建中间文件）
└── 熔盐管理文件上传工具.spec       ← PyInstaller 配置文件
```

## 🚀 运行打包后的程序

### 方式 1：双击运行（最简单）

直接在 `dist` 文件夹中双击 `熔盐管理文件上传工具.exe` 运行。

### 方式 2：从命令行运行

```bash
.\dist\熔盐管理文件上传工具.exe
```

### 方式 3：创建桌面快捷方式

1. 在 `dist\熔盐管理文件上传工具.exe` 上右键
2. 选择"创建快捷方式"
3. 移动快捷方式到桌面

---

## 🔧 高级配置

### 自定义打包（使用 .spec 文件）

项目中已有 `熔盐管理文件上传工具.spec` 文件，可自定义以下选项：

#### 1. 包含额外数据文件

```python
datas=[
    ('parse_daily_report_excel.py', '.'),
    ('convert_to_api_format.py', '.'),
    ('assets/', 'assets'),  # 添加 assets 文件夹
]
```

#### 2. 隐藏导入模块

已配置的模块：

```python
hiddenimports=[
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'openpyxl',
    'requests'
]
```

如需添加更多：

```python
hiddenimports=[
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'openpyxl',
    'requests',
    # 添加其他模块
    'your_module_name'
]
```

#### 3. 添加应用图标

```python
exe = EXE(
    # ... 其他参数
    icon='path/to/your/icon.ico',  # 指定 .ico 格式的图标
)
```

#### 4. 使用自定义 .spec 文件打包

```bash
pyinstaller 熔盐管理文件上传工具.spec
```

---

## ❌ 常见问题与解决方案

### 问题 1：打包失败 - "ModuleNotFoundError"

**原因**：模块未安装或隐藏导入配置不完整

**解决方案**：

```bash
# 1. 重新安装依赖
pip install -r requirements.txt

# 2. 检查是否安装了 PyInstaller
pip install PyInstaller>=6.0.0

# 3. 清理旧构建并重新打包
rmdir /s /q build
rmdir /s /q dist
pyinstaller --onefile --windowed --name="熔盐管理文件上传工具" main.py
```

### 问题 2：打包过程很慢

**原因**：第一次打包需要收集所有依赖和编译模块

**解决方案**：

- 关闭其他程序释放系统资源
- 使用 SSD 可加快打包速度
- 第一次打包后，后续会更快

### 问题 3：生成的 .exe 文件很大（>100MB）

**原因**：这是正常现象，PyQt6 和所有依赖都被打包进去了

**解决方案**：

- 如果需要更小的文件，可以使用压缩工具
- 或配置 UPX 压缩（在 .spec 文件中配置 `upx=True`）

### 问题 4：运行时找不到依赖文件

**原因**：打包脚本中的 `datas` 配置不完整

**解决方案**：
编辑 `.spec` 文件，确保所有需要的文件都在 `datas` 列表中：

```python
datas=[
    ('parse_daily_report_excel.py', '.'),
    ('convert_to_api_format.py', '.'),
    ('services/', 'services'),
    ('ui/', 'ui'),
]
```

---

## 📦 分发和部署

### 1. 生成版本号

编辑 `main.py` 添加版本信息：

```python
__version__ = "1.0.0"
__app_name__ = "熔盐管理文件上传工具"
```

### 2. 清理临时文件

```bash
rmdir /s /q build
del 熔盐管理文件上传工具.spec
```

### 3. 打包分发

只需要分发 `dist\熔盐管理文件上传工具.exe` 文件即可，无需其他依赖。

### 4. 创建安装程序（可选）

使用 NSIS 或 Inno Setup 创建 Windows 安装程序：

```bash
# 安装 NSIS 或 Inno Setup
# 创建 .iss 脚本文件并编译
```

---

## 🔍 验证打包结果

打包完成后，建议进行以下检查：

### 1. 检查可执行文件

```bash
# 检查文件大小和属性
dir dist\熔盐管理文件上传工具.exe

# 运行程序
.\dist\熔盐管理文件上传工具.exe
```

### 2. 测试功能

- ✅ 应用正常启动
- ✅ 登录界面显示正常
- ✅ 能够读取 Excel 文件
- ✅ 网络请求功能正常
- ✅ UI 响应速度满足预期

### 3. 检查错误日志

如果程序运行有问题，从命令行运行可以看到错误信息：

```bash
.\dist\熔盐管理文件上传工具.exe
```

---

## 📚 相关文件参考

| 文件名                      | 说明                   |
| --------------------------- | ---------------------- |
| `build_windows.bat`         | Windows 自动打包脚本   |
| `熔盐管理文件上传工具.spec` | PyInstaller 配置文件   |
| `requirements.txt`          | Python 依赖清单        |
| `main.py`                   | 应用主入口             |
| `build_macos.sh`            | macOS 打包脚本（参考） |

---

## 💡 打包优化建议

### 1. 减少文件大小

- 使用 `--onefile` 参数：单个可执行文件
- 启用 UPX 压缩：`upx=True`
- 排除不必要的模块

### 2. 提高启动速度

- 使用 `--optimize=2` 参数优化字节码
- 预编译常用模块

### 3. 增强安全性

- 考虑使用代码签名
- 添加版本信息和公司信息

---

## 🆘 故障排除详细流程

如果打包或运行出现问题，按照以下步骤排查：

```
1. 检查 Python 版本 → python --version
   ↓
2. 检查依赖安装 → pip list | grep PyQt6
   ↓
3. 测试应用运行 → python main.py
   ↓
4. 检查打包配置 → cat 熔盐管理文件上传工具.spec
   ↓
5. 清理并重新打包 → build_windows.bat
   ↓
6. 检查构建日志 → build\熔盐管理文件上传工具\build.log
```

---

## 📞 获取帮助

- 查看 [快速修复指南.md](./快速修复指南.md)
- 查看 [调试说明.md](./调试说明.md)
- 参考 [项目说明.md](./项目说明.md)

---

**最后更新**: 2025 年 10 月 24 日  
**适用版本**: PyInstaller 6.0+
