# 熔盐管理文件上传工具 - Python 版本

> 基于 PyQt5 的传统桌面应用

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
python main.py
```

---

## 📦 项目结构

```
python-app/
├── main.py                         # 应用入口
├── ui/                             # PyQt5 界面层
│   ├── main_window.py              # 主窗口
│   ├── login_widget.py             # 登录界面
│   └── upload_widget.py            # 上传界面
├── services/                       # 服务层
│   ├── auth_service.py             # 认证服务
│   ├── project_service.py          # 项目服务
│   └── upload_service.py           # 上传服务
├── requirements.txt                # Python 依赖
└── 熔盐管理文件上传工具.spec       # 打包配置
```

---

## ✨ 主要功能

- ✅ 用户登录认证
- ✅ Token 自动刷新
- ✅ 项目选择
- ✅ Excel 文件解析
- ✅ 数据预览
- ✅ 批量上传
- ✅ 进度显示
- ✅ 覆盖选项

---

## 🔧 技术栈

- **界面框架**: PyQt5
- **HTTP 客户端**: requests
- **Excel 解析**: openpyxl + pandas
- **打包工具**: PyInstaller

---

## 🛠️ 开发命令

### 运行应用

```bash
# 直接运行
python main.py

# 或使用脚本（macOS）
./run_macos.sh
```

### 打包应用

#### macOS

```bash
# 标准打包
./build_macos.sh

# 调试打包
./build_macos_debug.sh

# 手动打包
pyinstaller 熔盐管理文件上传工具.spec
```

#### Windows

```bash
# 使用批处理脚本
build_windows.bat

# 手动打包
pyinstaller 熔盐管理文件上传工具.spec
```

---

## 📋 依赖管理

### 安装依赖

```bash
# macOS
./install.sh

# Windows
install.bat

# 或手动安装
pip install -r requirements.txt
```

### 更新依赖列表

```bash
pip freeze > requirements.txt
```

---

## 🐛 常见问题

### 运行问题

**问题：导入错误**

```bash
# 解决方案
pip install -r requirements.txt
```

**问题：PyQt5 错误**

```bash
# macOS
brew install qt@5
pip uninstall PyQt5
pip install PyQt5

# Windows
# 确保安装了 VC++ 运行库
pip install --upgrade PyQt5
```

### 打包问题

**问题：打包失败**

```bash
# 清理后重新打包
rm -rf build dist
pyinstaller --clean 熔盐管理文件上传工具.spec
```

**问题：打包后无法运行**

- 检查 spec 文件中的资源路径
- 确保所有依赖都在 hiddenimports 中
- 查看日志文件获取错误信息

---

## 📝 开发指南

### 1. 代码结构

- `main.py` - 应用入口，创建主窗口
- `ui/main_window.py` - 主窗口，管理界面切换
- `ui/login_widget.py` - 登录界面
- `ui/upload_widget.py` - 上传界面
- `services/` - 所有业务逻辑

### 2. 添加新功能

1. 在 `services/` 中添加新的服务类
2. 在 `ui/` 中添加新的界面组件
3. 在 `main_window.py` 中集成新组件

### 3. 调试技巧

```python
# 添加调试日志
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 在代码中使用
logger.debug('调试信息')
logger.info('普通信息')
logger.error('错误信息')
```

---

## 🔄 与 Tauri 版本的差异

| 特性         | Python 版本   | Tauri 版本          |
| ------------ | ------------- | ------------------- |
| **界面**     | PyQt5 原生    | Web 界面            |
| **性能**     | 中等          | 优秀                |
| **体积**     | ~50MB+        | ~5MB                |
| **开发效率** | 快速          | 需要学习 Rust       |
| **跨平台**   | Windows/macOS | Windows/macOS/Linux |

---

## 📖 参考文档

- **[PYTHON_PROJECT_STRUCTURE.md](../PYTHON_PROJECT_STRUCTURE.md)** - 详细项目结构
- **[项目结构说明.md](../项目结构说明.md)** - 整体架构说明
- **[INDEX.md](../INDEX.md)** - 完整文档索引

---

## 🔗 相关链接

- [PyQt5 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [PyInstaller 文档](https://pyinstaller.readthedocs.io/)
- [pandas 文档](https://pandas.pydata.org/)

---

## 📄 许可证

本项目仅供内部使用。

---

**最后更新**: 2025 年 10 月 26 日  
**版本**: v2.0  
**状态**: 🟢 可运行

---

**返回**: [项目根目录](../) | [Tauri 版本](../tauri-app/)
